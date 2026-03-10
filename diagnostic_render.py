#!/usr/bin/env python
"""Diagnostic complet de la connexion à Neon et des utilisateurs"""

import os
import sys

# Forcer la configuration Render
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_QWCGJNnPr4Y6@ep-icy-sun-ah25tfea-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteweb.settings')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import django
    django.setup()
    
    from django.db import connection
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    print("=" * 60)
    print("DIAGNOSTIC CONNEXION RENDER/NEON")
    print("=" * 60)
    
    # 1. Test connexion directe
    print("\n1. CONNEXION DIRECTE À NEON:")
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"   ✓ Connecté: {version[:50]}...")
    
    # 2. Vérifier les tables
    print("\n2. TABLES UTILISATEURS:")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename LIKE '%utilisateur%'
        """)
        tables = cursor.fetchall()
        for t in tables:
            print(f"   ✓ {t[0]}")
    
    # 3. Compter les utilisateurs
    print("\n3. UTILISATEURS DANS NEON:")
    user_count = User.objects.count()
    print(f"   Total: {user_count} utilisateurs")
    
    # 4. Vérifier l'admin spécifiquement
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    try:
        admin = User.objects.filter(username=admin_username).first()
        if admin:
            print(f"\n4. ADMIN '{admin_username}':")
            print(f"   ✓ Existe: oui")
            print(f"   ✓ Email: {admin.email}")
            print(f"   ✓ Role: {admin.role}")
            print(f"   ✓ is_superuser: {admin.is_superuser}")
            print(f"   ✓ is_staff: {admin.is_staff}")
            print(f"   ✓ is_active: {admin.is_active}")
            
            # Tester le mot de passe
            from django.contrib.auth import authenticate
            admin_pass = os.environ.get('ADMIN_PASSWORD', 'DevAfrique2026!')
            auth_user = authenticate(username=admin_username, password=admin_pass)
            if auth_user:
                print(f"   ✓ Authentification: RÉUSSIE")
            else:
                print(f"   ✗ Authentification: ÉCHEC")
                print(f"      Le mot de passe ne correspond pas!")
        else:
            print(f"\n4. ADMIN '{admin_username}':")
            print(f"   ✗ N'existe pas!")
            print("   → Création nécessaire: python manage.py creer_superuser")
    except Exception as e:
        print(f"\n4. ERREUR: {e}")
    
    # 5. Lister tous les utilisateurs
    print("\n5. TOUS LES UTILISATEURS:")
    for u in User.objects.all()[:10]:
        print(f"   - {u.username} ({u.email}) - superuser:{u.is_superuser}")
    
    print("\n" + "=" * 60)
    print("CONFIGURATION DATABASE:")
    from django.conf import settings
    db_config = settings.DATABASES['default']
    print(f"   Engine: {db_config.get('ENGINE')}")
    print(f"   Host: {db_config.get('HOST', 'N/A')}")
    print(f"   SSL: {db_config.get('OPTIONS', {}).get('sslmode', 'non')}")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERREUR CRITIQUE: {e}")
    import traceback
    traceback.print_exc()
