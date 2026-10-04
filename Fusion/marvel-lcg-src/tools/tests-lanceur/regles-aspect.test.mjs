// Tests du module pur `public/js/deckbuilder/regles.js`, côté LIMITE D'ASPECT.
//
//     node --test tools/tests-lanceur/regles-aspect.test.mjs
//
// Ce que ce fichier prouve, et qu'aucune lecture de code ne prouve : un héros
// dont la carte lève la limite d'aspect la lève POUR SES CARTES À LUI, et pour
// personne d'autre. Les deux moitiés comptent autant l'une que l'autre — une
// exemption trop large rendrait légal n'importe quel deck à quatre couleurs.
//
// Écrit le 22/09/2026 après un refus signalé en jeu : un deck marvelcdb de
// Cable bâti sur les manigances annexes était recalé au collage (« Trop
// d'aspects (Justice, Leadership, Aggression, Protection) »), alors que
// Nathan Summers (40001b) dit mot pour mot « You may include player side
// schemes from any aspect in your deck ».
import { test } from "node:test";
import assert from "node:assert/strict";
import { exemptDeLaLimiteAspect, validerDeck } from "../../public/js/deckbuilder/regles.js";

/** Un catalogue minuscule : ce que `validerDeck` lit d'une carte, et rien de
 *  plus (`class`, `type`, `name`, `desc`). */
const CATALOGUE = {
    // Les manigances annexes des TROIS autres aspects : le cœur du signalement.
    ps_justice: { name: "Manigance Justice", class: "Justice", type: "PlayerSideScheme", desc: {} },
    ps_aggression: { name: "Manigance Aggression", class: "Aggression", type: "PlayerSideScheme", desc: {} },
    ps_protection: { name: "Manigance Protection", class: "Protection", type: "PlayerSideScheme", desc: {} },
    // L'orthographe de marvelcdb, que `TYPES_JOUEUR` accepte aussi.
    ps_marvelcdb: { name: "Manigance importée", class: "Justice", type: "Player_Side_Scheme", desc: {} },
    // Une carte hors aspect qui N'EST PAS une manigance annexe : l'exemption
    // ne doit pas déborder dessus.
    allie_justice: { name: "Allié Justice", class: "Justice", type: "Ally", desc: {} },
};

// Le corps du deck, dans l'aspect choisi. Neuf titres DIFFÉRENTS et non un
// seul répété : la limite ordinaire est de 3 exemplaires par titre, et c'est
// elle qui parlerait sinon, à la place de la règle qu'on mesure.
for (let i = 1; i <= 9; i++) {
    CATALOGUE[`lead${i}`] = { name: `Pilier ${i}`, class: "Leadership", type: "Ally", desc: {} };
}

const carte = (id) => CATALOGUE[id];
const heros = (id) => ({ id, name: id, deck: { hero_deck: Array(15).fill("sig") } });

/** Un deck de 40 cartes : 15 signatures + 25 choisies, dont `extra`. */
function choisies(extra) {
    const m = new Map(Object.entries(extra));
    let reste = 25 - somme(extra);
    for (let i = 1; reste > 0; i++) {
        const n = Math.min(3, reste);
        m.set(`lead${i}`, n);
        reste -= n;
    }
    return m;
}
const somme = (o) => Object.values(o).reduce((a, b) => a + b, 0);

test("Cable : les manigances annexes d'autres aspects ne comptent pas", () => {
    const verdict = validerDeck({
        hero: heros("cable"),
        choisies: choisies({ ps_justice: 2, ps_aggression: 2, ps_protection: 2 }),
        carte,
    });
    assert.deepEqual(verdict.problemes, []);
    assert.equal(verdict.ok, true);
    assert.deepEqual(verdict.aspects, ["Leadership"]);
    assert.equal(verdict.total, 40);
});

test("Cable : l'orthographe Player_Side_Scheme de marvelcdb passe aussi", () => {
    assert.equal(exemptDeLaLimiteAspect(heros("cable"), CATALOGUE.ps_marvelcdb), true);
});

test("⚠ Cable : l'exemption s'arrête aux manigances, un allié hors aspect reste refusé", () => {
    const verdict = validerDeck({
        hero: heros("cable"),
        choisies: choisies({ ps_justice: 2, allie_justice: 2 }),
        carte,
    });
    assert.equal(verdict.ok, false);
    assert.deepEqual(verdict.aspects.sort(), ["Justice", "Leadership"]);
    assert.match(verdict.problemes.join(" "), /Trop d’aspects/);
});

test("⚠ LE TÉMOIN QUI MORD : le même deck chez un autre héros reste refusé", () => {
    // Sans ce cas, une exemption posée pour tout le monde passerait au vert
    // au-dessus, et rendrait légal n'importe quel deck à quatre couleurs.
    const verdict = validerDeck({
        hero: heros("spider_man"),
        choisies: choisies({ ps_justice: 2, ps_aggression: 2, ps_protection: 2 }),
        carte,
    });
    assert.equal(verdict.ok, false);
    assert.match(verdict.problemes.join(" "), /Trop d’aspects/);
    assert.deepEqual(verdict.aspects.sort(), ["Aggression", "Justice", "Leadership", "Protection"]);
});

// ---------------------------------------------------------------------------
// Gamora (18001b, Skilled Tactician) : « up to 6 attack and thwart events from
// aspects other than your own ». Signalement Phocéa n°32 (30/09/2026) : le deck
// était refusé (« Trop d'aspects ») faute de règle déclarée. On lit le VRAI
// deck/starter/gamora.json, pas une copie : c'est ce fichier qui était fautif.
import { readFileSync } from "node:fs";

const gamoraDeck = JSON.parse(readFileSync(new URL("../../deck/starter/gamora.json", import.meta.url), "utf8"));
const gamora = { id: "gamora", name: "Gamora", deck: gamoraDeck };

const evenements = [
    ["ev_j1", "Justice", "ATTACK"], ["ev_j2", "Justice", "THWART"],
    ["ev_p1", "Protection", "ATTACK"], ["ev_p2", "Protection", "THWART"],
    ["ev_a1", "Aggression", "ATTACK"], ["ev_a2", "Aggression", "THWART"],
    ["ev_a3", "Aggression", "ATTACK"],
];
for (const [id, classe, trait] of evenements) {
    CATALOGUE[id] = { name: `Événement ${id}`, class: classe, type: "Event", traits: [trait], desc: {} };
}
// Un événement hors aspect SANS trait attaque/menace, et un allié ATTACK.
CATALOGUE.ev_sans_trait = { name: "Événement neutre", class: "Justice", type: "Event", traits: ["TACTIC"], desc: {} };
CATALOGUE.allie_attack = { name: "Allié Aggression", class: "Aggression", type: "Ally", traits: ["ATTACK"], desc: {} };

test("Gamora : 6 événements attaque/menace d'autres aspects sont légaux", () => {
    const verdict = validerDeck({
        hero: gamora,
        choisies: choisies({ ev_j1: 1, ev_j2: 1, ev_p1: 1, ev_p2: 1, ev_a1: 1, ev_a2: 1 }),
        carte,
    });
    assert.deepEqual(verdict.problemes, []);
    assert.equal(verdict.ok, true);
    assert.deepEqual(verdict.aspects, ["Leadership"]);
});

test("Gamora : un 7e événement hors aspect dépasse le quota", () => {
    const verdict = validerDeck({
        hero: gamora,
        choisies: choisies({ ev_j1: 1, ev_j2: 1, ev_p1: 1, ev_p2: 1, ev_a1: 1, ev_a2: 1, ev_a3: 1 }),
        carte,
    });
    assert.equal(verdict.ok, false);
    assert.match(verdict.problemes.join(" "), /Hors aspect : au plus 6 .*actuellement 7/);
});

test("⚠ Gamora : l'exemption s'arrête aux événements attaque/menace", () => {
    for (const id of ["ev_sans_trait", "allie_attack"]) {
        const verdict = validerDeck({
            hero: gamora,
            choisies: choisies({ [id]: 2 }),
            carte,
        });
        assert.equal(verdict.ok, false, id);
        assert.match(verdict.problemes.join(" "), /Trop d’aspects/, id);
    }
});

test("⚠ LE TÉMOIN QUI MORD : les mêmes 6 événements chez un autre héros restent refusés", () => {
    const verdict = validerDeck({
        hero: heros("spider_man"),
        choisies: choisies({ ev_j1: 1, ev_j2: 1, ev_p1: 1, ev_p2: 1, ev_a1: 1, ev_a2: 1 }),
        carte,
    });
    assert.equal(verdict.ok, false);
    assert.match(verdict.problemes.join(" "), /Trop d’aspects/);
});

// ---------------------------------------------------------------------------
// Maria Hill (50001b) : « the maximum number of copies of 3 S.H.I.E.L.D.
// supports from aspects other than your chosen aspect ». Signalement Aghenatak
// du 03/10/2026 : le deck marvelcdb 64390 (Triskelion, Command Team x3,
// Ops Room x3 hors Justice) etait refuse. Le quota compte des TITRES.
const mariaDeck = JSON.parse(readFileSync(new URL("../../deck/starter/maria_hill.json", import.meta.url), "utf8"));
const maria = { id: "maria_hill", name: "Maria Hill", deck: mariaDeck };
Object.assign(CATALOGUE, {
    sh_trisk: { name: "The Triskelion", class: "Leadership", type: "Support", traits: ["S.H.I.E.L.D"], desc: {} },
    sh_cmd: { name: "Command Team", class: "Leadership", type: "Support", traits: ["S.H.I.E.L.D"], desc: {} },
    sh_ops: { name: "Ops Room", class: "Protection", type: "Support", traits: ["S.H.I.E.L.D."], desc: {} },
    sh_quatre: { name: "Quatrieme support", class: "Aggression", type: "Support", traits: ["S.H.I.E.L.D"], desc: {} },
    sh_allie: { name: "Agent hors aspect", class: "Protection", type: "Ally", traits: ["S.H.I.E.L.D"], desc: {} },
});
for (let i = 1; i <= 9; i++) {
    CATALOGUE[`jus${i}`] = { name: `Justice ${i}`, class: "Justice", type: "Ally", desc: {} };
}
/** 25 choisies : `extra` hors aspect, le reste en Justice. */
function choisiesMaria(extra) {
    const m = new Map(Object.entries(extra));
    let reste = 25 - somme(extra);
    for (let i = 1; reste > 0; i++) {
        const n = Math.min(3, reste);
        m.set(`jus${i}`, n);
        reste -= n;
    }
    return m;
}

test("Maria Hill : 3 supports S.H.I.E.L.D. d'autres aspects en exemplaires max (deck 64390)", () => {
    const verdict = validerDeck({ hero: maria, choisies: choisiesMaria({ sh_trisk: 1, sh_cmd: 3, sh_ops: 3 }), carte });
    assert.deepEqual(verdict.problemes, []);
    assert.deepEqual(verdict.aspects, ["Justice"]);
    assert.equal(verdict.horsAspect, 3);
});

test("Maria Hill : un 4e titre hors aspect depasse le quota", () => {
    const verdict = validerDeck({ hero: maria, choisies: choisiesMaria({ sh_trisk: 1, sh_cmd: 3, sh_ops: 3, sh_quatre: 1 }), carte });
    assert.equal(verdict.ok, false);
    assert.match(verdict.problemes.join(" "), /Hors aspect : au plus 3 supports .*actuellement 4/);
});

test("⚠ Maria Hill : un allie S.H.I.E.L.D. d'un autre aspect reste refuse", () => {
    const verdict = validerDeck({ hero: maria, choisies: choisiesMaria({ sh_allie: 1 }), carte });
    assert.equal(verdict.ok, false);
    assert.match(verdict.problemes.join(" "), /Trop d’aspects/);
});

test("⚠ LE TEMOIN QUI MORD : les memes supports chez un autre heros restent refuses", () => {
    const verdict = validerDeck({ hero: heros("spider_man"), choisies: choisiesMaria({ sh_trisk: 1, sh_cmd: 3, sh_ops: 3 }), carte });
    assert.equal(verdict.ok, false);
    assert.match(verdict.problemes.join(" "), /Trop d’aspects/);
});

// ---------------------------------------------------------------------------
// AUDIT DU 03/10/2026 : chaque identite dont la carte touche a la construction,
// relevee sur le texte imprime de tout le catalogue (et confrontee a 4180 decks
// publies sur marvelcdb). Un cas qui passe, un cas qui mord.
const starter = (id) => {
    const deck = JSON.parse(readFileSync(new URL(`../../deck/starter/${id}.json`, import.meta.url), "utf8"));
    return { id, name: deck.name, deck };
};
Object.assign(CATALOGUE, {
    xmen_j: { name: "Allie X-Men", class: "Justice", type: "Ally", traits: ["X-MEN"], desc: {} },
    skill_j: { name: "Skill Justice", class: "Justice", type: "Event", traits: ["SKILL"], desc: {} },
    skill_p: { name: "Skill Protection", class: "Protection", type: "Upgrade", traits: ["SKILL"], desc: {} },
    energie_j: { name: "Evenement energie", class: "Justice", type: "Event", desc: { RES: "Y" } },
    mental_j: { name: "Evenement mental", class: "Justice", type: "Event", desc: { RES: "B" } },
    tech1: { name: "Tech 1", class: "Justice", type: "Upgrade", traits: ["TECH"], desc: {} },
    tech2: { name: "Tech 2", class: "Protection", type: "Upgrade", traits: ["TECH"], desc: {} },
    tech3: { name: "Tech 3", class: "Aggression", type: "Upgrade", traits: ["TECH"], desc: {} },
    tech4: { name: "Tech 4", class: "Aggression", type: "Upgrade", traits: ["TECH"], desc: {} },
    ev_j: { name: "Evenement J", class: "Justice", type: "Event", desc: {} },
    allie_basique: { name: "Allie basique", class: "Basic", type: "Ally", desc: {} },
});

test("Cyclops : les allies X-MEN d'autres aspects passent, un evenement non", () => {
    assert.equal(validerDeck({ hero: heros("cyclops"), choisies: choisies({ xmen_j: 1 }), carte }).ok, true);
    assert.match(validerDeck({ hero: heros("cyclops"), choisies: choisies({ ev_j: 1 }), carte }).problemes.join(" "), /Trop d’aspects/);
    assert.equal(validerDeck({ hero: heros("spider_man"), choisies: choisies({ xmen_j: 1 }), carte }).ok, false);
});

test("Kate Bishop : les cartes SKILL de tout aspect passent", () => {
    assert.equal(validerDeck({ hero: heros("kate_bishop"), choisies: choisies({ skill_j: 1, skill_p: 1 }), carte }).ok, true);
    assert.equal(validerDeck({ hero: heros("spider_man"), choisies: choisies({ skill_j: 1 }), carte }).ok, false);
});

test("Wonder Man : les evenements a ressource energie passent, pas les mentaux", () => {
    assert.equal(validerDeck({ hero: heros("wonder_man"), choisies: choisies({ energie_j: 2 }), carte }).ok, true);
    assert.equal(validerDeck({ hero: heros("wonder_man"), choisies: choisies({ mental_j: 1 }), carte }).ok, false);
});

test("Harry Osborn : 3 titres TECH hors aspect, pas 4", () => {
    const harry = starter("harry_osborn");
    assert.deepEqual(validerDeck({ hero: harry, choisies: choisies({ tech1: 3, tech2: 3, tech3: 3 }), carte }).problemes, []);
    assert.match(validerDeck({ hero: harry, choisies: choisies({ tech1: 1, tech2: 1, tech3: 1, tech4: 1 }), carte }).problemes.join(" "), /actuellement 4/);
});

test("Night Thrasher : 4 cartes SKILL hors aspect, pas 5", () => {
    const nt = starter("night_thrasher");
    assert.equal(validerDeck({ hero: nt, choisies: choisies({ skill_j: 2, skill_p: 2 }), carte }).ok, true);
    assert.match(validerDeck({ hero: nt, choisies: choisies({ skill_j: 3, skill_p: 2 }), carte }).problemes.join(" "), /actuellement 5/);
});

test("Red Sonja : 6 evenements hors aspect, pas un allie", () => {
    const rs = starter("red_sonja");
    assert.equal(validerDeck({ hero: rs, choisies: choisies({ ev_j: 3, ev_a1: 1, ev_a2: 1, ev_p1: 1 }), carte }).ok, true);
    assert.equal(validerDeck({ hero: rs, choisies: choisies({ allie_justice: 1 }), carte }).ok, false);
});

test("Iron Patriot : pas d'allie d'aspect, les allies basiques restent permis", () => {
    const ip = starter("iron_patriot");
    const v = validerDeck({ hero: ip, choisies: choisies({}), carte });
    assert.match(v.problemes.join(" "), /refuse ce type de carte/);
    const sansAllies = new Map([["allie_basique", 1], ...[...Array(8)].map((_, i) => [`ev_lead${i}`, 3])]);
    for (let i = 0; i < 8; i++) CATALOGUE[`ev_lead${i}`] = { name: `Evt Lead ${i}`, class: "Leadership", type: "Event", desc: {} };
    assert.deepEqual(validerDeck({ hero: ip, choisies: sansAllies, carte }).problemes, []);
});

test("Adam Warlock : un exemplaire par titre, les 4 aspects, en nombres egaux", () => {
    const adam = heros("adam_warlock");
    for (const a of ["Aggression", "Justice", "Leadership", "Protection"]) {
        for (let i = 0; i < 7; i++) CATALOGUE[`aw_${a}${i}`] = { name: `${a} ${i}`, class: a, type: "Event", desc: {} };
    }
    const deck = (n, extra = {}) => {
        const m = new Map(Object.entries(extra));
        for (const a of ["Aggression", "Justice", "Leadership", "Protection"]) for (let i = 0; i < n[a]; i++) m.set(`aw_${a}${i}`, 1);
        return m;
    };
    assert.deepEqual(validerDeck({ hero: adam, choisies: deck({ Aggression: 6, Justice: 6, Leadership: 6, Protection: 6 }, { allie_basique: 1 }), carte }).problemes, []);
    assert.match(validerDeck({ hero: adam, choisies: deck({ Aggression: 7, Justice: 6, Leadership: 6, Protection: 5 }, { allie_basique: 1 }), carte }).problemes.join(" "), /autant de cartes/);
    assert.match(validerDeck({ hero: adam, choisies: deck({ Aggression: 6, Justice: 6, Leadership: 6, Protection: 5 }, { allie_basique: 2 }), carte }).problemes.join(" "), /Trop d’exemplaires de « Allie basique » : 2\/1/);
});

test("Spider-Woman : deux aspects en nombres egaux", () => {
    const sw = heros("spider_woman");
    const egal = new Map([["lead1", 3], ["lead2", 3], ["lead3", 3], ["lead4", 3], ["jus1", 3], ["jus2", 3], ["jus3", 3], ["jus4", 3], ["allie_basique", 1]]);
    assert.deepEqual(validerDeck({ hero: sw, choisies: egal, carte }).problemes, []);
    const inegal = new Map(egal).set("jus4", 2).set("lead5", 1);
    assert.match(validerDeck({ hero: sw, choisies: inegal, carte }).problemes.join(" "), /autant de cartes de chaque aspect \(Leadership 13, Justice 11\)/);
});

test("Moon Knight : cout imprime 3 ou plus refuse, au moins 4 cartes par aspect", () => {
    const mk = heros("moon_knight");
    for (const a of ["Aggression", "Justice", "Leadership", "Protection"]) {
        for (let i = 0; i < 3; i++) CATALOGUE[`mk_${a}${i}`] = { name: `MK ${a} ${i}`, class: a, type: "Event", desc: { Cost: "2" } };
    }
    CATALOGUE.mk_cher = { name: "Trop cher", class: "Justice", type: "Event", desc: { Cost: "3" } };
    const base = new Map([["mk_Aggression0", 3], ["mk_Aggression1", 3], ["mk_Justice0", 3], ["mk_Justice1", 3], ["mk_Leadership0", 3], ["mk_Leadership1", 3], ["mk_Protection0", 3], ["mk_Protection1", 3], ["allie_basique", 1]]);
    assert.deepEqual(validerDeck({ hero: mk, choisies: base, carte }).problemes, []);
    assert.match(validerDeck({ hero: mk, choisies: new Map([...base, ["mk_cher", 1]]), carte }).problemes.join(" "), /Coût imprimé 3 ou plus/);
    const troisProtections = new Map(base).set("mk_Protection0", 2).set("mk_Protection1", 1).set("mk_Aggression2", 3);
    assert.match(validerDeck({ hero: mk, choisies: troisProtections, carte }).problemes.join(" "), /Au moins 4 cartes de chaque aspect \(Moon Knight\) : Protection/);
});

// Copies et unicite (Rules Reference v1.8, « Copy » et « Unique Icon »).
Object.assign(CATALOGUE, {
    sw_a: { name: "* Spider-Woman", subtitle: "Jessica Drew", class: "Justice", type: "Ally", desc: {} },
    sw_b: { name: "* Spider-Woman", subtitle: "Ashley Barton", class: "Justice", type: "Ally", desc: {} },
    pym_a: { name: "* Ant-Man", subtitle: "Hank Pym", class: "Justice", type: "Ally", desc: {} },
    pym_b: { name: "* Yellow Jacket", subtitle: "Hank Pym", class: "Basic", type: "Ally", desc: {} },
    tony: { name: "* Iron Man", subtitle: "Tony Stark", class: "Justice", type: "Ally", desc: {} },
    id_im_a: { name: "* Iron Man", type: "Hero", desc: {} },
    id_im_b: { name: "Tony Stark", type: "AlterEgo", desc: {} },
});

test("Copies : deux allies de meme titre mais de sous-titres differents ne sont pas des copies", () => {
    const v = validerDeck({ hero: heros("madame_web_test"), choisies: choisiesMaria({ sw_a: 1, sw_b: 1 }), carte });
    assert.deepEqual(v.problemes, []);
});

test("Unicite : une carte unique ne figure qu'une fois", () => {
    assert.match(validerDeck({ hero: heros("x"), choisies: choisiesMaria({ sw_a: 2 }), carte }).problemes.join(" "), /2\/1/);
});

test("Unicite : deux cartes uniques qui se correspondent par le sous-titre sont refusees", () => {
    assert.match(validerDeck({ hero: heros("x"), choisies: choisiesMaria({ pym_a: 1, pym_b: 1 }), carte }).problemes.join(" "), /se correspondent/);
});

test("Unicite : l'allie qui correspond a l'identite est refuse (Iron Man chez Iron Man)", () => {
    const ironMan = { id: "iron_man_test", name: "Iron Man", deck: { hero: ["id_im_a,id_im_b"], hero_deck: Array(15).fill("sig") } };
    assert.match(validerDeck({ hero: ironMan, choisies: choisiesMaria({ tony: 1 }), carte }).problemes.join(" "), /se correspondent/);
    assert.deepEqual(validerDeck({ hero: heros("x"), choisies: choisiesMaria({ tony: 1 }), carte }).problemes, []);
});

// Classes doubles du catalogue : « Hero;Aggression » est une signature.
import { classeDeConstruction } from "../../public/js/deckbuilder/regles.js";
import { versDeckMoteur } from "../../public/js/marvelcdb/conversion.js";

test("Classe double : signature d'abord, sinon l'aspect, sinon le neutre", () => {
    assert.equal(classeDeConstruction("Hero;Aggression"), "Hero");
    assert.equal(classeDeConstruction("Campaign;Justice"), "Justice");
    assert.ok(["Campaign", "Basic"].includes(classeDeConstruction("Campaign;Basic")));
    assert.equal(classeDeConstruction("Justice"), "Justice");
});

test("Import marvelcdb : une signature « Hero;Aggression » ne tombe pas dans la pioche", () => {
    const deck = versDeckMoteur({ id: 1, nom: "x", cartes: { sig_double: 1, ev_j: 2 } }, { hero: [], hero_deck: [] }, (id) => (id === "sig_double" ? "Hero;Aggression" : "Justice"));
    assert.deepEqual(deck.player_deck, ["ev_j", "ev_j"]);
});
