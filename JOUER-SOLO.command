#!/bin/bash
# Lanceur macOS — equivalent de JOUER-SOLO.bat, qui lui passe par WSL.
#
# Le jeu est un programme Unix : il tourne deja sous Linux aujourd'hui, Windows
# ne fait que lancer WSL. Sur Mac il n'y a donc pas d'emulation, on execute
# directement le moteur.
#
# Ce script se suffit a lui-meme :
#   1. il trouve un Python 3.10 ou plus recent ;
#   2. il cree un environnement isole `.venv-mac` DANS le dossier du jeu, au
#      premier lancement seulement, et y installe les 3 dependances ;
#   3. il lance le moteur, qui ouvre le navigateur tout seul.
#
# Rien n'est installe ailleurs sur la machine, et supprimer le dossier du jeu
# supprime tout.

set -u
cd "$(dirname "$0")" || exit 1

MOTEUR="Fusion/marvel-lcg-src"
VENV=".venv-mac"

echo "Marvel Champions — partie solo"
echo "(laisse cette fenetre ouverte pendant toute la partie)"
echo

if [ ! -f "$MOTEUR/launcher.py" ]; then
    echo "ERREUR : $MOTEUR/launcher.py est introuvable."
    echo "Ce script doit rester a la racine du dossier du jeu, a cote du dossier Fusion."
    echo
    read -r -p "Appuie sur Entree pour fermer." _
    exit 1
fi

# --- 1. trouver un Python utilisable ----------------------------------------
# macOS livre python3 en 3.9 selon les versions, ce qui est TROP ANCIEN. On
# cherche donc explicitement les versions recentes avant de se rabattre.
PY=""
# 3.10 EN PREMIER : c'est la seule version sur laquelle le moteur est eprouve.
# Les suivantes sont acceptees en repli, avec un avertissement du launcher.
for candidat in python3.10 python3.11 python3.12 python3.13 python3; do
    chemin=$(command -v "$candidat" 2>/dev/null) || continue
    if "$chemin" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)' 2>/dev/null; then
        PY="$chemin"
        break
    fi
done

if [ -z "$PY" ]; then
    echo "ERREUR : aucun Python 3.10 ou plus recent n'a ete trouve."
    echo
    echo "Deux facons de l'installer :"
    echo "  - le plus simple : telecharger l'installeur sur https://www.python.org/downloads/"
    echo "  - avec Homebrew  : brew install python@3.12"
    echo
    echo "Puis relance ce fichier."
    echo
    read -r -p "Appuie sur Entree pour fermer." _
    exit 1
fi

echo "Python utilise : $("$PY" --version 2>&1) ($PY)"

# --- 2. environnement isole, cree une seule fois -----------------------------
# On verifie que l'environnement FONCTIONNE, pas seulement qu'il existe : un
# dossier copie depuis Windows peut contenir un environnement Linux, dont le
# binaire ne s'execute pas sur Mac. Sans ce controle, le script le reutiliserait
# et echouerait sans qu'on comprenne pourquoi.
if [ -e "$VENV/bin/python" ] && ! "$VENV/bin/python" -c 'pass' 2>/dev/null; then
    echo "L'environnement present vient d'une autre machine, je le refais."
    rm -rf "$VENV"
fi

if [ ! -x "$VENV/bin/python" ]; then
    echo "Premier lancement : preparation de l'environnement (une minute environ)..."
    if ! "$PY" -m venv "$VENV"; then
        echo
        echo "ERREUR : impossible de creer l'environnement Python."
        echo "Sur certaines installations il manque le module venv."
        echo "Essaie : $PY -m pip install --user virtualenv"
        echo
        read -r -p "Appuie sur Entree pour fermer." _
        exit 1
    fi
    if ! "$VENV/bin/python" -m pip install --quiet --upgrade pip aiohttp colorama requests; then
        echo
        echo "ERREUR : l'installation des dependances a echoue."
        echo "Verifie la connexion internet, puis relance ce fichier."
        echo "(Les dependances sont : aiohttp, colorama, requests.)"
        echo
        read -r -p "Appuie sur Entree pour fermer." _
        exit 1
    fi
    echo "Environnement pret."
    echo
fi

# --- 3. lancement -------------------------------------------------------------
# Chemin ABSOLU vers l'interpreteur : launcher.py fait un chdir vers son
# repertoire de jeu compile, un chemin relatif ne resoudrait plus rien ensuite.
PYTHON_JEU="$(cd "$VENV/bin" && pwd)/python"

echo "Demarrage du moteur... le navigateur s'ouvrira tout seul."
echo
cd "$MOTEUR" || exit 1
"$PYTHON_JEU" launcher.py

echo
echo "Partie terminee."
read -r -p "Appuie sur Entree pour fermer." _
