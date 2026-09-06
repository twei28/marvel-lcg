#!/usr/bin/env bash
# ==============================================================================
# Redimensionne les images custom SUR LE SERVEUR (ImageMagick y est installé).
# À lancer seulement si le disque se remplit :
#     ssh root@IP 'bash /opt/narwhal/redimensionner-images.sh 800'
# Les originaux restent intacts sur votre poste ; seule la copie serveur change.
# ==============================================================================
set -euo pipefail
LARGEUR="${1:-800}"
PICS="${PICS:-/opt/narwhal/Fusion/marvel-lcg-src/assets/pics}"

[ -d "$PICS" ] || { echo "Introuvable : $PICS" >&2; exit 1; }
command -v mogrify >/dev/null || { echo "ImageMagick absent." >&2; exit 1; }

avant="$(du -sh "$PICS" | cut -f1)"
echo "Avant : $avant — redimensionnement vers ${LARGEUR}px de large…"

n=0
while IFS= read -r -d '' img; do
  # -resize "800x>" ne touche pas les images déjà plus petites.
  mogrify -resize "${LARGEUR}x>" -strip -quality 88 "$img"
  n=$((n + 1))
  [ $((n % 200)) -eq 0 ] && echo "  $n images…"
done < <(find "$PICS" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) -print0)

apres="$(du -sh "$PICS" | cut -f1)"
echo "Terminé : $n images, $avant -> $apres"
echo "⚠ Au prochain déploiement, les originaux seraient renvoyés : relancez ce"
echo "  script après, ou passez REDIM=1 dans le script de déploiement."
