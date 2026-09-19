// couleurs.js — les règles pures de l'éditeur de palettes. Aucun DOM, aucun
// réseau : tout ce qui se teste sans navigateur vit ici
// (`tools/tests-lanceur/palettes-couleurs.test.mjs`).
//
// ⚠ LE FOND DE PLATEAU EST RECOPIÉ ICI, ET C'EST VOULU.
// `fondDe` reproduit à l'identique `ui-app/src/board/halo-heros.ts`. L'éditeur
// doit montrer le VRAI rendu, pas un aplat : juger une couleur sur un carré
// plein est exactement ce qui a produit les couleurs fausses qu'on vient
// corriger. Les deux copies sont tenues d'accord par
// `ui-app/src/board/halo-heros-accord.test.ts`, qui compare leurs sorties : si
// l'une bouge sans l'autre, cette gate rougit.

"use strict";

/** « #1a2b3c » ou « 1a2b3c » → [26, 43, 60]. Rend null si ce n'est pas une
 *  couleur : l'éditeur doit pouvoir refuser une saisie sans planter. */
export function hexVersRgb(texte) {
    const propre = String(texte || "").trim().replace(/^#/, "");
    if (!/^[0-9a-fA-F]{6}$/.test(propre)) return null;
    return [
        parseInt(propre.slice(0, 2), 16),
        parseInt(propre.slice(2, 4), 16),
        parseInt(propre.slice(4, 6), 16),
    ];
}

/** [26, 43, 60] → « #1a2b3c ». Borne chaque composante à 0..255 : une valeur
 *  hors bornes viendrait d'un fichier abîmé, pas d'une saisie. */
export function rgbVersHex(couleur) {
    if (!Array.isArray(couleur) || couleur.length !== 3) return "";
    const borne = (v) => Math.max(0, Math.min(255, Math.round(Number(v) || 0)));
    return "#" + couleur.map((v) => borne(v).toString(16).padStart(2, "0")).join("");
}

/** Les arrêts de la bande diagonale, position en % et force de la couleur.
 *  Mêmes valeurs que le plateau, montées le 14/09/2026 à la demande de
 *  l'utilisateur (0,32 / 0,24 / 0,14 → 0,46 / 0,34 / 0,20). */
export const ARRETS = [
    { a: 0, force: 0.46 },
    { a: 16, force: 0.34 },
    { a: 30, force: 0.2 },
];

/** Le fond du plateau pour ces couleurs : une bande diagonale au coin bas
 *  droit, qui s'éteint avant le centre. Voir `halo-heros.ts` pour le pourquoi
 *  de chaque valeur. */
export function fondDe(couleurs, sombre) {
    if (!Array.isArray(couleurs) || couleurs.length === 0) return sombre;
    const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
    const derniere = couleurs[couleurs.length - 1];
    const etapes = ARRETS.map((arret, i) => {
        const couleur = couleurs[i] ?? derniere;
        return `${rgba(couleur, arret.force)} ${arret.a}%`;
    });
    const fin = couleurs[ARRETS.length - 1] ?? derniere;
    return `linear-gradient(315deg, ${etapes.join(", ")}, ${rgba(fin, 0)} 50%), ${sombre}`;
}

/** L'identité à laquelle appartient une carte : « 03001a » → « 03001 ».
 *
 *  ⚠ LES FACES D'UNE MÊME IDENTITÉ PARTAGENT LEUR PALETTE. Se transformer ne
 *  doit pas faire sauter la couleur du fond : on corrige donc une identité,
 *  jamais une face seule. Un identifiant sans lettre finale est rendu tel
 *  quel — les palettes fan-made en ont (`aa001a`, mais aussi des clés courtes).
 */
export function identiteDe(cardId) {
    const texte = String(cardId || "");
    return /[a-z]$/.test(texte) ? texte.slice(0, -1) : texte;
}

/** Regroupe un relevé de palettes par identité.
 *
 *  Rend, par identité, la liste TRIÉE de ses faces et la palette commune (la
 *  première rencontrée : le générateur écrit la même sur toutes les faces).
 */
export function grouperParIdentite(palettes) {
    const groupes = new Map();
    for (const [carte, couleurs] of Object.entries(palettes || {})) {
        const identite = identiteDe(carte);
        const groupe = groupes.get(identite) || { identite, cartes: [], couleurs: [] };
        groupe.cartes.push(carte);
        if (groupe.couleurs.length === 0 && Array.isArray(couleurs)) {
            groupe.couleurs = couleurs.map((c) => [c[0], c[1], c[2]]);
        }
        groupes.set(identite, groupe);
    }
    for (const groupe of groupes.values()) groupe.cartes.sort();
    return groupes;
}

/** Les trois champs de l'éditeur, rendus au format du fichier.
 *
 *  ⚠ UNE COULEUR VIDE ARRÊTE LA LISTE. Un héros peut n'avoir qu'une ou deux
 *  couleurs (onze cadres sont noirs ou gris) : laisser un champ vide est une
 *  façon légitime de dire « il n'en a que deux ». Mais un TROU au milieu est
 *  une faute de frappe, pas une intention : on refuse plutôt que de deviner.
 */
export function couleursDepuisChamps(champs) {
    const couleurs = [];
    let fini = false;
    for (const champ of champs) {
        const vide = String(champ || "").trim() === "";
        if (vide) { fini = true; continue; }
        if (fini) return { erreur: "trou", couleurs: [] };
        const rgb = hexVersRgb(champ);
        if (!rgb) return { erreur: "hex", couleurs: [] };
        couleurs.push(rgb);
    }
    if (couleurs.length === 0) return { erreur: "vide", couleurs: [] };
    return { erreur: "", couleurs };
}

/** Deux palettes sont-elles identiques ? Sert à ne PAS écrire une correction
 *  qui ne corrige rien : le fichier ne doit porter que les écarts. */
export function memePalette(a, b) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((couleur, i) =>
        couleur[0] === b[i][0] && couleur[1] === b[i][1] && couleur[2] === b[i][2]);
}
