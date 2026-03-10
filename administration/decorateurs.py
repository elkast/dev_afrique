from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_requis(vue_func):
    @wraps(vue_func)
    def _enveloppe(request, *args, **kwargs):
        if not hasattr(request.user, 'est_admin') or not request.user.est_admin():
            messages.error(request, 'Accès refusé. Vous devez être administrateur.')
            return redirect('accueil')
        return vue_func(request, *args, **kwargs)
    return _enveloppe
