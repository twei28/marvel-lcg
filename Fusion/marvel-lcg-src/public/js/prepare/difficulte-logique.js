// difficulte-logique.js — la logique PURE de la page « Difficulté et sets modulaires » (30/10/2026).
//
// Ni DOM ni stockage : testée par `node --test tools/tests-lanceur/difficulte-logique.test.mjs`.
// Les propositions viennent de villaintheory.js (généré par tools/importer_villaintheory.py).
"use strict";

/** Sans accents, sans casse, sans ponctuation : pour chercher « alerte bombe » comme « Alerte à la Bombe ». */
export function normaliser(texte) {
    return String(texte || "")
        .normalize("NFD").replace(/[̀-ͯ]/g, "")
        .toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

/** Les propositions d'un scénario : celles qui le citent, les « Default modular » en tête puis par difficulté. */
export function combinaisonsDuScenario(scenarioId, donnees) {
    const liste = (donnees && donnees.combinaisons) || [];
    return liste
        .filter((c) => c.scenarios.includes(scenarioId))
        .sort((a, b) => (b.defaut - a.defaut) || (a.difficulte - b.difficulte) || a.nom.localeCompare(b.nom));
}

/** Une proposition se joue-t-elle ? Non si un de ses sets n'existe pas dans le jeu. */
export function estJouable(combinaison) {
    return !(combinaison.manquants && combinaison.manquants.length);
}

/** Pourquoi elle est grisée (texte français, vide si elle se joue). */
export function raisonGrisee(combinaison) {
    if (estJouable(combinaison)) return "";
    return combinaison.manquants.length === 1
        ? "Set « " + combinaison.manquants[0] + " » absent du jeu"
        : "Sets absents du jeu : " + combinaison.manquants.join(", ");
}

/** « +2 », « −1 », « +0 » ; avec « ? » quand l'auteur n'est pas sûr. */
export function libelleDifficulte(valeur, incertain = false) {
    if (valeur === null || valeur === undefined) return "";
    const signe = valeur < 0 ? "−" : "+";
    return signe + Math.abs(valeur) + (incertain ? "?" : "");
}

function memeEnsemble(a, b) {
    return a.length === b.length && a.every((x) => b.includes(x));
}

/**
 * La difficulté estimée de ce que le joueur a choisi. On ne calcule rien : on lit la note d'une proposition
 * VillainTheory quand la sélection est EXACTEMENT la sienne ; sans proposition, la sélection recommandée vaut +0.
 * Le niveau (Standard II, Expert…) n'entre pas en compte : la note de l'auteur ne le dit pas.
 * Rend { valeur, incertain, source: "villaintheory" | "recommande" | null, nom }.
 */
export function difficulteEstimee(selection, recommandes, propositions) {
    const choisis = [...new Set(selection)];
    const trouvee = propositions.find((c) => estJouable(c) && !c.defaut && memeEnsemble(c.sets, choisis));
    if (trouvee) return { valeur: trouvee.difficulte, incertain: !!trouvee.incertain, source: "villaintheory", nom: trouvee.nom };
    if (memeEnsemble(recommandes, choisis)) return { valeur: 0, incertain: false, source: "recommande", nom: "" };
    return { valeur: null, incertain: false, source: null, nom: "" };
}

/**
 * Les sets rangés par boîte, boîtes dans l'ordre donné, sets par nom dans chaque boîte.
 * @param sets      [{ name, displayName }]
 * @param boiteDe   (nomDeFichier) => clé de boîte ("1. Core Set") ou ""
 * @param ordre     (cléDeBoîte) => nombre (tri des boîtes)
 * @param titre     (cléDeBoîte) => titre affiché
 * Rend [{ cle, titre, sets }] ; les sets sans boîte connue vont dans une dernière boîte « autres ».
 */
export function grouperParBoite(sets, boiteDe, ordre, titre, titreAutres = "Autres") {
    const parBoite = new Map();
    for (const s of sets) {
        const cle = boiteDe(s.name) || "";
        if (!parBoite.has(cle)) parBoite.set(cle, []);
        parBoite.get(cle).push(s);
    }
    const groupes = [...parBoite.entries()].map(([cle, liste]) => ({
        cle,
        titre: cle ? titre(cle) : titreAutres,
        sets: liste.sort((a, b) => a.displayName.localeCompare(b.displayName)),
    }));
    return groupes.sort((a, b) => (a.cle === "") - (b.cle === "") || ordre(a.cle) - ordre(b.cle));
}

/** Garde les sets dont le nom OU la boîte contient la recherche ; une recherche vide garde tout. */
export function filtrerGroupes(groupes, recherche) {
    const q = normaliser(recherche);
    if (!q) return groupes;
    return groupes
        .map((g) => (normaliser(g.titre).includes(q) ? g : { ...g, sets: g.sets.filter((s) => normaliser(s.displayName).includes(q)) }))
        .filter((g) => g.sets.length);
}

/** Bascule un set dans la sélection ; rend la nouvelle liste (sans doublon, ordre conservé). */
export function basculerSet(selection, nom) {
    return selection.includes(nom) ? selection.filter((s) => s !== nom) : [...selection, nom];
}

/** Le plus de sets modulaires qu'une partie accepte. Les règles en permettent plus que la boîte n'en
 *  recommande (Règles de référence 1.7) et les propositions VillainTheory montent à 7 : le plafond de la
 *  préparation est donc de 8, sauf scénario qui en recommande davantage. */
export const MAX_SETS_MODULAIRES = 8;
export function nombreMaxDeSets(scenario) {
    const prevu = scenario && scenario.modularSlots ? scenario.modularSlots.max : 0;
    return Math.max(prevu || 0, MAX_SETS_MODULAIRES);
}
