#!/bin/bash
# Lanceur Linux : equivalent de JOUER-SOLO.bat (Windows, via WSL) et de
# JOUER-SOLO.command (macOS). Sous Linux il n'y a rien a emuler : on execute
# directement le moteur.
#
# Ce script se suffit a lui-meme :
#   1. si une partie tourne deja sur le port 2345, il ouvre le navigateur
#      dessus au lieu d'en lancer une seconde ;
#   2. il trouve un Python 3.10 ou plus recent ;
#   3. il cree un environnement isole `.venv-linux` DANS le dossier du jeu, au
#      premier lancement seulement, et y installe les 3 dependances ;
#   4. il repare le dossier .game s'il vient d'une autre machine (voir plus bas) ;
#   5. il lance le moteur, qui ouvre le navigateur tout seul.

set -u
cd "$(dirname "$(readlink -f "$0")")" || exit 1

MOTEUR="Fusion/marvel-lcg-src"
VENV=".venv-linux"
# Bibliotheques dont le moteur a besoin (noms pip, puis noms d'import).
DEPENDANCES="aiohttp colorama requests packaging numpy pillow typing_extensions"
IMPORTS="aiohttp, colorama, requests, packaging, numpy, PIL, typing_extensions"
ADRESSE="http://127.0.0.1:2345/"

fermer() {
    echo
    read -r -p "Appuie sur Entree pour fermer." _
    exit "${1:-0}"
}

echo "Marvel Champions : partie solo"
echo "(laisse cette fenetre ouverte pendant toute la partie)"
echo

if [ ! -f "$MOTEUR/launcher_fast.py" ]; then
    echo "ERREUR : $MOTEUR/launcher_fast.py est introuvable."
    echo "Ce script doit rester a la racine du dossier du jeu, a cote du dossier Fusion."
    fermer 1
fi

# --- 1. partie deja lancee ? --------------------------------------------------
if curl -s -o /dev/null --max-time 3 "$ADRESSE"; then
    echo "Une partie tourne deja sur le port 2345."
    echo "J'ouvre le navigateur dessus plutot que d'en lancer une seconde."
    echo "Pour repartir de zero, ferme d'abord le jeu en cours."
    xdg-open "$ADRESSE" >/dev/null 2>&1 &
    fermer 0
fi

# --- 2. trouver un Python utilisable ----------------------------------------
# 3.10 EN PREMIER : c'est la seule version sur laquelle le moteur est eprouve.
# Les suivantes sont acceptees en repli, avec un avertissement du launcher.
# ~/.local/bin d'abord : c'est la que `uv python install 3.10` depose son
# Python, et ce dossier manque au PATH quand on lance par double-clic.
export PATH="$HOME/.local/bin:$PATH"
PY=""
for candidat in python3.10 python3.11 python3.12 python3.13 python3; do
    chemin=$(command -v "$candidat" 2>/dev/null) || continue
    if "$chemin" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)' 2>/dev/null; then
        PY="$chemin"
        break
    fi
done

if [ -z "$PY" ]; then
    echo "ERREUR : aucun Python 3.10 ou plus recent n'a ete trouve."
    echo "Installe-le sans droits administrateur avec :  uv python install 3.10"
    echo "(ou avec :  sudo apt install python3 python3-venv)"
    fermer 1
fi
echo "Python utilise : $("$PY" --version 2>&1) ($PY)"

# --- 3. environnement isole, cree une seule fois -----------------------------
# On verifie que l'environnement FONCTIONNE, pas seulement qu'il existe : un
# environnement copie depuis une autre machine peut pointer vers un Python qui
# n'existe pas ici.
if [ -e "$VENV/bin/python" ] && ! "$VENV/bin/python" -c 'pass' 2>/dev/null; then
    echo "L'environnement present vient d'une autre machine, je le refais."
    rm -rf "$VENV"
fi

if [ ! -x "$VENV/bin/python" ]; then
    echo "Premier lancement : preparation de l'environnement (une minute environ)..."
    if ! "$PY" -m venv "$VENV" >/dev/null 2>&1; then
        rm -rf "$VENV"
        VERSION=$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
        echo
        echo "ERREUR : impossible de creer l'environnement Python : le module venv manque."
        echo "Installe-le avec :  sudo apt install python${VERSION}-venv"
        echo "puis relance ce fichier."
        fermer 1
    fi
    echo "Environnement cree."
fi

# Dependances verifiees a CHAQUE lancement : une liste qui s'allonge ne doit
# pas obliger a refaire l'environnement a la main.
if ! "$VENV/bin/python" -c "import $IMPORTS" 2>/dev/null; then
    echo "Installation des dependances du jeu..."
    if ! "$VENV/bin/python" -m pip install --quiet --upgrade pip $DEPENDANCES; then
        echo
        echo "ERREUR : l'installation des dependances a echoue."
        echo "Verifie la connexion internet, puis relance ce fichier."
        echo "(Les dependances sont : $DEPENDANCES.)"
        fermer 1
    fi
    echo "Dependances pretes."
    echo
fi

# Chemin ABSOLU vers l'interpreteur : le launcher fait un chdir vers .game.
PYTHON_JEU="$(cd "$VENV/bin" && pwd)/python"

# --- 4. reparer un .game venu d'une autre machine ----------------------------
# a) Les liens symboliques data/deck/public/puzzle/assets de .game deviennent
#    des fichiers VIDES quand on copie le dossier depuis Windows. Le launcher
#    croirait alors qu'il s'agit d'un ancien dossier et planterait en essayant
#    de le supprimer. On efface ces coquilles vides : il refait les liens.
GAME="$MOTEUR/.game"
for nom in data deck public puzzle assets; do
    if [ -f "$GAME/$nom" ] && [ ! -s "$GAME/$nom" ] && [ ! -L "$GAME/$nom" ]; then
        rm -f "$GAME/$nom"
    fi
done
# b) Les .pyc de .game sont propres a UNE version de Python. Compiles par une
#    autre (le 3.10 de WSL, par exemple), ils seraient juges « a jour » par la
#    compilation incrementale et refuses a l'import (« bad magic number »).
#    On compare la signature et on force une reconstruction complete si besoin.
OPTIONS=()
if [ -f "$GAME/main.pyc" ]; then
    ATTENDU=$("$PYTHON_JEU" -c 'import importlib.util; print(importlib.util.MAGIC_NUMBER.hex())')
    PRESENT=$(head -c 4 "$GAME/main.pyc" | od -An -tx1 | tr -d ' \n')
    if [ "$ATTENDU" != "$PRESENT" ]; then
        echo "Le jeu a ete compile par une autre version de Python : reconstruction complete"
        echo "(le premier lancement sera plus long, les suivants redeviendront rapides)."
        OPTIONS+=(--clean)
    fi
fi

# --- 5. lancement -------------------------------------------------------------
echo "Demarrage du moteur... le navigateur s'ouvrira tout seul."
echo
cd "$MOTEUR" || exit 1
# Droits d'administrateur EN LOCAL (palettes, boutons d'admin) : le reglage vit dans launch.admin-local.json,
# a la racine du depot, HORS de Fusion/marvel-lcg-src (le dossier envoye au serveur par le deploiement).
# Sans lui, ou ailleurs que sur ce poste, le moteur ne te reconnait pas comme administrateur.
if [ -f ../../launch.admin-local.json ]; then
    OPTIONS+=(--config ../../launch.admin-local.json)
fi
"$PYTHON_JEU" launcher_fast.py "${OPTIONS[@]}"

echo
echo "Partie terminee."
fermer 0
