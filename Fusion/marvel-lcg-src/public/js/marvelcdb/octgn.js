// Import d'un deck OCTGN (.o8d), 16/10/2026.
//
// Un .o8d est un XML : `<card qty="3" id="<GUID>">Nom anglais</card>`, une ligne par
// carte, sans distinguer le heros ni sa signature. Chaque ligne est ramenee a un
// code de carte du jeu : d'abord par le GUID (table data/octgn_guids.json, tiree de
// MarvelCDB et MC4DB par tools/octgn_guids.py), puis par le NOM anglais quand le GUID
// est inconnu ou que son code n'existe pas chez nous. Ce qui n'est retrouve d'aucune
// facon est RENDU a l'appelant, jamais ignore en silence.
//
// Le resultat a la forme d'un deck MarvelCDB (`slots`), pour passer par la meme
// conversion (conversion.js) : les cartes signature d'un autre heros sont ecartees
// a ce moment-la, comme pour un lien.
"use strict";

const ENTITES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'" };

function decoder(texte) {
    return String(texte).replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
        if (e[0] === "#") {
            const n = e[1].toLowerCase() === "x" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
            return Number.isFinite(n) ? String.fromCodePoint(n) : m;
        }
        return ENTITES[e.toLowerCase()] ?? m;
    });
}

/** Les lignes de carte d'un .o8d. Rend null si ce n'est pas un deck OCTGN lisible. */
export function lireO8d(texte) {
    const s = String(texte || "");
    if (!/<deck[\s>]/i.test(s)) return null;
    const cartes = [];
    const re = /<card\b([^>]*)>([\s\S]*?)<\/card>/gi;
    let m;
    while ((m = re.exec(s))) {
        const attr = (nom) => { const a = m[1].match(new RegExp(`\\b${nom}="([^"]*)"`, "i")); return a ? a[1] : ""; };
        const qte = parseInt(attr("qty"), 10);
        if (!Number.isFinite(qte) || qte < 1) continue;
        cartes.push({ qte, guid: attr("id").toLowerCase(), nom: decoder(m[2]).trim() });
    }
    return cartes.length ? { cartes } : null;
}

/** Index nom anglais -> code, parmi les cartes OFFICIELLES (5 chiffres), la plus ancienne gagnant. */
export function indexParNom(toutes) {
    const idx = new Map();
    for (const c of toutes) {
        const code = c && c.card_id;
        if (!c || !c.name || !/^\d{5}$/.test(String(code))) continue;
        const cle = String(c.name).trim().toLowerCase();
        if (!idx.has(cle) || String(code) < idx.get(cle)) idx.set(cle, String(code));
    }
    return idx;
}

/**
 * @param {{cartes: Array<{qte:number, guid:string, nom:string}>}} deck  rendu de lireO8d
 * @param {{parGuid: Object<string,string>, existe: (code:string)=>boolean, parNom: Map<string,string>}} sources
 * @returns {{slots: Object<string,number>, inconnues: Array<{qte:number, nom:string}>, total:number}}
 */
export function versSlots(deck, { parGuid, existe, parNom }) {
    const slots = {};
    const inconnues = [];
    let total = 0;
    for (const { qte, guid, nom } of deck.cartes) {
        total += qte;
        let code = parGuid[guid];
        if (!code || !existe(code)) code = parNom.get(nom.toLowerCase());
        if (!code) { inconnues.push({ qte, nom }); continue; }
        slots[code] = (slots[code] || 0) + qte;
    }
    return { slots, inconnues, total };
}
