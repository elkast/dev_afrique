#!/usr/bin/env python
"""Réinitialise le mot de passe admin sur Neon"""

import os
import sys

os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_QWCGJNnPr4Y6@ep-icy-sun-ah25tfea-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteweb.settings')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
admin_password = os.environ.get('ADMIN_PASSWORD', 'DevAfrique2026!')

try:
    user = User.objects.get(username=admin_username)
    user.set_password(admin_password)
    user.save()
    print(f"✓ Mot de passe de '{admin_username}' réinitialisé avec succès!")
    print(f"✓ Nouveau mot de passe: {admin_password}")
    
    # Vérifier
    from django.contrib.auth import authenticate
    auth_user = authenticate(username=admin_username, password=admin_password)
    if auth_user:
        print("✓ Authentification testée: OK")
    else:
        print("✗ Erreur d'authentification")
except User.DoesNotExist:
    print(f"✗ Utilisateur '{admin_username}' non trouvé")
except Exception as e:
    print(f"✗ Erreur: {e}")
