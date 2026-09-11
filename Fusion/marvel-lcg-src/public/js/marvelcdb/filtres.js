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
 * @param {{aspect?: string, tag?: string, texte?: string, masquerIncomplets?: boolean,
 *          tri?: "date"|"populaire", classesSeulement?: boolean}} criteres
 * @returns {Array} decks retenus, du plus récent au plus ancien par défaut
 */
export function filtrer(decks, criteres) {
    const { aspect, tag, texte, masquerIncomplets = true,
            tri = "date", classesSeulement = false } = criteres || {};
    const recherche = normaliser(texte);
    return (decks || [])
        .filter((d) => (!masquerIncomplets || d.jouable))
        .filter((d) => (!classesSeulement || d.rang))
        .filter((d) => (!aspect || d.aspect === aspect))
        .filter((d) => (!tag || (d.tags || []).includes(tag)))
        .filter((d) => (!recherche || normaliser(d.nom).includes(recherche)))
        .sort(tri === "populaire" ? parPopularite : parDate);
}

function parDate(a, b) {
    return (b.date || "").localeCompare(a.date || "") || b.id - a.id;
}

/** Le plus populaire d'abord. ⚠ UN DECK SANS RANG N'EST PAS IMPOPULAIRE : il
 *  est seulement absent du relevé, qui ne descend que jusqu'à un certain rang.
 *  Il passe donc APRÈS les classés, et garde entre eux l'ordre chronologique,
 *  au lieu d'être jeté au hasard. */
function parPopularite(a, b) {
    if (a.rang && b.rang) return a.rang - b.rang;
    if (a.rang) return -1;
    if (b.rang) return 1;
    return parDate(a, b);
}

/** Y a-t-il de quoi trier par popularité ? Sert à ne pas proposer un tri qui
 *  ne trierait rien quand le relevé n'a jamais tourné. */
export function aDesRangs(decks) {
    return (decks || []).some((d) => d.rang);
}

/** Aspects réellement présents dans une liste, pour ne proposer que ceux-là. */
export function aspectsPresents(decks) {
    return [...new Set((decks || []).map((d) => d.aspect).filter(Boolean))].sort();
}

/** Tags réellement présents, même usage. */
export function tagsPresents(decks) {
    return [...new Set((decks || []).flatMap((d) => d.tags || []))].sort();
}
