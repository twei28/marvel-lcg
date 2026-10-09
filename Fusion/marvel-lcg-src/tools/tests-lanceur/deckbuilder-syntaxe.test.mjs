// node --test tools/tests-lanceur/deckbuilder-syntaxe.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { analyser, satisfait, satisfaitTout, nombreDe } from "../../public/js/deckbuilder/syntaxe.js";

const mariaHill = { name: "* Maria Hill", type: "Ally", class: "Leadership", cost: "2", package_name: "core",
    traits: ["S.H.I.E.L.D."], desc: { Cost: "2", HP: "2", ATK: "1*", THW: "2*" } };
const urgence = { name: "Emergency", type: "Event", class: "Basic", cost: "0", package_name: "core", traits: ["THWART"], desc: { Cost: "0" } };
const xCout = { name: "Unleashed", type: "Event", class: "Aggression", cost: "X", traits: [], desc: { Cost: "X" } };

test("reconnaît les clés courtes et garde le texte libre", () => {
    const r = analyser("t:shield c:2 atk>=1 hill");
    assert.deepEqual(r.criteres.map((c) => [c.cle, c.op, c.valeur]),
        [["trait", "=", "shield"], ["cout", "=", 2], ["atk", ">=", 1]]);
    assert.equal(r.texte, "hill");
    assert.deepEqual(r.erreurs, []);
});

test("accepte les clés et valeurs françaises, avec préfixe et sans accents", () => {
    const r = analyser("a:commandement ty:allié pv>=2 u:oui");
    assert.deepEqual(r.criteres.map((c) => c.valeur), ["Leadership", "Ally", 2, true]);
    assert.equal(satisfaitTout(mariaHill, r.criteres), true);
    assert.equal(satisfaitTout(urgence, r.criteres), false);
});

test("compare les statistiques imprimées avec étoile", () => {
    assert.equal(nombreDe("2*"), 2);
    assert.equal(satisfait(mariaHill, { cle: "thw", op: ">=", valeur: 2 }), true);
    assert.equal(satisfait(mariaHill, { cle: "atk", op: ">", valeur: 1 }), false);
});

test("une carte sans la statistique demandée ne passe pas", () => {
    assert.equal(satisfait(urgence, { cle: "atk", op: ">=", valeur: 0 }), false);
});

test("le coût X se cherche par c:x", () => {
    const r = analyser("c:x");
    assert.equal(satisfaitTout(xCout, r.criteres), true);
    assert.equal(satisfaitTout(urgence, r.criteres), false);
});

test("une valeur illisible est signalée et ignorée", () => {
    const r = analyser("c:abc a:inconnu atk>trois");
    assert.deepEqual(r.criteres, []);
    assert.deepEqual(r.erreurs, ["c:abc", "a:inconnu", "atk>trois"]);
});

test("une clé inconnue reste du texte libre", () => {
    const r = analyser("spider:man");
    assert.deepEqual(r.criteres, []);
    assert.equal(r.texte, "spider:man");
});

test("guillemets pour un trait de plusieurs mots", () => {
    const r = analyser('t:"s.h.i.e.l.d" mansion');
    assert.equal(r.criteres[0].valeur, "s.h.i.e.l.d");
    assert.equal(satisfaitTout(mariaHill, r.criteres), true);
    assert.equal(r.texte, "mansion");
});
