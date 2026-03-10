#!/usr/bin/env python
"""Diagnostic de connexion à la base de données"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteweb.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings

print("=" * 60)
print("DIAGNOSTIC CONNEXION BASE DE DONNÉES")
print("=" * 60)

# 1. Vérifier DATABASE_URL
print("\n1. VARIABLE D'ENVIRONNEMENT DATABASE_URL:")
db_url = os.environ.get('DATABASE_URL', '')
if db_url:
    # Masquer le mot de passe pour l'affichage
    masked = db_url
    if '@' in db_url:
        parts = db_url.split('@')
        creds = parts[0].split('://')[1] if '://' in parts[0] else parts[0]
        masked = db_url.replace(creds, '***:***')
    print(f"   ✓ Configurée: {masked[:60]}...")
else:
    print("   ✗ NON CONFIGURÉE (fallback sur SQLite)")

# 2. Voir la configuration Django
print("\n2. CONFIGURATION DJANGO ACTUELLE:")
db_config = settings.DATABASES['default']
print(f"   Engine: {db_config.get('ENGINE')}")
print(f"   Name: {db_config.get('NAME')}")
if 'HOST' in db_config:
    print(f"   Host: {db_config.get('HOST')}")
    print(f"   Port: {db_config.get('PORT')}")

# 3. Tester la connexion
print("\n3. TEST DE CONNEXION:")
from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("   ✓ Connexion réussie!")
        
        # Identifier le type de base
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"   Version: {version[:50]}...")
        
        # Vérifier si c'est SQLite ou PostgreSQL
        if 'sqlite' in db_config.get('ENGINE', '').lower():
            print("   ⚠️  ATTENTION: Tu utilises SQLITE (local), pas Neon!")
        elif 'postgres' in db_config.get('ENGINE', '').lower():
            print("   ✓ Tu utilises bien PostgreSQL (Neon)")
            
except Exception as e:
    print(f"   ✗ Erreur de connexion: {e}")

# 4. Compter les enregistrements dans les tables principales
print("\n4. DONNÉES STOCKÉES:")
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    print(f"   Utilisateurs: {User.objects.count()}")
    
    from cours.models import Cours, Lecon
    print(f"   Cours: {Cours.objects.count()}")
    print(f"   Leçons: {Lecon.objects.count()}")
    
    from projets.models import ProjetCommunautaire
    print(f"   Projets: {ProjetCommunautaire.objects.count()}")
    
except Exception as e:
    print(f"   Erreur: {e}")

print("\n" + "=" * 60)
print("CONCLUSION:")
if 'sqlite' in db_config.get('ENGINE', '').lower():
    print("❌ Tes données vont dans SQLite local, PAS sur Neon!")
    print("\nPour utiliser Neon en local, ajoute dans ton .env:")
    print("DATABASE_URL=postgresql://neondb_owner:npg_QWCGJNnPr4Y6@ep-icy-sun-ah25tfea-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")
else:
    print("✅ Tes données vont bien sur Neon PostgreSQL!")
print("=" * 60)
