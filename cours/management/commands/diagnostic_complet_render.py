# -*- coding: utf-8 -*-
"""
Diagnostic complet: Authentification + Stockage Neon + Affichage
Exécuter avec: python manage.py diagnostic_complet_render
"""
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.contrib.auth import authenticate, get_user_model
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware

Utilisateur = get_user_model()


class Command(BaseCommand):
    help = 'Diagnostic complet du déploiement Render'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Corriger automatiquement les problèmes trouvés',
        )

    def handle(self, *args, **options):
        fix = options['fix']
        errors = []
        warnings = []
        
        self.stdout.write("=" * 70)
        self.stdout.write("DIAGNOSTIC COMPLET RENDER/NEON")
        self.stdout.write("=" * 70)

        # 1. Connexion base de données
        self.stdout.write("\n[1] CONNEXION BASE DE DONNEES")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                cursor.execute("SELECT current_database()")
                db_name = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(f"✓ Connecté à: {db_name}"))
                self.stdout.write(f"  Version: {version[:50]}...")
                
                # Test écriture/lecture
                cursor.execute("CREATE TABLE IF NOT EXISTS test_connexion (id serial PRIMARY KEY, test_val varchar(50))")
                cursor.execute("INSERT INTO test_connexion (test_val) VALUES ('test_render') RETURNING id")
                test_id = cursor.fetchone()[0]
                cursor.execute("SELECT test_val FROM test_connexion WHERE id = %s", [test_id])
                result = cursor.fetchone()[0]
                cursor.execute("DROP TABLE test_connexion")
                
                if result == 'test_render':
                    self.stdout.write(self.style.SUCCESS("✓ Écriture/Lecture OK"))
                else:
                    errors.append("Échec lecture/écriture base de données")
                    self.stdout.write(self.style.ERROR("✗ Échec lecture/écriture"))
        except Exception as e:
            errors.append(f"Connexion DB: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))

        # 2. Authentification - Admin
        self.stdout.write("\n[2] AUTHENTIFICATION ADMIN")
        try:
            admin = Utilisateur.objects.filter(username='admin').first()
            if admin:
                self.stdout.write(f"  Admin trouvé (id={admin.id}, role={admin.role})")
                
                # Test authentification
                user_auth = authenticate(username='admin', password='DevAfrique2026!')
                if user_auth:
                    self.stdout.write(self.style.SUCCESS("✓ Authentification admin OK"))
                else:
                    errors.append("Mot de passe admin incorrect")
                    self.stdout.write(self.style.ERROR("✗ Mot de passe admin INCORRECT"))
                    
                    if fix:
                        admin.set_password('DevAfrique2026!')
                        admin.save()
                        self.stdout.write(self.style.WARNING("  → Mot de passe réinitialisé"))
            else:
                errors.append("Admin n'existe pas")
                self.stdout.write(self.style.ERROR("✗ Admin n'existe PAS"))
                
                if fix:
                    admin = Utilisateur.objects.create_superuser(
                        username='admin',
                        email='admin@devafrique.com',
                        password='DevAfrique2026!',
                        role='administrateur'
                    )
                    self.stdout.write(self.style.WARNING("  → Admin créé"))
        except Exception as e:
            errors.append(f"Authentification: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))

        # 3. Création utilisateur test
        self.stdout.write("\n[3] CRÉATION UTILISATEUR TEST")
        try:
            test_user, created = Utilisateur.objects.get_or_create(
                username='test_diagnostic_render',
                defaults={
                    'email': 'test_render@devafrique.com',
                    'role': 'apprenant',
                }
            )
            if created:
                test_user.set_password('TestPass123!')
                test_user.save()
                self.stdout.write(self.style.SUCCESS("✓ Utilisateur test créé"))
            else:
                self.stdout.write("  Utilisateur test existant")
            
            # Test authentification utilisateur
            user_auth = authenticate(username='test_diagnostic_render', password='TestPass123!')
            if user_auth:
                self.stdout.write(self.style.SUCCESS("✓ Authentification utilisateur OK"))
            else:
                errors.append("Authentification utilisateur test échoue")
                self.stdout.write(self.style.ERROR("✗ Authentification échoue"))
                
                if fix:
                    test_user.set_password('TestPass123!')
                    test_user.save()
                    self.stdout.write(self.style.WARNING("  → Mot de passe réinitialisé"))
        except Exception as e:
            errors.append(f"Création utilisateur: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))

        # 4. Test related_name (source de l'erreur 500)
        self.stdout.write("\n[4] TEST RELATED_NAME 'progressions'")
        try:
            test_user = Utilisateur.objects.filter(username='test_diagnostic_render').first()
            if test_user:
                # Test accès à progressions
                progressions = test_user.progressions
                count = progressions.count()
                self.stdout.write(self.style.SUCCESS(f"✓ user.progressions accessible ({count} progressions)"))
            else:
                warnings.append("Pas d'utilisateur test pour vérifier progressions")
        except AttributeError as e:
            errors.append(f"Related_name 'progressions' manquant: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR related_name: {e}"))
        except Exception as e:
            errors.append(f"Test progressions: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))

        # 5. Test des vues avec requêtes simulées
        self.stdout.write("\n[5] TEST DES VUES")
        try:
            from pages.views import vue_accueil, vue_tableau_bord
            
            factory = RequestFactory()
            
            # Test vue_accueil anonyme
            request = factory.get('/')
            request.user = type('AnonymousUser', (), {'is_authenticated': False})()
            response = vue_accueil(request)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("✓ vue_accueil (anonyme) HTTP 200"))
            else:
                errors.append(f"vue_accueil anonyme HTTP {response.status_code}")
                self.stdout.write(self.style.ERROR(f"✗ vue_accueil HTTP {response.status_code}"))
            
            # Test vue_accueil authentifié
            test_user = Utilisateur.objects.filter(username='test_diagnostic_render').first()
            if test_user:
                request = factory.get('/')
                request.user = test_user
                
                # Ajouter session
                middleware = SessionMiddleware(lambda req: None)
                middleware.process_request(request)
                request.session.save()
                
                auth_middleware = AuthenticationMiddleware(lambda req: None)
                auth_middleware.process_request(request)
                
                try:
                    response = vue_accueil(request)
                    if response.status_code == 200:
                        self.stdout.write(self.style.SUCCESS("✓ vue_accueil (auth) HTTP 200"))
                    elif response.status_code == 302:
                        self.stdout.write(self.style.SUCCESS("✓ vue_accueil redirige (normal)"))
                    else:
                        errors.append(f"vue_accueil auth HTTP {response.status_code}")
                        self.stdout.write(self.style.ERROR(f"✗ vue_accueil auth HTTP {response.status_code}"))
                except Exception as e:
                    errors.append(f"vue_accueil auth: {e}")
                    self.stdout.write(self.style.ERROR(f"✗ ERREUR vue_accueil: {e}"))
        except Exception as e:
            errors.append(f"Test vues: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))

        # 6. Données glossaire
        self.stdout.write("\n[6] DONNÉES GLOSSAIRE")
        try:
            from glossaire.models import TermeGlossaire
            count = TermeGlossaire.objects.count()
            if count == 0:
                errors.append("Glossaire vide - aucun terme")
                self.stdout.write(self.style.ERROR(f"✗ Glossaire VIDE ({count} termes)"))
            elif count < 5:
                warnings.append(f"Glossaire peuplé ({count} termes)")
                self.stdout.write(self.style.WARNING(f"⚠ Glossaire incomplet ({count} termes)"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✓ Glossaire OK ({count} termes)"))
                
            # Test affichage glossaire
            termes = list(TermeGlossaire.objects.all()[:3])
            for terme in termes:
                self.stdout.write(f"  - {terme.terme}: {terme.definition[:40]}...")
        except Exception as e:
            errors.append(f"Glossaire: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))

        # 7. Données parcours et cours
        self.stdout.write("\n[7] DONNÉES COURS")
        try:
            from cours.models import Parcours, Cours, Lecon
            
            nb_parcours = Parcours.objects.count()
            nb_cours = Cours.objects.count()
            nb_lecons = Lecon.objects.count()
            
            self.stdout.write(f"  Parcours: {nb_parcours}")
            self.stdout.write(f"  Cours: {nb_cours}")
            self.stdout.write(f"  Leçons: {nb_lecons}")
            
            if nb_parcours == 0:
                errors.append("Aucun parcours")
                self.stdout.write(self.style.ERROR("✗ Aucun parcours"))
            elif nb_cours == 0:
                errors.append("Aucun cours")
                self.stdout.write(self.style.ERROR("✗ Aucun cours"))
            else:
                self.stdout.write(self.style.SUCCESS("✓ Données cours OK"))
                
            # Test affichage
            parcours = Parcours.objects.first()
            if parcours:
                cours_list = list(parcours.cours.all()[:3])
                self.stdout.write(f"  Parcours '{parcours.titre}': {len(cours_list)} cours")
        except Exception as e:
            errors.append(f"Données cours: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))

        # 8. Données forum
        self.stdout.write("\n[8] DONNÉES FORUM")
        try:
            from forum.models import SujetForum, ReponseForum
            
            nb_sujets = SujetForum.objects.count()
            nb_reponses = ReponseForum.objects.count()
            
            self.stdout.write(f"  Sujets: {nb_sujets}")
            self.stdout.write(f"  Réponses: {nb_reponses}")
            
            if nb_sujets == 0:
                warnings.append("Forum vide")
                self.stdout.write(self.style.WARNING("⚠ Forum vide"))
            else:
                self.stdout.write(self.style.SUCCESS("✓ Forum OK"))
        except Exception as e:
            errors.append(f"Forum: {e}")
            self.stdout.write(self.style.ERROR(f"✗ ERREUR: {e}"))

        # 9. Sessions Django
        self.stdout.write("\n[9] SESSIONS DJANGO")
        try:
            from django.contrib.sessions.models import Session
            from django.utils import timezone
            
            # Compter sessions actives
            sessions = Session.objects.filter(expire_date__gt=timezone.now())
            self.stdout.write(f"  Sessions actives: {sessions.count()}")
            self.stdout.write(self.style.SUCCESS("✓ Table sessions OK"))
        except Exception as e:
            warnings.append(f"Sessions: {e}")
            self.stdout.write(self.style.WARNING(f"⚠ Sessions: {e}"))

        # 10. Configuration sécurité
        self.stdout.write("\n[10] CONFIGURATION SÉCURITÉ")
        from django.conf import settings
        
        self.stdout.write(f"  DEBUG: {settings.DEBUG}")
        self.stdout.write(f"  SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', 'N/A')}")
        self.stdout.write(f"  SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', 'N/A')}")
        self.stdout.write(f"  CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', 'N/A')}")
        self.stdout.write(f"  CSRF_TRUSTED_ORIGINS: {getattr(settings, 'CSRF_TRUSTED_ORIGINS', [])}")
        
        if not settings.DEBUG:
            if getattr(settings, 'SESSION_COOKIE_SECURE', False):
                warnings.append("SESSION_COOKIE_SECURE=True peut causer problèmes sur Render")
            if getattr(settings, 'CSRF_COOKIE_SECURE', False):
                warnings.append("CSRF_COOKIE_SECURE=True peut causer problèmes sur Render")

        # RÉSUMÉ
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write("RÉSUMÉ")
        self.stdout.write("=" * 70)
        
        if errors:
            self.stdout.write(self.style.ERROR(f"\n✗ ERREURS ({len(errors)}):"))
            for err in errors:
                self.stdout.write(self.style.ERROR(f"  - {err}"))
        
        if warnings:
            self.stdout.write(self.style.WARNING(f"\n⚠ AVERTISSEMENTS ({len(warnings)}):"))
            for warn in warnings:
                self.stdout.write(self.style.WARNING(f"  - {warn}"))
        
        if not errors and not warnings:
            self.stdout.write(self.style.SUCCESS("\n✓ TOUT EST OK!"))
        elif not errors:
            self.stdout.write(self.style.WARNING("\n⚠ Quelques avertissements mais fonctionnel"))
        
        self.stdout.write("\n" + "=" * 70)
        
        # Cleanup
        try:
            Utilisateur.objects.filter(username='test_diagnostic_render').delete()
            self.stdout.write("  (Utilisateur test nettoyé)")
        except:
            pass

        return len(errors)
