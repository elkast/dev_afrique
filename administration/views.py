from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from cours.models import Parcours, Cours, Lecon
from projets.models import ProjetCommunautaire
from utilisateurs.models import Utilisateur
from forum.models import SujetForum
from glossaire.models import TermeGlossaire
from .models import Signalement
from .decorateurs import admin_requis
from .formulaires import (
    FormulaireParcoursAdmin, FormulaireCoursAdmin,
    FormulaireLeconAdmin, FormulaireStatutProjet,
    FormulaireTermeGlossaireAdmin, FormulaireSignalement
)


@login_required
@admin_requis
def vue_tableau_de_bord(request):
    stats = {
        'total_utilisateurs': Utilisateur.objects.count(),
        'total_cours': Cours.objects.count(),
        'total_lecons': Lecon.objects.count(),
        'projets_en_attente': ProjetCommunautaire.objects.filter(statut='en_attente').count(),
        'total_parcours': Parcours.objects.count(),
        'total_sujets_forum': SujetForum.objects.count(),
        'total_termes_glossaire': TermeGlossaire.objects.count(),
        'signalements_en_attente': Signalement.objects.filter(statut='en_attente').count(),
    }
    projets_recents = ProjetCommunautaire.objects.filter(statut='en_attente')[:5]
    signalements_recents = Signalement.objects.filter(statut='en_attente')[:5]
    return render(request, 'administration/tableau_de_bord.html', {
        'stats': stats,
        'projets_recents': projets_recents,
        'signalements_recents': signalements_recents,
    })


# ─── PARCOURS ────────────────────────────────────────────────
@login_required
@admin_requis
def vue_liste_parcours_admin(request):
    parcours = Parcours.objects.all()
    return render(request, 'administration/parcours/liste.html', {'parcours_liste': parcours})


@login_required
@admin_requis
def vue_creer_parcours(request):
    if request.method == 'POST':
        formulaire = FormulaireParcoursAdmin(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Parcours créé avec succès.')
            return redirect('admin_liste_parcours')
    else:
        formulaire = FormulaireParcoursAdmin()
    return render(request, 'administration/parcours/formulaire.html', {
        'formulaire': formulaire, 'action': 'Créer'
    })


@login_required
@admin_requis
def vue_modifier_parcours(request, pk):
    parcours = get_object_or_404(Parcours, pk=pk)
    if request.method == 'POST':
        formulaire = FormulaireParcoursAdmin(request.POST, instance=parcours)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Parcours modifié avec succès.')
            return redirect('admin_liste_parcours')
    else:
        formulaire = FormulaireParcoursAdmin(instance=parcours)
    return render(request, 'administration/parcours/formulaire.html', {
        'formulaire': formulaire, 'action': 'Modifier'
    })


@login_required
@admin_requis
def vue_supprimer_parcours(request, pk):
    parcours = get_object_or_404(Parcours, pk=pk)
    if request.method == 'POST':
        parcours.delete()
        messages.success(request, 'Parcours supprimé.')
        return redirect('admin_liste_parcours')
    return render(request, 'administration/confirmer_suppression.html', {
        'objet': parcours, 'type': 'parcours', 'retour': 'admin_liste_parcours'
    })


# ─── COURS ───────────────────────────────────────────────────
@login_required
@admin_requis
def vue_liste_cours_admin(request):
    cours = Cours.objects.select_related('parcours').all()
    return render(request, 'administration/cours/liste.html', {'cours_liste': cours})


@login_required
@admin_requis
def vue_creer_cours(request):
    if request.method == 'POST':
        formulaire = FormulaireCoursAdmin(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Cours créé avec succès.')
            return redirect('admin_liste_cours')
    else:
        formulaire = FormulaireCoursAdmin()
    return render(request, 'administration/cours/formulaire.html', {
        'formulaire': formulaire, 'action': 'Créer'
    })


@login_required
@admin_requis
def vue_modifier_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        formulaire = FormulaireCoursAdmin(request.POST, instance=cours)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Cours modifié avec succès.')
            return redirect('admin_liste_cours')
    else:
        formulaire = FormulaireCoursAdmin(instance=cours)
    return render(request, 'administration/cours/formulaire.html', {
        'formulaire': formulaire, 'action': 'Modifier'
    })


@login_required
@admin_requis
def vue_supprimer_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        cours.delete()
        messages.success(request, 'Cours supprimé.')
        return redirect('admin_liste_cours')
    return render(request, 'administration/confirmer_suppression.html', {
        'objet': cours, 'type': 'cours', 'retour': 'admin_liste_cours'
    })


# ─── LEÇONS ──────────────────────────────────────────────────
@login_required
@admin_requis
def vue_liste_lecons_admin(request):
    lecons = Lecon.objects.select_related('cours', 'cours__parcours').all()
    return render(request, 'administration/lecons/liste.html', {'lecons_liste': lecons})


@login_required
@admin_requis
def vue_creer_lecon(request):
    if request.method == 'POST':
        formulaire = FormulaireLeconAdmin(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Leçon créée avec succès.')
            return redirect('admin_liste_lecons')
    else:
        formulaire = FormulaireLeconAdmin()
    return render(request, 'administration/lecons/formulaire.html', {
        'formulaire': formulaire, 'action': 'Créer'
    })


@login_required
@admin_requis
def vue_modifier_lecon(request, pk):
    lecon = get_object_or_404(Lecon, pk=pk)
    if request.method == 'POST':
        formulaire = FormulaireLeconAdmin(request.POST, instance=lecon)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Leçon modifiée avec succès.')
            return redirect('admin_liste_lecons')
    else:
        formulaire = FormulaireLeconAdmin(instance=lecon)
    return render(request, 'administration/lecons/formulaire.html', {
        'formulaire': formulaire, 'action': 'Modifier'
    })


@login_required
@admin_requis
def vue_supprimer_lecon(request, pk):
    lecon = get_object_or_404(Lecon, pk=pk)
    if request.method == 'POST':
        lecon.delete()
        messages.success(request, 'Leçon supprimée.')
        return redirect('admin_liste_lecons')
    return render(request, 'administration/confirmer_suppression.html', {
        'objet': lecon, 'type': 'leçon', 'retour': 'admin_liste_lecons'
    })


# ─── PROJETS ─────────────────────────────────────────────────
@login_required
@admin_requis
def vue_liste_projets_admin(request):
    statut_filtre = request.GET.get('statut', '')
    projets = ProjetCommunautaire.objects.select_related('auteur').all()
    if statut_filtre:
        projets = projets.filter(statut=statut_filtre)
    return render(request, 'administration/projets/liste.html', {
        'projets_liste': projets,
        'statut_filtre': statut_filtre,
    })


@login_required
@admin_requis
def vue_moderer_projet(request, pk):
    projet = get_object_or_404(ProjetCommunautaire, pk=pk)
    if request.method == 'POST':
        formulaire = FormulaireStatutProjet(request.POST, instance=projet)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, f'Statut du projet mis à jour : {projet.get_statut_display()}')
            return redirect('admin_liste_projets')
    else:
        formulaire = FormulaireStatutProjet(instance=projet)
    return render(request, 'administration/projets/moderer.html', {
        'projet': projet, 'formulaire': formulaire
    })


# ─── UTILISATEURS ────────────────────────────────────────────
@login_required
@admin_requis
def vue_liste_utilisateurs_admin(request):
    role_filtre = request.GET.get('role', '')
    utilisateurs = Utilisateur.objects.all().order_by('-date_joined')
    if role_filtre:
        utilisateurs = utilisateurs.filter(role=role_filtre)
    paginator = Paginator(utilisateurs, 20)
    page = request.GET.get('page')
    utilisateurs = paginator.get_page(page)
    return render(request, 'administration/utilisateurs/liste.html', {
        'utilisateurs_liste': utilisateurs,
        'role_filtre': role_filtre,
    })


@login_required
@admin_requis
def vue_modifier_role(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    if request.method == 'POST':
        nouveau_role = request.POST.get('role', 'apprenant')
        if nouveau_role in dict(Utilisateur.ROLE_CHOIX):
            utilisateur.role = nouveau_role
            utilisateur.save(update_fields=['role'])
            messages.success(request, f'Rôle de {utilisateur.username} mis à jour : {utilisateur.get_role_display()}')
    return redirect('admin_liste_utilisateurs')


# ─── SIGNALEMENTS ────────────────────────────────────────────
@login_required
@admin_requis
def vue_liste_signalements(request):
    statut_filtre = request.GET.get('statut', 'en_attente')
    signalements = Signalement.objects.select_related('signaleur').all()
    if statut_filtre:
        signalements = signalements.filter(statut=statut_filtre)
    return render(request, 'administration/signalements/liste.html', {
        'signalements': signalements,
        'statut_filtre': statut_filtre,
    })


@login_required
@admin_requis
def vue_traiter_signalement(request, pk):
    signalement = get_object_or_404(Signalement, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action', 'ignore')
        signalement.statut = 'traite' if action == 'traiter' else 'ignore'
        signalement.traite_par = request.user
        signalement.date_traitement = timezone.now()
        signalement.save()
        messages.success(request, 'Signalement traité.')
    return redirect('admin_liste_signalements')


# ─── GLOSSAIRE ───────────────────────────────────────────────
@login_required
@admin_requis
def vue_liste_glossaire_admin(request):
    termes = TermeGlossaire.objects.all()
    return render(request, 'administration/glossaire/liste.html', {'termes': termes})


@login_required
@admin_requis
def vue_creer_terme(request):
    if request.method == 'POST':
        formulaire = FormulaireTermeGlossaireAdmin(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Terme ajouté au glossaire.')
            return redirect('admin_liste_glossaire')
    else:
        formulaire = FormulaireTermeGlossaireAdmin()
    return render(request, 'administration/glossaire/formulaire.html', {
        'formulaire': formulaire, 'action': 'Créer'
    })


@login_required
@admin_requis
def vue_modifier_terme(request, pk):
    terme = get_object_or_404(TermeGlossaire, pk=pk)
    if request.method == 'POST':
        formulaire = FormulaireTermeGlossaireAdmin(request.POST, instance=terme)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Terme modifié.')
            return redirect('admin_liste_glossaire')
    else:
        formulaire = FormulaireTermeGlossaireAdmin(instance=terme)
    return render(request, 'administration/glossaire/formulaire.html', {
        'formulaire': formulaire, 'action': 'Modifier'
    })


@login_required
@admin_requis
def vue_supprimer_terme(request, pk):
    terme = get_object_or_404(TermeGlossaire, pk=pk)
    if request.method == 'POST':
        terme.delete()
        messages.success(request, 'Terme supprimé.')
        return redirect('admin_liste_glossaire')
    return render(request, 'administration/confirmer_suppression.html', {
        'objet': terme, 'type': 'terme', 'retour': 'admin_liste_glossaire'
    })
