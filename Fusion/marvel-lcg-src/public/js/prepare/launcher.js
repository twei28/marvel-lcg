// launcher.js — construit le NewGameDescriptor et lance la partie.
// IMPORTANT : reproduit à l'identique le contrat /new?data= de l'ancien scene.html.
"use strict";
import { catalog } from "/public/js/prepare/catalog.js";
import { appliquerTutoriel } from "/public/js/prepare/tutoriel-etat.js";
import { appliquerNiveau } from "/public/js/prepare/niveau-standard.js";
import { reglesIntense } from "/public/js/prepare/intense-combatants.js";
import { cards } from "/public/js/prepare/cards.js";
import { t } from "/public/js/prepare/langue.js";
import { echangesTeamUp, appliquerEchange } from "/public/js/prepare/team-up.js";

const uniq = (arr) => [...new Set(arr)];

/** Résout le JSON d'un scénario à envoyer au moteur (variante Expert si demandée). */
async function resolveRaw(state, sc) {
    if (!sc) return null;
    if (state.difficulty.base === "expert" && sc.hasExpertVariant) {
        const ev = await catalog.expertVariant(sc.id.replace(/_expert$/, ""));
        if (ev) return ev.rawJson;
    }
    return sc.rawJson;
}

async function resolveScenarioRaw(state) { return resolveRaw(state, state.scenario); }

/** Mode Bataille : deux équipes, chacune face au scénario apporté par l'autre. */
function estBataille(state) { return !!state.mode && state.mode.id === "bataille"; }

function buildRules(state) {
    const rules = [];
    if (state.difficulty.skirmish) rules.push("mode_skirmish");
    if (state.mode.id === "campaign") rules.push("mode_campaign");
    // Kingsfall multi-tables (assemblees, 22/10/2026) : le serveur du moteur s'inscrit dans l'assemblee AVANT de lancer la partie et remplace cette demande
    // par la regle `assemblee_<CODE>_<TABLE>` (server_new_game.py). Une demande sans code ne part pas.
    if (state.assemblee && state.assemblee.mode === "creer") rules.push("assemblee_creer");
    if (state.assemblee && state.assemblee.mode === "rejoindre" && String(state.assemblee.code || "").trim()) {
        rules.push("assemblee_rejoindre_" + String(state.assemblee.code).trim().toUpperCase());
    }
    const h = state.difficulty.heroic | 0;
    if (h > 0) rules.push("mode_heroic_" + h);
    // Règles v16 débrayables depuis le bloc « Avancé » (actives par défaut).
    if (state.reglesV16 !== false) rules.push("v16_all");
    // Rules Reference 1.8 : toujours pour une partie neuve (les sauvegardes
    // d'avant ne portent pas la regle et se rejouent dans les anciennes).
    rules.push("v18_all");
    // La tuile « Bac a sable » du selecteur de modes. Le mode passe par
    // `rules`, donc il est inscrit dans la scene et survit au chargement
    // d'une sauvegarde — on saura toujours si une victoire comptait.
    if (state.mode && state.mode.id === "sandbox") rules.push("mode_sandbox");
    // Le mode « Puzzle » : un plateau d'EDITEUR. Bac a sable (commandes `Puzzle.*`, catalogue) + table manuelle (le moteur se tait, rien ne
    // se declenche quand on deplace une carte) + `mode_createur_puzzle` (le bouton « Enregistrer le puzzle » du plateau).
    if (state.mode && state.mode.id === "puzzle") rules.push("mode_sandbox", "mode_manuel", "mode_createur_puzzle");
    // Partie manuelle : apres la mise en place, le moteur ne conduit plus et ne
    // declenche plus rien. Comme les autres modes, le drapeau passe par `rules`
    // et survit donc au chargement d'une sauvegarde.
    if (state.modeManuel === true) rules.push("mode_manuel");
    // Bataille : le moteur ouvre une seconde zone de jeu, y pose le second
    // leader et enfile les phases camp par camp. Comme les autres modes, le
    // drapeau passe par `rules` et survit donc au chargement d'une sauvegarde.
    if (estBataille(state)) rules.push("mode_competitive");
    rules.push("no_crisis_of_infinite_deadpools");
    rules.push("no_encounter_cards_ignore_crisis");
    // Le temps d'arrêt sur la face A de la manigance principale (spec du
    // 15/09/2026). Posé par les parties NEUVES uniquement : une sauvegarde
    // rechargée garde les règles inscrites dans sa scène, donc ne pose pas la
    // question et rejoue ses opérations sans décalage.
    rules.push("confirm_main_scheme");
    // Le meme temps d'arret pour une manigance ANNEXE que le scenario met en
    // jeu (avenant du 15/09/2026). Drapeau SEPARE : une sauvegarde ecrite entre
    // les deux ne porte que le premier et doit se rejouer sans le second.
    rules.push("confirm_side_scheme");
    // L'ordre du livret pour ces deux temps d'arret (10/10/2026) : drapeau
    // separe, une sauvegarde ecrite avant pose ses questions dans l'ancien ordre.
    rules.push("confirm_scheme_setup_order");
    return rules;
}

export async function buildDescriptor(state) {
    const raw = await resolveScenarioRaw(state);
    const modular = state.difficulty.selectedModularSets || [];
    // Le niveau du set Standard (I, II ou III) REMPLACE celui du scenario, et
    // ne touche a rien d'autre : ni Expert, ni les modulaires, ni les sets
    // propres au scenario. Voir niveau-standard.js.
    const setsDuScenario = appliquerNiveau(raw.encounter_sets || [], state.difficulty.standard);
    const encounter_set_names = uniq([...setsDuScenario, ...modular]);
    // Premier joueur : le moteur fait toujours commencer l'index 0, on fait
    // donc pivoter les joueurs retenus pour placer le premier joueur en tête.
    // (En multijoueur par sièges, le siège N correspond au joueur N : l'ordre
    // des sièges suit donc ce choix.)
    const retenus = state.players.slice(0, state.playerCount);
    // ⚠ EN MULTI PAR SIEGES, AUCUNE ROTATION (21/09/2026). Le siege N est une
    // PERSONNE : la faire tourner donnerait a chacun le deck de son voisin, et
    // le salon — qui verifie desormais que son siege tient bien SON heros — ne
    // reconnaitrait plus rien, laissant l'invite dehors. L'ecran grise deja le
    // selecteur dans ce cas, mais c'est une politesse d'interface : la garde
    // doit vivre ICI, ou le descripteur se fabrique, et pas dans le formulaire
    // qui le remplit.
    const siegesAuxPersonnes = !!(state.salon && state.salon.multi) && state.coopEnLigne !== false;
    const pj = (!siegesAuxPersonnes && state.premierJoueur > 0
        && state.premierJoueur < retenus.length) ? state.premierJoueur : 0;
    const ordre = retenus.slice(pj).concat(retenus.slice(0, pj));
    const hero_json = ordre
        .filter((p) => p && p.deck)
        // Le NOM du joueur en jeu = deck.name. On force le NOM DU HÉROS (X-23…)
        // au lieu du nom du deck marvelcdb (« Honey Badger… »), pour que la
        // narration dise « … would activate against X-23 », pas le titre du deck.
        // `p.identity` : identité alternative choisie à l'étape des decks
        // (mêmes cartes, autres faces héros/alter-ego — voir blocIdentiteHeros).
        .map((p) => JSON.stringify({
            ...p.deck,
            hero: (p.identity && p.identity.hero) || p.deck.hero,
            name: (p.hero && p.hero.name) || p.deck.name,
        }));
    const descriptor = {
        campaign_json: JSON.stringify(raw),
        encounter_set_names,
        hero_json,
        seed: state.seed == null ? -1 : state.seed,
        timeout: state.timeoutSecondes > 0 ? state.timeoutSecondes : 0,
        challenges: raw.challenges || [],
        // te201 Intense Combatants : la case de la préparation, prise en compte
        // seulement si la partie joue TMNT Standard ou Expert (intense-combatants.js).
        rules: [...buildRules(state), ...reglesIntense(state.difficulty.intenseCombatants, encounter_set_names)],
        campaign_log: (state.mode && state.mode.id === "campaign" && state.campaignLog) ? state.campaignLog : {},
    };

    // Bataille : la seconde table, et le camp de chaque siège. Le livret ne
    // connaît que le 1v1 et le 2v2 (mc56 p.14), donc le camp se déduit du
    // siège : première moitié contre seconde moitié. `ordre` a déjà tourné
    // pour placer le premier joueur en tête, on lit donc les camps dessus.
    if (estBataille(state) && state.scenario2) {
        const raw2 = await resolveRaw(state, state.scenario2);
        if (raw2) {
            descriptor.campaign_json_2 = JSON.stringify(raw2);
            descriptor.encounter_set_names_2 = uniq([
                ...appliquerNiveau(raw2.encounter_sets || [], state.difficulty.standard),
                ...(raw2.modular_sets || []),
            ]);
            const total = hero_json.length;
            descriptor.teams = hero_json.map((_, i) => (i < Math.ceil(total / 2) ? 0 : 1));
        }
    }

    return descriptor;
}

/** Identifiants de toutes les cartes des sets de rencontre du scénario.
 *  On lit les FICHIERS de set : leurs noms ("bomb_scare") ne correspondent pas
 *  aux `set_name` des cartes ("Bomb Scare"), un filtrage par set_name ne
 *  trouverait donc jamais rien. */
async function cartesDesSets(descriptor) {
    const { api } = await import("/public/js/prepare/api.js");
    const noms = descriptor.encounter_set_names || [];
    const ids = [];
    for (const nom of noms) {
        try {
            const set = await api.encounterSet(nom);
            for (const id of (set.encounters || [])) ids.push(String(id).split(",")[0]);
        } catch (e) { /* set introuvable : on continue */ }
    }
    // Le scénario apporte aussi ses propres cartes de rencontre : sans elles,
    // les sets modulaires seuls ne fournissent souvent qu'un sbire.
    try {
        const raw = JSON.parse(descriptor.campaign_json || "{}");
        for (const id of (raw.encounters || [])) ids.push(String(id).split(",")[0]);
        for (const id of (raw.set_aside || [])) ids.push(String(id).split(",")[0]);
    } catch (e) { /* descripteur illisible : on garde les sets */ }
    return ids;
}

/** Sélectionne `combien` cartes d'un type donné parmi les sets du scénario. */
async function cartesDuScenario(descriptor, type, combien) {
    const { cards } = await import("/public/js/prepare/cards.js");
    await cards.load();
    const vus = new Set();
    const sortie = [];
    for (const id of await cartesDesSets(descriptor)) {
        const c = cards.get(id);
        if (!c || String(c.type).replace(/ /g, "") !== type) continue;
        const nom = String(c.name || "");
        if (!nom || vus.has(nom)) continue;
        vus.add(nom);
        sortie.push(id);
        if (sortie.length >= combien) break;
    }
    return sortie;
}

/** Clé de consigne lue par /sandbox.html au chargement. */
export const CLE_GARNISSAGE = "mc_sandbox_garnir";

/** Prépare le garnissage : 2 sbires + 2 complots annexes du scénario.
 *  On ne l'EXÉCUTE pas ici — cette page va être quittée pour le plateau, et
 *  toute requête différée mourrait avec elle. On dépose donc la consigne, que
 *  la page compagnon (qui, elle, survit) exécutera au bon moment.
 *  Les cartes sont visées par IDENTIFIANT : seule forme que le moteur sait
 *  fabriquer quand la carte n'est encore nulle part (voir CreateCard). */
async function preparerGarnissage(descriptor) {
    const sbires = await cartesDuScenario(descriptor, "Minion", 2);
    const complots = await cartesDuScenario(descriptor, "SideScheme", 2);
    const ids = [...sbires, ...complots];
    try {
        window.localStorage.setItem(CLE_GARNISSAGE, JSON.stringify(ids));
    } catch (e) { /* stockage indisponible : le mode reste jouable */ }
}

/**
 * Les échanges Team-Up de la mise en place (RR 1.8, annexe I) : « may », donc
 * une question par échange possible. Le deck sauvegardé n'est pas touché, seul
 * le deck de CETTE partie change (la règle vaut à chaque mise en place).
 */
async function proposerEchangesTeamUp(state) {
    const retenus = (state.players || []).slice(0, state.playerCount);
    const joueurs = retenus
        .map((p, index) => ({ index, deck: p && p.deck ? { ...p.deck, hero: (p.identity && p.identity.hero) || p.deck.hero } : null }))
        .filter((j) => j.deck);
    if (joueurs.length < 2) return state;
    await cards.load();
    const echanges = echangesTeamUp(joueurs, (id) => cards.get(id), cards.ids());
    if (!echanges.length) return state;
    const nom = (id) => { const c = cards.get(id); return c ? String(c.name).replace(/^\*\s*/, "") : id; };
    const players = [...state.players];
    for (const e of echanges) {
        const p = players[e.joueur];
        const qui = (p.hero && p.hero.name) || `${t("Joueur")} ${e.joueur + 1}`;
        const question = t("{qui} : « {retirer} » correspond au héros d’un autre joueur. Règle Team-Up (Rules Reference 1.8) : la remplacer par « {ajouter} » pour cette partie ?")
            .replace("{qui}", qui).replace("{retirer}", nom(e.retirer)).replace("{ajouter}", nom(e.ajouter));
        if (window.confirm(question)) players[e.joueur] = { ...p, deck: appliquerEchange(p.deck, e) };
    }
    return { ...state, players };
}

/** Crée la scène puis rejoint la partie (hot-seat = joue tous les héros en local).
 *
 *  `redirect: false` (campagne en ligne, plusieurs héros, 27/10/2026) : la partie
 *  est créée côté serveur (le moteur passe en `mode_campaign`) mais le navigateur
 *  de l'hôte NE PART PAS tout de suite sur le plateau — `campagne/app.js` montre
 *  d'abord un écran d'invitation (liens de siège), puis rejoint lui-même quand
 *  l'hôte clique « Rejoindre ». Sans cette option, l'hôte atterrirait seul sur le
 *  plateau avant d'avoir pu donner les liens à qui que ce soit. */
export async function launch(state, { redirect = true } = {}) {
    state = await proposerEchangesTeamUp(state);
    const descriptor = await buildDescriptor(state);
    const cmd = encodeURIComponent(JSON.stringify(descriptor));
    const res = await fetch("new?data=" + cmd);
    if (!res.ok) {
        // Un refus du serveur qui dit POURQUOI (assemblee inconnue, pleine...) : on montre son message plutot qu'un code HTTP.
        let message = "Failed to create the game (HTTP " + res.status + ")";
        try { const corps = await res.json(); if (corps && corps.error) message = corps.error; } catch (e) { /* corps absent : le code HTTP suffit */ }
        throw new Error(message);
    }

    // Mode Decouverte : on arme le coach du plateau, et on le DESARME pour tout
    // autre mode. La cle est lue par ui-app/src/board/CoucheCoach.tsx
    // (CLE_TUTORIEL) ; sa valeur est l'identifiant de la lecon courante.
    // Sans le desarmement, un tutoriel abandonne en cours de route laissait la
    // cle en place et le coach revenait sur toutes les parties suivantes.
    appliquerTutoriel(window.localStorage, state.mode);

    // Meme precaution pour la campagne : une partie ORDINAIRE doit desarmer le
    // contexte de campagne, sinon le panneau de recompenses s'ouvrirait a la
    // fin d'une partie qui n'a rien a voir et rattacherait sa victoire au
    // dernier scenario joue. L'ecran des campagnes, lui, pose la cle juste
    // avant d'appeler launch() en mode campagne : elle survit donc.
    if (!state.mode || state.mode.id !== "campaign") {
        try { window.localStorage.removeItem("mc-campagne-partie"); } catch (e) {}
    }

    // L'ancienne console separee (/sandbox.html) n'est plus ouverte : le
    // bac a sable vit desormais DANS le plateau, en panneau escamotable.
    // Le garnissage automatique disparait avec elle — on prepare
    // desormais la situation a la main, ce qui est tout l'interet.

    // Rejoint la partie : la racine "/?hot_seat" sert le jeu (marvel.html),
    // pas "?hot_seat" qui resterait sur /prepare.html.
    if (redirect) window.location.href = "/app/board.html";
    return descriptor;
}

/** La racine vers laquelle `launch({redirect: false})` renvoie une fois l'hôte prêt. */
export const URL_PLATEAU = "/app/board.html";
