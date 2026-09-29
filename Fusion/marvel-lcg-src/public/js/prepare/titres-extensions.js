// titres-extensions.js — le nom d'une extension tel que le JOUEUR le lit.
//
// Les clés de `sets_info.json` (« 4. The Rise of Red Skull ») sont les titres
// anglais. Jusqu'au 29/09/2026 l'écran de préparation les affichait tels
// quels, même en français (signalé par l'utilisateur : « ça me casse les
// couilles que ce soit pas encore 100 % français »). Les titres français sont
// ceux imprimés sur les boîtes vendues en France (Asmodee), relevés sur les
// fiches Philibert et la page Wikipédia FR du jeu.
//
// ⚠ TABLE PAR NUMÉRO, PAS PAR TITRE : le numéro de la clé est stable, le
// titre anglais peut être retouché. Un paquet dont le titre est identique
// dans les deux langues (Civil War, NeXt Evolution, les paquets héros nommés
// d'après le personnage) n'a pas de ligne : on lui rend la clé sans numéro.
//
// Module pur, sans DOM : testé par `tools/tests-lanceur/titres-extensions.test.mjs`.
"use strict";

export const TITRES_FR = {
    1:  "Set de base",
    2:  "Le Bouffon Vert",
    4:  "L’Avènement de Crâne Rouge",
    7:  "Les Démolisseurs",
    11: "Kang le Conquérant",
    16: "Convoitise Galactique",
    21: "L’Ombre du Titan Fou",
    27: "Sinistres Motivations",
    32: "La Genèse des Mutants",
    45: "L’Ère d’Apocalypse",
    50: "Agents du S.H.I.E.L.D.",
    60: "Peur de Rien",
    90: "Set modulaire Ronan",
};

/** Le numéro que porte une clé d'extension (« 12. Ant-Man » -> 12), ou null. */
export function numeroDExtension(cle) {
    const m = /^(\d+)\.\s*/.exec(String(cle || ""));
    return m ? Number(m[1]) : null;
}

/** Le titre à afficher pour une clé d'extension, dans la langue demandée
 *  ("fr" par défaut). Toujours sans le numéro. */
export function nomExtension(cle, langue = "fr") {
    const brut = String(cle || "").replace(/^\d+\.\s*/, "");
    if (langue === "en") return brut;
    const numero = numeroDExtension(cle);
    return (numero !== null && TITRES_FR[numero]) || brut;
}

/** Le titre français d'une grande boîte à partir de son titre anglais (celui
 *  des vagues, `NOMS_VAGUES` dans catalog.js), ou le titre anglais s'il n'a
 *  pas de version française. */
export function titreDeBoite(titreAnglais, langue = "fr") {
    if (langue === "en" || !titreAnglais) return titreAnglais || "";
    const cle = Object.keys(TITRES_ANGLAIS_DES_BOITES).find((k) => TITRES_ANGLAIS_DES_BOITES[k] === titreAnglais);
    return (cle && TITRES_FR[cle]) || titreAnglais;
}

// Les titres anglais des grandes boîtes, par numéro, pour `titreDeBoite`.
// Même source que `NOMS_VAGUES` (catalog.js) : à tenir en miroir.
const TITRES_ANGLAIS_DES_BOITES = {
    4:  "The Rise of Red Skull",
    16: "The Galaxy's Most Wanted",
    21: "The Mad Titan's Shadow",
    27: "Sinister Motives",
    32: "Mutant Genesis",
    40: "NeXt Evolution",
    45: "Age of Apocalypse",
    50: "Agents of S.H.I.E.L.D.",
    56: "Civil War",
    60: "Fear No Evil",
};
