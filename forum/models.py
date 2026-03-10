from django.db import models
from django.utils.text import slugify


class SujetForum(models.Model):
    CATEGORIE_CHOIX = [
        ('html_css', 'HTML & CSS'),
        ('javascript', 'JavaScript'),
        ('python', 'Python'),
        ('django', 'Django'),
        ('react', 'React'),
        ('mobile', 'Mobile'),
        ('devops', 'DevOps'),
        ('general', 'Général'),
        ('projets', 'Aide projets'),
        ('emploi', 'Emploi & Carrière'),
    ]
    auteur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE, related_name='sujets_forum')
    titre = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=350)
    contenu = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOIX, default='general')
    est_resolu = models.BooleanField(default=False)
    est_epingle = models.BooleanField(default=False)
    nb_vues = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sujet du forum'
        verbose_name_plural = 'Sujets du forum'
        ordering = ['-est_epingle', '-date_creation']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)[:300]
            self.slug = base_slug
            n = 1
            while SujetForum.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{base_slug}-{n}'
                n += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def nombre_reponses(self):
        return self.reponses.count()


class ReponseForum(models.Model):
    sujet = models.ForeignKey(SujetForum, on_delete=models.CASCADE, related_name='reponses')
    auteur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE, related_name='reponses_forum')
    contenu = models.TextField()
    est_solution = models.BooleanField(default=False)
    nb_votes = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Réponse du forum'
        verbose_name_plural = 'Réponses du forum'
        ordering = ['-est_solution', '-nb_votes', 'date_creation']

    def __str__(self):
        return f'Réponse de {self.auteur} sur « {self.sujet.titre[:50]} »'
