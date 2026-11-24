#!/usr/bin/env bash
# Equivalent manuel de `deployer.ps1 -Code`, pour une machine Linux native (pas de WSL,
# pas de ssh.exe). Reproduit EXACTEMENT les memes etapes et exclusions que deployer.ps1,
# dans le meme ordre : controles, code (tar+raze+extraction), documents PDF, scripts et
# configuration serveur, environnement Python + redemarrage, rapatriement comptes et
# palettes, verification.
#
# N'ENVOIE PAS LES IMAGES (equivalent de -Code, pas de -Images) : assets/pics est exclu
# de l'archive de code, comme dans le .ps1.
#
# A LANCER A LA MAIN, APRES RELECTURE : bash deploiement/deployer-code-linux-manuel.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PROJET="$(pwd)"
ICI="$PROJET/deploiement"
CLE="$ICI/cle_narwhal"
IP=178.105.177.39
DOMAINE=narwhalchampions.com
DIST=/opt/narwhal

chmod 600 "$CLE"

echo "== Controles"
for o in ssh scp tar; do command -v "$o" >/dev/null || { echo "$o introuvable"; exit 1; }; done
[ -f "$CLE" ] || { echo "Cle SSH introuvable : $CLE"; exit 1; }
[ -f "$PROJET/site/orchestrateur.py" ] || { echo "orchestrateur.py introuvable dans $PROJET/site"; exit 1; }
ssh -i "$CLE" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 "root@$IP" "true"
echo "   ok - serveur joignable"

echo "== Code du moteur et orchestrateur"
TGZ=$(mktemp /tmp/narwhal-code.XXXXXX.tgz)
trap 'rm -f "$TGZ"' EXIT

# ⚠ tar GNU (Linux) ANCRE un motif contenant un "/" au DEBUT du chemin archive, contrairement a
# tar.exe (bsdtar/libarchive, Windows) qui le fait matcher n'importe ou dans le chemin. Un motif
# comme "assets/pics-hd" ne matcherait donc PAS "Fusion/marvel-lcg-src/assets/pics-hd" sous GNU tar :
# constate le 04/11/2026, archive de 3720 Mo au lieu de ~62 (scans HD, vignettes, PDF tous inclus).
# Ici, chaque motif a "/" est prefixe de "Fusion/marvel-lcg-src/" (ou laisse sans "/" pour matcher
# n'importe quel composant du chemin, comme GNU tar le fait nativement).
tar -czf "$TGZ" -C "$PROJET" \
  --exclude=.git --exclude=node_modules --exclude=__pycache__ \
  --exclude='.game' --exclude='.game-src*' --exclude='.game-essai*' \
  --exclude='*.pyc' --exclude=.venv --exclude=venv \
  --exclude='Fusion/marvel-lcg-src/assets/pics' --exclude='Fusion/marvel-lcg-src/assets/pics-fr' \
  --exclude='Fusion/marvel-lcg-src/assets/pics-proxy' \
  --exclude='Fusion/marvel-lcg-src/assets/vignettes' \
  --exclude='Fusion/marvel-lcg-src/assets/pics-hd' \
  --exclude='Fusion/marvel-lcg-src/assets/docs' \
  --exclude='Fusion/marvel-lcg-src/assets/export-cartes' \
  --exclude='*-serveur-*' \
  --exclude='*/serveur-*' \
  --exclude='games_history.json' --exclude='statistics.json' \
  --exclude='achievements.json' --exclude='legacy.json' \
  --exclude='sauvegardes' --exclude='saves' \
  --exclude='Fusion/marvel-lcg-src/sauvegardes-serveur' \
  --exclude='Fusion/marvel-lcg-src/campagnes' \
  --exclude='.site' \
  --exclude='replays' --exclude='logs' \
  --exclude='comptes.json' --exclude='*.db' --exclude='*.sqlite3' \
  --exclude='Fusion/marvel-lcg-src/data/palettes-heros-corrections.json' \
  "Fusion/marvel-lcg-src" "site"

mo=$(du -m "$TGZ" | cut -f1)
echo "   archive : ${mo} Mo"

scp -i "$CLE" "$TGZ" "root@$IP:/tmp/narwhal-code.tgz"

# Razage puis extraction avec -m (date d'extraction, comme le .ps1 : evite un .py
# plus recent que son .pyc compile avant lui).
ssh -i "$CLE" "root@$IP" "
set -e
rm -rf $DIST/Fusion/marvel-lcg-src/src
rm -rf $DIST/Fusion/marvel-lcg-src/public
if [ -d $DIST/site ]; then
  find $DIST/site -mindepth 1 -maxdepth 1 \
    ! -name 'comptes.json' ! -name '*.db' ! -name '*.sqlite3' \
    ! -name '*.db-*' ! -name '*.sqlite3-*' \
    ! -name 'rapports' -exec rm -rf {} + || true
fi
mkdir -p $DIST
tar -xzmf /tmp/narwhal-code.tgz -C $DIST
rm -f /tmp/narwhal-code.tgz
chown -R narwhal:narwhal $DIST
"
rm -f "$TGZ"
trap - EXIT
echo "   code deploye"

echo "== Documents PDF"
DOCS="$PROJET/Fusion/marvel-lcg-src/assets/docs"
DOCS_DIST="$DIST/Fusion/marvel-lcg-src/assets/docs"
if [ -d "$DOCS" ]; then
  declare -A DEJA_LA
  while IFS='|' read -r nom taille; do
    [ -n "$nom" ] && DEJA_LA["$nom"]="$taille"
  done < <(ssh -i "$CLE" "root@$IP" "cd $DOCS_DIST 2>/dev/null && find . -type f -name '*.pdf' -printf '%P|%s\n' || true")
  echo "   deja sur le serveur : ${#DEJA_LA[@]} documents"

  MANQUANTS=()
  declare -A LOCAL_NAMES
  while IFS= read -r -d '' f; do
    nom="$(basename "$f")"
    LOCAL_NAMES["$nom"]=1
    taille=$(stat -c%s "$f")
    if [ "${DEJA_LA[$nom]:-}" != "$taille" ]; then
      MANQUANTS+=("$nom")
    fi
  done < <(find "$DOCS" -maxdepth 1 -type f -name '*.pdf' -print0)

  A_EFFACER=()
  for nom in "${!DEJA_LA[@]}"; do
    [ -z "${LOCAL_NAMES[$nom]:-}" ] && A_EFFACER+=("$nom")
  done
  if [ "${#A_EFFACER[@]}" -gt 0 ]; then
    echo "   a effacer : ${#A_EFFACER[@]} document(s) disparu(s) en local"
    for nom in "${A_EFFACER[@]}"; do
      echo "     - $nom"
      ssh -i "$CLE" "root@$IP" "rm -f '$DOCS_DIST/${nom//\'/\'\'\'}'"
    done
  fi

  if [ "${#MANQUANTS[@]}" -eq 0 ]; then
    echo "   rien a envoyer, tout est a jour"
  else
    echo "   a envoyer : ${#MANQUANTS[@]} documents"
    ssh -i "$CLE" "root@$IP" "mkdir -p $DOCS_DIST"
    TGZD=$(mktemp /tmp/narwhal-docs.XXXXXX.tgz)
    tar -czf "$TGZD" -C "$DOCS" "${MANQUANTS[@]}"
    scp -i "$CLE" "$TGZD" "root@$IP:/tmp/narwhal-docs.tgz"
    ssh -i "$CLE" "root@$IP" "tar -xzf /tmp/narwhal-docs.tgz -C $DOCS_DIST && rm -f /tmp/narwhal-docs.tgz && chown -R narwhal:narwhal $DOCS_DIST"
    rm -f "$TGZD"
    echo "   documents deployes"
  fi
fi

echo "== Scripts et configuration du serveur"
CONFS=(synchroniser-conf.sh sauvegarde.sh purge.sh narwhal.service narwhal-sauvegarde.service narwhal-purge.service narwhal-sauvegarde.timer narwhal-purge.timer Caddyfile)
for c in "${CONFS[@]}"; do
  [ -f "$ICI/$c" ] || { echo "Fichier de configuration absent : $c"; exit 1; }
done
TGZC=$(mktemp /tmp/narwhal-conf.XXXXXX.tgz)
tar -czf "$TGZC" -C "$ICI" "${CONFS[@]}"
scp -i "$CLE" "$TGZC" "root@$IP:/tmp/narwhal-conf.tgz"
rm -f "$TGZC"
ssh -i "$CLE" "root@$IP" "rm -rf /tmp/narwhal-conf && mkdir -p /tmp/narwhal-conf && tar -xzf /tmp/narwhal-conf.tgz -C /tmp/narwhal-conf && rm -f /tmp/narwhal-conf.tgz && bash /tmp/narwhal-conf/synchroniser-conf.sh $DIST narwhal $DOMAINE && rm -rf /tmp/narwhal-conf"

echo "== Environnement Python 3.10 et redemarrage"
ssh -i "$CLE" "root@$IP" "
set -e
[ -x $DIST/venv310/bin/python ] || python3.10 -m venv $DIST/venv310
$DIST/venv310/bin/python --version
for req in $DIST/Fusion/marvel-lcg-src/requirements.txt $DIST/site/requirements.txt; do
  [ -f \"\$req\" ] && $DIST/venv310/bin/pip install -q --upgrade -r \"\$req\" || true
done
$DIST/venv310/bin/python $DIST/Fusion/marvel-lcg-src/tools/generer_vignettes.py || echo '  vignettes : generation en erreur, le plateau sert les scans complets'
$DIST/venv310/bin/python $DIST/Fusion/marvel-lcg-src/tools/telecharger_scans_hd.py || echo '  scans HD : telechargement en erreur, la scene sert les scans habituels'
chown -R narwhal:narwhal $DIST
systemctl restart narwhal
sleep 3
systemctl is-active narwhal
"

echo "== Sauvegarde des comptes rapatriee"
DOSSIER_SAUV="$PROJET/sauvegardes-serveur"
mkdir -p "$DOSSIER_SAUV"
ssh -i "$CLE" "root@$IP" "sudo -u narwhal RACINE=$DIST /usr/local/bin/narwhal-sauvegarde >/dev/null 2>&1 || true"
DEST="$DOSSIER_SAUV/comptes-$(date +%F).tar.gz"
scp -i "$CLE" "root@$IP:/var/backups/narwhal/comptes-dernier.tar.gz" "$DEST" 2>/dev/null || true
if [ -f "$DEST" ]; then echo "   $DEST"; else echo "   (pas encore de sauvegarde sur le serveur)"; fi

echo "== Palettes corrigees rapatriees"
PALETTES="$PROJET/Fusion/marvel-lcg-src/data/palettes-heros-corrections.json"
scp -i "$CLE" "root@$IP:$DIST/Fusion/marvel-lcg-src/data/palettes-heros-corrections.json" "$PALETTES" 2>/dev/null || true
if [ -f "$PALETTES" ]; then echo "   data/palettes-heros-corrections.json"; else echo "   (aucune palette corrigee sur le serveur)"; fi

echo "== Verification"
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "https://$DOMAINE/" || echo "ECHEC")
echo "   https://$DOMAINE/ -> HTTP $code"

echo ""
echo "Termine."
