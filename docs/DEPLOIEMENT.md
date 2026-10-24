# Déploiement du portail

> **Statut au 24/10/2026 : aucun déploiement automatique n’est encore actif.**
> Le site public `nsi.xyz` sert toujours la page d’attente violette et l’archive
> 2021-2026. Ce dépôt contient la future page d’accueil, pas la production.

## Principe prévu

Le portail est un site **statique** : aucun build n’est nécessaire. La cible
naturelle est **Cloudflare Pages**, comme les autres sites de l’écosystème.

| Paramètre | Valeur prévue |
|---|---|
| Dépôt | `nsi-xyz/portail` (branche `main`) |
| Projet Pages | `portail-nsi-xyz` (nom sans point, important pour le TLS) |
| Commande de build | aucune |
| Dossier de sortie | `/` (racine du dépôt) |
| Domaine | `nsi.xyz` et `www.nsi.xyz`, après validation |

Le nom du projet Pages ne doit **pas** contenir de point : un projet nommé
`portail.nsi.xyz` produirait `portail.nsi.xyz.pages.dev`, non couvert par le
certificat `*.pages.dev` (erreur 1014).

## Pull requests et préversions

Une fois le dépôt connecté à Cloudflare Pages :

- chaque pull request peut produire une **URL de préversion** ;
- `main` produit la production, mais seulement après validation ;
- aucune PR ne doit être mergée sans avoir vérifié la préversion.

## Ce qu’il ne faut pas faire

- déployer depuis un dossier local mélangé avec les sauvegardes ;
- mettre des médias de l’ancien site dans ce dépôt ;
- ajouter des variables secrètes dans le code ;
- modifier les MX ou les autres enregistrements DNS lors d’une bascule.

## Bascule finale (plus tard)

1. valider la page sur une URL de préversion ;
2. connecter le projet Pages au dépôt ;
3. créer le domaine personnalisé `nsi.xyz` ;
4. basculer le CNAME de `nsi-xyz.pages.dev` vers `portail-nsi-xyz.pages.dev` ;
5. conserver l’archive `/v2/` accessible (elle vit dans un autre projet) ;
6. vérifier HTTP → HTTPS, les redirections et les pages légales ;
7. seulement ensuite, annoncer la mise en ligne.

Tant que la bascule n’est pas faite, `https://nsi.xyz/` reste l’ancienne page
d’attente : il ne faut pas communiquer l’URL comme « nouveau portail ».
