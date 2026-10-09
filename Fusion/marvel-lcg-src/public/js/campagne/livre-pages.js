// livre-pages.js : quelles pages du livret le « livre ouvert » de l'ecran de
// campagne montre, selon l'etape. Module PUR, teste par
// `node --test tools/tests-lanceur/livre-pages.test.mjs`.
//
// Decisions de l'utilisateur (09/10/2026, .planning/todos/2026-10-09-ecran-campagne-livre-ouvert.md) :
//   debut de campagne : couverture, intro et regles de la campagne, puis le scenario 1 ;
//   entre deux scenarios : epilogue du precedent, puis intro et regles du suivant ;
//   fin : epilogue final ;
//   un onglet « Regles de campagne » toujours disponible.
// Les libelles sont des cles francaises : l'ecran les passe a t().
"use strict";

export const COUVERTURE = "00-couverture.jpg";

const bd = (fichier) => ({ fichier, classe: "bd" });
const regle = (fichier) => ({ fichier, classe: "regles" });

/** Une planche qui termine un scenario ET ouvre le suivant n'est pas dupliquee
 *  par pages_livret.py : le scenario suivant la reference comme intro. */
function sansDoublon(pages) {
    const vues = new Set();
    return pages.filter((p) => !vues.has(p.fichier) && vues.add(p.fichier));
}

/** Les pages valables pour toute la campagne : regles, et regles expertes en campagne experte. */
export function pagesDeCampagne(definition, expert) {
    return sansDoublon([
        ...(definition.pages_regles || []).map(regle),
        ...(expert ? (definition.pages_expert || []).map(regle) : []),
    ]);
}

/** Les onglets du livre d'une campagne lineaire.
 *  `index` : scenario a jouer ; `finie`, `perdue` : etat de la campagne. */
export function ongletsLineaires(definition, { index, finie, perdue, expert }) {
    const scenarios = definition.scenarios || [];
    const campagne = pagesDeCampagne(definition, expert);
    let etape;
    let libelle;
    if (finie) {
        // Pas de planche d'epilogue sur une defaite : elle raconte la victoire.
        const dernier = scenarios[scenarios.length - 1] || {};
        etape = perdue ? [] : ((dernier.pages || {}).epilogue || []).map(bd);
        libelle = "Épilogue";
    } else {
        const pages = (scenarios[index] || {}).pages || {};
        const courant = [...(pages.intro || []).map(bd), ...(pages.regles || []).map(regle)];
        if (index === 0) {
            etape = [bd(COUVERTURE), ...(definition.pages_intro || []).map(bd), ...campagne, ...courant];
            libelle = "Début de campagne";
        } else {
            const precedent = ((scenarios[index - 1] || {}).pages || {}).epilogue || [];
            etape = [...precedent.map(bd), ...courant];
            libelle = "Ce scénario";
        }
    }
    return onglets(sansDoublon(etape), libelle, campagne);
}

/** Les onglets du livre d'une campagne en ordre libre (Fear No Evil) : la
 *  planche d'ouverture, puis l'intro et les regles de l'affaire montree. */
export function ongletsLibres(definition, { affaire, expert }) {
    const pages = (affaire && affaire.pages) || {};
    const etape = sansDoublon([
        ...(definition.pages_intro || []).map(bd),
        ...(pages.intro || []).map(bd),
        ...(pages.regles || []).map(regle),
    ]);
    return onglets(etape, "Le livret", pagesDeCampagne(definition, expert));
}

function onglets(etape, libelle, campagne) {
    const liste = [];
    if (etape.length) liste.push({ id: "etape", libelle, pages: etape });
    if (campagne.length) liste.push({ id: "campagne", libelle: "Règles de la campagne", pages: campagne });
    return liste;
}

/** Premiere page affichee pour un debut demande : les doubles pages commencent
 *  sur un indice pair (0-1, 2-3...), une page seule sur n'importe lequel. */
export function caler(debut, total, simple) {
    if (total <= 0) return 0;
    const pas = simple ? 1 : 2;
    const max = Math.floor((total - 1) / pas) * pas;
    const borne = Math.max(0, Math.min(debut, max));
    return borne - (borne % pas);
}

/** Le compteur affiche : « 3-4 / 7 », ou « 5 / 7 » pour une page seule. */
export function compteur(debut, total, simple) {
    if (total <= 0) return "";
    const fin = simple ? debut + 1 : Math.min(debut + 2, total);
    return (fin > debut + 1 ? (debut + 1) + "-" + fin : String(debut + 1)) + " / " + total;
}
