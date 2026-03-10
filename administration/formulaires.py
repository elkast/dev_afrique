from django import forms
from cours.models import Parcours, Cours, Lecon
from projets.models import ProjetCommunautaire
from glossaire.models import TermeGlossaire
from .models import Signalement


class FormulaireParcoursAdmin(forms.ModelForm):
    class Meta:
        model = Parcours
        fields = ['titre', 'description', 'type_parcours', 'icone', 'image_url', 'ordre', 'est_publie']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'champ-formulaire'}),
            'description': forms.Textarea(attrs={'class': 'champ-formulaire', 'rows': 4}),
            'type_parcours': forms.Select(attrs={'class': 'champ-formulaire'}),
            'icone': forms.TextInput(attrs={'class': 'champ-formulaire'}),
            'image_url': forms.URLInput(attrs={'class': 'champ-formulaire', 'placeholder': 'URL image de couverture'}),
            'ordre': forms.NumberInput(attrs={'class': 'champ-formulaire'}),
        }


class FormulaireCoursAdmin(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['parcours', 'titre', 'description', 'icone', 'image_url', 'niveau', 'ordre', 'est_publie']
        widgets = {
            'parcours': forms.Select(attrs={'class': 'champ-formulaire'}),
            'titre': forms.TextInput(attrs={'class': 'champ-formulaire'}),
            'description': forms.Textarea(attrs={'class': 'champ-formulaire', 'rows': 4}),
            'icone': forms.TextInput(attrs={'class': 'champ-formulaire'}),
            'image_url': forms.URLInput(attrs={'class': 'champ-formulaire'}),
            'niveau': forms.Select(attrs={'class': 'champ-formulaire'}),
            'ordre': forms.NumberInput(attrs={'class': 'champ-formulaire'}),
        }


class FormulaireLeconAdmin(forms.ModelForm):
    class Meta:
        model = Lecon
        fields = ['cours', 'titre', 'contenu', 'ordre', 'duree_minutes', 'est_publie']
        widgets = {
            'cours': forms.Select(attrs={'class': 'champ-formulaire'}),
            'titre': forms.TextInput(attrs={'class': 'champ-formulaire'}),
            'contenu': forms.Textarea(attrs={'class': 'champ-formulaire zone-code', 'rows': 20}),
            'ordre': forms.NumberInput(attrs={'class': 'champ-formulaire'}),
            'duree_minutes': forms.NumberInput(attrs={'class': 'champ-formulaire'}),
        }


class FormulaireStatutProjet(forms.ModelForm):
    class Meta:
        model = ProjetCommunautaire
        fields = ['statut']
        widgets = {
            'statut': forms.Select(attrs={'class': 'champ-formulaire'}),
        }


class FormulaireTermeGlossaireAdmin(forms.ModelForm):
    class Meta:
        model = TermeGlossaire
        fields = ['terme', 'definition', 'exemple_code', 'langage_exemple', 'categorie']
        widgets = {
            'terme': forms.TextInput(attrs={'class': 'champ-formulaire'}),
            'definition': forms.Textarea(attrs={'class': 'champ-formulaire', 'rows': 4}),
            'exemple_code': forms.Textarea(attrs={'class': 'champ-formulaire zone-code', 'rows': 8}),
            'langage_exemple': forms.TextInput(attrs={'class': 'champ-formulaire', 'placeholder': 'HTML, Python, JavaScript...'}),
            'categorie': forms.Select(attrs={'class': 'champ-formulaire'}),
        }


class FormulaireSignalement(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = ['type_contenu', 'id_contenu', 'raison', 'description']
        widgets = {
            'type_contenu': forms.Select(attrs={'class': 'champ-formulaire'}),
            'id_contenu': forms.NumberInput(attrs={'class': 'champ-formulaire'}),
            'raison': forms.Select(attrs={'class': 'champ-formulaire'}),
            'description': forms.Textarea(attrs={'class': 'champ-formulaire', 'rows': 3}),
        }
