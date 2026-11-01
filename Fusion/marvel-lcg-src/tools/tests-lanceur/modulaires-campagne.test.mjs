// Tests du module pur `public/js/campagne/modulaires.js` (28/10/2026) : le choix des sets modulaires d'un scénario de
// campagne MojoMania (livret p.13 et p.17 : « vous ne pouvez pas choisir les sets cochés au carnet »).
//
//     node --test tools/tests-lanceur/modulaires-campagne.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { nombreDeModules, listeDuCarnet, proposerModules } from "../../public/js/campagne/modulaires.js";

const RESERVE = ["crime", "fantasy", "horror", "sci_fi", "sitcom", "western"];
const premier = (liste) => liste[0];

test("nombreDeModules : un entier tel quel, « joueurs+1 » selon le nombre de héros", () => {
    assert.equal(nombreDeModules(3, 2), 3);
    assert.equal(nombreDeModules("joueurs+1", 1), 2);
    assert.equal(nombreDeModules("joueurs+1", 4), 5);
    assert.equal(nombreDeModules("joueurs", 3), 3);
    assert.equal(nombreDeModules("n'importe quoi", 3), 0);
});

test("listeDuCarnet : « a;b » en tableau, sans vide ni doublon", () => {
    assert.deepEqual(listeDuCarnet("crime;fantasy"), ["crime", "fantasy"]);
    assert.deepEqual(listeDuCarnet("crime;;crime"), ["crime"]);
    assert.deepEqual(listeDuCarnet(undefined), []);
});

test("scénario 1 (hasard, 1 set) : un seul set de la réserve, jamais un autre nombre", () => {
    const r = proposerModules({ reserve: RESERVE, utilises: [], nombre: 1, hasard: true, tirer: premier });
    assert.deepEqual(r, { modules: ["crime"] });
});

test("scénario 2 (3 sets au choix) : le joueur choisit parmi les 5 sets non cochés", () => {
    const r = proposerModules({ reserve: RESERVE, utilises: ["crime"], nombre: 3 });
    assert.deepEqual(r, { choix: { parmi: ["fantasy", "horror", "sci_fi", "sitcom", "western"], nombre: 3, imposes: [] } });
});

test("un set coché n'est jamais proposé tant qu'il en reste assez de libres", () => {
    const r = proposerModules({ reserve: RESERVE, utilises: ["crime", "fantasy", "horror", "sci_fi"], nombre: 2 });
    assert.deepEqual(r, { modules: ["sitcom", "western"] });
});

test("scénario 3, un joueur (2 sets) : les deux sets restants partent d'office, sans choix", () => {
    const r = proposerModules({ reserve: RESERVE, utilises: ["crime", "fantasy", "horror", "sci_fi"], nombre: 2 });
    assert.deepEqual(r.modules.sort(), ["sitcom", "western"]);
});

test("scénario 3, quatre joueurs (5 sets) : les 2 libres partent, le joueur complète avec 3 des 4 déjà passés", () => {
    const r = proposerModules({ reserve: RESERVE, utilises: ["crime", "fantasy", "horror", "sci_fi"], nombre: 5 });
    assert.deepEqual(r, { choix: { parmi: ["crime", "fantasy", "horror", "sci_fi"], nombre: 3, imposes: ["sitcom", "western"] } });
});

test("scénario 3, trois joueurs (4 sets) : les 2 libres + 2 cochés au choix", () => {
    const r = proposerModules({ reserve: RESERVE, utilises: ["crime", "fantasy", "horror", "sci_fi"], nombre: 4 });
    assert.deepEqual(r.choix.imposes, ["sitcom", "western"]);
    assert.equal(r.choix.nombre, 2);
    assert.equal(r.choix.parmi.length, 4);
});

test("scénario 3, cinq joueurs (6 sets) : tous les sets de la réserve partent, rien à choisir", () => {
    const r = proposerModules({ reserve: RESERVE, utilises: ["crime", "fantasy", "horror", "sci_fi"], nombre: 6 });
    assert.deepEqual(r.modules.sort(), [...RESERVE].sort());
});

test("réserve épuisée en tirage au sort : on retombe sur un set déjà passé plutôt que de ne rien envoyer", () => {
    const r = proposerModules({ reserve: ["crime"], utilises: ["crime"], nombre: 1, hasard: true, tirer: premier });
    assert.deepEqual(r, { modules: ["crime"] });
});
