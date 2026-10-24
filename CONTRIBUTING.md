# Contribuer au portail nsi.xyz

Merci de participer ! Ce dépôt sert à faire évoluer la page d’accueil du portail
**sans jamais toucher à la production directement**. Tout passe par une branche
et une **pull request** (PR).

## Règle d’or

- `main` reste stable et lisible : **on ne pousse jamais directement sur `main`**.
- Une PR = **un sujet** (un correctif, une amélioration, une section).
- On ne modifie pas les fichiers d’une autre PR en cours.

## Pas à pas

### 1. Récupérer le dépôt

Le dépôt est **public**. Tu peux travailler sur un fork, ou demander à
l’enseignant de t’ajouter comme collaborateur pour pousser une branche
directement. Dans les deux cas, la pull request devra être validée avant fusion.

```bash
git clone git@github.com:nsi-xyz/nsi.xyz.git
cd portail
```

### 2. Créer une branche

```bash
git switch -c eleve/mon-idee
```

Exemples de noms : `eleve/menu-mobile`, `fix/lien-omega`, `design/hero-2026`.

### 3. Modifier et tester

```bash
python3 -m http.server 8080
# ouvrir http://127.0.0.1:8080/
```

Tester au minimum :

- la page à 1366 × 768 et sur un écran de téléphone (mode responsive) ;
- la navigation au clavier (Tab, Entrée, Échap) ;
- les liens modifiés ;
- l’absence d’erreur dans la console du navigateur.

### 4. Vérifier

```bash
python3 outils-dev/verifier.py
```

### 5. Committer et pousser

```bash
git add index.html assets/...
git commit -m "Menu mobile : fermeture au clic sur un lien"
git push -u origin eleve/menu-mobile
```

### 6. Ouvrir la pull request

Sur GitHub, ouvrir une PR de `eleve/mon-idee` vers `main`, puis remplir le modèle :
description, captures avant/après, tests effectués.

## Ce qu’on accepte volontiers

- corrections de liens, de fautes, de responsive ;
- améliorations d’accessibilité (contrastes, focus, lecteurs d’écran) ;
- nouveaux sites à présenter, avec une capture `assets/apercus/hote.webp` ;
- optimisations de performance raisonnables (poids des images, chargement) ;
- idées de sections ou d’animations, si elles restent sobres et lisibles.

## Ce qu’il faut éviter

- ajouter un framework ou une étape de build : le site doit rester statique ;
- ajouter un CDN ou un script externe sans accord préalable ;
- réécrire tout `index.html` avec un formateur automatique (le fichier est gros
  et le diff deviendrait illisible) ;
- modifier `conditions.html` ou `confidentialite.html` sans raison juridique ;
- mettre des mots de passe, jetons, clés ou données personnelles dans le dépôt ;
- ajouter des médias lourds (vidéos, archives, polices supplémentaires) sans en
  parler d’abord.

## Utiliser une IA

Les assistants IA sont les bienvenus, à condition de cadrer le travail :

1. faire lire **`AGENTS.md`** (ou `CLAUDE.md` pour Claude Code) ;
2. suivre [`docs/GUIDE_IA.md`](docs/GUIDE_IA.md) pour les prompts et les précautions ;
3. demander une modification **limitée** et une branche dédiée ;
4. relire le diff avant de committer ;
5. ne jamais coller un jeton GitHub, un mot de passe ou une clé dans le prompt ;
6. vérifier le rendu et lancer `outils-dev/verifier.py` avant la PR.

Une IA peut proposer, mais c’est l’élève qui reste responsable de ce qui est
envoyé.

## En cas de doute

Ouvrir une *issue* avec le modèle « Idée » ou demander avant de commencer un gros
chantier. Il vaut mieux discuter cinq minutes que réécrire trois jours.
