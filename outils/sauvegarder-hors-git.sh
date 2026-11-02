#!/bin/bash
# Sauvegarde de tout ce que GitHub NE contient PAS (02/11/2026).
#
#   bash outils/sauvegarder-hors-git.sh /media/oem/USB/sauvegarde-marvel          # copie reelle
#   bash outils/sauvegarder-hors-git.sh /media/oem/USB/sauvegarde-marvel --essai  # montre sans copier
#
# GitHub garde le code et les donnees. Ce script copie le reste, ignore par .gitignore :
# les scans (EN, FR, HD), les livrets PDF, les paquets de createurs et les zips sources.
# Copie incrementale (rsync) : relancer ne recopie que ce qui a change. Rien n'est jamais supprime
# a la destination. Environ 28 Go (dont 17 Go de zips a la racine) : verifier la place libre avant.
set -euo pipefail

DEST="${1:?Usage : sauvegarder-hors-git.sh <dossier-destination> [--essai]}"
OPTION="${2:-}"
RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RACINE"

ARGS=(-a --info=progress2 --human-readable)
[ "$OPTION" = "--essai" ] && ARGS+=(--dry-run)
mkdir -p "$DEST"

# Dossiers entiers (chemins relatifs a la racine du depot).
DOSSIERS=(
  "Fusion/marvel-lcg-src/assets/pics"
  "Fusion/marvel-lcg-src/assets/pics-fr"
  "Fusion/marvel-lcg-src/assets/pics-hd"
  "Fusion/marvel-lcg-src/assets/docs"
  "A créer"
  "paquets-cartes"
  "medias"
)
for d in "${DOSSIERS[@]}"; do
  [ -d "$d" ] || { echo "absent, ignore : $d"; continue; }
  echo "== $d"
  rsync "${ARGS[@]}" -R "$d" "$DEST/"
done

# Zips sources a la racine du depot.
echo "== zips a la racine"
rsync "${ARGS[@]}" --include='*.zip' --exclude='*' ./ "$DEST/zips-racine/"

echo "Termine : $DEST"
