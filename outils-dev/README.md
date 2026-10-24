# Outils de développement

Ces scripts ne sont **pas** utilisés par le site en production.

## `verifier.py`

Vérification à lancer avant chaque pull request :

```bash
python3 outils-dev/verifier.py
```

Il contrôle les liens et assets locaux, les ancres, les identifiants HTML, les
images sans `alt`, les polices référencées dans le CSS et les métadonnées de base.
La même commande tourne dans GitHub Actions.

## `deployer.sh`

Déploie le portail **avec l’archive v2** vers le projet Cloudflare Pages
`nsi-xyz`. Le script prend le dossier local de l’archive en argument, pour
conserver les médias qui ne sont pas versionnés.

```bash
export CLOUDFLARE_API_TOKEN=…
export CLOUDFLARE_ACCOUNT_ID=…
./outils-dev/deployer.sh /chemin/vers/archive-v2 preview
./outils-dev/deployer.sh /chemin/vers/archive-v2 production
```

## `apercus.py`

Outil historique de génération des captures `assets/apercus/*.webp`. Il dépend de
Chromium/Chrome et de la disponibilité des sites distants. À utiliser seulement
si une capture doit être refaite.

## `apercu-discover.mjs`

Capture ciblée d’un site via Chrome et le protocole CDP. Le chemin de Chrome est
codé pour Windows (`C:/Program Files/...`) : l’adapter à la machine avant usage.
