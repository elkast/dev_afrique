# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from utilisateurs.models import Utilisateur
from cours.models import Parcours, Cours, Lecon


class Command(BaseCommand):
    help = 'Charge les données initiales du site'

    def handle(self, *args, **options):
        # Supprimer les anciennes données
        Lecon.objects.all().delete()
        Cours.objects.all().delete()
        Parcours.objects.all().delete()

        # Admin
        admin, cree = Utilisateur.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@devsanstabou.com',
                'role': 'administrateur',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if cree:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin cr\u00e9\u00e9 (admin / admin123)'))

        # Parcours Web
        parcours_web = Parcours.objects.create(
            titre='Parcours D\u00e9veloppement Web',
            slug='parcours-web',
            description='De z\u00e9ro \u00e0 h\u00e9ros : ma\u00eetrisez le frontend (HTML, CSS, JS, React, Tailwind) et le backend (Django, Flask, FastAPI). D\u00e9ployez vos projets sur Render et Neon.',
            type_parcours='web',
            icone='\U0001f310',
            ordre=1,
        )

        # Parcours Mobile
        parcours_mobile = Parcours.objects.create(
            titre='Parcours D\u00e9veloppement Mobile',
            slug='parcours-mobile',
            description='Cr\u00e9ez des applications mobiles avec React Native. Du JavaScript essentiel aux API REST, en passant par l\'architecture compl\u00e8te frontend/backend.',
            type_parcours='mobile',
            icone='\U0001f4f1',
            ordre=2,
        )

        # Cours Web
        cours_html = Cours.objects.create(
            parcours=parcours_web, titre='Les bases du HTML', slug='les-bases-html',
            description='Apprenez \u00e0 structurer une page web avec HTML. Les balises essentielles, les formulaires, les tableaux et la s\u00e9mantique.',
            icone='\U0001f3d7\ufe0f', ordre=1,
        )
        cours_css = Cours.objects.create(
            parcours=parcours_web, titre='Les bases du CSS', slug='les-bases-css',
            description='Stylisez vos pages web. Flexbox, Grid, responsive design, animations et bonnes pratiques.',
            icone='\U0001f3a8', ordre=2,
        )
        cours_js = Cours.objects.create(
            parcours=parcours_web, titre='JavaScript Essentiel', slug='javascript-essentiel',
            description='Les fondamentaux de JavaScript : variables, fonctions, DOM, \u00e9v\u00e9nements, fetch API, async/await.',
            icone='\u26a1', ordre=3,
        )
        cours_react = Cours.objects.create(
            parcours=parcours_web, titre='React pour le Frontend', slug='react-frontend',
            description='Construisez des interfaces modernes avec React. Composants, hooks, state management et routing.',
            icone='\u269b\ufe0f', ordre=4,
        )
        Cours.objects.create(
            parcours=parcours_web, titre='Tailwind CSS', slug='tailwind-css',
            description='Utilisez Tailwind CSS pour styliser vos applications React rapidement et efficacement.',
            icone='\U0001f4a8', ordre=5,
        )
        cours_django = Cours.objects.create(
            parcours=parcours_web, titre='Django \u2014 Backend Python', slug='django-backend',
            description='Cr\u00e9ez des API REST avec Django. Mod\u00e8les, vues, URLs, templates, authentification et base de donn\u00e9es.',
            icone='\U0001f40d', ordre=6,
        )
        Cours.objects.create(
            parcours=parcours_web, titre='Flask \u2014 Backend L\u00e9ger', slug='flask-backend',
            description='Un framework minimaliste pour cr\u00e9er des API rapidement. Routes, templates, SQLAlchemy.',
            icone='\U0001f9ea', ordre=7,
        )
        Cours.objects.create(
            parcours=parcours_web, titre='FastAPI \u2014 API Modernes', slug='fastapi-backend',
            description='Le framework Python le plus rapide pour les API. Typage, validation automatique, documentation Swagger.',
            icone='\U0001f680', ordre=8,
        )
        Cours.objects.create(
            parcours=parcours_web, titre='D\u00e9ploiement (Render & Neon)', slug='deploiement',
            description='Mettez vos projets en ligne. Render pour l\'h\u00e9bergement, Neon pour la base de donn\u00e9es PostgreSQL.',
            icone='\u2601\ufe0f', ordre=9,
        )
        Cours.objects.create(
            parcours=parcours_web, titre='Int\u00e9gration de l\'IA', slug='integration-ia',
            description='Ajoutez de l\'intelligence artificielle \u00e0 vos projets : API OpenAI, chatbots, g\u00e9n\u00e9ration de contenu.',
            icone='\U0001f916', ordre=10,
        )

        # Cours Mobile
        Cours.objects.create(
            parcours=parcours_mobile, titre='JavaScript pour le Mobile', slug='javascript-pour-mobile',
            description='Les concepts JS essentiels pour React Native : ES6+, modules, promesses, destructuration.',
            icone='\U0001f4f2', ordre=1,
        )
        Cours.objects.create(
            parcours=parcours_mobile, titre='React \u2014 Les Fondamentaux', slug='react-fondamentaux',
            description='Ma\u00eetrisez React avant de passer au mobile. Composants, hooks, state, props et lifecycle.',
            icone='\u269b\ufe0f', ordre=2,
        )
        Cours.objects.create(
            parcours=parcours_mobile, titre='React Native', slug='react-native',
            description='Cr\u00e9ez des applications iOS et Android avec React Native. Navigation, composants natifs, API.',
            icone='\U0001f4f1', ordre=3,
        )
        Cours.objects.create(
            parcours=parcours_mobile, titre='Architecture Frontend / Backend', slug='architecture-frontend-backend',
            description='Comprenez comment connecter votre app mobile \u00e0 un serveur. REST API, authentification, gestion des donn\u00e9es.',
            icone='\U0001f517', ordre=4,
        )

        self.stdout.write(self.style.SUCCESS('Tous les cours cr\u00e9\u00e9s'))

        # Lecons HTML
        Lecon.objects.create(
            cours=cours_html, titre='Introduction au HTML', slug='introduction-html', ordre=1,
            contenu='''<h2>Qu'est-ce que le HTML ?</h2>
<p><strong>HTML</strong> (HyperText Markup Language) est le langage de base de toute page web. Il d\u00e9finit la <strong>structure</strong> du contenu : les titres, les paragraphes, les images, les liens, etc.</p>

<div class="note-info">
<strong>\U0001f4a1 \u00c0 retenir :</strong> HTML n'est pas un langage de programmation. C'est un langage de <strong>balisage</strong> (markup). Il d\u00e9crit la structure, pas le comportement.
</div>

<h2>Votre premi\u00e8re page HTML</h2>
<p>Cr\u00e9ez un fichier <code>index.html</code> et copiez ce code :</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!DOCTYPE html&gt;
&lt;html lang="fr"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
    &lt;title&gt;Ma premi\u00e8re page&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Bonjour le monde !&lt;/h1&gt;
    &lt;p&gt;Ceci est ma premi\u00e8re page web.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
</div>

<h2>Explication ligne par ligne</h2>
<ul>
    <li><code>&lt;!DOCTYPE html&gt;</code> \u2014 Indique au navigateur que c'est du HTML5</li>
    <li><code>&lt;html lang="fr"&gt;</code> \u2014 L'\u00e9l\u00e9ment racine, en fran\u00e7ais</li>
    <li><code>&lt;head&gt;</code> \u2014 Contient les m\u00e9tadonn\u00e9es (titre, encodage, etc.)</li>
    <li><code>&lt;body&gt;</code> \u2014 Contient tout le contenu visible de la page</li>
    <li><code>&lt;h1&gt;</code> \u2014 Un titre de niveau 1 (le plus important)</li>
    <li><code>&lt;p&gt;</code> \u2014 Un paragraphe de texte</li>
</ul>

<div class="note-succes">
<strong>\u2705 Exercice :</strong> Ouvrez votre fichier <code>index.html</code> dans un navigateur. Modifiez le texte et rafra\u00eechissez la page pour voir les changements.
</div>''',
        )

        Lecon.objects.create(
            cours=cours_html, titre='Les balises HTML essentielles', slug='balises-html-essentielles', ordre=2,
            contenu='''<h2>Les balises les plus utilis\u00e9es</h2>
<p>Voici les balises que vous utiliserez dans 90% de vos pages :</p>

<h3>Titres (h1 \u00e0 h6)</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;h1&gt;Titre principal (un seul par page)&lt;/h1&gt;
&lt;h2&gt;Sous-titre&lt;/h2&gt;
&lt;h3&gt;Sous-sous-titre&lt;/h3&gt;
&lt;h4&gt;Titre de niveau 4&lt;/h4&gt;</pre>
</div>

<h3>Texte et mise en forme</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;p&gt;Un paragraphe de texte.&lt;/p&gt;
&lt;strong&gt;Texte en gras (important)&lt;/strong&gt;
&lt;em&gt;Texte en italique (emphase)&lt;/em&gt;
&lt;br&gt; &lt;!-- Retour \u00e0 la ligne --&gt;
&lt;hr&gt; &lt;!-- Ligne horizontale --&gt;</pre>
</div>

<h3>Liens et images</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- Lien --&gt;
&lt;a href="https://example.com"&gt;Cliquez ici&lt;/a&gt;

&lt;!-- Image --&gt;
&lt;img src="photo.jpg" alt="Description de l'image"&gt;

&lt;!-- Lien qui ouvre dans un nouvel onglet --&gt;
&lt;a href="https://example.com" target="_blank"&gt;Nouvel onglet&lt;/a&gt;</pre>
</div>

<h3>Listes</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- Liste non ordonn\u00e9e (\u00e0 puces) --&gt;
&lt;ul&gt;
    &lt;li&gt;Premier \u00e9l\u00e9ment&lt;/li&gt;
    &lt;li&gt;Deuxi\u00e8me \u00e9l\u00e9ment&lt;/li&gt;
&lt;/ul&gt;

&lt;!-- Liste ordonn\u00e9e (num\u00e9rot\u00e9e) --&gt;
&lt;ol&gt;
    &lt;li&gt;\u00c9tape 1&lt;/li&gt;
    &lt;li&gt;\u00c9tape 2&lt;/li&gt;
&lt;/ol&gt;</pre>
</div>

<div class="note-info">
<strong>\U0001f4a1 R\u00e8gle d'or :</strong> Chaque balise ouverte doit \u00eatre ferm\u00e9e. <code>&lt;p&gt;...&lt;/p&gt;</code>. Les balises auto-fermantes comme <code>&lt;br&gt;</code> et <code>&lt;img&gt;</code> sont des exceptions.
</div>''',
        )

        Lecon.objects.create(
            cours=cours_html, titre='Les formulaires HTML', slug='formulaires-html', ordre=3,
            contenu='''<h2>Cr\u00e9er un formulaire</h2>
<p>Les formulaires permettent aux utilisateurs d'envoyer des donn\u00e9es. C'est la base de toute application web interactive.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;form action="/envoyer" method="POST"&gt;
    &lt;label for="nom"&gt;Votre nom :&lt;/label&gt;
    &lt;input type="text" id="nom" name="nom" required&gt;

    &lt;label for="email"&gt;Votre email :&lt;/label&gt;
    &lt;input type="email" id="email" name="email" required&gt;

    &lt;label for="message"&gt;Message :&lt;/label&gt;
    &lt;textarea id="message" name="message" rows="4"&gt;&lt;/textarea&gt;

    &lt;button type="submit"&gt;Envoyer&lt;/button&gt;
&lt;/form&gt;</pre>
</div>

<h2>Les types d'input</h2>
<ul>
    <li><code>type="text"</code> \u2014 Champ texte simple</li>
    <li><code>type="email"</code> \u2014 Valide automatiquement le format email</li>
    <li><code>type="password"</code> \u2014 Masque le texte saisi</li>
    <li><code>type="number"</code> \u2014 Accepte uniquement des chiffres</li>
    <li><code>type="date"</code> \u2014 Affiche un s\u00e9lecteur de date</li>
    <li><code>type="checkbox"</code> \u2014 Case \u00e0 cocher</li>
    <li><code>type="radio"</code> \u2014 Bouton radio (choix unique)</li>
    <li><code>type="file"</code> \u2014 Upload de fichier</li>
</ul>

<h2>Attributs importants</h2>
<ul>
    <li><code>required</code> \u2014 Le champ est obligatoire</li>
    <li><code>placeholder</code> \u2014 Texte d'aide dans le champ</li>
    <li><code>name</code> \u2014 Le nom envoy\u00e9 au serveur (essentiel !)</li>
    <li><code>value</code> \u2014 La valeur par d\u00e9faut</li>
</ul>

<div class="note-info">
<strong>\U0001f4a1 Important :</strong> L'attribut <code>method="POST"</code> est utilis\u00e9 pour envoyer des donn\u00e9es sensibles. <code>method="GET"</code> met les donn\u00e9es dans l'URL (pour les recherches par exemple).
</div>''',
        )

        # Lecons JavaScript
        Lecon.objects.create(
            cours=cours_js, titre='Variables et types de donn\u00e9es', slug='variables-types-javascript', ordre=1,
            contenu='''<h2>D\u00e9clarer des variables</h2>
<p>En JavaScript moderne, on utilise <code>let</code> et <code>const</code>. Oubliez <code>var</code>.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// const : valeur qui ne change pas
const nom = "Alice";
const age = 25;
const estEtudiant = true;

// let : valeur qui peut changer
let compteur = 0;
compteur = compteur + 1; // OK

// \u274c Ceci provoque une erreur :
// const nom = "Bob"; // Impossible de r\u00e9assigner un const</pre>
</div>

<h2>Les types de donn\u00e9es</h2>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// String (texte)
const message = "Bonjour";
const template = \`Salut \${nom}, tu as \${age} ans\`; // Template literal

// Number (nombre)
const prix = 19.99;
const quantite = 3;

// Boolean (vrai/faux)
const estConnecte = true;

// Array (tableau)
const fruits = ["pomme", "banane", "orange"];
console.log(fruits[0]); // "pomme"
console.log(fruits.length); // 3

// Object (objet)
const utilisateur = {
    nom: "Alice",
    age: 25,
    email: "alice@email.com"
};
console.log(utilisateur.nom); // "Alice"</pre>
</div>

<div class="note-info">
<strong>\U0001f4a1 R\u00e8gle simple :</strong> Utilisez <code>const</code> par d\u00e9faut. Utilisez <code>let</code> uniquement si la valeur doit changer. N'utilisez jamais <code>var</code>.
</div>''',
        )

        Lecon.objects.create(
            cours=cours_js, titre='Fonctions et fonctions fl\u00e9ch\u00e9es', slug='fonctions-javascript', ordre=2,
            contenu='''<h2>D\u00e9clarer une fonction</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// Fonction classique
function saluer(nom) {
    return \`Bonjour, \${nom} !\`;
}

// Fonction fl\u00e9ch\u00e9e (arrow function) \u2014 la syntaxe moderne
const saluer2 = (nom) => {
    return \`Bonjour, \${nom} !\`;
};

// Version courte (une seule expression)
const saluer3 = (nom) => \`Bonjour, \${nom} !\`;

// Utilisation
console.log(saluer("Alice")); // "Bonjour, Alice !"</pre>
</div>

<h2>Fonctions avec plusieurs param\u00e8tres</h2>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>const calculerPrix = (prix, quantite, reduction = 0) => {
    const total = prix * quantite;
    return total - (total * reduction / 100);
};

console.log(calculerPrix(10, 3));       // 30
console.log(calculerPrix(10, 3, 20));   // 24 (20% de r\u00e9duction)</pre>
</div>

<h2>M\u00e9thodes de tableaux (tr\u00e8s utilis\u00e9es)</h2>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>const nombres = [1, 2, 3, 4, 5];

// map : transformer chaque \u00e9l\u00e9ment
const doubles = nombres.map(n => n * 2);
// [2, 4, 6, 8, 10]

// filter : garder certains \u00e9l\u00e9ments
const pairs = nombres.filter(n => n % 2 === 0);
// [2, 4]

// find : trouver un \u00e9l\u00e9ment
const premier = nombres.find(n => n > 3);
// 4

// forEach : parcourir sans retourner
nombres.forEach(n => console.log(n));</pre>
</div>

<div class="note-succes">
<strong>\u2705 Les 3 m\u00e9thodes \u00e0 ma\u00eetriser :</strong> <code>map</code>, <code>filter</code> et <code>find</code>. Elles sont utilis\u00e9es partout en React.
</div>''',
        )

        # Lecons Django
        Lecon.objects.create(
            cours=cours_django, titre='Introduction \u00e0 Django', slug='introduction-django', ordre=1,
            contenu='''<h2>Qu'est-ce que Django ?</h2>
<p><strong>Django</strong> est un framework web Python qui permet de cr\u00e9er des applications web rapidement. Il suit le principe <strong>"Don't Repeat Yourself"</strong> (DRY).</p>

<h2>Installation</h2>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Cr\u00e9er un environnement virtuel
python -m venv env

# Activer l'environnement (Windows)
env\\Scripts\\activate

# Activer l'environnement (Mac/Linux)
source env/bin/activate

# Installer Django
pip install django

# Cr\u00e9er un projet
django-admin startproject monprojet .

# Lancer le serveur
python manage.py runserver</pre>
</div>

<div class="note-info">
<strong>\U0001f4a1 Important :</strong> Le point <code>.</code> \u00e0 la fin de <code>startproject</code> cr\u00e9e le projet dans le dossier courant au lieu de cr\u00e9er un sous-dossier suppl\u00e9mentaire.
</div>

<h2>Structure d'un projet Django</h2>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Structure</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>monprojet/
\u251c\u2500\u2500 manage.py          # Commandes Django
\u251c\u2500\u2500 monprojet/
\u2502   \u251c\u2500\u2500 settings.py    # Configuration du projet
\u2502   \u251c\u2500\u2500 urls.py        # Routes principales
\u2502   \u251c\u2500\u2500 wsgi.py        # Point d'entr\u00e9e serveur
\u2502   \u2514\u2500\u2500 __init__.py
\u2514\u2500\u2500 db.sqlite3         # Base de donn\u00e9es (cr\u00e9\u00e9e automatiquement)</pre>
</div>

<h2>Cr\u00e9er une application</h2>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Cr\u00e9er une app
python manage.py startapp blog

# N'oubliez pas d'ajouter l'app dans settings.py :
# INSTALLED_APPS = [..., 'blog']</pre>
</div>

<div class="note-succes">
<strong>\u2705 Concept cl\u00e9 :</strong> Un <strong>projet</strong> Django contient plusieurs <strong>applications</strong>. Chaque app g\u00e8re une fonctionnalit\u00e9 (blog, utilisateurs, produits, etc.).
</div>''',
        )

        Lecon.objects.create(
            cours=cours_django, titre='Mod\u00e8les et base de donn\u00e9es', slug='modeles-django', ordre=2,
            contenu='''<h2>Cr\u00e9er un mod\u00e8le</h2>
<p>Un mod\u00e8le Django est une classe Python qui repr\u00e9sente une table dans la base de donn\u00e9es.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python \u2014 blog/models.py</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>from django.db import models

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.CharField(max_length=100)
    date_publication = models.DateTimeField(auto_now_add=True)
    est_publie = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre</pre>
</div>

<h2>Types de champs courants</h2>
<ul>
    <li><code>CharField</code> \u2014 Texte court (max_length obligatoire)</li>
    <li><code>TextField</code> \u2014 Texte long</li>
    <li><code>IntegerField</code> \u2014 Nombre entier</li>
    <li><code>BooleanField</code> \u2014 Vrai/Faux</li>
    <li><code>DateTimeField</code> \u2014 Date et heure</li>
    <li><code>EmailField</code> \u2014 Email valid\u00e9</li>
    <li><code>URLField</code> \u2014 URL valid\u00e9e</li>
    <li><code>ForeignKey</code> \u2014 Relation vers un autre mod\u00e8le</li>
</ul>

<h2>Appliquer les migrations</h2>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Cr\u00e9er les fichiers de migration
python manage.py makemigrations

# Appliquer les migrations \u00e0 la base de donn\u00e9es
python manage.py migrate</pre>
</div>

<h2>Utiliser les mod\u00e8les (CRUD)</h2>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Cr\u00e9er
article = Article.objects.create(
    titre="Mon premier article",
    contenu="Contenu de l'article...",
    auteur="Alice"
)

# Lire tous
articles = Article.objects.all()

# Lire avec filtre
publies = Article.objects.filter(est_publie=True)

# Lire un seul
article = Article.objects.get(id=1)

# Modifier
article.titre = "Titre modifi\u00e9"
article.save()

# Supprimer
article.delete()</pre>
</div>

<div class="note-info">
<strong>\U0001f4a1 CRUD :</strong> Create (cr\u00e9er), Read (lire), Update (modifier), Delete (supprimer). C'est la base de toute application.
</div>''',
        )

        self.stdout.write(self.style.SUCCESS('Toutes les le\u00e7ons cr\u00e9\u00e9es'))
        self.stdout.write(self.style.SUCCESS('\n\U0001f389 Donn\u00e9es initiales charg\u00e9es avec succ\u00e8s !'))
        self.stdout.write('Connectez-vous avec : admin / admin123')
