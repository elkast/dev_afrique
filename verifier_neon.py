#!/usr/bin/env python
"""Vérification des migrations et création admin sur Neon"""

import os
import sys

# Forcer DATABASE_URL pour Render/Neon
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
    print("VÉRIFICATION RENDER/NEON")
    print("=" * 60)
    
    # 1. Test connexion
    print("\n1. CONNEXION NEON:")
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"   ✓ Connecté: {version[:40]}...")
    
    # 2. Vérifier si tables utilisateurs existent
    print("\n2. TABLES EXISTANTES:")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename LIKE '%utilisateur%'
        """)
        tables = cursor.fetchall()
        if tables:
            for t in tables:
                print(f"   ✓ {t[0]}")
        else:
            print("   ✗ Aucune table utilisateur trouvée!")
    
    # 3. Vérifier admin
    print("\n3. SUPERUTILISATEUR:")
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    try:
        admin = User.objects.filter(username=admin_username).first()
        if admin:
            print(f"   ✓ Admin '{admin_username}' existe (role: {admin.role})")
        else:
            print(f"   ✗ Admin '{admin_username}' n'existe PAS!")
            print("   → Création nécessaire: python manage.py creer_superuser")
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        print("   → Les migrations ne sont probablement pas appliquées")
    
    # 4. Liste des migrations appliquées
    print("\n4. MIGRATIONS:")
    try:
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        migrations = recorder.applied_migrations()
        print(f"   Total: {len(migrations)} migrations appliquées")
        recent = list(migrations)[-5:]
        for m in recent:
            print(f"   - {m[0]}: {m[1]}")
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
