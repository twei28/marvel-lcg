// narval.js — la mascotte du moment, cote JEU.
//
// Demande de l'utilisateur, 17/09/2026 : la mascotte change toutes les trois
// heures, dans l'onglet comme sur les pages.
//
// ⚠ JUMEAU DE `site/narval.py`, ET IL DOIT LE RESTER. Le site et le jeu sont
// deux processus, sur deux sous-domaines, qui ne partagent rien : chacun
// calcule le narval de son cote. S'ils divergent, l'onglet et la page
// affichent deux mascottes differentes au meme instant. `site/test_narval.py`
// compare les deux listes et les deux formules, et refuse qu'elles s'ecartent.
//
// ⚠ EN UTC, comme cote site : sur l'heure locale, deux joueurs dans deux
// fuseaux verraient deux mascottes differentes au meme moment.
"use strict";

/** Les mascottes, dans l'ordre de passage. Jumelle de `NARVALS` (narval.py). */
export const NARVALS = ["cap", "magneto", "cyclope", "wolverine", "thor"];

/** Duree d'un passage, en heures. */
export const HEURES = 3;

/** Le numero de la tranche horaire en cours, depuis l'epoque UTC. */
export function tranche(maintenant) {
    const ms = maintenant === undefined ? Date.now() : maintenant;
    return Math.floor(ms / 1000 / (HEURES * 3600));
}

/** Le nom du narval a afficher. */
export function narval(maintenant) {
    const i = ((tranche(maintenant) % NARVALS.length) + NARVALS.length) % NARVALS.length;
    return NARVALS[i];
}

/**
 * L'adresse de son image.
 *
 * ⚠ SANS EXTENSION : le moteur sert les images par leur NOM
 * (`server_files.py`), en cherchant .webp/.jpg/.png dans les dossiers
 * d'images puis `assets/textures`. « /narwhal-cap.png » repondrait 404 ;
 * « /narwhal-cap » trouve le fichier, exactement comme un scan de carte.
 */
export function urlNarval(maintenant) {
    return "/narwhal-" + narval(maintenant);
}
