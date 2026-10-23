// puzzle-brouillon.js : le BROUILLON de l'assistant de création de puzzle (E5) et sa
// traduction en puzzle de format 2 (docs/puzzle/FORMAT-V2.md).
//
// Module pur, sans page ni réseau : il tourne dans le navigateur ET sous Node (test :
// outils/test_puzzle_moteur.py, cas `brouillon_vers_moteur`). La grammaire des commandes
// est celle de la capture du moteur (src/game/puzzle/puzzle_capture.py) : le brouillon
// d'un puzzle capturé et sa capture doivent dire la même chose.
"use strict";

export const ETATS_CARTE = ["Confused", "Stunned", "Tough", "Exposed", "Cloaked", "Dazed", "Intensified"];
export const GENRES_EN_JEU = ["ally", "support", "minion", "side_scheme", "environment", "upgrade"];

export function joueurVide() {
    return { identity: "", hand: [], deck: [], discard: [], setAside: [], state: {} };
}

// Un brouillon neuf : tout est facultatif et a une valeur par défaut raisonnable.
export function brouillonVide() {
    return {
        title: "", description: "", difficulty: 0, hints: [],
        villain: [], schemes: [], expert: false,
        players: [joueurVide()],
        encounterDeck: [], encounterDiscard: [], setAside: [],
        villainState: {}, schemeState: {},
        // Cartes posées : { kind, card, siege, host (indice dans enJeu), engaged, state }
        enJeu: [],
        firstPlayer: 0, startPhase: "",
        objectives: [], objectivesMode: "all",
        solution: "", solutionVisibility: "after",
    };
}

// ------------------------------------------------------------------ commandes
// Littéral Python d'une valeur du format (texte, entier, booléen, None, listes).
function py(valeur) {
    if (valeur === null || valeur === undefined) return "None";
    if (valeur === true) return "True";
    if (valeur === false) return "False";
    if (typeof valeur === "number") return String(Math.trunc(valeur));
    if (Array.isArray(valeur)) return "[" + valeur.map(py).join(", ") + "]";
    return "'" + String(valeur).replace(/\\/g, "\\\\").replace(/'/g, "\\'") + "'";
}

// Arguments d'état. `etat` : { exhausted, health, statuses:[[nom,n]], counters, tokens, threat }.
// Seules les clés renseignées sortent, dans l'ordre de la capture.
function argsEtat(etat) {
    const e = etat || {};
    const sortie = [];
    if (e.exhausted === true) sortie.push("exhausted=True");
    if (e.health !== undefined && e.health !== null) sortie.push("health=" + py(e.health));
    for (const nom of ["statuses", "counters", "tokens"]) {
        const liste = (e[nom] || []).filter(([, n]) => n);
        if (liste.length) sortie.push(nom + "=" + py(liste));
    }
    if (e.threat !== undefined && e.threat !== null && e.threat !== "") sortie.push("threat=" + py(e.threat));
    return sortie.length ? ", " + sortie.join(", ") : "";
}

function aEtat(etat) {
    return argsEtat(etat) !== "";
}

// Les commandes de l'état de départ : stades, états des cartes déjà en jeu, cartes posées.
export function commandesDuBrouillon(b) {
    const commandes = [];
    let compteur = 0;
    const cles = new Map(); // carte posée (indice dans enJeu) -> clé ; "h0", "v", "s" : cartes déjà en jeu

    for (let i = 0; i < (b.villainStage || 0); i++) commandes.push("Puzzle.AdvanceVillain()");
    for (let i = 0; i < (b.schemeStage || 0); i++) commandes.push("Puzzle.AdvanceMainScheme()");

    // Cartes DÉJÀ en jeu au départ : l'identité de chaque héros, le méchant, le complot principal.
    const dejaEnJeu = [];
    b.players.forEach((joueur, siege) => {
        if (joueur.identity) dejaEnJeu.push({ ref: "h" + siege, id: joueur.identity, etat: joueur.state });
    });
    // Le stade courant : le méchant est l'entrée `villainStage` de la liste ; le complot,
    // la face « b » de l'entrée `schemeStage` (celle qui est en jeu au départ).
    const idMechant = (b.villain || [])[b.villainStage || 0];
    if (idMechant) dejaEnJeu.push({ ref: "v", id: idMechant, etat: b.villainState });
    const idComplot = ((b.schemes || [])[b.schemeStage || 0] || "").split(",").pop();
    if (idComplot) dejaEnJeu.push({ ref: "s", id: idComplot, etat: b.schemeState });

    for (const carte of dejaEnJeu) {
        const aDesAmeliorations = b.enJeu.some((x) => x.kind === "upgrade" && x.hostRef === carte.ref);
        if (!aEtat(carte.etat) && !aDesAmeliorations) continue;
        compteur += 1;
        const cle = "e" + compteur;
        cles.set(carte.ref, cle);
        commandes.push(`Puzzle.RestoreState(${py(carte.id)}, key=${py(cle)}${argsEtat(carte.etat)})`);
    }

    // Cartes à POSER : un porteur doit être posé avant ses améliorations.
    const posees = new Set();
    const poser = (indice) => {
        if (posees.has(indice)) return;
        const carte = b.enJeu[indice];
        if (carte.kind === "upgrade" && carte.host !== undefined && carte.host !== null) poser(carte.host);
        posees.add(indice);
        compteur += 1;
        const cle = "e" + compteur;
        cles.set(indice, cle);
        let args = `${py(cle)}, ${py(carte.card)}, ${py(carte.kind)}, siege=${carte.siege || 0}`;
        if (carte.kind === "upgrade") {
            const hote = carte.host !== undefined && carte.host !== null ? cles.get(carte.host) : cles.get(carte.hostRef);
            if (!hote) throw new Error(`amélioration ${carte.card} sans porteur`);
            args += `, host=${py(hote)}`;
        }
        if (carte.engaged) args += ", engaged=True";
        commandes.push(`Puzzle.RestoreCard(${args}${argsEtat(carte.state)})`);
    };
    b.enJeu.forEach((_, indice) => poser(indice));
    return commandes;
}

// ------------------------------------------------------------------ puzzle v2
export function brouillonVersPuzzle(b, { auteur = "", version = "0.5.8", graine = 1 } = {}) {
    return {
        version, author: auteur, cover: (b.villain || [])[0] || "", comment: b.title || "", seed: graine,
        villain: [...b.villain], schemes: [...b.schemes],
        encounter_deck: [...b.encounterDeck], encounter_discard_pile: [...b.encounterDiscard],
        set_aside: [...b.setAside], expert: !!b.expert,
        players: b.players.map((j) => ({
            identities: j.identity ? [j.identity] : [],
            hand_cards: [...j.hand], player_deck: [...j.deck], player_discard_pile: [...j.discard],
            set_aside: [...j.setAside], deck_name: j.deckName || "",
        })),
        puzzle_command: commandesDuBrouillon(b),
        format: 2, title: b.title, description: b.description, difficulty: b.difficulty || 0,
        hints: [...b.hints], objectives: b.objectives.map((o) => ({ kind: o.kind, target: o.target || "", text: o.text || "" })),
        objectives_mode: b.objectivesMode, start_phase: b.startPhase || "", start_step: "",
        first_player: b.firstPlayer || 0, solution_visibility: b.solutionVisibility || "after",
        solution_text: (b.solution || "").trim(), has_solution: !!(b.solution || "").trim(),
    };
}

// ------------------------------------------------------------------ vérifications
// Les mêmes limites que le moteur (puzzle_validation.py), pour refuser AVANT l'envoi.
export function erreursDuBrouillon(b) {
    const erreurs = [];
    if (!b.villain.length) erreurs.push("Choisis un méchant.");
    if (!b.schemes.length) erreurs.push("Choisis un complot principal.");
    if (b.players.length < 1 || b.players.length > 4) erreurs.push("Un puzzle a de 1 à 4 héros.");
    b.players.forEach((j, i) => {
        if (!j.identity) erreurs.push(`Héros ${i + 1} : choisis un héros.`);
        for (const [nom, zone] of [["main", j.hand], ["deck", j.deck], ["défausse", j.discard]]) {
            if (zone.length > 200) erreurs.push(`Héros ${i + 1} : ${nom} trop grande (200 cartes au plus).`);
        }
    });
    if (b.title.length > 80) erreurs.push("Titre trop long (80 caractères au plus).");
    if (b.description.length > 2000) erreurs.push("Histoire trop longue (2000 caractères au plus).");
    if (b.hints.length > 10) erreurs.push("10 indices au plus.");
    if (b.objectives.length > 6) erreurs.push("6 objectifs au plus.");
    if ((b.solution || "").length > 4000) erreurs.push("Solution trop longue (4000 caractères au plus).");
    b.enJeu.forEach((c, i) => {
        if (!GENRES_EN_JEU.includes(c.kind)) erreurs.push(`Carte en jeu ${i + 1} : genre inconnu.`);
        if ((c.siege || 0) >= b.players.length) erreurs.push(`Carte en jeu ${i + 1} : ce héros n'existe pas.`);
    });
    return erreurs;
}
