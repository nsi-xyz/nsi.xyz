# Architecture du portail

## Vue d’ensemble

`index.html` est une page autonome : le CSS est dans un `<style>` en tête et le
JavaScript dans un `<script>` en fin de document. Il n’y a ni build, ni framework,
ni dépendance npm. Les seules ressources externes sont les liens vers les sites
de l’écosystème nsi.xyz ; les polices et les captures sont locales.

## Sections de la page

| Ancre | Contenu |
|---|---|
| — | en-tête fixe, logo, menu « Tous les sites », bouton de connexion |
| — | hero : promesse, boutons, modules animés (binaire, terminal) |
| `#essentiels` | les sites du quotidien (login, py, e3c, workflow, nsi42, rc, abc) |
| `#spe` | présentation de la spécialité NSI et des domaines |
| `#outils` | outils en ligne (py, basthon, pyweb, workspace, python.snt, web.snt, simulateurs) |
| `#numworks` | simulateurs Epsilon, Omega, Psi, gestionnaire de scripts |
| `#demos` | démos de cours (discover, css, get, post, password) |
| `#projets` | projets et curiosités (orbis, 42, ia-maths, election, webos, labohelp, 2go…) |
| `#archive` | accès à l’archive 2021-2026 (`/v2/`) et au plan du site |
| — | pied de page, crédits, pages légales |

## Système de design

Les variables sont définies dans `:root` :

- couleurs : `--black`, `--carbon`, `--dark`, `--light`, `--accent`, `--grad` ;
- transparences : `--w2` à `--w73` (fond sombre) et `--d4` à `--d73` (fond clair) ;
- polices : `--f-display` (Instrument Sans), `--f-body` (Geist), `--f-mono` ;
- mise en page : `--site` (largeur max), `--gutter`, `--nav-h` ;
- animations : `--ease`, `--dur`.

Les composants principaux sont `.wrap`, `.btn` (variantes `--main`, `--ghost`,
`--white`, `--sm`), `.big`, `.panel`, `.tile`, `.menu`, `.footer`.

## Cartes de sites et menu automatique

Chaque carte interactive porte :

- `data-site` : marque la carte comme site (utilisé pour les aperçus et le menu) ;
- `data-tile` : 2 ou 3 caractères affichés dans la pastille ;
- `data-k` : mots-clés de recherche, en minuscules et sans accents.

Le menu « Tous les sites » est construit au chargement à partir de ces cartes,
groupées par section. Ajouter une carte correctement suffit donc à l’ajouter au
menu, sans modifier le JavaScript.

## JavaScript

Le script principal est une IIFE. Il gère notamment :

- le fond de la barre de navigation au défilement ;
- l’ouverture et la fermeture du menu (clic, Échap, focus) ;
- les aperçus de sites au survol et au focus ;
- la vitrine NumWorks (rotation automatique, pause au survol) ;
- le module binaire interactif ;
- les onglets du programme NSI ;
- les révélations au défilement (`IntersectionObserver`).

Les animations respectent `prefers-reduced-motion` via la classe `calm` posée
sur `<html>`.

## Accessibilité

- lien d’évitement, landmarks sémantiques, titres hiérarchisés ;
- focus visible, navigation clavier, fermeture du menu avec Échap ;
- textes alternatifs sur les images ;
- contrastes élevés sur fond sombre ;
- les contenus purement décoratifs sont masqués aux lecteurs d’écran.

## Fichiers de développement

- `outils-dev/verifier.py` : contrôles avant PR ;
- `outils-dev/apercus.py` : génération des captures (outil historique) ;
- `outils-dev/apercu-discover.mjs` : capture ciblée via Chrome/CDP (outil historique,
  chemin Chrome à adapter selon la machine).
