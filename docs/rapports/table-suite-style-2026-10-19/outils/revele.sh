#!/bin/bash
# Captures du point 3 : « −X PV » des effets d'une carte revelee, avant (build de base, port 2598) et apres (2599).
# Usage : bash revele.sh   (serveur de jeu sur 2597, relais 2598/2599 : voir le rapport)
cd "$(dirname "$0")"
O="$(cd ../captures && pwd)"
lancer() { # carte tag port nom
  rm -f "$O"/revele-"$2"-delta-*
  CARTE=$1 BASE=http://127.0.0.1:$3 DIST=serveur TAG=$2 CAS=revele OUT="$O" timeout 400 node attaque.mjs 2>&1 | grep -E "BILAN\+"
  for f in 150 250 300 400 500 600 800; do [ -f "$O/revele-$2-delta-$f.png" ] && mv "$O/revele-$2-delta-$f.png" "$O/revele-$4-$2-$f.png"; done
}
lancer 01154 apres 2599 2cibles
lancer 01154 avant 2598 2cibles
lancer 04030 apres 2599 1cible
lancer 04030 avant 2598 1cible
ls "$O" | grep revele
