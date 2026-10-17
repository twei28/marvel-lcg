// Tests de construction des 12 cartes DUAL SHINOBI (TMNT Shinobi, Inkwire, pack tmnt_shinobi_dual, prefixe `sc`), 17/10/2026.
//
//     node --test tools/tests-lanceur/regles-shinobi-dual.test.mjs
//
// Livret p.7 : une carte Dual « compte comme LES DEUX types » pendant la construction ET pendant le jeu. Ce fichier prouve le
// versant CONSTRUCTION sur les 12 cartes REELLES de data/cards.json (le versant jeu : tools/cas/tmnt_shinobi_dual.py) :
//  - chaque Dual est une carte Shinobi, de ses DEUX types exactement, ni aspect ni Basic, et entre dans le constructeur ;
//  - un filtre de classe de l'UN et de l'AUTRE de ses types la trouve, pas un filtre des deux autres types ;
//  - un Path qui n'autorise que l'UN des deux types suffit (4 Paths standard x chaque Dual), l'autre type aussi ;
//  - un Path qui n'autorise AUCUN des deux types la refuse ;
//  - sans Path, elle est refusee comme toute carte Shinobi ; elle ne compte pas comme un aspect.
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { estCarteJoueur, validerDeck } from "../../public/js/deckbuilder/regles.js";
import { CLASSES_SHINOBI, typesShinobi, estShinobi } from "../../public/js/deckbuilder/paths-shinobi.js";
import { filtresVides, passeFiltres } from "../../public/js/deckbuilder/filtres.js";

const RACINE = new URL("../../", import.meta.url);
const CARTES = JSON.parse(fs.readFileSync(new URL("data/cards.json", RACINE), "utf-8"));
const normaliser = (c) => ({ name: c.name, class: c.desc.Class, type: c.type, desc: c.desc });
const CATALOGUE = {};
for (const c of [...CARTES.tmnt_shinobi_dual, ...CARTES.tmnt_shinobi_paths]) CATALOGUE[c.card_id] = normaliser(c);
const DUALS = CARTES.tmnt_shinobi_dual.map((c) => c.card_id);
// Paths STANDARD : un seul type chacun (Kagemusha = Ninjutsu, Onmyodo = Kuji-Kiri, Samurai = Bushido, Shihan = Taijutsu)
const PATH_DU_TYPE = { Ninjutsu: "se001", "Kuji-Kiri": "se002", Bushido: "se003", Taijutsu: "se004" };

for (const cls of CLASSES_SHINOBI) {
    for (let i = 1; i <= 9; i++) CATALOGUE[`${cls}${i}`] = { name: `${cls} ${i}`, class: cls, type: "Event", desc: {} };
}
for (let i = 1; i <= 9; i++) CATALOGUE[`basic${i}`] = { name: `Basique ${i}`, class: "Basic", type: "Event", desc: {} };

const carte = (id) => CATALOGUE[id];
const heros = (id) => ({ id, name: id, deck: { hero_deck: Array(15).fill("sig") } });
/** 15 signatures + 25 choisies : `extra`, complete avec des cartes Basic (3 exemplaires par titre au plus). */
function choisies(extra) {
    const m = new Map(Object.entries(extra));
    let reste = 25 - Object.entries(extra).filter(([id]) => !id.startsWith("se")).reduce((s, [, n]) => s + n, 0);
    for (let i = 1; reste > 0; i++) {
        const n = Math.min(3, reste);
        m.set(`basic${i}`, n);
        reste -= n;
    }
    return m;
}
const verdict = (extra) => validerDeck({ hero: heros("x"), choisies: choisies(extra), carte });
const ctx = { ressourcesDe: () => [], motsClesDe: () => [], correspondTexte: () => true };

test("le catalogue porte les 12 Dual, type Event ou Upgrade, deux classes Shinobi chacune, credit Inkwire", () => {
    assert.equal(DUALS.length, 12);
    for (const c of CARTES.tmnt_shinobi_dual) {
        assert.ok(["Event", "Upgrade"].includes(c.type), c.card_id);
        assert.equal(c.custom, "Inkwire", c.card_id);
        assert.equal(c.set_name, "TMNT Shinobi Dual", c.card_id);
        assert.equal(typesShinobi(c.desc.Class).length, 2, `${c.card_id} : DEUX types Shinobi`);
        assert.equal(new Set(typesShinobi(c.desc.Class)).size, 2, `${c.card_id} : deux types DIFFERENTS`);
    }
});

for (const id of DUALS) {
    const [a, b] = typesShinobi(CATALOGUE[id].class);
    const autres = CLASSES_SHINOBI.filter((t) => t !== a && t !== b);
    const nom = `${id} ${CATALOGUE[id].name} (${a}/${b})`;

    test(`${nom} : carte Shinobi, entre dans le constructeur, sous les filtres des DEUX types et d'aucun autre`, () => {
        assert.equal(estShinobi(carte(id)), true);
        assert.equal(estCarteJoueur(carte(id)), true);
        for (const t of [a, b]) {
            const f = filtresVides();
            f.fanMade = true;
            f.aspects = new Set([t]);
            assert.equal(passeFiltres(carte(id), f, ctx), true, `filtre ${t}`);
        }
        for (const t of [...autres, "Aggression", "Justice", "Leadership", "Protection"]) {
            const f = filtresVides();
            f.fanMade = true;
            f.aspects = new Set([t]);
            assert.equal(passeFiltres(carte(id), f, ctx), false, `filtre ${t} ne doit pas la montrer`);
        }
    });

    test(`${nom} : admise par un Path ${a} seul ET par un Path ${b} seul, refusee par un Path ${autres[0]} seul et par un Path ${autres[1]} seul`, () => {
        for (const t of [a, b]) {
            const v = verdict({ [PATH_DU_TYPE[t]]: 1, [id]: 3 });
            assert.deepEqual(v.problemes, [], `Path ${t} : ${v.problemes.join(" | ")}`);
        }
        for (const t of autres) {
            const v = verdict({ [PATH_DU_TYPE[t]]: 1, [id]: 3 });
            assert.equal(v.ok, false, `Path ${t} : devrait refuser`);
            assert.match(v.problemes.join(" | "), /Types Shinobi non autorisés par le Path/, `Path ${t}`);
            assert.match(v.problemes.join(" | "), new RegExp(CATALOGUE[id].name), `Path ${t} : cite la carte`);
        }
    });

    test(`${nom} : sans Path elle est refusee ; avec un Path elle ne compte PAS comme un aspect (3 exemplaires, aucun aspect)`, () => {
        const sans = verdict({ [id]: 3 });
        assert.equal(sans.ok, false);
        assert.match(sans.problemes.join(" | "), /Cartes Shinobi sans Path/);
        const avec = verdict({ [PATH_DU_TYPE[a]]: 1, [id]: 3 });
        assert.deepEqual(avec.aspects, [], "une Dual n'est pas un aspect");
    });
}
