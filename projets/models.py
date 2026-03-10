from django.db import models
from django.utils.text import slugify


class ProjetCommunautaire(models.Model):
    STATUT_CHOIX = [
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('refuse', 'Refusé'),
    ]
    auteur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE, related_name='projets')
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    technologies = models.CharField(max_length=500, help_text='Technologies séparées par des virgules')
    lien_projet = models.URLField(blank=True, default='')
    lien_github = models.URLField(blank=True, default='')
    capture_url = models.URLField(blank=True, default='', help_text="URL de la capture d'écran")
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='en_attente')
    nb_likes = models.IntegerField(default=0)
    date_soumission = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Projet communautaire'
        verbose_name_plural = 'Projets communautaires'
        ordering = ['-date_soumission']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def liste_technologies(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def mettre_a_jour_likes(self):
        self.nb_likes = self.likes.count()
        self.save(update_fields=['nb_likes'])


class Like(models.Model):
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE, related_name='likes')
    projet = models.ForeignKey(ProjetCommunautaire, on_delete=models.CASCADE, related_name='likes')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ['utilisateur', 'projet']

    def __str__(self):
        return f'{self.utilisateur} ❤ {self.projet}'
