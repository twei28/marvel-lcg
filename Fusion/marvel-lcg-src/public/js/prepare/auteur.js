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

/** La liste COMMUNE des remerciements (demande du 17/10/2026) : les créateurs de tous
 *  les héros fan-made ET de toutes les extensions fan-made (vilains, sets), chacun une
 *  fois. La même phrase s'affiche sur l'écran des héros et sur celui des méchants : un
 *  nouveau contenu s'ajoute aux deux d'un coup, jamais à un seul. `auteursExtensions` :
 *  les créateurs des extensions fan-made, une chaîne chacun (« A + B » accepté). */
export function createursDeTout(heroes, auteursExtensions) {
    const dEntrees = (auteursExtensions || []).filter(Boolean).map((a) => ({ homebrew: true, auteur: a }));
    return createursDe([...(heroes || []), ...dEntrees]);
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

/** Les créateurs d'extensions que les cartes ne disent pas (champ `custom` vide,
 *  ou set partagé avec des cartes officielles). Clé : le nom entre parenthèses de
 *  l'extension (« Custom (Web of Deceit) » → « Web of Deceit »). Donnés par
 *  l'administrateur le 16/10/2026. */
export const AUTEURS_EXTENSIONS = {
    "web of deceit": "Ripper3",
    "gorr the god butcher": "BlueHG",
    // Le set « Custom (Shredder) » contient les cartes du scénario ET celles du set TMNT : le nom ne retrouve pas le créateur seul (18/10/2026).
    "shredder": "Inkwire",
    // Campagne MC×DC 2026 (demande du 22/10/2026) : « La ville ne dort jamais (MCDC 2026) », et ses défis à part.
    "la ville ne dort jamais": "MCDC 2026",
    "challenges": "MCDC 2026",
};

/** Le créateur d'une extension par son nom, ou "" si on ne le connaît pas. */
export function auteurConnuDeLExtension(nomInterne) {
    return AUTEURS_EXTENSIONS[String(nomInterne || "").trim().toLowerCase()] || "";
}
