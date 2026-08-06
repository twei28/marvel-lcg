// filtres.js — sélection et tri des decks d'un héros. Fonctions PURES, sans
// DOM ni réseau : la refonte React de l'écran de préparation les reprendra
// telles quelles.
"use strict";

/** Minuscules sans accents, pour comparer un nom de deck à une recherche.
    La plage ̀-ͯ est écrite en échappement : un caractère combinant
    posé littéralement dans le fichier serait invisible et illisible. */
function normaliser(texte) {
    return String(texte || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

/**
 * @param {Array} decks  entrées d'index
 * @param {{aspect?: string, tag?: string, texte?: string, masquerIncomplets?: boolean}} criteres
 * @returns {Array} decks retenus, du plus récent au plus ancien
 */
export function filtrer(decks, criteres) {
    const { aspect, tag, texte, masquerIncomplets = true } = criteres || {};
    const recherche = normaliser(texte);
    return (decks || [])
        .filter((d) => (!masquerIncomplets || d.jouable))
        .filter((d) => (!aspect || d.aspect === aspect))
        .filter((d) => (!tag || (d.tags || []).includes(tag)))
        .filter((d) => (!recherche || normaliser(d.nom).includes(recherche)))
        .sort((a, b) => (b.date || "").localeCompare(a.date || "") || b.id - a.id);
}

/** Aspects réellement présents dans une liste, pour ne proposer que ceux-là. */
export function aspectsPresents(decks) {
    return [...new Set((decks || []).map((d) => d.aspect).filter(Boolean))].sort();
}

/** Tags réellement présents, même usage. */
export function tagsPresents(decks) {
    return [...new Set((decks || []).flatMap((d) => d.tags || []))].sort();
}
