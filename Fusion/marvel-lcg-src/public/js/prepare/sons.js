// sons.js — les sons de l'écran de préparation.
//
// Le PLATEAU joue les sons que le moteur lui nomme (ui-app/src/board/sons.ts) ;
// ici personne ne nous nomme rien, c'est l'interface qui décide : choisir un
// héros, verrouiller une cible, lancer la partie. On réutilise les fichiers
// existants (assets/sounds/, servis à la racine par le moteur) plutôt que d'en
// ajouter : la liste des noms est figée côté moteur, et remplacer un `.wav`
// suffit à changer ce qu'on entend (voir docs/reference/SONS-DECLENCHEURS.md).
//
// Mêmes règles que le plateau, à dessein :
//   — volume 0.2 ;
//   — rien si l'onglet n'est pas visible ;
//   — un seul élément audio par fichier, rejoué depuis le début ;
//   — l'échec est silencieux. Le navigateur refuse de jouer avant la première
//     interaction de la page ; inutile de crier, le son suivant passera.
//
// ⚠ LE RÉGLAGE EST CELUI DU PLATEAU, `marvel-board-sons` (board.tsx). Une
// deuxième clé donnerait deux boutons à couper pour un seul silence voulu.

"use strict";

const VOLUME = 0.2;
const CLE_SONS = "marvel-board-sons";

/** Les sons que cet écran utilise, nommés par ce qu'ils VEULENT DIRE ici.
 *  La valeur est le fichier du moteur ; le nom de gauche est ce qu'on lit
 *  dans app.js, pour qu'un appel se relise sans aller voir la table. */
export const SON = {
    mode: "set",             // une tuile de mode se pose
    heros: "carddrop",       // le héros arrive sur la table
    herosRetire: "removecounter",
    favori: "token",         // un jeton posé sur la carte
    cible: "reveal",         // le méchant se retourne face visible
    etapeSuivante: "nextturn",
    etapePrecedente: "removecounter",
    aleatoire: "shuffle",    // on brasse
    lancement: "phase",      // le gong : la partie commence
};

const cache = new Map();

function actif() {
    try {
        // Actif PAR DÉFAUT, comme le plateau : l'absence de réglage veut dire
        // « je n'ai rien demandé », pas « je veux le silence ».
        return localStorage.getItem(CLE_SONS) !== "off";
    } catch (e) {
        return true;
    }
}

/** Joue un son de la table `SON`. Ne lève jamais. */
export function jouerSon(nom) {
    if (!nom || !actif()) return;
    if (document.visibilityState !== "visible") return;
    try {
        let audio = cache.get(nom);
        if (!audio) {
            audio = new Audio("/" + nom + ".wav");
            audio.volume = VOLUME;
            cache.set(nom, audio);
        }
        audio.currentTime = 0;
        const p = audio.play();
        if (p && p.catch) p.catch(() => undefined);
    } catch (e) {
        // Audio indisponible (contexte restreint, mémoire) : le silence est un
        // repli acceptable, une exception non.
    }
}
