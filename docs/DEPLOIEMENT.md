# Déploiement du portail

> **Statut au 24/10/2026 : en production sur https://nsi.xyz/.**
> Le portail est à la racine ; l’archive 2021-2026 est servie sous `/v2/`.
> La production est déployée par le script `outils-dev/deployer.sh`, pas
> automatiquement à chaque push.

## Contrainte à garder en tête

Le portail doit continuer à servir l’archive sous `/v2/`, `/plan/` et les
anciennes URL d’articles. Un domaine Cloudflare Pages ne pointe que vers **un
seul projet** : la production est donc construite en combinant le portail et
l’archive dans un même déploiement.

## Architecture retenue : un seul projet Pages

Le projet Cloudflare Pages **`nsi-xyz`** sert :

```
/                  → portail (fichiers de ce dépôt)
/v2/               → accueil de l’archive 2021-2026
/v2/plan/          → plan de l’archive (l’ancien /plan/ redirige)
/projets/, /tutoriels/, /art/, /numapps/… → articles à leurs URL d’origine
/wp-content/…      → médias de l’archive
```

Le script `outils-dev/deployer.sh` :

1. copie l’archive locale (code + médias) dans un dossier de staging ;
2. remplace la racine par les fichiers du portail ;
3. déploie le tout vers le projet `nsi-xyz`.

```bash
export CLOUDFLARE_API_TOKEN=…
export CLOUDFLARE_ACCOUNT_ID=…
./outils-dev/deployer.sh /chemin/vers/archive-v2 preview
./outils-dev/deployer.sh /chemin/vers/archive-v2 production
```

Cette méthode conserve les 1,9 Go de médias de l’archive, qui ne sont pas dans
Git. Si l’archive devient un jour déployée automatiquement depuis GitHub, il
faudra d’abord intégrer ces médias (après optimisation WebP) ou les placer sur
un stockage externe.

## Préversions des pull requests

Le dépôt `nsi-xyz/nsi.xyz` peut être connecté à un projet Pages de préversion
distinct (`portail-nsi-xyz`) pour obtenir une URL par PR. La production reste
déployée par le script ci-dessus, après fusion et validation.

Aucune PR ne doit être mergée sans avoir vérifié le rendu.

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
