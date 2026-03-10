"""
Script de création des 50 leçons détaillées pour DevAfrique.
Exécuter avec: python manage.py shell < donnees_lecons.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteweb.settings')
django.setup()

from cours.models import Cours, Lecon

# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════

def creer_lecon(cours_slug, slug, titre, ordre, duree, contenu):
    try:
        cours = Cours.objects.get(slug=cours_slug)
    except Cours.DoesNotExist:
        print(f'⚠️ Cours {cours_slug} introuvable, leçon ignorée: {titre}')
        return
    _, cree = Lecon.objects.update_or_create(
        slug=slug,
        defaults={
            'cours': cours,
            'titre': titre,
            'ordre': ordre,
            'duree_minutes': duree,
            'contenu': contenu,
            'est_publie': True,
        }
    )
    action = 'créée' if cree else 'mise à jour'
    print(f'  ✅ [{cours_slug}] {titre} ({action})')


# ═══════════════════════════════════════════════════════════════
#  COURS 1: LES BASES DU HTML (7 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n📖 Cours: Les bases du HTML')

creer_lecon('les-bases-html', 'introduction-html', 'Introduction au HTML', 1, 15, """
<h2>Qu'est-ce que le HTML ?</h2>
<p><strong>HTML</strong> (HyperText Markup Language) est le langage de base de toutes les pages web. C'est lui qui structure le contenu : texte, images, liens, formulaires. Imaginez HTML comme le <strong>squelette</strong> d'une page web.</p>

<div class="note-info">
    <strong>💡 Bon à savoir :</strong> HTML n'est pas un langage de programmation mais un langage de <strong>balisage</strong>. Il ne fait pas de calculs, il organise le contenu.
</div>

<h3>Votre première page HTML</h3>
<p>Créez un fichier <code>index.html</code> et tapez ceci :</p>
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
    &lt;title&gt;Ma première page&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Bonjour le monde !&lt;/h1&gt;
    &lt;p&gt;Ceci est ma première page web.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
</div>

<h3>Anatomie d'une balise HTML</h3>
<p>Une balise HTML a cette structure :</p>
<ul>
    <li><code>&lt;balise&gt;</code> — balise ouvrante</li>
    <li><code>&lt;/balise&gt;</code> — balise fermante</li>
    <li>Le contenu se place entre les deux</li>
    <li>Certaines balises sont <strong>auto-fermantes</strong> : <code>&lt;br&gt;</code>, <code>&lt;img&gt;</code>, <code>&lt;hr&gt;</code></li>
</ul>

<h3>Structure obligatoire</h3>
<p>Chaque page HTML doit avoir :</p>
<ul>
    <li><code>&lt;!DOCTYPE html&gt;</code> — déclare que c'est du HTML5</li>
    <li><code>&lt;html&gt;</code> — racine du document</li>
    <li><code>&lt;head&gt;</code> — métadonnées (titre, encodage, CSS)</li>
    <li><code>&lt;body&gt;</code> — le contenu visible</li>
</ul>

<blockquote>
    <strong>🎯 Exercice :</strong> Créez un fichier <code>index.html</code>, ouvrez-le dans votre navigateur. Modifiez le texte et rafraîchissez la page pour voir les changements.
</blockquote>
""")

creer_lecon('les-bases-html', 'balises-html-essentielles', 'Les balises HTML essentielles', 2, 20, """
<h2>Les balises de texte</h2>
<p>HTML fournit des balises pour structurer le texte de manière <strong>sémantique</strong> — c'est-à-dire que chaque balise a un sens.</p>

<h3>Titres : h1 à h6</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;h1&gt;Titre principal (un seul par page)&lt;/h1&gt;
&lt;h2&gt;Sous-titre&lt;/h2&gt;
&lt;h3&gt;Sous-sous-titre&lt;/h3&gt;
&lt;h4&gt;Titre de section&lt;/h4&gt;
&lt;h5&gt;Petit titre&lt;/h5&gt;
&lt;h6&gt;Très petit titre&lt;/h6&gt;</pre>
</div>

<div class="note-info">
    <strong>⚠️ Règle importante :</strong> N'utilisez jamais <code>&lt;h1&gt;</code> plus d'une fois par page. C'est important pour le <strong>référencement (SEO)</strong> et l'accessibilité.
</div>

<h3>Paragraphes et mise en forme</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;p&gt;Un paragraphe de texte normal.&lt;/p&gt;
&lt;p&gt;Du texte &lt;strong&gt;en gras&lt;/strong&gt; et &lt;em&gt;en italique&lt;/em&gt;.&lt;/p&gt;
&lt;p&gt;Un &lt;a href="https://example.com"&gt;lien hypertexte&lt;/a&gt;.&lt;/p&gt;
&lt;br&gt; &lt;!-- Retour à la ligne --&gt;
&lt;hr&gt; &lt;!-- Ligne horizontale --&gt;</pre>
</div>

<h3>Listes</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- Liste non ordonnée (points) --&gt;
&lt;ul&gt;
    &lt;li&gt;Premier élément&lt;/li&gt;
    &lt;li&gt;Deuxième élément&lt;/li&gt;
&lt;/ul&gt;

&lt;!-- Liste ordonnée (numéros) --&gt;
&lt;ol&gt;
    &lt;li&gt;Étape 1&lt;/li&gt;
    &lt;li&gt;Étape 2&lt;/li&gt;
&lt;/ol&gt;</pre>
</div>

<h3>Images</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;img src="photo.jpg" alt="Description de l'image" width="400"&gt;</pre>
</div>
<p>L'attribut <code>alt</code> est <strong>obligatoire</strong> — il décrit l'image pour les personnes malvoyantes et pour Google.</p>

<blockquote>
    <strong>🎯 Exercice :</strong> Créez une page de présentation personnelle avec un titre, un paragraphe de biographie, une liste de vos compétences et une image.
</blockquote>
""")

creer_lecon('les-bases-html', 'formulaires-html', 'Les formulaires HTML', 3, 25, """
<h2>Créer des formulaires</h2>
<p>Les formulaires permettent aux utilisateurs d'<strong>envoyer des données</strong> au serveur : inscription, connexion, recherche, commentaires...</p>

<h3>Structure d'un formulaire</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;form action="/inscription" method="POST"&gt;
    &lt;label for="nom"&gt;Votre nom :&lt;/label&gt;
    &lt;input type="text" id="nom" name="nom" placeholder="Jean Dupont" required&gt;

    &lt;label for="email"&gt;Email :&lt;/label&gt;
    &lt;input type="email" id="email" name="email" placeholder="jean@mail.com" required&gt;

    &lt;label for="mdp"&gt;Mot de passe :&lt;/label&gt;
    &lt;input type="password" id="mdp" name="mot_de_passe" minlength="8" required&gt;

    &lt;label for="message"&gt;Message :&lt;/label&gt;
    &lt;textarea id="message" name="message" rows="4"&gt;&lt;/textarea&gt;

    &lt;button type="submit"&gt;Envoyer&lt;/button&gt;
&lt;/form&gt;</pre>
</div>

<h3>Types d'input courants</h3>
<ul>
    <li><code>text</code> — texte libre</li>
    <li><code>email</code> — valide automatiquement le format email</li>
    <li><code>password</code> — masque les caractères</li>
    <li><code>number</code> — accepte uniquement des chiffres</li>
    <li><code>tel</code> — numéro de téléphone</li>
    <li><code>date</code> — sélecteur de date</li>
    <li><code>file</code> — upload de fichier</li>
    <li><code>checkbox</code> — case à cocher</li>
    <li><code>radio</code> — bouton radio (choix unique)</li>
</ul>

<h3>Sélection et listes déroulantes</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;select name="pays"&gt;
    &lt;option value=""&gt;Choisir un pays&lt;/option&gt;
    &lt;option value="ci"&gt;Côte d'Ivoire&lt;/option&gt;
    &lt;option value="sn"&gt;Sénégal&lt;/option&gt;
    &lt;option value="cm"&gt;Cameroun&lt;/option&gt;
    &lt;option value="ml"&gt;Mali&lt;/option&gt;
&lt;/select&gt;</pre>
</div>

<div class="note-info">
    <strong>🔒 Sécurité :</strong> Utilisez toujours <code>method="POST"</code> pour les formulaires sensibles (connexion, paiement). La méthode <code>GET</code> affiche les données dans l'URL.
</div>

<blockquote>
    <strong>🎯 Exercice :</strong> Créez un formulaire d'inscription complet avec nom, email, mot de passe, pays (liste déroulante), et un bouton d'envoi.
</blockquote>
""")

creer_lecon('les-bases-html', 'tableaux-html', 'Les tableaux HTML', 4, 20, """
<h2>Structurer des données avec les tableaux</h2>
<p>Les tableaux HTML servent à afficher des <strong>données tabulaires</strong> : résultats, comparaisons, statistiques.</p>

<h3>Structure d'un tableau</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;table&gt;
    &lt;thead&gt;
        &lt;tr&gt;
            &lt;th&gt;Langage&lt;/th&gt;
            &lt;th&gt;Type&lt;/th&gt;
            &lt;th&gt;Difficulté&lt;/th&gt;
        &lt;/tr&gt;
    &lt;/thead&gt;
    &lt;tbody&gt;
        &lt;tr&gt;
            &lt;td&gt;HTML&lt;/td&gt;
            &lt;td&gt;Balisage&lt;/td&gt;
            &lt;td&gt;Facile&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;Python&lt;/td&gt;
            &lt;td&gt;Programmation&lt;/td&gt;
            &lt;td&gt;Moyen&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;JavaScript&lt;/td&gt;
            &lt;td&gt;Programmation&lt;/td&gt;
            &lt;td&gt;Moyen&lt;/td&gt;
        &lt;/tr&gt;
    &lt;/tbody&gt;
&lt;/table&gt;</pre>
</div>

<h3>Éléments du tableau</h3>
<ul>
    <li><code>&lt;table&gt;</code> — conteneur du tableau</li>
    <li><code>&lt;thead&gt;</code> — en-tête du tableau</li>
    <li><code>&lt;tbody&gt;</code> — corps du tableau</li>
    <li><code>&lt;tr&gt;</code> — ligne (table row)</li>
    <li><code>&lt;th&gt;</code> — cellule d'en-tête (gras par défaut)</li>
    <li><code>&lt;td&gt;</code> — cellule de données</li>
</ul>

<h3>Fusion de cellules</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- Fusionner 2 colonnes --&gt;
&lt;td colspan="2"&gt;Cette cellule occupe 2 colonnes&lt;/td&gt;

&lt;!-- Fusionner 3 lignes --&gt;
&lt;td rowspan="3"&gt;Cette cellule occupe 3 lignes&lt;/td&gt;</pre>
</div>

<blockquote>
    <strong>🎯 Exercice :</strong> Créez un tableau comparatif de 5 langages de programmation avec leurs caractéristiques.
</blockquote>
""")

creer_lecon('les-bases-html', 'html-semantique', 'HTML sémantique et accessibilité', 5, 20, """
<h2>Le HTML sémantique</h2>
<p>Le HTML sémantique utilise des balises qui <strong>décrivent le sens</strong> du contenu, pas juste son apparence. C'est crucial pour le SEO et l'accessibilité.</p>

<h3>Balises sémantiques principales</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;header&gt;En-tête du site ou d'une section&lt;/header&gt;
&lt;nav&gt;Navigation principale&lt;/nav&gt;
&lt;main&gt;Contenu principal (un seul par page)&lt;/main&gt;
&lt;section&gt;Section thématique&lt;/section&gt;
&lt;article&gt;Contenu indépendant (blog post, news)&lt;/article&gt;
&lt;aside&gt;Contenu secondaire (sidebar)&lt;/aside&gt;
&lt;footer&gt;Pied de page&lt;/footer&gt;
&lt;figure&gt;Illustration avec légende&lt;/figure&gt;
&lt;figcaption&gt;Légende d'une figure&lt;/figcaption&gt;</pre>
</div>

<h3>Pourquoi c'est important ?</h3>
<ul>
    <li><strong>SEO</strong> — Google comprend mieux la structure de votre page</li>
    <li><strong>Accessibilité</strong> — Les lecteurs d'écran naviguent grâce aux balises sémantiques</li>
    <li><strong>Maintenance</strong> — Le code est plus lisible et maintenable</li>
</ul>

<h3>Exemple de page complète sémantique</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;body&gt;
    &lt;header&gt;
        &lt;nav&gt;
            &lt;a href="/"&gt;Accueil&lt;/a&gt;
            &lt;a href="/cours"&gt;Cours&lt;/a&gt;
        &lt;/nav&gt;
    &lt;/header&gt;

    &lt;main&gt;
        &lt;article&gt;
            &lt;h1&gt;Mon article&lt;/h1&gt;
            &lt;p&gt;Contenu de l'article...&lt;/p&gt;
            &lt;figure&gt;
                &lt;img src="image.jpg" alt="Description"&gt;
                &lt;figcaption&gt;Légende de l'image&lt;/figcaption&gt;
            &lt;/figure&gt;
        &lt;/article&gt;
        &lt;aside&gt;
            &lt;h2&gt;Articles similaires&lt;/h2&gt;
        &lt;/aside&gt;
    &lt;/main&gt;

    &lt;footer&gt;
        &lt;p&gt;&amp;copy; 2026 Mon Site&lt;/p&gt;
    &lt;/footer&gt;
&lt;/body&gt;</pre>
</div>

<div class="note-succes">
    <strong>✅ Bonne pratique :</strong> Utilisez toujours <code>&lt;main&gt;</code>, <code>&lt;nav&gt;</code>, <code>&lt;header&gt;</code>, <code>&lt;footer&gt;</code> au lieu de <code>&lt;div&gt;</code> quand c'est possible.
</div>

<blockquote>
    <strong>🎯 Exercice :</strong> Restructurez votre page de présentation en utilisant uniquement des balises sémantiques.
</blockquote>
""")

creer_lecon('les-bases-html', 'multimedia-html', 'Multimédia : images, audio et vidéo', 6, 20, """
<h2>Intégrer du multimédia</h2>
<p>HTML5 permet d'intégrer nativement des <strong>images, sons et vidéos</strong> sans plugin externe.</p>

<h3>Images avancées</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- Image responsive --&gt;
&lt;img src="photo.jpg"
     alt="Description détaillée"
     width="800"
     height="600"
     loading="lazy"&gt;

&lt;!-- Image avec figure --&gt;
&lt;figure&gt;
    &lt;img src="equipe.jpg" alt="Notre équipe"&gt;
    &lt;figcaption&gt;L'équipe DevAfrique à Abidjan&lt;/figcaption&gt;
&lt;/figure&gt;

&lt;!-- Images responsives avec srcset --&gt;
&lt;img srcset="photo-300.jpg 300w,
             photo-600.jpg 600w,
             photo-1200.jpg 1200w"
     sizes="(max-width: 600px) 300px, 600px"
     src="photo-600.jpg"
     alt="Photo responsive"&gt;</pre>
</div>

<h3>Vidéo</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;video controls width="640" poster="miniature.jpg"&gt;
    &lt;source src="video.mp4" type="video/mp4"&gt;
    &lt;source src="video.webm" type="video/webm"&gt;
    Votre navigateur ne supporte pas la vidéo HTML5.
&lt;/video&gt;

&lt;!-- Intégrer YouTube --&gt;
&lt;iframe width="560" height="315"
        src="https://www.youtube.com/embed/VIDEO_ID"
        allowfullscreen&gt;
&lt;/iframe&gt;</pre>
</div>

<h3>Audio</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;audio controls&gt;
    &lt;source src="musique.mp3" type="audio/mpeg"&gt;
    &lt;source src="musique.ogg" type="audio/ogg"&gt;
    Votre navigateur ne supporte pas l'audio.
&lt;/audio&gt;</pre>
</div>

<div class="note-info">
    <strong>⚡ Performance :</strong> Utilisez <code>loading="lazy"</code> sur les images pour qu'elles ne se chargent que quand elles sont visibles. Cela accélère votre page.
</div>
""")

creer_lecon('les-bases-html', 'projet-final-html', 'Projet final : Page portfolio', 7, 30, """
<h2>Projet : Créez votre portfolio</h2>
<p>Mettons en pratique tout ce que vous avez appris en créant une <strong>page portfolio complète</strong>.</p>

<h3>Objectif</h3>
<p>Créer une page web qui vous présente professionnellement avec :</p>
<ul>
    <li>Un en-tête avec navigation</li>
    <li>Une section "À propos" avec photo</li>
    <li>Un tableau de compétences</li>
    <li>Un formulaire de contact</li>
    <li>Un pied de page</li>
</ul>

<h3>Code complet du projet</h3>
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
    &lt;title&gt;Mon Portfolio&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;header&gt;
        &lt;nav&gt;
            &lt;a href="#apropos"&gt;À propos&lt;/a&gt;
            &lt;a href="#competences"&gt;Compétences&lt;/a&gt;
            &lt;a href="#contact"&gt;Contact&lt;/a&gt;
        &lt;/nav&gt;
    &lt;/header&gt;

    &lt;main&gt;
        &lt;section id="apropos"&gt;
            &lt;h1&gt;Bonjour, je suis [Votre Nom]&lt;/h1&gt;
            &lt;figure&gt;
                &lt;img src="photo.jpg" alt="Ma photo" width="200"&gt;
            &lt;/figure&gt;
            &lt;p&gt;Développeur web passionné, basé en [Ville, Pays].
            Je crée des sites web modernes et accessibles.&lt;/p&gt;
        &lt;/section&gt;

        &lt;section id="competences"&gt;
            &lt;h2&gt;Mes compétences&lt;/h2&gt;
            &lt;table&gt;
                &lt;thead&gt;
                    &lt;tr&gt;&lt;th&gt;Technologie&lt;/th&gt;&lt;th&gt;Niveau&lt;/th&gt;&lt;/tr&gt;
                &lt;/thead&gt;
                &lt;tbody&gt;
                    &lt;tr&gt;&lt;td&gt;HTML&lt;/td&gt;&lt;td&gt;Avancé&lt;/td&gt;&lt;/tr&gt;
                    &lt;tr&gt;&lt;td&gt;CSS&lt;/td&gt;&lt;td&gt;Intermédiaire&lt;/td&gt;&lt;/tr&gt;
                    &lt;tr&gt;&lt;td&gt;JavaScript&lt;/td&gt;&lt;td&gt;Débutant&lt;/td&gt;&lt;/tr&gt;
                &lt;/tbody&gt;
            &lt;/table&gt;
        &lt;/section&gt;

        &lt;section id="contact"&gt;
            &lt;h2&gt;Me contacter&lt;/h2&gt;
            &lt;form action="#" method="POST"&gt;
                &lt;label for="nom"&gt;Nom :&lt;/label&gt;
                &lt;input type="text" id="nom" name="nom" required&gt;

                &lt;label for="email"&gt;Email :&lt;/label&gt;
                &lt;input type="email" id="email" name="email" required&gt;

                &lt;label for="msg"&gt;Message :&lt;/label&gt;
                &lt;textarea id="msg" name="message" rows="5"&gt;&lt;/textarea&gt;

                &lt;button type="submit"&gt;Envoyer&lt;/button&gt;
            &lt;/form&gt;
        &lt;/section&gt;
    &lt;/main&gt;

    &lt;footer&gt;
        &lt;p&gt;&amp;copy; 2026 [Votre Nom] — Tous droits réservés&lt;/p&gt;
    &lt;/footer&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous avez terminé le cours HTML ! Vous savez maintenant structurer une page web complète. La prochaine étape : le <strong>CSS</strong> pour rendre votre page belle.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 2: LES BASES DU CSS (7 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n🎨 Cours: Les bases du CSS')

creer_lecon('les-bases-css', 'introduction-css', 'Introduction au CSS', 1, 15, """
<h2>Qu'est-ce que le CSS ?</h2>
<p><strong>CSS</strong> (Cascading Style Sheets) est le langage qui rend vos pages web <strong>belles</strong>. Il contrôle les couleurs, tailles, espacements, animations — tout ce qui concerne l'apparence.</p>

<h3>3 façons d'ajouter du CSS</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- 1. CSS externe (recommandé) --&gt;
&lt;link rel="stylesheet" href="styles.css"&gt;

&lt;!-- 2. CSS interne --&gt;
&lt;style&gt;
    h1 { color: blue; }
&lt;/style&gt;

&lt;!-- 3. CSS inline (à éviter) --&gt;
&lt;h1 style="color: blue;"&gt;Titre&lt;/h1&gt;</pre>
</div>

<h3>Syntaxe CSS</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>/* Sélecteur { propriété: valeur; } */
h1 {
    color: #6C5CE7;          /* Couleur du texte */
    font-size: 2rem;          /* Taille de police */
    font-weight: bold;        /* Graisse */
    margin-bottom: 1rem;      /* Marge extérieure bas */
    padding: 1rem;            /* Marge intérieure */
    background-color: #F8F8FA; /* Couleur de fond */
    border-radius: 8px;       /* Coins arrondis */
}</pre>
</div>

<h3>Sélecteurs principaux</h3>
<ul>
    <li><code>element</code> — sélectionne toutes les balises (ex: <code>p</code>, <code>h1</code>)</li>
    <li><code>.classe</code> — sélectionne par classe (ex: <code>.carte</code>)</li>
    <li><code>#id</code> — sélectionne par identifiant (ex: <code>#header</code>)</li>
    <li><code>parent enfant</code> — descendant (ex: <code>nav a</code>)</li>
    <li><code>element:hover</code> — au survol de la souris</li>
</ul>

<blockquote>
    <strong>🎯 Exercice :</strong> Créez un fichier <code>styles.css</code> et changez les couleurs et tailles de votre page HTML portfolio.
</blockquote>
""")

creer_lecon('les-bases-css', 'modele-boite-css', 'Le modèle de boîte (Box Model)', 2, 20, """
<h2>Comprendre le Box Model</h2>
<p>Chaque élément HTML est une <strong>boîte</strong>. Le Box Model définit comment cette boîte est construite :</p>
<ul>
    <li><strong>Content</strong> — le contenu (texte, image)</li>
    <li><strong>Padding</strong> — espace intérieur (entre contenu et bordure)</li>
    <li><strong>Border</strong> — la bordure</li>
    <li><strong>Margin</strong> — espace extérieur (entre la boîte et les autres éléments)</li>
</ul>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>/* Box Model en action */
.carte {
    width: 300px;
    padding: 20px;       /* Espace intérieur */
    border: 2px solid #E5E7EB;
    margin: 16px;        /* Espace extérieur */
    border-radius: 12px; /* Coins arrondis */
}

/* IMPORTANT: box-sizing fait que padding et border
   sont INCLUS dans la largeur */
* {
    box-sizing: border-box;
}

/* Raccourcis margin/padding */
.element {
    margin: 10px;            /* Tous les côtés */
    margin: 10px 20px;       /* Haut/Bas  Gauche/Droite */
    margin: 10px 20px 15px;  /* Haut  G/D  Bas */
    margin: 10px 20px 15px 5px; /* Haut Droite Bas Gauche */
    margin-top: 10px;        /* Un seul côté */
}</pre>
</div>

<div class="note-info">
    <strong>💡 Astuce :</strong> Ajoutez toujours <code>* { box-sizing: border-box; }</code> en début de votre CSS. Sans ça, les calculs de largeur deviennent compliqués.
</div>
""")

creer_lecon('les-bases-css', 'flexbox-css', 'Flexbox — Mise en page flexible', 3, 25, """
<h2>Maîtriser Flexbox</h2>
<p>Flexbox est la méthode moderne pour <strong>aligner et distribuer</strong> des éléments. C'est l'outil que vous utiliserez le plus en CSS.</p>

<h3>Activer Flexbox</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>.conteneur {
    display: flex;              /* Active Flexbox */
    justify-content: center;    /* Axe horizontal */
    align-items: center;        /* Axe vertical */
    gap: 1rem;                  /* Espace entre éléments */
}

/* justify-content: flex-start | center | flex-end |
   space-between | space-around | space-evenly */

/* align-items: flex-start | center | flex-end | stretch */

/* flex-direction: row | row-reverse | column | column-reverse */

/* flex-wrap: nowrap | wrap */</pre>
</div>

<h3>Exemple : Navbar</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>.navbar {
    display: flex;
    justify-content: space-between; /* Logo à gauche, liens à droite */
    align-items: center;
    padding: 1rem 2rem;
    background: #0B0B14;
}

.navbar-liens {
    display: flex;
    gap: 1.5rem;
    list-style: none;
}</pre>
</div>

<h3>Propriétés des enfants</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>.element {
    flex: 1;           /* Prend tout l'espace disponible */
    flex-grow: 1;      /* Grandir pour remplir */
    flex-shrink: 0;    /* Ne pas rétrécir */
    flex-basis: 200px; /* Taille de base */
    order: 2;          /* Changer l'ordre visuel */
}</pre>
</div>

<blockquote>
    <strong>🎯 Exercice :</strong> Créez une barre de navigation avec un logo à gauche et des liens à droite en utilisant Flexbox.
</blockquote>
""")

creer_lecon('les-bases-css', 'grid-css', 'CSS Grid — Grilles de mise en page', 4, 25, """
<h2>Créer des grilles avec CSS Grid</h2>
<p>CSS Grid est parfait pour les <strong>mises en page complexes</strong> en 2 dimensions (lignes ET colonnes).</p>

<h3>Activer CSS Grid</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>.grille {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* 3 colonnes égales */
    gap: 1.5rem;                           /* Espace entre cellules */
}

/* Colonnes de tailles différentes */
.grille-mixte {
    grid-template-columns: 250px 1fr 1fr; /* Sidebar fixe + 2 flexibles */
}

/* Responsive avec auto-fit */
.grille-responsive {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
}</pre>
</div>

<h3>Exemple : Page avec sidebar</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>.page-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
}

.header { grid-column: 1 / -1; } /* Occupe toute la largeur */
.sidebar { grid-row: 2; }
.contenu { grid-row: 2; }
.footer { grid-column: 1 / -1; }</pre>
</div>

<div class="note-info">
    <strong>💡 Flexbox vs Grid :</strong> Utilisez <strong>Flexbox</strong> pour aligner des éléments sur une ligne (navbar, boutons). Utilisez <strong>Grid</strong> pour des mises en page complètes (pages, grilles de cartes).
</div>
""")

creer_lecon('les-bases-css', 'responsive-design', 'Responsive Design et Media Queries', 5, 20, """
<h2>Rendre votre site adaptatif</h2>
<p>En Afrique, <strong>plus de 70% des utilisateurs</strong> naviguent sur mobile. Votre site DOIT s'adapter à toutes les tailles d'écran.</p>

<h3>La balise meta viewport</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- OBLIGATOIRE dans le &lt;head&gt; --&gt;
&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;</pre>
</div>

<h3>Media Queries</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>/* Mobile first: styles de base = mobile */
.grille {
    display: grid;
    grid-template-columns: 1fr; /* 1 colonne sur mobile */
    gap: 1rem;
}

/* Tablette (768px et plus) */
@media (min-width: 768px) {
    .grille {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Desktop (1024px et plus) */
@media (min-width: 1024px) {
    .grille {
        grid-template-columns: repeat(3, 1fr);
    }
    .sidebar { display: block; }
}

/* Cacher la sidebar sur mobile */
@media (max-width: 768px) {
    .sidebar { display: none; }
    .navbar-liens { display: none; }
    .menu-burger { display: block; }
}</pre>
</div>

<h3>Unités responsives</h3>
<ul>
    <li><code>rem</code> — relatif à la taille de police racine (16px par défaut)</li>
    <li><code>%</code> — pourcentage du parent</li>
    <li><code>vw / vh</code> — pourcentage de la fenêtre</li>
    <li><code>clamp(min, préféré, max)</code> — taille fluide avec limites</li>
</ul>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>h1 {
    /* S'adapte de 1.5rem à 3rem selon la taille d'écran */
    font-size: clamp(1.5rem, 5vw, 3rem);
}

img {
    max-width: 100%; /* Ne dépasse jamais son conteneur */
    height: auto;
}</pre>
</div>
""")

creer_lecon('les-bases-css', 'animations-transitions', 'Animations et transitions CSS', 6, 20, """
<h2>Donner vie à vos pages</h2>
<p>Les transitions et animations CSS rendent votre site plus <strong>professionnel</strong> et agréable à utiliser.</p>

<h3>Transitions</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>.bouton {
    background: #6C5CE7;
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    /* Transition fluide */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.bouton:hover {
    background: #5A4BD1;
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(108, 92, 231, 0.35);
}

.carte {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.carte:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}</pre>
</div>

<h3>Animations @keyframes</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>@keyframes apparaitre {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.anime {
    animation: apparaitre 0.6s ease forwards;
}

/* Animation de chargement */
@keyframes tourner {
    to { transform: rotate(360deg); }
}

.spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #E5E7EB;
    border-top-color: #6C5CE7;
    border-radius: 50%;
    animation: tourner 0.8s linear infinite;
}</pre>
</div>

<div class="note-info">
    <strong>⚡ Performance :</strong> Animez uniquement <code>transform</code> et <code>opacity</code> — ces propriétés sont accélérées par le GPU. Évitez d'animer <code>width</code>, <code>height</code> ou <code>margin</code>.
</div>
""")

creer_lecon('les-bases-css', 'projet-final-css', 'Projet final : Portfolio stylisé', 7, 30, """
<h2>Projet : Styliser votre portfolio</h2>
<p>Reprenez votre portfolio HTML et ajoutez un <strong>design professionnel</strong> avec CSS.</p>

<h3>Design System à utiliser</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">CSS</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>:root {
    --primaire: #6C5CE7;
    --primaire-clair: #A78BFA;
    --fond: #F8F8FA;
    --fond-surface: #FFFFFF;
    --texte: #111827;
    --texte-leger: #6B7280;
    --bordure: #E5E7EB;
    --rayon: 12px;
    --ombre: 0 4px 12px rgba(0,0,0,0.08);
    --transition: 0.3s ease;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Inter', sans-serif;
    background: var(--fond);
    color: var(--texte);
    line-height: 1.7;
}

.conteneur {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

.btn {
    background: var(--primaire);
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: var(--rayon);
    cursor: pointer;
    font-weight: 600;
    transition: all var(--transition);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(108, 92, 231, 0.35);
}</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous maîtrisez maintenant les bases du CSS ! Prochaine étape : <strong>JavaScript</strong> pour rendre votre site interactif.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 3: JAVASCRIPT ESSENTIEL (8 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n⚡ Cours: JavaScript Essentiel')

creer_lecon('javascript-essentiel', 'variables-types-javascript', 'Variables et types de données', 1, 20, """
<h2>Les variables en JavaScript</h2>
<p>Une variable est une <strong>boîte nommée</strong> qui stocke une valeur. JavaScript propose 3 mots-clés pour déclarer des variables.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// const — valeur qui ne change PAS (préféré)
const nom = "Aminata";
const age = 22;
const PI = 3.14159;

// let — valeur qui peut changer
let score = 0;
score = score + 10; // ✅ OK

// var — ancien, à ÉVITER
var ancienneVariable = "ne plus utiliser";</pre>
</div>

<h3>Types de données</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// String (texte)
const prenom = "Kofi";
const message = `Bonjour, ${prenom} !`; // Template literal

// Number (nombre)
const prix = 1500;
const temperature = -5.3;

// Boolean (vrai/faux)
const estConnecte = true;
const estAdmin = false;

// Array (tableau)
const fruits = ["mangue", "banane", "papaye"];
console.log(fruits[0]); // "mangue"
console.log(fruits.length); // 3

// Object (objet)
const utilisateur = {
    nom: "Aminata",
    age: 22,
    pays: "Côte d'Ivoire",
    competences: ["HTML", "CSS", "JavaScript"]
};
console.log(utilisateur.nom); // "Aminata"

// null — valeur vide volontaire
const resultat = null;

// undefined — pas encore de valeur
let adresse;</pre>
</div>

<div class="note-info">
    <strong>💡 Règle d'or :</strong> Utilisez <code>const</code> par défaut. Utilisez <code>let</code> uniquement si la valeur doit changer. N'utilisez <strong>jamais</strong> <code>var</code>.
</div>
""")

creer_lecon('javascript-essentiel', 'fonctions-javascript', 'Fonctions et fonctions fléchées', 2, 25, """
<h2>Les fonctions</h2>
<p>Une fonction est un <strong>bloc de code réutilisable</strong>. Vous l'écrivez une fois, vous l'appelez autant de fois que nécessaire.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// Déclaration classique
function saluer(nom) {
    return `Bonjour, ${nom} !`;
}

// Fonction fléchée (syntaxe moderne, préférée)
const saluer = (nom) => {
    return `Bonjour, ${nom} !`;
};

// Raccourci si une seule expression
const doubler = (n) => n * 2;

// Appel
console.log(saluer("Aminata")); // "Bonjour, Aminata !"
console.log(doubler(5));         // 10</pre>
</div>

<h3>Paramètres par défaut</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>const saluer = (nom = "visiteur") => `Bonjour, ${nom} !`;

console.log(saluer());        // "Bonjour, visiteur !"
console.log(saluer("Kofi"));  // "Bonjour, Kofi !"</pre>
</div>

<h3>Fonctions de tableau essentielles</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>const nombres = [1, 2, 3, 4, 5];

// map — transformer chaque élément
const doubles = nombres.map(n => n * 2);
// [2, 4, 6, 8, 10]

// filter — garder selon condition
const pairs = nombres.filter(n => n % 2 === 0);
// [2, 4]

// find — trouver le premier
const premier = nombres.find(n => n > 3);
// 4

// reduce — accumuler
const somme = nombres.reduce((acc, n) => acc + n, 0);
// 15

// forEach — parcourir
nombres.forEach(n => console.log(n));</pre>
</div>
""")

creer_lecon('javascript-essentiel', 'conditions-boucles-js', 'Conditions et boucles', 3, 20, """
<h2>Prendre des décisions avec les conditions</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>const age = 17;

// if / else if / else
if (age >= 18) {
    console.log("Majeur");
} else if (age >= 13) {
    console.log("Adolescent");
} else {
    console.log("Enfant");
}

// Opérateur ternaire (raccourci)
const statut = age >= 18 ? "Majeur" : "Mineur";

// Switch
const jour = "lundi";
switch (jour) {
    case "lundi":
    case "mardi":
        console.log("Début de semaine");
        break;
    case "vendredi":
        console.log("Bientôt le weekend !");
        break;
    default:
        console.log("Jour normal");
}</pre>
</div>

<h3>Les boucles</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// for classique
for (let i = 0; i < 5; i++) {
    console.log(i);
}

// for...of (parcourir un tableau)
const langages = ["Python", "JavaScript", "Dart"];
for (const lang of langages) {
    console.log(lang);
}

// for...in (parcourir les propriétés d'un objet)
const user = { nom: "Ali", age: 25 };
for (const cle in user) {
    console.log(`${cle}: ${user[cle]}`);
}

// while
let compteur = 0;
while (compteur < 3) {
    console.log(compteur);
    compteur++;
}</pre>
</div>
""")

creer_lecon('javascript-essentiel', 'dom-javascript', 'Manipuler le DOM', 4, 25, """
<h2>Le DOM : Document Object Model</h2>
<p>Le DOM est la <strong>représentation en mémoire</strong> de votre page HTML. JavaScript utilise le DOM pour modifier dynamiquement le contenu.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// SÉLECTIONNER des éléments
const titre = document.querySelector('h1');           // Premier h1
const boutons = document.querySelectorAll('.btn');     // Tous les .btn
const formulaire = document.getElementById('form-contact');

// MODIFIER le contenu
titre.textContent = 'Nouveau titre';    // Texte brut
titre.innerHTML = '&lt;span&gt;Titre&lt;/span&gt;';  // HTML

// MODIFIER les styles
titre.style.color = '#6C5CE7';
titre.style.fontSize = '2rem';

// AJOUTER / SUPPRIMER des classes
titre.classList.add('anime');
titre.classList.remove('cache');
titre.classList.toggle('actif');

// CRÉER un nouvel élément
const paragraphe = document.createElement('p');
paragraphe.textContent = 'Nouveau paragraphe';
document.body.appendChild(paragraphe);

// SUPPRIMER un élément
paragraphe.remove();</pre>
</div>

<h3>Exemple pratique : compteur</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>let compteur = 0;
const affichage = document.querySelector('#compteur');
const btnPlus = document.querySelector('#btn-plus');
const btnMoins = document.querySelector('#btn-moins');

btnPlus.addEventListener('click', () => {
    compteur++;
    affichage.textContent = compteur;
});

btnMoins.addEventListener('click', () => {
    compteur--;
    affichage.textContent = compteur;
});</pre>
</div>
""")

creer_lecon('javascript-essentiel', 'evenements-javascript', 'Les événements', 5, 20, """
<h2>Réagir aux actions de l'utilisateur</h2>
<p>Les événements permettent à votre code de <strong>réagir</strong> quand l'utilisateur fait quelque chose : clic, frappe clavier, scroll...</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// Clic
bouton.addEventListener('click', (e) => {
    console.log('Bouton cliqué !');
});

// Survol
carte.addEventListener('mouseenter', () => {
    carte.classList.add('survol');
});
carte.addEventListener('mouseleave', () => {
    carte.classList.remove('survol');
});

// Soumission de formulaire
formulaire.addEventListener('submit', (e) => {
    e.preventDefault(); // Empêcher le rechargement
    const donnees = new FormData(formulaire);
    console.log(donnees.get('email'));
});

// Frappe clavier
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        fermerModal();
    }
});

// Scroll
window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    if (scrollY > 100) {
        navbar.classList.add('scrolled');
    }
});</pre>
</div>

<div class="note-info">
    <strong>💡 e.preventDefault()</strong> empêche le comportement par défaut du navigateur. Par exemple, empêcher un formulaire de recharger la page.
</div>
""")

creer_lecon('javascript-essentiel', 'fetch-api-javascript', 'Fetch API et requêtes HTTP', 6, 25, """
<h2>Communiquer avec un serveur</h2>
<p><code>fetch()</code> permet d'envoyer des requêtes HTTP pour <strong>récupérer ou envoyer des données</strong> à un serveur.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// GET — Récupérer des données
const reponse = await fetch('https://api.example.com/cours');
const cours = await reponse.json();
console.log(cours);

// POST — Envoyer des données
const reponse = await fetch('/api/inscription', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({
        nom: 'Aminata',
        email: 'aminata@mail.com',
    }),
});
const resultat = await reponse.json();</pre>
</div>

<h3>Gestion des erreurs</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>const chargerDonnees = async () => {
    try {
        const reponse = await fetch('/api/donnees');
        if (!reponse.ok) {
            throw new Error(`Erreur HTTP: ${reponse.status}`);
        }
        const donnees = await reponse.json();
        afficherDonnees(donnees);
    } catch (erreur) {
        console.error('Erreur:', erreur.message);
        afficherErreur('Impossible de charger les données.');
    }
};</pre>
</div>
""")

creer_lecon('javascript-essentiel', 'async-await-javascript', 'Async/Await et Promesses', 7, 25, """
<h2>Le code asynchrone</h2>
<p>JavaScript est <strong>single-threaded</strong> — il ne fait qu'une chose à la fois. L'asynchrone permet de ne pas <strong>bloquer</strong> l'interface pendant les opérations longues (requêtes réseau, lecture fichier).</p>

<h3>Promesses</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// Créer une promesse
const attendre = (ms) => new Promise(resolve => {
    setTimeout(resolve, ms);
});

// Utiliser une promesse avec .then()
attendre(2000).then(() => {
    console.log('2 secondes écoulées !');
});

// Avec async/await (plus lisible)
const demarrer = async () => {
    console.log('Début...');
    await attendre(2000);
    console.log('2 secondes plus tard !');
};
demarrer();</pre>
</div>

<h3>Promise.all — requêtes parallèles</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// Charger plusieurs données EN MÊME TEMPS
const chargerTout = async () => {
    const [cours, projets, utilisateur] = await Promise.all([
        fetch('/api/cours').then(r => r.json()),
        fetch('/api/projets').then(r => r.json()),
        fetch('/api/utilisateur').then(r => r.json()),
    ]);
    // Les 3 requêtes sont terminées ici
    console.log(cours, projets, utilisateur);
};</pre>
</div>
""")

creer_lecon('javascript-essentiel', 'projet-final-js', 'Projet final : App de tâches', 8, 30, """
<h2>Projet : Todo App interactive</h2>
<p>Créez une application de gestion de tâches complète avec JavaScript pur.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// ─── Todo App ────────────────────────────────────
const formulaire = document.querySelector('#form-todo');
const input = document.querySelector('#input-todo');
const liste = document.querySelector('#liste-todos');

// Charger depuis localStorage
let todos = JSON.parse(localStorage.getItem('todos')) || [];

const sauvegarder = () => {
    localStorage.setItem('todos', JSON.stringify(todos));
};

const afficher = () => {
    liste.innerHTML = '';
    todos.forEach((todo, index) => {
        const li = document.createElement('li');
        li.className = todo.fait ? 'todo fait' : 'todo';
        li.innerHTML = `
            &lt;span onclick="basculer(${index})"&gt;${todo.texte}&lt;/span&gt;
            &lt;button onclick="supprimer(${index})"&gt;✕&lt;/button&gt;
        `;
        liste.appendChild(li);
    });
};

const ajouter = (texte) => {
    todos.push({ texte, fait: false });
    sauvegarder();
    afficher();
};

const basculer = (index) => {
    todos[index].fait = !todos[index].fait;
    sauvegarder();
    afficher();
};

const supprimer = (index) => {
    todos.splice(index, 1);
    sauvegarder();
    afficher();
};

formulaire.addEventListener('submit', (e) => {
    e.preventDefault();
    const texte = input.value.trim();
    if (texte) {
        ajouter(texte);
        input.value = '';
    }
});

afficher();</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous maîtrisez JavaScript ! Vous êtes prêt pour <strong>React</strong> et la construction d'interfaces modernes.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 4: REACT FRONTEND (7 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n⚛️ Cours: React pour le Frontend')

creer_lecon('react-frontend', 'introduction-react', 'Introduction à React', 1, 20, """
<h2>Qu'est-ce que React ?</h2>
<p><strong>React</strong> est une bibliothèque JavaScript créée par Facebook pour construire des interfaces utilisateur modernes. Elle est basée sur le concept de <strong>composants réutilisables</strong>.</p>

<h3>Pourquoi React ?</h3>
<ul>
    <li>Interfaces <strong>dynamiques</strong> et réactives</li>
    <li>Code <strong>réutilisable</strong> grâce aux composants</li>
    <li>Immense <strong>écosystème</strong> et communauté</li>
    <li>Utilisé par Facebook, Instagram, Airbnb, Netflix</li>
</ul>

<h3>Créer un projet React</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>npx create-react-app mon-app
cd mon-app
npm start</pre>
</div>

<h3>Premier composant</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JSX</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>function Bonjour({ nom }) {
    return (
        &lt;div&gt;
            &lt;h1&gt;Bonjour, {nom} !&lt;/h1&gt;
            &lt;p&gt;Bienvenue sur DevAfrique.&lt;/p&gt;
        &lt;/div&gt;
    );
}

// Utilisation
&lt;Bonjour nom="Aminata" /&gt;</pre>
</div>

<div class="note-info">
    <strong>💡 JSX</strong> c'est du HTML dans du JavaScript. Chaque composant retourne du JSX. Les expressions JavaScript s'écrivent entre accolades <code>{}</code>.
</div>
""")

creer_lecon('react-frontend', 'composants-props-react', 'Composants et Props', 2, 25, """
<h2>Découper votre interface en composants</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JSX</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// Composant Carte réutilisable
function Carte({ titre, description, icone, lien }) {
    return (
        &lt;a href={lien} className="carte"&gt;
            &lt;div className="carte-icone"&gt;{icone}&lt;/div&gt;
            &lt;h3&gt;{titre}&lt;/h3&gt;
            &lt;p&gt;{description}&lt;/p&gt;
        &lt;/a&gt;
    );
}

// Utilisation dans une page
function PageCours() {
    const cours = [
        { titre: "HTML", desc: "Les bases", icone: "🏗️", lien: "/html" },
        { titre: "CSS", desc: "Le style", icone: "🎨", lien: "/css" },
        { titre: "JS", desc: "L'interactif", icone: "⚡", lien: "/js" },
    ];

    return (
        &lt;div className="grille"&gt;
            {cours.map((c, i) => (
                &lt;Carte
                    key={i}
                    titre={c.titre}
                    description={c.desc}
                    icone={c.icone}
                    lien={c.lien}
                /&gt;
            ))}
        &lt;/div&gt;
    );
}</pre>
</div>
""")

creer_lecon('react-frontend', 'state-hooks-react', 'State et Hooks', 3, 25, """
<h2>Gérer l'état avec useState et useEffect</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JSX</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>import { useState, useEffect } from 'react';

function Compteur() {
    const [compteur, setCompteur] = useState(0);
    const [nom, setNom] = useState('');

    // useEffect — exécuter du code au montage / changement
    useEffect(() => {
        document.title = `Compteur: ${compteur}`;
    }, [compteur]); // Se déclenche quand compteur change

    return (
        &lt;div&gt;
            &lt;h2&gt;Compteur: {compteur}&lt;/h2&gt;
            &lt;button onClick={() => setCompteur(c => c + 1)}&gt;+1&lt;/button&gt;
            &lt;button onClick={() => setCompteur(c => c - 1)}&gt;-1&lt;/button&gt;
            &lt;button onClick={() => setCompteur(0)}&gt;Reset&lt;/button&gt;

            &lt;input
                value={nom}
                onChange={(e) => setNom(e.target.value)}
                placeholder="Votre nom"
            /&gt;
            &lt;p&gt;Bonjour, {nom || 'visiteur'} !&lt;/p&gt;
        &lt;/div&gt;
    );
}</pre>
</div>
""")

creer_lecon('react-frontend', 'fetch-donnees-react', 'Charger des données avec React', 4, 25, """
<h2>Requêtes API dans React</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JSX</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>import { useState, useEffect } from 'react';

function ListeCours() {
    const [cours, setCours] = useState([]);
    const [chargement, setChargement] = useState(true);
    const [erreur, setErreur] = useState(null);

    useEffect(() => {
        const charger = async () => {
            try {
                const rep = await fetch('/api/cours');
                if (!rep.ok) throw new Error('Erreur serveur');
                const donnees = await rep.json();
                setCours(donnees);
            } catch (err) {
                setErreur(err.message);
            } finally {
                setChargement(false);
            }
        };
        charger();
    }, []);

    if (chargement) return &lt;div className="spinner"&gt;&lt;/div&gt;;
    if (erreur) return &lt;div className="erreur"&gt;{erreur}&lt;/div&gt;;

    return (
        &lt;div className="grille"&gt;
            {cours.map(c => (
                &lt;Carte key={c.id} titre={c.titre} /&gt;
            ))}
        &lt;/div&gt;
    );
}</pre>
</div>
""")

creer_lecon('react-frontend', 'formulaires-react', 'Formulaires contrôlés', 5, 20, """
<h2>Gérer les formulaires dans React</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JSX</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>import { useState } from 'react';

function FormulaireInscription() {
    const [formData, setFormData] = useState({
        nom: '', email: '', motDePasse: ''
    });
    const [erreurs, setErreurs] = useState({});

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const valider = () => {
        const errs = {};
        if (!formData.nom) errs.nom = 'Nom requis';
        if (!formData.email.includes('@')) errs.email = 'Email invalide';
        if (formData.motDePasse.length &lt; 8) errs.motDePasse = 'Min 8 caractères';
        return errs;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const errs = valider();
        if (Object.keys(errs).length > 0) {
            setErreurs(errs);
            return;
        }
        // Envoyer au serveur
        const rep = await fetch('/api/inscription', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });
        // ...
    };

    return (
        &lt;form onSubmit={handleSubmit}&gt;
            &lt;input name="nom" value={formData.nom}
                   onChange={handleChange} placeholder="Nom" /&gt;
            {erreurs.nom && &lt;span className="erreur"&gt;{erreurs.nom}&lt;/span&gt;}
            {/* ... autres champs */}
            &lt;button type="submit"&gt;S'inscrire&lt;/button&gt;
        &lt;/form&gt;
    );
}</pre>
</div>
""")

creer_lecon('react-frontend', 'routing-react', 'Navigation avec React Router', 6, 20, """
<h2>Créer un site multi-pages avec React Router</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>npm install react-router-dom</pre>
</div>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JSX</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
    return (
        &lt;BrowserRouter&gt;
            &lt;nav&gt;
                &lt;Link to="/"&gt;Accueil&lt;/Link&gt;
                &lt;Link to="/cours"&gt;Cours&lt;/Link&gt;
                &lt;Link to="/profil"&gt;Profil&lt;/Link&gt;
            &lt;/nav&gt;

            &lt;Routes&gt;
                &lt;Route path="/" element={&lt;Accueil /&gt;} /&gt;
                &lt;Route path="/cours" element={&lt;ListeCours /&gt;} /&gt;
                &lt;Route path="/cours/:id" element={&lt;DetailCours /&gt;} /&gt;
                &lt;Route path="/profil" element={&lt;Profil /&gt;} /&gt;
                &lt;Route path="*" element={&lt;Page404 /&gt;} /&gt;
            &lt;/Routes&gt;
        &lt;/BrowserRouter&gt;
    );
}</pre>
</div>
""")

creer_lecon('react-frontend', 'projet-final-react', 'Projet final : Dashboard React', 7, 30, """
<h2>Projet : Tableau de bord en React</h2>
<p>Construisez un dashboard complet avec cartes de stats, liste de cours et formulaire de recherche.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JSX</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>function Dashboard() {
    const [stats, setStats] = useState(null);
    const [recherche, setRecherche] = useState('');

    useEffect(() => {
        fetch('/api/stats').then(r => r.json()).then(setStats);
    }, []);

    return (
        &lt;div className="dashboard"&gt;
            &lt;h1&gt;Tableau de bord&lt;/h1&gt;

            &lt;div className="stats-grille"&gt;
                &lt;StatCard titre="Cours" valeur={stats?.cours} /&gt;
                &lt;StatCard titre="Utilisateurs" valeur={stats?.users} /&gt;
                &lt;StatCard titre="Projets" valeur={stats?.projets} /&gt;
            &lt;/div&gt;

            &lt;input
                value={recherche}
                onChange={(e) => setRecherche(e.target.value)}
                placeholder="Rechercher..."
            /&gt;

            &lt;ListeCours filtre={recherche} /&gt;
        &lt;/div&gt;
    );
}</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous maîtrisez React ! Prochaine étape : <strong>Tailwind CSS</strong> pour styliser vos composants rapidement.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 5: TAILWIND CSS (4 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n💨 Cours: Tailwind CSS')

creer_lecon('tailwind-css', 'introduction-tailwind', 'Introduction à Tailwind CSS', 1, 20, """
<h2>Tailwind CSS : le CSS utilitaire</h2>
<p>Tailwind CSS est un framework CSS qui utilise des <strong>classes utilitaires</strong> pour styliser directement dans le HTML. Plus besoin d'écrire du CSS séparé !</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- Sans Tailwind --&gt;
&lt;button class="mon-bouton"&gt;Cliquez&lt;/button&gt;

&lt;!-- Avec Tailwind --&gt;
&lt;button class="bg-purple-600 text-white px-6 py-3 rounded-lg
               font-semibold hover:bg-purple-700
               transition-all shadow-md hover:shadow-lg
               hover:-translate-y-0.5"&gt;
    Cliquez
&lt;/button&gt;</pre>
</div>

<h3>Installation</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>npm install tailwindcss @tailwindcss/vite
npx tailwindcss init</pre>
</div>

<h3>Classes les plus utilisées</h3>
<ul>
    <li><code>p-4</code> padding, <code>m-4</code> margin, <code>gap-4</code> espace</li>
    <li><code>text-xl</code> taille, <code>font-bold</code> graisse, <code>text-gray-600</code> couleur</li>
    <li><code>bg-white</code> fond, <code>rounded-lg</code> coins arrondis</li>
    <li><code>flex</code> flexbox, <code>grid</code> grille, <code>items-center</code> alignement</li>
    <li><code>w-full</code> largeur 100%, <code>max-w-4xl</code> largeur max</li>
</ul>
""")

creer_lecon('tailwind-css', 'composants-tailwind', 'Créer des composants avec Tailwind', 2, 25, """
<h2>Composants réutilisables</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JSX</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>function Carte({ titre, description, icone }) {
    return (
        &lt;div className="bg-white rounded-xl border border-gray-100
                        p-6 hover:shadow-lg hover:-translate-y-1
                        transition-all duration-300"&gt;
            &lt;div className="w-12 h-12 bg-purple-100 text-purple-600
                            rounded-lg flex items-center justify-center
                            mb-4"&gt;
                {icone}
            &lt;/div&gt;
            &lt;h3 className="text-lg font-bold mb-2"&gt;{titre}&lt;/h3&gt;
            &lt;p className="text-gray-500 text-sm"&gt;{description}&lt;/p&gt;
        &lt;/div&gt;
    );
}

function Badge({ variante = 'primaire', children }) {
    const styles = {
        primaire: 'bg-purple-100 text-purple-700',
        succes: 'bg-green-100 text-green-700',
        danger: 'bg-red-100 text-red-700',
    };
    return (
        &lt;span className={`px-2 py-0.5 rounded-full text-xs
                          font-semibold ${styles[variante]}`}&gt;
            {children}
        &lt;/span&gt;
    );
}</pre>
</div>
""")

creer_lecon('tailwind-css', 'responsive-tailwind', 'Design responsive avec Tailwind', 3, 20, """
<h2>Mobile-first avec les breakpoints</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- Grille responsive --&gt;
&lt;div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"&gt;
    &lt;div&gt;Carte 1&lt;/div&gt;
    &lt;div&gt;Carte 2&lt;/div&gt;
    &lt;div&gt;Carte 3&lt;/div&gt;
&lt;/div&gt;

&lt;!-- Cacher/montrer selon taille --&gt;
&lt;div class="hidden md:block"&gt;Visible sur desktop uniquement&lt;/div&gt;
&lt;div class="md:hidden"&gt;Visible sur mobile uniquement&lt;/div&gt;

&lt;!-- Taille de texte responsive --&gt;
&lt;h1 class="text-2xl md:text-4xl lg:text-5xl font-bold"&gt;
    Titre responsive
&lt;/h1&gt;</pre>
</div>

<h3>Breakpoints Tailwind</h3>
<ul>
    <li><code>sm:</code> — 640px et plus</li>
    <li><code>md:</code> — 768px et plus</li>
    <li><code>lg:</code> — 1024px et plus</li>
    <li><code>xl:</code> — 1280px et plus</li>
    <li><code>2xl:</code> — 1536px et plus</li>
</ul>
""")

creer_lecon('tailwind-css', 'dark-mode-tailwind', 'Dark mode et personnalisation', 4, 20, """
<h2>Mode sombre et thème personnalisé</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;div class="bg-white dark:bg-gray-900
            text-gray-900 dark:text-white"&gt;
    &lt;h1 class="text-purple-600 dark:text-purple-400"&gt;
        Ce titre s'adapte au mode sombre
    &lt;/h1&gt;
&lt;/div&gt;</pre>
</div>

<h3>Personnaliser les couleurs</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// tailwind.config.js
module.exports = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primaire: {
                    DEFAULT: '#6C5CE7',
                    clair: '#A78BFA',
                    fonce: '#5A4BD1',
                },
            },
        },
    },
};</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous maîtrisez Tailwind CSS ! Vous pouvez maintenant styliser vos apps React à la vitesse de l'éclair.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 6: DJANGO BACKEND (6 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n🐍 Cours: Django — Backend Python')

creer_lecon('django-backend', 'introduction-django', 'Introduction à Django', 1, 20, """
<h2>Qu'est-ce que Django ?</h2>
<p><strong>Django</strong> est un framework web Python puissant qui suit le principe <em>"batteries incluses"</em>. Il fournit tout ce dont vous avez besoin pour construire des applications web : ORM, admin, authentification, formulaires, etc.</p>

<h3>Installer Django</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Créer un environnement virtuel
python -m venv env
source env/bin/activate  # Linux/Mac
env\\Scripts\\activate     # Windows

# Installer Django
pip install django

# Créer un projet
django-admin startproject mon_projet
cd mon_projet
python manage.py runserver</pre>
</div>

<h3>Architecture MTV</h3>
<p>Django utilise l'architecture <strong>MTV</strong> :</p>
<ul>
    <li><strong>Model</strong> — définit la structure des données (base de données)</li>
    <li><strong>Template</strong> — gère l'affichage HTML</li>
    <li><strong>View</strong> — contient la logique métier (ce qui se passe quand on visite une URL)</li>
</ul>

<h3>Structure d'un projet Django</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>mon_projet/
├── manage.py              # Commandes Django
├── mon_projet/
│   ├── settings.py        # Configuration
│   ├── urls.py            # Routes principales
│   └── wsgi.py            # Point d'entrée serveur
└── mon_app/
    ├── models.py           # Modèles de données
    ├── views.py            # Logique métier
    ├── urls.py             # Routes de l'app
    ├── templates/          # Fichiers HTML
    └── admin.py            # Interface admin</pre>
</div>

<div class="note-info">
    <strong>💡 Bon à savoir :</strong> Django est utilisé par Instagram, Mozilla, Pinterest et la NASA. C'est un choix solide pour vos projets.
</div>
""")

creer_lecon('django-backend', 'modeles-django', 'Modèles et base de données', 2, 30, """
<h2>Les modèles Django</h2>
<p>Un modèle Django est une <strong>classe Python</strong> qui représente une table dans la base de données. Django crée automatiquement les tables à partir de vos modèles.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>from django.db import models

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)
    est_publie = models.BooleanField(default=False)
    nb_vues = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_publication']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.titre</pre>
</div>

<h3>Types de champs courants</h3>
<ul>
    <li><code>CharField</code> — texte court (max_length obligatoire)</li>
    <li><code>TextField</code> — texte long</li>
    <li><code>IntegerField</code> — nombre entier</li>
    <li><code>BooleanField</code> — vrai/faux</li>
    <li><code>DateTimeField</code> — date et heure</li>
    <li><code>ForeignKey</code> — relation vers un autre modèle</li>
    <li><code>SlugField</code> — URL-friendly (ex: mon-article)</li>
    <li><code>ImageField</code> — upload d'image</li>
    <li><code>EmailField</code> — email validé</li>
</ul>

<h3>Migrations</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Créer les fichiers de migration
python manage.py makemigrations

# Appliquer les migrations (créer les tables)
python manage.py migrate

# Voir le SQL généré
python manage.py sqlmigrate mon_app 0001</pre>
</div>

<h3>Requêtes ORM</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Créer
article = Article.objects.create(titre="Mon article", contenu="...")

# Lire
tous = Article.objects.all()
publiés = Article.objects.filter(est_publie=True)
article = Article.objects.get(id=1)

# Mettre à jour
article.titre = "Nouveau titre"
article.save()

# Supprimer
article.delete()

# Requêtes avancées
recents = Article.objects.filter(
    est_publie=True
).order_by('-date_publication')[:5]</pre>
</div>

<blockquote>
    <strong>🎯 Exercice :</strong> Créez un modèle <code>Produit</code> avec nom, prix, description, catégorie et stock. Testez les requêtes dans le shell Django.
</blockquote>
""")

creer_lecon('django-backend', 'vues-urls-django', 'Vues et URLs', 3, 25, """
<h2>Les vues Django</h2>
<p>Une vue est une <strong>fonction Python</strong> qui reçoit une requête HTTP et retourne une réponse. C'est le cœur de la logique de votre application.</p>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Article

def liste_articles(request):
    articles = Article.objects.filter(est_publie=True)
    return render(request, 'blog/liste.html', {
        'articles': articles,
    })

def detail_article(request, slug):
    article = get_object_or_404(Article, slug=slug, est_publie=True)
    article.nb_vues += 1
    article.save()
    return render(request, 'blog/detail.html', {
        'article': article,
    })

# Vue API (retourne du JSON)
def api_articles(request):
    articles = Article.objects.filter(est_publie=True).values(
        'id', 'titre', 'date_publication'
    )
    return JsonResponse(list(articles), safe=False)</pre>
</div>

<h3>Configuration des URLs</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># urls.py de l'application
from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_articles, name='liste_articles'),
    path('article/&lt;slug:slug&gt;/', views.detail_article, name='detail_article'),
    path('api/articles/', views.api_articles, name='api_articles'),
]

# urls.py du projet (principal)
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]</pre>
</div>

<h3>Paramètres d'URL</h3>
<ul>
    <li><code>&lt;int:id&gt;</code> — nombre entier</li>
    <li><code>&lt;str:nom&gt;</code> — chaîne de caractères</li>
    <li><code>&lt;slug:slug&gt;</code> — slug (lettres, chiffres, tirets)</li>
    <li><code>&lt;uuid:id&gt;</code> — identifiant UUID</li>
</ul>
""")

creer_lecon('django-backend', 'templates-django', 'Templates Django', 4, 25, """
<h2>Le système de templates</h2>
<p>Les templates Django utilisent un langage de balisage simple pour <strong>afficher dynamiquement</strong> des données dans le HTML.</p>

<h3>Syntaxe de base</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- Afficher une variable --&gt;
&lt;h1&gt;{{ article.titre }}&lt;/h1&gt;
&lt;p&gt;Par {{ article.auteur }}&lt;/p&gt;

&lt;!-- Condition --&gt;
{% if article.est_publie %}
    &lt;span class="badge-vert"&gt;Publié&lt;/span&gt;
{% else %}
    &lt;span class="badge-rouge"&gt;Brouillon&lt;/span&gt;
{% endif %}

&lt;!-- Boucle --&gt;
{% for article in articles %}
    &lt;div class="carte"&gt;
        &lt;h3&gt;{{ article.titre }}&lt;/h3&gt;
        &lt;p&gt;{{ article.contenu|truncatewords:30 }}&lt;/p&gt;
        &lt;a href="{% url 'detail_article' slug=article.slug %}"&gt;
            Lire la suite
        &lt;/a&gt;
    &lt;/div&gt;
{% empty %}
    &lt;p&gt;Aucun article pour le moment.&lt;/p&gt;
{% endfor %}</pre>
</div>

<h3>Héritage de templates</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- base.html — template parent --&gt;
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;{% block titre %}Mon Site{% endblock %}&lt;/title&gt;
    {% block css_extra %}{% endblock %}
&lt;/head&gt;
&lt;body&gt;
    &lt;nav&gt;...&lt;/nav&gt;
    &lt;main&gt;
        {% block contenu %}{% endblock %}
    &lt;/main&gt;
    &lt;footer&gt;...&lt;/footer&gt;
&lt;/body&gt;
&lt;/html&gt;

&lt;!-- blog/liste.html — template enfant --&gt;
{% extends "base.html" %}
{% block titre %}Articles — Mon Site{% endblock %}
{% block contenu %}
    &lt;h1&gt;Nos articles&lt;/h1&gt;
    {% for article in articles %}
        ...
    {% endfor %}
{% endblock %}</pre>
</div>

<h3>Filtres utiles</h3>
<ul>
    <li><code>{{ texte|truncatewords:30 }}</code> — couper après 30 mots</li>
    <li><code>{{ date|date:"d/m/Y" }}</code> — formater une date</li>
    <li><code>{{ nombre|intcomma }}</code> — 1 000 000 au lieu de 1000000</li>
    <li><code>{{ texte|linebreaks }}</code> — convertir les retours à la ligne en &lt;p&gt;</li>
    <li><code>{{ texte|safe }}</code> — ne pas échapper le HTML</li>
</ul>
""")

creer_lecon('django-backend', 'auth-django', 'Authentification et permissions', 5, 25, """
<h2>Système d'authentification Django</h2>
<p>Django fournit un système d'authentification complet : inscription, connexion, déconnexion, réinitialisation de mot de passe.</p>

<h3>Vues d'authentification</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># views.py
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def vue_inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            return redirect('accueil')
    else:
        form = InscriptionForm()
    return render(request, 'auth/inscription.html', {'form': form})

def vue_connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request, 'Identifiants incorrects.')
    return render(request, 'auth/connexion.html')

@login_required
def vue_profil(request):
    return render(request, 'auth/profil.html')

def vue_deconnexion(request):
    logout(request)
    return redirect('accueil')</pre>
</div>

<h3>Protéger les vues</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Décorateur — seuls les connectés peuvent accéder
@login_required
def tableau_de_bord(request):
    return render(request, 'dashboard.html')

# Vérifier les permissions dans le template
{% if user.is_authenticated %}
    &lt;p&gt;Bonjour, {{ user.username }} !&lt;/p&gt;
    &lt;a href="{% url 'deconnexion' %}"&gt;Déconnexion&lt;/a&gt;
{% else %}
    &lt;a href="{% url 'connexion' %}"&gt;Connexion&lt;/a&gt;
{% endif %}</pre>
</div>

<div class="note-info">
    <strong>🔒 Sécurité :</strong> Django protège automatiquement contre les attaques CSRF, XSS et injection SQL. Utilisez toujours les outils intégrés plutôt que de réinventer la roue.
</div>
""")

creer_lecon('django-backend', 'projet-final-django', 'Projet final : Blog complet', 6, 30, """
<h2>Projet : Blog avec Django</h2>
<p>Construisez un blog complet avec CRUD, authentification, commentaires et déploiement.</p>

<h3>Modèles du blog</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>class Article(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenu = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True)
    est_publie = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)</pre>
</div>

<h3>Vue de création d'article</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>@login_required
def creer_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.slug = slugify(article.titre)
            article.save()
            form.save_m2m()  # Sauvegarder les tags
            messages.success(request, 'Article créé !')
            return redirect('detail_article', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'blog/creer.html', {'form': form})</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous maîtrisez Django ! Vous savez créer un backend complet avec modèles, vues, templates et authentification.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 7: FLASK BACKEND (4 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n🧪 Cours: Flask — Backend Léger')

creer_lecon('flask-backend', 'introduction-flask', 'Introduction à Flask', 1, 20, """
<h2>Qu'est-ce que Flask ?</h2>
<p><strong>Flask</strong> est un micro-framework Python pour le web. Contrairement à Django, il est <strong>minimaliste</strong> : vous choisissez vous-même les outils (ORM, authentification, etc.).</p>

<h3>Installation et premier serveur</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>pip install flask</pre>
</div>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/api/bonjour/&lt;nom&gt;')
def api_bonjour(nom):
    return jsonify({
        'message': f'Bonjour, {nom} !',
        'statut': 'succès'
    })

if __name__ == '__main__':
    app.run(debug=True)</pre>
</div>

<h3>Flask vs Django</h3>
<ul>
    <li><strong>Flask</strong> — léger, flexible, parfait pour les API et petits projets</li>
    <li><strong>Django</strong> — complet, structuré, parfait pour les gros projets</li>
    <li>Flask vous donne la <strong>liberté</strong>, Django vous donne la <strong>structure</strong></li>
</ul>

<div class="note-info">
    <strong>💡 Quand utiliser Flask ?</strong> Pour les API REST, les microservices, les prototypes rapides, ou quand vous voulez un contrôle total sur votre stack.
</div>
""")

creer_lecon('flask-backend', 'routes-templates-flask', 'Routes et Templates Flask', 2, 25, """
<h2>Gérer les routes</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route simple
@app.route('/')
def accueil():
    return render_template('accueil.html', titre='Accueil')

# Route avec paramètre
@app.route('/utilisateur/&lt;username&gt;')
def profil(username):
    return render_template('profil.html', nom=username)

# Route avec méthodes HTTP
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        message = request.form['message']
        # Traiter le formulaire...
        return redirect(url_for('accueil'))
    return render_template('contact.html')</pre>
</div>

<h3>Templates Jinja2</h3>
<p>Flask utilise <strong>Jinja2</strong>, un moteur de templates très similaire à celui de Django.</p>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">HTML</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>&lt;!-- templates/base.html --&gt;
&lt;html&gt;
&lt;body&gt;
    &lt;nav&gt;
        &lt;a href="{{ url_for('accueil') }}"&gt;Accueil&lt;/a&gt;
        &lt;a href="{{ url_for('contact') }}"&gt;Contact&lt;/a&gt;
    &lt;/nav&gt;
    {% block contenu %}{% endblock %}
&lt;/body&gt;
&lt;/html&gt;

&lt;!-- templates/accueil.html --&gt;
{% extends "base.html" %}
{% block contenu %}
    &lt;h1&gt;{{ titre }}&lt;/h1&gt;
    {% for item in items %}
        &lt;p&gt;{{ item.nom }} — {{ item.prix }} FCFA&lt;/p&gt;
    {% endfor %}
{% endblock %}</pre>
</div>
""")

creer_lecon('flask-backend', 'api-rest-flask', 'Créer une API REST avec Flask', 3, 25, """
<h2>API REST avec Flask</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de données simulée
produits = [
    {'id': 1, 'nom': 'Laptop', 'prix': 450000},
    {'id': 2, 'nom': 'Smartphone', 'prix': 150000},
]

# GET — Liste des produits
@app.route('/api/produits', methods=['GET'])
def get_produits():
    return jsonify(produits)

# GET — Un produit par ID
@app.route('/api/produits/&lt;int:id&gt;', methods=['GET'])
def get_produit(id):
    produit = next((p for p in produits if p['id'] == id), None)
    if produit is None:
        return jsonify({'erreur': 'Produit non trouvé'}), 404
    return jsonify(produit)

# POST — Créer un produit
@app.route('/api/produits', methods=['POST'])
def creer_produit():
    data = request.get_json()
    nouveau = {
        'id': len(produits) + 1,
        'nom': data['nom'],
        'prix': data['prix'],
    }
    produits.append(nouveau)
    return jsonify(nouveau), 201

# PUT — Modifier un produit
@app.route('/api/produits/&lt;int:id&gt;', methods=['PUT'])
def modifier_produit(id):
    produit = next((p for p in produits if p['id'] == id), None)
    if produit is None:
        return jsonify({'erreur': 'Produit non trouvé'}), 404
    data = request.get_json()
    produit.update(data)
    return jsonify(produit)

# DELETE — Supprimer un produit
@app.route('/api/produits/&lt;int:id&gt;', methods=['DELETE'])
def supprimer_produit(id):
    global produits
    produits = [p for p in produits if p['id'] != id]
    return jsonify({'message': 'Produit supprimé'}), 200</pre>
</div>

<div class="note-info">
    <strong>💡 Test rapide :</strong> Utilisez <code>curl</code> ou un outil comme Postman pour tester vos routes API.
</div>
""")

creer_lecon('flask-backend', 'projet-final-flask', 'Projet final : API de gestion', 4, 30, """
<h2>Projet : API complète avec Flask + SQLAlchemy</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    terminee = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'terminee': self.terminee,
        }

@app.route('/api/taches', methods=['GET'])
def liste_taches():
    taches = Tache.query.all()
    return jsonify([t.to_dict() for t in taches])

@app.route('/api/taches', methods=['POST'])
def creer_tache():
    data = request.get_json()
    tache = Tache(titre=data['titre'], description=data.get('description', ''))
    db.session.add(tache)
    db.session.commit()
    return jsonify(tache.to_dict()), 201

@app.route('/api/taches/&lt;int:id&gt;/terminer', methods=['PATCH'])
def terminer_tache(id):
    tache = Tache.query.get_or_404(id)
    tache.terminee = not tache.terminee
    db.session.commit()
    return jsonify(tache.to_dict())

@app.route('/api/taches/&lt;int:id&gt;', methods=['DELETE'])
def supprimer_tache(id):
    tache = Tache.query.get_or_404(id)
    db.session.delete(tache)
    db.session.commit()
    return jsonify({'message': 'Tâche supprimée'})

with app.app_context():
    db.create_all()</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous savez créer des API REST avec Flask ! Prochaine étape : <strong>FastAPI</strong> pour des performances encore meilleures.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 8: FASTAPI (3 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n🚀 Cours: FastAPI — API Modernes')

creer_lecon('fastapi-backend', 'introduction-fastapi', 'Introduction à FastAPI', 1, 20, """
<h2>Qu'est-ce que FastAPI ?</h2>
<p><strong>FastAPI</strong> est le framework Python le plus rapide pour créer des API. Il utilise le <strong>typage Python</strong> pour valider automatiquement les données et générer une documentation interactive.</p>

<h3>Installation</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>pip install fastapi uvicorn</pre>
</div>

<h3>Première API</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mon API DevAfrique")

class Utilisateur(BaseModel):
    nom: str
    email: str
    age: int | None = None

@app.get("/")
async def accueil():
    return {"message": "Bienvenue sur l'API DevAfrique !"}

@app.get("/utilisateurs/{user_id}")
async def get_utilisateur(user_id: int):
    return {"id": user_id, "nom": "Aminata"}

@app.post("/utilisateurs")
async def creer_utilisateur(user: Utilisateur):
    return {"message": f"Utilisateur {user.nom} créé !", "data": user}</pre>
</div>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Lancer le serveur
uvicorn main:app --reload

# Documentation auto: http://127.0.0.1:8000/docs</pre>
</div>

<div class="note-info">
    <strong>💡 Avantage clé :</strong> FastAPI génère automatiquement une documentation Swagger à <code>/docs</code>. C'est idéal pour tester et partager votre API.
</div>
""")

creer_lecon('fastapi-backend', 'crud-fastapi', 'CRUD complet avec FastAPI', 2, 25, """
<h2>API CRUD avec FastAPI</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Schéma de validation
class ProduitBase(BaseModel):
    nom: str
    prix: float
    description: Optional[str] = None
    en_stock: bool = True

class ProduitCreate(ProduitBase):
    pass

class Produit(ProduitBase):
    id: int

# Base de données simulée
db_produits: dict[int, Produit] = {}
compteur_id = 0

@app.get("/produits", response_model=list[Produit])
async def liste_produits():
    return list(db_produits.values())

@app.get("/produits/{produit_id}", response_model=Produit)
async def get_produit(produit_id: int):
    if produit_id not in db_produits:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return db_produits[produit_id]

@app.post("/produits", response_model=Produit, status_code=201)
async def creer_produit(produit: ProduitCreate):
    global compteur_id
    compteur_id += 1
    nouveau = Produit(id=compteur_id, **produit.dict())
    db_produits[compteur_id] = nouveau
    return nouveau

@app.put("/produits/{produit_id}", response_model=Produit)
async def modifier_produit(produit_id: int, produit: ProduitCreate):
    if produit_id not in db_produits:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    modifie = Produit(id=produit_id, **produit.dict())
    db_produits[produit_id] = modifie
    return modifie

@app.delete("/produits/{produit_id}")
async def supprimer_produit(produit_id: int):
    if produit_id not in db_produits:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    del db_produits[produit_id]
    return {"message": "Produit supprimé"}</pre>
</div>

<h3>Paramètres de requête (filtres)</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>@app.get("/produits/recherche/")
async def rechercher(
    q: str = "",
    prix_min: float = 0,
    prix_max: float = 1_000_000,
    en_stock: bool = True,
):
    resultats = [
        p for p in db_produits.values()
        if q.lower() in p.nom.lower()
        and prix_min <= p.prix <= prix_max
        and p.en_stock == en_stock
    ]
    return resultats</pre>
</div>
""")

creer_lecon('fastapi-backend', 'projet-final-fastapi', 'Projet final : API de tâches', 3, 30, """
<h2>Projet : API de gestion de tâches avec base de données</h2>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./taches.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TacheDB(Base):
    __tablename__ = "taches"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    description = Column(String, default="")
    terminee = Column(Boolean, default=False)

Base.metadata.create_all(engine)
app = FastAPI(title="API Tâches DevAfrique")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/taches")
def liste_taches(terminee: bool = None, db: Session = Depends(get_db)):
    query = db.query(TacheDB)
    if terminee is not None:
        query = query.filter(TacheDB.terminee == terminee)
    return query.all()

@app.post("/taches", status_code=201)
def creer_tache(titre: str, description: str = "", db: Session = Depends(get_db)):
    tache = TacheDB(titre=titre, description=description)
    db.add(tache)
    db.commit()
    db.refresh(tache)
    return tache

@app.patch("/taches/{id}/toggle")
def toggle_tache(id: int, db: Session = Depends(get_db)):
    tache = db.query(TacheDB).get(id)
    if not tache:
        raise HTTPException(404, "Tâche non trouvée")
    tache.terminee = not tache.terminee
    db.commit()
    return tache</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous maîtrisez FastAPI ! Vous savez créer des API modernes, typées et documentées automatiquement.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 9: DEPLOIEMENT (2 leçons)
# ═══════════════════════════════════════════════════════════════
print('\\n☁️ Cours: Déploiement (Render & Neon)')

creer_lecon('deploiement', 'deployer-render', 'Déployer sur Render', 1, 25, """
<h2>Mettre votre projet en ligne avec Render</h2>
<p><strong>Render</strong> est une plateforme cloud qui simplifie le déploiement. C'est l'alternative moderne à Heroku — et il propose un plan <strong>gratuit</strong>.</p>

<h3>Préparer votre projet Django</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Installer les dépendances de production
pip install gunicorn whitenoise dj-database-url psycopg2-binary

# Créer le fichier requirements.txt
pip freeze > requirements.txt</pre>
</div>

<h3>Fichier build.sh</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Bash</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate</pre>
</div>

<h3>Configuration settings.py pour la production</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>import dj_database_url

# Base de données — utilise DATABASE_URL en production
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

# WhiteNoise pour les fichiers statiques
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}</pre>
</div>

<h3>Étapes sur Render</h3>
<ol>
    <li>Créer un compte sur <a href="https://render.com">render.com</a></li>
    <li>Connecter votre dépôt GitHub</li>
    <li>Créer un "Web Service"</li>
    <li>Build Command : <code>./build.sh</code></li>
    <li>Start Command : <code>gunicorn siteweb.wsgi:application</code></li>
    <li>Ajouter les variables d'environnement</li>
</ol>

<div class="note-info">
    <strong>💡 Variables d'environnement :</strong> Ne mettez jamais vos mots de passe ou clés secrètes dans le code. Utilisez les variables d'environnement.
</div>
""")

creer_lecon('deploiement', 'base-de-donnees-neon', 'Base de données PostgreSQL avec Neon', 2, 20, """
<h2>PostgreSQL en production avec Neon</h2>
<p><strong>Neon</strong> est un service PostgreSQL serverless — parfait pour les projets Django. Il offre un plan gratuit généreux.</p>

<h3>Configurer Neon</h3>
<ol>
    <li>Créer un compte sur <a href="https://neon.tech">neon.tech</a></li>
    <li>Créer un nouveau projet</li>
    <li>Copier la chaîne de connexion (Connection String)</li>
</ol>

<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Format de la chaîne de connexion Neon
postgresql://user:password@host/database?sslmode=require</pre>
</div>

<h3>Configurer Django</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># settings.py
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
    )
}

# En production, la variable DATABASE_URL
# est automatiquement utilisée par dj-database-url</pre>
</div>

<h3>Tester la connexion</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Terminal</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># Définir la variable d'environnement
export DATABASE_URL="postgresql://user:pass@host/db?sslmode=require"

# Appliquer les migrations
python manage.py migrate

# Vérifier la connexion
python manage.py dbshell</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Votre application est maintenant déployée avec une base de données PostgreSQL en production ! Vous êtes un développeur full-stack.
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  COURS 10: INTEGRATION IA (2 leçons)
# ═══════════════════════════════════════════════════════════════
print("\n🤖 Cours: Intégration de l'IA")

creer_lecon('integration-ia', 'introduction-ia-web', "L'IA dans le développement web", 1, 20, """
<h2>Intégrer l'IA dans vos projets</h2>
<p>L'intelligence artificielle transforme le développement web. Vous pouvez ajouter des fonctionnalités <strong>IA</strong> à vos applications grâce aux API disponibles.</p>

<h3>Cas d'utilisation courants</h3>
<ul>
    <li><strong>Chatbots</strong> — assistant virtuel pour votre site</li>
    <li><strong>Génération de contenu</strong> — articles, descriptions de produits</li>
    <li><strong>Traduction automatique</strong> — rendre votre site multilingue</li>
    <li><strong>Analyse de sentiments</strong> — comprendre les avis clients</li>
    <li><strong>Recommandations</strong> — suggérer du contenu personnalisé</li>
    <li><strong>Recherche intelligente</strong> — comprendre les questions en langage naturel</li>
</ul>

<h3>Utiliser l'API OpenAI</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>import openai

client = openai.OpenAI(api_key="votre-clé-api")

reponse = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Tu es un assistant pédagogique pour développeurs africains."},
        {"role": "user", "content": "Explique-moi les hooks React simplement."},
    ],
    temperature=0.7,
    max_tokens=500,
)

print(reponse.choices[0].message.content)</pre>
</div>

<h3>Intégrer dans Django</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># views.py
from django.http import JsonResponse
import openai

def vue_chatbot(request):
    question = request.GET.get('q', '')
    if not question:
        return JsonResponse({'erreur': 'Posez une question'}, status=400)

    client = openai.OpenAI()
    reponse = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Assistant DevAfrique."},
            {"role": "user", "content": question},
        ],
    )
    return JsonResponse({
        'reponse': reponse.choices[0].message.content
    })</pre>
</div>

<div class="note-info">
    <strong>⚠️ Important :</strong> Ne mettez jamais votre clé API dans le code. Utilisez une variable d'environnement : <code>OPENAI_API_KEY</code>.
</div>
""")

creer_lecon('integration-ia', 'projet-chatbot-ia', 'Projet : Chatbot IA pour votre site', 2, 30, """
<h2>Projet : Créer un chatbot IA</h2>
<p>Ajoutez un assistant IA à votre site web qui répond aux questions des utilisateurs.</p>

<h3>Backend Django</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">Python</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre># views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_chat(request):
    if request.method != 'POST':
        return JsonResponse({'erreur': 'POST uniquement'}, status=405)

    data = json.loads(request.body)
    message = data.get('message', '')

    # Simulation de réponse IA (remplacer par OpenAI en production)
    reponses = {
        'html': 'HTML est le langage de base du web. Commencez par le cours "Les bases du HTML" !',
        'css': 'CSS permet de styliser vos pages. Flexbox et Grid sont essentiels à maîtriser.',
        'javascript': 'JavaScript rend vos pages interactives. Apprenez d\\'abord les bases puis passez à React.',
        'django': 'Django est un framework Python puissant. Il suit le principe batteries incluses.',
        'react': 'React est une bibliothèque pour créer des interfaces modernes avec des composants.',
    }

    # Recherche simple par mots-clés
    reponse = "Je suis l'assistant DevAfrique ! Posez-moi une question sur HTML, CSS, JavaScript, React ou Django."
    for mot, rep in reponses.items():
        if mot in message.lower():
            reponse = rep
            break

    return JsonResponse({'reponse': reponse})</pre>
</div>

<h3>Frontend JavaScript</h3>
<div class="bloc-code">
    <div class="bloc-code-header">
        <span class="bloc-code-langage">JavaScript</span>
        <button class="btn-copier">Copier</button>
    </div>
    <pre>// Chat widget
const chatForm = document.querySelector('#chat-form');
const chatMessages = document.querySelector('#chat-messages');
const chatInput = document.querySelector('#chat-input');

const ajouterMessage = (texte, type) => {
    const div = document.createElement('div');
    div.className = `message message-${type}`;
    div.textContent = texte;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    ajouterMessage(message, 'utilisateur');
    chatInput.value = '';

    try {
        const rep = await fetch('/api/chat/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });
        const data = await rep.json();
        ajouterMessage(data.reponse, 'assistant');
    } catch (err) {
        ajouterMessage('Erreur de connexion.', 'erreur');
    }
});</pre>
</div>

<div class="note-succes">
    <strong>🎉 Félicitations !</strong> Vous avez terminé tous les cours ! Vous êtes maintenant un développeur web complet. Continuez à pratiquer et à construire des projets.
    <br><br>
    <strong>🌍 L'Afrique a besoin de développeurs comme vous. Allez créer l'avenir !</strong>
</div>
""")


# ═══════════════════════════════════════════════════════════════
#  RÉSUMÉ
# ═══════════════════════════════════════════════════════════════
print('\\n' + '═' * 60)
print(f'📊 Total leçons créées/mises à jour: {Lecon.objects.count()}')
print('═' * 60)
print('\\n🎉 Toutes les 50 leçons ont été chargées avec succès !')
print("🌍 DevAfrique — La meilleure formation tech pour l'Afrique !")