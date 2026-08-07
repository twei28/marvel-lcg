#!/usr/bin/env bash
# Lanceur "serveur" : N moteurs INDEPENDANTS derriere N tunnels, pour que des
# amis jouent CHACUN leur partie classique tant que ce script tourne.
# Rien a voir avec launcher-multi.sh : ici, aucune partie n'est partagee.
# Ctrl+C ferme tout : les liens ne fonctionnent plus.
set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-$HOME/marvel-work/python/bin/python3.10}"
CLOUDFLARED="${CLOUDFLARED:-$HOME/marvel-work/tools/cloudflared}"
# SANS_TUNNEL=1 : moteurs seuls, adresses locales. Sert aux tests.
SANS_TUNNEL="${SANS_TUNNEL:-0}"
PORT_BASE=2350

NB_PLACES="${1:-4}"
case "$NB_PLACES" in
  1|2|3|4) ;;
  *) echo "Nombre de places invalide : '$NB_PLACES'. Attendu 1, 2, 3 ou 4." >&2; exit 2 ;;
esac

[ -x "$PYTHON" ] || { echo "Introuvable ou non executable : $PYTHON" >&2; exit 1; }
if [ "$SANS_TUNNEL" != "1" ]; then
  [ -x "$CLOUDFLARED" ] || { echo "Introuvable ou non executable : $CLOUDFLARED" >&2; exit 1; }
fi

cd "$RACINE"
"$PYTHON" tools/config_serveur.py "$NB_PLACES" >/dev/null || {
  echo "Generation des configurations impossible." >&2; exit 1; }

PIDS=()
JOURNAUX_TUNNEL=()
LIENS=()

nettoyer() {
  echo
  echo "Fermeture du serveur..."
  for pid in "${PIDS[@]:-}"; do
    [ -n "$pid" ] && kill "$pid" 2>/dev/null
  done
  wait 2>/dev/null
  for journal in "${JOURNAUX_TUNNEL[@]:-}"; do
    [ -n "$journal" ] && rm -f "$journal"
  done
  echo "Moteurs arretes, tunnels fermes. Les liens ne fonctionnent plus."
}
trap nettoyer EXIT INT TERM

for place in $(seq 1 "$NB_PLACES"); do
  port=$((PORT_BASE + place))
  journal_jeu="/tmp/marvel-serveur-$place.log"
  echo "Place $place : demarrage du moteur sur le port $port..."
  # PYTHONUNBUFFERED : sans lui, Python tamponne sa sortie des qu'elle n'est
  # plus un terminal, et le journal reste vide au moment ou l'on en a besoin.
  PYTHONUNBUFFERED=1 "$PYTHON" -u launcher_fast.py --config ".serveur/launch-$place.json" --no-browser \
    >"$journal_jeu" 2>&1 &
  pid_jeu=$!
  PIDS+=("$pid_jeu")

  pret=0
  for _ in $(seq 1 240); do
    curl -s -o /dev/null "http://127.0.0.1:$port/" && { pret=1; break; }
    kill -0 "$pid_jeu" 2>/dev/null || break
    sleep 1
  done
  if [ "$pret" != "1" ]; then
    echo "Place $place : le moteur n'a pas demarre. Voir $journal_jeu" >&2
    continue
  fi

  if [ "$SANS_TUNNEL" = "1" ]; then
    LIENS+=("Place $place : http://127.0.0.1:$port/prepare.html")
    continue
  fi

  journal_tunnel="$(mktemp)"
  JOURNAUX_TUNNEL+=("$journal_tunnel")
  "$CLOUDFLARED" tunnel --url "http://127.0.0.1:$port" --no-autoupdate \
    >"$journal_tunnel" 2>&1 &
  PIDS+=("$!")
  url=""
  for _ in $(seq 1 60); do
    url="$(grep -oE 'https://[-a-z0-9]+\.trycloudflare\.com' "$journal_tunnel" | head -1)"
    [ -n "$url" ] && break
    sleep 1
  done
  if [ -z "$url" ]; then
    echo "Place $place : tunnel non etabli, cette place restera locale." >&2
    continue
  fi
  LIENS+=("Place $place : $url/prepare.html")
done

# Degradation choisie : trois liens valent mieux que zero. On ne s'arrete que
# si AUCUNE place n'a pu s'ouvrir.
if [ "${#LIENS[@]}" -eq 0 ]; then
  echo "Aucune place n'a pu s'ouvrir. Rien a partager." >&2
  exit 1
fi

MESSAGE="Marvel Champions, sers-toi !
Ouvre TON lien, cree ta partie, joue quand tu veux.
$(printf '%s\n' "${LIENS[@]}")
(le lien ne marche que tant que mon PC tourne)"

COPIE=""
if command -v clip.exe >/dev/null 2>&1; then
  printf '%s' "$MESSAGE" | clip.exe 2>/dev/null && \
    COPIE="   (message deja copie : Ctrl+V dans Discord ou WhatsApp)"
fi

cat <<INFOS

==============================================================
   SERVEUR PRET  (${#LIENS[@]} place(s) sur $NB_PLACES)
==============================================================

$(printf '   %s\n' "${LIENS[@]}")

$COPIE

   Un lien par personne : deux personnes sur le meme lien
   jouent la MEME partie et se genent.

   Journaux des moteurs : /tmp/marvel-serveur-N.log
   Ctrl+C ici = fin pour tout le monde.
==============================================================

INFOS

wait
