# -*- coding: utf-8 -*-
"""
Commande de management pour vérifier l'état complet de la base sur Render
Exécuter avec: python manage.py verifier_deploiement
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth import authenticate
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    help = 'Vérifie l\'état complet du déploiement sur Render'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("VERIFICATION DEPLOIEMENT RENDER")
        self.stdout.write("=" * 60)
        
        # 1. Connexion
        self.stdout.write("\n[1] CONNEXION BASE DE DONNEES:")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(f"✓ Connecté: {version[:40]}..."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))
            return
        
        # 2. Migrations
        self.stdout.write("\n[2] MIGRATIONS:")
        try:
            recorder = MigrationRecorder(connection)
            migrations = recorder.applied_migrations()
            self.stdout.write(self.style.SUCCESS(f"✓ {len(migrations)} migrations appliquées"))
            
            # Vérifier la migration 0004 spécifiquement
            if ('cours', '0004_alter_progressionutilisateur_utilisateur') in migrations:
                self.stdout.write(self.style.SUCCESS("✓ Migration 0004 (related_name) OK"))
            else:
                self.stdout.write(self.style.ERROR("✗ Migration 0004 MANQUANTE!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))
        
        # 3. Tables
        self.stdout.write("\n[3] TABLES:")
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tables = [row[0] for row in cursor.fetchall()]
                
                required = [
                    'utilisateurs_utilisateur',
                    'cours_parcours', 
                    'cours_cours',
                    'cours_lecon',
                    'cours_progressionutilisateur',
                    'glossaire_termeglossaire',
                    'forum_sujetforum'
                ]
                for table in required:
                    if table in tables:
                        self.stdout.write(self.style.SUCCESS(f"✓ {table}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"✗ {table} MANQUANT"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))
        
        # 4. Données
        self.stdout.write("\n[4] DONNEES:")
        try:
            from utilisateurs.models import Utilisateur
            from cours.models import Parcours, Cours, Lecon
            from glossaire.models import TermeGlossaire
            from forum.models import SujetForum
            
            self.stdout.write(f"  Utilisateurs: {Utilisateur.objects.count()}")
            self.stdout.write(f"  Parcours: {Parcours.objects.count()}")
            self.stdout.write(f"  Cours: {Cours.objects.count()}")
            self.stdout.write(f"  Leçons: {Lecon.objects.count()}")
            self.stdout.write(f"  Glossaire: {TermeGlossaire.objects.count()}")
            self.stdout.write(f"  Forum: {SujetForum.objects.count()}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))
        
        # 5. Test admin
        self.stdout.write("\n[5] COMPTE ADMIN:")
        try:
            admin = Utilisateur.objects.filter(username='admin').first()
            if admin:
                self.stdout.write(self.style.SUCCESS(f"✓ Admin existe (id={admin.id})"))
                user = authenticate(username='admin', password='DevAfrique2026!')
                if user:
                    self.stdout.write(self.style.SUCCESS("✓ Mot de passe OK"))
                else:
                    self.stdout.write(self.style.ERROR("✗ Mot de passe INCORRECT"))
            else:
                self.stdout.write(self.style.ERROR("✗ Admin n'existe pas"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))
        
        # 6. Test related_name
        self.stdout.write("\n[6] TEST RELATED_NAME:")
        try:
            # Créer un utilisateur test
            user, _ = Utilisateur.objects.get_or_create(
                username='test_related',
                defaults={'email': 'test@test.com'}
            )
            # Tester l'accès à progressions
            _ = user.progressions
            self.stdout.write(self.style.SUCCESS("✓ user.progressions accessible"))
            user.delete()
        except AttributeError as e:
            self.stdout.write(self.style.ERROR(f"✗ ERREUR related_name: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))
        
        # 7. Test vue_accueil
        self.stdout.write("\n[7] TEST VUE ACCUEIL:")
        try:
            from pages.views import vue_accueil
            from django.test import RequestFactory
            
            factory = RequestFactory()
            request = factory.get('/')
            request.user = Utilisateur.objects.filter(username='admin').first()
            
            response = vue_accueil(request)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f"✓ vue_accueil HTTP 200"))
            else:
                self.stdout.write(self.style.ERROR(f"✗ vue_accueil HTTP {response.status_code}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("VERIFICATION TERMINEE")
        self.stdout.write("=" * 60)
