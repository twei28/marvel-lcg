// catalogue-carnet.js — le scenario du catalogue qu'une etape de campagne doit lancer, quand le CARNET le decide.
//
// « La ville ne dort jamais » (Punisher MC×DC 2026) : le combat 2 depend du lieu de la derniere piste et du Trafiquant d'armes du
// combat 1 (20 scenarios), le combat 3 du subordonne affronte au combat 2 (4 scenarios). Le fichier de la campagne declare la regle
// sous `catalogue_selon_carnet` : un `modele` (« tracking_the_buyer_{manigance}_{sous_fifre} »), des `variables` (la cle du carnet
// lue et sa table de correspondance) et un `defaut` si le carnet est incomplet. Fonction PURE : aucun acces au DOM ni au reseau.
"use strict";

/** La valeur d'une variable d'apres le carnet : correspondance exacte, puis sans tenir compte de la casse. null si inconnue. */
function valeurDeLaVariable(variable, carnet) {
    const lu = String((carnet || {})[variable.cle] || "").trim();
    if (!lu) return null;
    const table = variable.table || {};
    if (Object.prototype.hasOwnProperty.call(table, lu)) return table[lu];
    const bas = lu.toLowerCase();
    for (const [cle, valeur] of Object.entries(table)) {
        if (cle.toLowerCase() === bas) return valeur;
    }
    return null;
}

/**
 * L'id du scenario du catalogue pour une etape, ou null si l'etape n'a pas de regle de carnet.
 * Carnet incomplet : le `defaut` du fichier (jamais d'exception : l'ecran doit pouvoir afficher l'etape).
 * `expert` ajoute le suffixe `_expert` (les scenarios generes existent dans les deux difficultes).
 */
export function catalogueSelonCarnet(scenario, carnet, expert) {
    const regle = scenario && scenario.catalogue_selon_carnet;
    if (!regle) return null;
    const suffixe = expert ? "_expert" : "";
    let id = regle.modele;
    for (const [nom, variable] of Object.entries(regle.variables || {})) {
        const valeur = valeurDeLaVariable(variable, carnet);
        if (valeur === null) return regle.defaut ? regle.defaut + suffixe : null;
        id = id.split("{" + nom + "}").join(valeur);
    }
    return id + suffixe;
}

/** Le scenario du catalogue d'une etape : la regle du carnet, sinon `catalogue`, sinon l'id de l'etape. */
export function scenarioDuCatalogueDeLEtape(scenario, carnet, expert) {
    return catalogueSelonCarnet(scenario, carnet, expert) || scenario.catalogue || scenario.id;
}
