from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import FileExtensionValidator
from .models import Utilisateur


class FormulaireInscription(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'champ-formulaire', 'placeholder': 'votre@email.com'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'champ-formulaire', 'placeholder': "Nom d'utilisateur"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'champ-formulaire', 'placeholder': 'Mot de passe'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'champ-formulaire', 'placeholder': 'Confirmer le mot de passe'
    }))

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password1', 'password2']


class FormulaireConnexion(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'champ-formulaire', 'placeholder': "Nom d'utilisateur"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'champ-formulaire', 'placeholder': 'Mot de passe'
    }))


class FormulaireProfilUtilisateur(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        widget=forms.FileInput(attrs={
            'class': 'champ-formulaire',
            'accept': 'image/jpeg,image/png,image/gif,image/webp',
            'id': 'avatar-input',
        }),
        help_text='Formats acceptés : JPG, PNG, GIF, WebP. Max 2 Mo.',
    )

    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'biographie', 'site_web',
                  'pays', 'ville', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'champ-formulaire', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'champ-formulaire', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'champ-formulaire', 'placeholder': 'Email'}),
            'biographie': forms.Textarea(attrs={'class': 'champ-formulaire', 'rows': 4, 'placeholder': 'Parlez-nous de vous...'}),
            'site_web': forms.URLInput(attrs={'class': 'champ-formulaire', 'placeholder': 'https://...'}),
            'pays': forms.TextInput(attrs={'class': 'champ-formulaire', 'placeholder': "Côte d'Ivoire, Sénégal..."}),
            'ville': forms.TextInput(attrs={'class': 'champ-formulaire', 'placeholder': 'Abidjan, Dakar...'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'size'):
            if avatar.size > 2 * 1024 * 1024:  # 2 Mo
                raise forms.ValidationError('La taille de l\'image ne doit pas dépasser 2 Mo.')
        return avatar
