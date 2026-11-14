#!/usr/bin/env bash
# Tests de logique de deploiement/deployer-linux.sh. AUCUNE connexion reelle :
# un depot temporaire, et de fausses commandes ssh/scp/curl/python placees en
# tete du PATH (elles journalisent leurs appels). Lancer :
#   bash deploiement/tests/test-deployer-linux.sh
set -uo pipefail
SCRIPT_REEL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/deployer-linux.sh"
OUTILS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../outils" && pwd)"
BASE="$(mktemp -d)"; trap 'rm -rf "$BASE"' EXIT
ECHECS=0; REUSSIS=0
ok()  { REUSSIS=$((REUSSIS+1)); echo "  ok   : $1"; }
ko()  { ECHECS=$((ECHECS+1)); echo "  ECHEC: $1"; }
verifie() {
  if eval "$2"; then ok "$1"; else ko "$1"; if [ -n "${DEBUG:-}" ]; then printf '%s\n' "${SORTIE:-}" | tail -15 | sed 's/^/       > /'; fi; fi
}

# --- fausses commandes --------------------------------------------------------
BIN="$BASE/bin"; mkdir -p "$BIN"
APPELS="$BASE/appels.log"
cat > "$BIN/ssh" <<'FAKE'
#!/usr/bin/env bash
# Fausse commande ssh : journalise les arguments et le script recu, repond selon la demande.
echo "SSH $*" >> "$APPELS"
if [ "${*: -1}" = "bash -s" ]; then cat >> "$APPELS"; echo "--fin-script" >> "$APPELS"; exit 0; fi
case "$*" in
  *"palettes-heros-corrections.json"*) printf '%s' "${FAUX_PALETTES_SERVEUR:-}" ;;
  *"ss -Htn"*) echo "${FAUX_JOUEURS:-0}" ;;
  *"md5sum /opt/narwhal-play/"*) echo "$FAUX_MD5_PLAY" ;;
  *"md5sum"*) echo "${FAUX_MD5_SITE}"; echo active ;;
  *"is-active"*) echo active ;;
  *"ls -1t"*) echo /root/rollback-code-ancien.tgz ;;
  *) echo 3 ;;
esac
FAKE
cat > "$BIN/scp" <<'FAKE'
#!/usr/bin/env bash
echo "SCP $*" >> "$APPELS"
FAKE
cat > "$BIN/rsync" <<'FAKE'
#!/usr/bin/env bash
echo "RSYNC $*" >> "$APPELS"
FAKE
cat > "$BIN/curl" <<'FAKE'
#!/usr/bin/env bash
echo "CURL $*" >> "$APPELS"
printf '%s' "${FAUX_HTTP:-200}"
FAKE
cat > "$BIN/fauxpython" <<'FAKE'
#!/usr/bin/env bash
echo "PUBLIER cle=${NARWHAL_CLE:-} py310=${NARWHAL_PY310:-} args=$*" >> "$APPELS"
mkdir -p navigateur/dist/app/assets; echo "play-board" > navigateur/dist/app/assets/board-play.js
if [ "${FAUX_PUBLIER_ECHEC:-0}" = 1 ]; then exit 1; fi
echo "20 identiques, 0 differentes"
FAKE
chmod +x "$BIN"/*
export APPELS FAUX_MD5_SITE FAUX_MD5_PLAY
FAUX_MD5_SITE="$(echo "board" | md5sum | cut -c1-32)"
FAUX_MD5_PLAY="$(echo "play-board" | md5sum | cut -c1-32)"

# --- depot temporaire ----------------------------------------------------------
nouveau_depot() {
  D="$BASE/depot-$1"; rm -rf "$D"; mkdir -p "$D"; cd "$D" || exit 1
  git init -q . && git config user.email t@t && git config user.name t
  mkdir -p deploiement ui-app ui-check navigateur site Fusion/marvel-lcg-src/public/js/prepare Fusion/marvel-lcg-src/src Fusion/marvel-lcg-src/data
  cp "$SCRIPT_REEL" deploiement/
  mkdir -p outils; cp "$OUTILS/fusionner-palettes.py" outils/
  for f in synchroniser-conf.sh sauvegarde.sh purge.sh narwhal.service narwhal-sauvegarde.service narwhal-purge.service narwhal-sauvegarde.timer narwhal-purge.timer Caddyfile; do echo "# $f" > "deploiement/$f"; done
  echo "date: \"$(date +%F)\"" > Fusion/marvel-lcg-src/public/js/prepare/nouveautes.js
  echo "print(1)" > site/app.py; echo "x" > Fusion/marvel-lcg-src/src/m.py
  printf '#!/usr/bin/env bash\nmkdir -p Fusion/marvel-lcg-src/public/app/assets\necho board > Fusion/marvel-lcg-src/public/app/assets/board-abc.js\n' > ui-app/deployer.sh
  echo "cle-factice" > deploiement/cle_narwhal
  printf 'deploiement/cle_narwhal\ndeploiement/dernier-deploiement.log\n.claude/\nnavigateur/.cache\nnavigateur/dist\nui-app/node_modules\n' > .gitignore
  git add -A && git commit -q -m "feat(test): depart"
  : > "$APPELS"
}
lancer() {   # lancer <entree stdin> options... ; sortie dans $SORTIE, code dans $CODE
  local entree="$1"; shift
  SORTIE="$(printf '%b' "$entree" | PATH="$BIN:$PATH" DEPLOYER_HOTE=root@test.invalid DEPLOYER_TMP="$BASE/tmp" \
    DEPLOYER_PLAY_PYTHON="$BIN/fauxpython" DEPLOYER_ATTENTE_SECONDES=0 bash deploiement/deployer-linux.sh "$@" 2>&1)"
  CODE=$?
}
mkdir -p "$BASE/tmp"

echo "1. simulation par defaut : aucun appel ssh/scp/curl"
nouveau_depot sim
lancer ""
verifie "code 0" '[ "$CODE" = 0 ]'
verifie "aucun appel reseau" '[ ! -s "$APPELS" ]'
verifie "annonce montree (texte vouvoye)" 'grep -q "Sauvegardez la votre" <<<"$SORTIE"'
verifie "archives creees et verifiees" 'grep -q "contenu verifie" <<<"$SORTIE"'
verifie "journal ecrit" '[ -s deploiement/dernier-deploiement.log ]'
verifie "la cle n'est pas dans l'archive du code" '! tar -tzf "$BASE"/tmp/narwhal-code-*.tgz | grep -q cle_narwhal'
verifie "retour arriere annonce" 'grep -q "retour-arriere /root/rollback-code-" <<<"$SORTIE"'

echo "2. arbre sale refuse"
nouveau_depot sale; echo "z" >> site/app.py
lancer ""
verifie "refus" '[ "$CODE" != 0 ] && grep -q "pas propre" <<<"$SORTIE"'
nouveau_depot nonsuivi; echo a > intrus.txt
lancer ""; verifie "fichier non suivi tolere" '[ "$CODE" = 0 ]'

echo "3. mauvais commit refuse"
nouveau_depot commit
lancer "" --commit "HEAD"; verifie "HEAD accepte" '[ "$CODE" = 0 ]'
git commit -q --allow-empty -m "autre"; PREMIER="$(git rev-parse HEAD~1)"
lancer "" --commit "$PREMIER"; verifie "ancien commit refuse" '[ "$CODE" != 0 ] && grep -q "pas $PREMIER" <<<"$SORTIE"'

echo "4. nouveautes en retard refusees"
nouveau_depot nouv
sed -i 's/date: \"[0-9-]*\"/date: \"2000-01-01\"/' Fusion/marvel-lcg-src/public/js/prepare/nouveautes.js; git commit -q -am "docs"
echo y >> site/app.py; git commit -q -am "feat(site): chose neuve"
lancer ""; verifie "refus" '[ "$CODE" != 0 ] && grep -q "journal des nouveautes" <<<"$SORTIE"'
export NOUVEAUTES_A_JOUR=1; lancer ""; unset NOUVEAUTES_A_JOUR
verifie "contournement NOUVEAUTES_A_JOUR=1" '[ "$CODE" = 0 ]'

echo "5. mode reel sans la bonne phrase : rien d'envoye"
nouveau_depot reel1; export FAUX_JOUEURS=0
lancer "pas la phrase\n" --oui
verifie "refus" '[ "$CODE" != 0 ] && grep -q "confirmation differente" <<<"$SORTIE"'
verifie "pas de scp, pas d'annonce" '! grep -q "^SCP" "$APPELS" && ! grep -q "INSERT INTO annonces" "$APPELS"'
verifie "seule lecture : ss" '[ "$(grep -c "^SSH" "$APPELS")" = 1 ] && grep -q "ss -Htn" "$APPELS"'

echo "6. joueurs connectes : demande, refus sans « oui »"
nouveau_depot reel2; export FAUX_JOUEURS=4
lancer "non\n" --oui
verifie "nombre affiche" 'grep -q "ports 80/443 : 4" <<<"$SORTIE"'
verifie "abandon" '[ "$CODE" != 0 ] && grep -q "abandon" <<<"$SORTIE"'
verifie "rien envoye" '! grep -q "^SCP" "$APPELS"'

echo "7. deploiement reel complet (faux serveur)"
nouveau_depot reel3; export FAUX_JOUEURS=2; COURT="$(git rev-parse --short HEAD)"
lancer "oui\nJe deploie $COURT\n" --oui --annonce 5
verifie "code 0" '[ "$CODE" = 0 ]' || echo "$SORTIE" | tail -20
verifie "annonce de 5 minutes" 'grep -q "dans 5 minutes" "$APPELS"'
verifie "ordre : annonce < scp < rollback < extraction < restart < retrait" \
  'a=$(grep -n "INSERT INTO annonces" "$APPELS" | head -1 | cut -d: -f1); s=$(grep -n "^SCP" "$APPELS" | head -1 | cut -d: -f1); r=$(grep -n "tar -czf /root/rollback-code" "$APPELS" | head -1 | cut -d: -f1); e=$(grep -n "tar -xzmf" "$APPELS" | head -1 | cut -d: -f1); x=$(grep -n "systemctl restart narwhal" "$APPELS" | head -1 | cut -d: -f1); z=$(grep -n "annonce retiree" "$APPELS" | head -1 | cut -d: -f1); [ "$a" -lt "$s" ] && [ "$s" -lt "$r" ] && [ "$r" -lt "$e" ] && [ "$e" -lt "$x" ] && [ "$x" -lt "$z" ]'
verifie "trois scp : code, conf et couleurs fusionnees" '[ "$(grep -c "^SCP" "$APPELS")" = 3 ] && grep -q "test.invalid:/tmp/narwhal-code.tgz" "$APPELS" && grep -q "test.invalid:/tmp/narwhal-palettes-corrections.json" "$APPELS"'
verifie "comptes preserves a l'extraction" 'grep -q "! -name comptes.json" "$APPELS" && grep -q "! -name rapports" "$APPELS"'
verifie "jamais d'ecriture dans narwhal.service/Caddyfile cote serveur" '! grep -E "(install|cp|mv|tee|sed -i).*(/etc/systemd/system/narwhal.service|/etc/caddy/Caddyfile)" "$APPELS"'
verifie "publier : simulation puis --oui --sans-construire" 'grep -q "^PUBLIER .*publier.py$" "$APPELS" && grep -q "publier.py --oui --sans-construire" "$APPELS"'
verifie "variables NARWHAL_CLE / PY310 passees" 'grep -q "py310=.*python3.10" "$APPELS" && grep -q "cle=.*/cle " "$APPELS"'
verifie "sons copies" 'grep -q "originaux/sounds" "$APPELS"'
verifie "HTTP 200 site et play" '[ "$(grep -c "^CURL" "$APPELS")" = 2 ] && grep -q "HTTP site / play  : 200 / 200" <<<"$SORTIE"'
verifie "resume : joueurs vus et commande de retour" 'grep -q "joueurs vus       : 2" <<<"$SORTIE" && grep -q "pour restaurer" <<<"$SORTIE"'

echo "7b. couleurs corrigees a la main : poste <-> serveur, a trois"
nouveau_depot pal; export FAUX_JOUEURS=2
D_DATA=Fusion/marvel-lcg-src/data
printf '{"_lisez_moi":"x","palettes":{"a":[[1,1,1]],"b":[[1,1,1]]},"version":1}' > "$D_DATA/palettes-heros-corrections.synchro.json"
printf '{"_lisez_moi":"x","palettes":{"a":[[9,9,9]],"b":[[1,1,1]]},"version":1}' > "$D_DATA/palettes-heros-corrections.json"
git add -A && git commit -q -m "couleurs du poste"; COURT="$(git rev-parse --short HEAD)"
# le serveur a corrige b en ligne ; a est reste comme a la derniere synchro
export FAUX_PALETTES_SERVEUR='{"_lisez_moi":"x","palettes":{"a":[[1,1,1]],"b":[[7,7,7]]},"version":1}'
lancer "oui\nJe deploie $COURT\n" --oui --annonce 5; unset FAUX_PALETTES_SERVEUR
verifie "code 0" '[ "$CODE" = 0 ]'
verifie "la correction du poste (a) part en ligne ET celle du serveur (b) est gardee" \
  'python3 -c "import json,sys; p=json.load(open(sys.argv[1]))[\"palettes\"]; sys.exit(0 if p[\"a\"]==[[9,9,9]] and p[\"b\"]==[[7,7,7]] else 1)" "$D_DATA/palettes-heros-corrections.json"'
verifie "le fichier du poste ET la base sont rendus identiques apres le deploiement" 'cmp -s "$D_DATA/palettes-heros-corrections.json" "$D_DATA/palettes-heros-corrections.synchro.json"'
verifie "pose cote serveur avant le redemarrage" 'p=$(grep -n "cp /tmp/narwhal-palettes-corrections.json" "$APPELS" | head -1 | cut -d: -f1); x=$(grep -n "systemctl restart narwhal" "$APPELS" | head -1 | cut -d: -f1); [ -n "$p" ] && [ "$p" -lt "$x" ]'
verifie "le fichier de corrections reste exclu de l'archive du code" '! tar -tzf "$BASE"/tmp/narwhal-code-*.tgz | grep -q "palettes-heros-corrections.json"'

echo "7c. simulation : rien lu, rien envoye pour les couleurs"
nouveau_depot palsim
lancer ""
verifie "etape annoncee, aucun appel reseau" 'grep -q "Couleurs corrigees a la main" <<<"$SORTIE" && [ ! -s "$APPELS" ]'

echo "8. echec de Play avant extraction : annonce retiree, code serveur intact"
nouveau_depot reel4; export FAUX_JOUEURS=0; COURT="$(git rev-parse --short HEAD)"
export FAUX_PUBLIER_ECHEC=1; lancer "Je deploie $COURT\n" --oui --annonce 1; unset FAUX_PUBLIER_ECHEC
verifie "echec" '[ "$CODE" != 0 ]'
verifie "pas d'extraction" '! grep -q "tar -xzmf" "$APPELS"'
verifie "annonce retiree" 'grep -q "DELETE FROM annonces" "$APPELS"'

echo "9. plateau different sur le serveur : arret"
nouveau_depot reel5; COURT="$(git rev-parse --short HEAD)"; SAUVE="$FAUX_MD5_SITE"; export FAUX_MD5_SITE=00000000000000000000000000000000
lancer "Je deploie $COURT\n" --oui
export FAUX_MD5_SITE="$SAUVE"
verifie "arret sur md5" '[ "$CODE" != 0 ] && grep -q "different de celui construit" <<<"$SORTIE"'
verifie "retour arriere indique" 'grep -q "retour-arriere" <<<"$SORTIE"'

echo "10. HTTP != 200 : arret"
nouveau_depot reel6; COURT="$(git rev-parse --short HEAD)"
export FAUX_HTTP=502; lancer "Je deploie $COURT\n" --oui; unset FAUX_HTTP
verifie "arret" '[ "$CODE" != 0 ] && grep -q "502" <<<"$SORTIE"'

echo "11. --site-seul et --play-seul"
nouveau_depot seul1; COURT="$(git rev-parse --short HEAD)"
lancer "Je deploie $COURT\n" --oui --site-seul
verifie "site-seul : pas de publier, pas de sons" '[ "$CODE" = 0 ] && ! grep -q "^PUBLIER" "$APPELS" && ! grep -q "originaux/sounds" "$APPELS"'
nouveau_depot seul2; COURT="$(git rev-parse --short HEAD)"
lancer "Je deploie $COURT\n" --oui --play-seul
verifie "play-seul : ni annonce, ni scp, ni restart, ni ss" '[ "$CODE" = 0 ] && ! grep -q "INSERT INTO annonces" "$APPELS" && ! grep -q "^SCP" "$APPELS" && ! grep -q "systemctl restart" "$APPELS" && ! grep -q "ss -Htn" "$APPELS"'
verifie "play-seul : publication faite" 'grep -q "publier.py --oui --sans-construire" "$APPELS"'
lancer "" --site-seul --play-seul; verifie "options exclusives refusees" '[ "$CODE" != 0 ]'

echo "12. --retour-arriere"
nouveau_depot rb
lancer "" --retour-arriere /root/rollback-code-X.tgz
verifie "simulation : aucun appel" '[ "$CODE" = 0 ] && [ ! -s "$APPELS" ]'
lancer "" --retour-arriere /etc/passwd; verifie "chemin hors modele refuse" '[ "$CODE" != 0 ]'
lancer "mauvaise\n" --oui --retour-arriere /root/rollback-code-X.tgz
verifie "reel : mauvaise phrase, rien restaure" '[ "$CODE" != 0 ] && ! grep -q "tar -xzmf" "$APPELS"'
lancer "Je restaure /root/rollback-code-X.tgz\n" --oui --retour-arriere /root/rollback-code-X.tgz
verifie "reel : restauration + redemarrage" '[ "$CODE" = 0 ] && grep -q "tar -xzmf /root/rollback-code-X.tgz" "$APPELS" && grep -q "systemctl restart narwhal" "$APPELS"'

echo "13. option inconnue / annonce invalide"
lancer "" --bidon; verifie "option inconnue" '[ "$CODE" != 0 ]'
lancer "" --annonce abc; verifie "annonce invalide" '[ "$CODE" != 0 ]'

echo; echo "Reussis : $REUSSIS, echecs : $ECHECS"
[ "$ECHECS" = 0 ]
