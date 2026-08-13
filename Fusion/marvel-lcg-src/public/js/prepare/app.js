// app.js - Assistant "Preparer une partie" : briefing Marvel Champions.
"use strict";
import { cardImageUrl, extensionImageUrl } from "/public/js/prepare/api.js?v=8b2b67ef";
import { cards } from "/public/js/prepare/cards.js";
import { catalog, titleize, titreDeVague } from "/public/js/prepare/catalog.js";
import { validate } from "/public/js/prepare/validation.js";
import { launch } from "/public/js/prepare/launcher.js?v=1d88f584";
import { prefs } from "/public/js/prepare/prefs.js";
import { boutonLangue, synchroniserLangueServeur, t, langueActuelle } from "/public/js/prepare/langue.js";
import { DEFIS_INFO } from "/public/js/prepare/defis-info.js";
import { HEROS_INFO } from "/public/js/prepare/heros-info.js";
import { etatSalon } from "/public/js/prepare/salon-etat.js";
import { appliquerTutoriel } from "/public/js/prepare/tutoriel-etat.js";
import { versDeckMoteur, ecartDeConversion } from "/public/js/marvelcdb/conversion.js";
import { chargerHeros } from "/public/js/marvelcdb/index.js";
import { filtrer, aspectsPresents, tagsPresents } from "/public/js/marvelcdb/filtres.js";
import { lireFavoris, basculerFavori } from "/public/js/marvelcdb/favoris.js";
import { lireBrouillon, ecrireBrouillon } from "/public/js/campagne/brouillon.js";

// CREATION D'EQUIPE POUR UNE CAMPAGNE.
//
// Le mode Campagne a son propre ecran (/campagne.html) : boite, difficulte,
// progression, histoire, carnet. Une seule chose lui manque, choisir une
// equipe — et ce selecteur-la vit ici, avec ses identites alternatives, ses
// decks marvelcdb et ses aspects. Plutot que de le dupliquer, l'ecran des
// campagnes nous envoie sur /prepare.html?campagne avec un brouillon, et on
// lui rend l'equipe. Le wizard se reduit alors a ses deux premieres etapes :
// ni mechant, ni menace, ni bouton de lancement — c'est la campagne qui
// impose tout cela.
const BROUILLON_CAMPAGNE = new URLSearchParams(window.location.search).has("campagne")
    ? lireBrouillon()
    : null;
const creationCampagne = () => !!BROUILLON_CAMPAGNE;

// Le deck que la campagne a deja enregistre, par siege. Garde a part de
// state.players : re-cliquer son propre heros appelle assignHero, qui remet le
// deck de base. Sans ce registre, un clic de curiosite ferait disparaitre le
// deck de la campagne de la liste, et il n'y aurait plus aucun moyen d'y
// revenir sans ressortir de l'ecran.
const DECKS_CAMPAGNE = new Map();

function el(tag, props, ...kids) {
    const n = document.createElement(tag);
    if (props) for (const k in props) {
        const v = props[k];
        if (v == null || v === false) continue;
        if (k === "class") n.className = v;
        else if (k === "html") n.innerHTML = v;
        else if (k === "style" && typeof v === "object") Object.assign(n.style, v);
        else if (k.startsWith("on") && typeof v === "function") n.addEventListener(k.slice(2).toLowerCase(), v);
        else n.setAttribute(k, v === true ? "" : v);
    }
    for (const kid of kids.flat()) {
        if (kid == null || kid === false) continue;
        n.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
    }
    return n;
}

const ASPECTS = {
    aggression: "#d83b32",
    justice: "#efc34a",
    leadership: "#2f7de1",
    protection: "#35a865",
    basic: "#9aa0aa",
    pool: "#a34ad9",
    // Meme mauve que le lisere des cartes Determination sur le plateau et que
    // sa pastille dans l'editeur de deck : un aspect, une couleur, partout.
    // Sans cette ligne la pastille tombait sur le gris de repli (#555).
    determination: "#965cc4",
};
const MODES = [
    { id: "solo", label: "Solo", desc: t("1 héros"), players: 1, fixed: true, mark: "1" },
    { id: "hotseat", label: t("Coop locale"), desc: t("2 à 4 héros"), players: 2, min: 2, max: 4, mark: "4" },
    { id: "campaign", label: t("Campagne"), desc: "Progression", players: 1, min: 1, max: 4, mark: "C" },
    // Bac a sable : partie normale (mêmes règles, mêmes choix), mais le plateau
    // démarre garni côté vilain et le panneau de triche s'ouvre à côté.
    { id: "sandbox", label: t("Bac à sable"), desc: t("Test des cartes"), players: 1, fixed: true, mark: "T" },
    // Decouverte : partie FIGEE (Spider-Man / Rhino / seed 42) doublee d'un
    // coach qui donne une mission a la fois. Les lecons NOMMENT des cartes
    // precises, d'ou le seed impose : voir tools/test_seed_tutoriel.py.
];
const STEPS = (creationCampagne() ? ["Équipe", "Decks"] : ["Équipe", "Decks", "Méchant", "Menace", "Final"])
    .map((s) => t(s));
const LAST_STEP = STEPS.length - 1;
const rnd = (arr) => arr[Math.floor(Math.random() * arr.length)];

const isCampaignMode = () => state.mode && state.mode.id === "campaign";

const playerLogKey = (field, i) => field.perPlayer ? ("Player " + (i + 1) + " " + field.key) : field.key;

function portrait(cardId, cls) {
    return el("div", {
        class: "portrait " + (cls || ""),
        style: cardId ? { backgroundImage: `url(${cardImageUrl(cardId)})` } : {},
    });
}

/** Portrait d'un héros qui en compte DEUX (Cloak & Dagger) : les deux visuels
 *  se partagent la tuile en diagonale, le premier en haut à gauche, le second
 *  en bas à droite.
 *
 *  Chaque moitié n'a plus que la moitié de la largeur : la garder au cadrage
 *  commun (centre, 154 %) couperait chaque personnage en plein sur la diagonale.
 *  On tire donc le cadrage de chacun VERS SON TRIANGLE — d'où les deux classes
 *  `duo-a` / `duo-b`, dont les valeurs sont réglées dans prepare.css. */
function portraitDuo(hero, cls) {
    return el("div", { class: "portrait-duo " + (cls || "") },
        portrait(hero.heroCardId, "duo duo-a"),
        portrait(hero.lie.heroCardId, "duo duo-b"),
    );
}

/** Portrait d'un héros dans la grille : double si le deck porte une identité
 *  liée, simple sinon. Un seul point de décision pour tous les appelants. */
function portraitHeros(hero, cls) {
    return hero && hero.lie ? portraitDuo(hero, cls) : portrait(hero && hero.heroCardId, cls);
}

/** Nom affiché : celui du duo (le nom du deck) quand il y a deux identités,
 *  sinon le nom du héros. « Cloak » seul mentirait sur ce qu'on voit. */
function nomAffiche(hero) {
    if (!hero) return "";
    if (hero.lie) return cleanNomDeck(hero.deck && hero.deck.name) || hero.name;
    return hero.name;
}

function cleanNomDeck(nom) {
    return String(nom || "").replace(/^\*\s*/, "").trim();
}

/** PV affichés : les deux réserves quand il y a deux identités. Elles sont
 *  distinctes (7 pour Cloak, 5 pour Dagger) et chacune se défausse séparément :
 *  n'en montrer qu'une tromperait sur ce que le joueur emmène. */
function pvAffiches(hero) {
    if (!hero || hero.hp == null) return null;
    if (hero.lie && hero.lie.hp != null) return hero.hp + " / " + hero.lie.hp;
    return String(hero.hp);
}

const state = {
    step: 0,
    mode: MODES[0],
    playerCount: 1,
    players: [0, 1, 2, 3].map((i) => ({ index: i, hero: null, deck: null, deckSource: null })),
    activeSlot: 0,
    // homebrew : decoche = uniquement les heros officiels, coche = uniquement
    // les fan-made (Stan Lee, Hulk (Rainy), Thor (Jane Foster)).
    heroFilters: { q: "", vague: "", fav: false, homebrew: false },
    scenario: null,
    extensionTab: null,
    difficulty: {
        base: "standard",
        skirmish: false,
        heroic: 0,
        modularConfig: "recommended",
        selectedModularSets: [],
        scenarioOptions: {},
    },
    seed: null,
    // Bloc « Avancé » de l'étape finale.
    timeoutSecondes: 0,   // 0 = illimité
    premierJoueur: 0,     // index dans les joueurs retenus (rotation au lancement)
    // Salon multijoueur : les invites choisissent leur heros et leur deck depuis
    // LEUR siege. En solo, /get_choix_sieges rend multi:false et tout ce qui
    // depend de `salon` reste inerte : le wizard se comporte comme avant.
    salon: { multi: false, sieges: {}, prete: true, manquants: [], choixParSiege: new Map() },
    // Sur un serveur qui accepte des invites, l'hote peut TOUJOURS vouloir jouer
    // plusieurs heros lui-meme, autour du meme ecran. C'est donc un choix, jamais
    // une deduction du serveur. Vrai par defaut : si on a lance le serveur en
    // ligne, c'est presque toujours pour attendre du monde.
    coopEnLigne: true,
    reglesV16: true,      // pousse "v16_all" dans rules (défaut actif)
};

/**
 * Les autres sieges sont-ils tenus par des personnes A DISTANCE ?
 *
 * Deux conditions, et il faut les deux : le serveur accepte des invites
 * (`salon.multi`), ET l'hote a choisi de les attendre (`coopEnLigne`).
 * Tout ce qui attend quelqu'un doit passer par ici, jamais par `salon.multi`
 * seul : sinon une partie hot-seat lancee depuis le serveur en ligne resterait
 * bloquee a attendre un invite qui ne viendra pas.
 */
function enLigne() {
    return state.salon.multi && state.coopEnLigne !== false;
}

function activePlayers() {
    return state.players.slice(0, state.playerCount);
}

function stepComplete(step) {
    const active = activePlayers();
    switch (step) {
        // En multi, les sieges des invites sont remplis par le SALON : bloquer
        // la navigation dessus condamnerait l'hote a attendre sur l'ecran des
        // heros sans rien pouvoir faire. Seul son propre siege le retient ; le
        // LANCEMENT, lui, attend tout le monde (validate + salon.prete).
        case 0: return !!state.mode && (enLigne() ? !!active[0] && !!active[0].hero : active.every((p) => p.hero));
        case 1: return enLigne() ? !!active[0] && !!active[0].deck : active.every((p) => p.deck);
        case 2: return !!state.scenario;
        case 3: return true;
        case 4: return validate(state).ok;
        default: return false;
    }
}
function canContinue() { return stepComplete(state.step); }
function goto(step) {
    if (step < 0 || step > LAST_STEP) return;
    if (step > state.step) {
        for (let s = state.step; s < step; s++) if (!stepComplete(s)) return;
    }
    hideHover();
    state.step = step;
    render();
}
const next = () => { if (canContinue()) goto(state.step + 1); };
const prev = () => goto(state.step - 1);

async function randomize() {
    if (state.step === 0) {
        const heroes = await catalog.heroes();
        const used = new Set(activePlayers().filter((p) => p.hero).map((p) => p.hero.id));
        for (let i = 0; i < state.playerCount; i++) {
            if (state.players[i].hero) continue;
            const pool = heroes.filter((h) => !used.has(h.id));
            const hero = rnd(pool.length ? pool : heroes);
            assignHero(i, hero);
            used.add(hero.id);
        }
        render();
    } else if (state.step === 2) {
        // En campagne, l'ordre est imposé : on ne tire pas de scénario au hasard.
        if (!isCampaignMode()) {
            const scs = await catalog.scenariosForExtension(state.extensionTab);
            if (scs.length) selectScenario(rnd(scs));
        }
        render();
    } else if (state.step === 3) {
        state.difficulty.modularConfig = "random";
        applyModularConfig();
        render();
    }
}

function assignHero(slotIndex, hero) {
    const p = state.players[slotIndex];
    p.hero = hero;
    p.deck = hero.deck;
    p.deckSource = "base";
    // Deck posé automatiquement : l'étape Decks pourra le remplacer par le
    // dernier deck utilisé pour ce héros (mémoire des choix).
    p.deckAuto = true;
}

/* ---------------- Salon multijoueur ---------------- */

/** Traduit les choix recus en heros + deck dans state.players. */
async function appliquerChoixSalon() {
    // En coop locale sur un serveur en ligne, les sieges sont a l'hote : un
    // choix arrive du salon ne doit surtout pas ecraser le sien.
    if (!enLigne()) return;
    const heroes = await catalog.heroes();
    for (const [p, choix] of state.salon.choixParSiege) {
        // Le siege 0 est celui de l'hote : il choisit dans SON wizard.
        if (p === 0 || p >= state.playerCount) continue;
        const hero = heroes.find((h) => h.heroCardId === choix.hero_card_id);
        if (!hero) continue;
        const joueur = state.players[p];
        if (!joueur) continue;
        const decks = await catalog.decksForHero(hero);
        const dk = decks.find((d) => d.id === choix.deck_id);
        if (!dk) continue;
        joueur.hero = hero;
        joueur.deck = dk.deck;
        joueur.deckSource = dk.source;
        joueur.deckAuto = false;
        joueur.duSalon = true;
    }
}

async function sonderSalon() {
    let brut;
    try {
        const res = await fetch("get_choix_sieges?");
        brut = await res.json();
    } catch (e) {
        return;  // serveur momentanement injoignable : on reessaiera
    }
    // Hors multi, on remet l'etat NEUTRE et on s'arrete la. Sans ce garde-fou,
    // etatSalon conclurait « il manque le Joueur 2 » sur une partie hot-seat a
    // deux, et le bouton de lancement resterait grise en SOLO.
    if (!brut.multi) {
        state.salon = { multi: false, sieges: {}, prete: true, manquants: [], choixParSiege: new Map() };
        return;
    }
    const calcul = etatSalon({ nombreJoueurs: state.playerCount, sieges: brut.sieges || {} });
    const empreinte = JSON.stringify([brut.multi, brut.sieges, state.playerCount]);
    state.salon = { multi: true, sieges: brut.sieges || {}, ...calcul };
    await appliquerChoixSalon();
    if (empreinte !== sonderSalon.derniere) {
        sonderSalon.derniere = empreinte;
        render();
    }
}

/** Mode Découverte : la partie est imposée, on saute les 5 étapes.
 *  Spider-Man contre Rhino, seed 42 : ce sont ces valeurs exactes qui rendent
 *  les leçons possibles (elles nomment des cartes). Le garde-fou est
 *  tools/test_seed_tutoriel.py. */
async function preparerDecouverte() {
    state.seed = 42;
    state.premierJoueur = 0;
    try {
        const heroes = await catalog.heroes();
        const spiderman = heroes.find((h) => h.id === "spider_man");
        // Les scénarios se listent PAR EXTENSION : catalog.scenarios() n'existe pas.
        const exts = await catalog.extensions();
        const boite = exts.find((e) => (e.scenarios || []).includes("rhino"));
        const scs = boite ? await catalog.scenariosForExtension(boite.key) : [];
        const rhino = scs.find((sc) => sc.id === "rhino");
        if (spiderman && rhino) {
            assignHero(0, spiderman);
            selectScenario(rhino);
            state.step = LAST_STEP;
        }
    } catch (e) {
        // Catalogue indisponible : on laisse le joueur faire les étapes à la main
        // plutôt que de le bloquer sur un mode qui ne démarre pas.
        console.error("mode Découverte:", e);
    }
    render();
}

function selectScenario(sc) {
    state.scenario = sc;
    state.difficulty.base = sc.expert ? "expert" : "standard";
    state.difficulty.modularConfig = "recommended";
    applyModularConfig();
    prefs.setLastScenario(sc.id);
}

function applyModularConfig() {
    const sc = state.scenario;
    if (!sc) return;
    const d = state.difficulty;
    if (d.modularConfig === "recommended") {
        d.selectedModularSets = [...sc.recommendedModularSets];
    } else if (d.modularConfig === "random") {
        catalog.encounterSets().then((all) => {
            const pool = all.filter((s) => s.kind === "modular").map((s) => s.name);
            const k = Math.max(1, sc.modularSlots.min || 1);
            const picked = new Set();
            while (picked.size < k && picked.size < pool.length) picked.add(rnd(pool));
            d.selectedModularSets = [...picked];
            render();
        });
    }
}

const root = document.getElementById("app");

// La police Marvel ne contient pas d'accents : on les retire du texte
// affiché en police Marvel (.mvl et labels d'étapes) pour éviter le mélange
// de polices (« HÉROS » -> « HEROS »).
function deaccent(s) { return String(s).normalize("NFD").replace(/[̀-ͯ]/g, ""); }
function fixMarvelText() {
    document.querySelectorAll(".mvl, .pstep .plabel, .brand-title").forEach((elm) => {
        const walker = document.createTreeWalker(elm, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = walker.nextNode())) { const d = deaccent(n.nodeValue); if (d !== n.nodeValue) n.nodeValue = d; }
    });
}

/**
 * Dit a la grille ou elle commence, pour qu'elle sache ou s'arreter.
 *
 * La grille des heros defile a l'interieur d'elle-meme et sa hauteur etait
 * `62vh` : une fraction de la FENETRE, qui ne sait rien de ce qui la precede
 * (titre, recherche, filtres). Sur un ecran court sa boite descendait sous la
 * barre fixe du bas, et la derniere rangee de heros s'y trouvait coupee en
 * plein sur les noms — signale en jeu, en mode campagne.
 *
 * On mesure avec getBoundingClientRect() + scrollY, PAS avec offsetTop :
 * offsetTop se compte depuis le premier ancetre positionne, et l'animation
 * d'apparition de .step pose un transform qui en cree un le temps de la
 * transition — la mesure valait alors 194 px au lieu de 336, et le plafond ne
 * mordait plus. La position dans le document, elle, ne ment pas.
 *
 * La mesure ne peut pas etre prise une fois pour toutes : ce qui precede la
 * grille bouge apres coup — la barre de filtres se replie sur une fenetre
 * etroite, les listes d'equipes et d'extensions se remplissent une fois les
 * heros charges. Mesuree trop tot, la valeur valait 194 px au lieu de 336, et
 * le plafond ne mordait pas. On observe donc la page plutot que de parier sur
 * un delai.
 *
 * Pas de boucle a craindre : ce qu'on ecrit change la HAUTEUR de la grille,
 * jamais sa position ; la mesure suivante rend la meme valeur et la garde
 * d'egalite arrete la chaine.
 */
function ajusterGrilles() {
    document.querySelectorAll(".hero-grid, .scn-grid").forEach((grille) => {
        const haut = Math.round(grille.getBoundingClientRect().top + window.scrollY);
        if (grille.style.getPropertyValue("--grille-haut") !== haut + "px") {
            grille.style.setProperty("--grille-haut", haut + "px");
        }
    });
}

window.addEventListener("resize", ajusterGrilles);

const observateurGrilles = typeof ResizeObserver === "function"
    ? new ResizeObserver(ajusterGrilles)
    : null;

/**
 * On surveille CE QUI POUSSE la grille vers le bas : ses freres precedents.
 *
 * Observer la seule .step ne suffisait pas — quand un frere du dessus grandit,
 * la grille se retracte d'autant et la hauteur de .step ne bouge pas : aucune
 * notification, et la mesure restait fausse de plusieurs dizaines de pixels,
 * juste assez pour repasser sous la barre.
 */
function surveillerGrilles() {
    if (!observateurGrilles) return;
    observateurGrilles.disconnect();
    document.querySelectorAll(".hero-grid, .scn-grid").forEach((grille) => {
        for (let frere = grille.previousElementSibling; frere; frere = frere.previousElementSibling) {
            observateurGrilles.observe(frere);
        }
    });
}

function render() {
    root.replaceChildren(
        progressBar(),
        el("div", { class: "layout" },
            el("main", { class: "stage" }, stepView()),
            recapPanel(),
        ),
        navBar(),
    );
    fixMarvelText();
    ajusterGrilles();
    surveillerGrilles();
}

function progressBar() {
    // Le titre de l'onglet est ecrit en dur en ANGLAIS dans prepare.html, donc
    // faux des qu'on joue en francais. On le repose ici, ou t() existe.
    document.title = t("Préparation de mission") + " — Marvel Champions";
    const entete = el("header", { class: "progress" },
        el("a", { class: "brand", href: "main" },
            el("span", { class: "brand-back" }, "<"),
            el("span", { class: "brand-lockup logo" },
                el("img", { class: "brand-logo", src: "/mvc_logo.svg", alt: "Marvel Champions" }),
                el("span", { class: "brand-sub" }, t("Préparation de mission")),
            ),
        ),
        boutonLangue("btn ghost btn-langue"),
        el("div", { class: "steps" }, STEPS.map((label, i) => {
            const done = i < state.step && stepComplete(i);
            const cls = "pstep" + (i === state.step ? " active" : "") + (done ? " done" : "");
            return el("button", { class: cls, onclick: () => goto(i) },
                el("span", { class: "pnum" }, done ? "OK" : String(i + 1)),
                el("span", { class: "plabel" }, label));
        })),
    );
    // Adopte la rangee d'outils (Reprendre/Stats/Puzzles/Galerie) creee par
    // les scripts annexes : le header est reconstruit a chaque rendu, on
    // DEPLACE donc le noeud vivant (listeners conserves) a cote du bouton
    // langue plutot que de le laisser flotter par-dessus les etapes.
    const rangee = document.querySelector(".reprise-boutons");
    if (rangee) {
        rangee.classList.remove("est-flottante");
        entete.insertBefore(rangee, entete.querySelector(".steps"));
    }
    return entete;
}

function navBar() {
    const showRandom = [0, 2, 3].includes(state.step);
    return el("footer", { class: "nav" },
        el("button", { class: "btn ghost", disabled: state.step === 0 || undefined, onclick: prev }, t("Retour")),
        el("div", { class: "nav-status" }, navStatus()),
        el("div", { class: "spacer" }),
        showRandom ? el("button", { class: "btn ghost", onclick: randomize }, t("Aléatoire")) : el("span"),
        state.step < LAST_STEP
            ? el("button", { class: "btn primary", disabled: !canContinue() || undefined, onclick: next },
                t("Continuer"))
            : creationCampagne()
                ? el("button", {
                    class: "btn launch",
                    disabled: !stepComplete(1) || undefined,
                    onclick: validerEquipeCampagne,
                }, BROUILLON_CAMPAGNE.modifie ? t("Valider les decks") : t("Valider l'équipe"))
                : el("button", {
                    class: "btn launch",
                    disabled: (!validate(state).ok || (enLigne() && !state.salon.prete)) || undefined,
                    onclick: doLaunch,
                }, t("Lancer la partie")),
    );
}

function navStatus() {
    if (enLigne() && !state.salon.prete) {
        const qui = state.salon.manquants.map((n) => `${t("Joueur")} ${n}`).join(", ");
        return `${t("En attente de")} ${qui}`;
    }
    const heroes = activePlayers().filter((p) => p.hero).length;
    if (creationCampagne()) {
        return `${heroes}/${state.playerCount} ${t("héros")} - ${t("équipe de campagne")}`;
    }
    const sc = state.scenario ? state.scenario.name : t("Cible inconnue");
    return `${heroes}/${state.playerCount} ${t("héros")} - ${sc}`;
}

async function doLaunch() {
    // Le carnet ne vient plus d'ici : l'ecran des campagnes le passe lui-meme a
    // `launch()` (voir `lancerScenario` dans public/js/campagne/app.js). Cet ecran
    // ne lance donc jamais de partie de campagne.
    state.campaignLog = {};
    try { await launch(state); }
    catch (e) { alert(t("Erreur de lancement :") + " " + e.message); }
}

/**
 * Rend l'équipe à l'écran des campagnes et s'efface.
 *
 * On fige ici la forme DÉFINITIVE de chaque héros — identité résolue, nom du
 * héros plutôt que titre du deck — pour que la campagne relance ses cinq
 * scénarios sans jamais avoir à redemander quoi que ce soit. Le deck est
 * recopié en entier : c'est ce que le moteur consomme, et une campagne doit
 * survivre à la suppression du deck marvelcdb dont elle est partie.
 */
/**
 * Modification des decks : on remet l'equipe en place telle que la campagne
 * l'a enregistree.
 *
 * Sans cela l'ecran revenait vierge, et le joueur devait re-choisir ses heros
 * dans le meme ordre sous peine de refus au retour (le livret fige les
 * identites). Le geste demande ici est d'AJUSTER un deck, pas de refaire une
 * equipe : elle est donc deja la, et seule l'etape des decks attend un clic.
 *
 * Le heros se retrouve par sa CARTE d'identite, jamais par son nom : le nom
 * est traduit a l'affichage, la carte non. Une identite alternative (The Thing
 * Avenger ou Guardian) est portee par `variants`, d'ou la seconde recherche.
 */
async function reprendreEquipeCampagne() {
    const membres = (BROUILLON_CAMPAGNE && BROUILLON_CAMPAGNE.modifie
        && BROUILLON_CAMPAGNE.equipeActuelle) || [];
    if (!membres.length) return;
    const heroes = await catalog.heroes();
    membres.forEach((m, i) => {
        const p = state.players[i];
        if (!p) return;
        const carte = String((m.identite && m.identite[0]) || "").split(",")[0];
        const hero = heroes.find((h) => h.heroCardId === carte)
            || heroes.find((h) => (h.variants || []).some((v) => v.heroCardId === carte));
        if (!hero || !m.deck) return;
        p.hero = hero;
        p.identity = (hero.variants || []).find((v) => v.heroCardId === carte) || null;
        p.deck = m.deck;
        // Source a part : ce deck ne vient d'aucune liste de l'ecran, il a ete
        // compose puis range dans la campagne. loadDecks lui fabrique son
        // entree, sinon il serait le seul choix impossible a re-selectionner.
        p.deckSource = "campagne";
        p.deckAuto = false;
        DECKS_CAMPAGNE.set(i, m.deck);
    });
}

function validerEquipeCampagne() {
    const brouillon = BROUILLON_CAMPAGNE;
    brouillon.equipe = activePlayers().filter((p) => p && p.deck).map((p) => {
        const identite = (p.identity && p.identity.hero) || p.deck.hero || [];
        const nomHeros = (p.hero && p.hero.name) || p.deck.name || "";
        return {
            heros: (p.hero && p.hero.id) || "",
            nomHeros,
            identite,
            deck: { ...p.deck, hero: identite, name: nomHeros },
        };
    });
    ecrireBrouillon(brouillon);
    window.location.href = "/campagne.html";
}

function recapPanel() {
    const p = el("aside", { class: "recap" },
        // Aperçu du héros survolé : prend toute la colonne à la place de la
        // fiche de mission (classe `apercu` sur .recap), puis s'efface.
        el("div", { class: "recap-apercu", id: "recap-apercu" }),
        el("div", { class: "recap-title mvl" }, t("Fiche de mission")),
        recapRow("Mode", state.mode ? libelleMode(state.mode) + " - " + state.playerCount + "p" : "-"),
    );
    const players = el("div", { class: "recap-block team" }, el("div", { class: "recap-k" }, t("Équipe")));
    for (let i = 0; i < state.playerCount; i++) {
        const pl = state.players[i];
        const on = state.step === 0 && state.activeSlot === i;
        // En multi, un siege d'invite appartient a son occupant : l'hote ne
        // peut pas lui choisir son heros a sa place.
        const pilotable = !(enLigne() && i > 0);
        players.append(el("button", {
            class: "recap-slot cut" + (on ? " active" : "") + (pl.hero ? " filled" : "") + (pilotable ? "" : " salon-invite"),
            disabled: pilotable ? undefined : "",
            title: pilotable ? undefined : t("Ce joueur choisit depuis son propre écran"),
            onclick: () => { if (!pilotable) return; state.activeSlot = i; goto(0); },
        },
            pl.hero
                ? portrait(pl.hero.heroCardId, "team")
                : el("div", { class: "portrait team empty" }, el("span", { class: "plus mvl" }, "+")),
            el("div", { class: "rs-meta" },
                el("div", { class: "rh-name" }, pl.hero ? pl.hero.name : t("Joueur") + " " + (i + 1)),
                el("div", { class: "rh-sub" }, pl.hero
                    ? (pl.deck ? (pl.deckSource === "base" ? t("Deck de base") : pl.deck.name) : t("Deck à choisir"))
                    : t("Emplacement vide")),
            ),
        ));
    }
    p.append(players);

    const sc = state.scenario;
    p.append(el("div", { class: "recap-block target" },
        el("div", { class: "recap-k" }, t("Cible")),
        el("div", { class: "recap-scn" },
            portrait(sc ? sc.tileImage : null, "mini villain"),
            el("div", {},
                el("div", { class: "rh-name" }, sc ? sc.name : "-"),
                el("div", { class: "rh-sub" }, sc && sc.villainNames.length ? sc.villainNames.join(", ") : t("Méchant non défini")),
            ),
        ),
    ));
    if (sc) {
        const d = state.difficulty;
        const tags = [d.base === "expert" ? "Expert" : "Standard"];
        if (d.skirmish) tags.push("Skirmish");
        if (d.heroic > 0) tags.push(t("Héroïque") + " " + d.heroic);
        p.append(recapRow(t("Menace"), tags.join(" - ")));
        p.append(recapRow(t("Sets modulaires"), String(d.selectedModularSets.length)));
    }
    return p;
}
function recapRow(k, v) {
    return el("div", { class: "recap-row" },
        el("span", { class: "recap-k" }, k),
        el("span", { class: "recap-v" }, v),
    );
}

function stepView() {
    switch (state.step) {
        case 0: return stepTeam();
        case 1: return stepDecks();
        case 2: return stepScenario();
        case 3: return stepDifficulty();
        case 4: return stepSummary();
    }
}

function stepHead(kicker, title, sub) {
    return el("div", { class: "step-head" },
        el("div", { class: "kicker" }, kicker),
        el("h1", { class: "mvl" }, title),
        sub ? el("p", {}, sub) : null,
    );
}

/**
 * Libelle du mode tel qu'il doit s'AFFICHER. « Coop locale » devient « Coop en
 * ligne » des que le serveur annonce une partie en ligne. A utiliser PARTOUT ou
 * le mode est montre a l'utilisateur : le recapitulatif qui afficherait encore
 * « locale » recreerait exactement la confusion que ce renommage supprime.
 */
function libelleMode(m) {
    if (!m) return "-";
    return enLigne() && m.id === "hotseat" ? t("Coop en ligne") : m.label;
}

function modeStrip() {
    const strip = el("div", { class: "mode-strip" });
    // En création d'équipe pour une campagne, le mode et le nombre de héros
    // sont déjà décidés et ne se rediscutent pas : on l'annonce au lieu de
    // proposer des tuiles qui mentiraient.
    if (creationCampagne()) {
        strip.append(el("div", { class: "mode-pill sel campagne-bandeau" },
            el("span", { class: "mode-mark mvl" }, "C"),
            el("span", { class: "mode-copy" },
                el("b", {}, (BROUILLON_CAMPAGNE.modifie ? t("Modifier les decks") : t("Campagne"))
                    + " — " + BROUILLON_CAMPAGNE.nom),
                // En modification, l'equipe est deja remise en place : le
                // bandeau dit ce qui reste interdit, l'identite, et nomme
                // celles qui sont engagees.
                el("small", {}, BROUILLON_CAMPAGNE.modifie
                    ? t("Équipe déjà en place. Change ce que tu veux au deck, jamais l'identité :")
                        + " " + (BROUILLON_CAMPAGNE.identites || []).join(", ")
                    : BROUILLON_CAMPAGNE.nbJoueurs + " " + t("héros") + " · "
                        + (BROUILLON_CAMPAGNE.difficulte === "expert" ? t("Campagne experte") : t("Standard"))
                        + " · " + t("identités figées pour toute la campagne")),
            ),
        ));
        return strip;
    }
    // « Coop locale » MENT quand la partie est en ligne : les autres joueurs ne
    // sont pas a cote de toi, et ils choisissent eux-memes leur heros. Le
    // serveur nous dit deja s'il s'agit d'une partie en ligne (salon.multi), on
    // renomme donc a la volee. Pas de mode supplementaire : le moteur n'en
    // connait pas, et un mode de plus serait un etat de plus a tenir juste.
    const distant = enLigne();
    for (const m of MODES) {
        const on = state.mode.id === m.id;
        const libelle = libelleMode(m);
        const detail = distant && m.id === "hotseat" ? t("2 à 4 héros, chacun choisit le sien") : m.desc;
        strip.append(el("button", {
            class: "mode-pill" + (on ? " sel" : ""),
            onclick: () => {
                // La campagne n'est plus un mode du wizard : elle a son écran,
                // qui impose l'ordre des scénarios, les sets et la difficulté.
                if (m.id === "campaign") { window.location.href = "/campagne.html"; return; }
                const wasCampaign = isCampaignMode();
                state.mode = m;
                // Le catalogue de scénarios diffère en campagne : on repart d'une cible vierge.
                if ((m.id === "campaign") !== wasCampaign) state.scenario = null;
                state.playerCount = m.fixed ? 1 : Math.max(m.min || 1, Math.min(m.max || 4, state.playerCount));
                if (state.activeSlot >= state.playerCount) state.activeSlot = state.playerCount - 1;
                if (m.id === "decouverte") { preparerDecouverte(); return; }
                render();
            },
        },
            el("span", { class: "mode-mark mvl" }, m.mark),
            el("span", { class: "mode-copy" },
                el("b", {}, libelle),
                el("small", {}, detail),
            ),
        ));
    }
    return strip;
}

/**
 * Dit a l'hote, en une phrase et avant qu'il ne se pose la question, ce qu'on
 * attend de lui quand la partie est en ligne. Sans ce bandeau il doit deviner
 * s'il choisit pour tout le monde ou seulement pour lui.
 * Rend null hors ligne : aucun bandeau ne s'affiche en solo ni en hot-seat.
 */
/**
 * Sur un serveur qui accepte des invites, l'hote choisit ici qui tient les
 * autres sieges. Ce choix n'existe que la : ailleurs il n'y a rien a decider,
 * et un bouton de plus serait du bruit.
 */
function choixCoop() {
    if (!state.salon.multi || state.mode.id !== "hotseat") return null;
    const bouton = (distant, titre, detail) => el("button", {
        class: "coop-choix" + ((state.coopEnLigne !== false) === distant ? " sel" : ""),
        onclick: () => { state.coopEnLigne = distant; render(); },
    }, el("b", { class: "mvl" }, titre), el("small", {}, detail));
    return el("div", { class: "coop-bascule" },
        bouton(true, t("Chacun sur son appareil"), t("Les autres joueurs choisissent leur héros depuis leur lien")),
        bouton(false, t("Tous sur cet écran"), t("Tu choisis et joues tous les héros toi-même")),
    );
}

function bandeauEnLigne() {
    // A un seul joueur il n'y a pas d'« autres joueurs » : le bandeau mentirait.
    if (!enLigne() || state.playerCount < 2) return null;

    // Qui a choisi, et QUOI. Sans cette liste, l'hote ne savait que le nombre
    // de manquants — d'ou le « on peut lancer ? » sur Discord a chaque partie.
    // Sieges invites uniquement : le 0 est le sien, il le voit dans son wizard.
    const lignes = [];
    for (let p = 1; p < state.playerCount; p += 1) {
        const choix = state.salon.choixParSiege.get(p);
        const joueur = state.players[p];
        const pret = !!choix && !!joueur && !!joueur.hero;
        lignes.push(el("li", { class: "salon-siege" + (pret ? " est-pret" : "") },
            el("span", { class: "salon-siege-marque" }, pret ? "✓" : "·"),
            // Libelle affiche = index technique + 1 (voir salon-etat.js).
            el("b", {}, `${t("Joueur")} ${p + 1}`),
            el("span", { class: "salon-siege-choix" },
                pret ? joueur.hero.name : t("en attente de son choix")),
        ));
    }

    return el("div", { class: "salon-bandeau" },
        el("b", { class: "mvl" }, t("Partie en ligne")),
        el("span", {}, t("Choisis seulement TON héros et TON deck. Les autres joueurs choisissent les leurs depuis le lien que tu leur as envoyé.")),
        el("ul", { class: "salon-sieges" }, ...lignes),
    );
}

function playerCountRow() {
    if (state.mode.fixed) return null;
    // Le nombre de héros d'une campagne est arrêté à sa création : le changer
    // ici produirait une équipe que la campagne refuserait ensuite.
    if (creationCampagne()) return null;
    const row = el("div", { class: "count-row" }, el("span", { class: "lbl" }, t("Joueurs")));
    for (let n = (state.mode.min || 1); n <= (state.mode.max || 4); n++) {
        row.append(el("button", {
            class: "count-btn" + (state.playerCount === n ? " sel" : ""),
            onclick: () => {
                state.playerCount = n;
                if (state.activeSlot >= n) state.activeSlot = n - 1;
                render();
            },
        }, String(n)));
    }
    return row;
}

function stepTeam() {
    const wrap = el("section", { class: "step team-step" },
        el("div", { class: "team-header" },
            stepHead("Briefing 01", t("Rassemble tes héros"), t("Sélection prête")),
            bandeauEnLigne(),
            el("div", { class: "command-band" }, modeStrip(), playerCountRow()),
            choixCoop(),
        ),
    );
    const f = state.heroFilters;
    wrap.append(el("div", { class: "filterbar" },
        el("input", {
            class: "search",
            placeholder: t("Rechercher un héros"),
            value: f.q,
            oninput: (e) => { f.q = e.target.value; refreshHeroGrid(); },
        }),
        el("button", {
            class: "chip" + (f.fav ? " on" : ""),
            onclick: () => { f.fav = !f.fav; refreshHeroGrid(); },
        }, t("Favoris")),
        el("select", {
            class: "sel vague-select",
            onchange: (e) => { f.vague = e.target.value; refreshHeroGrid(); },
        }, el("option", { value: "" }, t("Toutes les vagues"))),
        el("button", {
            class: "chip" + (f.homebrew ? " on" : ""),
            title: t("Héros fan-made, hors de toute extension officielle"),
            onclick: (e) => {
                f.homebrew = !f.homebrew;
                e.currentTarget.classList.toggle("on", f.homebrew);
                // Les fan-made n'appartiennent a aucune vague : garder un filtre
                // de vague actif en passant de l'un a l'autre ne rendrait jamais
                // rien. On le relache, et le menu se cache (voir majMenuVagues).
                f.vague = "";
                majMenuVagues();
                refreshHeroGrid();
            },
        }, "Fan-made"),
    ));
    wrap.append(el("div", { class: "hero-grid full", id: "hero-grid" }, el("div", { class: "loading" }, t("Chargement des héros..."))));
    loadHeroes();
    return wrap;
}

/** Libellé d'une vague : la vague 0 est le Set de base, qui n'en est pas une.
 *
 *  Les autres portent le numero ET le titre de leur grande boite, parce que le
 *  numero seul ne dit rien a qui connait le jeu par ses boites — et parce que
 *  notre numerotation compte une vague de plus que celle qui circule dans la
 *  communaute (elle ne compte pas les premiers paquets), donc le titre est ce
 *  qui leve l'ambiguite. Une vague sans titre connu garde son numero seul. */
function nomDeVague(vague) {
    if (vague === 0) return t("Set de base");
    // Le titre de la boite ne passe PAS par t() : il reste en anglais dans les
    // deux langues, comme partout ailleurs dans l'appli (voir NOMS_VAGUES).
    // La vague 1 n'a pas de boite : son libelle est de nous, donc traduit.
    const titre = vague === 1 ? t("Les premiers paquets") : titreDeVague(vague);
    return t("Vague") + " " + vague + (titre ? " · " + titre : "");
}

/** Remplit le menu des vagues avec CELLES QUI EXISTENT dans la liste affichable.
 *
 *  On ne code pas la liste en dur : elle se deduit des heros charges, donc une
 *  vague a venir apparaitra d'elle-meme, et une vague dont aucun heros n'est
 *  installe ne proposera pas un filtre qui ne rendrait rien.
 *
 *  Cote fan-made il n'y a aucune vague : le menu se cache plutot que d'afficher
 *  un choix unique et inerte. */
function majMenuVagues(heroes) {
    const sel = document.querySelector(".vague-select");
    if (!sel) return;
    const liste = heroes || _herosCharges;
    if (!liste) return;
    const f = state.heroFilters;
    const vagues = [...new Set(liste
        .filter((h) => !!h.homebrew === f.homebrew && h.vague != null)
        .map((h) => h.vague))].sort((a, b) => a - b);
    sel.replaceChildren(el("option", { value: "" }, t("Toutes les vagues")));
    vagues.forEach((v) => sel.append(
        el("option", { value: String(v), selected: f.vague === String(v) }, nomDeVague(v))));
    sel.hidden = vagues.length === 0;
}

let _herosCharges = null;

async function loadHeroes() {
    const heroes = await catalog.heroes();
    _herosCharges = heroes;
    majMenuVagues(heroes);
    refreshHeroGrid(heroes);
}

async function refreshHeroGrid(pre) {
    if (!document.getElementById("hero-grid")) return;
    const heroes = pre || await catalog.heroes();
    const grid = document.getElementById("hero-grid");
    if (!grid) return;
    const f = state.heroFilters;
    const q = f.q.toLowerCase();
    const favs = prefs.favHeroes();
    const list = heroes.filter((h) =>
        (!q || h.name.toLowerCase().includes(q)) &&
        (!f.vague || String(h.vague) === f.vague) &&
        (!f.fav || favs.includes(h.id)) &&
        // Le homebrew est masqué par défaut et s'affiche seul quand on le coche.
        (!!h.homebrew === f.homebrew));
    if (!list.length) {
        grid.replaceChildren(el("div", { class: "empty-state" }, t("Aucun héros trouvé")));
        return;
    }
    grid.replaceChildren(...list.map((h) => {
        const chosen = activePlayers().some((p) => p.hero && p.hero.id === h.id);
        return el("button", {
            class: "hero-card cut" + (chosen ? " chosen" : ""),
            onclick: () => { assignHero(state.activeSlot, h); autoAdvanceSlot(); render(); },
            onmouseenter: (e) => showHeroHover(h, e.currentTarget),
            onmouseleave: scheduleHide,
        },
            portraitHeros(h),
            el("span", { class: "hc-name mvl" }, nomAffiche(h)),
            pvAffiches(h) ? el("span", { class: "hc-hp" }, t("PV") + " " + pvAffiches(h)) : null,
            // Pastille discrète : ce héros a au moins un art alternatif.
            (ARTS_HEROS[String(h.heroCardId || "").split(",")[0]] || []).length
                ? el("span", { class: "hc-art", title: t("Art alternatif disponible") }, t("ART ALT"))
                : null,
            el("span", {
                class: "hc-fav" + (prefs.isFavHero(h.id) ? " on" : ""),
                title: t("Favori"),
                onclick: (e) => {
                    e.stopPropagation();
                    e.preventDefault();
                    const on = prefs.toggleFavHero(h.id);
                    e.currentTarget.classList.toggle("on", on);
                },
            }, "★"),
        );
    }));
}

function autoAdvanceSlot() {
    for (let i = 0; i < state.playerCount; i++) {
        if (!state.players[i].hero) {
            state.activeSlot = i;
            return;
        }
    }
}

let _hoverPop = null, _hideTimer = null;
function hoverPop() {
    if (!_hoverPop) {
        _hoverPop = el("div", {
            class: "card-hover",
            id: "card-hover",
            onmouseenter: () => clearTimeout(_hideTimer),
            onmouseleave: scheduleHide,
        });
        document.body.appendChild(_hoverPop);
    }
    return _hoverPop;
}
function positionHover(box, anchorEl) {
    // Aperçu large (les trois cartes d'une collection) : le coller à la vignette
    // le fait déborder et masque une carte sur deux. On le sort donc du flux et
    // on le centre en haut de l'écran, au niveau des decks.
    if (box.classList.contains("trio")) {
        const bw = box.offsetWidth || 900;
        const bh = box.offsetHeight || 460;
        let y = Math.round(window.innerHeight * 0.12);
        if (y + bh > window.innerHeight - 12) y = Math.max(12, window.innerHeight - bh - 12);
        box.style.left = Math.max(12, Math.round((window.innerWidth - bw) / 2)) + "px";
        box.style.top = y + "px";
        return;
    }
    const r = anchorEl.getBoundingClientRect();
    const bw = box.offsetWidth || 284;
    const pad = 12;
    let x = r.right + 12;
    if (x + bw > window.innerWidth - pad) x = r.left - bw - 12;
    if (x < pad) x = pad;
    const bh = box.offsetHeight || 460;
    let y = r.top - 10;
    if (y + bh > window.innerHeight - pad) y = window.innerHeight - bh - pad;
    if (y < pad) y = pad;
    box.style.left = x + "px";
    box.style.top = y + "px";
}
function popShow(box, anchorEl) {
    clearTimeout(_hideTimer);
    box.classList.add("show");
    positionHover(box, anchorEl);
}
function hideHover() {
    clearTimeout(_hideTimer);
    if (_hoverPop) _hoverPop.classList.remove("show");
}
function scheduleHide() {
    clearTimeout(_hideTimer);
    _hideTimer = setTimeout(() => {
        if (_hoverPop) _hoverPop.classList.remove("show");
        cacherApercuHeros();
    }, 160);
}

/** Visuel en tête de fiche : une carte, ou les DEUX côte à côte.
 *
 *  Dans la fiche il y a la largeur qu'il n'y a pas sur la tuile : plutôt que de
 *  redécouper les deux cartes en diagonale, on les montre entières, en
 *  demi-largeur. La hauteur consommée reste celle d'une seule carte, donc la
 *  biographie et l'état civil gardent leur place — et le panneau tient toujours
 *  dans l'écran, comme réglé dans `.recap`. */
function visuelFiche(h) {
    const carteDe = (cardId, nom) =>
        el("img", { class: "hh-card", src: cardImageUrl(picIdHeros(cardId)), alt: nom || "" });
    if (!h.lie) return carteDe(h.heroCardId, h.name);
    return el("div", { class: "hh-duo" },
        carteDe(h.heroCardId, h.name),
        carteDe(h.lie.heroCardId, h.lie.name),
    );
}

/** Contenu de la fiche d'un héros : carte, nom, extension, bio, état civil.
 *  Servi soit dans la colonne de droite, soit dans l'infobulle. */
function ficheHeros(h) {
    const info = HEROS_INFO[h.heroCardId];
    const carte = visuelFiche(h);
    if (!info) return [carte];      // héros sans biographie rédigée : visuel seul

    // En anglais, on prefere la version *En quand elle existe.
    const en = langueActuelle() === "en";
    const champ = (fr, versionEn) => (en && versionEn) || fr;

    return [
        carte,
        el("div", { class: "hh-name mvl" }, nomAffiche(h)),
        el("div", { class: "hh-ext" }, (h.extension || "").replace(/^\d+\.\s*/, "")),
        el("p", { class: "hh-bio" }, champ(info.bio, info.bioEn)),
        info.civil ? detailRow(t("Identité civile"), champ(info.civil, info.civilEn)) : null,
        info.base ? detailRow(t("Base"), champ(info.base, info.baseEn)) : null,
        info.equipes ? detailRow(t("Équipes"), champ(info.equipes, info.equipesEn)) : null,
        info.ennemis ? detailRow(t("Ennemis"), champ(info.ennemis, info.ennemisEn)) : null,
        info.apparition ? detailRow(t("Première apparition"), info.apparition) : null,
    ];
}

/** La colonne de droite est-elle réellement à côté de la grille ?
 *  Sous 1180px le layout passe sur une seule colonne (voir prepare.css) : la
 *  fiche s'y afficherait hors écran, on garde alors l'infobulle. */
function colonneApercuDisponible() {
    return window.matchMedia("(min-width:1181px)").matches
        && !!document.getElementById("recap-apercu");
}

function showHeroHover(h, cardEl) {
    // Affichage préféré : dans la colonne de droite, à la place de la fiche de
    // mission. Rien ne recouvre la grille, et la place permet une carte plus
    // grande que dans l'infobulle.
    if (colonneApercuDisponible()) {
        clearTimeout(_hideTimer);
        const zone = document.getElementById("recap-apercu");
        zone.replaceChildren(...ficheHeros(h).filter(Boolean));
        const recap = zone.closest(".recap");
        if (recap) recap.classList.add("apercu");
        hideHover();                 // pas d'infobulle en plus
        return;
    }

    const box = hoverPop();
    const info = HEROS_INFO[h.heroCardId];
    box.classList.remove("trio");
    box.classList.toggle("bare", !info);
    box.classList.toggle("wide", !!info);
    box.replaceChildren(...ficheHeros(h).filter(Boolean));
    popShow(box, cardEl);
}

/** Rend la fiche de mission à la colonne de droite (fin du survol). */
function cacherApercuHeros() {
    const zone = document.getElementById("recap-apercu");
    const recap = zone && zone.closest(".recap");
    if (recap) recap.classList.remove("apercu");
}

function showScnHover(sc, tileEl) {
    const box = hoverPop();
    box.classList.remove("bare", "trio");
    const vcards = (sc.villainCards && sc.villainCards.length) ? sc.villainCards : [sc.tileImage].filter(Boolean);
    const multi = vcards.length > 1;
    box.classList.toggle("wide", multi);
    const cardsEl = multi
        ? el("div", { class: "hh-row" }, ...vcards.map((id) => el("img", { class: "hh-rowcard", src: cardImageUrl(id), alt: sc.name })))
        : el("img", { class: "hh-card", src: cardImageUrl(vcards[0] || sc.tileImage), alt: sc.name });
    box.replaceChildren(
        cardsEl,
        multi ? el("div", { class: "hh-rowhint" }, vcards.length + " " + t("méchants")) : null,
        el("div", { class: "hh-name mvl" }, sc.name),
        el("div", { class: "hh-ext" }, sc.extension.replace(/^\d+\.\s*/, "")),
        detailRow(t("Méchant(s)"), sc.villainNames.length ? sc.villainNames.join(", ") : t("Pas de méchant fixe")),
        multi ? detailRow(t("Nombre de méchants"), String(vcards.length)) : detailRow(t("Stades du méchant"), String(sc.villains.length || "-")),
        detailRow(t("Manigances"), String(sc.schemes.length)),
        detailRow(t("Sets requis"), sc.mandatoryEncounterSets.map(titleize).join(", ") || "-"),
        detailRow(t("Sets recommandés"), sc.recommendedModularSets.map(titleize).join(", ") || "-"),
        ...defiRows(sc),
        sc.hasExpertVariant ? el("div", { class: "sd-badge" }, t("Expert disponible")) : null,
    );
    popShow(box, tileEl);
}

/** Lignes « règle du défi » du panneau de survol d'un scénario-défi. */
function defiRows(sc) {
    if (!sc.challenges || !sc.challenges.length) return [];
    const info = DEFIS_INFO[sc.challenges[0]];
    if (!info) return [];
    // En anglais, on prefere la reformulation officielle (regleEn/contrainteEn).
    const en = langueActuelle() === "en";
    const regle = (en && info.regleEn) || info.regle;
    const contrainte = (en && info.contrainteEn) || info.contrainte;
    const lignes = [detailRow(t("Règle du défi"), regle)];
    if (contrainte) lignes.push(detailRow(t("Contrainte"), contrainte));
    return lignes;
}

function showExtHover(ext, tabEl) {
    const box = hoverPop();
    box.classList.remove("wide", "bare", "trio");
    if (ext.key === "defis") {
        box.replaceChildren(
            el("div", { class: "hh-name mvl" }, t("Défis")),
            el("div", { class: "hh-ext" }, t("Défis mensuels : scénario imposé + règle spéciale")),
            detailRow(t("Défis"), String(ext.scenarios.length)),
        );
        popShow(box, tabEl);
        return;
    }
    box.replaceChildren(
        el("img", { class: "hh-card", src: extensionImageUrl(ext.key), alt: ext.key }),
        el("div", { class: "hh-name mvl" }, ext.key.replace(/^\d+\.\s*/, "")),
        detailRow(t("Scénarios"), String(ext.scenarios.length)),
        detailRow(t("Héros"), String(ext.heroes.length)),
        detailRow(t("Sets de rencontre"), String(ext.encounters.length)),
    );
    popShow(box, tabEl);
}

/* ---- Arts alternatifs des ressources doubles (promos FFG) ----------------
   Purement cosmétique : la carte reste 01088/01089/01090 pour le moteur. Le
   choix se fait ICI (à l'assignation du deck), vaut pour les TROIS ressources
   d'un même héros, et est mémorisé par héros. Le plateau (ui-app) lit la même
   clé localStorage. Images : assets/pics/<card_id>_<code>.jpg */
const COLLECTIONS_RESSOURCES = [
    // « Standard » et « Aléatoire » en tête, tout le reste par ordre
    // alphabétique. Trois origines mélangées : rééditions d'extension
    // (vrais codes de carte), promos « Play-and-Share » de FFG, et
    // collections fan-made « DesignHacker ». Sinister Motives (27020-22)
    // est volontairement absent : visuel identique au jeu de base.
    { code: "standard", nom: "Standard", apercu: "01089" },
    { code: "random", nom: "Aléatoire", apercu: null },
    { code: "dh_adamwarlock", nom: "Adam Warlock", apercu: "01089_dh_adamwarlock" },
    { code: "shield", nom: "Agents of SHIELD", apercu: "50026" },
    { code: "am", nom: "Ant-Man", apercu: "01089_am" },
    { code: "bp", nom: "Black Panther", apercu: "01089_bp" },
    { code: "bw", nom: "Black Widow", apercu: "01089_bw" },
    { code: "ca", nom: "Captain America", apercu: "01089_ca" },
    { code: "cm", nom: "Captain Marvel", apercu: "01089_cm" },
    { code: "civilwar", nom: "Civil War", apercu: "56021" },
    { code: "ds", nom: "Doctor Strange", apercu: "01089_ds" },
    { code: "dh_drax", nom: "Drax", apercu: "01089_dh_drax" },
    { code: "dh_gamora", nom: "Gamora", apercu: "01089_dh_gamora" },
    { code: "dh_ghostspider", nom: "Ghost-Spider", apercu: "01089_dh_ghostspider" },
    { code: "dh_groot", nom: "Groot", apercu: "01089_dh_groot" },
    { code: "hk", nom: "Hawkeye", apercu: "01089_hk" },
    { code: "hu", nom: "Hulk", apercu: "01089_hu" },
    { code: "im", nom: "Iron Man", apercu: "01089_im" },
    { code: "ekaug_jj", nom: "Jessica Jones", apercu: "01089_ekaug_jj" },
    { code: "dh_miles", nom: "Miles Morales", apercu: "01089_dh_miles" },
    { code: "mm", nom: "Ms. Marvel", apercu: "01089_mm" },
    { code: "mutant", nom: "Mutant Genesis", apercu: "32023" },
    { code: "dh_nebula", nom: "Nebula", apercu: "01089_dh_nebula" },
    { code: "dh_quicksilver", nom: "Quicksilver", apercu: "01089_dh_quicksilver" },
    { code: "dh_rocket", nom: "Rocket", apercu: "01089_dh_rocket" },
    { code: "dh_scarletwitch", nom: "Scarlet Witch", apercu: "01089_dh_scarletwitch" },
    { code: "sh", nom: "She-Hulk", apercu: "01089_sh" },
    { code: "dh_spectrum", nom: "Spectrum", apercu: "01089_dh_spectrum" },
    { code: "sm", nom: "Spider-Man", apercu: "01089_sm" },
    { code: "sw", nom: "Spider-Woman", apercu: "01089_sw" },
    { code: "dh_starlord", nom: "Star-Lord", apercu: "01089_dh_starlord" },
    { code: "th", nom: "Thor", apercu: "01089_th" },
    { code: "dh_valkyrie", nom: "Valkyrie", apercu: "01089_dh_valkyrie" },
    { code: "dh_venom", nom: "Venom", apercu: "01089_dh_venom" },
    { code: "dh_vision", nom: "Vision", apercu: "01089_dh_vision" },
    { code: "dh_warmachine", nom: "War Machine", apercu: "01089_dh_warmachine" },
    { code: "wa", nom: "Wasp", apercu: "01089_wa" },
];

/* ---- Arts alternatifs des CARTES DE HEROS ------------------------------
   Planche « Alternate Art Hero Cards » de M3T4LB0X (hallofheroeslcg.com).
   Purement cosmétique : la carte reste la même pour le moteur.
   N'ont été retenus que les arts dont les VALEURS IMPRIMÉES sont identiques à
   notre carte ; un art affichant d'autres chiffres mentirait en pleine partie.
   Doit rester aligné avec ui-app/src/board/variantes.ts (ARTS_HEROS). */
const ARTS_HEROS = {
    "01001a": [{ code: "m3t", nom: "M3T4LB0X" }],
    "01010a": [{ code: "m3t", nom: "M3T4LB0X" }],
    "01019a": [{ code: "m3t", nom: "M3T4LB0X" }],
    "01029a": [{ code: "m3t", nom: "M3T4LB0X" }],
    "03001a": [{ code: "m3t", nom: "M3T4LB0X" }],
    "04001a": [{ code: "m3t", nom: "M3T4LB0X" }],
};

/** Identifiant d'image de la carte de héros, art alternatif choisi compris. */
function picIdHeros(heroCardId) {
    const base = String(heroCardId || "").split(",")[0];
    const arts = ARTS_HEROS[base];
    if (!arts || !arts.length) return base;
    const choix = prefs.heroArt(heroCardId);
    return arts.some((a) => a.code === choix) ? `${base}_${choix}` : base;
}

function blocArtHeros(hero) {
    const arts = ARTS_HEROS[String(hero.heroCardId || "").split(",")[0]];
    if (!arts || !arts.length) return null;      // rien a proposer : pas de bloc
    const choixActuel = prefs.heroArt(hero.heroCardId);
    const zone = el("div", { class: "res-art" },
        el("div", { class: "ra-tete" },
            el("span", { class: "ra-titre" }, t("Carte de héros")),
            el("span", { class: "ra-sous" }, t("Art alternatif — mêmes valeurs de jeu")),
        ),
    );
    const choix = el("div", { class: "ra-choix" });
    [{ code: "standard", nom: "Standard", apercu: hero.heroCardId }]
        .concat(arts.map((a) => ({ code: a.code, nom: a.nom, apercu: `${hero.heroCardId}_${a.code}` })))
        .forEach((c) => {
            const bouton = el("button", {
                class: "ra-option" + (c.code === choixActuel ? " sel" : ""),
                title: t(c.nom),
                onmouseenter: (e) => showCardHover(c.apercu, e.currentTarget),
                onmouseleave: scheduleHide,
                onclick: () => {
                    prefs.setHeroArt(hero.heroCardId, c.code);
                    [...choix.children].forEach((b) => b.classList.remove("sel"));
                    bouton.classList.add("sel");
                },
            });
            bouton.append(el("img", { class: "ra-vignette", src: cardImageUrl(c.apercu), loading: "lazy", alt: "" }));
            bouton.append(el("span", {}, t(c.nom)));
            choix.append(bouton);
        });
    zone.append(choix);
    return zone;
}

/** Sélecteur d'identité : certains héros existent en plusieurs versions au
 *  texte identique mais aux TRAITS différents (The Thing Avenger ou Guardian).
 *  Contrairement au bloc « art alternatif » ci-dessus, ce choix change les
 *  valeurs de jeu : il part dans le deck envoyé au moteur. */
function blocIdentiteHeros(p, i) {
    const variantes = (p.hero && p.hero.variants) || [];
    if (variantes.length < 2) return null;      // cas courant : aucun sélecteur

    const actuel = identiteChoisie(p);
    const zone = el("div", { class: "res-art" },
        el("div", { class: "ra-tete" },
            el("span", { class: "ra-titre" }, t("Identité")),
            el("span", { class: "ra-sous" }, t("Mêmes capacités — le trait du héros change")),
        ),
    );
    const choix = el("div", { class: "ra-choix" });
    variantes.forEach((v) => {
        const bouton = el("button", {
            class: "ra-option" + (v.heroCardId === actuel.heroCardId ? " sel" : ""),
            title: v.name,
            onmouseenter: (e) => showCardHover(v.heroCardId, e.currentTarget),
            onmouseleave: scheduleHide,
            onclick: () => { p.identity = v; render(); },
        });
        bouton.append(el("img", { class: "ra-vignette", src: cardImageUrl(v.heroCardId), loading: "lazy", alt: "" }));
        // Le libellé montre ce qui distingue vraiment cette version.
        bouton.append(el("span", {}, (v.distinctif && v.distinctif[0]) || v.name));
        choix.append(bouton);
    });
    zone.append(choix);
    return zone;
}

/** Identité retenue pour un joueur : son choix, sinon la version de base. */
function identiteChoisie(p) {
    const variantes = (p.hero && p.hero.variants) || [];
    if (!variantes.length) return { heroCardId: p.hero && p.hero.heroCardId, hero: p.deck && p.deck.hero };
    return variantes.find((v) => p.identity && v.heroCardId === p.identity.heroCardId) || variantes[0];
}

/** Les trois ressources d'une collection, déduites de son aperçu (Genius). */
function tripletRessources(apercu) {
    const m = String(apercu || "").match(/^(\d{5})(_.+)?$/);
    if (!m) return apercu ? [apercu] : [];
    const n = parseInt(m[1], 10), suffixe = m[2] || "";
    const pad = (v) => String(v).padStart(5, "0");
    return [pad(n - 1) + suffixe, pad(n) + suffixe, pad(n + 1) + suffixe];
}

/** Agrandissement d'une collection : les TROIS cartes côte à côte. */
function showTrioHover(apercu, anchorEl) {
    const ids = tripletRessources(apercu);
    if (!ids.length) return;
    const box = hoverPop();
    box.classList.remove("wide", "trio");
    box.classList.add("bare", "trio");
    box.replaceChildren(el("div", { class: "hh-trio" },
        ...ids.map((id) => el("img", { class: "hh-card", src: cardImageUrl(id), alt: "" }))));
    popShow(box, anchorEl);
}

/** Nom réduit à sa substance : sans accents, sans ponctuation, sans casse.
 *  « Ms. Marvel » et « ms marvel » doivent se rejoindre, mais « Spider-Man »
 *  et « Spider-Woman » doivent rester distincts — d'où une égalité stricte
 *  après réduction, jamais une correspondance partielle. */
function _cleRessource(nom) {
    return String(nom || "")
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .toLowerCase().replace(/[^a-z0-9]/g, "");
}

/** La collection de ressources qui porte le nom de ce héros, s'il en existe une. */
function collectionDuHeros(nomHeros) {
    const cle = _cleRessource(nomHeros);
    if (!cle) return null;
    const trouvee = COLLECTIONS_RESSOURCES.find((c) => _cleRessource(c.nom) === cle);
    return trouvee ? trouvee.code : null;
}

function blocRessources(hero) {
    // Défaut : la collection au nom du héros. « Standard » ne s'impose plus que
    // pour les héros qui n'en ont pas — ou si le joueur l'a explicitement remis.
    const choixActuel = prefs.resourceArt(hero.heroCardId, collectionDuHeros(hero.name));
    const zone = el("div", { class: "res-art" },
        el("div", { class: "ra-tete" },
            el("span", { class: "ra-titre" }, t("Cartes ressources doubles")),
            el("span", { class: "ra-sous" }, t("Energy · Genius · Strength — même collection")),
        ),
    );
    const choix = el("div", { class: "ra-choix" });
    COLLECTIONS_RESSOURCES.forEach((c) => {
        const bouton = el("button", {
            class: "ra-option" + (c.code === choixActuel ? " sel" : ""),
            title: t(c.nom),
            // « Aléatoire » n'a pas d'aperçu : rien à agrandir.
            onmouseenter: c.apercu ? (e) => showTrioHover(c.apercu, e.currentTarget) : undefined,
            onmouseleave: c.apercu ? scheduleHide : undefined,
            onclick: () => {
                prefs.setResourceArt(hero.heroCardId, c.code);
                [...choix.children].forEach((b) => b.classList.remove("sel"));
                bouton.classList.add("sel");
            },
        });
        if (!c.apercu) {
            bouton.append(el("div", { class: "ra-vignette ra-hasard" }, "?"));
        } else {
            bouton.append(el("img", { class: "ra-vignette", src: cardImageUrl(c.apercu), loading: "lazy", alt: "" }));
        }
        bouton.append(el("span", {}, t(c.nom)));
        choix.append(bouton);
    });
    zone.append(choix);
    return zone;
}

/* ---- Import marvelcdb ---- */
function mcdbExtractId(input) {
    const s = String(input || "").trim();
    const um = s.match(/(?:decklist|deck)\/(?:view\/)?(\d+)/);
    if (um) return um[1];
    const m = s.match(/(\d{3,})/);
    return m ? m[1] : "";
}
async function mcdbFetch(id) {
    const urls = [
        `https://marvelcdb.com/api/public/decklist/${id}.json`,
        `https://marvelcdb.com/api/public/deck/${id}.json`,
    ];
    for (const u of urls) {
        try { const r = await fetch(u); if (r.ok) return await r.json(); } catch (e) {}
    }
    throw new Error(t("Deck introuvable sur marvelcdb") + " (ID " + id + "). " + t("Vérifie que le deck est public."));
}
async function importMarvelcdb(slotIndex, input) {
    const id = mcdbExtractId(input);
    if (!id) throw new Error(t("URL/ID marvelcdb invalide."));
    const data = await mcdbFetch(id);
    await cards.load();
    // marvelcdb renvoie le heros sous "hero_code" (Marvel Champions), pas
    // "investigator_code" (qui est le champ d'Arkham Horror et reste null ici).
    // Sans ce champ, aucun heros ne matchait -> "hero not available".
    const inv = String(data.hero_code || data.investigator_code || "").split(",")[0];
    const invBase = inv.replace(/[a-z]$/, "");
    const heroes = await catalog.heroes();
    const memeHero = (code) => {
        const c = String(code || "").split(",")[0];
        return c === inv || c.replace(/[a-z]$/, "") === invBase;
    };
    const hero = heroes.find((h) => memeHero(h.heroCardId))
        || heroes.find((h) => memeHero((h.deck.hero || [])[0]));
    if (!hero) throw new Error(t("Le héros de ce deck n’est pas disponible dans le jeu."));
    // La règle de conversion vit dans public/js/marvelcdb/conversion.js : le
    // panneau de recherche et ce champ « coller un lien » doivent produire
    // EXACTEMENT le même deck, sinon un deck jouable ici serait refusé là.
    const deck = versDeckMoteur(
        { id, nom: data.name || hero.name, cartes: data.slots || {} },
        hero.deck,
        (cid) => { const c = cards.get(cid); return (c && c.class) || ""; },
    );
    return { hero, deck };
}

/* ---- Visionneuse : cartes d'un deck ---- */
function showCardHover(id, anchorEl) {
    const box = hoverPop();
    box.classList.remove("wide", "trio");
    box.classList.add("bare");
    box.replaceChildren(el("img", { class: "hh-card", src: cardImageUrl(id), alt: "" }));
    popShow(box, anchorEl);
}
function showDeckCards(deck) {
    const ids = [...(deck.hero || []).flatMap((x) => String(x).split(",")), ...(deck.hero_deck || []), ...(deck.player_deck || [])];
    const counts = {};
    for (const id of ids) counts[id] = (counts[id] || 0) + 1;
    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) { hideHover(); overlay.remove(); } } },
        el("div", { class: "deck-modal-panel" },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, deck.name || "Deck"),
                el("span", { class: "dm-sub" }, ids.length + " " + t("cartes")),
                el("button", { class: "dm-close", onclick: () => { hideHover(); overlay.remove(); } }, "✕"),
            ),
            el("div", { class: "dm-grid" }, ...Object.keys(counts).map((id) =>
                el("div", { class: "dm-card" },
                    el("img", { src: cardImageUrl(id), loading: "lazy", onmouseenter: (e) => showCardHover(id, e.currentTarget), onmouseleave: scheduleHide }),
                    counts[id] > 1 ? el("span", { class: "dm-count" }, "x" + counts[id]) : null,
                ))),
        ));
    document.body.append(overlay);
}

/* ---- Panneau : parcourir les decks MarvelCDB indexés ---- */
// L'index est produit hors ligne par tools/marvelcdb_index.py. Aucune requête
// vers marvelcdb ici : tout est local, cartes comprises.
async function ouvrirPanneauCdb(i) {
    const p = state.players[i];
    if (!p || !p.hero) return;
    await cards.load();
    const paquet = await chargerHeros(p.hero.heroCardId);
    const criteres = { aspect: "", tag: "", texte: "", masquerIncomplets: true };
    let favoris = lireFavoris();

    const liste = el("div", { class: "cdb-liste" });
    const compte = el("span", { class: "dm-sub" });

    const ligne = (d) => {
        const marque = favoris.includes(String(d.id));
        const etoile = el("button", {
            class: "cdb-etoile" + (marque ? " on" : ""),
            title: t("Mettre de côté"),
            onclick: (e) => { e.stopPropagation(); favoris = basculerFavori(d.id); rendre(); },
        }, marque ? "★" : "☆");

        const choisir = () => {
            if (!d.jouable) {
                alert(t("Ce deck utilise des cartes absentes du jeu :") + "\n" +
                      d.cartes_absentes.join(", "));
                return;
            }
            const deck = versDeckMoteur(d, p.hero.deck,
                (cid) => { const c = cards.get(cid); return (c && c.class) || ""; });
            if (ecartDeConversion(d, deck) !== 0) {
                alert(t("Ce deck n’a pas pu être converti proprement, il n’est pas proposé."));
                return;
            }
            p.deck = deck; p.deckSource = "imported"; p.deckAuto = false;
            overlay.remove();
            render();
        };

        return el("div", { class: "cdb-ligne" + (d.jouable ? "" : " incomplet"), onclick: choisir },
            etoile,
            el("div", { class: "cdb-nom" },
                el("b", {}, d.nom),
                el("span", { class: "cdb-date" }, d.date)),
            el("div", { class: "do-tags" },
                d.aspect ? el("span", { class: "tag asp", style: { background: ASPECTS[d.aspect] || "#555" } }, d.aspect) : null,
                ...(d.tags || []).map((tg) => el("span", { class: "tag" }, tg)),
                d.jouable ? null : el("span", { class: "tag manque" },
                    `${d.cartes_absentes.length} ${t("cartes manquantes")}`)),
        );
    };

    const rendre = () => {
        const retenus = filtrer(paquet.decks, criteres);
        // Les favoris remontent en tête, l'ordre chronologique tient le reste.
        retenus.sort((a, b) => favoris.includes(String(b.id)) - favoris.includes(String(a.id)));
        compte.textContent = `${retenus.length} ${t("decks")}`;
        if (!retenus.length) {
            liste.replaceChildren(el("div", { class: "cdb-vide" },
                paquet.decks.length
                    ? t("Aucun deck ne correspond à ces filtres.")
                    : t("Aucun deck indexé pour ce héros. Lance tools/marvelcdb_index.py.")));
            return;
        }
        liste.replaceChildren(...retenus.map(ligne));
    };

    const opt = (v, libelle) => el("option", { value: v }, libelle);

    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) overlay.remove(); } },
        el("div", { class: "deck-modal-panel" },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, `${t("Decks MarvelCDB")} — ${p.hero.name}`),
                compte,
                el("button", { class: "dm-close", onclick: () => overlay.remove() }, "✕"),
            ),
            el("div", { class: "cdb-filtres" },
                el("input", {
                    class: "mcdb-input", placeholder: t("Chercher par nom..."),
                    oninput: (e) => { criteres.texte = e.target.value; rendre(); },
                }),
                el("select", { onchange: (e) => { criteres.aspect = e.target.value; rendre(); } },
                    opt("", t("Tous les aspects")),
                    ...aspectsPresents(paquet.decks).map((a) => opt(a, a))),
                el("select", { onchange: (e) => { criteres.tag = e.target.value; rendre(); } },
                    opt("", t("Tous les tags")),
                    ...tagsPresents(paquet.decks).map((tg) => opt(tg, tg))),
                el("label", { class: "cdb-tout" },
                    el("input", {
                        type: "checkbox",
                        onchange: (e) => { criteres.masquerIncomplets = !e.target.checked; rendre(); },
                    }),
                    t("Montrer les decks incomplets")),
            ),
            liste,
        ));

    rendre();
    document.body.append(overlay);
}

function stepDecks() {
    const wrap = el("section", { class: "step decks-step" },
        stepHead("Briefing 02", "Arsenal", t("Decks assignés")),
    );
    for (let i = 0; i < state.playerCount; i++) {
        const p = state.players[i];
        // Siege d'invite en multi : son occupant choisit depuis le salon. On
        // montre son choix, on ne le modifie pas ; et tant qu'il n'a rien
        // choisi on dit qu'on l'attend, au lieu de sauter la ligne en silence.
        if (enLigne() && i > 0) {
            wrap.append(p.duSalon && p.hero
                ? el("div", { class: "deck-block cut salon-choix" },
                    el("div", { class: "db-head" },
                        portrait(p.hero.heroCardId, "mini"),
                        el("div", {},
                            el("b", { class: "mvl" }, `${t("Joueur")} ${i + 1} — ${p.hero.name}`),
                            el("span", {}, `${p.deck ? p.deck.name : ""} ✓`)),
                    ),
                    el("div", { class: "salon-note" }, t("Choisi par le joueur depuis son écran")))
                : el("div", { class: "deck-block cut salon-attente" },
                    el("b", { class: "mvl" }, `${t("Joueur")} ${i + 1}`),
                    el("span", {}, t("en attente de son choix…"))));
            continue;
        }
        if (!p.hero) continue;
        const idt = identiteChoisie(p);
        const block = el("div", { class: "deck-block cut" },
            el("div", { class: "db-head" },
                portrait(idt.heroCardId || p.hero.heroCardId, "mini"),
                el("div", {}, el("b", { class: "mvl" }, p.hero.name), el("span", {}, t("Deck prêt"))),
            ),
            blocIdentiteHeros(p, i),
            el("div", { class: "db-list", id: "db-" + i }, el("div", { class: "loading" }, t("Chargement des decks..."))),
            el("div", { class: "deck-import" },
                el("input", { class: "mcdb-input", id: "mcdb-" + i, placeholder: t("Colle une URL ou un ID marvelcdb...") }),
                el("button", { class: "btn-ghost", onclick: () => doImport(i) }, "Import"),
                el("button", {
                    class: "btn-ghost",
                    title: t("Parcourir les decks publiés sur MarvelCDB"),
                    onclick: () => ouvrirPanneauCdb(i),
                }, t("Decks MarvelCDB")),
                el("button", {
                    class: "btn-ghost",
                    title: t("Construire un deck personnalisé pour ce héros"),
                    onclick: () => { window.open("/deck-builder.html?hero=" + encodeURIComponent(p.hero.id), "_blank"); },
                }, t("Éditeur de deck")),
                el("span", { class: "mcdb-status", id: "mcdb-st-" + i }),
            ),
            blocArtHeros(p.hero),
            blocRessources(p.hero),
        );
        wrap.append(block);
        loadDecks(i);
    }
    return wrap;
}

async function doImport(i) {
    const input = document.getElementById("mcdb-" + i);
    const status = document.getElementById("mcdb-st-" + i);
    if (!input || !input.value.trim()) return;
    if (status) status.textContent = t("Import en cours...");
    try {
        const { hero, deck } = await importMarvelcdb(i, input.value);
        const p = state.players[i];
        p.hero = hero; p.deck = deck; p.deckSource = "imported"; p.deckAuto = false;
        if (window.confirm(`Deck \u00ab ${deck.name} \u00bb ${t("importé")} (${deck.player_deck.length} ${t("cartes")}).\n\n${t("Le sauvegarder pour plus tard ?")}`)) {
            prefs.saveDeck(deck);
        }
        render();
    } catch (e) {
        if (status) status.textContent = "";
        alert(t("Échec de l’import :") + " " + e.message);
    }
}

/** Joueurs dont les paquets d'aspect sont dépliés. Voir loadDecks(). */
const aspectsDeplies = new Set();

async function loadDecks(i) {
    const p = state.players[i];
    await cards.load();
    const catDecks = await catalog.decksForHero(p.hero);
    const saved = prefs.savedDecksForHero(p.hero.heroCardId).map((d, idx) => ({
        id: "saved-" + idx, name: d.name || t("Deck importé"), source: "saved", deck: d,
        aspects: [...new Set((d.player_deck || []).map((id) => cards.aspectOf(id)).filter((a) => a && a !== "basic"))],
    }));
    const decks = [...catDecks, ...saved];
    // Le deck deja joue par cette equipe n'est dans aucune de ces listes : ni
    // deck de base, ni deck sauvegarde, ni package d'aspect. Il lui faut sa
    // propre entree, sinon il serait le seul choix qu'un clic de curiosite
    // ferait perdre pour de bon.
    const deCampagne = DECKS_CAMPAGNE.get(i);
    if (deCampagne && String((deCampagne.hero || [])[0] || "").split(",")[0] === p.hero.heroCardId) {
        decks.unshift({
            id: "campagne", name: t("Deck actuel de la campagne"), source: "campagne", deck: deCampagne,
            aspects: [...new Set((deCampagne.player_deck || []).map((id) => cards.aspectOf(id)).filter((a) => a && a !== "basic"))],
        });
    }
    // Mémoire des choix : si le deck actuel a été posé automatiquement à
    // l'assignation du héros, on présélectionne le dernier deck utilisé pour
    // ce héros, s'il est encore disponible (base ou sauvegardé).
    if (p.deckAuto) {
        p.deckAuto = false;
        const dernierId = prefs.lastDeckFor(p.hero.heroCardId);
        const dk = dernierId != null ? decks.find((d) => d.id === dernierId) : null;
        if (dk && dk.deck !== p.deck) {
            p.deck = dk.deck;
            p.deckSource = dk.source;
            render();
            return;
        }
    }
    const box = document.getElementById("db-" + i);
    if (!box) return;

    const option = (dk) => {
        const on = p.deckSource === dk.source && p.deck && p.deck.name === dk.deck.name;
        const st = deckStats(dk.deck);
        // Contrôle de construction : signalé, jamais bloquant.
        const ecarts = verifierDeck(dk.deck);
        const etiquette = dk.source === "base" ? "Base"
            : dk.source === "aspect" ? t("Conseillé")
            : dk.source === "campagne" ? t("En cours")
            : t("Sauvegardé");
        return el("button", {
            class: "deck-opt cut" + (on ? " sel" : ""),
            onclick: () => {
                p.deck = dk.deck; p.deckSource = dk.source; p.deckAuto = false;
                // « campagne » n'existe que sur cet ecran-ci : le retenir comme
                // dernier deck du heros ne designerait plus rien demain.
                if (dk.source !== "campagne") prefs.setLastDeck(p.hero.heroCardId, dk.id);
                render();
            },
        },
            el("div", { class: "do-name" }, dk.name),
            el("div", { class: "do-tags" },
                el("span", { class: "tag" }, etiquette),
                ...dk.aspects.map((a) => el("span", { class: "tag asp", style: { background: ASPECTS[a] || "#555" } }, a)),
            ),
            aspectBar(st),
            el("div", { class: "do-foot" },
                el("span", { class: "do-size" }, st.total + " " + t("cartes")),
                ...(ecarts.length
                    ? [el("span", {
                        class: "do-alerte",
                        title: ecarts.join(" · "),
                      }, "⚠ " + t("Hors règles"))]
                    : []),
                el("span", { class: "do-view", onclick: (e) => { e.stopPropagation(); e.preventDefault(); showDeckCards(dk.deck); } }, t("Voir les cartes")),
            ),
        );
    };

    // Les paquets d'aspect conseillés sont repliés. Ils sont utiles, mais à
    // quatre ils enterraient le deck de base et les decks sauvegardés — ceux
    // qu'on vient chercher neuf fois sur dix.
    //
    // Le pli est mémorisé PAR JOUEUR dans un état de module : loadDecks() est
    // rappelé à chaque render(), donc à chaque clic sur un deck. Un simple
    // booléen local se refermerait sous les doigts.
    const principaux = decks.filter((dk) => dk.source !== "aspect");
    const aspects = decks.filter((dk) => dk.source === "aspect");
    const enfants = principaux.map(option);

    if (aspects.length) {
        const deplie = aspectsDeplies.has(i);
        const liste = el("div", { class: "deck-aspects" + (deplie ? " est-deplie" : "") },
            ...aspects.map(option));
        const bascule = el("button", {
            type: "button",
            class: "deck-aspects-bascule" + (deplie ? " est-deplie" : ""),
            "aria-expanded": deplie ? "true" : "false",
        }, `${t("Paquets d’aspect conseillés")} (${aspects.length})`);
        bascule.addEventListener("click", () => {
            const ouvert = !aspectsDeplies.has(i);
            if (ouvert) aspectsDeplies.add(i); else aspectsDeplies.delete(i);
            liste.classList.toggle("est-deplie", ouvert);
            bascule.classList.toggle("est-deplie", ouvert);
            bascule.setAttribute("aria-expanded", ouvert ? "true" : "false");
        });
        enfants.push(bascule, liste);
    }

    box.replaceChildren(...enfants);
}
/* ---- Contrôle de construction (Rules Reference 1.8, Appendice I) ---------
   L'écran ne vérifiait rien, d'où les 37 cartes de Spider-Woman passées
   inaperçues. On avertit sans jamais bloquer : un deck hors clous reste
   jouable, mais on le voit. */
const DECK_MIN = 40;
const DECK_MAX = 50;
const EXEMPLAIRES_MAX = 3;

/** Toutes les cartes du deck : signature ET aspect. */
function _cartesDuDeck(deck) {
    return [...(deck.hero_deck || []), ...(deck.player_deck || [])];
}

/** Une carte permanente ne compte pas dans la taille du deck. */
function _estPermanente(id) {
    const c = cards.get(id);
    return !!(c && c.desc && c.desc.Permanent);
}

/** Le nom sert de titre : deux exemplaires d'une carte partagent leur nom. */
function _titre(id) {
    const c = cards.get(id);
    return (c && c.name) || id;
}

/** Une carte unique porte un astérisque en tête de nom. */
function _estUnique(id) {
    return String(_titre(id)).startsWith("*");
}

/** Plafond d'exemplaires : 3, ou moins si la carte l'impose elle-même. */
function _plafond(id) {
    if (_estUnique(id)) return 1;
    const c = cards.get(id);
    const max = c && c.desc && c.desc.MaxPerDeck;
    const n = parseInt(max, 10);
    return Number.isFinite(n) ? n : EXEMPLAIRES_MAX;
}

/** Les écarts d'un deck aux règles de construction. Liste vide = conforme. */
function verifierDeck(deck) {
    const ecarts = [];
    const toutes = _cartesDuDeck(deck);
    const comptees = toutes.filter((id) => !_estPermanente(id));

    if (comptees.length < DECK_MIN) {
        ecarts.push(`${comptees.length} ${t("cartes")} — ${t("minimum")} ${DECK_MIN}`);
    } else if (comptees.length > DECK_MAX) {
        ecarts.push(`${comptees.length} ${t("cartes")} — ${t("maximum")} ${DECK_MAX}`);
    }

    // La limite d'exemplaires ne vaut QUE pour la partie personnalisable. Le
    // deck signature est imposé par le héros, en quantités fixes qui dépassent
    // parfois trois — Black Panther a cinq « Wakanda Forever! ». Sans cette
    // distinction, le contrôle accusait les decks officiels du jeu.
    const personnalisable = deck.player_deck || [];
    const parTitre = new Map();
    for (const id of personnalisable) {
        const cle = _titre(id);
        parTitre.set(cle, (parTitre.get(cle) || 0) + 1);
    }
    for (const [titre, nombre] of parTitre) {
        const id = personnalisable.find((x) => _titre(x) === titre);
        const max = _plafond(id);
        if (nombre > max) {
            const propre = String(titre).replace(/^\*\s*/, "");
            ecarts.push(`${propre} ×${nombre} — ${t("maximum")} ${max}`);
        }
    }
    return ecarts;
}

function deckStats(deck) {
    const asp = {};
    for (const id of (deck.player_deck || [])) {
        const a = cards.aspectOf(id) || "basic";
        asp[a] = (asp[a] || 0) + 1;
    }
    return { asp, total: (deck.player_deck || []).length };
}
function aspectBar(st) {
    const order = ["aggression", "justice", "leadership", "protection", "basic", "pool"];
    const segs = order
        .filter((a) => st.asp[a])
        .map((a) => el("span", { class: "seg", style: { background: ASPECTS[a], flex: st.asp[a] }, title: a + " : " + st.asp[a] }));
    return el("div", { class: "aspect-bar" }, ...segs);
}

function stepScenario() {
    const wrap = el("section", { class: "step scenario-step" },
        stepHead("Briefing 03", t("Identifie la cible"), t("Scénario et adversaire")),
    );
    wrap.append(targetBanner());
    wrap.append(
        el("div", { class: "ext-tabs", id: "ext-tabs" }, el("div", { class: "loading" }, "...")),
        el("div", { class: "scn-grid full", id: "scn-grid" }),
    );
    loadExtTabs();
    return wrap;
}

function targetBanner() {
    const sc = state.scenario;
    const style = sc && sc.tileImage ? { backgroundImage: `url("${cardImageUrl(sc.tileImage)}")` } : {};
    return el("div", { class: "target-banner cut" },
        el("div", { class: "target-art", style }),
        el("div", { class: "target-copy" },
            el("span", { class: "target-k" }, t("Cible actuelle")),
            el("strong", { class: "mvl" }, sc ? sc.name : t("Cible non définie")),
            el("span", {}, sc && sc.villainNames.length ? sc.villainNames.join(", ") : t("Aucun scénario verrouillé")),
        ),
    );
}

/** Mémoire des choix : hors campagne, si aucune cible n'est choisie, resélectionne
    le dernier scénario joué (et recale l'onglet d'extension, y compris « Défis »).
    Renvoie true si une sélection a été appliquée (il faut alors re-rendre). */
async function preselectionDernierScenario() {
    if (state.scenario || isCampaignMode()) return false;
    const dernier = prefs.lastScenario();
    if (!dernier) return false;
    const exts = await catalog.extensions();
    const ext = exts.find((x) => (x.scenarios || []).includes(dernier));
    if (!ext) return false;
    const scs = await catalog.scenariosForExtension(ext.key);
    const sc = scs.find((s) => s.id === dernier);
    if (!sc) return false;
    state.extensionTab = ext.key;
    selectScenario(sc);
    return true;
}

async function loadExtTabs() {
    if (await preselectionDernierScenario()) { render(); return; }
    const exts = (await catalog.extensions()).filter((e) => e.scenarios.length);
    // Si l'onglet courant n'existe plus dans la liste, on le recale.
    const validKeys = new Set(exts.map((e) => e.key));
    if (!state.extensionTab || !validKeys.has(state.extensionTab)) {
        state.extensionTab = exts[0] ? exts[0].key : null;
    }
    const tabs = document.getElementById("ext-tabs");
    if (!tabs) return;
    tabs.replaceChildren(...exts.map((e) => el("button", {
        class: "ext-tab cut" + (state.extensionTab === e.key ? " on" : ""),
        title: e.key,
        onclick: () => { hideHover(); state.extensionTab = e.key; loadExtTabs(); loadScnGrid(); },
        onmouseenter: (ev) => showExtHover(e, ev.currentTarget),
        onmouseleave: scheduleHide,
    },
        e.key === "defis"
            ? el("div", { class: "box box-defis" }, "\u{1F3C6}")
            : el("div", { class: "box", style: { backgroundImage: `url("${extensionImageUrl(e.key)}")` } }),
        el("span", { class: "exname" }, e.key === "defis" ? t("Défis") : e.key.replace(/^\d+\.\s*/, "")),
    )));
    loadScnGrid();
}

async function loadScnGrid() {
    let grid = document.getElementById("scn-grid");
    if (!grid) return;
    grid.replaceChildren(el("div", { class: "loading" }, t("Chargement des scénarios...")));
    const scs = await catalog.scenariosForExtension(state.extensionTab);
    grid = document.getElementById("scn-grid");
    if (!grid) return;
    grid.replaceChildren(...scs.map((sc) => {
        const on = state.scenario && state.scenario.id === sc.id;
        return el("button", {
            class: "scn-tile cut" + (on ? " sel" : ""),
            onclick: () => { selectScenario(sc); render(); },
            onmouseenter: (e) => showScnHover(sc, e.currentTarget),
            onmouseleave: scheduleHide,
        },
            el("div", { class: "st-illus", style: { backgroundImage: `url("${cardImageUrl(sc.tileImage)}")` } }),
            el("div", { class: "st-name mvl" }, sc.name),
            el("div", { class: "st-meta" }, sc.villainNames.slice(0, 2).join(", ") || t("Scénario")),
            (sc.challenges && sc.challenges.length) ? el("span", { class: "st-exp" }, t("DÉFI")) : null,
            sc.hasExpertVariant ? el("span", { class: "st-exp" }, "EXPERT") : null,
        );
    }));
}



function detailRow(k, v) {
    return el("div", { class: "detail-row" },
        el("span", { class: "dr-k" }, k),
        el("span", { class: "dr-v" }, v),
    );
}

function stepDifficulty() {
    const wrap = el("section", { class: "step difficulty-step" },
        stepHead("Briefing 04", t("Niveau de menace"), t("Règles et sets modulaires")),
    );
    if (!state.scenario) {
        wrap.append(el("p", { class: "muted" }, t("Sélectionne un scénario.")));
        return wrap;
    }
    const d = state.difficulty;
    wrap.append(el("div", { class: "presets" },
        preset("standard", "Standard", t("Expérience standard."), d.base === "standard" && !d.skirmish && !d.heroic),
        state.scenario.hasExpertVariant ? preset("expert", "Expert", t("Méchant expert + set expert."), d.base === "expert") : null,
        toggleCard("skirmish", "Skirmish", t("Partie plus courte."), d.skirmish),
        heroicCard(d.heroic),
    ));
    wrap.append(el("div", { class: "cfg-head" }, t("Sets modulaires") + " - " + (state.scenario.modularSlots.min || 0) + " " + t("recommandés")));
    wrap.append(el("div", { class: "cfg-modes" },
        cfgBtn("recommended", t("Recommandés")),
        cfgBtn("custom", t("Personnalisés")),
        cfgBtn("random", t("Aléatoire")),
    ));
    wrap.append(el("div", { class: "modular-box", id: "modular-box" }));
    renderModular();
    return wrap;
}
function preset(id, title, desc, on) {
    return el("button", {
        class: "preset cut" + (on ? " on" : ""),
        onclick: () => { state.difficulty.base = id; render(); },
    }, el("div", { class: "p-title mvl" }, title), el("div", { class: "p-desc" }, desc));
}
function toggleCard(key, title, desc, on) {
    return el("button", {
        class: "preset cut" + (on ? " on" : ""),
        onclick: () => { state.difficulty[key] = !state.difficulty[key]; render(); },
    }, el("div", { class: "p-title mvl" }, title), el("div", { class: "p-desc" }, desc));
}
function heroicCard(level) {
    return el("div", { class: "preset heroic cut" + (level > 0 ? " on" : "") },
        el("div", { class: "p-title mvl" }, t("Héroïque") + " " + (level > 0 ? level : "")),
        el("input", {
            type: "range",
            min: "0",
            max: "8",
            value: String(level),
            oninput: (e) => {
                state.difficulty.heroic = +e.target.value;
                document.querySelectorAll(".preset.heroic .p-title").forEach((n) => {
                    n.textContent = t("Héroïque") + " " + (e.target.value > 0 ? e.target.value : "");
                });
            },
        }),
    );
}
function cfgBtn(id, label) {
    return el("button", {
        class: "cfg-btn" + (state.difficulty.modularConfig === id ? " on" : ""),
        onclick: () => { state.difficulty.modularConfig = id; applyModularConfig(); render(); },
    }, label);
}
async function renderModular() {
    await Promise.resolve();
    const box = document.getElementById("modular-box");
    if (!box) return;
    const d = state.difficulty;
    if (d.modularConfig === "recommended") {
        box.replaceChildren(el("div", { class: "mod-chips" },
            ...state.scenario.recommendedModularSets.map((s) => el("span", { class: "mod-chip on" }, titleize(s))),
            state.scenario.recommendedModularSets.length === 0 ? el("span", { class: "muted" }, t("Aucun set modulaire recommandé.")) : null,
        ));
    } else if (d.modularConfig === "random") {
        box.replaceChildren(el("div", { class: "mod-chips" }, ...d.selectedModularSets.map((s) => el("span", { class: "mod-chip on" }, titleize(s)))));
    } else {
        box.replaceChildren(el("div", { class: "loading" }, t("Chargement des sets modulaires...")));
        const all = (await catalog.encounterSets()).filter((s) => s.kind === "modular");
        const sel = new Set(d.selectedModularSets);
        box.replaceChildren(el("div", { class: "mod-chips" }, ...all.map((s) =>
            el("span", {
                class: "mod-chip" + (sel.has(s.name) ? " on" : ""),
                onclick: (e) => {
                    sel.has(s.name) ? sel.delete(s.name) : sel.add(s.name);
                    d.selectedModularSets = [...sel];
                    e.target.classList.toggle("on");
                },
            }, s.displayName))));
    }
}

function stepSummary() {
    const wrap = el("section", { class: "step summary-step" },
        stepHead("Briefing 05", t("Face à face"), t("Prêt au combat")),
    );
    const v = validate(state);
    const sc = state.scenario;
    const heroCards = el("div", { class: "fo-cards" });
    for (let i = 0; i < state.playerCount; i++) {
        const p = state.players[i];
        heroCards.append(p.hero
            ? el("div", { class: "fo-card" },
                el("img", {
                    src: cardImageUrl(picIdHeros(p.hero.heroCardId)),
                    alt: p.hero.name,
                    onmouseenter: (e) => showCardHover(picIdHeros(p.hero.heroCardId), e.currentTarget),
                    onmouseleave: scheduleHide,
                }),
                el("div", { class: "fo-cap mvl" }, p.hero.name, el("span", {}, p.deckSource === "base" ? t("Deck de base") : (p.deck ? p.deck.name : ""))),
            )
            : el("div", { class: "fo-empty" }, t("Joueur") + " " + (i + 1)));
    }
    const villCards = el("div", { class: "fo-cards villain-cards" });
    const vc = sc ? ((sc.villainCards && sc.villainCards.length) ? sc.villainCards : [sc.tileImage].filter(Boolean)) : [];
    (vc.length ? vc : [null]).forEach((id) => villCards.append(id
        ? el("div", { class: "fo-card villain" }, el("img", { src: cardImageUrl(id), alt: sc.name }))
        : el("div", { class: "fo-empty" }, "-")));
    wrap.append(el("div", { class: "faceoff" },
        el("div", { class: "fo-side heroes-side" }, el("div", { class: "fo-label heroes mvl" }, t("Héros")), heroCards),
        el("div", { class: "fo-vs mvl" }, "VS"),
        el("div", { class: "fo-side villain-side" },
            el("div", { class: "fo-label villain mvl" }, t("Méchant")),
            villCards,
            sc ? el("div", { class: "fo-vname mvl" }, sc.name) : null,
            sc ? el("div", { class: "fo-vsub" }, sc.villainNames.join(", ") || t("Scénario")) : null,
        ),
    ));
    if (sc) {
        const d = state.difficulty;
        const tags = [libelleMode(state.mode) + " - " + state.playerCount + "p", d.base === "expert" ? "Expert" : "Standard"];
        if (d.skirmish) tags.push("Skirmish");
        if (d.heroic > 0) tags.push(t("Héroïque") + " " + d.heroic);
        wrap.append(el("div", { class: "sum-meta" },
            ...tags.map((t) => el("span", { class: "meta-pill" }, t)),
            el("span", { class: "meta-pill" }, t("Sets :") + " " + [...sc.mandatoryEncounterSets, ...d.selectedModularSets].map(titleize).join(", ")),
        ));
    }
    if (!v.ok) {
        wrap.append(el("div", { class: "errors" },
            el("h3", { class: "mvl" }, t("À compléter")),
            ...v.errors.map((e) => el("div", { class: "err", onclick: () => goto(e.step) }, e.message + " >")),
        ));
    } else {
        wrap.append(el("div", { class: "ready mvl" }, t("Tout est prêt")));
    }
    wrap.append(blocAvance());
    return wrap;
}

/* ---- Bloc « Avancé » : seed, temps par décision, premier joueur, règles ----
   Replié par défaut : sans y toucher, le descripteur reste identique à avant
   (seed -1, timeout 0, v16_all présent, ordre des joueurs inchangé). Les
   contrôles écrivent directement dans state, sans re-render (le <details>
   resterait sinon fermé à chaque frappe). */
function blocAvance() {
    if (state.premierJoueur >= state.playerCount) state.premierJoueur = 0;
    const ligne = (titre, controle, note) => el("div", { class: "av-field" },
        el("div", { class: "av-label" }, titre),
        controle,
        note ? el("div", { class: "av-note" }, note) : null,
    );

    const seedInput = el("input", {
        class: "cj-int av-seed", type: "number", min: "1", step: "1",
        placeholder: t("Vide = aléatoire"),
        value: state.seed == null ? "" : String(state.seed),
        oninput: (e) => {
            const n = parseInt(e.target.value, 10);
            state.seed = Number.isFinite(n) ? n : null;
        },
    });
    const btnCopier = el("button", {
        class: "chip av-btn",
        title: t("Copier la seed"),
        onclick: () => {
            const v = seedInput.value.trim();
            if (!v || !navigator.clipboard) return; // fallback silencieux
            navigator.clipboard.writeText(v).then(() => {
                btnCopier.textContent = t("Copié");
                setTimeout(() => { btnCopier.textContent = t("Copier"); }, 1200);
            }).catch(() => {});
        },
    }, t("Copier"));
    const seedRow = el("div", { class: "av-row" },
        seedInput,
        el("button", {
            class: "chip av-btn",
            title: t("Générer une seed aléatoire"),
            onclick: () => {
                state.seed = 1 + Math.floor(Math.random() * 2147483647); // 1..2^31
                seedInput.value = String(state.seed);
            },
        }, "\u{1F3B2}"),
        btnCopier,
    );

    const timeoutInput = el("input", {
        class: "cj-int", type: "number", min: "0", step: "1",
        value: String(state.timeoutSecondes > 0 ? state.timeoutSecondes : 0),
        oninput: (e) => {
            const n = parseInt(e.target.value, 10);
            state.timeoutSecondes = Number.isFinite(n) && n > 0 ? n : 0;
        },
    });

    let lignePremierJoueur = null;
    if (state.playerCount > 1) {
        // En multi, le siege N est une PERSONNE. buildDescriptor fait tourner
        // l'ordre des joueurs pour appliquer ce reglage : chacun se retrouverait
        // avec le deck de son voisin. On le grise plutot que de le retirer :
        // en hot-seat local il reste utile et sans danger.
        const sel = el("select", {
            class: "cj-sel",
            disabled: enLigne() ? "" : undefined,
            onchange: (e) => { state.premierJoueur = +e.target.value || 0; },
        }, ...activePlayers().map((p, i) => el("option", {
            value: String(i),
            selected: state.premierJoueur === i || undefined,
        }, p.hero ? p.hero.name : t("Joueur") + " " + (i + 1))));
        lignePremierJoueur = ligne(
            t("Premier joueur"),
            sel,
            enLigne()
                ? t("En multi, c’est toujours le Joueur 1 qui commence : les sièges restent attachés aux personnes.")
                : t("En ligne, l'ordre des sièges suit ce choix"));
    }

    const v16 = el("label", { class: "cj-chk" },
        el("input", {
            type: "checkbox",
            checked: state.reglesV16 !== false || undefined,
            onchange: (e) => { state.reglesV16 = e.target.checked; },
        }),
        el("span", {}, t("Activées (recommandé)")));

    return el("details", { class: "camp-journal avance" },
        el("summary", {}, t("Avancé")),
        el("div", { class: "cj-body" },
            ligne(t("Seed"), seedRow, t("Même seed + mêmes choix = même partie")),
            ligne(t("Temps par décision (secondes)"), timeoutInput, t("0 = illimité")),
            lignePremierJoueur,
            ligne(t("Règles v16"), v16, null),
        ),
    );
}

(async () => {
    // Revenir a la preparation desarme toujours le coach du mode Decouverte :
    // c'est le seul point de passage commun aux quatre facons de rejoindre le
    // plateau (lancement normal, puzzle, reprise, salon multi), dont trois
    // n'arment jamais rien. Un lancement en mode Decouverte le rearmera juste
    // avant de rediriger (launcher.js). Le coach survit donc a un F5 sur le
    // plateau, mais jamais a un retour ici.
    appliquerTutoriel(window.localStorage, null);
    synchroniserLangueServeur();
    if (creationCampagne()) {
        state.mode = MODES.find((m) => m.id === "campaign") || state.mode;
        state.playerCount = Math.max(1, Math.min(4, BROUILLON_CAMPAGNE.nbJoueurs | 0)) || 1;
        state.difficulty.base = BROUILLON_CAMPAGNE.difficulte === "expert" ? "expert" : "standard";
    }
    try {
        await cards.load();
        const exts = await catalog.extensions();
        state.extensionTab = (exts.find((e) => e.scenarios.length) || exts[0] || {}).key || null;
    } catch (e) {
        console.error("prepare init:", e);
    }
    // Apres cards.load() : la reprise interroge le catalogue des heros.
    try {
        await reprendreEquipeCampagne();
    } catch (e) {
        console.error("reprise equipe campagne:", e);
    }
    render();
    // Le salon ne concerne que le multi, mais on sonde toujours : la reponse
    // dit elle-meme si on y est (multi:false en solo, et tout reste inerte).
    await sonderSalon();
    setInterval(sonderSalon, 2000);
})();
