# -*- coding: utf-8 -*-
"""
Commande unique qui initialise TOUTE la base de données sur Render.
Usage: python manage.py init_render
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()


class Command(BaseCommand):
    help = 'Initialise complètement la base Render (données + admin)'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("INITIALISATION RENDER COMPLETE")
        self.stdout.write("=" * 60)

        # 1. Admin
        self.stdout.write("\n[1] CREATION ADMIN...")
        admin, cree = Utilisateur.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@devafrique.com',
                'role': 'administrateur',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin.set_password('DevAfrique2026!')
        admin.save()
        self.stdout.write(self.style.SUCCESS(f"✓ Admin {'créé' if cree else 'mis à jour'}"))

        # 2. Parcours
        self.stdout.write("\n[2] CREATION PARCOURS...")
        from cours.models import Parcours, Cours, Lecon
        
        parcours_web, _ = Parcours.objects.get_or_create(
            slug='parcours-web',
            defaults={
                'titre': 'Parcours Développement Web',
                'description': 'De zéro à héros : maîtrisez le frontend et backend.',
                'type_parcours': 'web',
                'icone': '🌐',
                'ordre': 1,
            }
        )
        parcours_mobile, _ = Parcours.objects.get_or_create(
            slug='parcours-mobile',
            defaults={
                'titre': 'Parcours Développement Mobile',
                'description': 'Créez des applications mobiles avec React Native.',
                'type_parcours': 'mobile',
                'icone': '📱',
                'ordre': 2,
            }
        )
        self.stdout.write(self.style.SUCCESS("✓ 2 parcours créés"))

        # 3. Cours Web
        self.stdout.write("\n[3] CREATION COURS WEB...")
        cours_web_data = [
            ('les-bases-html', 'Les bases du HTML', 'Structurer une page web.', '🏗️', 1, 'debutant'),
            ('les-bases-css', 'Les bases du CSS', 'Stylisez vos pages.', '🎨', 2, 'debutant'),
            ('javascript-essentiel', 'JavaScript Essentiel', 'Variables, fonctions, DOM.', '⚡', 3, 'debutant'),
            ('react-frontend', 'React pour le Frontend', 'Interfaces modernes.', '⚛️', 4, 'intermediaire'),
            ('tailwind-css', 'Tailwind CSS', 'Stylisation rapide.', '💨', 5, 'intermediaire'),
            ('django-backend', 'Django — Backend Python', 'API REST avec Django.', '🐍', 6, 'intermediaire'),
            ('flask-backend', 'Flask — Backend Léger', 'API rapides.', '🧪', 7, 'intermediaire'),
            ('fastapi-backend', 'FastAPI — API Modernes', 'Framework rapide.', '🚀', 8, 'avance'),
            ('deploiement', 'Déploiement', 'Mettez en ligne.', '☁️', 9, 'avance'),
            ('integration-ia', "Intégration de l'IA", 'API OpenAI.', '🤖', 10, 'avance'),
        ]
        for slug, titre, desc, icone, ordre, niveau in cours_web_data:
            Cours.objects.get_or_create(slug=slug, defaults={
                'parcours': parcours_web, 'titre': titre, 'description': desc,
                'icone': icone, 'ordre': ordre, 'niveau': niveau, 'auteur': admin,
            })
        self.stdout.write(self.style.SUCCESS(f"✓ {len(cours_web_data)} cours Web"))

        # 4. Cours Mobile
        self.stdout.write("\n[4] CREATION COURS MOBILE...")
        cours_mobile_data = [
            ('javascript-pour-mobile', 'JavaScript pour le Mobile', 'JS pour React Native.', '📲', 1, 'debutant'),
            ('react-fondamentaux', 'React — Les Fondamentaux', 'React de base.', '⚛️', 2, 'intermediaire'),
            ('react-native', 'React Native', 'Apps iOS/Android.', '📱', 3, 'intermediaire'),
            ('architecture-frontend-backend', 'Architecture Frontend/Backend', 'Connectez app au serveur.', '🔗', 4, 'avance'),
        ]
        for slug, titre, desc, icone, ordre, niveau in cours_mobile_data:
            Cours.objects.get_or_create(slug=slug, defaults={
                'parcours': parcours_mobile, 'titre': titre, 'description': desc,
                'icone': icone, 'ordre': ordre, 'niveau': niveau, 'auteur': admin,
            })
        self.stdout.write(self.style.SUCCESS(f"✓ {len(cours_mobile_data)} cours Mobile"))

        # 5. Glossaire
        self.stdout.write("\n[5] CREATION GLOSSAIRE...")
        from glossaire.models import TermeGlossaire
        termes = [
            ('API', "Interface de communication entre logiciels.", 'api', 'backend', '', ''),
            ('HTML', "Langage de structure des pages web.", 'html', 'frontend', '<h1>Hello</h1>', 'HTML'),
            ('CSS', "Langage de style.", 'css', 'frontend', 'h1 { color: blue; }', 'CSS'),
            ('JavaScript', "Langage de programmation web.", 'javascript', 'frontend', 'console.log("hello")', 'JavaScript'),
            ('Framework', "Ensemble d'outils pour développer.", 'framework', 'general', '', ''),
            ('Backend', "Partie serveur invisible.", 'backend-terme', 'backend', '', ''),
            ('Frontend', "Partie visible du site.", 'frontend-terme', 'frontend', '', ''),
            ('Base de données', "Stockage organisé des données.", 'base-de-donnees', 'base_donnees', '', ''),
            ('Git', "Gestion de versions.", 'git', 'devops', 'git init', 'Terminal'),
            ('React', "Bibliothèque JS pour interfaces.", 'react', 'frontend', 'const App = () => <div />', 'JSX'),
            ('Django', "Framework Python.", 'django-terme', 'backend', 'from django import ...', 'Python'),
            ('Variable', "Conteneur de valeur.", 'variable', 'general', 'let x = 5', 'JavaScript'),
            ('Fonction', "Bloc de code réutilisable.", 'fonction', 'general', 'function f() {}', 'JavaScript'),
            ('Responsive', "Adaptation mobile/desktop.", 'responsive', 'design', '@media (min-width: 768px)', 'CSS'),
            ('Déploiement', "Mise en ligne.", 'deploiement-terme', 'devops', '', ''),
            ('REST', "Architecture API web.", 'rest', 'backend', 'GET /api/users', ''),
            ('DOM', "Représentation de la page.", 'dom', 'frontend', 'document.querySelector', 'JavaScript'),
            ('Composant', "Morceau d'interface.", 'composant', 'frontend', '<Button />', 'JSX'),
        ]
        for terme, definition, slug, categorie, exemple, langage in termes:
            TermeGlossaire.objects.get_or_create(
                slug=slug,
                defaults={
                    'terme': terme,
                    'definition': definition,
                    'categorie': categorie,
                    'exemple_code': exemple,
                    'langage_exemple': langage,
                }
            )
        self.stdout.write(self.style.SUCCESS(f"✓ {len(termes)} termes glossaire"))

        # 6. Forum
        self.stdout.write("\n[6] CREATION FORUM...")
        from forum.models import SujetForum, ReponseForum
        sujet, cree = SujetForum.objects.get_or_create(
            slug='bienvenue',
            defaults={
                'auteur': admin,
                'titre': 'Bienvenue sur DevAfrique !',
                'contenu': 'Posez vos questions ici.',
                'categorie': 'general',
                'est_epingle': True,
            }
        )
        if cree:
            ReponseForum.objects.create(
                sujet=sujet, auteur=admin,
                contenu='Bienvenue ! Comment pouvons-nous vous aider ?',
                est_solution=True,
            )
            sujet.est_resolu = True
            sujet.save()
        self.stdout.write(self.style.SUCCESS("✓ Forum initialisé"))

        # 7. Résumé
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("RESUME")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Utilisateurs: {Utilisateur.objects.count()}")
        self.stdout.write(f"Parcours: {Parcours.objects.count()}")
        self.stdout.write(f"Cours: {Cours.objects.count()}")
        self.stdout.write(f"Leçons: {Lecon.objects.count()}")
        self.stdout.write(f"Glossaire: {TermeGlossaire.objects.count()}")
        self.stdout.write(f"Sujets forum: {SujetForum.objects.count()}")
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("INITIALISATION TERMINEE!"))
        self.stdout.write("=" * 60)
        self.stdout.write("\n✓ Admin: admin / DevAfrique2026!")
        self.stdout.write("✓ Site prêt à l'emploi")
