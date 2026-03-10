from django.db import models


class Signalement(models.Model):
    TYPE_CONTENU_CHOIX = [
        ('cours', 'Cours'),
        ('lecon', 'Leçon'),
        ('projet', 'Projet'),
        ('commentaire', 'Commentaire'),
        ('sujet_forum', 'Sujet du forum'),
        ('reponse_forum', 'Réponse du forum'),
    ]
    RAISON_CHOIX = [
        ('fausse_info', 'Fausse information'),
        ('spam', 'Spam'),
        ('hors_sujet', 'Hors sujet'),
        ('inapproprie', 'Contenu inapproprié'),
        ('plagiat', 'Plagiat'),
        ('autre', 'Autre'),
    ]
    STATUT_CHOIX = [
        ('en_attente', 'En attente'),
        ('traite', 'Traité'),
        ('ignore', 'Ignoré'),
    ]
    signaleur = models.ForeignKey('utilisateurs.Utilisateur', on_delete=models.CASCADE, related_name='signalements_faits')
    type_contenu = models.CharField(max_length=20, choices=TYPE_CONTENU_CHOIX)
    id_contenu = models.IntegerField(help_text='ID de l\'objet signalé')
    raison = models.CharField(max_length=20, choices=RAISON_CHOIX)
    description = models.TextField(blank=True, default='')
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='en_attente')
    traite_par = models.ForeignKey(
        'utilisateurs.Utilisateur', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='signalements_traites'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'
        ordering = ['-date_creation']

    def __str__(self):
        return f'Signalement {self.type_contenu} #{self.id_contenu} — {self.get_raison_display()}'
