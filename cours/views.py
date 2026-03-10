from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Parcours, Cours, Lecon, ProgressionUtilisateur


def vue_liste_parcours(request):
    parcours_liste = Parcours.objects.filter(est_publie=True)
    return render(request, 'cours/liste_parcours.html', {
        'parcours_liste': parcours_liste,
    })


def vue_detail_parcours(request, slug):
    parcours = get_object_or_404(Parcours, slug=slug, est_publie=True)
    cours_liste = parcours.cours_set.filter(est_publie=True)
    return render(request, 'cours/detail_parcours.html', {
        'parcours': parcours,
        'cours_liste': cours_liste,
    })


def vue_liste_cours(request):
    parcours_filtre = request.GET.get('parcours', '')
    cours_liste = Cours.objects.filter(est_publie=True).select_related('parcours')
    if parcours_filtre:
        cours_liste = cours_liste.filter(parcours__slug=parcours_filtre)
    parcours_tous = Parcours.objects.filter(est_publie=True)
    return render(request, 'cours/liste_cours.html', {
        'cours_liste': cours_liste,
        'parcours_tous': parcours_tous,
        'parcours_filtre': parcours_filtre,
    })


def vue_detail_cours(request, slug):
    cours = get_object_or_404(Cours, slug=slug, est_publie=True)
    lecons = cours.lecon_set.filter(est_publie=True)
    return render(request, 'cours/detail_cours.html', {
        'cours': cours,
        'lecons': lecons,
    })


def vue_lecon(request, cours_slug, lecon_slug):
    cours = get_object_or_404(Cours, slug=cours_slug, est_publie=True)
    lecon = get_object_or_404(Lecon, slug=lecon_slug, cours=cours, est_publie=True)
    lecons_du_cours = cours.lecon_set.filter(est_publie=True)

    progression = None
    if request.user.is_authenticated:
        progression, _ = ProgressionUtilisateur.objects.get_or_create(
            utilisateur=request.user, lecon=lecon
        )

    return render(request, 'cours/lecon.html', {
        'cours': cours,
        'lecon': lecon,
        'lecons_du_cours': lecons_du_cours,
        'progression': progression,
    })


@login_required
def vue_marquer_terminee(request, cours_slug, lecon_slug):
    cours = get_object_or_404(Cours, slug=cours_slug)
    lecon = get_object_or_404(Lecon, slug=lecon_slug, cours=cours)
    progression, _ = ProgressionUtilisateur.objects.get_or_create(
        utilisateur=request.user, lecon=lecon
    )
    progression.terminee = True
    progression.date_completion = timezone.now()
    progression.save()

    suivante = lecon.lecon_suivante()
    if suivante:
        return redirect('lecon', cours_slug=cours.slug, lecon_slug=suivante.slug)
    return redirect('detail_cours', slug=cours.slug)
