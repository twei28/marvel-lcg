#!/usr/bin/env bash
# ==============================================================================
# Sauvegarde des comptes NarwhalChampions.
# Lancé chaque nuit par narwhal-sauvegarde.timer, et à la main quand on veut :
#     sudo -u narwhal RACINE=/opt/narwhal narwhal-sauvegarde
#
# Le fichier des comptes est la seule donnée du site qui ne se régénère pas.
# On ne cherche pas à deviner son nom : on archive tous les petits fichiers
# d'état de site/ (json, db, sqlite), ce qui le contient forcément.
# ==============================================================================
set -euo pipefail

RACINE="${RACINE:-@RACINE@}"
DESTINATION="${DESTINATION:-/var/backups/narwhal}"
CONSERVER="${CONSERVER:-30}"   # nombre d'archives quotidiennes gardées

horodatage="$(date +%Y-%m-%d)"
archive="$DESTINATION/comptes-$horodatage.tar.gz"

mkdir -p "$DESTINATION"

# -maxdepth 2 : l'état vit à la racine de site/, pas au fond de l'arborescence.
mapfile -t fichiers < <(
  find "$RACINE/site" -maxdepth 2 -type f \
       \( -name '*.json' -o -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) \
       -size -20M -print
)

if [ "${#fichiers[@]}" -eq 0 ]; then
  echo "Aucun fichier d'état trouvé dans $RACINE/site — sauvegarde annulée." >&2
  exit 1
fi

tar -czf "$archive" -C / "${fichiers[@]#/}"
chmod 600 "$archive"
echo "Sauvegarde : $archive ($(du -h "$archive" | cut -f1), ${#fichiers[@]} fichiers)"

# Une copie « courante », toujours au même nom, que le script de déploiement
# rapatrie sur le poste sans avoir à deviner la date.
cp -f "$archive" "$DESTINATION/comptes-dernier.tar.gz"

# Rotation.
find "$DESTINATION" -maxdepth 1 -name 'comptes-20*.tar.gz' -type f \
  -printf '%T@ %p\n' | sort -rn | tail -n +$((CONSERVER + 1)) | cut -d' ' -f2- \
  | while read -r vieux; do rm -f -- "$vieux"; echo "Rotation : $vieux supprimé"; done
