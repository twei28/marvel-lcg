// favoris.js — decks mis de côté, mémorisés dans le navigateur.
//
// Le stockage est un PARAMÈTRE (défaut : localStorage) : sans ça le module
// serait intestable hors navigateur, et un localStorage indisponible (mode
// privé strict) ferait planter l'écran de préparation entier.
"use strict";

export const CLE_FAVORIS = "marvelcdb_favoris";

function stockageParDefaut() {
    try {
        return window.localStorage;
    } catch {
        return { getItem: () => null, setItem: () => {} };
    }
}

export function lireFavoris(stockage) {
    const st = stockage || stockageParDefaut();
    try {
        const brut = JSON.parse(st.getItem(CLE_FAVORIS) || "[]");
        return Array.isArray(brut) ? brut.map(String) : [];
    } catch {
        return [];
    }
}

export function estFavori(id, stockage) {
    return lireFavoris(stockage).includes(String(id));
}

/** Ajoute ou retire, puis rend la liste à jour. */
export function basculerFavori(id, stockage) {
    const st = stockage || stockageParDefaut();
    const cle = String(id);
    const liste = lireFavoris(st);
    const suite = liste.includes(cle) ? liste.filter((x) => x !== cle) : [...liste, cle];
    try {
        st.setItem(CLE_FAVORIS, JSON.stringify(suite));
    } catch {
        /* quota plein ou stockage refusé : le favori ne survivra pas à la
           session, ce qui vaut mieux qu'une exception dans l'écran. */
    }
    return suite;
}
