from django.db import models
from django.utils.text import slugify
import uuid


class Parcours(models.Model):
    TYPE_CHOIX = [
        ('web', 'Développement Web'),
        ('mobile', 'Développement Mobile'),
        ('data', 'Data & IA'),
        ('devops', 'DevOps & Cloud'),
        ('design', 'Design & UI/UX'),
        ('autre', 'Autre'),
    ]
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    type_parcours = models.CharField(max_length=20, choices=TYPE_CHOIX)
    icone = models.CharField(max_length=50, default='🌐')
    image_url = models.URLField(blank=True, default='')
    ordre = models.IntegerField(default=0)
    est_publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Parcours'
        verbose_name_plural = 'Parcours'
        ordering = ['ordre']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def nombre_cours(self):
        return self.cours_set.filter(est_publie=True).count()


class Cours(models.Model):
    NIVEAU_CHOIX = [
        ('debutant', '🌱 Débutant'),
        ('intermediaire', '🌿 Intermédiaire'),
        ('avance', '🌳 Avancé'),
    ]
    STATUT_CHOIX = [
        ('brouillon', 'Brouillon'),
        ('en_attente', 'En attente de validation'),
        ('publie', 'Publié'),
        ('refuse', 'Refusé'),
    ]
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    icone = models.CharField(max_length=50, default='📘')
    image_url = models.URLField(blank=True, default='')
    auteur = models.ForeignKey(
        'utilisateurs.Utilisateur', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='cours_crees'
    )
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOIX, default='debutant')
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='publie')
    ordre = models.IntegerField(default=0)
    est_publie = models.BooleanField(default=True)
    nb_vues = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'
        ordering = ['ordre']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def nombre_lecons(self):
        return self.lecon_set.filter(est_publie=True).count()

    def premiere_lecon(self):
        return self.lecon_set.filter(est_publie=True).first()

    def duree_totale(self):
        total = self.lecon_set.filter(est_publie=True).aggregate(
            total=models.Sum('duree_minutes')
        )['total']
        return total or 0


class Lecon(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    contenu = models.TextField(help_text='Contenu HTML de la leçon')
    ordre = models.IntegerField(default=0)
    duree_minutes = models.IntegerField(default=10, help_text='Durée estimée en minutes')
    est_publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Leçon'
        verbose_name_plural = 'Leçons'
        ordering = ['ordre']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def lecon_suivante(self):
        return Lecon.objects.filter(
            cours=self.cours, ordre__gt=self.ordre, est_publie=True
        ).first()

    def lecon_precedente(self):
        return Lecon.objects.filter(
            cours=self.cours, ordre__lt=self.ordre, est_publie=True
        ).last()


class ProgressionUtilisateur(models.Model):
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE)
    lecon = models.ForeignKey(Lecon, on_delete=models.CASCADE)
    terminee = models.BooleanField(default=False)
    date_completion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Progression'
        verbose_name_plural = 'Progressions'
        unique_together = ['utilisateur', 'lecon']

    def __str__(self):
        statut = '✅' if self.terminee else '⏳'
        return f'{self.utilisateur} - {self.lecon} {statut}'


class Certificat(models.Model):
    utilisateur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE, related_name='certificats')
    parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE)
    code_unique = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    date_obtention = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Certificat'
        verbose_name_plural = 'Certificats'
        unique_together = ['utilisateur', 'parcours']

    def __str__(self):
        return f'Certificat {self.utilisateur} — {self.parcours}'


class Commentaire(models.Model):
    auteur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE, related_name='commentaires')
    contenu = models.TextField()
    lecon = models.ForeignKey(Lecon, on_delete=models.CASCADE, null=True, blank=True, related_name='commentaires')
    projet = models.ForeignKey('projets.ProjetCommunautaire', on_delete=models.CASCADE, null=True, blank=True, related_name='commentaires')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reponses')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        ordering = ['date_creation']

    def __str__(self):
        return f'{self.auteur} — {self.contenu[:50]}'
