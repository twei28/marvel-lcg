// sons.js — les sons de l'écran de préparation.
//
// Le PLATEAU joue les sons que le moteur lui nomme (ui-app/src/board/sons.ts) ;
// ici personne ne nous nomme rien, c'est l'interface qui décide : choisir un
// héros, verrouiller une cible, lancer la partie. On réutilise les fichiers
// existants (assets/sounds/, servis à la racine par le moteur) plutôt que d'en
// ajouter : la liste des noms est figée côté moteur, et remplacer un `.wav`
// suffit à changer ce qu'on entend (voir docs/reference/SONS-DECLENCHEURS.md).
//
// Mêmes règles que le plateau, à dessein (ui-app/src/board/sons.ts) :
//   — volume des effets réglable, PARTAGÉ avec le plateau
//     (`marvel-board-volume-sons`, en %, 20 par défaut) ;
//   — rien si l'onglet n'est pas visible ;
//   — au plus 2 sons à la fois (refonte des sons, 07/10/2026) ;
//   — survol des boutons et des tuiles : très bas, jamais en rafale ;
//   — l'échec est silencieux. Le navigateur refuse de jouer avant la première
//     interaction de la page ; inutile de crier, le son suivant passera.
//
// ⚠ LE RÉGLAGE EST CELUI DU PLATEAU, `marvel-board-sons` (board.tsx). Une
// deuxième clé donnerait deux boutons à couper pour un seul silence voulu.

"use strict";

const CLE_SONS = "marvel-board-sons";
const CLE_VOLUME = "marvel-board-volume-sons";
const VOLUME_PAR_DEFAUT = 20;
const MAX_SIMULTANES = 2;
const FACTEUR_SURVOL = 0.35;
const ECART_SURVOL_MS = 80;
/** Ce qui se survole sur cet écran : ses boutons et ses tuiles de choix. */
const SELECTEUR_SURVOL = 'button, [role="button"], .acc-tuile, .tb-carte';

/** Les sons que cet écran utilise, nommés par ce qu'ils VEULENT DIRE ici.
 *  La valeur est le fichier du moteur ; le nom de gauche est ce qu'on lit
 *  dans app.js, pour qu'un appel se relise sans aller voir la table. */
export const SON = {
    mode: "set",             // une tuile de mode se pose
    heros: "carddrop",       // le héros arrive sur la table
    herosRetire: "removecounter",
    favori: "token",         // un jeton posé sur la carte
    cible: "reveal",         // le méchant se retourne face visible
    etapeSuivante: "nextturn",
    etapePrecedente: "removecounter",
    aleatoire: "shuffle",    // on brasse
    lancement: "phase",      // le gong : la partie commence
};

/** Quand on le choisit (`jouerReplique`), ce héros dit une de SES répliques,
 *  tirée au hasard. Fichiers
 *  `assets/sounds/<valeur>`, extension comprise. Origine : SOURCES.md. Seule la
 *  MÊME personne a une voix (pas Miles Morales ni X-23). */
const SON_SURVOL_HEROS = {
    adam_warlock: ["voix-adam_warlock-1.mp3", "voix-adam_warlock-2.mp3", "voix-adam_warlock-3.mp3"],
    angela: ["voix-angela-1.mp3", "voix-angela-2.mp3", "voix-angela-3.mp3"],
    black_cat: ["voix-black_cat-1.mp3", "voix-black_cat-2.mp3", "voix-black_cat-3.mp3"],
    black_panther: ["voix-black_panther-1.mp3", "voix-black_panther-2.mp3", "voix-black_panther-3.mp3"],
    black_widow: ["voix-black_widow-1.mp3", "voix-black_widow-2.mp3", "voix-black_widow-3.mp3"],
    blade: ["voix-blade-1.mp3", "voix-blade-2.mp3", "voix-blade-3.mp3"],
    captain_america: ["voix-captain_america-1.mp3", "voix-captain_america-2.mp3", "voix-captain_america-3.mp3"],
    cloak_dagger: ["voix-cloak_dagger-1.mp3", "voix-cloak_dagger-2.mp3", "voix-cloak_dagger-3.mp3"],
    cyclops: ["voix-cyclops-1.mp3", "voix-cyclops-2.mp3", "voix-cyclops-3.mp3"],
    daredevil: ["voix-daredevil-1.mp3", "voix-daredevil-2.mp3", "voix-daredevil-3.mp3"],
    deadpool: ["voix-deadpool-1.mp3", "voix-deadpool-2.mp3", "voix-deadpool-3.mp3"],
    doctor_strange: ["voix-doctor_strange-1.mp3", "voix-doctor_strange-2.mp3", "voix-doctor_strange-3.mp3"],
    gambit: ["voix-gambit-1.mp3", "voix-gambit-2.mp3", "voix-gambit-3.mp3"],
    groot: ["voix-groot-1.mp3", "voix-groot-2.mp3"],
    hawkeye: ["voix-hawkeye-1.mp3", "voix-hawkeye-2.mp3", "voix-hawkeye-3.mp3"],
    hulk: ["voix-hulk-1.mp3", "voix-hulk-2.mp3", "voix-hulk-3.mp3"],
    human_torch: ["voix-human_torch-1.mp3", "voix-human_torch-2.mp3", "voix-human_torch-3.mp3"],
    invisible_woman: ["voix-invisible_woman-1.mp3", "voix-invisible_woman-2.mp3", "voix-invisible_woman-3.mp3"],
    iron_man: ["voix-iron_man-1.mp3", "voix-iron_man-2.mp3", "voix-iron_man-3.mp3"],
    jubilee: ["voix-jubilee-1.mp3", "voix-jubilee-2.mp3", "voix-jubilee-3.mp3"],
    magik: ["voix-magik-1.mp3", "voix-magik-2.mp3", "voix-magik-3.mp3"],
    magneto: ["voix-magneto-1.mp3", "voix-magneto-2.mp3", "voix-magneto-3.mp3"],
    mister_fantastic: ["voix-mister_fantastic-1.mp3", "voix-mister_fantastic-2.mp3", "voix-mister_fantastic-3.mp3"],
    moon_knight: ["voix-moon_knight-1.mp3", "voix-moon_knight-2.mp3", "voix-moon_knight-3.mp3"],
    phoenix: ["voix-phoenix-1.mp3", "voix-phoenix-2.mp3", "voix-phoenix-3.mp3"],
    rocket_raccoon: ["voix-rocket_raccoon-1.mp3", "voix-rocket_raccoon-2.mp3", "voix-rocket_raccoon-3.mp3"],
    rogue: ["voix-rogue-1.mp3", "voix-rogue-2.mp3", "voix-rogue-3.mp3"],
    scarlet_witch: ["voix-scarlet_witch-1.mp3", "voix-scarlet_witch-2.mp3", "voix-scarlet_witch-3.mp3"],
    spider_man: ["voix-spider_man-1.mp3", "voix-spider_man-2.mp3", "voix-spider_man-3.mp3"],
    star_lord: ["voix-star_lord-1.mp3", "voix-star_lord-2.mp3", "voix-star_lord-3.mp3"],
    storm: ["voix-storm-1.mp3", "voix-storm-2.mp3", "voix-storm-3.mp3"],
    the_thing: ["voix-the_thing-1.mp3", "voix-the_thing-2.mp3", "voix-the_thing-3.mp3"],
    thor: ["voix-thor-1.mp3", "voix-thor-2.mp3", "voix-thor-3.mp3"],
    winter_soldier: ["voix-winter_soldier-1.mp3", "voix-winter_soldier-2.mp3", "voix-winter_soldier-3.mp3"],
    wolverine: ["heros-wolverine.mp3", "voix-wolverine-2.mp3", "voix-wolverine-3.mp3"],
};

/** Même chose quand on choisit un scénario (son id), pour son méchant. */
const SON_SURVOL_MECHANTS = {
    kingpin_fne: ["voix-kingpin-1.mp3", "voix-kingpin-2.mp3", "voix-kingpin-3.mp3"],
    venom: ["voix-venom-1.mp3", "voix-venom-2.mp3", "voix-venom-3.mp3"],
    wd_kingpin: ["voix-kingpin-1.mp3", "voix-kingpin-2.mp3", "voix-kingpin-3.mp3"],
    gorr: ["voix-gorr-1.mp3", "voix-gorr-2.mp3", "voix-gorr-3.mp3"],
    hela: ["voix-hela-1.mp3", "voix-hela-2.mp3", "voix-hela-3.mp3"],
    loki: ["voix-loki-1.mp3", "voix-loki-2.mp3", "voix-loki-3.mp3"],
    magneto: ["voix-magneto-1.mp3", "voix-magneto-2.mp3", "voix-magneto-3.mp3"],
    the_hood: ["voix-the_hood-1.mp3", "voix-the_hood-2.mp3", "voix-the_hood-3.mp3"],
    the_hood_2: ["voix-the_hood-1.mp3", "voix-the_hood-2.mp3", "voix-the_hood-3.mp3"],
    ultron: ["voix-ultron-1.mp3", "voix-ultron-2.mp3", "voix-ultron-3.mp3"],
};

/** La dernière réplique jouée par liste : on ne la rejoue pas deux fois de suite. */
const derniereReplique = new Map();

function repliqueAuHasard(liste) {
    const precedente = derniereReplique.get(liste);
    const possibles = liste.length > 1 ? liste.filter((f) => f !== precedente) : liste;
    const choisie = possibles[Math.floor(Math.random() * possibles.length)];
    derniereReplique.set(liste, choisie);
    return choisie;
}

const enCours = new Set();
let dernierSurvol = -Infinity;

function actif() {
    try {
        // Actif PAR DÉFAUT, comme le plateau : l'absence de réglage veut dire
        // « je n'ai rien demandé », pas « je veux le silence ».
        return localStorage.getItem(CLE_SONS) !== "off";
    } catch (e) {
        return true;
    }
}

function volume() {
    try {
        const brut = localStorage.getItem(CLE_VOLUME);
        if (brut === null) return VOLUME_PAR_DEFAUT / 100;
        const v = Number(brut);
        return Number.isFinite(v) ? Math.min(100, Math.max(0, v)) / 100 : VOLUME_PAR_DEFAUT / 100;
    } catch (e) {
        return VOLUME_PAR_DEFAUT / 100;
    }
}

function jouer(nom, facteur) {
    if (!nom || !actif()) return false;
    if (document.visibilityState !== "visible") return false;
    for (const a of enCours) if (a.ended || a.paused || a.error) enCours.delete(a);
    if (enCours.size >= MAX_SIMULTANES) return false;
    try {
        const audio = new Audio("/" + (nom.includes(".") ? nom : nom + ".wav"));
        audio.volume = Math.min(1, volume() * facteur);
        audio.addEventListener("ended", () => enCours.delete(audio));
        enCours.add(audio);
        const p = audio.play();
        if (p && p.catch) p.catch(() => enCours.delete(audio));
        return true;
    } catch (e) {
        // Audio indisponible (contexte restreint, mémoire) : le silence est un
        // repli acceptable, une exception non.
        return false;
    }
}

/** La réplique d'un héros (`data-hero`) ou du méchant d'un scénario (`data-scn`),
 *  jouée QUAND ON LE CHOISIT, plus au survol (demande du 08/10/2026 : au survol,
 *  c'était trop). Rien si ce personnage n'a pas de voix. Ne lève jamais. */
export function jouerReplique(id, genre) {
    const repliques = (genre === "mechant" ? SON_SURVOL_MECHANTS : SON_SURVOL_HEROS)[id];
    if (repliques) jouer(repliqueAuHasard(repliques), 1);
}

// LE CLIC DE LA ROUE (« Partie au hasard », 08/10/2026) : le son de survol,
// déjà très court, à volume bas, une case qui passe sous le repère. Plusieurs
// bandeaux tournent ensemble : on n'en garde qu'un toutes les 45 ms, sinon les
// clics de quatre bandeaux se marchent dessus et saturent les deux places.
const FACTEUR_CLIC_ROUE = 0.3;
const ECART_CLIC_ROUE_MS = 45;
let dernierClicRoue = -Infinity;

/** Un clic de roue. Ne lève jamais. */
export function jouerClicRoue() {
    const t = performance.now();
    if (t - dernierClicRoue < ECART_CLIC_ROUE_MS) return;
    dernierClicRoue = t;
    jouer("survol", FACTEUR_CLIC_ROUE);
}

/** Joue un son de la table `SON`. Ne lève jamais. */
export function jouerSon(nom) {
    jouer(nom, 1);
}

// Le survol : écoute déléguée, souris seulement (au doigt, pas de survol), un
// seul son par élément survolé, et pas plus d'un toutes les 80 ms.
let dernierSurvole = null;
document.addEventListener("pointerover", (evenement) => {
    if (evenement.pointerType && evenement.pointerType !== "mouse") return;
    const cible = evenement.target instanceof Element ? evenement.target.closest(SELECTEUR_SURVOL) : null;
    if (cible === dernierSurvole) return;
    dernierSurvole = cible;
    if (!cible || cible.disabled) return;
    const t = performance.now();
    if (t - dernierSurvol < ECART_SURVOL_MS) return;
    if (jouer("survol", FACTEUR_SURVOL)) dernierSurvol = t;
});
