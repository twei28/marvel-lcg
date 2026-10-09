// node --test tools/tests-lanceur/livre-pages.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { ongletsLineaires, ongletsLibres, caler, compteur, COUVERTURE } from "../../public/js/campagne/livre-pages.js";

const def = {
    pages_regles: ["00-campagne-regles-1.jpg", "00-campagne-regles-2.jpg"],
    pages_expert: ["00-expert.jpg"],
    scenarios: [
        { id: "a", pages: { intro: ["01-intro.jpg"], regles: ["01-regles.jpg"], epilogue: ["01-epilogue.jpg"] } },
        { id: "b", pages: { intro: ["01-epilogue.jpg", "02-intro.jpg"], regles: ["02-regles.jpg"], epilogue: ["02-epilogue.jpg"] } },
    ],
};
const fichiers = (o) => o.pages.map((p) => p.fichier);

test("debut de campagne : couverture, regles de campagne, puis scenario 1", () => {
    const [etape, campagne] = ongletsLineaires(def, { index: 0, finie: false, perdue: false, expert: false });
    assert.equal(etape.libelle, "Début de campagne");
    assert.deepEqual(fichiers(etape), [COUVERTURE, "00-campagne-regles-1.jpg", "00-campagne-regles-2.jpg", "01-intro.jpg", "01-regles.jpg"]);
    assert.deepEqual(fichiers(campagne), ["00-campagne-regles-1.jpg", "00-campagne-regles-2.jpg"]);
});

test("entre deux scenarios : epilogue du precedent sans doublon, puis le suivant", () => {
    const [etape] = ongletsLineaires(def, { index: 1, finie: false, perdue: false, expert: false });
    assert.equal(etape.libelle, "Ce scénario");
    assert.deepEqual(fichiers(etape), ["01-epilogue.jpg", "02-intro.jpg", "02-regles.jpg"]);
});

test("fin : epilogue final, rien sur une defaite", () => {
    assert.deepEqual(fichiers(ongletsLineaires(def, { index: 2, finie: true, perdue: false })[0]), ["02-epilogue.jpg"]);
    const perdue = ongletsLineaires(def, { index: 2, finie: true, perdue: true });
    assert.equal(perdue.length, 1);
    assert.equal(perdue[0].id, "campagne");
});

test("campagne experte : les regles expertes rejoignent l'onglet campagne", () => {
    const o = ongletsLineaires(def, { index: 1, finie: false, perdue: false, expert: true });
    assert.deepEqual(fichiers(o[1]), ["00-campagne-regles-1.jpg", "00-campagne-regles-2.jpg", "00-expert.jpg"]);
});

test("ordre libre : planche d'ouverture puis l'affaire montree", () => {
    const libre = { pages_intro: ["00-intro.jpg"], pages_regles: [], scenarios: [] };
    const o = ongletsLibres(libre, { affaire: { pages: { intro: ["03-i.jpg"], regles: ["03-r.jpg"] } }, expert: false });
    assert.equal(o.length, 1);
    assert.deepEqual(fichiers(o[0]), ["00-intro.jpg", "03-i.jpg", "03-r.jpg"]);
    assert.deepEqual(ongletsLibres({ pages_regles: [] }, { affaire: null }), []);
});

test("doubles pages calees sur un indice pair, page seule libre", () => {
    assert.equal(caler(3, 5, false), 2);
    assert.equal(caler(9, 5, false), 4);
    assert.equal(caler(-2, 5, false), 0);
    assert.equal(caler(3, 5, true), 3);
    assert.equal(caler(0, 0, false), 0);
});

test("compteur", () => {
    assert.equal(compteur(0, 5, false), "1-2 / 5");
    assert.equal(compteur(4, 5, false), "5 / 5");
    assert.equal(compteur(2, 5, true), "3 / 5");
    assert.equal(compteur(0, 1, false), "1 / 1");
});

test("toutes les campagnes : chaque page declaree reste dans un onglet a une etape", () => {
    const dossier = new URL("../../data/campagnes/", import.meta.url);
    for (const nom of readdirSync(dossier).filter((f) => f.endsWith(".json"))) {
        const d = JSON.parse(readFileSync(new URL(nom, dossier), "utf8"));
        const vues = new Set();
        const n = (d.scenarios || []).length;
        const ajouter = (liste) => liste.forEach((o) => o.pages.forEach((p) => vues.add(p.fichier)));
        if (d.ordre_libre) {
            for (const s of d.scenarios || []) ajouter(ongletsLibres(d, { affaire: s, expert: true }));
        } else {
            for (let i = 0; i < n; i++) ajouter(ongletsLineaires(d, { index: i, finie: false, perdue: false, expert: true }));
            ajouter(ongletsLineaires(d, { index: n, finie: true, perdue: false, expert: true }));
        }
        const declarees = new Set([
            ...(d.pages_regles || []), ...(d.pages_expert || []), ...(d.pages_intro || []),
            ...(d.scenarios || []).flatMap((s) => Object.values(s.pages || {}).flat()),
        ]);
        // Les epilogues des scenarios intermediaires d'une campagne en ordre
        // libre sont montres par le panneau de recompenses du plateau.
        if (d.ordre_libre) for (const s of d.scenarios || []) for (const f of (s.pages || {}).epilogue || []) declarees.delete(f);
        const manquent = [...declarees].filter((f) => !vues.has(f));
        assert.deepEqual(manquent, [], `${nom} : pages jamais montrees`);
    }
});
