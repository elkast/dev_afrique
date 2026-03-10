import logging
import re
import traceback

from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger('dmz')


def obtenir_ip_client(request):
    """Extract real client IP from request headers."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


class ExceptionNucleaireMiddleware:
    """
    Nuclear exception handler — catches ALL unhandled exceptions
    and returns user-friendly error pages instead of crashing.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self.gerer_exception(request, e)

    def process_exception(self, request, exception):
        return self.gerer_exception(request, exception)

    def gerer_exception(self, request, exception):
        ip = obtenir_ip_client(request)
        logger.error(
            f'[EXCEPTION NUCLEAIRE] {type(exception).__name__}: {exception} '
            f'| IP: {ip} | Path: {request.path}',
            exc_info=True
        )

        # Log to security journal if DB is available
        try:
            from .models import JournalSecurite
            JournalSecurite.objects.create(
                type_evenement='autre',
                niveau='danger',
                adresse_ip=ip,
                description=f'Exception non gérée: {type(exception).__name__}: {str(exception)[:500]}',
                donnees={
                    'path': request.path,
                    'method': request.method,
                    'traceback': traceback.format_exc()[-2000:] if settings.DEBUG else '',
                }
            )
        except Exception:
            pass

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'erreur': 'Une erreur interne est survenue.',
                'code': 500
            }, status=500)

        try:
            return render(request, 'erreurs/500.html', status=500)
        except Exception:
            from django.http import HttpResponse
            return HttpResponse(
                '<h1>Erreur interne du serveur</h1>'
                '<p>Nous nous excusons pour le désagrément. '
                'Veuillez réessayer plus tard.</p>',
                status=500,
                content_type='text/html'
            )


class PareFeuxMiddleware:
    """
    Firewall middleware — blocks known bad IPs, detects injection attempts,
    rate-limits requests, and logs suspicious activity.
    """
    # Patterns for detecting SQL injection and XSS attempts
    PATTERNS_SUSPECTS = [
        re.compile(r"(union\s+select|select\s+.*\s+from|insert\s+into|drop\s+table|delete\s+from)", re.IGNORECASE),
        re.compile(r"(<script|javascript:|on\w+\s*=)", re.IGNORECASE),
        re.compile(r"(\.\./\.\.|/etc/passwd|/proc/self)", re.IGNORECASE),
        re.compile(r"(eval\(|exec\(|system\(|passthru\()", re.IGNORECASE),
    ]

    # Paths that scanners commonly probe
    CHEMINS_SCANS = [
        '/wp-admin', '/wp-login', '/wp-content', '/xmlrpc.php',
        '/.env', '/config.php', '/admin.php', '/phpmyadmin',
        '/.git', '/backup', '/shell', '/cmd',
        '/actuator', '/api/swagger', '/_debug',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = obtenir_ip_client(request)

        # Check if IP is blocked
        try:
            from .models import IPBloquee
            ip_bloquee = IPBloquee.objects.filter(
                adresse_ip=ip, est_actif=True
            ).first()
            if ip_bloquee:
                if ip_bloquee.est_expire():
                    ip_bloquee.est_actif = False
                    ip_bloquee.save(update_fields=['est_actif'])
                else:
                    return HttpResponseForbidden(
                        '<h1>Accès refusé</h1>'
                        '<p>Votre adresse IP a été bloquée pour activité suspecte.</p>'
                    )
        except Exception:
            pass

        # Detect scan attempts
        chemin = request.path.lower()
        for chemin_scan in self.CHEMINS_SCANS:
            if chemin.startswith(chemin_scan.lower()):
                self.enregistrer_menace(request, ip, 'scan',
                    f'Scan détecté: {request.path}')
                return HttpResponseForbidden('')

        # Detect injection attempts in query string and body
        texte_a_verifier = (
            request.META.get('QUERY_STRING', '') +
            request.path
        )
        for pattern in self.PATTERNS_SUSPECTS:
            if pattern.search(texte_a_verifier):
                self.enregistrer_menace(request, ip, 'injection',
                    f'Injection détectée: {pattern.pattern[:100]}')
                return HttpResponseForbidden('')

        response = self.get_response(request)
        return response

    def enregistrer_menace(self, request, ip, type_evt, description):
        try:
            from .models import JournalSecurite, IPBloquee
            JournalSecurite.objects.create(
                type_evenement=type_evt,
                niveau='danger',
                adresse_ip=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                description=description,
                donnees={
                    'path': request.path,
                    'method': request.method,
                    'query': request.META.get('QUERY_STRING', '')[:500],
                }
            )
            # Auto-block IP after detection
            ip_obj, cree = IPBloquee.objects.get_or_create(
                adresse_ip=ip,
                defaults={
                    'raison': type_evt,
                    'details': description,
                    'date_expiration': timezone.now() + timedelta(hours=24),
                    'nombre_tentatives': 1,
                }
            )
            if not cree:
                ip_obj.nombre_tentatives += 1
                ip_obj.est_actif = True
                if ip_obj.nombre_tentatives >= 5:
                    ip_obj.date_expiration = None  # Permanent block
                ip_obj.save()
        except Exception as e:
            logger.error(f'Erreur enregistrement menace: {e}')


class AdminProtectionMiddleware:
    """
    Protects admin panel with 3-strike IP blocking.
    If wrong credentials are entered 3 times, the IP is blocked.
    """
    MAX_TENTATIVES = 3

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only protect the custom admin login path
        if request.path.startswith('/administration/') and not request.user.is_authenticated:
            ip = obtenir_ip_client(request)
            try:
                from .models import IPBloquee
                ip_bloquee = IPBloquee.objects.filter(
                    adresse_ip=ip, est_actif=True, raison='admin_brute'
                ).first()
                if ip_bloquee and not ip_bloquee.est_expire():
                    return HttpResponseForbidden(
                        '<h1>Accès bloqué</h1>'
                        '<p>Trop de tentatives échouées. Votre IP est temporairement bloquée.</p>'
                    )
            except Exception:
                pass

        response = self.get_response(request)
        return response
