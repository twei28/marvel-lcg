#!/bin/bash
# Recree les liens symboliques de Fusion/marvel-lcg-src/.game-src (et de ses
# freres .game-src-*), le dossier
# que vise tout l'outillage de validation (test_cards, test_capacites,
# verifier_tous_les_decks... voir docs/reference/GUIDE-CREATION-CONTENU.md §8).
#
# Pourquoi : ces liens sont des chemins ABSOLUS, propres a une machine. Copies
# d'un ordinateur a l'autre (Windows/WSL <-> Linux), ils arrivent casses ou
# changes en dossiers VIDES, et les outils testent alors un moteur sans cartes
# sans le dire. Constate le 15/10/2026 apres le passage du PC Windows a Linux.
#
# Sans danger : ne remplace qu'un lien casse, un lien qui pointe ailleurs, ou
# un dossier VIDE. Un dossier non vide est laisse tel quel et signale.
# Marche sous Linux et sous WSL (lancer depuis la machine qui fera les tests).

set -u
RACINE="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
MOTEUR="$RACINE/Fusion/marvel-lcg-src"
[ -d "$MOTEUR/src" ] || { echo "Moteur introuvable : $MOTEUR"; exit 1; }
mkdir -p "$MOTEUR/.game-src"

lier() {  # lier <nom dans le dossier de jeu> <cible absolue>
    local nom="$1" cible="$2" chemin="$DEST/$1"
    if [ -L "$chemin" ]; then
        [ "$(readlink "$chemin")" = "$cible" ] && [ -e "$chemin" ] && { echo "ok      $nom"; return; }
        rm -f "$chemin"
    elif [ -d "$chemin" ]; then
        if [ -n "$(ls -A "$chemin")" ]; then
            echo "LAISSE  $nom : dossier non vide, a verifier a la main"; return
        fi
        rmdir "$chemin"
    elif [ -e "$chemin" ]; then
        echo "LAISSE  $nom : fichier ordinaire, a verifier a la main"; return
    fi
    ln -s "$cible" "$chemin" && echo "relie   $nom -> $cible"
}

# Tous les dossiers de jeu de test : `.game-src` et ses freres crees par les
# harnais (`.game-src-par0`... pour PARALLELES=n, `.game-src-camp0`... pour
# test_campagnes, `.game-src-a`, `-b2`... pour les agents). Ils ont TOUS le
# meme defaut apres une copie d'une machine a l'autre.
for DEST in "$MOTEUR"/.game-src "$MOTEUR"/.game-src-*; do
    [ -d "$DEST" ] || continue
    echo "== $(basename "$DEST")"
    for d in cards core engine game editor; do lier "$d" "$MOTEUR/src/$d"; done
    for d in data deck assets public puzzle; do lier "$d" "$MOTEUR/$d"; done
done
