from django.contrib.auth.models import AbstractUser
from django.db import models
import os


def chemin_avatar(instance, filename):
    """Generate unique path for avatar uploads."""
    ext = os.path.splitext(filename)[1].lower()
    return f'avatars/{instance.username}{ext}'


class Utilisateur(AbstractUser):
    ROLE_CHOIX = [
        ('apprenant', 'Apprenant'),
        ('formateur', 'Formateur'),
        ('moderateur', 'Modérateur'),
        ('administrateur', 'Administrateur'),
    ]
    NIVEAU_CHOIX = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOIX, default='apprenant')
    biographie = models.TextField(blank=True, default='')
    site_web = models.URLField(blank=True, default='')
    avatar_url = models.URLField(blank=True, default='')
    avatar = models.ImageField(upload_to=chemin_avatar, blank=True, null=True,
        help_text='Photo de profil (JPG, PNG, max 2 Mo)')
    pays = models.CharField(max_length=100, blank=True, default='')
    ville = models.CharField(max_length=100, blank=True, default='')
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOIX, default='debutant')
    points_xp = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.username

    def est_admin(self):
        return self.role == 'administrateur'

    def est_moderateur(self):
        return self.role in ('moderateur', 'administrateur')

    def est_formateur(self):
        return self.role in ('formateur', 'moderateur', 'administrateur')

    def ajouter_xp(self, points):
        self.points_xp += points
        # Mise à jour automatique du niveau
        if self.points_xp >= 5000:
            self.niveau = 'expert'
        elif self.points_xp >= 2000:
            self.niveau = 'avance'
        elif self.points_xp >= 500:
            self.niveau = 'intermediaire'
        self.save(update_fields=['points_xp', 'niveau'])

    def get_avatar_display(self):
        if self.avatar:
            return self.avatar.url
        if self.avatar_url:
            return self.avatar_url
        return f"https://i.pravatar.cc/150?u={self.username}"

    def get_niveau_display_icon(self):
        icons = {
            'debutant': '🌱',
            'intermediaire': '🌿',
            'avance': '🌳',
            'expert': '⭐',
        }
        return icons.get(self.niveau, '🌱')
