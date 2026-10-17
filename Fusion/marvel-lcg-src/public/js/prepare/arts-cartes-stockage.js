// arts-cartes-stockage.js : lecture et ecriture, dans le navigateur, du choix
// d'art alternatif des cartes de deck (cle `mc_card_art_v1`, lue aussi par le
// plateau : ui-app/src/board/arts-cartes.ts) et de la case « Ne plus proposer ».
// La logique est dans arts-cartes-choix.js (pure) ; ici, seulement le stockage.
"use strict";

import { CLE_STOCKAGE, CLE_NE_PLUS_PROPOSER, appliquer, codeAffiche, picIdAvecArt, artsDe } from "./arts-cartes-choix.js";

/** La table { card_id officiel -> code } ; {} si le stockage est illisible. */
export function lireChoixCartes() {
    try {
        const brut = window.localStorage.getItem(CLE_STOCKAGE);
        const table = brut ? JSON.parse(brut) : {};
        return table && typeof table === "object" && !Array.isArray(table) ? table : {};
    } catch { return {}; }
}

/** Ecrit un changement `{ id: code | null }` ; rend la nouvelle table. */
export function ecrireChoixCartes(changements) {
    const suite = appliquer(lireChoixCartes(), changements);
    try { window.localStorage.setItem(CLE_STOCKAGE, JSON.stringify(suite)); } catch { /* stockage indisponible */ }
    return suite;
}

export function lireNePlusProposer() {
    try { return window.localStorage.getItem(CLE_NE_PLUS_PROPOSER) === "1"; } catch { return false; }
}

export function ecrireNePlusProposer(valeur) {
    try { window.localStorage.setItem(CLE_NE_PLUS_PROPOSER, valeur ? "1" : "0"); } catch { /* préférence non critique */ }
}

/** L'identifiant d'image à demander pour cette carte de deck, selon le choix
 *  enregistré et le héros du deck (`heros` : card_id de sa face). */
export function picIdDeCarte(id, heros) {
    return artsDe(id).length ? picIdAvecArt(id, codeAffiche(id, lireChoixCartes(), heros)) : String(id);
}
