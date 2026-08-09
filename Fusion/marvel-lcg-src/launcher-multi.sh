#!/usr/bin/env bash
# Lanceur de partie multijoueur en ligne.
# Demarre le moteur avec launch.online.json (mot de passe actif), ouvre un
# tunnel Cloudflare, puis affiche LE lien et LE mot de passe a donner.
# Rien n'est expose en dehors de la duree de ce script : Ctrl+C ferme tout.
set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-$HOME/marvel-work/python/bin/python3.10}"
CLOUDFLARED="${CLOUDFLARED:-$HOME/marvel-work/tools/cloudflared}"
CONFIG="${CONFIG:-launch.online.json}"

lire_config() { python3 -c "import json,sys;print(json.load(open(sys.argv[1]))$1)" "$RACINE/$CONFIG"; }
PORT="$(lire_config "['server_addresses'][0].split(':')[-1]")"
MOT_DE_PASSE="$(lire_config "['password']")"

for outil in "$PYTHON" "$CLOUDFLARED"; do
  [ -x "$outil" ] || { echo "Introuvable ou non executable : $outil" >&2; exit 1; }
done
# Sans mot de passe d'entree, le lien du tunnel est la SEULE barriere. C'est un
# choix assume pour une partie entre amis : l'adresse est aleatoire et change a
# chaque lancement. Le script previent, il ne refuse plus.
if [ -z "$MOT_DE_PASSE" ]; then
  echo "Partie SANS mot de passe : quiconque a le lien peut entrer." >&2
fi

JOURNAL_TUNNEL="$(mktemp)"
# Journal du MOTEUR. Il partait dans /dev/null : quand une partie refusait de
# se creer, la trace de l'erreur disparaissait avec elle et il ne restait qu'un
# plateau vide a Round 0, sans rien a lire. Chemin fixe (pas un mktemp) pour
# qu'on puisse l'ouvrir pendant que la partie tourne.
JOURNAL_JEU="/tmp/marvel-multi.log"
PID_JEU=""
PID_TUNNEL=""

nettoyer() {
  echo
  echo "Fermeture de la partie..."
  [ -n "$PID_TUNNEL" ] && kill "$PID_TUNNEL" 2>/dev/null
  [ -n "$PID_JEU" ] && kill "$PID_JEU" 2>/dev/null
  wait 2>/dev/null
  rm -f "$JOURNAL_TUNNEL"
  echo "Tunnel ferme, moteur arrete. Le lien ne fonctionne plus."
}
trap nettoyer EXIT INT TERM

echo "Demarrage du moteur..."
cd "$RACINE"
# PYTHONUNBUFFERED : sans lui, Python tamponne sa sortie des qu'elle n'est plus
# un terminal. Le journal restait a 24 octets pendant que le moteur tournait,
# c'est-a-dire inutilisable au moment precis ou l'on en a besoin.
PYTHONUNBUFFERED=1 "$PYTHON" -u launcher_fast.py --config "$CONFIG" >"$JOURNAL_JEU" 2>&1 &
PID_JEU=$!
echo "Journal du moteur : $JOURNAL_JEU"

for _ in $(seq 1 240); do
  curl -s -o /dev/null "http://127.0.0.1:$PORT/" && break
  kill -0 "$PID_JEU" 2>/dev/null || { echo "Le moteur s'est arrete au demarrage." >&2; exit 1; }
  sleep 1
done
curl -s -o /dev/null "http://127.0.0.1:$PORT/" || { echo "Le moteur ne repond pas sur le port $PORT." >&2; exit 1; }

echo "Ouverture du tunnel..."
"$CLOUDFLARED" tunnel --url "http://127.0.0.1:$PORT" --no-autoupdate >"$JOURNAL_TUNNEL" 2>&1 &
PID_TUNNEL=$!

URL=""
for _ in $(seq 1 60); do
  URL="$(grep -oE 'https://[-a-z0-9]+\.trycloudflare\.com' "$JOURNAL_TUNNEL" | head -1)"
  [ -n "$URL" ] && break
  kill -0 "$PID_TUNNEL" 2>/dev/null || break
  sleep 1
done
[ -n "$URL" ] || { echo "Tunnel non etabli. Journal :" >&2; cat "$JOURNAL_TUNNEL" >&2; exit 1; }

LIEN="$URL/rejoindre.html"

# Mots de passe de sieges (protection : personne ne peut prendre le siege d'un
# autre). Chaque joueur recoit SON lien pret a cliquer.
SIEGE_1="$(lire_config "['seat_passwords'][1]" 2>/dev/null || echo '')"
SIEGE_2="$(lire_config "['seat_passwords'][2]" 2>/dev/null || echo '')"
SIEGE_3="$(lire_config "['seat_passwords'][3]" 2>/dev/null || echo '')"
SIEGE_0="$(lire_config "['seat_passwords'][0]" 2>/dev/null || echo '')"

if [ -n "$MOT_DE_PASSE" ]; then
  LIGNE_MDP="Mot de passe d'entree : $MOT_DE_PASSE
"
else
  LIGNE_MDP=""
fi

MESSAGE="Marvel Champions, on joue !
${LIGNE_MDP}Ton lien PERSONNEL (il reserve ton siege, ne le partage pas) :
- Joueur 2 : $URL/claim_seat?p=1&key=$SIEGE_1&to=salon
- Joueur 3 : $URL/claim_seat?p=2&key=$SIEGE_2&to=salon
- Joueur 4 : $URL/claim_seat?p=3&key=$SIEGE_3&to=salon
(chacun ne clique QUE sur le sien ; spectateurs : $LIEN)"

if command -v clip.exe >/dev/null 2>&1; then
  printf '%s' "$MESSAGE" | clip.exe 2>/dev/null && COPIE="  (message deja copie : Ctrl+V dans Discord ou WhatsApp)" || COPIE=""
else
  COPIE=""
fi

if [ -n "$MOT_DE_PASSE" ]; then
  BLOC_MDP="
   MOT DE PASSE D'ENTREE (demande a l'arrivee)
   $MOT_DE_PASSE
"
else
  BLOC_MDP="
   AUCUN MOT DE PASSE : le lien suffit pour entrer.
   Il est aleatoire et change a chaque lancement.
"
fi

cat <<INFOS

==============================================================
   PARTIE MULTI PRETE
==============================================================

   LIENS PERSONNELS A DONNER (un par joueur, il reserve son siege)
   Joueur 2 : $URL/claim_seat?p=1&key=$SIEGE_1&to=salon
   Joueur 3 : $URL/claim_seat?p=2&key=$SIEGE_2&to=salon
   Joueur 4 : $URL/claim_seat?p=3&key=$SIEGE_3&to=salon

$BLOC_MDP$COPIE

   TOI (hote, siege 1) : clique ce lien pour reserver TON siege
   puis creer la partie :
   http://127.0.0.1:$PORT/claim_seat?p=0&key=$SIEGE_0&to=prepare

   Spectateurs eventuels : $LIEN

   Si une partie refuse de se lancer, la raison est ici :
   $JOURNAL_JEU

   Ctrl+C ici = fin de la partie pour tout le monde.
   Le lien change a chaque lancement.
==============================================================

INFOS

wait "$PID_JEU"
