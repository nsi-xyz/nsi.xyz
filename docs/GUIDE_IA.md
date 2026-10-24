# Travailler avec son IA sur le portail

Ce guide explique comment utiliser Claude Code, OpenCode, Codex, Cursor ou un
autre assistant **sans casser le dépôt**. L’IA peut écrire le code ; c’est toi
qui vérifies, commites et ouvres la pull request.

## Prérequis

1. Ton compte GitHub est ajouté comme collaborateur du dépôt privé
   `nsi-xyz/portail`.
2. Git est installé et configuré (`git config --global user.name` et
   `user.email`).
3. Ton outil d’IA sait ouvrir un dossier et lancer des commandes dans un terminal.

## Mise en place

```bash
git clone git@github.com:nsi-xyz/portail.git
cd portail
```

Ouvre **le dossier `portail/`** dans ton IA, pas le dossier parent : le dépôt
Git s’arrête à `portail/`, le reste du disque contient des sauvegardes qui ne
doivent pas être touchées.

Demande à l’IA de lire `AGENTS.md` **avant** de commencer. Ce fichier contient
les règles, les conventions et les commandes de test.

## Exemple de prompt de départ

> Lis `AGENTS.md` et `CONTRIBUTING.md`. Je veux améliorer le menu mobile du
> portail. Travaille sur une branche `eleve/menu-mobile`, ne touche pas à `main`.
> Montre-moi le diff avant de committer, teste avec le serveur local et lance
> `python3 outils-dev/verifier.py`.

Pour une correction ciblée :

> Lis `AGENTS.md`. Le lien vers `omega.nsi.xyz` semble incorrect dans
> `index.html`. Corrige uniquement ce lien, sans reformater le fichier. Explique
> ce que tu as changé et lance la vérification.

Pour ajouter un site :

> Lis `AGENTS.md`. Ajoute une carte pour `mon-site.nsi.xyz` dans la section
> « Outils », avec `data-site`, `data-tile` et `data-k`. La capture est déjà dans
> `assets/apercus/mon-site.nsi.xyz.webp`. Vérifie que le menu « Tous les sites »
> la prend en compte.

## Ce que tu dois vérifier toi-même

- l’IA n’a pas touché à `main` ni réécrit l’historique ;
- le diff ne contient que les fichiers attendus ;
- le rendu est bon sur téléphone et sur ordinateur ;
- le clavier fonctionne (Tab, Entrée, Échap) ;
- `python3 outils-dev/verifier.py` passe ;
- aucun jeton, mot de passe ou donnée personnelle n’a été ajouté.

## Si l’IA ne peut pas pousser

Fais-lui préparer le commit sur la branche, puis pousse toi-même :

```bash
git push -u origin eleve/mon-idee
```

Ouvre ensuite la pull request sur GitHub. Si tu n’as pas le droit de pousser,
c’est que le compte n’a pas encore été ajouté comme collaborateur : demande à
l’enseignant.

## Ce qu’il ne faut jamais faire

- coller un **jeton GitHub** ou un mot de passe dans le prompt ;
- laisser l’IA exécuter `git push --force`, `git reset --hard` ou supprimer des
  tags ;
- merger une PR sans avoir regardé la préversion ;
- accepter un diff de 3 000 lignes sans le comprendre.

Une petite branche, un petit diff, une PR claire : c’est le plus rapide pour tout
le monde.
