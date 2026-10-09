// Quelles lignes du deck causent les problèmes que signale validerDeck
// (regles.js) ? Le verdict reste celui de regles.js : ce module ne fait que
// désigner les cartes à souligner. Testé par deckbuilder-fautives.test.mjs.
"use strict";

const titre = (c) => String((c && c.name) || "").replace(/^\*\s*/, "").trim();

/** Les noms qu'un message cite : « « X » » ou une liste après « : ». */
function nomsCites(probleme) {
    const noms = new Set();
    for (const m of probleme.matchAll(/«\s*([^»]+?)\s*»/g)) noms.add(m[1].replace(/\s*\(.*\)$/, "").trim());
    const liste = probleme.split(/\s:\s|:\s/).slice(1).join(": ");
    for (const morceau of liste.split(/,\s*/)) {
        const nom = morceau.replace(/^\*\s*/, "").replace(/\s+[—–]\s.*$/, "").trim();
        if (nom) noms.add(nom);
    }
    return noms;
}

/**
 * @param {Object} o
 * @param {Iterable} o.choisies   paires [id, n]
 * @param {Function} o.carte      id -> carte
 * @param {Object}   o.verdict    résultat de validerDeck
 * @param {Object}   o.regle      reglesAspect(hero) : { max }
 * @param {Array}    [o.neutres]  classes qui ne comptent pas comme aspect
 * @returns {Set} identifiants des cartes à souligner
 */
export function cartesFautives({ choisies, carte, verdict, regle, neutres = ["Basic", "Campaign", "Hero"] }) {
    const fautives = new Set();
    if (!verdict || verdict.ok) return fautives;
    const cites = new Set();
    for (const p of verdict.problemes || []) for (const nom of nomsCites(p)) cites.add(nom);
    const lignes = [...choisies].map(([id, n]) => ({ id, n, c: carte(id) })).filter((l) => l.c);
    for (const l of lignes) if (cites.has(titre(l.c)) || cites.has(l.c.name)) fautives.add(l.id);
    const aspects = verdict.aspects || [];
    if (regle && aspects.length > regle.max) {
        const parAspect = new Map();
        for (const l of lignes) {
            if (!aspects.includes(l.c.class) || neutres.includes(l.c.class)) continue;
            parAspect.set(l.c.class, (parAspect.get(l.c.class) || 0) + l.n);
        }
        const gardes = new Set([...parAspect.entries()].sort((a, b) => b[1] - a[1]).slice(0, regle.max).map(([a]) => a));
        for (const l of lignes) if (parAspect.has(l.c.class) && !gardes.has(l.c.class)) fautives.add(l.id);
    }
    return fautives;
}
