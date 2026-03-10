from django.shortcuts import render
from cours.models import Parcours, Cours


def vue_accueil(request):
    parcours_liste = Parcours.objects.filter(est_publie=True)
    cours_recents = Cours.objects.filter(est_publie=True).order_by('-date_creation')[:6]
    return render(request, 'pages/accueil.html', {
        'parcours_liste': parcours_liste,
        'cours_recents': cours_recents,
    })


def vue_a_propos(request):
    return render(request, 'pages/a_propos.html')


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
