// launcher.js — construit le NewGameDescriptor et lance la partie.
// IMPORTANT : reproduit à l'identique le contrat /new?data= de l'ancien scene.html.
"use strict";
import { catalog } from "/public/js/prepare/catalog.js";
import { appliquerTutoriel } from "/public/js/prepare/tutoriel-etat.js";

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
    const h = state.difficulty.heroic | 0;
    if (h > 0) rules.push("mode_heroic_" + h);
    // Règles v16 débrayables depuis le bloc « Avancé » (actives par défaut).
    if (state.reglesV16 !== false) rules.push("v16_all");
    // La tuile « Bac a sable » du selecteur de modes. Le mode passe par
    // `rules`, donc il est inscrit dans la scene et survit au chargement
    // d'une sauvegarde — on saura toujours si une victoire comptait.
    if (state.mode && state.mode.id === "sandbox") rules.push("mode_sandbox");
    // Bataille : le moteur ouvre une seconde zone de jeu, y pose le second
    // leader et enfile les phases camp par camp. Comme les autres modes, le
    // drapeau passe par `rules` et survit donc au chargement d'une sauvegarde.
    if (estBataille(state)) rules.push("mode_competitive");
    rules.push("no_crisis_of_infinite_deadpools");
    rules.push("no_encounter_cards_ignore_crisis");
    return rules;
}

export async function buildDescriptor(state) {
    const raw = await resolveScenarioRaw(state);
    const modular = state.difficulty.selectedModularSets || [];
    const encounter_set_names = uniq([...(raw.encounter_sets || []), ...modular]);
    // Premier joueur : le moteur fait toujours commencer l'index 0, on fait
    // donc pivoter les joueurs retenus pour placer le premier joueur en tête.
    // (En multijoueur par sièges, le siège N correspond au joueur N : l'ordre
    // des sièges suit donc ce choix.)
    const retenus = state.players.slice(0, state.playerCount);
    const pj = (state.premierJoueur > 0 && state.premierJoueur < retenus.length) ? state.premierJoueur : 0;
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
        rules: buildRules(state),
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
                ...(raw2.encounter_sets || []),
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

/** Crée la scène puis rejoint la partie (hot-seat = joue tous les héros en local). */
export async function launch(state) {
    const descriptor = await buildDescriptor(state);
    const cmd = encodeURIComponent(JSON.stringify(descriptor));
    const res = await fetch("new?data=" + cmd);
    if (!res.ok) throw new Error("Failed to create the game (HTTP " + res.status + ")");

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
    window.location.href = "/app/board.html";
    return descriptor;
}
