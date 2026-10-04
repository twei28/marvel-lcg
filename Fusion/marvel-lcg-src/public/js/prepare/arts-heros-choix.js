// arts-heros-choix.js : le choix d'art alternatif d'un héros, face par face.
//
// Le choix vit dans UNE table `{ cle: code }` (clé de stockage `mc_hero_art_v1`,
// lue aussi par le plateau) :
//   - « 38001 »  : l'art du héros ET, par défaut, celui de son alter ego ;
//   - « 38001b » : l'art de l'alter ego QUAND IL DIFFÈRE (« standard » compris,
//     qui force le scan). Absent : l'alter ego suit le héros.
// Un héros sans clé garde son scan standard.
//
// Module PUR (ni DOM ni stockage) : testé par
// `node --test tools/tests-lanceur/arts-heros-choix.test.mjs`.
"use strict";

export const STANDARD = "standard";

/** Clé de héros : numéro de carte sans suffixe de face (« 38001a » -> « 38001 »). */
export function cleHeros(heroCardId) {
    return String(heroCardId || "").split(",")[0].replace(/[a-z]$/, "");
}

/** Le choix d'un héros : `heros` ("standard" par défaut) et `alterEgo`
 *  (null tant qu'il suit le héros). */
export function lireChoix(arts, heroCardId) {
    const cle = cleHeros(heroCardId);
    return {
        heros: (arts && arts[cle]) || STANDARD,
        alterEgo: (arts && arts[cle + "b"]) || null,
    };
}

/** Les changements à écrire pour ce choix, au format de `/save_arts_heros` :
 *  `null` efface la clé. `alterEgo` null = l'alter ego suit le héros. */
export function changementsPour(heroCardId, heros, alterEgo) {
    const cle = cleHeros(heroCardId);
    if (!cle) return {};
    return {
        [cle]: !heros || heros === STANDARD ? null : heros,
        [cle + "b"]: alterEgo ? alterEgo : null,
    };
}

/** Applique des changements à une table, sans la modifier : une NOUVELLE table. */
export function appliquer(arts, changements) {
    const suite = { ...(arts || {}) };
    for (const [cle, code] of Object.entries(changements || {})) {
        if (code === null) delete suite[cle]; else suite[cle] = code;
    }
    return suite;
}

/** Le code que l'alter ego AFFICHE : le sien s'il en a un, sinon celui du
 *  héros pourvu que l'alter ego ait cet art (sinon son scan). */
export function codeAlterEgoAffiche(choix, codesAlterEgo) {
    const voulu = choix.alterEgo || choix.heros;
    return voulu !== STANDARD && (codesAlterEgo || []).includes(voulu) ? voulu : STANDARD;
}

/**
 * Réconcilie le navigateur avec la réponse de `/get_arts_heros`.
 *
 * Rend `null` quand le serveur n'est pas la référence (invité, moteur local) :
 * le navigateur reste seul maître. Sinon `{ arts, pousser }` : la table à
 * garder en local, et les changements à envoyer au serveur.
 *  - le compte a déjà un fichier : il fait foi, le navigateur s'y aligne ;
 *  - le compte n'en a pas encore : on y verse ce que le navigateur contient,
 *    pour que le premier passage ne fasse rien perdre.
 * Pas de fusion clé par clé : un choix remis sur « standard » sur un appareil
 * (clé effacée) reviendrait sinon d'un autre appareil resté en retard.
 */
export function reconcilier(local, reponse) {
    if (!reponse || !reponse.compte) return null;
    const arts = { ...(local || {}) };
    if (!reponse.existe) {
        return { arts, pousser: Object.keys(arts).length ? { ...arts } : {} };
    }
    return { arts: { ...(reponse.arts || {}) }, pousser: {} };
}

/** Deux tables disent-elles la même chose ? */
export function memesArts(a, b) {
    const ka = Object.keys(a || {}).sort();
    const kb = Object.keys(b || {}).sort();
    return ka.length === kb.length && ka.every((k, i) => k === kb[i] && a[k] === b[k]);
}
