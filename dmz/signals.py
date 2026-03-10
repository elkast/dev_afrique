from django.contrib.auth.signals import user_login_failed, user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .middleware import obtenir_ip_client

import logging
logger = logging.getLogger('dmz')


@receiver(user_login_failed)
def enregistrer_echec_connexion(sender, credentials, request, **kwargs):
    """Log every failed login attempt and auto-block after threshold."""
    if request is None:
        return

    ip = obtenir_ip_client(request)
    nom = credentials.get('username', '')[:150]

    try:
        from .models import TentativeConnexion, JournalSecurite, IPBloquee

        TentativeConnexion.objects.create(
            adresse_ip=ip,
            nom_utilisateur=nom,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            reussie=False,
            chemin=request.path[:500],
            referer=request.META.get('HTTP_REFERER', '')[:200],
        )

        # Count recent failures from this IP
        seuil = timezone.now() - timedelta(minutes=30)
        nb_echecs = TentativeConnexion.objects.filter(
            adresse_ip=ip, reussie=False, date__gte=seuil
        ).count()

        # Admin-specific blocking (3 attempts)
        if '/administration/' in request.path:
            from .models import TentativeAdmin
            TentativeAdmin.objects.create(
                adresse_ip=ip,
                nom_utilisateur=nom,
                reussie=False,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            )
            nb_admin = TentativeAdmin.objects.filter(
                adresse_ip=ip, reussie=False, date__gte=seuil
            ).count()
            if nb_admin >= 3:
                IPBloquee.objects.update_or_create(
                    adresse_ip=ip,
                    defaults={
                        'raison': 'admin_brute',
                        'details': f'3+ tentatives admin échouées pour: {nom}',
                        'est_actif': True,
                        'date_expiration': timezone.now() + timedelta(hours=6),
                        'nombre_tentatives': nb_admin,
                    }
                )
                JournalSecurite.objects.create(
                    type_evenement='admin_bloque',
                    niveau='critique',
                    adresse_ip=ip,
                    nom_utilisateur=nom,
                    description=f'IP bloquée: {nb_admin} tentatives admin échouées',
                )

        # General brute force detection (10 attempts)
        if nb_echecs >= 10:
            IPBloquee.objects.update_or_create(
                adresse_ip=ip,
                defaults={
                    'raison': 'brute_force',
                    'details': f'{nb_echecs} tentatives échouées en 30 min',
                    'est_actif': True,
                    'date_expiration': timezone.now() + timedelta(hours=2),
                    'nombre_tentatives': nb_echecs,
                }
            )
            JournalSecurite.objects.create(
                type_evenement='brute_force',
                niveau='critique',
                adresse_ip=ip,
                nom_utilisateur=nom,
                description=f'Brute force détecté: {nb_echecs} tentatives en 30 min',
            )
        elif nb_echecs >= 5:
            JournalSecurite.objects.create(
                type_evenement='login_echoue',
                niveau='warning',
                adresse_ip=ip,
                nom_utilisateur=nom,
                description=f'Multiples échecs: {nb_echecs} tentatives depuis {ip}',
            )
    except Exception as e:
        logger.error(f'Erreur enregistrement échec connexion: {e}')


@receiver(user_logged_in)
def enregistrer_connexion_reussie(sender, user, request, **kwargs):
    """Log successful logins."""
    if request is None:
        return

    ip = obtenir_ip_client(request)
    try:
        from .models import TentativeConnexion
        TentativeConnexion.objects.create(
            adresse_ip=ip,
            nom_utilisateur=user.username,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            reussie=True,
            chemin=request.path[:500],
        )
    except Exception as e:
        logger.error(f'Erreur enregistrement connexion: {e}')
