# Claude Code — portail nsi.xyz

Lire **`AGENTS.md`** avant toute action : il contient le contexte, les règles de
sécurité, les conventions et le workflow de pull request.

Points spécifiques à Claude Code :

- travailler sur une branche dédiée, jamais directement sur `main` ;
- ne pas lancer de formateur global sur `index.html` ;
- tester avec `python3 -m http.server 8080` puis `python3 outils-dev/verifier.py` ;
- ne pas modifier `conditions.html` ou `confidentialite.html` sans demande explicite ;
- ne jamais écrire de jeton ou de secret dans un fichier suivi par Git.

Le reste des consignes est dans `AGENTS.md`.
