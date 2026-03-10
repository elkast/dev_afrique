from django import forms
from .models import ProjetCommunautaire


class FormulaireProjet(forms.ModelForm):
    class Meta:
        model = ProjetCommunautaire
        fields = ['titre', 'description', 'technologies', 'lien_projet', 'lien_github', 'capture_url']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'champ-formulaire', 'placeholder': 'Nom de votre projet'}),
            'description': forms.Textarea(attrs={'class': 'champ-formulaire', 'rows': 5, 'placeholder': 'Décrivez votre projet...'}),
            'technologies': forms.TextInput(attrs={'class': 'champ-formulaire', 'placeholder': 'React, Django, PostgreSQL...'}),
            'lien_projet': forms.URLInput(attrs={'class': 'champ-formulaire', 'placeholder': 'https://mon-projet.com'}),
            'lien_github': forms.URLInput(attrs={'class': 'champ-formulaire', 'placeholder': 'https://github.com/...'}),
            'capture_url': forms.URLInput(attrs={'class': 'champ-formulaire', 'placeholder': 'URL de la capture d\'écran'}),
        }
