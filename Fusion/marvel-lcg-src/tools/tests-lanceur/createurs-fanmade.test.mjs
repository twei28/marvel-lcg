// Tests du module pur `public/js/prepare/createurs-fanmade.js` (26/10/2026) :
// la liste des créateurs de contenu fan-made de la page « Crédits », générée
// depuis cards.json (champ `custom`), jamais écrite à la main.
//
//     node --test tools/tests-lanceur/createurs-fanmade.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { aplatirCartes, libelleDuContenu, creditsParCreateur } from "../../public/js/prepare/createurs-fanmade.js";

const ICI = path.dirname(fileURLToPath(import.meta.url));

test("aplatir : accepte l'objet { pack: [cartes] } de /get_cards_json ou une liste", () => {
    assert.equal(aplatirCartes({ a: [{ card_id: "1" }], b: [{ card_id: "2" }, { card_id: "3" }] }).length, 3);
    assert.equal(aplatirCartes([{ card_id: "1" }]).length, 1);
    assert.deepEqual(aplatirCartes(null), []);
});

test("libellé : on enlève Nemesis / Deterrence, on garde le nom du héros ou du pack", () => {
    assert.equal(libelleDuContenu("Corsair Nemesis", "corsair"), "Corsair");
    assert.equal(libelleDuContenu("Batman Deterrence", "batman"), "Batman");
    assert.equal(libelleDuContenu("Wasp (Hank Pym)", "wasp_hank_pym"), "Wasp (Hank Pym)");
    assert.equal(libelleDuContenu("", "starjammers_aspects"), "Starjammers Aspects");
});

test("les officiels (sans custom) n'y figurent pas, les créateurs sont triés, un contenu une seule fois", () => {
    const cartes = {
        core: [{ card_id: "01001", set_name: "Spider-Man" }],
        corsair: [
            { card_id: "cr001a", set_name: "Corsair", custom: "Phenexian and Mysteltainn" },
            { card_id: "cr011", set_name: "Corsair Nemesis", custom: "Phenexian and Mysteltainn" },
        ],
        smasher: [{ card_id: "sz001a", set_name: "Smasher", custom: "Phenexian" }],
        deathstrike: [{ card_id: "ld001a", set_name: "Lady Deathstrike", custom: "Mysteltainn" }],
    };
    const credits = creditsParCreateur(cartes);
    assert.deepEqual(credits.map((c) => c.createur), ["Mysteltainn", "Phenexian"]);
    assert.deepEqual(credits[0].contenus, ["Corsair", "Lady Deathstrike"]);
    assert.deepEqual(credits[1].contenus, ["Corsair", "Smasher"]);
});

test("deux orthographes du même contenu ne font qu'une ligne (« Ch'od » / « Chod »)", () => {
    const cartes = {
        a: [{ card_id: "a1", set_name: "Chod", custom: "X" }],
        b: [{ card_id: "b1", set_name: "Ch'od", custom: "X" }, { card_id: "b2", set_name: "Agent Anti Venom", custom: "X" }],
        c: [{ card_id: "c1", set_name: "Agent Anti-Venom", custom: "X" }],
    };
    assert.deepEqual(creditsParCreateur(cartes)[0].contenus, ["Agent Anti-Venom", "Ch'od"]);
});

test("données réelles : nos héros sont crédités aux bonnes personnes", () => {
    const brut = JSON.parse(fs.readFileSync(path.join(ICI, "../../data/cards.json"), "utf8"));
    const par = new Map(creditsParCreateur(brut).map((c) => [c.createur, c.contenus]));
    assert.ok(!par.has("Phenexian and Mysteltainn"), "un nom composé ne doit pas rester tel quel");
    assert.ok(par.has("Phenexian") && par.has("Mysteltainn"));
    const dit = (createur, contenu) => assert.ok((par.get(createur) || []).includes(contenu), `${createur} devrait créditer ${contenu}`);
    dit("Phenexian", "Corsair");
    dit("Mysteltainn", "Corsair");
    dit("Phenexian", "Smasher");
    dit("Mysteltainn", "Lady Deathstrike");
    dit("ES", "Batman");
    dit("ES", "Batgirl");
    dit("JackHKP", "Wasp (Hank Pym)");
    dit("Dipsome", "New Ultimate Winter Soldier");
    dit("jakxin", "Roz");
    dit("DesignHacker", "U.S. Agent");
    dit("T-Wrecks", "Spider-Punisher");
    assert.ok(![...par.keys()].includes(""), "pas de créateur vide");
    const doublons = (liste) => { const vus = new Set(); return liste.filter((x) => { const k = x.toLowerCase().replace(/[^a-z0-9]/g, ""); const d = vus.has(k); vus.add(k); return d; }); };
    for (const [createur, contenus] of par) assert.deepEqual(doublons(contenus), [], `doublon d'orthographe chez ${createur}`);
});
