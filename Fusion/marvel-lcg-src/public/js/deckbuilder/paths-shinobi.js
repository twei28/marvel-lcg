// paths-shinobi.js — les regles de construction des PATHS SHINOBI (TMNT Shinobi, Inkwire). PUR.
//
// Miroir de `data/shinobi_paths.json` (transcription du livret « Shinobi Path Rulebook » et des 11 dos de Path,
// 17/10/2026) : `tools/tests-lanceur/regles-shinobi.test.mjs` verifie que les deux disent la meme chose.
// Un Path (type imprime PATH) est choisi au deck-building ; il est MIS DE COTE (hors des 40-50), mis en jeu au
// Setup, et lui seul autorise les cartes Shinobi du deck : types Shinobi, UN aspect au choix, cartes Basic.
// Lecture litterale du livret : aucun Path n'est reserve aux heros TMNT (question Q-S3).
"use strict";

export const CLASSES_SHINOBI = ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"];

/** Regles par card_id de Path. `aspects.max` : nombre d'aspects admis ; `libre` : « any combination of aspect
 *  cards » (The Last Ronin) ; `maxExemplaires` : plafond par carte quand il remplace le 3 habituel. */
export const PATHS_SHINOBI = {
    se001: { nom: "Kagemusha", types: ["Ninjutsu"], aspects: { max: 1 }, basic: true },
    se002: { nom: "Onmyodo", types: ["Kuji-Kiri"], aspects: { max: 1 }, basic: true },
    se003: { nom: "Samurai", types: ["Bushido"], aspects: { max: 1 }, basic: true },
    se004: { nom: "Shihan", types: ["Taijutsu"], aspects: { max: 1 }, basic: true },
    se005: { nom: "The Last Ronin", types: ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"], aspects: { max: 4, libre: true },
             basic: true, maxExemplaires: 1 },
    se006: { nom: "Yoshimitsu", types: ["Bushido", "Kuji-Kiri"], aspects: { max: 1 }, basic: true },
    se007: { nom: "Yamabushi", types: ["Kuji-Kiri", "Taijutsu"], aspects: { max: 1 }, basic: true },
    se008: { nom: "Onigari", types: ["Kuji-Kiri", "Ninjutsu"], aspects: { max: 1 }, basic: true },
    se009: { nom: "Ashigaru", types: ["Bushido", "Taijutsu"], aspects: { max: 1 }, basic: true },
    se010: { nom: "Onmitsu", types: ["Ninjutsu", "Taijutsu"], aspects: { max: 1 }, basic: true },
    se011: { nom: "Yojimbo", types: ["Bushido", "Ninjutsu"], aspects: { max: 1 }, basic: true },
};

const parties = (classe) => String(classe || "").split(";").map((x) => x.trim()).filter(Boolean);

/** Les types Shinobi d'une classe (« Bushido;Kuji-Kiri » -> les deux), [] si un seul membre n'est pas Shinobi
 *  (« Hero;Taijutsu » est une signature, pas une carte Shinobi). */
export function typesShinobi(classe) {
    const p = parties(classe);
    return p.length && p.every((x) => CLASSES_SHINOBI.includes(x)) ? p : [];
}

/** Carte SHINOBI (hors Path) : sa classe ne porte QUE des types Shinobi. Les classes Shinobi ne sont ni un
 *  aspect ni « Basic ». */
export function estShinobi(c) {
    return !!c && String(c.type) !== "Path" && typesShinobi(c.class).length > 0;
}

/** Carte PATH choisissable : type PATH et classe Shinobi seulement. Sosaiken (`tj011`, classe « Hero ») est la
 *  Voie PROPRE de Jennika : elle n'est pas dans le pool. */
export function estPath(c) {
    return !!c && String(c.type) === "Path" && typesShinobi(c.class).length > 0;
}

/** Regles du Path `c` (id facultatif) : la table ci-dessus, sinon derivees de la classe imprimee (un Path futur :
 *  types = ses classes, un seul aspect, Basic). */
export function reglesDuPath(c, id) {
    const cle = String(id || (c && (c.card_id || c.id)) || "").split(",")[0];
    if (PATHS_SHINOBI[cle]) return PATHS_SHINOBI[cle];
    return { nom: (c && c.name) || cle, types: typesShinobi(c && c.class), aspects: { max: 1 }, basic: true };
}

/** Voie PROPRE declaree par un heros (`metadata.deckbuilding.path` de son deck de depart) : Jennika et sa
 *  Sosaiken. Meme forme que `reglesDuPath`. */
export function reglesDuPathPropre(hero) {
    const m = hero && hero.deck && hero.deck.metadata;
    const p = m && m.deckbuilding && m.deckbuilding.path;
    if (!p || typeof p !== "object") return null;
    const types = (Array.isArray(p.types) ? p.types : []).filter((x) => CLASSES_SHINOBI.includes(x));
    if (!types.length) return null;
    return {
        nom: p.nom || "Path",
        types,
        aspects: { max: Number.isFinite(Number(p.aspects_max)) ? Number(p.aspects_max) : 1 },
        basic: p.basic !== false,
        propre: true,
    };
}

/** La carte Shinobi `c` est-elle admise par ce Path ? Une Dual l'est des qu'UN de ses types l'est. */
export function admiseParLePath(c, regles) {
    return typesShinobi(c.class).some((t) => regles.types.includes(t));
}
