#!/bin/bash
# Prepare une COPIE ISOLEE du depot (git worktree) pour lancer les harnais de test
# du moteur (tools/test_capacites.py, tools/autoplay.py...). Cree le 15/10/2026
# pour faire travailler plusieurs agents en parallele, chacun dans sa copie.
#
# Ce que `reparer-game-src.sh` ne fait pas : les fichiers NON versionnes que le
# lanceur pose a cote des liens dans `.game-src` (main.py, build.py,
# game_entry.py, winsound.py, launch.json). On les recopie depuis le depot
# principal (MAIN, 1er argument ; defaut : /home/oem/Desktop/Marvel LCG).
#
# Usage, depuis la RACINE de la copie :  bash outils/preparer-worktree.sh
set -eu
MAIN="${1:-/home/oem/Desktop/Marvel LCG}"
ICI="$(cd "$(dirname "$0")/.." && pwd)"
bash "$ICI/outils/reparer-game-src.sh" >/dev/null
M="$ICI/Fusion/marvel-lcg-src"
for f in main.py build.py game_entry.py; do cp -f "$M/src/$f" "$M/.game-src/$f"; done
for f in winsound.py launch.json; do
    [ -f "$MAIN/Fusion/marvel-lcg-src/.game-src/$f" ] && cp -f "$MAIN/Fusion/marvel-lcg-src/.game-src/$f" "$M/.game-src/$f"
done
# Les images (assets/pics) ne sont pas versionnees : liens vers celles du depot principal.
for d in pics pics-fr; do
    if [ -d "$MAIN/Fusion/marvel-lcg-src/assets/$d" ] && [ ! -e "$M/assets/$d" ]; then
        ln -s "$MAIN/Fusion/marvel-lcg-src/assets/$d" "$M/assets/$d"
    fi
done
echo "copie prete : $M/.game-src"
