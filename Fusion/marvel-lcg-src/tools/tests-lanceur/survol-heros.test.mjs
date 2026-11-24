// Tests du module pur `public/js/prepare/survol-heros.js`.
//
//     node --test tools/tests-lanceur/survol-heros.test.mjs
//
// Bug signalé sur le Discord (#bugs, 26/10/2026) : « dans la fenêtre héros, il n'est pas possible de cliquer sur le bouton "voir les
// cartes d'un héros ou biographie" car dès que je bouge la souris ça change le héros ». La scène de gauche montre le héros SURVOLÉ, avec
// son bouton « Voir ses cartes » : quitter la tuile la redessinait aussitôt avec le héros du siège (ou le vide), et chaque tuile
// croisée en chemin la changeait encore. Le survol doit donc avoir de l'INTENTION : on retient le dernier héros regardé le temps de
// rejoindre la scène.
import { test } from "node:test";
import assert from "node:assert/strict";
import { creerSurvolHeros } from "../../public/js/prepare/survol-heros.js";

/** Un minuteur factice : le temps n'avance que quand on le dit. */
function banc(options = {}) {
    let maintenant = 0;
    let suivant = 1;
    const attente = new Map();
    const minuteur = {
        set(fn, ms) { const id = suivant++; attente.set(id, { fn, a: maintenant + ms }); return id; },
        clear(id) { attente.delete(id); },
    };
    const journal = [];
    const survol = creerSurvolHeros({
        afficher: (h) => journal.push(["afficher", h]),
        revenir: () => journal.push(["revenir"]),
        minuteur,
        ...options,
    });
    const avancer = (ms) => {
        const fin = maintenant + ms;
        for (;;) {
            const prets = [...attente.entries()].filter(([, t]) => t.a <= fin).sort((x, y) => x[1].a - y[1].a);
            if (!prets.length) break;
            const [id, t] = prets[0];
            attente.delete(id);
            maintenant = t.a;
            t.fn();
        }
        maintenant = fin;
    };
    return { survol, journal, avancer };
}

test("le premier héros survolé s'affiche tout de suite", () => {
    const { survol, journal } = banc();
    survol.entrer("A");
    assert.deepEqual(journal, [["afficher", "A"]]);
});

test("quitter la tuile ne redessine PAS la scène aussitôt : le bouton reste là pendant qu'on s'en approche", () => {
    const { survol, journal, avancer } = banc();
    survol.entrer("A");
    survol.sortir();
    avancer(300);
    assert.deepEqual(journal, [["afficher", "A"]], "la scène ne doit pas être revenue au héros du siège en 300 ms");
});

test("entrer dans la scène retient le héros regardé, même longtemps après", () => {
    const { survol, journal, avancer } = banc();
    survol.entrer("A");
    survol.sortir();
    avancer(250);
    survol.entrerDansLaScene();
    avancer(10000);
    assert.deepEqual(journal, [["afficher", "A"]]);
});

test("une tuile seulement croisée en chemin ne change pas la scène", () => {
    const { survol, journal, avancer } = banc();
    survol.entrer("A");
    survol.sortir();
    avancer(50);
    survol.entrer("B"); // la souris traverse B...
    avancer(40);
    survol.sortir(); // ...sans s'y arrêter
    avancer(30);
    survol.entrerDansLaScene();
    avancer(5000);
    assert.deepEqual(journal, [["afficher", "A"]], "B n'a été que traversée : A reste en scène");
});

test("une tuile où la souris s'arrête prend la scène", () => {
    const { survol, journal, avancer } = banc();
    survol.entrer("A");
    survol.sortir();
    avancer(50);
    survol.entrer("B");
    avancer(500);
    assert.deepEqual(journal, [["afficher", "A"], ["afficher", "B"]]);
});

test("loin de tout (ni tuile ni scène), la scène revient au héros du siège", () => {
    const { survol, journal, avancer } = banc();
    survol.entrer("A");
    survol.sortir();
    avancer(2000);
    assert.deepEqual(journal, [["afficher", "A"], ["revenir"]]);
});

test("quitter la scène la ramène au héros du siège après un délai, sauf si on retourne sur une tuile", () => {
    const { survol, journal, avancer } = banc();
    survol.entrer("A");
    survol.sortir();
    survol.entrerDansLaScene();
    survol.sortirDeLaScene();
    avancer(200);
    survol.entrer("A"); // retour sur la tuile
    avancer(5000);
    assert.deepEqual(journal, [["afficher", "A"]]);
    survol.sortir();
    avancer(2000);
    assert.deepEqual(journal.at(-1), ["revenir"]);
});

test("le clavier (focus) affiche tout de suite, sans délai d'intention", () => {
    const { survol, journal } = banc();
    survol.entrer("A");
    survol.sortir();
    survol.entrerAuClavier("B");
    assert.deepEqual(journal, [["afficher", "A"], ["afficher", "B"]]);
});

test("remettreAZero annule tout ce qui était en attente (changement d'étape)", () => {
    const { survol, journal, avancer } = banc();
    survol.entrer("A");
    survol.sortir();
    survol.remettreAZero();
    avancer(5000);
    assert.deepEqual(journal, [["afficher", "A"]], "plus de retour tardif sur une scène qui n'existe plus");
});

// Bug signalé le 27/10/2026 : après un CLIC sur un héros (choix réel, pas un survol), la souris reste sur la
// grille et le survol suivant écrasait aussitôt la scène avec un autre héros — impossible de lire la fiche de
// celui qu'on venait de choisir. `geler()` fige la scène sur le choix ; seul un nouveau `geler()` la change.
test("geler fige la scène : le survol d'autres tuiles ne la bouge plus", () => {
    const { survol, journal, avancer } = banc();
    survol.geler("A"); // clic : A choisi (la souris est encore sur sa tuile)
    survol.sortir(); // la souris quitte la tuile de A...
    survol.entrer("B"); // ...et traîne sur B, C, etc.
    avancer(5000);
    survol.sortir();
    avancer(5000);
    assert.deepEqual(journal, [["afficher", "A"]], "A reste en scène : aucun survol ni retour au siège ne doit la bouger");
});

test("geler redessine toujours, même sur le héros déjà en scène (y compris null)", () => {
    const { survol, journal } = banc();
    survol.entrer("A");
    survol.geler("A"); // déjà en scène par survol : doit quand même repasser par afficher()
    survol.geler(null); // plus personne à ce siège (multijoueur, slot suivant vide)
    assert.deepEqual(journal, [["afficher", "A"], ["afficher", "A"], ["afficher", null]]);
});

test("un nouveau clic dégèle l'ancien choix et regèle sur le nouveau", () => {
    const { survol, journal, avancer } = banc();
    survol.geler("A");
    survol.geler("B"); // un deuxième héros choisi
    survol.sortir();
    survol.entrer("C"); // survol après le deuxième choix : ne doit plus bouger non plus
    avancer(5000);
    assert.deepEqual(journal, [["afficher", "A"], ["afficher", "B"]]);
});

test("remettreAZero dégèle : le survol fonctionne de nouveau dans une nouvelle étape", () => {
    const { survol, journal } = banc();
    survol.geler("A");
    survol.remettreAZero();
    survol.entrer("B");
    assert.deepEqual(journal, [["afficher", "A"], ["afficher", "B"]]);
});
