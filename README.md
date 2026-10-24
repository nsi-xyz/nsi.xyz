# Portail nsi.xyz

Maquette du futur portail d’accueil de **nsi.xyz**, conçue par **Ethan M**, élève
en spécialité NSI, avec Claude Opus 5.5, puis reprise dans le cadre du chantier
de migration du site.

> **État : version de travail, non déployée.**
> Le `nsi.xyz` public sert encore la page d’attente violette et l’archive 2021-2026.
> Ce dépôt prépare la future page d’accueil ; il ne remplace rien en production
> tant que la mise en ligne n’a pas été validée.

## Ce que contient le dépôt

Dépôt GitHub : **<https://github.com/nsi-xyz/portail>** (privé, accès sur invitation).

| Élément | Rôle |
|---|---|
| `index.html` | page d’accueil complète (HTML, CSS et JavaScript dans un seul fichier) |
| `conditions.html` | conditions d’utilisation |
| `confidentialite.html` | politique de confidentialité |
| `assets/fonts/` | polices libres Geist et Instrument Sans (SIL OFL 1.1) |
| `assets/apercus/` | captures d’écran des sites présentés (`hôte.webp`) |
| `outils-dev/` | scripts de développement : vérification des liens, captures |
| `docs/` | documentation du projet et historique des variantes |
| `AGENTS.md`, `CLAUDE.md` | consignes pour les assistants IA |

Ce dépôt ne contient **aucune sauvegarde de l’ancien site** et aucun fichier de
migration : ces éléments restent dans le dossier local `migration/`, hors dépôt.

## Voir la page en local

Aucun build, aucune dépendance : c’est du HTML/CSS/JS statique.

```bash
cd portail
python3 -m http.server 8080
```

Puis ouvrir <http://127.0.0.1:8080/>. Un simple double-clic sur `index.html`
fonctionne aussi, mais le serveur local est préférable pour tester les chemins.

## Vérifier avant de proposer une modification

```bash
python3 outils-dev/verifier.py
```

Le script contrôle les liens et assets locaux, les ancres, les identifiants HTML
et quelques métadonnées de base. Il est aussi exécuté automatiquement par GitHub
Actions sur chaque proposition.

## Proposer une amélioration

Le dépôt est partagé pour fonctionner par **pull requests** :

1. créer une branche (`eleve/mon-idee`, `fix/menu-mobile`…) ;
2. modifier le site et tester en local ;
3. lancer `python3 outils-dev/verifier.py` ;
4. pousser la branche et ouvrir une pull request vers `main`.

Le détail est dans [`CONTRIBUTING.md`](CONTRIBUTING.md). Si un assistant IA est
utilisé, lui faire lire [`AGENTS.md`](AGENTS.md) avant toute modification, et
suivre [`docs/GUIDE_IA.md`](docs/GUIDE_IA.md).

## Droits et crédits

- Conception initiale de la page : **Ethan M**, avec Claude Opus 5.5.
- Écosystème, contenus et intégration : **Vincent ROBERT**.
- `rc.nsi.xyz` et les simulateurs de physique-chimie : **Raphaël CLEMENTE**.
- Polices Geist et Instrument Sans : SIL Open Font License 1.1 (licences dans
  `assets/fonts/`).

Les projets d’élèves présentés restent la propriété de leurs auteurs.
