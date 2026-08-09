// api-campagne.js — client des endpoints de campagne (server_campagne.py).
//
// Deux notions distinctes, comme cote serveur : les DEFINITIONS (les boites
// livrees avec le jeu, en lecture seule) et les CAMPAGNES du joueur (ses
// parties en cours, ecrites sur le serveur).
"use strict";

const _cacheDefinitions = new Map();

async function getJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error("HTTP " + res.status + " sur " + url);
    return res.json();
}

async function postJSON(url, corps) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corps),
    });
    if (!res.ok) {
        let detail = "";
        try { detail = (await res.json()).error || ""; } catch (e) {}
        throw new Error("HTTP " + res.status + (detail ? " — " + detail : ""));
    }
    return res.json();
}

export const apiCampagne = {
    /** Entetes de toutes les boites-campagnes jouables. */
    boites: () => getJSON("/list_campagnes_definies?"),

    /** Definition complete d'une boite. Mise en cache : elle ne change jamais. */
    async definition(code) {
        if (_cacheDefinitions.has(code)) return _cacheDefinitions.get(code);
        const def = await getJSON("/get_campagne_definition?" + encodeURIComponent(code));
        _cacheDefinitions.set(code, def);
        return def;
    },

    /** Campagnes du joueur, la plus recente en tete. */
    liste: () => getJSON("/list_campagnes?"),

    charger: (id) => getJSON("/get_campagne?" + encodeURIComponent(id)),

    /** Ecrit la campagne et rend la version enregistree (id et date a jour). */
    async enregistrer(campagne) {
        const res = await postJSON("/save_campagne", { campagne });
        return res.campagne;
    },

    supprimer: (id) => postJSON("/delete_campagne", { id }),
};

/** URL d'une page de livret d'une campagne. */
export function pageLivretUrl(code, fichier) {
    return "/public/stories/" + encodeURIComponent(code) + "/" + encodeURIComponent(fichier);
}
