// scans-fr.js — scans de cartes en français, pour les pages hors plateau.
//
// Jumeau de ui-app/src/board/scans-fr.ts, qui rend le même service au plateau
// React. Même convention, volontairement : le pack d'images OCTGN FR est
// extrait par tools/importer_scans_fr.py sous assets/pics-fr, avec un préfixe
// « fr_ » dans le NOM DU FICHIER. C'est ce préfixe, et non une route ni un
// en-tête, qui distingue les deux collections — le serveur sert les deux
// dossiers sans rien savoir des langues, et les caches (serveur comme
// navigateur) ne peuvent pas les confondre.
//
// DIFFÉRENCE ASSUMÉE AVEC LE PLATEAU : lui embarque la liste des 4210 codes
// réellement extraits (scans-fr-liste.ts) pour ne demander « fr_ » que quand le
// fichier existe. Ici on ne l'embarque pas, et on demande « fr_ » pour TOUTE
// carte. C'est sans risque : le moteur retombe de lui-même sur le scan anglais
// quand « fr_<code> » est absent — le repli est écrit et commenté dans
// engine/file/cache.py, précisément parce que les 456 Mo d'images FR ne sont
// pas versionnés et peuvent manquer sur une installation neuve. Mesuré : sur
// une carte sans scan FR, /fr_<code> et /<code> rendent le même octet près.
//
// Le bénéfice est net : la galerie couvre les 4324 cartes sans traîner une
// liste de 4210 entrées à regénérer à chaque import, et une carte fan-made
// traduite plus tard sera servie en français sans toucher à ce fichier.
"use strict";

import { langueActuelle } from "/public/js/prepare/langue.js";

export const PREFIXE_FR = "fr_";

/** Nom de fichier à demander au serveur pour cette carte, dans la langue de
 *  l'interface. En anglais, ou sans identifiant, on ne préfixe rien. */
export function picIdLangue(picId) {
    if (!picId) return picId;
    if (langueActuelle() !== "fr") return picId;
    const id = String(picId);
    return id.startsWith(PREFIXE_FR) ? id : PREFIXE_FR + id;
}
