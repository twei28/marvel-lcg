// ordre-libre.js — la campagne « Fear No Evil » (livret mc60 p. 8-9) : cinq
// affaires jouables dans l'ordre choisi, chacune contre un vilain UNDERLING,
// des marques de progression tirées au hasard avant chaque partie, et Kingpin
// quand tout est résolu. Module PUR : ni DOM, ni réseau, ni moteur ; il lit et
// rend un carnet, pour être éprouvé par `tools/tests-lanceur/ordre-libre.test.mjs`.
//
// Les clés du carnet sont celles que le moteur relit
// (src/cards/pack/fne/campaign.py) : « Completed Scenarios », « Failed
// Scenarios », « Progress: <affaire> », « Villain: <affaire> ».
"use strict";

export const CLE_COMPLETED = "Completed Scenarios";
export const CLE_FAILED = "Failed Scenarios";
export const MARQUES_POUR_ECHOUER = 3;

const liste = (carnet, cle) => String((carnet || {})[cle] || "").split(";").filter(Boolean);
const entier = (carnet, cle) => parseInt((carnet || {})[cle] || "0", 10) || 0;

/** Les affaires (scénarios interchangeables) et le scénario final d'une définition. */
export function affaires(definition) {
    return (definition.scenarios || []).filter((s) => s.manigance);
}
export function scenarioFinal(definition) {
    return (definition.scenarios || []).find((s) => s.final) || null;
}

/** État d'une affaire d'après le carnet : "completed" | "failed" | "ouverte". */
export function etatAffaire(carnet, id) {
    if (liste(carnet, CLE_COMPLETED).includes(id)) return "completed";
    if (liste(carnet, CLE_FAILED).includes(id)) return "failed";
    return "ouverte";
}
export function marques(carnet, id) {
    return entier(carnet, "Progress: " + id);
}
export function vilainDe(carnet, id) {
    return (carnet || {})["Villain: " + id] || "";
}
export function affairesOuvertes(definition, carnet) {
    return affaires(definition).filter((a) => etatAffaire(carnet, a.id) === "ouverte");
}
/** Kingpin n'est proposé que lorsque les cinq affaires sont Completed ou Failed. */
export function kingpinDisponible(definition, carnet) {
    return affairesOuvertes(definition, carnet).length === 0;
}

/**
 * Étapes 1 à 3 de « Campaign Setup » (p. 9) : parmi les affaires encore
 * ouvertes, deux sont tirées au hasard et progressent d'une marque (s'il n'en
 * reste qu'une, elle progresse de deux). Trois marques : l'affaire est Failed.
 * Rend { carnet, tirees, echouees } sans modifier l'entrée. `hasard` est un
 * générateur dans [0, 1) (Math.random par défaut) pour que les tests le fixent.
 */
export function tirerLaProgression(definition, carnet, hasard = Math.random) {
    const suivant = Object.assign({}, carnet || {});
    const ouvertes = affairesOuvertes(definition, suivant).map((a) => a.id);
    const tirees = [];
    const echouees = [];
    if (ouvertes.length === 0) return { carnet: suivant, tirees, echouees };
    let nbMarques;
    if (ouvertes.length === 1) {
        tirees.push(ouvertes[0]);
        nbMarques = { [ouvertes[0]]: 2 };
    } else {
        const reste = ouvertes.slice();
        for (let k = 0; k < 2; k++) {
            const i = Math.min(reste.length - 1, Math.floor(hasard() * reste.length));
            tirees.push(reste.splice(i, 1)[0]);
        }
        nbMarques = Object.fromEntries(tirees.map((id) => [id, 1]));
    }
    for (const id of tirees) {
        const n = marques(suivant, id) + nbMarques[id];
        suivant["Progress: " + id] = String(n);
        if (n >= MARQUES_POUR_ECHOUER) {
            echouees.push(id);
            suivant[CLE_FAILED] = [...new Set([...liste(suivant, CLE_FAILED), id])].join(";");
        }
    }
    return { carnet: suivant, tirees, echouees };
}

/**
 * Étape 5 : le vilain d'une affaire. Déjà enregistré → imposé. Sinon, au
 * premier parcours, le premier vilain de la liste recommandée qui n'est encore
 * inscrit pour aucune affaire ; les autres restent proposés (le livret laisse
 * le choix au hasard aux parcours suivants). Rend { impose, suggere, choix }.
 */
export function vilainsPossibles(definition, carnet, id) {
    const tous = (definition.vilains || []).slice().sort((a, b) => (a.ordre || 0) - (b.ordre || 0));
    const inscrit = vilainDe(carnet, id);
    if (inscrit) return { impose: inscrit, suggere: inscrit, choix: [inscrit] };
    const pris = new Set(affaires(definition).map((a) => vilainDe(carnet, a.id)).filter(Boolean));
    const libres = tous.filter((v) => !pris.has(v.id)).map((v) => v.id);
    return { impose: null, suggere: libres[0] || tous[0].id, choix: libres.length ? libres : tous.map((v) => v.id) };
}

/** Le carnet une fois le vilain d'une affaire arrêté (étape 5, « record the name »). */
export function inscrireLeVilain(carnet, id, vilain) {
    return Object.assign({}, carnet || {}, { ["Villain: " + id]: vilain });
}

/** L'identifiant de scénario du catalogue pour une affaire et son vilain. */
export function scenarioDuCatalogue(affaire, vilain) {
    if (affaire.catalogue) return affaire.catalogue;
    return affaire.id + "_" + vilain;
}

/**
 * Une défaite. Affaire : rien en standard ; en campagne experte l'affaire
 * progresse d'une marque (encart DEFEAT, p. 13-21). Kingpin : en standard on
 * rejoue ; en expert on retourne un environnement Completed côté Failed (le
 * joueur choisit `retournee`) et on rejoue, faute d'environnement Completed la
 * campagne est perdue. Rend { carnet, perdue, echouee, aChoisir }.
 */
export function appliquerLaDefaite(definition, carnet, scenarioId, expert, retournee) {
    const suivant = Object.assign({}, carnet || {});
    const final = scenarioFinal(definition);
    if (final && scenarioId === final.id) {
        if (!expert) return { carnet: suivant, perdue: false, echouee: null, aChoisir: [] };
        const completees = liste(suivant, CLE_COMPLETED);
        if (completees.length === 0) return { carnet: suivant, perdue: true, echouee: null, aChoisir: [] };
        if (!retournee || !completees.includes(retournee)) {
            return { carnet: suivant, perdue: false, echouee: null, aChoisir: completees };
        }
        suivant[CLE_COMPLETED] = completees.filter((x) => x !== retournee).join(";");
        suivant[CLE_FAILED] = [...new Set([...liste(suivant, CLE_FAILED), retournee])].join(";");
        return { carnet: suivant, perdue: false, echouee: retournee, aChoisir: [] };
    }
    if (!expert) return { carnet: suivant, perdue: false, echouee: null, aChoisir: [] };
    const n = marques(suivant, scenarioId) + 1;
    suivant["Progress: " + scenarioId] = String(n);
    let echouee = null;
    if (n >= MARQUES_POUR_ECHOUER) {
        echouee = scenarioId;
        suivant[CLE_FAILED] = [...new Set([...liste(suivant, CLE_FAILED), scenarioId])].join(";");
    }
    return { carnet: suivant, perdue: false, echouee, aChoisir: [] };
}
