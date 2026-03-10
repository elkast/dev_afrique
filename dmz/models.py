from django.db import models
from django.utils import timezone


class TentativeConnexion(models.Model):
    """Tracks all login attempts for security monitoring."""
    adresse_ip = models.GenericIPAddressField(db_index=True)
    nom_utilisateur = models.CharField(max_length=150, blank=True, default='')
    user_agent = models.TextField(blank=True, default='')
    reussie = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    localisation = models.CharField(max_length=255, blank=True, default='')
    referer = models.URLField(blank=True, default='')
    chemin = models.CharField(max_length=500, blank=True, default='')

    class Meta:
        verbose_name = 'Tentative de connexion'
        verbose_name_plural = 'Tentatives de connexion'
        ordering = ['-date']

    def __str__(self):
        statut = '✅' if self.reussie else '❌'
        return f'{statut} {self.adresse_ip} — {self.nom_utilisateur} — {self.date}'


class IPBloquee(models.Model):
    """IPs blocked due to suspicious activity."""
    RAISON_CHOIX = [
        ('brute_force', 'Tentatives de brute force'),
        ('injection', 'Tentative d\'injection SQL/XSS'),
        ('scan', 'Scan de vulnérabilités'),
        ('spam', 'Spam'),
        ('manuelle', 'Blocage manuel'),
        ('admin_brute', 'Brute force admin'),
    ]
    adresse_ip = models.GenericIPAddressField(unique=True, db_index=True)
    raison = models.CharField(max_length=30, choices=RAISON_CHOIX)
    details = models.TextField(blank=True, default='')
    date_blocage = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField(null=True, blank=True,
        help_text='Laisser vide pour un blocage permanent')
    est_actif = models.BooleanField(default=True)
    nombre_tentatives = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'IP bloquée'
        verbose_name_plural = 'IPs bloquées'
        ordering = ['-date_blocage']

    def __str__(self):
        return f'🚫 {self.adresse_ip} — {self.get_raison_display()}'

    def est_expire(self):
        if self.date_expiration and timezone.now() > self.date_expiration:
            return True
        return False


class JournalSecurite(models.Model):
    """Security event log for monitoring threats."""
    NIVEAU_CHOIX = [
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('danger', 'Danger'),
        ('critique', 'Critique'),
    ]
    TYPE_CHOIX = [
        ('login_echoue', 'Connexion échouée'),
        ('brute_force', 'Brute force détecté'),
        ('ip_bloquee', 'IP bloquée'),
        ('injection', 'Tentative d\'injection'),
        ('acces_interdit', 'Accès interdit'),
        ('scan', 'Scan détecté'),
        ('admin_bloque', 'Admin bloqué'),
        ('fichier_suspect', 'Fichier suspect'),
        ('autre', 'Autre'),
    ]
    type_evenement = models.CharField(max_length=30, choices=TYPE_CHOIX)
    niveau = models.CharField(max_length=10, choices=NIVEAU_CHOIX, default='info')
    adresse_ip = models.GenericIPAddressField(blank=True, null=True)
    nom_utilisateur = models.CharField(max_length=150, blank=True, default='')
    user_agent = models.TextField(blank=True, default='')
    description = models.TextField()
    donnees = models.JSONField(default=dict, blank=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Journal de sécurité'
        verbose_name_plural = 'Journaux de sécurité'
        ordering = ['-date']

    def __str__(self):
        icones = {'info': 'ℹ️', 'warning': '⚠️', 'danger': '🔴', 'critique': '🚨'}
        return f'{icones.get(self.niveau, "ℹ️")} {self.get_type_evenement_display()} — {self.adresse_ip}'


class TentativeAdmin(models.Model):
    """Tracks admin panel login attempts with 3-strike blocking."""
    adresse_ip = models.GenericIPAddressField(db_index=True)
    nom_utilisateur = models.CharField(max_length=150)
    reussie = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Tentative admin'
        verbose_name_plural = 'Tentatives admin'
        ordering = ['-date']

    def __str__(self):
        statut = '✅' if self.reussie else '❌'
        return f'{statut} Admin: {self.nom_utilisateur} depuis {self.adresse_ip}'
