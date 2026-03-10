from django.shortcuts import render, get_object_or_404
from .models import TermeGlossaire


def vue_glossaire(request):
    lettre = request.GET.get('lettre', '')
    categorie = request.GET.get('categorie', '')
    recherche = request.GET.get('q', '')

    termes = TermeGlossaire.objects.all()
    if lettre:
        termes = termes.filter(lettre=lettre.upper())
    if categorie:
        termes = termes.filter(categorie=categorie)
    if recherche:
        termes = termes.filter(terme__icontains=recherche)

    # Toutes les lettres disponibles
    lettres = TermeGlossaire.objects.values_list('lettre', flat=True).distinct().order_by('lettre')

    return render(request, 'glossaire/glossaire.html', {
        'termes': termes,
        'lettres': lettres,
        'lettre_active': lettre.upper() if lettre else '',
        'categorie': categorie,
        'recherche': recherche,
        'categories': TermeGlossaire.CATEGORIE_CHOIX,
    })


def vue_detail_terme(request, slug):
    terme = get_object_or_404(TermeGlossaire, slug=slug)
    termes_lies = TermeGlossaire.objects.filter(categorie=terme.categorie).exclude(pk=terme.pk)[:5]
    return render(request, 'glossaire/detail_terme.html', {
        'terme': terme,
        'termes_lies': termes_lies,
    })
