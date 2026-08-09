// salon-etat.js — décide si la partie multi peut être lancée, et qui manque.
//
// Module PUR et sans import : il se teste sous Node
// (outils/verifier-salon-etat.mjs) sans navigateur ni serveur.
//
// ⚠️ DEUX NUMÉROTATIONS DE SIÈGES coexistent, ne jamais les mélanger :
//   index technique p = 0 (l'hôte), 1..3 (les invités)   → URL ?p=, cookie
//                                                          seat_token_<p>,
//                                                          index joueur moteur
//   libellé affiché  = p + 1                             → « Joueur 1 » à
//                                                          « Joueur 4 »
// Les confondre donne à quelqu'un le deck de son voisin. La conversion se fait
// ICI et nulle part ailleurs.
"use strict";

/** Un choix ne vaut que s'il désigne à la fois un héros et un deck. */
function choixComplet(choix) {
    return !!(choix && choix.hero_card_id && choix.deck_id);
}

/**
 * @param {{nombreJoueurs:number, sieges:Object}} etat
 *        `sieges` est indexé par index TECHNIQUE. Les clés arrivent en chaînes
 *        quand elles viennent du JSON de /get_choix_sieges.
 * @returns {{prete:boolean, manquants:number[], choixParSiege:Map<number,object>}}
 *        `manquants` liste les LIBELLÉS affichés, par ordre croissant.
 */
export function etatSalon({ nombreJoueurs, sieges }) {
    const choixParSiege = new Map();
    for (const [cle, choix] of Object.entries(sieges || {})) {
        const p = Number(cle);
        if (Number.isInteger(p) && choixComplet(choix)) choixParSiege.set(p, choix);
    }

    const manquants = [];
    // Le siège 0 est celui de l'hôte : il choisit dans son wizard, jamais ici.
    for (let p = 1; p < nombreJoueurs; p += 1) {
        if (!choixParSiege.has(p)) manquants.push(p + 1);
    }

    return { prete: manquants.length === 0, manquants, choixParSiege };
}
