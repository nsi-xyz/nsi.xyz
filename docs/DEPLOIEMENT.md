# Déploiement du portail

> **Statut au 24/10/2026 : aucun déploiement automatique n’est encore actif.**
> Le site public `nsi.xyz` sert toujours la page d’attente violette et l’archive
> 2021-2026. Ce dépôt contient la future page d’accueil, pas la production.

## Contrainte à garder en tête

Le portail doit continuer à servir l’archive sous `/v2/` et le plan sous `/plan/`.
Un domaine Cloudflare Pages ne pointe que vers **un seul projet** : il faut donc
choisir explicitement comment assembler les deux.

## Deux architectures possibles

### Option A — un seul projet Pages (recommandée à terme)

Le dépôt `nsi-xyz/nsi.xyz` devient le dépôt de production unique :

```
/            → portail (fichiers de ce dépôt)
/v2/         → archive 2021-2026 (déjà dans le dépôt de production)
/plan/       → plan du site
```

Les modifications validées dans `portail/` sont reportées dans le dépôt de
production (copie des fichiers, ou fusion Git). Avantages : un seul projet, un
seul domaine, pas de Worker de routage. Inconvénient : il faut organiser le
report des PR validées.

### Option B — projet Pages séparé

Un projet `portail-nsi-xyz` sert le portail, et un Worker route `/v2/*` et
`/plan/*` vers le projet de l’archive. Plus souple pour les préversions, mais
plus complexe à exploiter.

## Préversions des pull requests

Dans les deux cas, l’objectif est qu’une PR produise une **URL de préversion** :

- soit en connectant `nsi-xyz/portail` à un projet Pages de préversion ;
- soit en générant un déploiement de préversion par GitHub Actions.

Aucune PR ne doit être mergée sans avoir vérifié le rendu sur cette URL.

## Paramètres techniques

| Paramètre | Valeur |
|---|---|
| Type | site statique, aucun build |
| Dossier de sortie | `/` (racine du dépôt) |
| Nom de projet Pages | sans point (`portail-nsi-xyz`, pas `portail.nsi.xyz`) |
| Node | inutile pour le site ; Node ≥ 22 seulement pour Wrangler |

Le nom du projet Pages ne doit **pas** contenir de point : un projet nommé
`portail.nsi.xyz` produirait `portail.nsi.xyz.pages.dev`, non couvert par le
certificat `*.pages.dev` (erreur 1014).

## Bascule finale (plus tard)

1. choisir l’architecture A ou B ;
2. valider la page sur une URL de préversion ;
3. connecter le projet Pages au bon dépôt ;
4. vérifier `/`, `/v2/`, `/plan/`, les pages légales et les redirections ;
5. basculer le DNS de `nsi.xyz` si nécessaire ;
6. vérifier HTTP → HTTPS et les enregistrements MX/TXT (ne pas y toucher) ;
7. seulement ensuite, annoncer la mise en ligne.

Tant que la bascule n’est pas faite, `https://nsi.xyz/` reste l’ancienne page
d’attente : il ne faut pas communiquer l’URL comme « nouveau portail ».
