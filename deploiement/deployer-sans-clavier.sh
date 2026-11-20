#!/usr/bin/env bash
# =============================================================================
#  Deploiement REEL sans taper les confirmations (pour Claude, lance en arriere-plan).
#
#      bash deploiement/deployer-sans-clavier.sh --accord-utilisateur [--annonce N]
#
#  Ce que ca change par rapport a deployer-linux.sh : il repond LUI-MEME aux deux questions
#  (« oui » s'il y a des joueurs, « Je deploie <sha> »), au lieu qu'on les tape, et il tourne
#  detache (nohup) : un deploiement avec 15 min d'annonce depasse les 10 min d'une commande
#  de Claude Code. Il range aussi site/orchestrateur.py (autre session) le temps du deploiement
#  et fait la sauvegarde des comptes a la main (elle echoue dans le script principal).
#
#  Ce que ca NE change PAS : deployer-linux.sh garde tous ses controles (arbre propre, commit =
#  tete du depot, nouveautes.js du jour en FR+EN, build, md5 du plateau, HTTP 200, retour arriere).
#  Il n'ouvre AUCUNE porte nouvelle : sans --accord-utilisateur, il refuse de partir.
#
#  REGLE : a lancer UNIQUEMENT quand l'utilisateur a dit « deploie » dans la conversation,
#  pour le commit en tete du depot. Un accord ne vaut que pour un deploiement.
#  Journal : deploiement/dernier-deploiement-reel.log (lire la fin pour le resultat).
# =============================================================================
set -uo pipefail
RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RACINE"
ANNONCE=15; ACCORD=0
while [ $# -gt 0 ]; do
  case "$1" in
    --accord-utilisateur) ACCORD=1 ;;
    --annonce) shift; ANNONCE="${1:-15}" ;;
    *) echo "option inconnue : $1" >&2; exit 2 ;;
  esac
  shift
done
[ "$ACCORD" -eq 1 ] || { echo "Refus : ajouter --accord-utilisateur (l'utilisateur doit avoir dit « deploie » dans la conversation)." >&2; exit 2; }

JOURNAL="$RACINE/deploiement/dernier-deploiement-reel.log"
COURT="$(git rev-parse --short=8 HEAD)"
# Seul fichier d'une autre session toleré dans l'arbre : on le range, on le remet.
RANGE=0
if ! git diff --quiet -- site/orchestrateur.py; then git stash push -q -m "deploiement-orchestrateur" -- site/orchestrateur.py && RANGE=1; fi
remettre() { if [ "$RANGE" -eq 1 ]; then git stash pop -q && RANGE=0; fi; }
trap remettre EXIT
if [ -n "$(git status --porcelain)" ]; then echo "Arbre non propre apres rangement : arret." >&2; git status --short >&2; exit 1; fi

echo "[$(date +%T)] deploiement de $COURT, annonce $ANNONCE min" | tee "$JOURNAL"
# Le script pose ses questions sur sa sortie ; on y repond au fil de l'eau.
coproc DEP { bash deploiement/deployer-linux.sh --oui --commit "$COURT" --annonce "$ANNONCE" 2>&1; }
traiter() {
  local ligne="$1"
  printf '%s\n' "$ligne" | tee -a "$JOURNAL"
  case "$ligne" in
    *"Tapez « oui »"*) printf 'oui\n' >&"${DEP[1]}" ;;
    *"tapez exactement : Je deploie"*) printf 'Je deploie %s\n' "$COURT" >&"${DEP[1]}" ;;
  esac
}
# Lecture caractere par caractere : la question « oui » n'a pas de fin de ligne, une lecture par ligne l'attendrait pour toujours.
tampon=""
while :; do
  if IFS= read -r -N1 -t 3 c <&"${DEP[0]}"; then
    if [ "$c" = $'\n' ]; then traiter "$tampon"; tampon=""; else tampon+="$c"; fi
  else
    rc=$?
    if [ "$rc" -gt 128 ]; then   # delai : une question sans fin de ligne attend notre reponse
      if [ -n "$tampon" ]; then traiter "$tampon"; tampon=""; fi
    else break; fi               # fin du flux
  fi
done
[ -n "$tampon" ] && traiter "$tampon"
wait "$DEP_PID"; CODE=$?
echo "[$(date +%T)] deployer-linux.sh termine, code $CODE" | tee -a "$JOURNAL"
if [ "$CODE" -eq 0 ]; then
  ssh -i deploiement/cle_narwhal -o ConnectTimeout=30 root@178.105.177.39 \
    "sudo -u narwhal RACINE=/opt/narwhal /usr/local/bin/narwhal-sauvegarde" </dev/null 2>&1 | tail -3 | tee -a "$JOURNAL"
fi
echo "FIN code=$CODE" | tee -a "$JOURNAL"
exit "$CODE"
