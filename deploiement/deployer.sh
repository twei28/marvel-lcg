#!/usr/bin/env bash
# ==============================================================================
# NarwhalChampions — déploiement depuis votre poste vers le VPS.
#
#     ./deployer.sh              déploiement normal
#     ./deployer.sh --images     images uniquement (aucun redémarrage)
#     ./deployer.sh --code       code uniquement
#     ./deployer.sh --essai      montre ce qui serait transféré, ne transfère rien
#
# Le dépôt ne suffit pas : assets/pics/ est dans le .gitignore, les images
# custom ne voyagent que par ce script.
#
# Nécessite : bash, rsync, ssh. Sous Windows, lancez-le depuis WSL ou Git Bash.
# ==============================================================================
set -euo pipefail

# ---------------------------------------------------------------- réglages ---
SERVEUR="${SERVEUR:-narwhal@VOTRE_IP}"          # ← IP du VPS après achat
DOMAINE="${DOMAINE:-narwhalchampions.com}"
PROJET="${PROJET:-$HOME/NarwhalChampions}"       # ← racine du projet sur ce poste
RACINE_DIST="${RACINE_DIST:-/opt/narwhal}"

# Images custom : 0 = originaux 1500x2150 (~1,9 Go)
#                 1 = redimensionnés à LARGEUR px (~200 Mo)
# Commencez à 0 ; passez à 1 si le transfert ou le disque coince.
REDIM="${REDIM:-0}"
LARGEUR="${LARGEUR:-800}"
CACHE_REDIM="${CACHE_REDIM:-$PROJET/.images-redim}"

# Dossiers écrits par les tables : ils vivent sur le serveur et ne doivent
# jamais être ni écrasés par le poste, ni supprimés par --delete.
# ⚠ Ajustez cette liste aux noms réels de votre arborescence.
DONNEES=(
  --exclude 'sauvegardes/' --exclude 'saves/'
  --exclude 'decks/'       --exclude 'campagnes/'
  --exclude 'statistiques/' --exclude 'achievements/'
  --exclude 'replays/'     --exclude 'logs/'
  --exclude 'comptes.json' --exclude '*.db' --exclude '*.sqlite3'
)
JETABLES=(
  --exclude '.git/' --exclude '__pycache__/' --exclude '*.pyc'
  --exclude '.venv/' --exclude 'venv/' --exclude '.DS_Store'
  --exclude '.images-redim/'
  # ⚠ AJOUTE LE 05/09/2026, PANNE RENCONTREE EN PRODUCTION.
  # `.game/` et `.game-src/` sont les dossiers de CONSTRUCTION du moteur, et
  # ils ne contiennent que des LIENS SYMBOLIQUES vers des chemins du poste
  # local (`/mnt/c/Users/...`). Copies tels quels sur le serveur, ils y
  # arrivent tous casses : le moteur demarre puis meurt sur
  # « No such file or directory: .game/deck/serveur-1 », et l'orchestrateur
  # rend un 503 sans que rien n'explique pourquoi. Le serveur reconstruit ces
  # dossiers tout seul au premier `launcher_fast.py`.
  # `.site/` est de meme nature : configurations generees et journaux des
  # moteurs, propres a chaque machine.
  --exclude '.game/' --exclude '.game-src/' --exclude '.site/'
)
# ------------------------------------------------------------------------------

FAIRE_CODE=1; FAIRE_IMAGES=1; ESSAI=()
case "${1:-}" in
  --images) FAIRE_CODE=0 ;;
  --code)   FAIRE_IMAGES=0 ;;
  --essai)  ESSAI=(--dry-run) ;;
  "")       ;;
  *) echo "Option inconnue : $1" >&2; exit 2 ;;
esac

MOTEUR_LOCAL="$PROJET/Fusion/marvel-lcg-src"
PICS_LOCAL="$MOTEUR_LOCAL/assets/pics"

echo "== Contrôles"
[ -d "$MOTEUR_LOCAL" ] || { echo "Introuvable : $MOTEUR_LOCAL — corrigez PROJET." >&2; exit 1; }
[ -f "$PROJET/site/orchestrateur.py" ] || { echo "Introuvable : $PROJET/site/orchestrateur.py" >&2; exit 1; }
command -v rsync >/dev/null || { echo "rsync manquant." >&2; exit 1; }
ssh -o BatchMode=yes -o ConnectTimeout=10 "$SERVEUR" true \
  || { echo "SSH impossible vers $SERVEUR." >&2; exit 1; }
echo "   ok — $SERVEUR joignable"

if [ "$FAIRE_CODE" = 1 ]; then
  echo
  echo "== Code du moteur"
  rsync -a --delete "${ESSAI[@]}" --human-readable --info=stats1 \
    "${JETABLES[@]}" "${DONNEES[@]}" --exclude 'assets/pics/' \
    "$MOTEUR_LOCAL/" "$SERVEUR:$RACINE_DIST/Fusion/marvel-lcg-src/"

  echo
  echo "== Orchestrateur et site"
  rsync -a --delete "${ESSAI[@]}" --human-readable --info=stats1 \
    "${JETABLES[@]}" "${DONNEES[@]}" \
    "$PROJET/site/" "$SERVEUR:$RACINE_DIST/site/"
fi

if [ "$FAIRE_IMAGES" = 1 ]; then
  echo
  if [ ! -d "$PICS_LOCAL" ]; then
    echo "== Images : $PICS_LOCAL absent, étape sautée"
  elif [ "$REDIM" = 1 ]; then
    command -v magick >/dev/null || command -v convert >/dev/null \
      || { echo "ImageMagick manquant (REDIM=1 en a besoin)." >&2; exit 1; }
    CONVERT="$(command -v magick || command -v convert)"
    echo "== Images : préparation des versions ${LARGEUR}px"
    mkdir -p "$CACHE_REDIM"
    n=0
    while IFS= read -r -d '' src; do
      rel="${src#"$PICS_LOCAL"/}"
      dst="$CACHE_REDIM/$rel"
      # On ne reconvertit que ce qui a changé depuis la dernière fois.
      [ -f "$dst" ] && [ "$dst" -nt "$src" ] && continue
      mkdir -p "$(dirname "$dst")"
      "$CONVERT" "$src" -resize "${LARGEUR}x>" -strip -quality 88 "$dst"
      n=$((n + 1))
      [ $((n % 100)) -eq 0 ] && echo "   $n images converties…"
    done < <(find "$PICS_LOCAL" -type f \
             \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) -print0)
    echo "   $n images (re)converties, total $(du -sh "$CACHE_REDIM" | cut -f1)"
    SOURCE_IMAGES="$CACHE_REDIM"
  else
    echo "== Images : originaux (le premier envoi est long, les suivants non)"
    SOURCE_IMAGES="$PICS_LOCAL"
  fi

  if [ -n "${SOURCE_IMAGES:-}" ]; then
    # Pas de -z : ces fichiers sont déjà compressés.
    rsync -a --delete "${ESSAI[@]}" --human-readable --info=progress2,stats1 \
      --partial \
      "$SOURCE_IMAGES/" "$SERVEUR:$RACINE_DIST/Fusion/marvel-lcg-src/assets/pics/"
  fi
fi

if [ ${#ESSAI[@]} -gt 0 ]; then
  echo; echo "== Essai terminé, rien n'a été transféré ni redémarré."; exit 0
fi

echo
echo "== Environnement Python 3.10 et redémarrage"
ssh "$SERVEUR" RACINE="$RACINE_DIST" 'bash -s' <<'DISTANT'
set -euo pipefail
[ -x "$RACINE/venv310/bin/python" ] || python3.10 -m venv "$RACINE/venv310"
"$RACINE/venv310/bin/python" --version
for req in "$RACINE/Fusion/marvel-lcg-src/requirements.txt" "$RACINE/site/requirements.txt"; do
  [ -f "$req" ] && "$RACINE/venv310/bin/pip" install -q --upgrade -r "$req"
done
sudo systemctl restart narwhal
sleep 2
systemctl is-active narwhal
DISTANT

echo
echo "== Sauvegarde des comptes rapatriée"
mkdir -p "$PROJET/sauvegardes-serveur"
ssh "$SERVEUR" 'sudo -n /usr/local/bin/narwhal-sauvegarde >/dev/null 2>&1 || true'
rsync -a "$SERVEUR:/var/backups/narwhal/comptes-dernier.tar.gz" \
      "$PROJET/sauvegardes-serveur/comptes-$(date +%Y-%m-%d).tar.gz" 2>/dev/null \
  && echo "   $PROJET/sauvegardes-serveur/comptes-$(date +%Y-%m-%d).tar.gz" \
  || echo "   (pas encore de sauvegarde sur le serveur)"

echo
echo "== Vérification"
code="$(curl -s -o /dev/null -w '%{http_code}' "https://$DOMAINE/" || echo 000)"
echo "   https://$DOMAINE/ → HTTP $code"
[ "$code" = "200" ] || echo "   ⚠ regardez : ssh $SERVEUR 'journalctl -u narwhal -n 50'"
echo
echo "Terminé."
