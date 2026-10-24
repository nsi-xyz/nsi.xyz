#!/usr/bin/env bash
# Déploie le portail nsi.xyz en conservant l’archive v2 et ses médias.
#
# Usage :
#   ./outils-dev/deployer.sh /chemin/vers/archive-v2 preview
#   ./outils-dev/deployer.sh /chemin/vers/archive-v2 production
#
# Prérequis : wrangler (Node ≥ 22), CLOUDFLARE_API_TOKEN et
# CLOUDFLARE_ACCOUNT_ID dans l’environnement.
set -euo pipefail

PORTAL="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE="${1:-}"
MODE="${2:-preview}"

if [ -z "$ARCHIVE" ] || [ ! -f "$ARCHIVE/index.html" ] || [ ! -d "$ARCHIVE/wp-content" ]; then
	echo "Usage : $0 /chemin/vers/archive-v2 [preview|production]" >&2
	echo "Le dossier doit contenir index.html et wp-content/." >&2
	exit 2
fi

case "$MODE" in
	preview) BRANCH="preview" ;;
	production) BRANCH="main" ;;
	*) echo "Mode inconnu : $MODE (attendu : preview ou production)" >&2; exit 2 ;;
esac

if [ -z "${CLOUDFLARE_API_TOKEN:-}" ] || [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
	echo "CLOUDFLARE_API_TOKEN et CLOUDFLARE_ACCOUNT_ID doivent être définis." >&2
	exit 1
fi

export PATH="$HOME/.nvm/versions/node/v22.23.4/bin:$PATH"
WRANGLER="${WRANGLER:-/home/cent20/Informatique/2go-ovh/node_modules/.bin/wrangler}"
[ -x "$WRANGLER" ] || { echo "wrangler introuvable : $WRANGLER" >&2; exit 1; }

STAGE="$PORTAL/.deploy-staging"
trap 'rm -rf "$STAGE"' EXIT
rm -rf "$STAGE"
mkdir -p "$STAGE"

# L’archive est copiée avec des liens durs : rapide et sans doubler les 2 Go.
cp -al "$ARCHIVE/." "$STAGE/"

# On ne publie ni l’historique, ni les fichiers de travail.
rm -rf "$STAGE/.git" "$STAGE/.wrangler" "$STAGE/README.md" "$STAGE/.gitignore"

# Le portail prend la racine ; l’archive reste sous /v2/, /projets/, etc.
cp -a "$PORTAL/index.html" "$PORTAL/conditions.html" "$PORTAL/confidentialite.html" "$STAGE/"
mkdir -p "$STAGE/assets"
cp -a "$PORTAL/assets/." "$STAGE/assets/"

echo "Déploiement du portail + archive ($MODE)…"
cd "$STAGE"
"$WRANGLER" pages deploy . --project-name nsi-xyz --branch "$BRANCH"
