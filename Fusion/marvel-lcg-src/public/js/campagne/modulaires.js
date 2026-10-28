// modulaires.js — le choix des sets MODULAIRES d'un scénario de campagne (MojoMania, 28/10/2026).
//
// Module pur, sans DOM : testé par `node --test tools/tests-lanceur/modulaires-campagne.test.mjs`.
//
// Le livret de MojoMania (p.13 et p.17) dit, à la mise en place des scénarios 2 et 3 : « Vous ne pouvez pas choisir les sets
// modulaires cochés au carnet pour ce scénario. S'il n'en reste pas assez, vous pouvez choisir des sets cochés une fois
// tous les autres choisis. » Et au scénario 1 (carte 39002a) : « 1 set modulaire au hasard parmi ceux du pack ».
// Le moteur, lui, ne choisit rien : il prend les sets que l'écran lui envoie. C'est donc ici que la règle se tient.
//
// La définition de la campagne (data/campagnes/<code>.json) porte :
//   modulaires: {
//     reserve:      ["crime", "fantasy", ...],            // les sets du pack
//     cle_utilises: "Modular Sets Used",                  // la clé du carnet (liste « a;b »), écrite par le moteur
//     cle_injectee: "Modular Sets This Scenario",         // la clé que l'écran pose au lancement (liste « a;b »)
//     par_scenario: { magog: { nombre: 1, hasard: true }, spiral: { nombre: 3 }, mojo: { nombre: "joueurs+1" } }
//   }
"use strict";

/** « 3 » ou « "joueurs+1" » -> un entier, pour `nbJoueurs` héros. */
export function nombreDeModules(nombre, nbJoueurs) {
    if (typeof nombre === "number") return nombre;
    const m = /^joueurs\s*([+-]\s*\d+)?$/.exec(String(nombre || "").trim());
    if (!m) return 0;
    return nbJoueurs + (m[1] ? Number(m[1].replace(/\s+/g, "")) : 0);
}

/** La liste « a;b;c » du carnet, en tableau sans vide ni doublon. */
export function listeDuCarnet(valeur) {
    const vus = [];
    for (const x of String(valeur || "").split(";")) if (x && !vus.includes(x)) vus.push(x);
    return vus;
}

/**
 * Ce que l'écran doit faire pour ce scénario.
 *
 * Rend `{ modules }` quand la règle tranche seule, ou `{ choix: { parmi, nombre, imposes } }` quand le joueur doit
 * choisir `nombre` sets parmi `parmi` (en plus des `imposes`, qui partent d'office).
 *
 * @param {object} p
 * @param {string[]} p.reserve    les sets du pack
 * @param {string[]} p.utilises   les sets déjà cochés au carnet
 * @param {number}   p.nombre     combien de sets ce scénario exige
 * @param {boolean} [p.hasard]    tirage au sort (scénario 1) au lieu d'un choix
 * @param {(liste: string[]) => string} [p.tirer]  tire un élément (Math.random par défaut) : injecté par les tests
 */
export function proposerModules({ reserve, utilises, nombre, hasard = false, tirer }) {
    const tire = tirer || ((liste) => liste[Math.floor(Math.random() * liste.length)]);
    const cochees = new Set(utilises);
    const libres = reserve.filter((m) => !cochees.has(m));
    const dejaVus = reserve.filter((m) => cochees.has(m));
    const tirerParmi = (liste, k) => {
        const restants = [...liste];
        const choisis = [];
        while (choisis.length < k && restants.length) {
            const un = tire(restants);
            choisis.push(un);
            restants.splice(restants.indexOf(un), 1);
        }
        return choisis;
    };

    if (nombre <= 0) return { modules: [] };
    if (libres.length >= nombre) {
        if (hasard) return { modules: tirerParmi(libres, nombre) };
        if (libres.length === nombre) return { modules: libres };
        return { choix: { parmi: libres, nombre, imposes: [] } };
    }
    // Pas assez de sets libres : tous les libres partent, puis on complète avec des sets déjà passés.
    const manque = nombre - libres.length;
    if (hasard) return { modules: [...libres, ...tirerParmi(dejaVus, manque)] };
    if (dejaVus.length <= manque) return { modules: [...libres, ...dejaVus] };
    return { choix: { parmi: dejaVus, nombre: manque, imposes: libres } };
}
