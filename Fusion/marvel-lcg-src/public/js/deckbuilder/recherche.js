// Recherche du deckbuilder : module pur, testé par tools/tests-lanceur/recherche.test.mjs.
"use strict";

/** Minuscules, sans accents, apostrophe typographique ramenée à « ' ». */
export function normaliser(texte) {
    return String(texte || "")
        .normalize("NFD").replace(/[̀-ͯ]/g, "")
        .replace(/[’‘]/g, "'")
        .toLowerCase();
}

/** Vrai si la requête figure dans le nom anglais, le nom français officiel,
 *  le texte affiché ou les traits, quelle que soit la langue de l'interface. */
export function correspondRecherche(carte, requete, { nomsFr = {}, nomAffiche = "", texteAffiche = "" } = {}) {
    const voulu = normaliser(requete).trim();
    if (!voulu) return true;
    const nomOfficiel = nomsFr[carte.card_id || carte.id] || "";
    const dedans = [carte.name, nomOfficiel, nomAffiche, texteAffiche, carte.text, ...(carte.traits || [])]
        .map(normaliser).join(" ");
    return dedans.includes(voulu);
}
