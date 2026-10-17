// arts-cartes-choix.js : le choix d'art alternatif des CARTES DE DECK.
//
// Regle de l'utilisateur (17/10/2026) : si SEULE l'image d'une carte change,
// c'est un art alternatif de l'officielle, propose a tous ; si quoi que ce soit
// d'autre change (nom, traits, texte, cout, ressource, unicite, bandeau), c'est
// une carte EXCLUSIVE a la serie (heros TMNT seulement).
//
// Le choix vit dans UNE table `{ card_id officiel: code }` (cle de stockage
// `mc_card_art_v1`, lue aussi par le plateau) :
//   - absent    : le DEFAUT de la serie (art TMNT pour un heros TMNT, sinon
//                 l'officielle) ;
//   - « standard » : l'officielle, quel que soit le heros (choix explicite) ;
//   - « tmnt »  : l'art TMNT, quel que soit le heros.
//
// Module PUR (ni DOM ni stockage). Les tables (`ARTS_CARTES`, `SERIES_ARTS`)
// viennent de data/arts_alternatifs.json via tools/generer_arts_cartes.py ;
// chaque fonction les accepte en parametre pour etre testee sans elles.
// Test : `node --test tools/tests-lanceur/arts-cartes-choix.test.mjs`.
"use strict";

import { ARTS_CARTES, SERIES_ARTS, ORIGINES_CARTES } from "./arts-cartes-table.js";

export const STANDARD = "standard";
export const CLE_STOCKAGE = "mc_card_art_v1";
export const CLE_NE_PLUS_PROPOSER = "mc_card_art_noask_v1";

/** Identifiant de carte sans suffixe de liste (« 56013,56013 » -> « 56013 »). */
export function cleCarte(id) {
    return String(id || "").split(",")[0];
}

/** L'officielle d'une carte : pour une réimpression identique (`full_link`),
 *  l'impression d'origine, dont l'image et le choix valent pour toutes. */
export function origine(id, origines = ORIGINES_CARTES) {
    const cle = cleCarte(id);
    return origines[cle] || cle;
}

/** Clé de héros : numéro de carte sans suffixe de face (« tl001a » -> « tl001 »). */
export function cleHeros(heroCardId) {
    return cleCarte(heroCardId).replace(/[a-z]$/, "");
}

/** Les arts alternatifs d'une carte officielle ([] si elle n'en a pas). */
export function artsDe(id, arts = ARTS_CARTES) {
    return arts[origine(id)] || [];
}

/** La série d'art d'un héros (« tmnt »), ou null. `heros` : card_id de sa
 *  face (« tl001a ») OU identifiant de deck de départ (« leonardo »). */
export function serieDuHeros(heros, series = SERIES_ARTS) {
    const brut = cleCarte(heros);
    const cle = cleHeros(brut);
    for (const [code, s] of Object.entries(series)) {
        if ((s.heros_cartes || []).includes(cle) || (s.heros_ids || []).includes(brut)) return code;
    }
    return null;
}

/** Le code appliqué quand aucun choix n'est enregistré : celui de la série du
 *  héros s'il existe pour cette carte, sinon l'officielle. */
export function codeParDefaut(id, heros, arts = ARTS_CARTES, series = SERIES_ARTS) {
    const serie = serieDuHeros(heros, series);
    return serie && artsDe(id, arts).includes(serie) ? serie : STANDARD;
}

/** Le code que la carte AFFICHE : le choix enregistré s'il est valable, sinon le défaut. */
export function codeAffiche(id, choix, heros, arts = ARTS_CARTES, series = SERIES_ARTS) {
    const voulu = choix && choix[origine(id)];
    if (voulu === STANDARD) return STANDARD;
    if (voulu && artsDe(id, arts).includes(voulu)) return voulu;
    return codeParDefaut(id, heros, arts, series);
}

/** Identifiant d'image à demander (« 56013_tmnt ») : l'officielle si « standard ». */
export function picIdAvecArt(id, code) {
    const base = origine(id);
    return code && code !== STANDARD ? `${base}_${code}` : base;
}

/** Les changements à écrire pour ce choix, au format des hérauts :
 *  `null` efface la clé (retour au défaut). */
export function changementsPourCarte(id, code) {
    const cle = origine(id);
    if (!cle) return {};
    return { [cle]: code ? code : null };
}

/** Applique des changements à une table, sans la modifier : une NOUVELLE table. */
export function appliquer(choix, changements) {
    const suite = { ...(choix || {}) };
    for (const [cle, code] of Object.entries(changements || {})) {
        if (code === null) delete suite[cle]; else suite[cle] = code;
    }
    return suite;
}

/** Les cartes d'un deck qui ont un art alternatif, une fois chacune, dans
 *  l'ordre du deck. `ids` : liste d'identifiants (doublons permis). */
export function cartesAvecArt(ids, arts = ARTS_CARTES) {
    const vus = new Set();
    const out = [];
    for (const brut of ids || []) {
        const id = origine(brut);
        if (!id || vus.has(id) || artsDe(id, arts).length === 0) continue;
        vus.add(id);
        out.push(id);
    }
    return out;
}

/** Les choix à afficher dans la fenêtre : pour chaque carte, ses codes
 *  proposés (officielle d'abord), le code affiché et le nombre d'exemplaires. */
export function lignesDeChoix(ids, choix, heros, arts = ARTS_CARTES, series = SERIES_ARTS) {
    const nombre = new Map();
    for (const brut of ids || []) nombre.set(origine(brut), (nombre.get(origine(brut)) || 0) + 1);
    return cartesAvecArt(ids, arts).map((id) => ({
        id,
        exemplaires: nombre.get(id),
        codes: [STANDARD, ...artsDe(id, arts)],
        affiche: codeAffiche(id, choix, heros, arts, series),
    }));
}

/** Faut-il poser la question à la sélection d'un deck ? Oui si le deck a au
 *  moins une carte à art alternatif ET que « ne plus proposer » n'est pas coché. */
export function doitProposer(ids, nePlusProposer, arts = ARTS_CARTES) {
    return !nePlusProposer && cartesAvecArt(ids, arts).length > 0;
}

/* ---------------- Cartes exclusives ---------------- */

/** La série qui RÉSERVE ce set (« TMNT Aggression » -> « tmnt »), ou null. */
export function serieExclusive(setName, series = SERIES_ARTS) {
    for (const [code, s] of Object.entries(series)) {
        if ((s.sets_exclusifs || []).includes(setName)) return code;
    }
    return null;
}

/** Cette carte est-elle refusée dans le deck de ce héros ? C'est le cas d'une
 *  carte exclusive à une série dont le héros ne fait pas partie. */
export function exclusiveRefusee(setName, heros, series = SERIES_ARTS) {
    const serie = serieExclusive(setName, series);
    return !!serie && serieDuHeros(heros, series) !== serie;
}
