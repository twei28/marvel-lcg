// Syntaxe courte de la recherche du deckbuilder (« t:avenger c:2 atk>=2 »).
// Module pur, testé par tools/tests-lanceur/deckbuilder-syntaxe.test.mjs.
"use strict";

import { normaliser } from "./recherche.js";

/** Clé tapée (FR ou EN) -> critère. */
const CLES = {
    t: "trait", trait: "trait",
    c: "cout", cout: "cout", cost: "cout",
    a: "aspect", aspect: "aspect",
    p: "pack", pack: "pack",
    ty: "type", type: "type",
    u: "unique", unique: "unique",
    atk: "atk", thw: "thw", def: "def",
    pv: "hp", hp: "hp",
};
const NUMERIQUES = new Set(["cout", "atk", "thw", "def", "hp"]);

/** Noms d'aspects reconnus, FR et EN, vers la classe du moteur. */
const ASPECTS = {
    aggression: "Aggression", agressivite: "Aggression",
    justice: "Justice",
    leadership: "Leadership", commandement: "Leadership",
    protection: "Protection",
    pool: "'Pool",
    basic: "Basic", basique: "Basic",
    determination: "Determination",
    venomized: "Venomized",
};
const TYPES = {
    ally: "Ally", allie: "Ally",
    event: "Event", evenement: "Event",
    upgrade: "Upgrade", amelioration: "Upgrade",
    support: "Support", soutien: "Support",
    resource: "Resource", ressource: "Resource",
};

const OUI = new Set(["1", "oui", "yes", "true", "o", "y"]);
const NON = new Set(["0", "non", "no", "false", "n"]);

/** Découpe en mots, en gardant ensemble ce qui est entre guillemets. */
function mots(requete) {
    return String(requete || "").match(/(?:[^\s"]+|"[^"]*")+/g) || [];
}

/** Retrouve la valeur complète d'un nom (« lead » -> Leadership). */
function parPrefixe(table, valeur) {
    const v = normaliser(valeur);
    if (!v) return null;
    if (table[v]) return table[v];
    const cle = Object.keys(table).find((k) => k.startsWith(v));
    return cle ? table[cle] : null;
}

/**
 * Analyse une requête. Rend les critères reconnus, le texte libre restant et
 * les morceaux refusés (une clé connue avec une valeur illisible).
 */
export function analyser(requete) {
    const criteres = [];
    const libres = [];
    const erreurs = [];
    for (const mot of mots(requete)) {
        const m = mot.match(/^([a-zA-Z]+)(>=|<=|:|=|>|<)(.*)$/);
        const cle = m && CLES[m[1].toLowerCase()];
        if (!cle) { libres.push(mot.replace(/"/g, "")); continue; }
        const op = m[2] === ":" ? "=" : m[2];
        const brut = m[3].replace(/"/g, "").trim();
        if (!brut) { erreurs.push(mot); continue; }
        if (NUMERIQUES.has(cle)) {
            if (cle === "cout" && /^x$/i.test(brut) && op === "=") { criteres.push({ cle, op, valeur: "X" }); continue; }
            const n = Number(brut);
            if (!Number.isFinite(n)) { erreurs.push(mot); continue; }
            criteres.push({ cle, op, valeur: n });
            continue;
        }
        if (op !== "=") { erreurs.push(mot); continue; }
        if (cle === "aspect") {
            const a = parPrefixe(ASPECTS, brut);
            if (!a) { erreurs.push(mot); continue; }
            criteres.push({ cle, op, valeur: a });
        } else if (cle === "type") {
            const ty = parPrefixe(TYPES, brut);
            if (!ty) { erreurs.push(mot); continue; }
            criteres.push({ cle, op, valeur: ty });
        } else if (cle === "unique") {
            const v = normaliser(brut);
            if (OUI.has(v)) criteres.push({ cle, op, valeur: true });
            else if (NON.has(v)) criteres.push({ cle, op, valeur: false });
            else erreurs.push(mot);
        } else {
            criteres.push({ cle, op, valeur: normaliser(brut) });
        }
    }
    return { criteres, texte: libres.join(" ").trim(), erreurs };
}

/** Le nombre imprimé d'une valeur de carte (« 2* » -> 2), ou null. */
export function nombreDe(valeur) {
    const m = String(valeur ?? "").match(/^\s*(\d+)/);
    return m ? Number(m[1]) : null;
}

function compare(a, op, b) {
    if (op === ">=") return a >= b;
    if (op === "<=") return a <= b;
    if (op === ">") return a > b;
    if (op === "<") return a < b;
    return a === b;
}

const STAT = { atk: "ATK", thw: "THW", def: "DEF", hp: "HP" };

/** Vrai si la carte satisfait UN critère. */
export function satisfait(carte, critere) {
    const desc = carte.desc || {};
    const { cle, op, valeur } = critere;
    if (cle === "trait") return (carte.traits || []).some((tr) => normaliser(tr).replace(/\.$/, "").includes(valeur));
    if (cle === "pack") return normaliser(carte.package_name).includes(valeur);
    if (cle === "aspect") return carte.class === valeur;
    if (cle === "type") return carte.type === valeur;
    if (cle === "unique") return /^\*/.test(String(carte.name || "")) === valeur;
    if (cle === "cout") {
        const brut = String(carte.cost ?? desc.Cost ?? "").trim();
        if (valeur === "X") return /^x$/i.test(brut);
        const n = nombreDe(brut);
        return n !== null && compare(n, op, valeur);
    }
    const n = nombreDe(desc[STAT[cle]]);
    return n !== null && compare(n, op, valeur);
}

/** Vrai si la carte satisfait TOUS les critères. */
export function satisfaitTout(carte, criteres) {
    return criteres.every((c) => satisfait(carte, c));
}
