// teinte-choix.js : la TEINTE DU FOND, cote preparation (04/10/2026).
//
// ⚠ JUMEAU de `ui-app/src/board/teinte.ts` : MEMES bornes, MEMES couleurs.
// Leurs tests partagent les memes valeurs attendues
// (`tools/tests-lanceur/teinte-choix.test.mjs` / `board/teinte.test.ts`), et
// les bornes sont aussi celles du serveur (`TEINTE_BORNES`, server_get.py).
// Une seule cle de stockage, lue par le plateau : `mc_teinte_v1` = « h,s,l ».
//
// Module PUR (ni DOM ni stockage).
"use strict";

export const CLE_TEINTE = "mc_teinte_v1";
export const BORNES = { h: [0, 359], s: [0, 18], l: [6, 62] };
export const TEINTE_DE_DEPART = { h: 220, s: 8, l: 12 };
export const SEUIL_TABLE_CLAIRE = 44;

const borne = (v, [bas, haut]) => Math.min(haut, Math.max(bas, Math.round(v)));

export function lireTeinte(brut) {
    if (typeof brut !== "string") return undefined;
    const morceaux = brut.split(",");
    if (morceaux.length !== 3 || !morceaux.every((m) => /^\d+$/.test(m))) return undefined;
    const [h, s, l] = morceaux.map(Number);
    if (h > BORNES.h[1] || s > BORNES.s[1] || l < BORNES.l[0] || l > BORNES.l[1]) return undefined;
    return { h, s, l };
}

export function bornerTeinte(teinte) {
    return { h: borne(((teinte.h % 360) + 360) % 360, BORNES.h), s: borne(teinte.s, BORNES.s), l: borne(teinte.l, BORNES.l) };
}

export function ecrireTeinteEnTexte(teinte) {
    const t = bornerTeinte(teinte);
    return `${t.h},${t.s},${t.l}`;
}

export function hslVersRgb(h, s, l) {
    const sat = s / 100;
    const lum = l / 100;
    const k = (n) => (n + h / 30) % 12;
    const a = sat * Math.min(lum, 1 - lum);
    const f = (n) => lum - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
    return [f(0), f(8), f(4)].map((x) => Math.round(x * 255)).join(" ");
}

export function variablesDeTeinte(teinte) {
    const { h, s, l } = bornerTeinte(teinte);
    const lBandeau = Math.min(26, Math.max(5, l - 4));
    const lPanneau = Math.min(24, Math.max(8, l + 2));
    const lCadre = Math.min(36, lPanneau + 10);
    return {
        "--teinte-table": `hsl(${h} ${s}% ${l}%)`,
        "--teinte-table-rgb": hslVersRgb(h, s, l),
        "--teinte-bandeau": `hsl(${h} ${s}% ${lBandeau}%)`,
        "--teinte-bandeau-rgb": hslVersRgb(h, s, lBandeau),
        "--teinte-panneau": `hsl(${h} ${s}% ${lPanneau}%)`,
        "--teinte-panneau-rgb": hslVersRgb(h, s, lPanneau),
        "--teinte-cadre": `hsl(${h} ${Math.min(30, s + 4)}% ${lCadre}%)`,
        "--teinte-texte-table": l >= SEUIL_TABLE_CLAIRE ? "#1b1d21" : "rgba(226, 232, 240, 0.78)",
    };
}

export function teinteDuPoint(dx, dy, rayon, l) {
    const angle = (Math.atan2(dy, dx) * 180) / Math.PI;
    const distance = Math.min(1, Math.hypot(dx, dy) / Math.max(1, rayon));
    return bornerTeinte({ h: (angle + 90 + 360) % 360, s: distance * BORNES.s[1], l });
}

export function pointDeLaTeinte(teinte) {
    const t = bornerTeinte(teinte);
    const angle = ((t.h - 90) * Math.PI) / 180;
    const distance = t.s / BORNES.s[1];
    return { x: Math.cos(angle) * distance, y: Math.sin(angle) * distance };
}

/** Meme contrat que le plateau : `null` = le compte n'a pas de teinte,
 *  `undefined` = le navigateur reste la reference. */
export function teinteDuCompte(reponse) {
    if (!reponse || !reponse.compte || !reponse.existe) return undefined;
    return lireTeinte((reponse.preferences || {}).teinte) ?? null;
}
