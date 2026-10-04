#!/usr/bin/env bash
# ==============================================================================
# Purge disque NarwhalChampions.
# Lancé chaque dimanche par narwhal-purge.timer, ou à la main :
#     sudo -u narwhal RACINE=/opt/narwhal narwhal-purge
#     sudo -u narwhal RACINE=/opt/narwhal JOURS=90 narwhal-purge   (plus clément)
#     sudo -u narwhal RACINE=/opt/narwhal JOURS_REPLAYS=7 narwhal-purge   (sauvegardes seules)
#
# Chaque table écrit dans ses propres dossiers. Ce qui se régénère ou ne sert
# qu'un temps est purgé ; ce qui appartient aux joueurs (decks, comptes,
# campagnes, statistiques) n'est JAMAIS touché ici.
# ==============================================================================
set -euo pipefail

RACINE="${RACINE:-@RACINE@}"
MOTEUR="${MOTEUR:-$RACINE/Fusion/marvel-lcg-src}"
JOURS="${JOURS:-30}"
# Seuil propre aux sauvegardes de partie (24/09/2026, demande de
# l'utilisateur : la liste "Reprendre une partie" s'accumulait) -- plus court
# que JOURS, qui reste a 30 jours pour logs/tmp/journaux.
JOURS_REPLAYS="${JOURS_REPLAYS:-14}"

# Liste blanche explicite. Ajouter un dossier ici est une décision, pas un effet
# de bord : tout ce qui n'y figure pas survit.
DOSSIERS_PURGEABLES=(
  "$MOTEUR/replays"
  "$MOTEUR/logs"
  "$MOTEUR/tmp"
  "$RACINE/journaux"
)

echo "Purge des fichiers de plus de $JOURS jours ($JOURS_REPLAYS pour les sauvegardes de partie)"
for dossier in "${DOSSIERS_PURGEABLES[@]}"; do
  [ -d "$dossier" ] || { echo "  (absent, ignoré) $dossier"; continue; }
  seuil="$JOURS"
  [ "$dossier" = "$MOTEUR/replays" ] && seuil="$JOURS_REPLAYS"
  avant="$(du -sh "$dossier" 2>/dev/null | cut -f1)"
  supprimes="$(find "$dossier" -type f -mtime "+$seuil" -print -delete | wc -l)"
  find "$dossier" -mindepth 1 -type d -empty -delete 2>/dev/null || true
  apres="$(du -sh "$dossier" 2>/dev/null | cut -f1)"
  echo "  $dossier (+${seuil}j) : $supprimes fichiers supprimés ($avant -> $apres)"
done

# --- Rapports de bug classés « traité » ---------------------------------------
# ⚠ CE DOSSIER N'ÉTAIT PURGÉ PAR RIEN, et il est le seul du site à recevoir des
# octets d'inconnus. Le plafond est de 12 rapports par heure ET PAR TABLE, avec
# une capture jusqu'à 4 Mio : vingt tables donnent une borne de l'ordre du
# gigaoctet par heure, et la sauvegarde de nuit multipliait le total par trente
# en gardant trente archives.
#
# ⚠ ET ON NE LE FAIT PAS AVEC `find`. Effacer les fichiers en laissant les
# lignes derrière donnerait une page d'administration qui renvoie vers des
# captures disparues. L'orchestrateur sait faire les deux d'un coup : on
# l'appelle plutôt que de recopier la règle ici.
PYTHON="${PYTHON:-$RACINE/venv310/bin/python}"
ORCHESTRATEUR="$RACINE/site/orchestrateur.py"
echo
echo "Rapports de bug traités depuis plus de $JOURS jours :"
if [ ! -f "$ORCHESTRATEUR" ]; then
  echo "  (orchestrateur absent, ignoré) $ORCHESTRATEUR"
elif [ ! -x "$PYTHON" ]; then
  echo "  (python introuvable, ignoré) $PYTHON"
else
  "$PYTHON" "$ORCHESTRATEUR" purger-rapports "$JOURS" \
    || echo "  ⚠ la purge des rapports a échoué, rien n'a été supprimé"
fi

echo
echo "État du disque :"
df -h / | tail -n +1
