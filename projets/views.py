from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import ProjetCommunautaire, Like
from .formulaires import FormulaireProjet


def vue_liste_projets(request):
    projets = ProjetCommunautaire.objects.filter(statut='approuve').select_related('auteur')
    tech_filtre = request.GET.get('tech', '')
    tri = request.GET.get('tri', 'recent')

    if tech_filtre:
        projets = projets.filter(technologies__icontains=tech_filtre)

    if tri == 'populaire':
        projets = projets.order_by('-nb_likes', '-date_soumission')
    else:
        projets = projets.order_by('-date_soumission')

    return render(request, 'projets/liste_projets.html', {
        'projets': projets,
        'tech_filtre': tech_filtre,
        'tri': tri,
    })


def vue_detail_projet(request, slug):
    projet = get_object_or_404(ProjetCommunautaire, slug=slug, statut='approuve')
    commentaires = projet.commentaires.select_related('auteur').filter(parent__isnull=True)
    a_like = False
    if request.user.is_authenticated:
        a_like = Like.objects.filter(utilisateur=request.user, projet=projet).exists()
    return render(request, 'projets/detail_projet.html', {
        'projet': projet,
        'commentaires': commentaires,
        'a_like': a_like,
    })


@login_required
def vue_soumettre_projet(request):
    if request.method == 'POST':
        formulaire = FormulaireProjet(request.POST)
        if formulaire.is_valid():
            projet = formulaire.save(commit=False)
            projet.auteur = request.user
            projet.save()
            request.user.ajouter_xp(25)
            messages.success(request, 'Votre projet a été soumis et sera examiné par un modérateur.')
            return redirect('liste_projets')
    else:
        formulaire = FormulaireProjet()
    return render(request, 'projets/soumettre_projet.html', {'formulaire': formulaire})


@login_required
def vue_liker_projet(request, slug):
    projet = get_object_or_404(ProjetCommunautaire, slug=slug, statut='approuve')
    like, cree = Like.objects.get_or_create(utilisateur=request.user, projet=projet)
    if not cree:
        like.delete()
    projet.mettre_a_jour_likes()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'likes': projet.nb_likes, 'liked': cree})
    return redirect('detail_projet', slug=slug)


@login_required
def vue_commenter_projet(request, slug):
    from cours.models import Commentaire
    projet = get_object_or_404(ProjetCommunautaire, slug=slug, statut='approuve')
    if request.method == 'POST':
        contenu = request.POST.get('contenu', '').strip()
        if contenu:
            Commentaire.objects.create(
                auteur=request.user,
                projet=projet,
                contenu=contenu,
            )
            request.user.ajouter_xp(3)
            messages.success(request, 'Commentaire ajouté !')
    return redirect('detail_projet', slug=slug)
