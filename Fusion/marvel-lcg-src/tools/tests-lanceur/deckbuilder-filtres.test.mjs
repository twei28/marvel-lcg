// node --test tools/tests-lanceur/deckbuilder-filtres.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import {
    filtresVides, passeFiltres, cleCout, cleStat, aspectsParDefaut,
    comparateur, grouperDeck, courbeDesCouts, nombreFiltresActifs,
} from "../../public/js/deckbuilder/filtres.js";

const ctx = {
    ressourcesDe: (c) => String((c.desc && c.desc.RES) || "").split(""),
    motsClesDe: (c) => (/retaliate/i.test(c.text || "") ? ["Riposte"] : []),
    correspondTexte: (c, t) => c.name.toLowerCase().includes(t.toLowerCase()),
};
const carte = (o) => ({ traits: [], desc: {}, text: "", custom: "", package_name: "core", ...o });
const hill = carte({ name: "* Maria Hill", type: "Ally", class: "Leadership", cost: "2", traits: ["S.H.I.E.L.D."], desc: { Cost: "2", HP: "2", ATK: "1", THW: "2", RES: "B" } });
const coup = carte({ name: "Counter-Punch", type: "Event", class: "Protection", cost: "0", desc: { Cost: "0", RES: "R" } });
const lourd = carte({ name: "Avengers Mansion", type: "Support", class: "Basic", cost: "6", traits: ["AVENGER", "LOCATION"], desc: { Cost: "6" } });
const fan = carte({ name: "Fan card", type: "Event", class: "Determination", cost: "1", custom: "Auteur" });

const avec = (modif) => { const f = filtresVides(); modif(f); return f; };

test("sans filtre, toute carte officielle passe, le fan-made est caché", () => {
    const f = filtresVides();
    assert.equal(passeFiltres(hill, f, ctx), true);
    assert.equal(passeFiltres(fan, f, ctx), false);
    assert.equal(passeFiltres(fan, avec((x) => { x.fanMade = true; }), ctx), true);
});

test("aspects, types et coûts se cumulent", () => {
    const f = avec((x) => { x.aspects.add("Leadership"); x.types.add("Ally"); x.couts.add("2"); });
    assert.equal(passeFiltres(hill, f, ctx), true);
    assert.equal(passeFiltres(coup, f, ctx), false);
});

test("le palier 5+ couvre les coûts de 5 et plus", () => {
    assert.equal(cleCout(lourd), "5+");
    assert.equal(cleCout(carte({ cost: "X" })), "X");
    assert.equal(cleCout(carte({ cost: undefined })), "");
    assert.equal(passeFiltres(lourd, avec((x) => x.couts.add("5+")), ctx), true);
});

test("traits en OU puis en ET", () => {
    const ou = avec((x) => { x.traits.add("Avenger"); x.traits.add("S.H.I.E.L.D"); });
    assert.equal(passeFiltres(hill, ou, ctx), true);
    assert.equal(passeFiltres(lourd, ou, ctx), true);
    const et = avec((x) => { x.traits.add("Avenger"); x.traits.add("Location"); x.traitsMode = "et"; });
    assert.equal(passeFiltres(lourd, et, ctx), true);
    assert.equal(passeFiltres(hill, et, ctx), false);
});

test("statistiques par palier, la carte sans la stat ne passe pas", () => {
    assert.equal(cleStat("7"), "4+");
    assert.equal(cleStat(undefined), "");
    const f = avec((x) => x.stats.thw.add("2"));
    assert.equal(passeFiltres(hill, f, ctx), true);
    assert.equal(passeFiltres(coup, f, ctx), false);
});

test("unique, ressource, mot-clé, pack", () => {
    assert.equal(passeFiltres(coup, avec((x) => { x.unique = true; }), ctx), false);
    assert.equal(passeFiltres(hill, avec((x) => x.ressources.add("B")), ctx), true);
    assert.equal(passeFiltres(hill, avec((x) => x.motsCles.add("Riposte")), ctx), false);
    assert.equal(passeFiltres(hill, avec((x) => x.packs.add("cap")), ctx), false);
});

test("la recherche mêle syntaxe courte et texte libre", () => {
    assert.equal(passeFiltres(hill, avec((x) => { x.texte = "c:2 maria"; }), ctx), true);
    assert.equal(passeFiltres(hill, avec((x) => { x.texte = "c:3 maria"; }), ctx), false);
    assert.equal(passeFiltres(hill, avec((x) => { x.texte = "c:2 tony"; }), ctx), false);
});

test("aspects par défaut : ceux du deck plus Basique, rien si deck vide", () => {
    assert.deepEqual([...aspectsParDefaut(["Protection"])], ["Protection", "Basic"]);
    assert.deepEqual([...aspectsParDefaut([])], []);
    assert.deepEqual([...aspectsParDefaut(["Justice"], true)], ["Hero", "Justice", "Basic"]);
});

test("tri par aspect puis coût, et par nom", () => {
    const liste = [lourd, coup, hill];
    assert.deepEqual([...liste].sort(comparateur("aspect")).map((c) => c.name), ["* Maria Hill", "Counter-Punch", "Avengers Mansion"]);
    assert.deepEqual([...liste].sort(comparateur("nom")).map((c) => c.name), ["Avengers Mansion", "Counter-Punch", "* Maria Hill"]);
    assert.deepEqual([...liste].sort(comparateur("cout")).map((c) => c.name), ["Counter-Punch", "* Maria Hill", "Avengers Mansion"]);
});

test("groupes du deck par type, avec total", () => {
    const lignes = [{ id: "a", n: 2, carte: coup }, { id: "b", n: 1, carte: hill }, { id: "c", n: 1, carte: lourd }];
    const g = grouperDeck(lignes, "type");
    assert.deepEqual(g.map((x) => [x.valeur, x.total]), [["Ally", 1], ["Event", 2], ["Support", 1]]);
    assert.equal(grouperDeck([], "type").length, 0);
});

test("courbe des coûts de 0 à 5+", () => {
    const c = courbeDesCouts([{ n: 3, carte: coup }, { n: 1, carte: hill }, { n: 2, carte: lourd }]);
    assert.deepEqual(c.map((x) => x.total), [3, 0, 1, 0, 0, 2]);
});

test("compte des filtres actifs", () => {
    assert.equal(nombreFiltresActifs(filtresVides()), 0);
    assert.equal(nombreFiltresActifs(avec((x) => { x.aspects.add("Justice"); x.stats.hp.add("1"); x.texte = "a"; })), 3);
});
