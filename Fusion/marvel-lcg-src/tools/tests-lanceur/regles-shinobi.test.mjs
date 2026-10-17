// Tests des regles de construction SHINOBI (TMNT Shinobi, Inkwire, prefixes sb sj sa sh sc se), 17/10/2026.
//
//     node --test tools/tests-lanceur/regles-shinobi.test.mjs
//
// Livret « Shinobi Path Rulebook » p.5 : « Follow your Path deck-building rules in conjunction with the standard
// deck-building rules. » Ce que ce fichier prouve :
//  - le miroir JS des regles des Paths (paths-shinobi.js) dit EXACTEMENT ce que dit la transcription
//    data/shinobi_paths.json, et le catalogue (data/cards.json) porte bien les 11 Paths ;
//  - sans Path, AUCUNE carte Shinobi ; un seul Path ; les types Shinobi autorises sont ceux du Path (une carte
//    DUAL est admise des qu'UN de ses deux types l'est) ; UN aspect au choix (The Last Ronin : combinaison libre) ;
//    les cartes Basic restent permises ; 3 exemplaires de chaque carte Shinobi (sauf unique ; Last Ronin : 1 de toute
//    carte) ; le Path ne compte pas dans les 40-50 ;
//  - les classes Shinobi ne sont NI des aspects NI Basic : un deck Shinobi + un aspect n'a qu'UN aspect ;
//  - Jennika (Voie PROPRE, `metadata.deckbuilding.path`) n'a besoin d'aucun Path choisi, n'admet aucun aspect, et ne
//    peut pas en prendre un second.
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { estCarteJoueur, validerDeck, classeDeConstruction } from "../../public/js/deckbuilder/regles.js";
import { PATHS_SHINOBI, CLASSES_SHINOBI, typesShinobi, estShinobi, estPath, reglesDuPath, admiseParLePath } from "../../public/js/deckbuilder/paths-shinobi.js";
import { filtresVides, passeFiltres } from "../../public/js/deckbuilder/filtres.js";

const RACINE = new URL("../../", import.meta.url);
const lire = (chemin) => JSON.parse(fs.readFileSync(new URL(chemin, RACINE), "utf-8"));
const DONNEES = lire("data/shinobi_paths.json");

/* ----------------------------------------------------------------- catalogue de test ---- */
const CATALOGUE = {
    // Paths (classes = leurs types Shinobi, comme dans data/cards.json)
    se001: { name: "Kagemusha", class: "Ninjutsu", type: "Path", desc: { Permanent: "1" } },
    se003: { name: "Samurai", class: "Bushido", type: "Path", desc: { Permanent: "1" } },
    se004: { name: "Shihan", class: "Taijutsu", type: "Path", desc: { Permanent: "1" } },
    se005: { name: "* The Last Rōnin", class: "Bushido;Kuji-Kiri;Ninjutsu;Taijutsu", type: "Path", desc: { Permanent: "1" } },
    se009: { name: "Ashigaru", class: "Bushido;Taijutsu", type: "Path", desc: { Permanent: "1" } },
    // Voie PROPRE de Jennika : classe « Hero », jamais dans le pool
    tj011: { name: "Sōsaiken", class: "Hero", type: "Path", desc: { Permanent: "1" } },
    // Une signature de Jennika (classe « Hero;Taijutsu ») : PAS une carte Shinobi
    tj004: { name: "Decisive Strike", class: "Hero;Taijutsu", type: "Event", desc: {} },
    // Shinobi
    uniq: { name: "* Hitodama", class: "Ninjutsu;Taijutsu", type: "Event", desc: {} },
    dualBK: { name: "Nendō", class: "Bushido;Kuji-Kiri", type: "Event", desc: {} },
    dualBN: { name: "Omawari", class: "Bushido;Ninjutsu", type: "Event", desc: {} },
    dualNT: { name: "Kenbu", class: "Ninjutsu;Taijutsu", type: "Event", desc: {} },
    dualKT: { name: "Yomi", class: "Kuji-Kiri;Taijutsu", type: "Event", desc: {} },
};
for (const cls of CLASSES_SHINOBI) {
    for (let i = 1; i <= 9; i++) CATALOGUE[`${cls}${i}`] = { name: `${cls} ${i}`, class: cls, type: "Event", desc: {} };
}
for (const asp of ["Aggression", "Justice", "Leadership", "Protection"]) {
    for (let i = 1; i <= 9; i++) CATALOGUE[`${asp}${i}`] = { name: `${asp} ${i}`, class: asp, type: "Event", desc: {} };
}
for (let i = 1; i <= 9; i++) CATALOGUE[`basic${i}`] = { name: `Basique ${i}`, class: "Basic", type: "Event", desc: {} };

const carte = (id) => CATALOGUE[id];
const heros = (id, extra = {}) => ({ id, name: id, deck: { hero_deck: Array(15).fill("sig"), ...extra } });
const JENNIKA = heros("jennika", {
    metadata: { deckbuilding: { path: { nom: "Sosaiken", types: ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"], aspects_max: 0, basic: true } } },
});

/** 15 signatures + 25 choisies : `extra`, complete avec des cartes de `fond` (3 exemplaires par titre au plus). */
function choisies(extra, fond) {
    const m = new Map(Object.entries(extra));
    let reste = 25 - Object.entries(extra).filter(([id]) => !id.startsWith("se") && id !== "tj011").reduce((s, [, n]) => s + n, 0);
    for (let i = 1; reste > 0; i++) {
        const n = Math.min(3, reste);
        m.set(`${fond}${i}`, n);
        reste -= n;
    }
    return m;
}
const verdict = (hero, extra, fond = "basic") => validerDeck({ hero, choisies: choisies(extra, fond), carte });
const dit = (v, re) => assert.match(v.problemes.join(" | "), re);

/* ----------------------------------------------------------------- le miroir JS ---- */
test("paths-shinobi.js = data/shinobi_paths.json : onze Paths, memes types, memes aspects, memes plafonds", () => {
    assert.deepEqual(Object.keys(PATHS_SHINOBI).sort(), Object.keys(DONNEES.paths).sort());
    assert.equal(Object.keys(PATHS_SHINOBI).length, 11);
    for (const [id, regles] of Object.entries(PATHS_SHINOBI)) {
        const d = DONNEES.paths[id];
        assert.deepEqual(regles.types, d.types, `${id} : types`);
        assert.equal(regles.aspects.max, d.aspects.max, `${id} : aspects`);
        assert.equal(!!regles.aspects.libre, !!d.aspects.combinaison_libre, `${id} : combinaison libre`);
        assert.equal(regles.basic, d.basic, `${id} : basic`);
        assert.equal(regles.maxExemplaires || null, d.max_exemplaires || null, `${id} : max exemplaires`);
        assert.equal(regles.nom.replace(/ /g, "").toLowerCase(), d.nom.replace(/ /g, "").toLowerCase(), `${id} : nom`);
    }
});

test("data/shinobi_paths.json : regles communes du livret (taille de main -1, 3 exemplaires, un seul Path, Path hors 40-50)", () => {
    const c = DONNEES.regles_communes;
    assert.equal(c.taille_de_main, -1);
    assert.equal(c.exemplaires_par_carte_shinobi, 3);
    assert.equal(c.un_seul_path, true);
    assert.equal(c.path_obligatoire_pour_les_shinobi, true);
    assert.equal(c.dual_admise_si_un_type_est_autorise, true);
    assert.equal(c.shinobi_ni_aspect_ni_basic, true);
    assert.equal(c.limite_aux_heros_tmnt, false);
});

test("data/cards.json : les 11 Paths existent, type Path, Permanent, classe = types du Path, un seul Path unique", () => {
    const cartes = lire("data/cards.json").tmnt_shinobi_paths;
    assert.equal(cartes.length, 11);
    for (const c of cartes) {
        assert.equal(c.type, "Path", c.card_id);
        assert.equal(c.desc.Permanent, "1", c.card_id);
        assert.deepEqual([...typesShinobi(c.desc.Class)].sort(), [...PATHS_SHINOBI[c.card_id].types].sort(), `${c.card_id} : la classe imprimee = les types du Path`);
        assert.equal(estPath({ type: c.type, class: c.desc.Class }), true, c.card_id);
        assert.match(c.text, /You get -1 hand size\./, `${c.card_id} : -1 taille de main imprime`);
    }
    assert.deepEqual(cartes.filter((c) => c.name.startsWith("* ")).map((c) => c.card_id), ["se005"]);
});

/* ----------------------------------------------------------------- classification ---- */
test("classes : Shinobi (Dual comprise) ni aspect ni Basic ; « Hero;Taijutsu » est une signature", () => {
    assert.deepEqual(typesShinobi("Bushido;Kuji-Kiri"), ["Bushido", "Kuji-Kiri"]);
    assert.deepEqual(typesShinobi("Taijutsu"), ["Taijutsu"]);
    assert.deepEqual(typesShinobi("Hero;Taijutsu"), []);
    assert.deepEqual(typesShinobi("Aggression"), []);
    assert.deepEqual(typesShinobi("Basic"), []);
    assert.equal(estShinobi(CATALOGUE.dualBK), true);
    assert.equal(estShinobi(CATALOGUE.tj004), false);
    assert.equal(estShinobi(CATALOGUE.se001), false, "un Path n'est pas une carte Shinobi du deck");
    assert.equal(estPath(CATALOGUE.se001), true);
    assert.equal(estPath(CATALOGUE.tj011), false, "Sosaiken (classe Hero) n'est pas un Path a choisir");
    assert.equal(classeDeConstruction("Bushido;Kuji-Kiri"), "Bushido;Kuji-Kiri", "les deux types d'une Dual restent lisibles");
    assert.equal(classeDeConstruction("Hero;Taijutsu"), "Hero");
});

test("pool : une carte Shinobi, une Dual et un Path entrent dans le constructeur ; une signature ou Sosaiken non", () => {
    assert.equal(estCarteJoueur(CATALOGUE.Ninjutsu1), true);
    assert.equal(estCarteJoueur(CATALOGUE.dualBK), true);
    assert.equal(estCarteJoueur(CATALOGUE.se001), true);
    assert.equal(estCarteJoueur(CATALOGUE.tj004), false);
    assert.equal(estCarteJoueur(CATALOGUE.tj011), false);
});

test("filtre de classe : une Dual « Bushido;Kuji-Kiri » est visible sous Bushido ET sous Kuji-Kiri, pas sous Ninjutsu", () => {
    const ctx = { ressourcesDe: () => [], motsClesDe: () => [], correspondTexte: () => true };
    const f = filtresVides();
    f.fanMade = true;
    f.aspects = new Set(["Bushido"]);
    assert.equal(passeFiltres(CATALOGUE.dualBK, f, ctx), true);
    f.aspects = new Set(["Kuji-Kiri"]);
    assert.equal(passeFiltres(CATALOGUE.dualBK, f, ctx), true);
    f.aspects = new Set(["Ninjutsu"]);
    assert.equal(passeFiltres(CATALOGUE.dualBK, f, ctx), false);
});

/* ----------------------------------------------------------------- deck-building ---- */
test("⚠ sans Path, AUCUNE carte Shinobi dans le deck", () => {
    const v = verdict(heros("x"), { Ninjutsu1: 3 });
    assert.equal(v.ok, false);
    dit(v, /Cartes Shinobi sans Path/);
});

test("Kagemusha (Ninjutsu) + cartes Ninjutsu + UN aspect + Basic : legal, le Path ne compte pas dans les 40-50", () => {
    const v = verdict(heros("x"), { se001: 1, Ninjutsu1: 3, Ninjutsu2: 3, Aggression1: 3, Aggression2: 3 }, "basic");
    assert.deepEqual(v.problemes, []);
    assert.equal(v.total, 40, "15 signatures + 25 choisies, Path hors decompte");
    assert.deepEqual(v.aspects, ["Aggression"], "Ninjutsu n'est pas un aspect, Basic non plus");
});

test("⚠ Kagemusha + une carte Bushido : refusee (type non autorise par le Path)", () => {
    const v = verdict(heros("x"), { se001: 1, Bushido1: 2 });
    assert.equal(v.ok, false);
    dit(v, /Types Shinobi non autorisés par le Path Kagemusha/);
    dit(v, /Bushido 1/);
});

test("une carte DUAL est admise des qu'UN de ses types l'est : Kagemusha + (Bushido;Ninjutsu) legal, + (Bushido;Kuji-Kiri) refusee", () => {
    assert.deepEqual(verdict(heros("x"), { se001: 1, dualBN: 2 }).problemes, []);
    const v = verdict(heros("x"), { se001: 1, dualBK: 2 });
    assert.equal(v.ok, false);
    dit(v, /Nendō/);
});

test("Shihan (Taijutsu) admet une Dual Ninjutsu/Taijutsu ; Ashigaru (Bushido+Taijutsu) admet une Dual Bushido/Kuji-Kiri (FAQ du livret)", () => {
    assert.deepEqual(verdict(heros("x"), { se004: 1, dualNT: 2 }).problemes, []);
    assert.deepEqual(verdict(heros("x"), { se009: 1, dualBK: 2 }).problemes, []);
});

test("Path hybride : Ashigaru (Bushido + Taijutsu) admet les deux types, refuse Ninjutsu", () => {
    assert.deepEqual(verdict(heros("x"), { se009: 1, Bushido1: 3, Taijutsu1: 3 }).problemes, []);
    const v = verdict(heros("x"), { se009: 1, Ninjutsu1: 1 });
    assert.equal(v.ok, false);
});

test("⚠ un Path n'autorise qu'UN aspect : Kagemusha + Aggression + Justice refuse ; un aspect legal", () => {
    const v = verdict(heros("x"), { se001: 1, Ninjutsu1: 3, Aggression1: 3, Justice1: 3 });
    assert.equal(v.ok, false);
    dit(v, /Trop d’aspects/);
    assert.deepEqual(verdict(heros("x"), { se001: 1, Ninjutsu1: 3, Aggression1: 3 }).problemes, []);
});

test("The Last Ronin : combinaison LIBRE d'aspects et de types Shinobi", () => {
    const v = verdict(heros("x"), { se005: 1, Bushido1: 1, Ninjutsu1: 1, "Kuji-Kiri1": 1, Taijutsu1: 1, Aggression1: 1, Justice1: 1, Leadership1: 1, Protection1: 1 }, "basic");
    assert.deepEqual(v.problemes.filter((p) => !/Trop d’exemplaires/.test(p)), []);
});

test("⚠ The Last Ronin : UN seul exemplaire de toute carte (Basic et aspect compris)", () => {
    const v = verdict(heros("x"), { se005: 1, basic1: 2 });
    assert.equal(v.ok, false);
    dit(v, /Trop d’exemplaires de/);
    const v2 = verdict(heros("x"), { se005: 1, Bushido1: 2 });
    dit(v2, /Trop d’exemplaires de/);
});

test("⚠ un seul Path par deck", () => {
    const v = verdict(heros("x"), { se001: 1, se004: 1, Ninjutsu1: 1 });
    assert.equal(v.ok, false);
    dit(v, /Un seul Path par deck/);
});

test("3 exemplaires de chaque carte Shinobi, sauf unique : 3 legal, 4 refuse, 2 uniques identiques refuse", () => {
    assert.deepEqual(verdict(heros("x"), { se001: 1, Ninjutsu1: 3 }).problemes, []);
    const v4 = verdict(heros("x"), { se001: 1, Ninjutsu1: 4 });
    assert.equal(v4.ok, false);
    dit(v4, /Trop d’exemplaires de/);
    const vu = verdict(heros("x"), { se001: 1, uniq: 2 });
    dit(vu, /Trop d’exemplaires de « Hitodama »/);
});

test("les cartes Shinobi ne comptent NI comme aspect NI comme Basic : un aspect + des Shinobi = un seul aspect, un hero a 2 aspects requis garde sa regle", () => {
    const v = verdict(heros("x"), { se001: 1, Ninjutsu1: 3, Ninjutsu2: 3, Protection1: 3 });
    assert.deepEqual(v.aspects, ["Protection"]);
    // Spider-Woman exige EXACTEMENT 2 aspects : le Path (un aspect) ne casse pas cette exigence du heros.
    const m = new Map([["se001", 1], ["Ninjutsu1", 1], ["Aggression1", 3], ["Aggression2", 3], ["Aggression3", 3], ["Aggression4", 3],
                       ["Justice1", 3], ["Justice2", 3], ["Justice3", 3], ["Justice4", 3]]);
    const sw = validerDeck({ hero: heros("spider_woman"), choisies: m, carte });
    assert.deepEqual(sw.problemes, []);
});

test("Basic reste permis avec un Path (Kagemusha + Basic seulement) ; aucun Shinobi : le Path seul est legal", () => {
    assert.deepEqual(verdict(heros("x"), { se001: 1 }).problemes, []);
});

test("un deck SANS Shinobi ni Path reste jugé comme avant (aucun changement pour les 4 000 decks existants)", () => {
    const v = verdict(heros("x"), { Aggression1: 3 });
    assert.deepEqual(v.problemes, []);
    assert.deepEqual(v.aspects, ["Aggression"]);
});

test("Jennika (Voie PROPRE) : des cartes Shinobi sans Path choisi, aucun aspect, Basic permis", () => {
    assert.deepEqual(verdict(JENNIKA, { Ninjutsu1: 3, Bushido1: 3, Taijutsu1: 3, "Kuji-Kiri1": 3, dualBK: 2 }).problemes, []);
    const v = verdict(JENNIKA, { Ninjutsu1: 3, Aggression1: 3 });
    assert.equal(v.ok, false);
    dit(v, /Trop d’aspects/);
});

test("Jennika : un SECOND Path choisi est refuse (« ce héros a déjà sa Voie »)", () => {
    const v = verdict(JENNIKA, { se001: 1, Ninjutsu1: 3 });
    assert.equal(v.ok, false);
    dit(v, /ce héros a déjà sa Voie/);
});

test("regles du Path : un Path futur sans entree dans la table suit sa classe imprimee (types = classes, un aspect)", () => {
    const futur = { name: "Futur", class: "Bushido;Taijutsu", type: "Path" };
    const r = reglesDuPath(futur, "xx999");
    assert.deepEqual(r.types, ["Bushido", "Taijutsu"]);
    assert.equal(r.aspects.max, 1);
    assert.equal(admiseParLePath({ class: "Taijutsu" }, r), true);
    assert.equal(admiseParLePath({ class: "Ninjutsu" }, r), false);
});
