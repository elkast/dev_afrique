"""
Script de création des données initiales pour DevAfrique.
Exécuter avec: python manage.py shell < donnees_initiales.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteweb.settings')
django.setup()

from utilisateurs.models import Utilisateur
from cours.models import Parcours, Cours, Lecon
from glossaire.models import TermeGlossaire
from forum.models import SujetForum, ReponseForum

# ─── Créer l'administrateur ─────────────────────────────────
admin, cree = Utilisateur.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@devafrique.com',
        'role': 'administrateur',
        'is_staff': True,
        'is_superuser': True,
        'pays': "Côte d'Ivoire",
        'ville': 'Abidjan',
        'biographie': 'Administrateur de DevAfrique. Passionné par la démocratisation du savoir technologique en Afrique.',
        'points_xp': 5000,
        'niveau': 'expert',
    }
)
if cree:
    admin.set_password('admin123')
    admin.save()
    print('✅ Administrateur créé (admin / admin123)')

# ─── Parcours Web ────────────────────────────────────────────
parcours_web, _ = Parcours.objects.get_or_create(
    slug='parcours-web',
    defaults={
        'titre': 'Parcours Développement Web',
        'description': 'De zéro à héros : maîtrisez le frontend (HTML, CSS, JS, React, Tailwind) et le backend (Django, Flask, FastAPI). Déployez vos projets.',
        'type_parcours': 'web',
        'icone': '🌐',
        'ordre': 1,
    }
)
print(f'✅ Parcours Web : {parcours_web.titre}')

# ─── Parcours Mobile ─────────────────────────────────────────
parcours_mobile, _ = Parcours.objects.get_or_create(
    slug='parcours-mobile',
    defaults={
        'titre': 'Parcours Développement Mobile',
        'description': "Créez des applications mobiles avec React Native. Du JavaScript essentiel aux API REST, en passant par l'architecture complète.",
        'type_parcours': 'mobile',
        'icone': '📱',
        'ordre': 2,
    }
)
print(f'✅ Parcours Mobile : {parcours_mobile.titre}')

# ─── Cours du parcours Web ───────────────────────────────────
cours_data_web = [
    ('les-bases-html', 'Les bases du HTML', 'Structurer une page web avec HTML. Balises essentielles, formulaires, tableaux et sémantique.', '🏗️', 1, 'debutant'),
    ('les-bases-css', 'Les bases du CSS', 'Stylisez vos pages web. Flexbox, Grid, responsive design, animations et bonnes pratiques.', '🎨', 2, 'debutant'),
    ('javascript-essentiel', 'JavaScript Essentiel', 'Les fondamentaux : variables, fonctions, DOM, événements, fetch API, async/await.', '⚡', 3, 'debutant'),
    ('react-frontend', 'React pour le Frontend', 'Construisez des interfaces modernes. Composants, hooks, state management et routing.', '⚛️', 4, 'intermediaire'),
    ('tailwind-css', 'Tailwind CSS', 'Utilisez Tailwind CSS pour styliser vos applications React rapidement.', '💨', 5, 'intermediaire'),
    ('django-backend', 'Django — Backend Python', 'Créez des API REST avec Django. Modèles, vues, URLs, templates, authentification.', '🐍', 6, 'intermediaire'),
    ('flask-backend', 'Flask — Backend Léger', 'Framework minimaliste pour des API rapides. Routes, templates, SQLAlchemy.', '🧪', 7, 'intermediaire'),
    ('fastapi-backend', 'FastAPI — API Modernes', 'Le framework Python le plus rapide. Typage, validation, documentation Swagger.', '🚀', 8, 'avance'),
    ('deploiement', 'Déploiement (Render & Neon)', 'Mettez vos projets en ligne. Render pour l\'hébergement, Neon pour PostgreSQL.', '☁️', 9, 'avance'),
    ('integration-ia', "Intégration de l'IA", 'Ajoutez de l\'IA à vos projets : API OpenAI, chatbots, génération de contenu.', '🤖', 10, 'avance'),
]

for slug, titre, desc, icone, ordre, niveau in cours_data_web:
    Cours.objects.get_or_create(slug=slug, defaults={
        'parcours': parcours_web, 'titre': titre, 'description': desc,
        'icone': icone, 'ordre': ordre, 'niveau': niveau, 'auteur': admin,
    })

# ─── Cours du parcours Mobile ────────────────────────────────
cours_data_mobile = [
    ('javascript-pour-mobile', 'JavaScript pour le Mobile', 'Concepts JS essentiels pour React Native : ES6+, modules, promesses.', '📲', 1, 'debutant'),
    ('react-fondamentaux', 'React — Les Fondamentaux', 'Maîtrisez React avant le mobile. Composants, hooks, state, props.', '⚛️', 2, 'intermediaire'),
    ('react-native', 'React Native', 'Créez des apps iOS et Android. Navigation, composants natifs, API.', '📱', 3, 'intermediaire'),
    ('architecture-frontend-backend', 'Architecture Frontend / Backend', 'Connectez votre app mobile à un serveur. REST API, authentification.', '🔗', 4, 'avance'),
]

for slug, titre, desc, icone, ordre, niveau in cours_data_mobile:
    Cours.objects.get_or_create(slug=slug, defaults={
        'parcours': parcours_mobile, 'titre': titre, 'description': desc,
        'icone': icone, 'ordre': ordre, 'niveau': niveau, 'auteur': admin,
    })

print('✅ Tous les cours créés')

# ─── Leçons du cours HTML (existantes) ───────────────────────
cours_html = Cours.objects.get(slug='les-bases-html')
lecons_html = [
    ('introduction-html', 'Introduction au HTML', 1, 15),
    ('balises-html-essentielles', 'Les balises HTML essentielles', 2, 20),
    ('formulaires-html', 'Les formulaires HTML', 3, 25),
]

for slug, titre, ordre, duree in lecons_html:
    Lecon.objects.get_or_create(slug=slug, defaults={
        'cours': cours_html, 'titre': titre, 'ordre': ordre,
        'duree_minutes': duree,
        'contenu': f'<h2>{titre}</h2><p>Contenu de la leçon à venir...</p>',
    })

# ─── Leçons du cours JavaScript ──────────────────────────────
cours_js = Cours.objects.get(slug='javascript-essentiel')
lecons_js = [
    ('variables-types-javascript', 'Variables et types de données', 1, 20),
    ('fonctions-javascript', 'Fonctions et fonctions fléchées', 2, 25),
]

for slug, titre, ordre, duree in lecons_js:
    Lecon.objects.get_or_create(slug=slug, defaults={
        'cours': cours_js, 'titre': titre, 'ordre': ordre,
        'duree_minutes': duree,
        'contenu': f'<h2>{titre}</h2><p>Contenu de la leçon à venir...</p>',
    })

# ─── Leçons du cours Django ──────────────────────────────────
cours_django = Cours.objects.get(slug='django-backend')
lecons_django = [
    ('introduction-django', 'Introduction à Django', 1, 20),
    ('modeles-django', 'Modèles et base de données', 2, 30),
]

for slug, titre, ordre, duree in lecons_django:
    Lecon.objects.get_or_create(slug=slug, defaults={
        'cours': cours_django, 'titre': titre, 'ordre': ordre,
        'duree_minutes': duree,
        'contenu': f'<h2>{titre}</h2><p>Contenu de la leçon à venir...</p>',
    })

print('✅ Leçons créées')

# ─── Glossaire du développement ──────────────────────────────
termes = [
    ('API', "Une API (Application Programming Interface) est un ensemble de règles qui permettent à deux logiciels de communiquer entre eux. Par exemple, quand votre application mobile affiche la météo, elle utilise l'API d'un service météo.", 'api', 'backend', '',  ''),
    ('HTML', "HTML (HyperText Markup Language) est le langage de base de toutes les pages web. Il permet de structurer le contenu : texte, images, liens, formulaires. C'est comme le squelette d'une page web.", 'html', 'frontend', '<h1>Bonjour le monde !</h1>\n<p>Ceci est un paragraphe.</p>', 'HTML'),
    ('CSS', "CSS (Cascading Style Sheets) est le langage qui permet de styliser une page web. Il contrôle les couleurs, les tailles, les espacements, les animations — tout ce qui rend une page belle.", 'css', 'frontend', 'h1 {\n  color: blue;\n  font-size: 2rem;\n}', 'CSS'),
    ('JavaScript', "JavaScript est un langage de programmation qui rend les pages web interactives. C'est avec JavaScript qu'on crée des boutons qui font quelque chose, des formulaires dynamiques, des animations.", 'javascript', 'frontend', "const saluer = (nom) => {\n  return `Bonjour, ${nom} !`;\n};\nconsole.log(saluer('Alice'));", 'JavaScript'),
    ('Framework', "Un framework est un ensemble d'outils et de règles prêts à l'emploi pour créer des applications plus rapidement. Exemples : Django (Python), React (JavaScript), Laravel (PHP).", 'framework', 'general', '', ''),
    ('Backend', "Le backend est la partie invisible d'un site web. C'est le serveur qui traite les données, gère la base de données et envoie les réponses au navigateur. Exemples : Django, Flask, FastAPI.", 'backend-terme', 'backend', '', ''),
    ('Frontend', "Le frontend est la partie visible d'un site web — ce que l'utilisateur voit et avec quoi il interagit. C'est construit avec HTML, CSS et JavaScript.", 'frontend-terme', 'frontend', '', ''),
    ('Base de données', "Une base de données est un système organisé pour stocker des informations. Par exemple, la liste des utilisateurs, les articles d'un blog, les commandes d'un magasin en ligne. Exemples : PostgreSQL, MySQL, SQLite.", 'base-de-donnees', 'base_donnees', '', ''),
    ('Git', "Git est un outil de gestion de versions. Il permet de sauvegarder l'historique de votre code, de travailler en équipe, et de revenir en arrière si vous faites une erreur.", 'git', 'devops', 'git init\ngit add .\ngit commit -m "Premier commit"', 'Terminal'),
    ('React', "React est une bibliothèque JavaScript créée par Facebook pour construire des interfaces utilisateur modernes. Elle est basée sur les composants réutilisables.", 'react', 'frontend', "function Bonjour({ nom }) {\n  return <h1>Bonjour, {nom} !</h1>;\n}", 'JSX'),
    ('Django', "Django est un framework web Python puissant et rapide. Il suit le principe 'batteries incluses' : il fournit tout ce dont vous avez besoin (admin, auth, ORM, etc.).", 'django-terme', 'backend', "from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.accueil, name='accueil'),\n]", 'Python'),
    ('Variable', "Une variable est un conteneur qui stocke une valeur. C'est comme une boîte étiquetée dans laquelle vous rangez une information.", 'variable', 'general', "# Python\nnom = 'Alice'\nage = 25\n\n// JavaScript\nconst nom = 'Alice';\nlet age = 25;", 'Python / JavaScript'),
    ('Fonction', "Une fonction est un bloc de code réutilisable qui effectue une tâche spécifique. Vous l'écrivez une fois et vous pouvez l'appeler autant de fois que nécessaire.", 'fonction', 'general', "# Python\ndef saluer(nom):\n    return f'Bonjour, {nom} !'\n\nprint(saluer('Alice'))", 'Python'),
    ('Responsive', "Un design responsive s'adapte automatiquement à la taille de l'écran (téléphone, tablette, ordinateur). C'est essentiel car la majorité des utilisateurs africains naviguent sur mobile.", 'responsive', 'design', "@media (max-width: 768px) {\n  .grille {\n    grid-template-columns: 1fr;\n  }\n}", 'CSS'),
    ('Déploiement', "Le déploiement consiste à mettre votre application en ligne pour que tout le monde puisse y accéder. C'est passer de 'ça marche sur mon ordinateur' à 'tout le monde peut l'utiliser'.", 'deploiement-terme', 'devops', '', ''),
    ('REST', "REST (Representational State Transfer) est un style d'architecture pour créer des API web. Les API REST utilisent les méthodes HTTP (GET, POST, PUT, DELETE) pour manipuler les données.", 'rest', 'backend', "# Django REST Framework\nfrom rest_framework import viewsets\n\nclass ArticleViewSet(viewsets.ModelViewSet):\n    queryset = Article.objects.all()\n    serializer_class = ArticleSerializer", 'Python'),
    ('DOM', "Le DOM (Document Object Model) est une représentation en mémoire de la structure d'une page web. JavaScript utilise le DOM pour modifier dynamiquement le contenu d'une page.", 'dom', 'frontend', "// Sélectionner un élément\nconst titre = document.querySelector('h1');\n\n// Modifier son contenu\ntitre.textContent = 'Nouveau titre';", 'JavaScript'),
    ('Composant', "Un composant est un morceau d'interface réutilisable. En React, par exemple, un bouton, une carte, un formulaire sont des composants. On les assemble pour créer des pages complètes.", 'composant', 'frontend', "function Carte({ titre, description }) {\n  return (\n    <div className='carte'>\n      <h3>{titre}</h3>\n      <p>{description}</p>\n    </div>\n  );\n}", 'JSX'),
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

print('✅ Glossaire créé avec', TermeGlossaire.objects.count(), 'termes')

# ─── Sujets forum de démonstration ───────────────────────────
sujet1, cree = SujetForum.objects.get_or_create(
    slug='comment-commencer-le-developpement-web',
    defaults={
        'auteur': admin,
        'titre': 'Comment commencer le développement web en 2026 ?',
        'contenu': "Bonjour à tous ! Je suis débutant complet et je veux apprendre le développement web. Par où commencer ? HTML puis CSS puis JavaScript, c'est le bon ordre ? Merci pour vos conseils !",
        'categorie': 'general',
        'est_epingle': True,
    }
)
if cree:
    ReponseForum.objects.create(
        sujet=sujet1,
        auteur=admin,
        contenu="Bienvenue ! Oui, le parcours classique est : HTML → CSS → JavaScript → React → Backend (Django). Suis le Parcours Web Complet sur la plateforme, c'est exactement dans le bon ordre. Bon courage !",
        est_solution=True,
    )
    sujet1.est_resolu = True
    sujet1.save()

sujet2, _ = SujetForum.objects.get_or_create(
    slug='difference-entre-let-et-const',
    defaults={
        'auteur': admin,
        'titre': 'Quelle est la différence entre let et const en JavaScript ?',
        'contenu': "Je n'arrive pas à comprendre quand utiliser `let` et quand utiliser `const` en JavaScript. Quelqu'un peut m'expliquer simplement ?",
        'categorie': 'javascript',
    }
)

print('✅ Sujets forum créés')

print('\\n🎉 Données initiales DevAfrique chargées avec succès !')
print('Connectez-vous avec : admin / admin123')
print('\\n🌍 L\'Afrique mérite les meilleures formations !')
