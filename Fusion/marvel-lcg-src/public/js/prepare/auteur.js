// auteur.js — le créateur d'un héros fan-made, affiché entre parenthèses
// derrière son nom (demande du 18/09/2026). Module pur, sans DOM : testé par
// `node --test tools/tests-lanceur/auteur.test.mjs`.
//
// Le créateur vient du champ `custom` de la face héros (cards.json, voir
// GUIDE-CREATION-CONTENU §14). Un héros officiel n'en porte jamais.
"use strict";

/** « Lockjaw » + « Nugget » → « Lockjaw (Nugget) ». Rien pour un officiel,
 *  rien sans créateur, et pas de doublon quand leverLesHomonymes a déjà glissé
 *  le créateur dans le libellé (« Spider-Man (Rainy) »). */
export function nomAvecAuteur(nom, auteur, homebrew) {
    const n = String(nom || "");
    const a = String(auteur || "").trim();
    if (!homebrew || !a) return n;
    if (n.toLowerCase().includes(a.toLowerCase())) return n;
    return `${n} (${a})`;
}

/** Les créateurs d'une liste de héros, chacun une fois, dans l'ordre
 *  alphabétique : « BlueHG + DesignHacker » compte pour deux personnes. Sert
 *  au remerciement affiché sur le filtre fan-made. */
export function createursDe(heroes) {
    const vus = new Map();
    for (const h of heroes || []) {
        if (!h || !h.homebrew || !h.auteur) continue;
        for (const brut of String(h.auteur).split("+")) {
            const nom = brut.trim();
            if (nom && !vus.has(nom.toLowerCase())) vus.set(nom.toLowerCase(), nom);
        }
    }
    return [...vus.values()].sort((a, b) => a.localeCompare(b, undefined, { sensitivity: "base" }));
}

/** Le créateur d'un ensemble de cartes, quand il n'y a pas de doute : la seule
 *  valeur `custom` non vide qu'elles portent toutes. Deux auteurs, ou une
 *  carte officielle mêlée à des cartes maison, et on rend "" — mieux vaut ne
 *  rien attribuer que de se tromper de personne. Le set « Electro » est
 *  exactement ce cas, entre l'officiel et la campagne Web of Deceit. */
export function auteurUnique(customs) {
    let trouve = "";
    for (const brut of customs || []) {
        const a = String(brut || "").trim();
        if (!a) return "";
        if (!trouve) trouve = a;
        else if (trouve !== a) return "";
    }
    return trouve;
}
