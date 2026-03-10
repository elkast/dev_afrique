from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .formulaires import FormulaireInscription, FormulaireConnexion, FormulaireProfilUtilisateur
from .models import Utilisateur
from cours.models import ProgressionUtilisateur, Certificat
from projets.models import ProjetCommunautaire


def vue_inscription(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        formulaire = FormulaireInscription(request.POST)
        if formulaire.is_valid():
            utilisateur = formulaire.save()
            login(request, utilisateur)
            messages.success(request, 'Bienvenue ! Votre compte a été créé avec succès. 🎉')
            return redirect('accueil')
    else:
        formulaire = FormulaireInscription()
    return render(request, 'utilisateurs/inscription.html', {'formulaire': formulaire})


def vue_connexion(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        formulaire = FormulaireConnexion(request, data=request.POST)
        if formulaire.is_valid():
            utilisateur = formulaire.get_user()
            login(request, utilisateur)
            messages.success(request, f'Bienvenue, {utilisateur.username} !')
            suivant = request.GET.get('next', 'accueil')
            return redirect(suivant)
    else:
        formulaire = FormulaireConnexion()
    return render(request, 'utilisateurs/connexion.html', {'formulaire': formulaire})


def vue_deconnexion(request):
    logout(request)
    messages.info(request, 'Vous êtes déconnecté.')
    return redirect('accueil')


@login_required
def vue_profil(request):
    progressions = ProgressionUtilisateur.objects.filter(
        utilisateur=request.user, terminee=True
    ).select_related('lecon', 'lecon__cours')
    mes_projets = ProjetCommunautaire.objects.filter(auteur=request.user)
    certificats = Certificat.objects.filter(utilisateur=request.user).select_related('parcours')

    if request.method == 'POST':
        formulaire = FormulaireProfilUtilisateur(request.POST, request.FILES, instance=request.user)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profil')
    else:
        formulaire = FormulaireProfilUtilisateur(instance=request.user)

    return render(request, 'utilisateurs/profil.html', {
        'formulaire': formulaire,
        'progressions': progressions,
        'mes_projets': mes_projets,
        'certificats': certificats,
    })


def vue_profil_public(request, username):
    utilisateur = get_object_or_404(Utilisateur, username=username)
    projets = ProjetCommunautaire.objects.filter(auteur=utilisateur, statut='approuve')
    certificats = Certificat.objects.filter(utilisateur=utilisateur).select_related('parcours')
    progressions = ProgressionUtilisateur.objects.filter(
        utilisateur=utilisateur, terminee=True
    ).select_related('lecon', 'lecon__cours')

    return render(request, 'utilisateurs/profil_public.html', {
        'profil_utilisateur': utilisateur,
        'projets': projets,
        'certificats': certificats,
        'progressions': progressions,
    })
