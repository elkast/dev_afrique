from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import SujetForum, ReponseForum
from .formulaires import FormulaireSujet, FormulaireReponse


def vue_liste_sujets(request):
    categorie = request.GET.get('categorie', '')
    recherche = request.GET.get('q', '')
    sujets = SujetForum.objects.select_related('auteur').all()

    if categorie:
        sujets = sujets.filter(categorie=categorie)
    if recherche:
        sujets = sujets.filter(titre__icontains=recherche)

    paginator = Paginator(sujets, 15)
    page = request.GET.get('page')
    sujets = paginator.get_page(page)

    return render(request, 'forum/liste_sujets.html', {
        'sujets': sujets,
        'categorie': categorie,
        'recherche': recherche,
        'categories': SujetForum.CATEGORIE_CHOIX,
    })


def vue_detail_sujet(request, slug):
    sujet = get_object_or_404(SujetForum, slug=slug)
    sujet.nb_vues += 1
    sujet.save(update_fields=['nb_vues'])
    reponses = sujet.reponses.select_related('auteur').all()
    formulaire = FormulaireReponse()
    return render(request, 'forum/detail_sujet.html', {
        'sujet': sujet,
        'reponses': reponses,
        'formulaire': formulaire,
    })


@login_required
def vue_nouveau_sujet(request):
    if request.method == 'POST':
        formulaire = FormulaireSujet(request.POST)
        if formulaire.is_valid():
            sujet = formulaire.save(commit=False)
            sujet.auteur = request.user
            sujet.save()
            request.user.ajouter_xp(10)
            messages.success(request, 'Votre sujet a été publié !')
            return redirect('forum_detail', slug=sujet.slug)
    else:
        formulaire = FormulaireSujet()
    return render(request, 'forum/nouveau_sujet.html', {'formulaire': formulaire})


@login_required
def vue_repondre(request, slug):
    sujet = get_object_or_404(SujetForum, slug=slug)
    if request.method == 'POST':
        formulaire = FormulaireReponse(request.POST)
        if formulaire.is_valid():
            reponse = formulaire.save(commit=False)
            reponse.sujet = sujet
            reponse.auteur = request.user
            reponse.save()
            request.user.ajouter_xp(5)
            messages.success(request, 'Votre réponse a été publiée !')
    return redirect('forum_detail', slug=sujet.slug)


@login_required
def vue_marquer_solution(request, slug, reponse_id):
    sujet = get_object_or_404(SujetForum, slug=slug, auteur=request.user)
    reponse = get_object_or_404(ReponseForum, id=reponse_id, sujet=sujet)
    # Retirer solution précédente
    sujet.reponses.update(est_solution=False)
    reponse.est_solution = True
    reponse.save(update_fields=['est_solution'])
    sujet.est_resolu = True
    sujet.save(update_fields=['est_resolu'])
    reponse.auteur.ajouter_xp(20)
    messages.success(request, 'Réponse marquée comme solution !')
    return redirect('forum_detail', slug=sujet.slug)
