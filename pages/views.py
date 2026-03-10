from django.shortcuts import render
from cours.models import Parcours, Cours, Lecon
from glossaire.models import TermeGlossaire
from projets.models import ProjetCommunautaire
from forum.models import SujetForum


def vue_accueil(request):
    """Vue d'accueil - différente selon connexion."""
    if request.user.is_authenticated:
        return vue_tableau_bord(request)
    
    # Landing page pour visiteurs
    parcours_liste = Parcours.objects.filter(est_publie=True)
    cours_recents = Cours.objects.filter(est_publie=True).order_by('-date_creation')[:6]
    return render(request, 'pages/accueil.html', {
        'parcours_liste': parcours_liste,
        'cours_recents': cours_recents,
    })


def vue_a_propos(request):
    return render(request, 'pages/a_propos.html')


def vue_createur(request):
    """Page présentant le créateur Sossou Elkast."""
    return render(request, 'pages/createur.html')


def vue_tableau_bord(request):
    """Tableau de bord pour utilisateurs connectés."""
    # Cours recommandés (non commencés ou en cours)
    mes_cours_ids = request.user.progressions.values_list('lecon__cours_id', flat=True).distinct()
    cours_suivis = Cours.objects.filter(id__in=mes_cours_ids, est_publie=True)[:3]
    
    # Suggestions de nouveaux cours
    cours_suggestions = Cours.objects.exclude(
        id__in=mes_cours_ids
    ).filter(est_publie=True).select_related('parcours')[:3]
    
    # Parcours disponibles
    parcours_liste = Parcours.objects.filter(est_publie=True)[:4]
    
    # Glossaire - termes récents
    termes_glossaire = TermeGlossaire.objects.filter(est_publie=True)[:6]
    
    # Projets communautaires
    projets_recents = ProjetCommunautaire.objects.filter(
        statut='approuve'
    ).select_related('auteur')[:3]
    
    # Discussions forum récentes
    discussions_recentes = SujetForum.objects.filter(
        est_resolu=False
    ).select_related('auteur', 'categorie').order_by('-date_creation')[:5]
    
    # Progression de l'utilisateur
    progression_total = request.user.progressions.count()
    
    return render(request, 'pages/tableau_bord.html', {
        'cours_suivis': cours_suivis,
        'cours_suggestions': cours_suggestions,
        'parcours_liste': parcours_liste,
        'termes_glossaire': termes_glossaire,
        'projets_recents': projets_recents,
        'discussions_recentes': discussions_recentes,
        'progression_total': progression_total,
    })


def vue_bibliographie(request):
    return render(request, 'pages/bibliographie.html')


# ─── HTTP Error Views ────────────────────────────────────────
def vue_erreur_400(request, exception=None):
    return render(request, 'erreurs/400.html', status=400)


def vue_erreur_403(request, exception=None):
    return render(request, 'erreurs/403.html', status=403)


def vue_erreur_404(request, exception=None):
    return render(request, 'erreurs/404.html', status=404)


def vue_erreur_500(request):
    return render(request, 'erreurs/500.html', status=500)
