#  Plan de Transformation — « DevAfrique » (ex Développement Sans Tabou)

## Vision
Transformer la plateforme existante en **LA référence éducative africaine** pour le développement web et mobile — plus accessible qu'OpenClassrooms, plus concrète que W3Schools, pensée pour l'Afrique.

**Objectif** : Qu'un élève de 3ème puisse comprendre le développement et créer des projets concrets.

---

## 1. Acteurs du Système

| Acteur | Rôle | Actions principales |
|--------|------|---------------------|
| **Visiteur** | Non inscrit | Consulter cours, glossaire, projets publics, s'inscrire |
| **Apprenant** | Inscrit, suit les formations | Suivre cours, marquer progression, soumettre projets, commenter, liker, obtenir certificats, signaler contenu |
| **Formateur** | Crée du contenu pédagogique | Proposer cours/leçons, répondre aux questions forum, valider exercices |
| **Modérateur** | Régule la communauté | Approuver/refuser contenus, gérer signalements, modérer forum |
| **Administrateur** | Gère toute la plateforme | CRUD complet, gestion utilisateurs/rôles, statistiques, configuration |

---

## 2. Diagramme de Cas d'Utilisation (UML)

```
┌─────────────────────────────────────────────────────────────────┐
│                     PLATEFORME DevAfrique                       │
│                                                                 │
│  ┌──────────────────────┐   ┌───────────────────────────┐       │
│  │  Gestion Formations  │   │   Communauté & Projets    │       │
│  │                      │   │                           │       │
│  │ • Parcourir parcours │   │ • Soumettre un projet     │       │
│  │ • Suivre un cours    │   │ • Voir les projets        │       │
│  │ • Lire une leçon     │   │ • Liker / Commenter       │       │
│  │ • Marquer progression│   │ • Signaler un contenu     │       │
│  │ • Obtenir certificat │   │ • Discuter sur le forum   │       │
│  │ • Consulter glossaire│   │ • Partager connaissances  │       │
│  └──────────────────────┘   └───────────────────────────┘       │
│                                                                 │
│  ┌──────────────────────┐   ┌───────────────────────────┐       │
│  │  Gestion Contenu     │   │   Administration          │       │
│  │  (Formateur)         │   │                           │       │
│  │                      │   │ • Dashboard statistiques  │       │
│  │ • Proposer un cours  │   │ • Gérer utilisateurs      │       │
│  │ • Créer des leçons   │   │ • Modérer projets/cours   │       │
│  │ • Répondre au forum  │   │ • Traiter signalements    │       │
│  └──────────────────────┘   │ • Configurer plateforme   │       │
│                             └───────────────────────────┘       │
│  ┌──────────────────────┐                                       │
│  │  Authentification    │                                       │
│  │                      │                                       │
│  │ • S'inscrire         │                                       │
│  │ • Se connecter       │                                       │
│  │ • Gérer son profil   │                                       │
│  │ • Réinitialiser MDP  │                                       │
│  └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
```

### Acteurs ↔ Cas d'utilisation

```
  Visiteur ──────► Parcourir cours (lecture seule)
       │──────────► Consulter glossaire
       │──────────► Voir projets publics
       │──────────► S'inscrire / Se connecter

  Apprenant ─────► Suivre cours + marquer progression
       │──────────► Soumettre un projet
       │──────────► Liker / Commenter projets & leçons
       │──────────► Participer au forum (poser questions)
       │──────────► Signaler fausses informations
       │──────────► Obtenir certificats de complétion
       │──────────► Gérer son profil + avatar

  Formateur ─────► Proposer cours / leçons (soumis à validation)
       │──────────► Répondre aux questions du forum
       │──────────► Voir ses statistiques (vues, apprenants)

  Modérateur ────► Approuver / refuser cours proposés
       │──────────► Traiter les signalements
       │──────────► Modérer le forum (supprimer, éditer)

  Admin ─────────► Tout CRUD (parcours, cours, leçons, utilisateurs)
       │──────────► Promouvoir/Rétrograder rôles
       │──────────► Dashboard avec statistiques complètes
       │──────────► Gérer les catégories et tags
```

---

## 3. Diagramme de Classes (Modèles Django)

```
┌─────────────────────┐       ┌──────────────────────┐
│    Utilisateur       │       │      Parcours         │
├─────────────────────┤       ├──────────────────────┤
│ username             │       │ titre                 │
│ email                │       │ slug                  │
│ role (choix)         │       │ description           │
│ biographie           │       │ type_parcours         │
│ avatar_url           │       │ icone                 │
│ pays                 │       │ image_url             │
│ niveau               │       │ ordre                 │
│ points_xp            │       │ est_publie            │
│ site_web             │       └──────────┬───────────┘
└─────────┬───────────┘                   │ 1
          │                               │
          │ N                             │ N
          ▼                               ▼
┌─────────────────────┐       ┌──────────────────────┐
│    Progression       │       │       Cours           │
├─────────────────────┤       ├──────────────────────┤
│ utilisateur (FK)     │       │ parcours (FK)         │
│ lecon (FK)           │       │ titre                 │
│ terminee             │       │ slug                  │
│ date_completion      │       │ description           │
└─────────────────────┘       │ icone                 │
                              │ image_url             │
┌─────────────────────┐       │ auteur (FK)           │
│    Certificat        │       │ statut                │
├─────────────────────┤       │ ordre                 │
│ utilisateur (FK)     │       │ est_publie            │
│ parcours (FK)        │       │ niveau_difficulte     │
│ date_obtention       │       └──────────┬───────────┘
│ code_unique          │                   │ 1
└─────────────────────┘                   │
                                          │ N
                              ┌──────────────────────┐
                              │       Leçon           │
                              ├──────────────────────┤
                              │ cours (FK)            │
                              │ titre                 │
                              │ slug                  │
                              │ contenu (HTML)        │
                              │ ordre                 │
                              │ duree_minutes         │
                              │ est_publie            │
                              └──────────┬───────────┘
                                          │
                              ┌───────────┴──────────┐
                              ▼                      ▼
                   ┌──────────────────┐  ┌────────────────────┐
                   │   Commentaire     │  │  TermeGlossaire    │
                   ├──────────────────┤  ├────────────────────┤
                   │ auteur (FK)       │  │ terme              │
                   │ contenu           │  │ slug               │
                   │ lecon (FK, null)  │  │ definition         │
                   │ projet (FK, null) │  │ exemple_code       │
                   │ parent (FK, null) │  │ categorie          │
                   │ date_creation     │  │ lettre             │
                   └──────────────────┘  └────────────────────┘

┌─────────────────────┐       ┌──────────────────────┐
│ ProjetCommunautaire  │       │    Signalement        │
├─────────────────────┤       ├──────────────────────┤
│ auteur (FK)          │       │ signaleur (FK)        │
│ titre                │       │ type_contenu          │
│ description          │       │ id_contenu            │
│ technologies         │       │ raison                │
│ lien_projet          │       │ description           │
│ lien_github          │       │ statut                │
│ capture_url          │       │ traite_par (FK)       │
│ statut               │       │ date_creation         │
│ nb_likes             │       └──────────────────────┘
│ date_soumission      │
└─────────────────────┘       ┌──────────────────────┐
                              │   SujetForum          │
┌─────────────────────┐       ├──────────────────────┤
│       Like           │       │ auteur (FK)           │
├─────────────────────┤       │ titre                 │
│ utilisateur (FK)     │       │ contenu               │
│ projet (FK)          │       │ categorie             │
│ date_creation        │       │ est_resolu            │
└─────────────────────┘       │ est_epingle           │
                              │ nb_vues               │
                              │ date_creation         │
                              └──────────┬───────────┘
                                          │ 1..N
                              ┌──────────────────────┐
                              │   ReponseForum        │
                              ├──────────────────────┤
                              │ sujet (FK)            │
                              │ auteur (FK)           │
                              │ contenu               │
                              │ est_solution          │
                              │ nb_votes              │
                              │ date_creation         │
                              └──────────────────────┘
```

---

## 4. Diagramme de Séquence — Flux principal « Suivre un cours »

```
Apprenant        Navigateur         Django            Base de données
    │                │                  │                    │
    │─── Ouvre cours ─►                 │                    │
    │                │── GET /cours/x/ ─►                    │
    │                │                  │── Query cours ────►│
    │                │                  │◄── Cours + leçons ─│
    │                │◄── Page HTML ────│                    │
    │◄── Affichage ──│                  │                    │
    │                │                  │                    │
    │─── Lit leçon ──►                  │                    │
    │                │── GET leçon ─────►                    │
    │                │                  │── Query + progression ►│
    │                │◄── Leçon HTML ───│                    │
    │◄── Affichage ──│                  │                    │
    │                │                  │                    │
    │─── Marquer ────►                  │                    │
    │    terminée    │── POST terminer ─►                    │
    │                │                  │── UPDATE progression ─►│
    │                │                  │── CHECK toutes     │
    │                │                  │   leçons terminées?─►│
    │                │                  │◄── OUI/NON ────────│
    │                │                  │── Si OUI: créer    │
    │                │                  │   certificat ──────►│
    │                │◄── Redirect ─────│                    │
    │◄── Leçon suivante ─│              │                    │
```

---

## 5. Diagramme d'Activité — Soumission et Modération de Contenu

```
┌─────────┐
│  Début  │
└────┬────┘
     ▼
┌────────────────────┐
│ Utilisateur soumet │
│ cours/projet/sujet │
└────────┬───────────┘
         ▼
    ┌──────────┐
    │ Statut = │
    │en_attente│
    └────┬─────┘
         ▼
┌─────────────────────┐     ┌──────────────────────┐
│ Modérateur examine  │────►│ Contenu conforme ?    │
└─────────────────────┘     └───────┬──────┬───────┘
                                OUI │      │ NON
                                    ▼      ▼
                          ┌──────────┐ ┌──────────┐
                          │ Approuvé │ │ Refusé   │
                          │ + publié │ │ + notif  │
                          └──────────┘ └──────────┘

Signalement :
┌──────────────────┐     ┌───────────────────┐
│ Communauté       │────►│ Signalement créé  │
│ signale contenu  │     │ (type + raison)   │
└──────────────────┘     └────────┬──────────┘
                                  ▼
                         ┌─────────────────┐
                         │ Modérateur/Admin │
                         │ traite           │
                         └───────┬─────────┘
                           ┌─────┴─────┐
                           ▼           ▼
                      ┌────────┐ ┌──────────┐
                      │Ignoré  │ │Contenu   │
                      │        │ │supprimé  │
                      └────────┘ └──────────┘
```

---

## 6. Liste Exhaustive des Écrans

### 6.1 Pages Publiques
| # | Écran | Route | Description |
|---|-------|-------|-------------|
| 1 | **Accueil** | `/` | Hero animé, stats, parcours, cours récents, témoignages, CTA |
| 2 | **À propos** | `/a-propos/` | Mission, équipe, vision Afrique |
| 3 | **Glossaire A-Z** | `/glossaire/` | Termes du développement, triés par lettre, recherche |
| 4 | **Détail terme** | `/glossaire/<slug>/` | Définition, exemple de code, termes liés |

### 6.2 Formations
| # | Écran | Route | Description |
|---|-------|-------|-------------|
| 5 | **Liste parcours** | `/cours/parcours/` | Tous les parcours avec filtre par type |
| 6 | **Détail parcours** | `/cours/parcours/<slug>/` | Roadmap du parcours, cours listés |
| 7 | **Liste cours** | `/cours/` | Catalogue filtrable (parcours, niveau, recherche) |
| 8 | **Détail cours** | `/cours/<slug>/` | Description, leçons, progression utilisateur |
| 9 | **Leçon** | `/cours/<slug>/lecon/<slug>/` | Contenu, sidebar, navigation, code copiable |
| 10 | **Certificat** | `/certificat/<code>/` | Certificat de complétion, partageable |

### 6.3 Communauté & Projets
| # | Écran | Route | Description |
|---|-------|-------|-------------|
| 11 | **Liste projets** | `/projets/` | Galerie de projets, filtres, likes |
| 12 | **Détail projet** | `/projets/<slug>/` | Description, techs, liens, commentaires, likes |
| 13 | **Soumettre projet** | `/projets/soumettre/` | Formulaire de soumission |

### 6.4 Forum
| # | Écran | Route | Description |
|---|-------|-------|-------------|
| 14 | **Forum** | `/forum/` | Liste sujets, catégories, recherche, sujets épinglés |
| 15 | **Détail sujet** | `/forum/<slug>/` | Question + réponses, votes, marquer résolu |
| 16 | **Nouveau sujet** | `/forum/nouveau/` | Formulaire création sujet |

### 6.5 Utilisateurs
| # | Écran | Route | Description |
|---|-------|-------|-------------|
| 17 | **Inscription** | `/utilisateurs/inscription/` | Formulaire amélioré |
| 18 | **Connexion** | `/utilisateurs/connexion/` | Formulaire amélioré |
| 19 | **Profil** | `/utilisateurs/profil/` | Stats, progression, projets, certificats, badges |
| 20 | **Profil public** | `/utilisateurs/<username>/` | Profil visible par tous |

### 6.6 Administration
| # | Écran | Route | Description |
|---|-------|-------|-------------|
| 21 | **Dashboard** | `/administration/` | Stats complètes, graphiques, alertes |
| 22 | **Gestion parcours** | `/administration/parcours/` | CRUD parcours |
| 23 | **Gestion cours** | `/administration/cours/` | CRUD cours |
| 24 | **Gestion leçons** | `/administration/lecons/` | CRUD leçons |
| 25 | **Gestion projets** | `/administration/projets/` | Modération projets |
| 26 | **Gestion utilisateurs** | `/administration/utilisateurs/` | Liste, rôles, ban |
| 27 | **Gestion signalements** | `/administration/signalements/` | Traiter signalements |
| 28 | **Gestion forum** | `/administration/forum/` | Modérer sujets/réponses |
| 29 | **Gestion glossaire** | `/administration/glossaire/` | CRUD termes |

---

## 7. Modèle Économique

```
┌─────────────────────────────────────────────────────────┐
│              MODÈLE FREEMIUM + COMMUNAUTÉ               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  GRATUIT (100% des formations de base)                  │
│  ├── Tous les cours et leçons                           │
│  ├── Forum communautaire                                │
│  ├── Glossaire complet                                  │
│  ├── Soumettre 2 projets / mois                         │
│  └── Certificats de base                                │
│                                                         │
│  PREMIUM (futur - 2 000 FCFA/mois)                      │
│  ├── Projets illimités                                  │
│  ├── Certificats vérifiés (QR code)                     │
│  ├── Mentorat formateur                                 │
│  ├── Accès aux formations avancées                      │
│  └── Badge "Premium" sur profil                         │
│                                                         │
│  ENTREPRISES / UNIVERSITÉS (futur)                       │
│  ├── Dashboard classe / promotion                       │
│  ├── Suivi progression étudiants                        │
│  ├── Contenu personnalisé                               │
│  └── Licence annuelle                                   │
│                                                         │
│  FORMATEURS (commission sur contenu premium)             │
│  ├── 70% des revenus de leurs cours premium             │
│  └── Visibilité plateforme                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Améliorations Techniques Apportées

### 8.1 Nouveaux Modèles Django
- `TermeGlossaire` — Dictionnaire des termes du développement
- `Commentaire` — Commentaires sur leçons et projets (avec réponses imbriquées)
- `Like` — Likes sur projets
- `SujetForum` + `ReponseForum` — Forum Q&A
- `Signalement` — Signalement de contenus (fausses infos, spam, etc.)
- `Certificat` — Certificats de complétion de parcours
- Enrichissement `Utilisateur` : pays, niveau, points XP
- Enrichissement `Cours` : auteur, statut de validation, niveau de difficulté, image

### 8.2 Refonte UI/UX
- Design professionnel avec animations CSS
- Hero animé avec particules/formes géométriques
- Barre de recherche globale
- Dark mode automatique
- Micro-interactions (hover, transitions fluides)
- Responsive mobile-first optimisé Afrique
- Notifications toast améliorées

### 8.3 Fonctionnalités Communautaires
- Système de likes + compteur
- Commentaires imbriqués (réponses)
- Forum Q&A avec résolution
- Signalement par la communauté
- Profils publics avec badges
- Système de points XP (gamification légère)

---

## 9. Plan d'Implémentation

| Phase | Fichiers | Fonctionnalités |
|-------|----------|-----------------|
| **Phase 1** | `utilisateurs/models.py`, `cours/models.py`, `projets/models.py`, `forum/models.py`, `glossaire/models.py` | Nouveaux modèles + migrations |
| **Phase 2** | `forum/views.py`, `forum/urls.py`, `glossaire/views.py`, `glossaire/urls.py` | Nouvelles apps (forum + glossaire) |
| **Phase 3** | `static/css/styles.css` | Refonte CSS complète : animations, dark mode, micro-interactions |
| **Phase 4** | `templates/base.html` + tous les templates | Refonte templates : nouveau header, footer, toutes les pages |
| **Phase 5** | `administration/`, signalements, modération | Admin enrichi + modération communautaire |
| **Phase 6** | `donnees_initiales.py` | Données glossaire + forum + contenu de démonstration |

---

## 10. Stack Technique (conservée et enrichie)

| Composant | Technologie |
|-----------|-------------|
| Backend | Django 5.x (Python 3.12) |
| Base de données | SQLite (dev) → PostgreSQL (prod) |
| Templates | Django Templates |
| CSS | Vanilla CSS (variables, animations, responsive) |
| Fonts | Lexend + Source Sans 3 + JetBrains Mono |
| Icons | Emoji → SVG (Lucide via CDN) |
| Animations | CSS Keyframes + Transitions |
| Déploiement | Render + Neon (futur) |

---

*Document créé le 2026-03-09 — Version 1.0*
*L'Afrique mérite sa plateforme éducative de référence. *
