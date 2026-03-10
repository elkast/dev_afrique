from django import forms
from .models import SujetForum, ReponseForum


class FormulaireSujet(forms.ModelForm):
    class Meta:
        model = SujetForum
        fields = ['titre', 'contenu', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'champ-formulaire', 'placeholder': 'Votre question en une phrase claire'}),
            'contenu': forms.Textarea(attrs={'class': 'champ-formulaire', 'rows': 8, 'placeholder': 'Décrivez votre problème en détail. Ajoutez du code si nécessaire.'}),
            'categorie': forms.Select(attrs={'class': 'champ-formulaire'}),
        }


class FormulaireReponse(forms.ModelForm):
    class Meta:
        model = ReponseForum
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'champ-formulaire', 'rows': 5, 'placeholder': 'Votre réponse...'}),
        }
