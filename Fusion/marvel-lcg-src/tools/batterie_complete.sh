#!/usr/bin/env bash
# BATTERIE COMPLETE des cas de test (8400+ cas, environ 1 h 30), pour la veille d'un deploiement ou une passe de nuit (23/10/2026).
#
#   bash tools/batterie_complete.sh            # lance et attend
#   bash tools/batterie_complete.sh --fond     # lance en arriere-plan, rend la main tout de suite
#   FILTRE='sl043' bash tools/batterie_complete.sh   # essai rapide sur quelques cas (sous-chaines separees par |)
#
# Ecrit dans /tmp/batterie_complete/<date-heure>/ : `sortie.txt` (le journal), `rapport.json`, et `RESUME.txt` (le bilan et les echecs).
# Echecs CONNUS avant ce script : les 4 cas Squirrel Girl (sg006 sg007 sg009 sg013). Un cas « processus mort » est un plantage de la machine
# sous charge, pas un defaut : le relancer seul (`tools/test_capacites.py .game-src <port> <rapport> "<nom du cas>"`).
# ⚠ Jamais pendant qu'un autre harnais (test_capacites, autoplay) tourne sur ce dossier : voir l'avertissement de test_capacites.py.
# ⚠ Ne pas modifier `src/` ni `tools/test_capacites.py` pendant qu'il tourne : les processus fils relisent ces fichiers a chaque cas.
set -u
cd "$(dirname "$(readlink -f "$0")")/.." || exit 1
PYTHON="${PYTHON:-$HOME/.marvel-venv/bin/python}"
SORTIE="/tmp/batterie_complete/$(date +%Y%m%d-%H%M)"
mkdir -p "$SORTIE"

lancer() {
    # Port BAS (< 49152 : plage dynamique de Windows/WSL2, sinon des cas tombent sur des ports pris).
    CAS_PREFIX="bc_$(date +%H%M)_" PARALLELES="${PARALLELES:-4}" "$PYTHON" tools/test_capacites.py .game-src 38000 "$SORTIE/rapport.json" ${FILTRE:+"$FILTRE"} > "$SORTIE/sortie.txt" 2>&1
    {
        echo "Batterie complete du $(date '+%d/%m/%Y %H:%M')"
        grep "^BILAN" "$SORTIE/sortie.txt" || echo "BILAN introuvable (la batterie a ete interrompue ?)"
        echo "--- ECHECS ---"
        grep -A1 "^ECHEC" "$SORTIE/sortie.txt" | cut -c1-220
    } > "$SORTIE/RESUME.txt"
    echo "FIN" >> "$SORTIE/sortie.txt"
}

if [ "${1:-}" = "--fond" ]; then
    lancer > /dev/null 2>&1 &
    echo "Batterie lancee en arriere-plan. Resume attendu dans : $SORTIE/RESUME.txt"
else
    lancer
    cat "$SORTIE/RESUME.txt"
fi
