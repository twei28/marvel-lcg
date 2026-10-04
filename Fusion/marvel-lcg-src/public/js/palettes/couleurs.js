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
 *  Mêmes valeurs que le plateau, montées quatre fois à la demande de
 *  l'utilisateur : 14/09/2026 (0,32 / 0,24 / 0,14 → 0,46 / 0,34 / 0,20), puis
 *  22/09/2026 (→ 0,60 / 0,44 / 0,26), puis 23/09/2026 en deux temps (→ 0,74 /
 *  0,54 / 0,32, « encore plus flashy », puis au maximum → 1,0 / 0,9 / 0,75,
 *  la primaire à pleine opacité). Les POSITIONS ont aussi bougé une fois
 *  (0/16/30 % → 0/22/38 %, « la couleur primaire peut ressortir un peu
 *  plus » -- impossible de monter l'opacité plus haut que 1,0, alors la
 *  primaire pure occupe une plus grande part de la bande à la place). */
export const ARRETS = [
    { a: 0, force: 1.0 },
    { a: 22, force: 0.9 },
    { a: 38, force: 0.75 },
];

/** L'ordre dans lequel les trois couleurs du fichier (primaire, secondaire,
 *  tertiaire) tiennent les arrêts ci-dessus (23/09/2026, demande de
 *  l'utilisateur, capture de cet éditeur à l'appui : « la primaire je la
 *  veux à droite, la secondaire à gauche et le tertiaire au milieu »). La
 *  primaire (index 0) reste au coin (0 %, « à droite »), la tertiaire
 *  (index 2) tient l'arrêt du milieu (22 %), la secondaire (index 1) tient
 *  le dernier arrêt visible (38 %, le plus diffus -- « à gauche »). */
export const ORDRE = [0, 2, 1];

/** Le fond du plateau pour ces couleurs : une bande diagonale au coin bas
 *  droit, qui s'éteint avant le centre. Voir `halo-heros.ts` pour le pourquoi
 *  de chaque valeur. */
export function fondDe(couleurs, sombre) {
    if (!Array.isArray(couleurs) || couleurs.length === 0) return sombre;
    const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
    const derniere = couleurs[couleurs.length - 1];
    const etapes = ARRETS.map((arret, i) => {
        const couleur = couleurs[ORDRE[i]] ?? derniere;
        return `${rgba(couleur, arret.force)} ${arret.a}%`;
    });
    const fin = couleurs[ORDRE[ARRETS.length - 1]] ?? derniere;
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

/** Où le clic est tombé DANS l'image, en pixels de l'image.
 *
 *  Le canvas est dessiné à la taille réelle du scan, mais affiché à la taille
 *  que la page lui laisse : sans ce rapport, la pipette prélèverait à côté dès
 *  que la fenêtre n'a pas exactement la largeur du scan. Rend null hors cadre.
 */
export function coordonneesDansCanvas(rect, largeurCanvas, hauteurCanvas, clientX, clientY) {
    if (!rect || !rect.width || !rect.height) return null;
    const x = Math.floor((clientX - rect.left) * (largeurCanvas / rect.width));
    const y = Math.floor((clientY - rect.top) * (hauteurCanvas / rect.height));
    if (x < 0 || y < 0 || x >= largeurCanvas || y >= hauteurCanvas) return null;
    return { x, y };
}

/** La couleur MOYENNE d'un petit carré autour d'un point.
 *
 *  ⚠ JAMAIS UN SEUL PIXEL. Les scans sont des JPEG : un pixel isolé porte le
 *  bruit de compression, et deux clics voisins donnent deux couleurs
 *  différentes. Le générateur moyenne déjà le contour des cartes ; la pipette
 *  fait la même chose, en plus petit. `rayon = 2` donne un carré de 5 sur 5.
 *
 *  `pixels` est le tableau RVBA d'un `getImageData`. Les pixels transparents
 *  ne comptent pas : sur un scan à coins arrondis, ils tireraient la moyenne
 *  vers du noir qui n'est pas sur la carte.
 */
export function moyenneAutour(pixels, largeur, hauteur, x, y, rayon = 2) {
    let r = 0, v = 0, b = 0, n = 0;
    for (let dy = -rayon; dy <= rayon; dy += 1) {
        for (let dx = -rayon; dx <= rayon; dx += 1) {
            const px = x + dx;
            const py = y + dy;
            if (px < 0 || py < 0 || px >= largeur || py >= hauteur) continue;
            const i = (py * largeur + px) * 4;
            if (pixels[i + 3] === 0) continue;
            r += pixels[i]; v += pixels[i + 1]; b += pixels[i + 2]; n += 1;
        }
    }
    if (n === 0) return null;
    return [Math.round(r / n), Math.round(v / n), Math.round(b / n)];
}

/** Deux palettes sont-elles identiques ? Sert à ne PAS écrire une correction
 *  qui ne corrige rien : le fichier ne doit porter que les écarts. */
export function memePalette(a, b) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((couleur, i) =>
        couleur[0] === b[i][0] && couleur[1] === b[i][1] && couleur[2] === b[i][2]);
}
