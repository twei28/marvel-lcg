// Filtres et tris de l'éditeur de deck. Module pur : ce qui dépend de la page
// (texte français, mots-clés, ressources) arrive par `ctx`.
// Testé par tools/tests-lanceur/deckbuilder-filtres.test.mjs.
"use strict";

import { analyser, satisfaitTout, nombreDe } from "./syntaxe.js";
import { normaliser } from "./recherche.js";

export const COUTS = ["0", "1", "2", "3", "4", "5+", "X"];
export const PALIERS_STAT = ["0", "1", "2", "3", "4+"];
export const STATS = [
    { cle: "atk", desc: "ATK", libelle: "ATK" },
    { cle: "thw", desc: "THW", libelle: "THW" },
    { cle: "def", desc: "DEF", libelle: "DEF" },
    { cle: "hp", desc: "HP", libelle: "PV" },
];
export const ORDRE_TYPES = ["Ally", "Event", "Upgrade", "Support", "Resource", "PlayerSideScheme", "Player_Side_Scheme"];
const ORDRE_CLASSES = ["Hero", "Aggression", "Justice", "Leadership", "Protection", "'Pool", "Determination", "Venomized", "Basic", "Campaign"];

const ASPECTS_FILTRE = ["Aggression", "Justice", "Leadership", "Protection", "'Pool", "Determination", "Venomized"];
/** Carte DOUBLE ASPECT (« Aggression;Justice », pack tmnt_aspect_dual) : ses deux
 *  aspects, pour qu'elle apparaisse sous l'un ET sous l'autre filtre. Vide pour
 *  toute autre classe (« Hero;Aggression » reste une signature). */
function classesDoubles(carte) {
    const parts = String((carte && carte.class) || "").split(";").map((x) => x.trim()).filter(Boolean);
    return parts.length >= 2 && parts.every((x) => ASPECTS_FILTRE.includes(x)) ? parts : [];
}

export function filtresVides() {
    return {
        texte: "",
        aspects: new Set(), types: new Set(), couts: new Set(),
        ressources: new Set(), motsCles: new Set(),
        traits: new Set(), traitsMode: "ou",
        packs: new Set(),
        stats: { atk: new Set(), thw: new Set(), def: new Set(), hp: new Set() },
        unique: false,
        fanMade: false,
    };
}

/** Palier de coût d'une carte : « 0 » à « 4 », « 5+ », « X », ou "" sans coût. */
export function cleCout(carte) {
    const brut = String(carte.cost ?? (carte.desc && carte.desc.Cost) ?? "").trim();
    if (/^x$/i.test(brut)) return "X";
    const n = nombreDe(brut);
    if (n === null) return "";
    return n >= 5 ? "5+" : String(n);
}

/** Palier d'une statistique : « 0 » à « 3 », « 4+ », ou "" si la carte n'en a pas. */
export function cleStat(valeur) {
    const n = nombreDe(valeur);
    if (n === null) return "";
    return n >= 4 ? "4+" : String(n);
}

/** Aspects cochés au départ : ceux du deck, plus Basique (et les signatures
 *  pour Stan Lee). Un deck sans aspect ne filtre rien. */
export function aspectsParDefaut(aspectsDuDeck, stanLee = false) {
    const liste = [...(aspectsDuDeck || [])];
    if (!liste.length) return new Set();
    return new Set([...(stanLee ? ["Hero"] : []), ...liste, "Basic"]);
}

/**
 * Vrai si la carte passe tous les filtres.
 * ctx : { ressourcesDe(carte) -> lettres, motsClesDe(carte) -> noms,
 *         correspondTexte(carte, texte) -> bool }
 */
export function passeFiltres(carte, f, ctx) {
    if (!f.fanMade && carte.custom) return false;
    if (f.aspects.size && !f.aspects.has(carte.class) && !classesDoubles(carte).some((a) => f.aspects.has(a))) return false;
    if (f.types.size && !f.types.has(carte.type)) return false;
    if (f.couts.size && !f.couts.has(cleCout(carte))) return false;
    if (f.ressources.size && !ctx.ressourcesDe(carte).some((l) => f.ressources.has(l))) return false;
    if (f.motsCles.size) {
        const siens = ctx.motsClesDe(carte);
        if (![...f.motsCles].every((mot) => siens.includes(mot))) return false;
    }
    if (f.traits.size) {
        const siens = new Set((carte.traits || []).map((tr) => normaliser(tr).replace(/\.$/, "")));
        const voulus = [...f.traits].map((tr) => normaliser(tr).replace(/\.$/, ""));
        const ok = f.traitsMode === "et" ? voulus.every((v) => siens.has(v)) : voulus.some((v) => siens.has(v));
        if (!ok) return false;
    }
    if (f.packs.size && !f.packs.has(carte.package_name)) return false;
    for (const s of STATS) {
        const voulus = f.stats[s.cle];
        if (voulus && voulus.size && !voulus.has(cleStat((carte.desc || {})[s.desc]))) return false;
    }
    if (f.unique && !/^\*/.test(String(carte.name || ""))) return false;
    if (f.texte) {
        const { criteres, texte } = analyser(f.texte);
        if (!satisfaitTout(carte, criteres)) return false;
        if (texte && !ctx.correspondTexte(carte, texte)) return false;
    }
    return true;
}

/** Nombre de filtres actifs (pour « Filtres (2) » sur mobile). */
export function nombreFiltresActifs(f) {
    let n = 0;
    for (const s of [f.aspects, f.types, f.couts, f.ressources, f.motsCles, f.traits, f.packs]) if (s.size) n++;
    for (const s of STATS) if (f.stats[s.cle].size) n++;
    if (f.unique) n++;
    if (f.texte.trim()) n++;
    return n;
}

function rangClasse(c) {
    const i = ORDRE_CLASSES.indexOf(c);
    return i < 0 ? ORDRE_CLASSES.length : i;
}
function rangType(ty) {
    const i = ORDRE_TYPES.indexOf(ty);
    return i < 0 ? ORDRE_TYPES.length : i;
}
/** Coût pour un tri : sans coût en dernier, X juste avant. */
function rangCout(carte) {
    const k = cleCout(carte);
    if (k === "") return 99;
    if (k === "X") return 98;
    return nombreDe(String(carte.cost ?? (carte.desc && carte.desc.Cost)));
}
const nomTri = (c) => String(c.name || "").replace(/^\*\s*/, "");

/** Comparateur de cartes : `cle` vaut aspect, nom, cout, type ou pack. */
export function comparateur(cle, nomAffiche = nomTri) {
    const parNom = (a, b) => nomAffiche(a).localeCompare(nomAffiche(b));
    if (cle === "nom") return parNom;
    if (cle === "cout") return (a, b) => (rangCout(a) - rangCout(b)) || parNom(a, b);
    if (cle === "type") return (a, b) => (rangType(a.type) - rangType(b.type)) || (rangCout(a) - rangCout(b)) || parNom(a, b);
    if (cle === "pack") return (a, b) => String(a.package_name || "").localeCompare(String(b.package_name || "")) || (rangCout(a) - rangCout(b)) || parNom(a, b);
    return (a, b) => (rangClasse(a.class) - rangClasse(b.class)) || (rangCout(a) - rangCout(b)) || parNom(a, b);
}

/**
 * Range les lignes du deck en groupes selon `cle`.
 * lignes : [{ id, n, carte }] ; libelle(cle, valeur) -> titre du groupe.
 * Rend [{ valeur, titre, total, lignes }], dans l'ordre du tri.
 */
export function grouperDeck(lignes, cle, libelle = (k, v) => String(v), nomAffiche = nomTri) {
    const valeurDe = (c) => {
        if (cle === "type") return c.type || "";
        if (cle === "cout") return cleCout(c) || "—";
        if (cle === "aspect") return c.class || "";
        if (cle === "pack") return c.package_name || "";
        return "";
    };
    const groupes = new Map();
    for (const l of lignes) {
        const v = valeurDe(l.carte);
        if (!groupes.has(v)) groupes.set(v, []);
        groupes.get(v).push(l);
    }
    const ordreValeurs = (a, b) => {
        if (cle === "type") return rangType(a) - rangType(b);
        if (cle === "aspect") return rangClasse(a) - rangClasse(b);
        if (cle === "cout") return [...COUTS, "—"].indexOf(a) - [...COUTS, "—"].indexOf(b);
        return String(a).localeCompare(String(b));
    };
    const interne = cle === "nom" ? comparateur("nom", nomAffiche) : comparateur("cout", nomAffiche);
    return [...groupes.entries()].sort((a, b) => ordreValeurs(a[0], b[0])).map(([valeur, ls]) => ({
        valeur,
        titre: libelle(cle, valeur),
        total: ls.reduce((s, l) => s + l.n, 0),
        lignes: [...ls].sort((x, y) => interne(x.carte, y.carte)),
    }));
}

/** Histogramme des coûts 0 à 5+ (le X et les cartes sans coût n'y figurent pas). */
export function courbeDesCouts(lignes) {
    const paliers = ["0", "1", "2", "3", "4", "5+"];
    const compte = Object.fromEntries(paliers.map((p) => [p, 0]));
    for (const { n, carte } of lignes) {
        const k = cleCout(carte);
        if (k in compte) compte[k] += n;
    }
    return paliers.map((p) => ({ palier: p, total: compte[p] }));
}
