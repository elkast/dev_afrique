from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import timedelta
from administration.decorateurs import admin_requis
from .models import TentativeConnexion, IPBloquee, JournalSecurite, TentativeAdmin


@login_required
@admin_requis
def vue_tableau_dmz(request):
    """DMZ security dashboard."""
    maintenant = timezone.now()
    derniere_24h = maintenant - timedelta(hours=24)
    derniere_semaine = maintenant - timedelta(days=7)

    stats = {
        'tentatives_24h': TentativeConnexion.objects.filter(date__gte=derniere_24h).count(),
        'echecs_24h': TentativeConnexion.objects.filter(date__gte=derniere_24h, reussie=False).count(),
        'ips_bloquees': IPBloquee.objects.filter(est_actif=True).count(),
        'alertes_critiques': JournalSecurite.objects.filter(
            date__gte=derniere_semaine, niveau__in=['danger', 'critique']
        ).count(),
        'tentatives_admin': TentativeAdmin.objects.filter(
            date__gte=derniere_24h, reussie=False
        ).count(),
    }

    # Recent security events
    evenements_recents = JournalSecurite.objects.all()[:20]

    # Top attacking IPs
    top_ips = TentativeConnexion.objects.filter(
        reussie=False, date__gte=derniere_semaine
    ).values('adresse_ip').annotate(
        nb=Count('id')
    ).order_by('-nb')[:10]

    # Recent blocked IPs
    ips_bloquees = IPBloquee.objects.filter(est_actif=True)[:15]

    # Activity over last 7 days
    activite_jours = TentativeConnexion.objects.filter(
        date__gte=derniere_semaine
    ).annotate(
        jour=TruncDate('date')
    ).values('jour').annotate(
        total=Count('id'),
        echecs=Count('id', filter=Q(reussie=False)),
    ).order_by('jour')

    return render(request, 'dmz/tableau_dmz.html', {
        'stats': stats,
        'evenements_recents': evenements_recents,
        'top_ips': top_ips,
        'ips_bloquees': ips_bloquees,
        'activite_jours': list(activite_jours),
    })


@login_required
@admin_requis
def vue_journal_securite(request):
    """Full security event log."""
    niveau = request.GET.get('niveau', '')
    type_evt = request.GET.get('type', '')
    evenements = JournalSecurite.objects.all()
    if niveau:
        evenements = evenements.filter(niveau=niveau)
    if type_evt:
        evenements = evenements.filter(type_evenement=type_evt)

    paginator = Paginator(evenements, 30)
    page = request.GET.get('page')
    evenements = paginator.get_page(page)

    return render(request, 'dmz/journal.html', {
        'evenements': evenements,
        'niveau_filtre': niveau,
        'type_filtre': type_evt,
        'niveaux': JournalSecurite.NIVEAU_CHOIX,
        'types': JournalSecurite.TYPE_CHOIX,
    })


@login_required
@admin_requis
def vue_ips_bloquees(request):
    """List of blocked IPs with management."""
    ips = IPBloquee.objects.all()
    paginator = Paginator(ips, 30)
    page = request.GET.get('page')
    ips = paginator.get_page(page)
    return render(request, 'dmz/ips_bloquees.html', {'ips': ips})


@login_required
@admin_requis
def vue_debloquer_ip(request, pk):
    """Unblock an IP address."""
    ip = get_object_or_404(IPBloquee, pk=pk)
    if request.method == 'POST':
        ip.est_actif = False
        ip.save(update_fields=['est_actif'])
        JournalSecurite.objects.create(
            type_evenement='autre',
            niveau='info',
            adresse_ip=ip.adresse_ip,
            nom_utilisateur=request.user.username,
            description=f'IP débloquée manuellement par {request.user.username}',
        )
        messages.success(request, f'IP {ip.adresse_ip} débloquée.')
    return redirect('dmz_ips_bloquees')


@login_required
@admin_requis
def vue_bloquer_ip(request):
    """Manually block an IP."""
    if request.method == 'POST':
        ip = request.POST.get('adresse_ip', '').strip()
        raison = request.POST.get('raison', 'manuelle')
        details = request.POST.get('details', '')
        if ip:
            IPBloquee.objects.update_or_create(
                adresse_ip=ip,
                defaults={
                    'raison': raison,
                    'details': details,
                    'est_actif': True,
                }
            )
            JournalSecurite.objects.create(
                type_evenement='ip_bloquee',
                niveau='warning',
                adresse_ip=ip,
                nom_utilisateur=request.user.username,
                description=f'IP bloquée manuellement: {details}',
            )
            messages.success(request, f'IP {ip} bloquée.')
        else:
            messages.error(request, 'Adresse IP invalide.')
    return redirect('dmz_ips_bloquees')


@login_required
@admin_requis
def vue_tentatives_connexion(request):
    """View all login attempts."""
    statut = request.GET.get('statut', '')
    tentatives = TentativeConnexion.objects.all()
    if statut == 'echec':
        tentatives = tentatives.filter(reussie=False)
    elif statut == 'reussi':
        tentatives = tentatives.filter(reussie=True)

    paginator = Paginator(tentatives, 30)
    page = request.GET.get('page')
    tentatives = paginator.get_page(page)

    return render(request, 'dmz/tentatives.html', {
        'tentatives': tentatives,
        'statut_filtre': statut,
    })


@login_required
@admin_requis
def vue_tentatives_admin(request):
    """View admin-specific login attempts."""
    tentatives = TentativeAdmin.objects.all()
    paginator = Paginator(tentatives, 30)
    page = request.GET.get('page')
    tentatives = paginator.get_page(page)
    return render(request, 'dmz/tentatives_admin.html', {'tentatives': tentatives})
