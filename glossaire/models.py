from django.db import models
from django.utils.text import slugify


class TermeGlossaire(models.Model):
    CATEGORIE_CHOIX = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('mobile', 'Mobile'),
        ('base_donnees', 'Base de données'),
        ('devops', 'DevOps'),
        ('design', 'Design'),
        ('general', 'Général'),
        ('securite', 'Sécurité'),
        ('ia', 'Intelligence Artificielle'),
    ]
    terme = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    definition = models.TextField(help_text='Définition claire et simple')
    exemple_code = models.TextField(blank=True, default='', help_text='Exemple de code (optionnel)')
    langage_exemple = models.CharField(max_length=50, blank=True, default='', help_text='Langage de l\'exemple')
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOIX, default='general')
    lettre = models.CharField(max_length=1, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Terme du glossaire'
        verbose_name_plural = 'Termes du glossaire'
        ordering = ['terme']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.terme)
        self.lettre = self.terme[0].upper() if self.terme else ''
        super().save(*args, **kwargs)

    def __str__(self):
        return self.terme
