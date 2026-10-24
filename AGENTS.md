# Consignes pour les assistants IA — portail nsi.xyz

Ce fichier s’adresse à tout assistant IA (Claude Code, OpenCode, Codex, Cursor…)
qui travaille sur ce dépôt. Il doit être lu **avant** de proposer une modification.
Le dépôt est un site statique : **pas de build, pas de framework, pas de serveur**.

## 1. Contexte

- Projet : future page d’accueil du portail **nsi.xyz**.
- Public : élèves de seconde, première et terminale NSI, enseignants, visiteurs.
- Langue : **français**, ton clair et direct, sans jargon inutile.
- Auteur initial du design : Ethan M (élève), avec Claude Opus 5.5.
- Le site public actuel est encore l’ancienne page d’attente : ce dépôt n’est
  **pas** déployé en production. Ne pas promettre une mise en ligne.

## 2. Périmètre

Travailler **uniquement** dans ce dépôt. Les dossiers de sauvegarde, d’inventaire
et de migration de l’ancien site sont **hors dépôt** et ne doivent jamais être
créés, déplacés ou référencés ici.

Fichiers principaux :

| Fichier | Rôle |
|---|---|
| `index.html` | page complète ; CSS et JS sont volontairement inline |
| `conditions.html` | conditions d’utilisation |
| `confidentialite.html` | politique de confidentialité |
| `assets/fonts/` | polices locales, licences OFL |
| `assets/apercus/` | captures `hote.webp` des sites présentés |
| `outils-dev/verifier.py` | vérification liens, assets, ancres, IDs |
| `docs/` | architecture, déploiement, historique |

## 3. Règles à ne pas enfreindre

1. **Ne jamais pousser sur `main`.** Créer une branche :
   `eleve/<sujet>`, `fix/<sujet>` ou `design/<sujet>`.
2. **Ne jamais réécrire l’historique Git** (`rebase`, `reset --hard`, `push --force`,
   suppression de tags). Les tags `v1-vert` … `v13-retours-prof` documentent les
   versions successives.
3. **Ne pas ajouter de framework, bundler, npm, CDN ou script externe.** Le site
   doit rester ouvrable par double-clic et déployable tel quel.
4. **Ne pas reformater tout `index.html`.** Le fichier fait plus de 2 000 lignes ;
   un formateur global rendrait le diff impossible à relire. Modifier par petites
   touches ciblées.
5. **Préserver l’existant** : design, textes, liens, crédits, pages légales. Une
   modification de contenu doit être justifiée dans la PR.
6. **Aucun secret** : pas de jeton, mot de passe, clé SSH, adresse privée ou donnée
   personnelle d’élève dans le dépôt ou dans un prompt.
7. **Accessibilité** : conserver la navigation clavier, les `aria-*`, les contrastes
   et les textes alternatifs. Tester Tab / Entrée / Échap.
8. **Mobile** : vérifier au moins 360 px de large et 1366 × 768.

## 4. Workflow attendu

```bash
# 1. partir d’une main à jour
git switch main
git pull

# 2. branche dédiée
git switch -c eleve/mon-sujet

# 3. modifier, puis tester
python3 -m http.server 8080
python3 outils-dev/verifier.py

# 4. commit lisible, en français
git add <fichiers concernés>
git commit -m "Menu mobile : fermeture au clic sur un lien"
git push -u origin eleve/mon-sujet
```

Ensuite : ouvrir une **pull request** vers `main` et remplir le modèle. Ne pas
merger soi-même sans validation.

## 5. Conventions de code

- HTML sémantique : `header`, `nav`, `main`, `section`, `footer`, titres hiérarchisés.
- CSS : réutiliser les variables de `:root` (`--accent`, `--grad`, `--w*`, `--d*`,
  `--f-display`, `--f-body`, `--site`, `--gutter`). Ne pas introduire de couleur
  codée en dur si une variable existe.
- Le CSS et le JS sont inline dans `index.html` : garder cette organisation pour
  l’instant, sauf décision explicite de les extraire.
- JS : le script principal est une IIFE en fin de page. Ne pas créer de variable
  globale nouvelle. Les cartes de sites utilisent `data-site`, `data-tile`,
  `data-k` ; le menu « Tous les sites » est construit automatiquement à partir de
  ces attributs.
- Images : WebP de préférence, nommées `hote.webp`, poids raisonnable (< 150 Ko
  si possible). Les polices restent locales.
- Textes : français, typographie soignée (apostrophes courbes, espaces insécables
  là où elles existent déjà). Ne pas traduire les noms de sites.

## 6. Ajouter un site au portail

1. Ajouter la carte dans la section adaptée (`#essentiels`, `#outils`, `#numworks`,
   `#demos`, `#projets`…).
2. Renseigner `href`, `data-site`, `data-tile` (2-3 caractères) et `data-k`
   (mots-clés de recherche, sans accents).
3. Déposer la capture dans `assets/apercus/<hote>.webp`.
4. Vérifier que le menu « Tous les sites » l’a bien pris en compte.
5. Tester le lien externe et la carte au clavier.

## 7. Vérifications avant de rendre la main

- [ ] `python3 outils-dev/verifier.py` passe sans erreur.
- [ ] La page s’ouvre en local sans erreur console.
- [ ] Le rendu est correct sur mobile et desktop.
- [ ] La navigation clavier fonctionne (Tab, Entrée, Échap).
- [ ] Aucun secret ni donnée personnelle ajouté.
- [ ] Le diff ne contient que les fichiers utiles.
- [ ] La PR explique le **pourquoi**, pas seulement le **quoi**, avec captures si
      le rendu change.

## 8. Si une demande est floue

Ne pas inventer. Proposer une hypothèse courte, poser une question, ou faire une
modification minimale réversible. Mieux vaut une petite PR juste qu’une grosse PR
incertaine.
