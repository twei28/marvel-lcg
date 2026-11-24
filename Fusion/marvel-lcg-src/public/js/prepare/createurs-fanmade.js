// createurs-fanmade.js — les créateurs de contenu fan-made de la page « Crédits »
// (26/10/2026). Module pur, sans DOM : testé par
// `node --test tools/tests-lanceur/createurs-fanmade.test.mjs`.
//
// La liste n'est JAMAIS écrite à la main : elle se lit sur le champ `custom` des
// cartes (cards.json, voir GUIDE-CREATION-CONTENU §14), le même que la grille des
// héros fan-made. Un nouveau pack se déclare donc une fois et paraît ici.
"use strict";

import { separerCreateurs } from "./auteur.js";

/** Toutes les cartes à plat : `/get_cards_json` rend { pack: [cartes] }, un test
 *  peut aussi passer directement une liste. */
export function aplatirCartes(brut) {
    if (!brut) return [];
    if (Array.isArray(brut)) return brut.filter((c) => c && typeof c === "object");
    const cartes = [];
    for (const groupe of Object.values(brut)) {
        if (Array.isArray(groupe)) for (const c of groupe) if (c && typeof c === "object") cartes.push(c);
    }
    return cartes;
}

/** Le nom lisible d'un contenu : le set de la carte sans « Nemesis » ni
 *  « Deterrence » (le set némésis d'un héros se crédite avec le héros). Une carte
 *  sans set (cartes d'aspect, modules) prend le nom du pack, mis en forme. */
export function libelleDuContenu(setName, clePack) {
    const set = String(setName || "").trim().replace(/\s+(Nemesis|Deterrence)$/i, "").trim();
    if (set) return set;
    return String(clePack || "")
        .split("_")
        .filter(Boolean)
        .map((m) => m.charAt(0).toUpperCase() + m.slice(1))
        .join(" ");
}

const comparer = (a, b) => a.localeCompare(b, undefined, { sensitivity: "base" });

/** Quelle écriture garder : celle qui a l'apostrophe ou le trait d'union (« Ch'od »,
 *  « Anti-Venom »), à défaut la plus longue. */
const ecriture = (libelle) => (libelle.match(/['’-]/g) || []).length * 100 + libelle.length;

/** La clé de comparaison d'un contenu : sans accents, apostrophes, tirets ni espaces,
 *  pour que « Ch'od » et « Chod », « Agent Anti Venom » et « Agent Anti-Venom »
 *  ne fassent qu'une ligne (deux orthographes du même set dans cards.json). */
const cleDeContenu = (libelle) => libelle.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]/g, "");

/** [{ createur, contenus: [...] }], triés par créateur puis par contenu. Un
 *  créateur écrit « X and Y » est compté pour X ET pour Y. Les cartes sans
 *  `custom` (les officielles) n'y sont pas. */
export function creditsParCreateur(brut) {
    const parCreateur = new Map(); // clé minuscule → { createur, contenus: Map(clé minuscule → libellé) }
    const groupes = Array.isArray(brut) ? { "": brut } : brut || {};
    for (const [clePack, liste] of Object.entries(groupes)) {
        if (!Array.isArray(liste)) continue;
        for (const carte of liste) {
            if (!carte || typeof carte !== "object" || !carte.custom) continue;
            const contenu = libelleDuContenu(carte.set_name, clePack);
            if (!contenu) continue;
            for (const nom of separerCreateurs(carte.custom)) {
                const cle = nom.toLowerCase();
                if (!parCreateur.has(cle)) parCreateur.set(cle, { createur: nom, contenus: new Map() });
                const entree = parCreateur.get(cle);
                const cleContenu = cleDeContenu(contenu);
                const connu = entree.contenus.get(cleContenu);
                // Deux orthographes : on garde la plus complète (« Ch'od » plutôt que « Chod »).
                if (!connu || ecriture(contenu) > ecriture(connu)) entree.contenus.set(cleContenu, contenu);
            }
        }
    }
    return [...parCreateur.values()]
        .map((e) => ({ createur: e.createur, contenus: [...e.contenus.values()].sort(comparer) }))
        .sort((a, b) => comparer(a.createur, b.createur));
}
