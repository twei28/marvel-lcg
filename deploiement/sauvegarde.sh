#!/usr/bin/env bash
# ==============================================================================
# Sauvegarde des comptes NarwhalChampions, et des donnees des joueurs.
# Lancé chaque nuit par narwhal-sauvegarde.timer, et à la main quand on veut :
#     sudo -u narwhal RACINE=/opt/narwhal narwhal-sauvegarde
#     sudo -u narwhal RACINE=/opt/narwhal narwhal-sauvegarde --verifier
#
# Le fichier des comptes est la seule donnée du site qui ne se régénère pas.
# On ne cherche pas à deviner son nom : on archive tous les petits fichiers
# d'état de site/ (json, db, sqlite), ce qui le contient forcément.
#
# S'y ajoutent les CAPTURES DES RAPPORTS DE BUG (site/rapports/). Le texte des
# rapports vit dans narwhal.db, donc déjà pris ; les images, elles, sont sur
# disque et seraient perdues à la restauration — /admin afficherait alors des
# rapports dont la capture manque. Le plafond de -size 20M les couvre : une
# capture réduite par le navigateur pèse moins d'un mégaoctet.
#
# ⚠ AJOUTÉ LE 06/09/2026 (audit E, points 3 et B) : les DECKS, CAMPAGNES,
# HAUTS FAITS (achievements) et REPLAYS des joueurs, qui vivent sous
# Fusion/marvel-lcg-src/ et non sous site/ (deck/serveur-*, campagnes-
# serveur-*, achievements-serveur-*.json, games_history-serveur-*.json,
# statistics-serveur-*.json, replays/serveur-*). Avant ce jour, purge.sh
# effaçait les replays et logs de plus de 30 jours sans qu'ils aient jamais
# été sauvegardés : une partie en cours ou une campagne pouvait disparaître
# définitivement, sans aucun filet.
#
# ⚠ AJOUTÉ LE 06/09/2026 : narwhal.db est en mode WAL (le moteur y écrit sans
# arrêt). Une copie brute du fichier pendant une écriture peut manquer des
# pages encore dans le journal WAL et produire une sauvegarde incohérente.
# `Connection.backup` de Python prend un instantané cohérent, verrou SQLite
# compris. C'est pour ça qu'on passe par une zone de montage temporaire
# ($stage) plutôt que d'archiver les fichiers en place.
# ⚠ 16/09/2026 : cette ligne appelait le CLI `sqlite3`, qui N'EST PAS installé
# sur le serveur. La sauvegarde mourait sur « command not found » sans rien
# produire, et personne ne le voyait : le timer ne lit pas le code de sortie.
# ==============================================================================
set -euo pipefail

RACINE="${RACINE:-@RACINE@}"
# Python du venv du jeu, celui que lance narwhal.service. Repli sur python3 du
# systeme pour un poste de test ou le venv n'existe pas.
PYTHON="${PYTHON:-$RACINE/venv310/bin/python}"
[ -x "$PYTHON" ] || PYTHON="python3"
DESTINATION="${DESTINATION:-/var/backups/narwhal}"
CONSERVER="${CONSERVER:-30}"   # nombre d'archives quotidiennes gardées
MOTEUR="$RACINE/Fusion/marvel-lcg-src"

# --- Mode vérification --------------------------------------------------------
# Restaure la dernière archive dans un dossier temporaire et compte ce qu'elle
# contient. Une sauvegarde jamais restaurée n'est pas une sauvegarde.
if [ "${1:-}" = "--verifier" ]; then
  archive="$DESTINATION/comptes-dernier.tar.gz"
  [ -f "$archive" ] || { echo "Aucune sauvegarde à vérifier : $archive introuvable." >&2; exit 1; }

  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  tar -xzf "$archive" -C "$tmp"

  compter() { find "$tmp" -path "$1" -type f 2>/dev/null | wc -l; }

  echo "Vérification de $archive (restaurée dans $tmp) :"
  echo "  fichiers au total            : $(find "$tmp" -type f | wc -l)"
  echo "  captures de rapports de bug  : $(compter '*/site/rapports/*')"
  echo "  decks serveur                : $(compter '*/deck/serveur-*/*')"
  echo "  campagnes serveur            : $(compter '*/campagnes-serveur-*/*')"
  echo "  replays serveur              : $(compter '*/replays/serveur-*/*')"
  echo "  hauts faits (achievements)   : $(compter '*achievements-serveur-*.json')"
  echo "  fiches du mode Legacy        : $(compter '*legacy-serveur-*.json')"
  echo "  arts alternatifs de heros    : $(compter '*arts-heros-serveur-*.json')"
  echo "  preferences des comptes      : $(compter '*preferences-serveur-*.json')"
  echo "  projets du createur de cartes: $(compter '*/donnees-createur/*/*/courant.json')"

  base="$(find "$tmp" -name 'narwhal.db' -print -quit)"
  if [ -n "$base" ]; then
    n="$("$PYTHON" -c "import sqlite3,sys;print(sqlite3.connect(sys.argv[1]).execute('SELECT count(*) FROM comptes').fetchone()[0])" "$base" 2>/dev/null || echo '?')"
    echo "  comptes dans narwhal.db restaurée : $n"
  else
    echo "  ⚠ narwhal.db absente de l'archive restaurée"
  fi
  exit 0
fi

# --- Sauvegarde ----------------------------------------------------------------
horodatage="$(date +%Y-%m-%d)"
archive="$DESTINATION/comptes-$horodatage.tar.gz"

mkdir -p "$DESTINATION"
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

# Fichiers d'état de site/ (comptes, base, captures de rapports). -maxdepth 2 :
# l'état vit à la racine de site/, pas au fond de l'arborescence.
mapfile -t fichiers_site < <(
  find "$RACINE/site" -maxdepth 2 -type f \
       \( -name '*.json' -o -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \
          -o -name '*.png' -o -name '*.jpg' -o -name '*.webp' \) \
       -size -20M -print
)

if [ "${#fichiers_site[@]}" -eq 0 ]; then
  echo "Aucun fichier d'état trouvé dans $RACINE/site — sauvegarde annulée." >&2
  exit 1
fi

for f in "${fichiers_site[@]}"; do
  rel="${f#"$RACINE"/}"
  dest="$stage/$rel"
  mkdir -p "$(dirname "$dest")"
  case "$f" in
    *.db|*.sqlite|*.sqlite3)
      # Instantané cohérent malgré le mode WAL : voir la note en tête de fichier.
      # ⚠ PAR PYTHON, PAS PAR LE CLI `sqlite3` (16/09/2026). Le binaire n'est
      # PAS installé sur le serveur : `sqlite3: command not found`, et la
      # sauvegarde s'arrêtait là, sans rien produire. `Connection.backup`
      # (Python 3.7+) prend le même instantané, verrou compris, et Python est
      # de toute façon obligatoire pour faire tourner le jeu.
      "$PYTHON" - "$f" "$dest" <<'PYBACKUP'
import sqlite3, sys
source = sqlite3.connect(sys.argv[1])
copie = sqlite3.connect(sys.argv[2])
with copie:
    source.backup(copie)
copie.close()
source.close()
PYBACKUP
      ;;
    *)
      cp -p "$f" "$dest"
      ;;
  esac
done

# ⚠ AJOUTÉ LE 28/10/2026 : les PROJETS DU CRÉATEUR DE CARTES (donnees-createur/
# <compte>/<projet>/courant.json + versions/). Ce sont des fichiers, pas des
# lignes de narwhal.db : sans cette ligne, un compte créateur perdait tout à la
# restauration. Ils portent des images (quota 500 Mo par compte) : l'archive
# peut grossir, d'où la rotation à surveiller. Même dossier que
# `DOSSIER_CREATEUR` dans orchestrateur.py (par défaut à la racine du projet).
if [ -d "$RACINE/donnees-createur" ]; then
  mkdir -p "$stage/donnees-createur"
  cp -a "$RACINE/donnees-createur/." "$stage/donnees-createur/"
fi

# Données des joueurs sous Fusion/marvel-lcg-src/ : jamais sauvegardées avant
# le 06/09/2026, alors que purge.sh efface les replays et logs après 30 jours
# sans filet (voir la note en tête de fichier).
shopt -s nullglob
for dossier in \
  "$MOTEUR"/deck/serveur-*/ \
  "$MOTEUR"/campagnes-serveur-*/ \
  "$MOTEUR"/replays/serveur-*/ ; do
  for d in $dossier; do
    d="${d%/}"
    rel="${d#"$RACINE"/}"
    mkdir -p "$stage/$rel"
    cp -a "$d/." "$stage/$rel/"
  done
done
# ⚠ `legacy-serveur-*.json` AJOUTE LE 16/09/2026. Le mode Legacy est arrive le
# 13/09, cette liste datait du 06/09, et personne ne l'a reprise : ce que le
# joueur a debloque (la vague atteinte, les jetons depenses, la date de depart)
# n'avait donc aucun filet. Ce n'est PAS reconstructible depuis
# `games_history-serveur-N.json` : l'historique dit les parties, pas les jetons
# depenses ni le « repartir de zero ».
for motif in \
  "$MOTEUR"/achievements-serveur-*.json \
  "$MOTEUR"/games_history-serveur-*.json \
  "$MOTEUR"/statistics-serveur-*.json \
  "$MOTEUR"/legacy-serveur-*.json \
  "$MOTEUR"/arts-heros-serveur-*.json \
  "$MOTEUR"/preferences-serveur-*.json ; do
  for f in $motif; do
    rel="${f#"$RACINE"/}"
    mkdir -p "$(dirname "$stage/$rel")"
    cp -p "$f" "$stage/$rel"
  done
done
shopt -u nullglob

tar -czf "$archive" -C "$stage" .
chmod 600 "$archive"
echo "Sauvegarde : $archive ($(du -h "$archive" | cut -f1), $(find "$stage" -type f | wc -l) fichiers)"

# Une copie « courante », toujours au même nom, que le script de déploiement
# rapatrie sur le poste sans avoir à deviner la date.
cp -f "$archive" "$DESTINATION/comptes-dernier.tar.gz"

# Rotation.
find "$DESTINATION" -maxdepth 1 -name 'comptes-20*.tar.gz' -type f \
  -printf '%T@ %p\n' | sort -rn | tail -n +$((CONSERVER + 1)) | cut -d' ' -f2- \
  | while read -r vieux; do rm -f -- "$vieux"; echo "Rotation : $vieux supprimé"; done
