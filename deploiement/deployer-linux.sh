#!/usr/bin/env bash
# =============================================================================
#  Deploiement sous Linux de narwhalchampions.com (site) et play. (navigateur)
#
#      bash deploiement/deployer-linux.sh [options]
#
#  SIMULATION PAR DEFAUT : aucune connexion au serveur, rien n'est envoye.
#  Le mode reel demande `--oui` ET une phrase de confirmation tapee.
#
#  Options
#    --simulation          (defaut) prepare tout en local, montre ce qui serait fait
#    --oui                 mode reel (demande en plus la phrase de confirmation)
#    --commit <sha>        commit a deployer ; refus si la tete du depot est un autre commit
#    --annonce N           minutes d'annonce aux joueurs avant le redemarrage (15 par defaut)
#    --site-seul           site normal uniquement (pas de publication de play.)
#    --play-seul           play. uniquement (pas d'annonce, pas de redemarrage)
#    --retour-arriere <f>  restaure l'archive <f> du serveur (/root/rollback-code-<id>.tgz)
#    --aide
#
#  Remplace deployer.ps1 / deployer-tout.sh / DEPLOYER.bat (PowerShell, wslpath).
#  Journal horodate : deploiement/dernier-deploiement.log
#  Jamais d'ecriture dans narwhal.service ni dans le Caddyfile du serveur :
#  synchroniser-conf.sh les surveille sans les toucher.
# =============================================================================
set -euo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RACINE"
JOURNAL="$RACINE/deploiement/dernier-deploiement.log"

HOTE="${DEPLOYER_HOTE:-root@178.105.177.39}"
DOMAINE=narwhalchampions.com
DIST=/opt/narwhal
CLE_SOURCE="${DEPLOYER_CLE:-$RACINE/deploiement/cle_narwhal}"
PLAY_PYTHON="${DEPLOYER_PLAY_PYTHON:-$RACINE/.venv-linux/bin/python}"
PLAY_PY310="${DEPLOYER_PY310:-$RACINE/.venv-linux/bin/python3.10}"
COMMANDE_BUILD="${DEPLOYER_BUILD:-bash ui-app/deployer.sh}"
TMP_ARCHIVES="${DEPLOYER_TMP:-/tmp}"
DOSSIER_COPIE="${DEPLOYER_COPIE:-.claude/worktrees/deploy-prod3}"
NOUVEAUTES="Fusion/marvel-lcg-src/public/js/prepare/nouveautes.js"

REEL=0; ANNONCE=15; COMMIT_DEMANDE=""; SITE=1; PLAY=1; RETOUR=""
PHASE="debut"        # debut -> annonce -> extraction -> fini
TMP_CLE=""; CLE=""; ROLLBACK=""; PID_PLAY_SIM=""

heure() { date '+%H:%M:%S'; }
dire()  { printf '[%s] %s\n' "$(heure)" "$*"; }
etape() { printf '\n[%s] == %s\n' "$(heure)" "$*"; }
arret() { printf '[%s] ARRET : %s\n' "$(heure)" "$*" >&2; exit 1; }

usage() { sed -n '2,/^# ====/p' "$0" | sed 's/^# \{0,1\}//' | grep -v '^====' || true; }

# --- acces au serveur : tout passe par ces fonctions --------------------------
ssh_h() { ssh -i "$CLE" -o ConnectTimeout=30 -o StrictHostKeyChecking=accept-new "$HOTE" "$@"; }

# distant_script "description" < script  (execute par `bash -s`)
distant_script() {
  local desc="$1" script; script="$(cat)"
  if [ "$REEL" -eq 0 ]; then
    dire "[simulation] serveur : $desc"
    printf '%s\n' "$script" | sed 's/^/        | /'
    return 0
  fi
  printf '%s\n' "$script" | ssh_h 'bash -s'
}
envoyer() {   # envoyer fichier destination-distante
  if [ "$REEL" -eq 0 ]; then dire "[simulation] scp $1 -> $2"; return 0; fi
  scp -q -i "$CLE" -o ConnectTimeout=30 -o StrictHostKeyChecking=accept-new "$1" "$HOTE:$2"
}

# --- filet de securite en cas d'erreur ----------------------------------------
nettoyer() {
  local code=$?
  if [ -n "$TMP_CLE" ]; then rm -rf "$TMP_CLE"; fi
  if [ "$code" -ne 0 ] && [ "$REEL" -eq 1 ]; then
    case "$PHASE" in
      annonce)
        dire "Echec avant tout changement du code serveur : retrait de l'annonce."
        ssh_h "$DIST/venv310/bin/python -c \"import sqlite3; c=sqlite3.connect('$DIST/site/narwhal.db'); c.execute('DELETE FROM annonces'); c.commit()\"" </dev/null \
          || dire "Retrait de l'annonce impossible : a faire a la main (DELETE FROM annonces)." ;;
      extraction)
        dire "ECHEC PENDANT OU APRES L'EXTRACTION : le serveur est peut-etre dans un etat intermediaire."
        dire "Annonce laissee en place. Retour arriere : bash deploiement/deployer-linux.sh --retour-arriere ${ROLLBACK:-/root/rollback-code-<id>.tgz} --oui" ;;
    esac
  fi
  if [ "$code" -ne 0 ]; then dire "Termine en ERREUR (code $code). Journal : $JOURNAL"; fi
  return 0
}

confirmer() {   # confirmer "phrase attendue"
  local attendu="$1" saisie
  printf 'Pour continuer, tapez exactement : %s\n> ' "$attendu"
  IFS= read -r saisie || arret "aucune confirmation lue (entree fermee)."
  [ "$saisie" = "$attendu" ] || arret "confirmation differente de « $attendu » : rien n'a ete envoye."
}

preparer_cle() {
  if [ ! -f "$CLE_SOURCE" ]; then
    if [ "$REEL" -eq 1 ]; then arret "cle SSH introuvable : $CLE_SOURCE"; fi
    dire "cle SSH absente ($CLE_SOURCE) : sans importance en simulation."
    CLE="$CLE_SOURCE"; return 0
  fi
  TMP_CLE="$(mktemp -d)"; CLE="$TMP_CLE/cle"
  cp "$CLE_SOURCE" "$CLE"; chmod 600 "$CLE"
  dire "cle copiee dans un dossier temporaire (droits 600, jamais commitee)."
}

# =============================================================================
precontroles() {
  etape "0. Pre-controles"
  git rev-parse --git-dir >/dev/null 2>&1 || arret "pas dans un depot git."
  local sale; sale="$(git status --short | grep -v '^??' || true)"
  if [ -n "$sale" ]; then
    printf '%s\n' "$sale" >&2
    arret "l'arbre de travail n'est pas propre (fichiers suivis modifies). Commitez ou annulez d'abord."
  fi
  COMMIT="$(git rev-parse HEAD)"; COURT="$(git rev-parse --short HEAD)"
  if [ -n "$COMMIT_DEMANDE" ]; then
    local voulu; voulu="$(git rev-parse --verify "$COMMIT_DEMANDE^{commit}" 2>/dev/null)" || arret "commit inconnu : $COMMIT_DEMANDE"
    [ "$voulu" = "$COMMIT" ] || arret "la tete du depot est $COURT, pas $COMMIT_DEMANDE : basculez sur le bon commit avant."
  fi
  dire "commit a deployer : $COMMIT ($(git log -1 --format=%s | cut -c1-70))"
  ID="$(date +%Y%m%d-%H%M)-$COURT"
  ROLLBACK="/root/rollback-code-$ID.tgz"

  # Le journal des nouveautes doit suivre le code (meme controle que deployer-tout.sh).
  local derniere dernier
  derniere="$(grep -oE 'date: "[0-9-]+"' "$NOUVEAUTES" | cut -d'"' -f2 | sort -r | head -1)"
  dernier="$(git log -E --grep='^(feat|fix)' --format='%ad %s' --date=short -- ui-app Fusion/marvel-lcg-src/src Fusion/marvel-lcg-src/public Fusion/marvel-lcg-src/data site \
    | grep -vE '^[0-9-]+ (feat|fix)\(admin\)' | head -1 | cut -d' ' -f1 || true)"
  if [[ "$dernier" > "$derniere" && "${NOUVEAUTES_A_JOUR:-}" != "1" ]]; then
    arret "le journal des nouveautes s'arrete au $derniere, le code a change le $dernier. Ajoutez les entrees (fr + en) dans $NOUVEAUTES, ou relancez avec NOUVEAUTES_A_JOUR=1."
  fi
  NOUVEAUTE_DU_JOUR="$derniere"
  dire "nouveautes a jour (derniere entree $derniere)"
}

compter_joueurs() {
  etape "0b. Joueurs connectes (lecture seule)"
  local n r
  n="$(ssh_h "ss -Htn state established '( sport = :443 or sport = :80 )' | wc -l" </dev/null | tr -dc '0-9')"
  [ -n "$n" ] || arret "nombre de joueurs illisible : rien n'est envoye."
  JOUEURS="$n"
  dire "connexions etablies sur les ports 80/443 : $JOUEURS (approximation : un joueur peut en ouvrir plusieurs)"
  if [ "$JOUEURS" -gt 0 ]; then
    printf 'Des joueurs sont connectes. Le redemarrage coupera leurs parties.\nContinuer quand meme (annonce de %s min incluse) ? Tapez « oui » : ' "$ANNONCE"
    IFS= read -r r || arret "aucune reponse lue."
    [ "$r" = "oui" ] || arret "abandon a la demande de l'utilisateur : rien n'a ete envoye."
  fi
}

poser_annonce() {
  etape "2. Annonce aux joueurs ($ANNONCE min)"
  local texte="Mise a jour du jeu dans $ANNONCE minutes : les parties en cours seront interrompues. Sauvegardez la votre avec le bouton Save du plateau."
  PHASE="annonce"
  distant_script "poser l'annonce" <<REMOTE
set -e
$DIST/venv310/bin/python - "$ANNONCE" '$texte' <<'PY'
import sqlite3, sys, time
n, texte = int(sys.argv[1]), sys.argv[2]
c = sqlite3.connect("$DIST/site/narwhal.db")
c.execute("DELETE FROM annonces")
c.execute("INSERT INTO annonces (texte, jusqu_a, pose_le) VALUES (?,?,?)",
          (texte, time.time() + n * 60, time.strftime("%Y-%m-%d %H:%M", time.gmtime())))
c.commit()
print("annonce posee")
PY
REMOTE
  DEBUT_ANNONCE=$(date +%s)
}

retirer_annonce() {
  etape "8. Retrait de l'annonce"
  distant_script "supprimer l'annonce" <<REMOTE
set -e
$DIST/venv310/bin/python -c "import sqlite3; c=sqlite3.connect('$DIST/site/narwhal.db'); c.execute('DELETE FROM annonces'); c.commit(); print('annonce retiree')"
REMOTE
}

lier() {   # lier source cible
  if [ ! -e "$1" ]; then dire "avertissement : $1 absent, lien non cree."; return 0; fi
  if [ -e "$2" ] && [ ! -L "$2" ]; then return 0; fi
  mkdir -p "$(dirname "$2")"; ln -sfn "$1" "$2"
}

copie_propre() {
  etape "3. Copie propre et construction"
  WT="$RACINE/$DOSSIER_COPIE"
  if [ -e "$WT/.git" ]; then
    git -C "$WT" checkout --detach --force "$COMMIT" >/dev/null 2>&1
    dire "copie existante basculee sur $COURT : $DOSSIER_COPIE"
  else
    git worktree add --detach "$WT" "$COMMIT" >/dev/null 2>&1
    dire "copie creee : $DOSSIER_COPIE"
  fi
  lier "$RACINE/ui-app/node_modules" "$WT/ui-app/node_modules"
  lier "$RACINE/ui-check/node_modules" "$WT/ui-check/node_modules"
  local d
  for d in pics pics-fr pics-hd pics-proxy docs cache vignettes; do
    lier "$RACINE/Fusion/marvel-lcg-src/assets/$d" "$WT/Fusion/marvel-lcg-src/assets/$d"
  done
  dire "construction : $COMMANDE_BUILD (dans la copie)"
  ( cd "$WT" && eval "$COMMANDE_BUILD" ) || arret "la construction (ou ses gardes) a echoue : rien n'est envoye."
  BOARD_LOCAL="$(ls "$WT"/Fusion/marvel-lcg-src/public/app/assets/board-*.js 2>/dev/null | head -1 || true)"
  [ -n "$BOARD_LOCAL" ] || arret "aucun board-*.js apres la construction."
  MD5_LOCAL="$(md5sum "$BOARD_LOCAL" | cut -c1-32)"
  dire "plateau construit : $(basename "$BOARD_LOCAL") ($MD5_LOCAL)"
}

palettes_corrections() {
  # Les couleurs corrigees a la main se font a DEUX endroits (editeur local et
  # editeur en ligne) et valent pour tout le monde. Ce fichier est exclu de
  # l'archive du code (plus bas), sinon l'archive ecraserait celui du serveur ;
  # il voyage donc par cette etape, qui FUSIONNE au lieu d'ecraser :
  # `outils/fusionner-palettes.py` (a trois : base = derniere synchro). Rien
  # n'est envoye ici, tout part avec le code (`remplacer_code`) : un arret avant
  # laisse le serveur intact.
  # 21/10/2026, demande de l'utilisateur : « si je le fais en local, je veux que
  # ca passe en ligne ». Avant : le fichier n'allait JAMAIS dans ce sens.
  etape "3b. Couleurs corrigees a la main (poste <-> serveur)"
  local data="$RACINE/Fusion/marvel-lcg-src/data"
  PALETTES_LOCAL="$data/palettes-heros-corrections.json"
  PALETTES_BASE="$data/palettes-heros-corrections.synchro.json"
  PALETTES_FUSION="$TMP_ARCHIVES/palettes-corrections-$ID.json"
  if [ "$REEL" -eq 0 ]; then
    dire "[simulation] lecture du fichier du serveur, fusion a trois avec le poste (le poste gagne un conflit), envoi avec le code."
    PALETTES_FUSION=""
    return 0
  fi
  local serveur="$TMP_ARCHIVES/palettes-serveur-$ID.json"
  ssh_h "cat $DIST/Fusion/marvel-lcg-src/data/palettes-heros-corrections.json 2>/dev/null || true" </dev/null > "$serveur"
  python3 "$RACINE/outils/fusionner-palettes.py" "$PALETTES_BASE" "$PALETTES_LOCAL" "$serveur" "$PALETTES_FUSION" \
    || arret "la fusion des couleurs a echoue : le serveur n'a pas ete touche."
  envoyer "$PALETTES_FUSION" /tmp/narwhal-palettes-corrections.json
}

archives() {
  etape "4. Archives"
  local code="$TMP_ARCHIVES/narwhal-code-$ID.tgz" conf="$TMP_ARCHIVES/narwhal-conf-$ID.tgz"
  tar -czf "$code" -C "$WT" --exclude=.git --exclude=node_modules --exclude=__pycache__ \
    --exclude=.game --exclude='.game-src*' --exclude='.game-essai*' --exclude='*.pyc' --exclude=.venv --exclude=venv \
    --exclude=assets/pics --exclude=assets/pics-fr --exclude=assets/pics-proxy --exclude=assets/vignettes \
    --exclude=assets/pics-hd --exclude=assets/docs --exclude=assets/cache \
    --exclude='*-serveur-*' --exclude='*/serveur-*' --exclude=games_history.json --exclude=statistics.json \
    --exclude=achievements.json --exclude=legacy.json --exclude=sauvegardes --exclude=saves \
    --exclude=Fusion/marvel-lcg-src/campagnes --exclude=.site --exclude=replays --exclude=logs \
    --exclude=comptes.json --exclude='*.db' --exclude='*.sqlite3' --exclude=data/palettes-heros-corrections.json \
    Fusion/marvel-lcg-src site
  tar -czf "$conf" -C "$WT/deploiement" synchroniser-conf.sh sauvegarde.sh purge.sh narwhal.service \
    narwhal-sauvegarde.service narwhal-purge.service narwhal-sauvegarde.timer narwhal-purge.timer Caddyfile
  dire "code : $code ($(du -h "$code" | cut -f1)) ; conf : $conf"
  # Verifications de contenu : le plateau construit et le journal du jour doivent y etre.
  # ⚠ NE JAMAIS FAIRE `tar -tzf ... | grep -q ...` (21/10/2026, deploiement reel) : sous
  # `set -o pipefail`, des que `grep -q` trouve sa ligne il ferme le pipe et sort, ce qui
  # envoie SIGPIPE a `tar` encore en train d'ecrire le reste d'une longue liste (des
  # milliers d'entrees ici) ; `pipefail` remonte alors le code d'erreur de `tar` (signal),
  # PAS celui de `grep`, et la verification echoue alors que le fichier est bel et bien
  # present. Capturer d'abord la liste dans une variable, puis grep DESSUS (plus de pipe
  # vers un `tar` qui ecrit encore) : la seule facon fiable sous `pipefail`.
  local liste_code liste_conf nouveautes_contenu
  liste_code="$(tar -tzf "$code")"
  liste_conf="$(tar -tzf "$conf")"
  nouveautes_contenu="$(tar -xzOf "$code" "Fusion/marvel-lcg-src/public/js/prepare/nouveautes.js")"
  grep -q "^Fusion/marvel-lcg-src/public/app/assets/$(basename "$BOARD_LOCAL")$" <<<"$liste_code" \
    || arret "le plateau $(basename "$BOARD_LOCAL") n'est pas dans l'archive du code."
  grep -q "date: \"$NOUVEAUTE_DU_JOUR\"" <<<"$nouveautes_contenu" \
    || arret "la page de nouveautes du $NOUVEAUTE_DU_JOUR n'est pas dans l'archive."
  grep -q '^site/' <<<"$liste_code" || arret "le dossier site/ manque dans l'archive."
  grep -q '^synchroniser-conf.sh$' <<<"$liste_conf" || arret "synchroniser-conf.sh manque dans l'archive de conf."
  dire "contenu verifie (plateau, nouveautes du $NOUVEAUTE_DU_JOUR, site/, conf)."
  envoyer "$code" /tmp/narwhal-code.tgz
  envoyer "$conf" /tmp/narwhal-conf.tgz
}

lancer_publier() {   # lancer_publier <arguments...> ; execute dans la copie propre
  ( cd "$WT"
    NARWHAL_CLE="$CLE" NARWHAL_PY310="$PLAY_PY310" "$PLAY_PYTHON" navigateur/publier.py "$@" )
}

preparer_play() {
  mkdir -p "$RACINE/navigateur/.cache" "$WT/navigateur"
  if [ ! -e "$WT/navigateur/.cache" ]; then ln -sfn "$RACINE/navigateur/.cache" "$WT/navigateur/.cache"; fi
}

play_simulation_en_parallele() {
  etape "5. Play : simulation (build + controle) pendant l'attente"
  preparer_play
  if [ "$REEL" -eq 0 ]; then
    dire "[simulation] ici : $PLAY_PYTHON navigateur/publier.py (sans --oui), dans la copie. Non lance en simulation : il se connecte au serveur (rsync -n)."
    return 0
  fi
  lancer_publier > "$TMP_ARCHIVES/play-simulation-$ID.log" 2>&1 &
  PID_PLAY_SIM=$!
}

attendre_echeance() {
  if [ "$REEL" -eq 0 ]; then dire "[simulation] attente de $ANNONCE min sautee."; return 0; fi
  local total="${DEPLOYER_ATTENTE_SECONDES:-$((ANNONCE * 60))}" reste
  reste=$(( total - ( $(date +%s) - DEBUT_ANNONCE ) ))
  while [ "$reste" -gt 0 ]; do
    dire "attente de l'echeance de l'annonce : encore $(( (reste + 59) / 60 )) min"
    if [ "$reste" -gt 60 ]; then sleep 60; else sleep "$reste"; fi
    reste=$(( total - ( $(date +%s) - DEBUT_ANNONCE ) ))
  done
  if [ -n "$PID_PLAY_SIM" ]; then
    wait "$PID_PLAY_SIM" || { tail -20 "$TMP_ARCHIVES/play-simulation-$ID.log"; arret "la simulation de Play a echoue : le site n'a pas ete touche."; }
    PID_PLAY_SIM=""
    dire "simulation de Play reussie."
  fi
}

images_custom() {
  # ⚠ TROUVE LE 21/10/2026, PREMIER VRAI DEPLOIEMENT REEL AVEC CE SCRIPT :
  # `deployer.ps1` avait sa propre etape « Images custom » (comparaison taille
  # par taille, assets/pics SEUL — assets/pics-fr est un depot ponctuel, fait
  # a la main, jamais resynchronise ici) ; ce script-ci n'avait AUCUN
  # equivalent. L'archive de code exclut deja `assets/pics` (voir plus bas,
  # "les scans voyagent par une etape a part") : sans cette fonction, un scan
  # tout neuf (ex. les portraits Quasar/Binary de Galactic Storm) n'atteint
  # JAMAIS le serveur, silencieusement — la carte manque a l'ecran, rien ne le
  # signale. `rsync --delete` remplace la comparaison manuelle de deployer.ps1 :
  # memes effets (envoie ce qui manque ou differe, efface ce qui a disparu en
  # local), beaucoup moins de code.
  etape "5b. Images custom (assets/pics)"
  local source="$RACINE/Fusion/marvel-lcg-src/assets/pics/"
  local cible="$DIST/Fusion/marvel-lcg-src/assets/pics/"
  if [ "$REEL" -eq 0 ]; then
    dire "[simulation] rsync -az --delete $source -> $cible"
    return 0
  fi
  rsync -az --delete -e "ssh -i $CLE -o ConnectTimeout=30 -o StrictHostKeyChecking=accept-new" \
    "$source" "$HOTE:$cible"
  dire "images custom envoyees."
  planches_livret
}

planches_livret() {
  # ⚠ TROUVE LE 22/10/2026 : `public/stories/` (planches des livrets de campagne)
  # est dans le .gitignore, donc ABSENT de la copie propre dont l'archive de code
  # est tiree ; or l'etape 6 fait `rm -rf .../public` sur le serveur avant
  # d'extraire. Chaque deploiement effacait donc toutes les planches en ligne :
  # le livret de l'ecran de campagne s'affichait vide (« No booklet page for
  # this step »). On les renvoie depuis le poste, apres l'extraction, SANS
  # --delete : on ajoute et on remplace, on n'efface jamais.
  etape "5c. Planches de livret (public/stories)"
  local source="$RACINE/Fusion/marvel-lcg-src/public/stories/"
  local cible="$DIST/Fusion/marvel-lcg-src/public/stories/"
  [ -d "$source" ] || arret "public/stories introuvable sur le poste : le livret serait vide en ligne."
  if [ "$REEL" -eq 0 ]; then
    dire "[simulation] rsync -az $source -> $cible"
    return 0
  fi
  rsync -az -e "ssh -i $CLE -o ConnectTimeout=30 -o StrictHostKeyChecking=accept-new" \
    "$source" "$HOTE:$cible"
  ssh_h "chown -R narwhal:narwhal $cible"
  dire "planches de livret envoyees."
}

redemarrer() {
  distant_script "dependances, vignettes, scans HD, redemarrage" <<REMOTE
set -e
DIST=$DIST
\$DIST/venv310/bin/python --version
for req in \$DIST/Fusion/marvel-lcg-src/requirements.txt \$DIST/site/requirements.txt; do
  if [ -f "\$req" ]; then \$DIST/venv310/bin/python -m pip install -q --upgrade -r "\$req"; fi
done
\$DIST/venv310/bin/python \$DIST/Fusion/marvel-lcg-src/tools/generer_vignettes.py
\$DIST/venv310/bin/python \$DIST/Fusion/marvel-lcg-src/tools/telecharger_scans_hd.py
chown -R narwhal:narwhal \$DIST
systemctl restart narwhal
sleep 3
systemctl is-active narwhal
REMOTE
}

palettes_installer() {
  # Pose la fusion sur le serveur (le `chown -R` de `redemarrer` lui donne son
  # proprietaire), puis la rend au depot : le fichier du poste ET la base de la
  # prochaine fusion deviennent ce qui est maintenant en ligne.
  if [ "$REEL" -eq 0 ]; then
    dire "[simulation] serveur : data/palettes-heros-corrections.json <- fusion ; poste : fichier et base mis a jour."
    return 0
  fi
  distant_script "couleurs corrigees : pose de la fusion" <<REMOTE
set -e
test -s /tmp/narwhal-palettes-corrections.json
cp /tmp/narwhal-palettes-corrections.json $DIST/Fusion/marvel-lcg-src/data/palettes-heros-corrections.json
rm -f /tmp/narwhal-palettes-corrections.json
REMOTE
  cp "$PALETTES_FUSION" "$PALETTES_LOCAL"
  cp "$PALETTES_FUSION" "$PALETTES_BASE"
  dire "couleurs : fichier du poste et base de synchronisation mis a jour (a commiter)."
}

remplacer_code() {
  etape "6. Remplacement du code sur le serveur"
  distant_script "archive de retour arriere $ROLLBACK" <<REMOTE
set -e
tar -czf $ROLLBACK -C $DIST --exclude='site/comptes.json' --exclude='*.db*' --exclude='site/rapports' Fusion/marvel-lcg-src/src Fusion/marvel-lcg-src/public Fusion/marvel-lcg-src/data site
test -s $ROLLBACK
ls -lh $ROLLBACK
REMOTE
  PHASE="extraction"
  distant_script "extraction du code (sans toucher aux comptes, bases, rapports)" <<REMOTE
set -e
test -s /tmp/narwhal-code.tgz
rm -rf $DIST/Fusion/marvel-lcg-src/src $DIST/Fusion/marvel-lcg-src/public
find $DIST/site -mindepth 1 -maxdepth 1 ! -name comptes.json ! -name '*.db' ! -name '*.sqlite3' ! -name '*.db-*' ! -name '*.sqlite3-*' ! -name rapports -exec rm -rf {} +
tar -xzmf /tmp/narwhal-code.tgz -C $DIST
chown -R narwhal:narwhal $DIST
REMOTE
  distant_script "scripts et conf (narwhal.service et Caddyfile : surveilles, jamais ecrits)" <<REMOTE
set -e
test -s /tmp/narwhal-conf.tgz
rm -rf /tmp/narwhal-conf; mkdir -p /tmp/narwhal-conf
tar -xzf /tmp/narwhal-conf.tgz -C /tmp/narwhal-conf
bash /tmp/narwhal-conf/synchroniser-conf.sh $DIST narwhal $DOMAINE
REMOTE
  palettes_installer
  images_custom
  redemarrer
}

verifier_site() {
  if [ "$REEL" -eq 0 ]; then
    dire "[simulation] verification : md5 du board-*.js serveur = $MD5_LOCAL ; systemctl is-active narwhal ; curl https://$DOMAINE/ = 200"
    return 0
  fi
  local sortie md5d actif code
  sortie="$(ssh_h "md5sum $DIST/Fusion/marvel-lcg-src/public/app/assets/board-*.js | cut -c1-32; systemctl is-active narwhal" </dev/null)"
  md5d="$(printf '%s\n' "$sortie" | sed -n 1p)"; actif="$(printf '%s\n' "$sortie" | tail -1)"
  [ "$md5d" = "$MD5_LOCAL" ] || arret "plateau du serveur ($md5d) different de celui construit ($MD5_LOCAL)."
  [ "$actif" = "active" ] || arret "le service narwhal n'est pas actif ($actif)."
  code="$(curl -s -o /dev/null -w '%{http_code}' "https://$DOMAINE/")"
  [ "$code" = "200" ] || arret "https://$DOMAINE/ repond $code au lieu de 200."
  CODE_SITE="$code"; MD5_SERVEUR="$md5d"
  dire "site : plateau identique ($md5d), service actif, HTTP $code"
}

sauvegarde_et_verification_site() {
  etape "6b. Sauvegarde des comptes et verification du site"
  if [ "$REEL" -eq 1 ]; then
    ssh_h "sudo -u narwhal RACINE=$DIST /usr/local/bin/narwhal-sauvegarde" </dev/null \
      || dire "AVERTISSEMENT : la sauvegarde des comptes a echoue (le deploiement, lui, est fait). A relancer a la main."
  else
    dire "[simulation] serveur : sudo -u narwhal RACINE=$DIST /usr/local/bin/narwhal-sauvegarde"
  fi
  verifier_site
}

publier_play() {
  etape "7. Play"
  preparer_play
  if [ "$REEL" -eq 0 ]; then
    dire "[simulation] ici : publier.py --oui --sans-construire, copie des sons, verification du board-*.js, curl play. = 200"
    return 0
  fi
  lancer_publier --oui --sans-construire || arret "la publication de Play a echoue."
  ssh_h "cp -u $DIST/Fusion/marvel-lcg-src/assets/sounds/*.wav $DIST/Fusion/marvel-lcg-src/assets/sounds/*.mp3 /opt/narwhal-play-scans/originaux/sounds/; chown 1000:1000 /opt/narwhal-play-scans/originaux/sounds/*; ls /opt/narwhal-play-scans/originaux/sounds | wc -l" </dev/null \
    | sed 's/^/   sons de play. : /'
  local local_play distant code
  local_play="$(md5sum "$WT"/navigateur/dist/app/assets/board-*.js | head -1 | cut -c1-32)"
  distant="$(ssh_h "md5sum /opt/narwhal-play/app/assets/board-*.js | head -1 | cut -c1-32" </dev/null)"
  [ "$distant" = "$local_play" ] || arret "plateau de play. ($distant) different de navigateur/dist ($local_play)."
  code="$(curl -s -o /dev/null -w '%{http_code}' "https://play.$DOMAINE/navigateur.html")"
  [ "$code" = "200" ] || arret "https://play.$DOMAINE/navigateur.html repond $code au lieu de 200."
  CODE_PLAY="$code"
  dire "play. : plateau identique ($distant), HTTP $code"
}

retour_arriere() {
  etape "Retour arriere depuis $RETOUR"
  case "$RETOUR" in
    /root/rollback-code-*.tgz) ;;
    *) arret "fichier attendu : /root/rollback-code-<id>.tgz (chemin sur le serveur)." ;;
  esac
  ROLLBACK="$RETOUR"
  if [ "$REEL" -eq 1 ]; then
    printf 'Archives de retour arriere presentes sur le serveur :\n'
    ssh_h "ls -1t /root/rollback-code-*.tgz 2>/dev/null | head -10" </dev/null | sed 's/^/   /' || true
    confirmer "Je restaure $RETOUR"
  fi
  PHASE="extraction"
  distant_script "restauration de $RETOUR (comptes, bases et rapports intacts)" <<REMOTE
set -e
test -s $RETOUR
rm -rf $DIST/Fusion/marvel-lcg-src/src $DIST/Fusion/marvel-lcg-src/public
find $DIST/site -mindepth 1 -maxdepth 1 ! -name comptes.json ! -name '*.db' ! -name '*.sqlite3' ! -name '*.db-*' ! -name '*.sqlite3-*' ! -name rapports -exec rm -rf {} +
tar -xzmf $RETOUR -C $DIST
chown -R narwhal:narwhal $DIST
REMOTE
  redemarrer
  if [ "$REEL" -eq 1 ]; then
    local actif code
    actif="$(ssh_h "systemctl is-active narwhal" </dev/null)"
    [ "$actif" = "active" ] || arret "service narwhal non actif apres restauration ($actif)."
    code="$(curl -s -o /dev/null -w '%{http_code}' "https://$DOMAINE/")"
    [ "$code" = "200" ] || arret "https://$DOMAINE/ repond $code apres restauration."
    dire "restauration terminee : service actif, HTTP $code. Play n'est pas restaure par ce mode (republiez un ancien commit si besoin)."
  fi
  PHASE="fini"
}

resume() {
  etape "9. Resume"
  dire "commit            : $COMMIT"
  dire "mode              : $([ "$REEL" -eq 1 ] && echo REEL || echo SIMULATION)"
  dire "joueurs vus       : ${JOUEURS:-non lu}"
  dire "plateau (md5)     : $MD5_LOCAL (serveur : ${MD5_SERVEUR:-n/a})"
  dire "HTTP site / play  : ${CODE_SITE:-n/a} / ${CODE_PLAY:-n/a}"
  if [ "$SITE" -eq 1 ]; then
    dire "retour arriere    : $ROLLBACK (sur le serveur)"
    dire "pour restaurer    : bash deploiement/deployer-linux.sh --retour-arriere $ROLLBACK --oui"
  fi
  if [ "$REEL" -eq 0 ]; then dire "SIMULATION : rien n'a ete envoye. Pour deployer : relancer avec --oui."; fi
}

main() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --simulation) REEL=0 ;;
      --oui) REEL=1 ;;
      --annonce) shift; [[ "${1:-}" =~ ^[0-9]+$ ]] && [ "$1" -ge 1 ] || arret "--annonce attend un nombre de minutes (>= 1)."; ANNONCE="$1" ;;
      --commit) shift; COMMIT_DEMANDE="${1:?--commit attend un identifiant}" ;;
      --site-seul) PLAY=0 ;;
      --play-seul) SITE=0 ;;
      --retour-arriere) shift; RETOUR="${1:?--retour-arriere attend un fichier}" ;;
      --aide|-h|--help) usage; exit 0 ;;
      *) arret "option inconnue : $1 (voir --aide)" ;;
    esac
    shift
  done
  if [ "$SITE" -eq 0 ] && [ "$PLAY" -eq 0 ]; then arret "--site-seul et --play-seul s'excluent."; fi
  trap nettoyer EXIT
  dire "deployer-linux.sh : $([ "$REEL" -eq 1 ] && echo 'MODE REEL' || echo 'SIMULATION (aucun envoi)')"

  preparer_cle
  if [ -n "$RETOUR" ]; then
    retour_arriere
    return 0
  fi

  precontroles
  if [ "$REEL" -eq 1 ]; then
    printf '\nMODE REEL : le serveur de production va etre modifie.\n'
    if [ "$SITE" -eq 1 ]; then compter_joueurs; fi
    confirmer "Je deploie $COURT"
  else
    dire "[simulation] nombre de joueurs non lu (aucune connexion en simulation)."
  fi
  copie_propre
  if [ "$SITE" -eq 1 ]; then
    poser_annonce
    palettes_corrections
    archives
  fi
  if [ "$PLAY" -eq 1 ]; then play_simulation_en_parallele; fi
  if [ "$SITE" -eq 1 ]; then
    attendre_echeance
    remplacer_code
    sauvegarde_et_verification_site
  elif [ -n "$PID_PLAY_SIM" ]; then
    wait "$PID_PLAY_SIM" || arret "la simulation de Play a echoue."
  fi
  if [ "$PLAY" -eq 1 ]; then publier_play; fi
  if [ "$SITE" -eq 1 ]; then retirer_annonce; fi
  PHASE="fini"
  resume
}

main "$@" 2>&1 | tee "$JOURNAL"
exit "${PIPESTATUS[0]}"
