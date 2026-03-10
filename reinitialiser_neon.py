#!/usr/bin/env python
"""
Script de réinitialisation complète pour Render.
À exécuter sur Render pour tout réinitialiser proprement.
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteweb.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

print("=" * 60)
print("REINITIALISATION COMPLETE DE LA BASE NEON")
print("=" * 60)

# Étape 1: Supprimer toutes les tables
print("\n[1] Suppression des tables existantes...")
from django.db import connection

with connection.cursor() as cursor:
    # Liste des tables à supprimer (dans l'ordre inverse des dépendances)
    tables_to_drop = [
        'cours_progressionutilisateur',
        'cours_certificat',
        'cours_commentaire',
        'cours_lecon',
        'cours_cours',
        'cours_parcours',
        'glossaire_termeglossaire',
        'forum_reponseforum',
        'forum_sujetforum',
        'projets_projetcommunautaire',
        'projets_commentaireprojet',
        'utilisateurs_utilisateur_groups',
        'utilisateurs_utilisateur_user_permissions',
        'utilisateurs_utilisateur',
        'dmz_ipbloquee',
        'dmz_journalacces',
        'administration_ipbloquee',
        'administration_journalacces',
        'django_migrations',
        'django_session',
        'django_content_type',
        'auth_permission',
        'auth_group_permissions',
        'auth_group',
    ]
    
    for table in tables_to_drop:
        try:
            cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
            print(f"  ✓ {table} supprimée")
        except Exception as e:
            print(f"  - {table} (n'existait pas)")

print("\n[2] Suppression des migrations enregistrées...")
with connection.cursor() as cursor:
    try:
        cursor.execute("DELETE FROM django_migrations WHERE app IN ('cours', 'utilisateurs', 'glossaire', 'forum', 'projets')")
        print("  ✓ Migrations supprimées")
    except:
        print("  - Pas de migrations à supprimer")

print("\n[3] Recréation des tables (migrate)...")
from django.core.management import call_command
call_command('migrate', verbosity=0)
print("  ✓ Migrate terminé")

print("\n[4] Chargement des données initiales...")

# Créer admin
from utilisateurs.models import Utilisateur
admin, cree = Utilisateur.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@devafrique.com',
        'role': 'administrateur',
        'is_staff': True,
        'is_superuser': True,
    }
)
if cree:
    admin.set_password('DevAfrique2026!')
    admin.save()
    print("  ✓ Admin créé")
else:
    admin.set_password('DevAfrique2026!')
    admin.save()
    print("  ✓ Admin mis à jour")

# Créer parcours
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
print(f"  ✓ Parcours Web")

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
print(f"  ✓ Parcours Mobile")

# Cours Web
cours_data_web = [
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

for slug, titre, desc, icone, ordre, niveau in cours_data_web:
    Cours.objects.get_or_create(slug=slug, defaults={
        'parcours': parcours_web, 'titre': titre, 'description': desc,
        'icone': icone, 'ordre': ordre, 'niveau': niveau, 'auteur': admin,
    })
print(f"  ✓ {len(cours_data_web)} cours Web")

# Cours Mobile
cours_data_mobile = [
    ('javascript-pour-mobile', 'JavaScript pour le Mobile', 'JS pour React Native.', '📲', 1, 'debutant'),
    ('react-fondamentaux', 'React — Les Fondamentaux', 'React de base.', '⚛️', 2, 'intermediaire'),
    ('react-native', 'React Native', 'Apps iOS/Android.', '📱', 3, 'intermediaire'),
    ('architecture-frontend-backend', 'Architecture Frontend/Backend', 'Connectez app au serveur.', '🔗', 4, 'avance'),
]

for slug, titre, desc, icone, ordre, niveau in cours_data_mobile:
    Cours.objects.get_or_create(slug=slug, defaults={
        'parcours': parcours_mobile, 'titre': titre, 'description': desc,
        'icone': icone, 'ordre': ordre, 'niveau': niveau, 'auteur': admin,
    })
print(f"  ✓ {len(cours_data_mobile)} cours Mobile")

# Glossaire
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
print(f"  ✓ {len(termes)} termes glossaire")

# Forum
from forum.models import SujetForum, ReponseForum
sujet1, cree = SujetForum.objects.get_or_create(
    slug='comment-commencer',
    defaults={
        'auteur': admin,
        'titre': 'Comment commencer le développement web ?',
        'contenu': 'Je suis débutant, par où commencer ?',
        'categorie': 'general',
        'est_epingle': True,
    }
)
if cree:
    ReponseForum.objects.create(
        sujet=sujet1,
        auteur=admin,
        contenu='Commencez par HTML, CSS, puis JavaScript !',
        est_solution=True,
    )
    sujet1.est_resolu = True
    sujet1.save()
print(f"  ✓ Forum")

print("\n[5] Vérification finale...")
print(f"  - Utilisateurs: {Utilisateur.objects.count()}")
print(f"  - Parcours: {Parcours.objects.count()}")
print(f"  - Cours: {Cours.objects.count()}")
print(f"  - Glossaire: {TermeGlossaire.objects.count()}")

# Test related_name
print("\n[6] Test related_name 'progressions'...")
try:
    test_user = Utilisateur.objects.create_user('test_related_temp', email='temp@test.com', password='test123')
    _ = test_user.progressions
    print("  ✓ related_name fonctionne!")
    test_user.delete()
except Exception as e:
    print(f"  ✗ ERREUR: {e}")

print("\n" + "=" * 60)
print("REINITIALISATION TERMINEE!")
print("=" * 60)
print("\n✓ Admin: admin / DevAfrique2026!")
print("✓ Toutes les données sont chargées")
print("✓ La connexion devrait fonctionner maintenant")
