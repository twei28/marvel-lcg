// sons.js — les sons de l'écran de préparation.
//
// Le PLATEAU joue les sons que le moteur lui nomme (ui-app/src/board/sons.ts) ;
// ici personne ne nous nomme rien, c'est l'interface qui décide : choisir un
// héros, verrouiller une cible, lancer la partie. On réutilise les fichiers
// existants (assets/sounds/, servis à la racine par le moteur) plutôt que d'en
// ajouter : la liste des noms est figée côté moteur, et remplacer un `.wav`
// suffit à changer ce qu'on entend (voir docs/reference/SONS-DECLENCHEURS.md).
//
// Mêmes règles que le plateau, à dessein (ui-app/src/board/sons.ts) :
//   — volume des effets réglable, PARTAGÉ avec le plateau
//     (`marvel-board-volume-sons`, en %, 20 par défaut) ;
//   — rien si l'onglet n'est pas visible ;
//   — au plus 2 sons à la fois (refonte des sons, 07/10/2026) ;
//   — survol des boutons et des tuiles : très bas, jamais en rafale ;
//   — l'échec est silencieux. Le navigateur refuse de jouer avant la première
//     interaction de la page ; inutile de crier, le son suivant passera.
//
// ⚠ LE RÉGLAGE EST CELUI DU PLATEAU, `marvel-board-sons` (board.tsx). Une
// deuxième clé donnerait deux boutons à couper pour un seul silence voulu.

"use strict";

const CLE_SONS = "marvel-board-sons";
const CLE_VOLUME = "marvel-board-volume-sons";
const VOLUME_PAR_DEFAUT = 20;
const MAX_SIMULTANES = 2;
const FACTEUR_SURVOL = 0.35;
const ECART_SURVOL_MS = 80;
/** Ce qui se survole sur cet écran : ses boutons et ses tuiles de choix. */
const SELECTEUR_SURVOL = 'button, [role="button"], .acc-tuile, .tb-carte';

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

/** Au survol de son portrait (`data-hero`), ce héros joue SON son, à la place
 *  du survol générique. Fichier `assets/sounds/<valeur>`, extension comprise. */
const SON_SURVOL_HEROS = {
    wolverine: "heros-wolverine.mp3",
};

const enCours = new Set();
let dernierSurvol = -Infinity;

function actif() {
    try {
        // Actif PAR DÉFAUT, comme le plateau : l'absence de réglage veut dire
        // « je n'ai rien demandé », pas « je veux le silence ».
        return localStorage.getItem(CLE_SONS) !== "off";
    } catch (e) {
        return true;
    }
}

function volume() {
    try {
        const brut = localStorage.getItem(CLE_VOLUME);
        if (brut === null) return VOLUME_PAR_DEFAUT / 100;
        const v = Number(brut);
        return Number.isFinite(v) ? Math.min(100, Math.max(0, v)) / 100 : VOLUME_PAR_DEFAUT / 100;
    } catch (e) {
        return VOLUME_PAR_DEFAUT / 100;
    }
}

function jouer(nom, facteur) {
    if (!nom || !actif()) return false;
    if (document.visibilityState !== "visible") return false;
    for (const a of enCours) if (a.ended || a.paused || a.error) enCours.delete(a);
    if (enCours.size >= MAX_SIMULTANES) return false;
    try {
        const audio = new Audio("/" + (nom.includes(".") ? nom : nom + ".wav"));
        audio.volume = Math.min(1, volume() * facteur);
        audio.addEventListener("ended", () => enCours.delete(audio));
        enCours.add(audio);
        const p = audio.play();
        if (p && p.catch) p.catch(() => enCours.delete(audio));
        return true;
    } catch (e) {
        // Audio indisponible (contexte restreint, mémoire) : le silence est un
        // repli acceptable, une exception non.
        return false;
    }
}

/** Joue un son de la table `SON`. Ne lève jamais. */
export function jouerSon(nom) {
    jouer(nom, 1);
}

// Le survol : écoute déléguée, souris seulement (au doigt, pas de survol), un
// seul son par élément survolé, et pas plus d'un toutes les 80 ms.
let dernierSurvole = null;
document.addEventListener("pointerover", (evenement) => {
    if (evenement.pointerType && evenement.pointerType !== "mouse") return;
    const cible = evenement.target instanceof Element ? evenement.target.closest(SELECTEUR_SURVOL) : null;
    if (cible === dernierSurvole) return;
    dernierSurvole = cible;
    if (!cible || cible.disabled) return;
    const sonHeros = SON_SURVOL_HEROS[cible.getAttribute("data-hero")];
    if (sonHeros) {
        jouer(sonHeros, 1);
        return;
    }
    const t = performance.now();
    if (t - dernierSurvol < ECART_SURVOL_MS) return;
    if (jouer("survol", FACTEUR_SURVOL)) dernierSurvol = t;
});
