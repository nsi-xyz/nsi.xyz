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

## `apercus.py`

Outil historique de génération des captures `assets/apercus/*.webp`. Il dépend de
Chromium/Chrome et de la disponibilité des sites distants. À utiliser seulement
si une capture doit être refaite.

## `apercu-discover.mjs`

Capture ciblée d’un site via Chrome et le protocole CDP. Le chemin de Chrome est
codé pour Windows (`C:/Program Files/...`) : l’adapter à la machine avant usage.
