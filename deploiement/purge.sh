#!/usr/bin/env bash
# ==============================================================================
# Purge disque NarwhalChampions.
# Lancé chaque dimanche par narwhal-purge.timer, ou à la main :
#     sudo -u narwhal RACINE=/opt/narwhal narwhal-purge
#     sudo -u narwhal RACINE=/opt/narwhal JOURS=90 narwhal-purge   (plus clément)
#
# Chaque table écrit dans ses propres dossiers. Ce qui se régénère ou ne sert
# qu'un temps est purgé ; ce qui appartient aux joueurs (decks, comptes,
# campagnes, statistiques) n'est JAMAIS touché ici.
# ==============================================================================
set -euo pipefail

RACINE="${RACINE:-@RACINE@}"
MOTEUR="${MOTEUR:-$RACINE/Fusion/marvel-lcg-src}"
JOURS="${JOURS:-30}"

# Liste blanche explicite. Ajouter un dossier ici est une décision, pas un effet
# de bord : tout ce qui n'y figure pas survit.
DOSSIERS_PURGEABLES=(
  "$MOTEUR/replays"
  "$MOTEUR/logs"
  "$MOTEUR/tmp"
  "$RACINE/journaux"
)

echo "Purge des fichiers de plus de $JOURS jours"
for dossier in "${DOSSIERS_PURGEABLES[@]}"; do
  [ -d "$dossier" ] || { echo "  (absent, ignoré) $dossier"; continue; }
  avant="$(du -sh "$dossier" 2>/dev/null | cut -f1)"
  supprimes="$(find "$dossier" -type f -mtime "+$JOURS" -print -delete | wc -l)"
  find "$dossier" -mindepth 1 -type d -empty -delete 2>/dev/null || true
  apres="$(du -sh "$dossier" 2>/dev/null | cut -f1)"
  echo "  $dossier : $supprimes fichiers supprimés ($avant -> $apres)"
done

echo
echo "État du disque :"
df -h / | tail -n +1
