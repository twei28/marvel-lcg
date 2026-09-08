// app.js - Assistant "Preparer une partie" : briefing Marvel Champions.
"use strict";
import { cardImageUrl, cardImageUrlEn, cardImageUrlHd, extensionImageUrl, oublierDecksSauvegardes } from "/public/js/prepare/api.js?v=564d4a13";
import { cards } from "/public/js/prepare/cards.js";
import { catalog, titleize, titreDeVague } from "/public/js/prepare/catalog.js";
import { validate } from "/public/js/prepare/validation.js";
import { launch } from "/public/js/prepare/launcher.js?v=62115d60";
import { prefs } from "/public/js/prepare/prefs.js";
// Panneau « Documents ». Importe ICI plutot que pose en balise dans
// prepare.html : deux URL differentes (avec et sans ?v=) chargeraient le
// module deux fois et poseraient deux boutons dans l'en-tete.
import { livretDExtension, carnetDExtension } from "/public/js/prepare/panneau-documents.js";
import { boutonLangue, synchroniserLangueServeur, t, langueActuelle } from "/public/js/prepare/langue.js";
import { DEFIS_INFO } from "/public/js/prepare/defis-info.js";
import { HEROS_INFO } from "/public/js/prepare/heros-info.js";
import { GENRES, nouveautesTriees } from "/public/js/prepare/nouveautes.js";
import { MECHANTS_INFO } from "/public/js/prepare/mechants-info.js";
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

/** `replaceChildren` transforme un null en TEXTE « null » (contrairement à
 *  el(), qui l'ignore). Tout ce qui peut être absent passe par ici. */
function poser(hote, ...enfants) {
    hote.replaceChildren(...enfants.flat().filter((x) => x != null && x !== false));
}

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

/** Un picto Font Awesome (public/css/font-awesome.css), à la place d'un émoji. */
function picto(nom) {
    return el("i", { class: "fa " + nom, "aria-hidden": "true" });
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
    // Bataille : le mode competitif de Civil War et Synthezoid Smackdown. Deux
    // equipes s'affrontent, chacune face au leader prepare par l'autre. Le
    // livret (mc56 p.14) n'en connait que deux formats, 1v1 et 2v2 : d'ou 2 ou
    // 4 joueurs, et le camp deduit du siege plutot que demande.
    { id: "bataille", label: t("Bataille"), desc: t("2 équipes, 1v1 ou 2v2"), players: 2, min: 2, max: 4, mark: "B" },
    // Decouverte : partie FIGEE (Spider-Man / Rhino / seed 42) doublee d'un
    // coach qui donne une mission a la fois. Les lecons NOMMENT des cartes
    // precises, d'ou le seed impose : voir tools/test_seed_tutoriel.py.
];
// QUATRE étapes, plus cinq : le niveau de menace et les sets modulaires se
// choisissent sur l'écran de la cible, sous la grille des scénarios. C'est là
// qu'on décide de la difficulté, en voyant le méchant.
const STEPS = (creationCampagne() ? ["Équipe", "Decks"] : ["Équipe", "Decks", "Méchant", "Final"])
    .map((s) => t(s));
const LAST_STEP = STEPS.length - 1;
const rnd = (arr) => arr[Math.floor(Math.random() * arr.length)];

const isCampaignMode = () => state.mode && state.mode.id === "campaign";

const playerLogKey = (field, i) => field.perPlayer ? ("Player " + (i + 1) + " " + field.key) : field.key;

/** `url` : la fonction qui donne l'image (par défaut celle de la langue ; la
 *  scène du héros passe `cardImageUrlEn` pour éviter le filigrane FR). */
function portrait(cardId, cls, url = cardImageUrl) {
    return el("div", {
        class: "portrait " + (cls || ""),
        style: cardId ? { backgroundImage: `url(${url(cardId)})` } : {},
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
function portraitDuo(hero, cls, url = cardImageUrl) {
    return el("div", { class: "portrait-duo " + (cls || "") },
        portrait(hero.heroCardId, "duo duo-a", url),
        portrait(hero.lie.heroCardId, "duo duo-b", url),
    );
}

/** Les cartes des méchants d'un scénario (une par méchant, vide sans méchant fixe). */
function mechantsDe(sc) {
    return (sc && sc.villainCards) || [];
}

/** Portrait d'un scénario : l'image de sa tuile s'il n'a qu'un méchant, sinon
 *  la vignette PARTAGÉE entre ses méchants (deux moitiés, quatre quarts), pour
 *  qu'on voie d'un coup d'oeil que c'est un scénario à plusieurs (Wrecking
 *  Crew). Demande de l'utilisateur, 7 septembre 2026. */
function portraitScenario(sc, cls) {
    const ids = mechantsDe(sc);
    if (ids.length < 2) {
        return el("div", { class: "portrait " + (cls || ""), style: { backgroundImage: `url("${cardImageUrl(sc.tileImage)}")` } });
    }
    const n = Math.min(ids.length, 4);
    return el("div", { class: `portrait portrait-multi n${n} ` + (cls || "") },
        ...ids.slice(0, 4).map((id) => el("i", { style: { backgroundImage: `url("${cardImageUrl(id)}")` } })));
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
    // L'ACCUEIL (refonte du 7 septembre) : avant l'étape 1, un écran qui ne
    // demande qu'une chose, comment on joue. Le choix du mode quittait ainsi
    // l'écran des héros, où il prenait une rangée entière. Faux en création
    // d'équipe de campagne : le mode y est déjà décidé.
    accueil: !creationCampagne(),
    step: 0,
    mode: MODES[0],
    playerCount: 1,
    players: [0, 1, 2, 3].map((i) => ({ index: i, hero: null, deck: null, deckSource: null })),
    activeSlot: 0,
    // homebrew : decoche = uniquement les heros officiels, coche = uniquement
    // les fan-made (Stan Lee, Hulk (Rainy), Thor (Jane Foster)).
    heroFilters: { q: "", vague: "", fav: false, homebrew: false },
    scenario: null,
    // Bataille : le scenario pose devant la SECONDE equipe. Chaque equipe
    // affronte celui apporte par l'autre (mc56 p.14, etape 4).
    scenario2: null,
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
/** Vrai en mode Bataille (competitif, deux equipes). */
function estBataille() { return !!state.mode && state.mode.id === "bataille"; }

/** Le camp d'un siege : premiere moitie contre seconde moitie.
 *  Le livret ne connait que le 1v1 et le 2v2, donc le camp se deduit du siege
 *  et n'a pas a etre demande. */
function campDuSiege(index, total) { return index < Math.ceil(total / 2) ? 0 : 1; }

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
        case 2: return !!state.scenario && (!estBataille() || !!state.scenario2);
        case 3: return validate(state).ok;
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
    state.accueil = false;
    state.step = step;
    render();
}
const next = () => { if (canContinue()) goto(state.step + 1); };
const prev = () => {
    if (state.step === 0 && !creationCampagne()) { hideHover(); state.accueil = true; render(); return; }
    goto(state.step - 1);
};

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

// Decks deja relus apres un echec : evite de rejouer la lecture a chaque
// sondage pour un deck qui, lui, n'existe vraiment pas.
const decksRelus = new Set();

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
        let decks = await catalog.decksForHero(hero);
        let dk = decks.find((d) => d.id === choix.deck_id);
        if (!dk && !decksRelus.has(choix.deck_id)) {
            // Deck inconnu : l'invite vient peut-etre de l'importer depuis
            // MarvelCDB, et notre liste date d'avant. On la relit UNE fois par
            // deck — sans ce garde-fou, un deck reellement absent declencherait
            // une requete a chaque sondage, toutes les deux secondes.
            decksRelus.add(choix.deck_id);
            oublierDecksSauvegardes();
            decks = await catalog.decksForHero(hero);
            dk = decks.find((d) => d.id === choix.deck_id);
        }
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
    if (state.accueil) {
        // Pas d'en-tête sur l'accueil : logo, langue et onglets d'étapes n'y
        // disent rien, la page EST le titre. Les outils annexes (Reprendre,
        // Stats, Documents, Signaler un bug) gardent leur rangée flottante en
        // haut à droite, posée par leurs scripts quand l'en-tête est absent.
        document.title = t("Préparation de mission") + " — Marvel Champions";
        const rangee = document.querySelector(".reprise-boutons");
        if (rangee && !rangee.classList.contains("est-flottante")) {
            rangee.classList.add("est-flottante");
            document.body.append(rangee);
        }
        root.replaceChildren(
            el("div", { class: "layout accueil-layout" },
                el("main", { class: "stage accueil-stage" }, accueilView()),
            ),
        );
    } else {
        // Les quatre étapes prennent tout l'écran (direction « Affiche ») : la
        // moitié gauche est la scène, la droite ce qu'on choisit. La colonne
        // « fiche de mission » n'a plus lieu d'être : la scène et la rangée du
        // bas disent déjà où l'on en est.
        root.replaceChildren(
            progressBar(),
            el("div", { class: "layout accueil-layout" },
                el("main", { class: "stage stage-affiche" }, stepView()),
            ),
            navBar(),
        );
    }
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
            ),
        ),
        boutonLangue("btn ghost btn-langue"),
        el("div", { class: "steps" }, STEPS.map((label, i) => {
            const done = i < state.step && stepComplete(i);
            const cls = "pstep" + (i === state.step && !state.accueil ? " active" : "") + (done ? " done" : "");
            // Sans numero devant (demande de l'utilisateur) : la coche seule
            // marque une etape faite, rien ne marque les autres.
            return el("button", { class: cls, onclick: () => goto(i) },
                done ? el("span", { class: "pnum" }, "\u2713") : null,
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
    const showRandom = [0, 2].includes(state.step);
    return el("footer", { class: "nav" },
        el("button", { class: "btn ghost", disabled: (state.step === 0 && creationCampagne()) || undefined, onclick: prev }, t("Retour")),
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
    const sc = state.scenario ? state.scenario.name : t("Méchant inconnu");
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

function stepView() {
    switch (state.step) {
        case 0: return stepTeam();
        case 1: return stepDecks();
        case 2: return stepScenario();
        case 3: return stepSummary();
    }
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
    // DEUX TUILES, pas une qui se renomme.
    //
    // « Coop locale » et « Coop en ligne » sont deux facons de jouer, et on doit
    // pouvoir passer de l'une a l'autre d'un clic. La version precedente
    // n'affichait qu'une tuile dont le nom changeait selon un reglage pose plus
    // bas : il fallait avoir compris ce reglage pour savoir ou l'on etait.
    //
    // Cote MOTEUR il n'y a toujours qu'un mode, `hotseat` : les deux tuiles
    // designent le meme, et ne different que par `coopEnLigne`. Ajouter un vrai
    // mode obligerait a le porter dans le lanceur, la validation et le
    // recapitulatif, pour ne rien changer a la partie jouee.
    const tuiles = [];
    for (const m of MODES) {
        if (m.id === "hotseat" && state.salon.multi) {
            tuiles.push({ mode: m, distant: false, mark: m.mark,
                          libelle: m.label, detail: m.desc });
            tuiles.push({ mode: m, distant: true, mark: "@",
                          libelle: t("Coop en ligne"),
                          detail: t("2 à 4 héros, chacun choisit le sien") });
            continue;
        }
        tuiles.push({ mode: m, distant: null, mark: m.mark,
                      libelle: m.label, detail: m.desc });
    }
    for (const tuile of tuiles) {
        const m = tuile.mode;
        // Une tuile de coop n'est allumee que si le mode ET la destination
        // concordent : sans le second test, les deux s'allumeraient ensemble.
        const on = state.mode.id === m.id
            && (tuile.distant === null || (state.coopEnLigne !== false) === tuile.distant);
        const libelle = tuile.libelle;
        const detail = tuile.detail;
        strip.append(el("button", {
            class: "mode-pill" + (on ? " sel" : ""),
            onclick: () => {
                if (tuile.distant !== null) state.coopEnLigne = tuile.distant;
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
            el("span", { class: "mode-mark mvl" }, tuile.mark),
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
/**
 * Sous la bande des modes : de quoi convoquer les invites.
 *
 * L'ancienne bascule « Chacun sur son appareil / Tous sur cet ecran » a
 * disparu : elle disait la meme chose que les deux tuiles « Coop locale » et
 * « Coop en ligne », qui se choisissent maintenant directement.
 *
 * Ne reste donc ici que les liens, et seulement quand quelqu'un est attendu a
 * l'autre bout : les proposer en coop locale serait faux.
 */
function choixCoop() {
    if (!state.salon.multi || state.mode.id !== "hotseat") return null;
    if (state.coopEnLigne === false) return null;
    return el("div", { class: "coop-zone" }, blocLiens());
}

/* ---------------- Liens d'invitation ---------------- */

// Les cles de siege, une fois demandees au moteur. `null` tant que l'hote n'a
// rien demande : on ne va pas chercher des cles dont personne n'a besoin.
const liensInvites = { cles: null, erreur: "", copie: -1 };

/**
 * L'adresse a envoyer a l'invite du siege `p`.
 *
 * `location.origin` plutot qu'une adresse fabriquee par le moteur : le moteur
 * ignore tout du domaine public place devant lui (`p3.exemple.com`), la ou le
 * navigateur de l'hote le connait exactement. `to=salon` envoie l'invite
 * choisir son heros et son deck, pas directement au plateau.
 */
function lienDuSiege(p) {
    const cle = (liensInvites.cles || [])[p] || "";
    return location.origin + "/claim_seat?p=" + p
        + "&key=" + encodeURIComponent(cle) + "&to=salon";
}

async function genererLiens() {
    liensInvites.erreur = "";
    try {
        const res = await fetch("get_liens_sieges?");
        const brut = await res.json();
        // ⚠ `res.ok` NE SUFFIT PAS : le moteur repond 403 avec un corps JSON
        // quand le client ne tient pas le siege 0. Sans ce test, `cles` serait
        // `undefined` et chaque lien sortirait avec `key=`, c'est-a-dire
        // ouvert a qui devine l'adresse.
        if (!res.ok || !brut.multi || !Array.isArray(brut.cles)) {
            throw new Error(brut.error || "indisponible");
        }
        liensInvites.cles = brut.cles;
    } catch (e) {
        liensInvites.erreur = t("Impossible de récupérer les liens.");
    }
    render();
}

function blocLiens() {
    // A un seul heros il n'y a personne a inviter : le bouton mentirait.
    if (state.playerCount < 2) return null;

    if (!liensInvites.cles) {
        return el("div", { class: "liens-invites" },
            el("button", { class: "liens-bouton", onclick: genererLiens },
                t("Générer les liens à envoyer")),
            liensInvites.erreur
                ? el("small", { class: "liens-erreur" }, liensInvites.erreur)
                : null,
        );
    }

    const bloc = el("div", { class: "liens-invites ouvert" });
    // Un lien par siege d'INVITE, et le nombre suit celui des heros choisis :
    // le siege 0 est celui de l'hote, deja devant son ecran.
    for (let p = 1; p < state.playerCount; p += 1) {
        const url = lienDuSiege(p);
        bloc.append(el("div", { class: "liens-ligne" },
            el("span", { class: "liens-qui" }, t("Joueur") + " " + (p + 1)),
            el("input", {
                class: "liens-url", readonly: true, value: url,
                onclick: (ev) => ev.target.select(),
            }),
            el("button", {
                class: "liens-copier" + (liensInvites.copie === p ? " ok" : ""),
                onclick: async () => {
                    try {
                        await navigator.clipboard.writeText(url);
                        liensInvites.copie = p;
                    } catch (e) {
                        // Presse-papier refuse (page non securisee, permission) :
                        // le champ reste selectionnable a la main.
                        liensInvites.copie = -1;
                    }
                    render();
                },
            }, liensInvites.copie === p ? t("Copié") : t("Copier")),
        ));
    }
    bloc.append(el("small", { class: "liens-aide" },
        t("Un lien par personne, à envoyer. Chacun choisit son héros et son deck depuis le sien.")));
    return bloc;
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

/**
 * L'écran d'accueil : le titre, et une seule question, comment on joue.
 *
 * Une tuile par mode. Les modes à plusieurs (coop locale, coop en ligne,
 * bataille) portent leurs nombres de héros à même la tuile : choisir « 3 »
 * choisit le mode ET le nombre, en un clic. Solo et bac à sable partent au
 * clic sur la tuile. Campagne renvoie à son propre écran, comme avant.
 */
function accueilView() {
    const tuiles = [];
    for (const m of MODES) {
        if (m.id === "hotseat" && state.salon.multi) {
            tuiles.push({ mode: m, distant: false, mark: m.mark, libelle: m.label, detail: m.desc });
            tuiles.push({ mode: m, distant: true, mark: "@", libelle: t("Coop en ligne"),
                          detail: t("2 à 4 héros, chacun choisit le sien") });
            continue;
        }
        tuiles.push({ mode: m, distant: null, mark: m.mark, libelle: m.label, detail: m.desc });
    }

    const partir = (tuile, nombre) => {
        const m = tuile.mode;
        if (tuile.distant !== null) state.coopEnLigne = tuile.distant;
        if (m.id === "campaign") { window.location.href = "/campagne.html"; return; }
        const wasCampaign = isCampaignMode();
        state.mode = m;
        if ((m.id === "campaign") !== wasCampaign) state.scenario = null;
        state.playerCount = m.fixed ? 1
            : Math.max(m.min || 1, Math.min(m.max || 4, nombre || state.playerCount));
        if (state.activeSlot >= state.playerCount) state.activeSlot = state.playerCount - 1;
        goto(0);
    };

    const grille = el("div", { class: "acc-modes" });
    for (const tuile of tuiles) {
        const m = tuile.mode;
        const nombres = [];
        if (!m.fixed && m.id !== "campaign") {
            for (let n = (m.min || 1); n <= (m.max || 4); n++) {
                if (m.id === "bataille" && n % 2 !== 0) continue;
                nombres.push(el("button", {
                    class: "acc-nombre",
                    title: n + " " + t("héros"),
                    onclick: (e) => { e.stopPropagation(); partir(tuile, n); },
                }, m.id === "bataille" ? (n / 2) + "v" + (n / 2) : String(n)));
            }
        }
        // Pas de lettre ni de chiffre devant le nom : sur une grande tuile, le
        // nom se suffit.
        grille.append(el("button", {
            class: "acc-mode cut" + (nombres.length ? " avec-nombres" : ""),
            onclick: () => partir(tuile, null),
        },
            el("span", { class: "acc-copy" },
                el("b", { class: "mvl" }, tuile.libelle),
                el("small", {}, tuile.detail),
            ),
            nombres.length ? el("span", { class: "acc-nombres" },
                el("small", {}, t("héros")), ...nombres) : null,
        ));
    }

    return el("section", { class: "step accueil" },
        el("div", { class: "acc-titre" },
            el("div", { class: "recitatif" }, t("Préparation de mission")),
            el("h1", { class: "affiche" }, "Marvel", el("br"), "Champions"),
            el("p", {}, t("Comment veux-tu jouer ?")),
        ),
        grille,
        blocNouveautes(),
    );
}

/* ---- Le bloc « Nouveautés » de l'accueil (8 septembre 2026) ---------------
   Sous les tuiles de mode, les trois dernières lignes du journal, le reste
   replié sous « Tout voir ». Le contenu vit dans `nouveautes.js`, écrit pour
   les joueurs ; ici il n'y a que la mise en page.

   ⚠ PAS D'ÉTAT NI DE RE-RENDU. Le dépliage passe par un `<details>` natif,
   comme la biographie du roster : rien à retenir, rien à resynchroniser, et
   le clavier l'ouvre tout seul. */

/** Combien de lignes restent visibles sans rien déplier. */
const NOUVEAUTES_EN_TETE = 3;

/** « 8 sept. 2026 » / « 8 Sep 2026 », dans la langue de l'écran.
 *
 *  ⚠ ON NE PASSE PAS PAR `new Date("2026-09-08")` : cette forme est lue comme
 *  minuit UTC, et sous un fuseau en retard elle affiche la veille. On
 *  reconstruit la date à partir de ses morceaux, en heure locale. */
function dateCourteNouveaute(iso) {
    const [an, mois, jour] = String(iso).split("-").map(Number);
    if (!an || !mois || !jour) return String(iso);
    const quand = new Date(an, mois - 1, jour);
    const locale = langueActuelle() === "en" ? "en-GB" : "fr-FR";
    return quand.toLocaleDateString(locale, { day: "numeric", month: "short", year: "numeric" });
}

function ligneNouveaute(entree) {
    const anglais = langueActuelle() === "en";
    const genre = GENRES[entree.genre];
    return el("li", {},
        el("span", { class: "acc-nouv-date" }, dateCourteNouveaute(entree.date)),
        el("span", { class: "acc-nouv-genre " + entree.genre },
           anglais ? genre.en : genre.fr),
        el("span", { class: "acc-nouv-texte" }, anglais ? entree.en : entree.fr),
    );
}

function blocNouveautes() {
    const toutes = nouveautesTriees();
    if (!toutes.length) return null;
    const enTete = toutes.slice(0, NOUVEAUTES_EN_TETE);
    const reste = toutes.slice(NOUVEAUTES_EN_TETE);
    return el("section", { class: "acc-nouv" },
        el("h2", {}, t("Nouveautés")),
        el("ul", { class: "acc-nouv-liste" }, enTete.map(ligneNouveaute)),
        reste.length ? el("details", { class: "acc-nouv-plus" },
            el("summary", {}, t("Tout voir")),
            el("ul", { class: "acc-nouv-liste" }, reste.map(ligneNouveaute)),
        ) : null,
    );
}

function playerCountRow() {
    if (state.mode.fixed) return null;
    // Le nombre de héros d'une campagne est arrêté à sa création : le changer
    // ici produirait une équipe que la campagne refuserait ensuite.
    if (creationCampagne()) return null;
    const row = el("div", { class: "count-row" }, el("span", { class: "lbl" }, t("Joueurs")));
    for (let n = (state.mode.min || 1); n <= (state.mode.max || 4); n++) {
        // 1v1 ou 2v2, jamais 3 : le livret ne prevoit pas d'equipes inegales.
        if (estBataille() && n % 2 !== 0) continue;
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

/* ---- Étape 1, direction « Affiche » (7 septembre) --------------------------
   La moitié gauche est le héros EN SCÈNE : son art plein cadre, son nom en
   italique géant, ses chiffres en tampons. La droite est le roster : un mur
   de portraits carrés, tous visibles, et l'équipe en bas. Survoler un portrait
   le met en scène ; cliquer le recrute, avec le geste de la carte qui surgit
   (l'emprunt à la direction « Vitrine ») et son onomatopée. */

/** Le cri de chaque héros, par identifiant de deck : sa réplique fétiche
 *  quand il en a une (« Flame on ! », « Sweet Christmas ! »), sinon le bruit
 *  de son pouvoir tel que les comics l'écrivent (SNIKT, BAMF, THWIP).
 *  Repli : « BAM ! ». Liste du 7 septembre 2026, à corriger librement. */
const ONOMATOPEES = {
    /* --- officiels --- */
    adam_warlock: "SOUL GEM !", angel: "WHOOSH !", ant_man: "ZOOM !", bishop: "BZZT !",
    black_panther: "WAKANDA FOREVER !", black_panther_shuri: "WAKANDA FOREVER !",
    black_widow: "WIDOW'S BITE !", cable: "BODYSLIDE BY ONE !", captain_america: "AVENGERS, ASSEMBLE !",
    captain_marvel: "HIGHER, FURTHER, FASTER, MORE !", colossus: "KLANG !", cyclops: "ZRAKK !",
    daredevil: "THE MAN WITHOUT FEAR !", deadpool: "CHIMICHANGA !", doctor_strange: "BY THE VISHANTI !",
    domino: "BANG !", drax: "DESTROY !", echo: "WHAM !", falcon: "ON YOUR LEFT !",
    gambit: "MON AMI !", gamora: "DEADLIEST WOMAN !", ghost_spider: "THWIP !", groot: "I AM GROOT !",
    hawkeye: "TWANG !", hercules: "HAVE AT THEE !", hulk: "HULK SMASH !", hulkling: "EXCELSIOR !",
    iceman: "CHILL !", iron_man: "I AM IRON MAN !", ironheart: "FWOOSH !", jessica_jones: "CRACK !",
    jubilee: "PAF !", luke_cage: "SWEET CHRISTMAS !", magik: "SHING !", magneto: "MASTER OF MAGNETISM !",
    maria_hill: "COPY THAT !", ms_marvel: "EMBIGGEN !", nebula: "ZAP !", nick_fury: "WAH-HOOO !",
    nightcrawler: "BAMF !", nova: "BLUE BLAZES !", phoenix: "I AM PHOENIX !", psylocke: "PSYCHIC KNIFE !",
    quicksilver: "ZIP !", rocket_raccoon: "BLAM !", rogue: "SUGAH !", scarlet_witch: "HEX !",
    shadowcat: "PHASE !", she_hulk: "SMASH !", silk: "THWIP !", sp_dr: "BZZT !", spectrum: "FLASH !",
    spider_ham: "OINK !", spider_man: "THWIP !", spider_man_miles_morales: "VENOM BLAST !",
    spider_woman: "VENOM BLAST !", star_lord: "PEW PEW !", storm: "KRAKOOM !", thor: "I SAY THEE NAY !",
    tigra: "RAWR !", valkyrie: "FOR VALHALLA !", venom: "WE ARE VENOM !", vision: "I AM UNIQUE !",
    war_machine: "BRATATAT !", wasp: "WASP STING !", winter_soldier: "BLAM !", wolverine: "SNIKT !",
    wonder_man: "WHAM !", x_23: "SNIKT !",
    /* --- fan-made --- */
    agatha_harkness: "HEX !", agent_13: "BLAM !", agent_anti_venom: "WE ARE VENOM !", albert: "SNIKT !",
    alligator_loki: "CHOMP !", angela: "NOTHING FOR NOTHING !", armored_spidey: "THWIP !",
    beast: "STARS AND GARTERS !", beta_ray_bill: "FOR ASGARD !", black_cat: "BAD LUCK !",
    blink: "BLINK !", brawn: "SMASH !", cloak_dagger: "FLASH !", dazzler: "SPARKLE !",
    doctor_doom: "DOOM !", doctor_druid: "MASTER OF THE UNKNOWN !", harry_osborn: "HA HA HA !", gwenpool: "GWEN !",
    kate_bishop: "TWANG !", howard_the_duck: "WAUGH !", hulk_rainy: "SMASH !", human_torch: "FLAME ON !",
    invisible_woman: "FORCE FIELD !", iron_lad: "PEW !", iron_man_model_42: "I AM IRON MAN !",
    jessica_jones_custom: "CRACK !", lady_sif: "FOR ASGARD !", lockjaw: "WOOF !", madame_web: "I SEE !",
    mister_fantastic: "STRETCH !", moon_knight: "KHONSHU !", ms_america: "TICKET TO THE MULTIVERSE !",
    night_thrasher: "WHAM !", okoye: "WAKANDA FOREVER !", patriot: "KLANG !", red_guardian: "SLAM !",
    rescue_rainy: "MAG-FIELD !", scarlet_spider: "THWIP !", speed: "ZIP !", spider_man_rainy: "THWIP !",
    spider_man_noir: "THWIP !", stan_lee: "EXCELSIOR !", sunfire: "FWOOSH !",
    superior_iron_man: "I AM IRON MAN !", texas_twister: "YEEHAW !", the_thing: "IT'S CLOBBERIN' TIME !",
    thor_jane_foster: "FOR ASGARD !", throg: "RIBBIT !", totally_awesome_hulk: "SMASH !",
    venom_rainy: "WE ARE VENOM !", venompool: "CHIMICHANGA !", viv_vision: "WHIRR !", wiccan: "SPELL !",
    wolverine_x23: "SNIKT !", yondu: "FWEEET !",
};
function onomatopee(hero) {
    return ONOMATOPEES[hero.id] || "BAM !";
}


/** Le héros en scène : celui du siège actif, sauf pendant un survol. */
let herosSurvole = null;

function herosDuSiegeActif() {
    const p = state.players[state.activeSlot];
    return (p && p.hero) || null;
}

function stepTeam() {
    const wrap = el("section", { class: "step team-b" },
        el("div", { class: "tb-scene", id: "tb-scene" }),
    );
    const f = state.heroFilters;
    const droite = el("div", { class: "tb-droite" },
        bandeauEnLigne(),
        creationCampagne() ? el("div", { class: "command-band" }, modeStrip()) : null,
        choixCoop(),
        // La vue « cartes du héros » prend la place du roster (voir
        // ouvrirCartesHeros) ; les deux vivent côte à côte, une seule visible.
        el("div", { class: "tb-vue-cartes", id: "tb-vue-cartes", hidden: true }),
        el("div", { class: "tb-entete" },
            el("b", { class: "mvl" }, t("Héros")),
            el("span", { class: "tb-compte", id: "tb-compte" }, ""),
            creationCampagne() ? null : el("button", {
                class: "tb-mode",
                title: t("Changer de mode de jeu"),
                onclick: () => { hideHover(); state.accueil = true; render(); },
            }, libelleMode(state.mode) + " · " + state.playerCount + " " + t("héros") + " ›"),
        ),
        el("div", { class: "tb-filtres" },
            el("input", {
                class: "search tb-search",
                placeholder: t("Rechercher un héros ou un trait"),
                value: f.q,
                oninput: (e) => { f.q = e.target.value; refreshHeroGrid(); },
            }),
            el("button", {
                class: "tampon" + (f.fav ? " on" : ""),
                onclick: (e) => { f.fav = !f.fav; e.currentTarget.classList.toggle("on", f.fav); refreshHeroGrid(); },
            }, t("Favoris")),
            el("select", {
                class: "sel vague-select tampon",
                onchange: (e) => { f.vague = e.target.value; refreshHeroGrid(); },
            }, el("option", { value: "" }, t("Toutes les vagues"))),
            el("button", {
                class: "tampon" + (f.homebrew ? " on" : ""),
                title: t("Héros fan-made, hors de toute extension officielle"),
                onclick: (e) => {
                    f.homebrew = !f.homebrew;
                    e.currentTarget.classList.toggle("on", f.homebrew);
                    f.vague = "";
                    majMenuVagues();
                    refreshHeroGrid();
                },
            }, "Fan-made"),
        ),
        el("div", { class: "hero-grid tb-roster", id: "hero-grid" }, el("div", { class: "loading" }, t("Chargement des héros..."))),
        el("div", { class: "tb-equipe", id: "tb-equipe" }),
    );
    wrap.append(droite);
    herosSurvole = null;
    loadHeroes();
    // La scène et l'équipe se dessinent une fois la section DANS la page :
    // elles se retrouvent par identifiant.
    Promise.resolve().then(() => { rendreEquipe(); rendreScene(herosDuSiegeActif()); });
    return wrap;
}

/** Le pli du bas de scène : la biographie et l'état civil, repliés. Un écran
 *  de sélection n'a pas à les imposer, mais les perdre appauvrirait le jeu.
 *
 *  Le pli se RETIENT (la scène se reconstruit à chaque survol : sans cela, la
 *  biographie se refermerait au moindre mouvement de souris), et pendant qu'il
 *  est ouvert la scène efface son nom géant, que le panneau recouvrirait. */
let bioDepliee = false;

function pliBio(titre, lignes) {
    const contenu = lignes.filter(Boolean);
    if (!contenu.length) return null;
    const pli = el("details", { class: "tb-bio", open: bioDepliee || undefined },
        el("summary", {}, titre), ...contenu);
    pli.addEventListener("toggle", () => {
        bioDepliee = pli.open;
        const scene = pli.closest(".tb-scene");
        if (scene) scene.classList.toggle("bio-ouverte", pli.open);
    });
    return pli;
}

/** La moitié gauche : l'art, le nom, les chiffres du héros donné (ou l'appel
 *  à en choisir un). Reconstruite à chaque survol et à chaque choix. */
/** Le nom géant d'une scène : jamais coupé, jamais sur les tampons.
 *
 *  Deux réglages, mesurés après le rendu :
 *  - la HAUTEUR DE POSE : le nom se cale juste au-dessus de ce qui est sous
 *    lui (les tampons, la règle du défi), quelle que soit la hauteur que
 *    ceux-ci prennent (les tampons passent sur deux lignes dès que le méchant
 *    a des PV par joueur) ;
 *  - la TAILLE : elle descend, par pas, tant qu'un mot déborde la largeur ou
 *    que le nom sort par le haut de la scène. Un mot n'est jamais brisé.
 *  Constat de l'utilisateur : « des fois leur nom est coupé, car trop long »,
 *  et « ça ne doit jamais passer en dessous ou au-dessus des infos ». */
function ajusterNomGeant(scene) {
    const nom = scene && scene.querySelector(".tb-nomg");
    if (!nom) return;
    const mesurer = () => {
        const dessous = [".tb-tampons", ".tb-defi"]
            .map((sel) => scene.querySelector(sel))
            .filter((e) => e && e.offsetParent !== null);
        const bas = scene.getBoundingClientRect().bottom;
        const hautDuDessous = dessous.length
            ? Math.min(...dessous.map((e) => e.getBoundingClientRect().top))
            : bas - 110;
        nom.style.bottom = Math.round(bas - hautDuDessous + 14) + "px";
        const max = parseFloat(getComputedStyle(nom).fontSize) || 132;
        let taille = max;
        nom.style.fontSize = "";
        const debordeLargeur = () => nom.scrollWidth > nom.clientWidth + 1;
        const debordeHaut = () => nom.getBoundingClientRect().top < scene.getBoundingClientRect().top + 16;
        while (taille > 44 && (debordeLargeur() || debordeHaut())) {
            taille -= 4;
            nom.style.fontSize = taille + "px";
        }
    };
    // Deux images : les polices web et la mise en page des tampons doivent
    // être là avant de mesurer.
    requestAnimationFrame(() => requestAnimationFrame(mesurer));
}

function rendreScene(h) {
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    if (!h) {
        poser(scene,
            el("div", { class: "tb-art vide" }),
            el("div", { class: "tb-trame" }),
            el("div", { class: "tb-nomg" },
                el("small", {}, t("Siège") + " " + (state.activeSlot + 1)),
                t("Choisis un héros")),
        );
        return;
    }
    const traits = [...new Set([...(h.traits || []), ...(h.traitsAlterEgo || [])])].slice(0, 4).join(" · ");
    const vague = h.homebrew ? t("Fan-made")
        : (h.vague == null ? "" : (h.vague === 0 ? t("Set de base") : t("Vague") + " " + h.vague));
    const arts = (ARTS_HEROS[String(h.heroCardId || "").split(",")[0]] || []).length;
    poser(scene,
        // Scan anglais même en français : le scan FR porte un filigrane, très
        // visible à cette taille. Demande de l'utilisateur.
        h.lie
            ? el("div", { class: "tb-art" }, portraitDuo(h, "", cardImageUrlHd))
            : el("div", { class: "tb-art", style: { backgroundImage: `url("${cardImageUrlHd(picIdHeros(h.heroCardId))}")` } }),
        el("div", { class: "tb-trame" }),
        el("div", { class: "tb-nomg" },
            el("small", {}, traits || (h.extension || "").replace(/^\d+\.\s*/, "")),
            nomAffiche(h)),
        el("div", { class: "tb-tampons" },
            pvAffiches(h) ? el("span", { class: "tampon jaune" }, t("PV") + " " + pvAffiches(h)) : null,
            h.handSize != null ? el("span", { class: "tampon" }, t("Main") + " " + h.handSize) : null,
            vague ? el("span", { class: "tampon" }, vague) : null,
            arts ? el("button", {
                class: "tampon jaune tb-choix-art",
                title: t("Choisir l'art de la carte"),
                onclick: () => ouvrirArtsHeros(h),
            }, t("Art alt") + (prefs.heroArt(h.heroCardId) !== "standard" && prefs.heroArt(h.heroCardId) ? " ✓" : "")) : null,
        ),
        el("div", { class: "tb-bas" },
            el("button", {
                class: "tampon jaune tb-voir",
                title: t("Identité recto/verso et cartes signature"),
                onclick: () => ouvrirCartesHeros(h),
            }, t("Voir ses cartes")),
            bioDuHeros(h)),
    );
    scene.classList.toggle("bio-ouverte", bioDepliee && !!scene.querySelector(".tb-bio"));
    ajusterNomGeant(scene);
    scene.classList.remove("loupe-ouverte");
}

/* ---- Les cartes d'un héros : identité recto/verso, puis les signatures -----
   Le roster cède sa place à la liste ; survoler une carte l'agrandit sur la
   scène, à gauche. Ce sont les cartes que le héros apporte lui-même, jamais
   celles de son aspect : elles se choisissent à l'étape suivante. */

/** Les cartes d'un héros, dans l'ordre : identité(s), puis paquet signature. */
function cartesDuHeros(h) {
    const identites = [];
    for (const entree of (h.deck && h.deck.hero) || []) {
        for (const face of String(entree).split(",")) if (face) identites.push(face);
    }
    // Cloak & Dagger : la seconde identité est jouée en même temps.
    if (h.lie) {
        for (const entree of h.lie.hero || []) {
            for (const face of String(entree).split(",")) if (face) identites.push(face);
        }
    }
    const signatures = [
        ...((h.deck && h.deck.hero_deck) || []),
        ...((h.lie && h.lie.deck && h.lie.deck.hero_deck) || []),
    ];
    // Ce que le héros apporte AUSSI, et qui se retourne contre lui : son
    // obligation et son set némésis. Ils font partie du paquet, on les montre.
    const obligations = [
        ...((h.deck && h.deck.obligations) || []),
        ...((h.lie && h.lie.deck && h.lie.deck.obligations) || []),
    ];
    const nemesis = [
        ...((h.deck && h.deck.nemesis_set) || []),
        ...((h.lie && h.lie.deck && h.lie.deck.nemesis_set) || []),
    ];
    return { identites, signatures, obligations, nemesis };
}

function ouvrirCartesHeros(h) {
    const zone = document.getElementById("tb-vue-cartes");
    if (!zone) return;
    const { identites, signatures, obligations, nemesis } = cartesDuHeros(h);
    const compter = (liste) => {
        const nombres = new Map();
        for (const id of liste) nombres.set(id, (nombres.get(id) || 0) + 1);
        return nombres;
    };
    const nbSignatures = compter(signatures);
    const nbNemesis = compter(nemesis);

    const vignette = (id, classe, n, etiquette) => el("div", { class: "tb-carte " + (classe || "") },
        el("img", {
            src: cardImageUrl(id), loading: "lazy", alt: "",
            onmouseenter: () => loupe(id),
            onmouseleave: () => loupe(null),
        }),
        etiquette ? el("span", { class: "tb-carte-etiquette" }, etiquette) : null,
        n > 1 ? el("span", { class: "tb-carte-n" }, "×" + n) : null,
    );

    // Tout d'un bloc, identité en premier : une seule grille, sans onglet.
    // Puis les signatures, puis ce qui se retourne contre le héros : son
    // obligation (liseré ambre) et son set némésis (liseré rouge), étiquetés.
    poser(zone,
        el("div", { class: "tb-entete" },
            el("b", { class: "mvl" }, nomAffiche(h)),
            el("span", { class: "tb-compte" },
                identites.length + " " + t("faces") + " · " + signatures.length + " " + t("cartes")
                + (obligations.length ? " · " + t("obligation") : "")
                + (nemesis.length ? " · " + nemesis.length + " " + t("némésis") : "")),
            el("button", { class: "tb-mode", onclick: fermerCartesHeros }, "‹ " + t("Retour au roster")),
        ),
        el("div", { class: "tb-cartes-grille" },
            ...identites.map((id) => vignette(id, "identite", 0)),
            ...[...nbSignatures].map(([id, n]) => vignette(id, "", n)),
            ...obligations.map((id) => vignette(id, "obligation", 0, t("Obligation"))),
            ...[...nbNemesis].map(([id, n]) => vignette(id, "nemesis", n, t("Némésis"))),
        ),
    );
    zone.hidden = false;
    basculerVueCartes(true);
}

/** Le choix de l'art de la carte de héros, à la place du roster : la carte
 *  standard et chaque art alternatif, en grand, celui en usage cerclé de jaune.
 *  Un clic choisit et la scène suit ; c'est le réglage que l'étape Arsenal
 *  proposait déjà en vignettes, rendu visible là où l'on regarde le héros. */
function ouvrirArtsHeros(h) {
    const zone = document.getElementById("tb-vue-cartes");
    if (!zone) return;
    const base = String(h.heroCardId || "").split(",")[0];
    const arts = ARTS_HEROS[base] || [];
    const choix = prefs.heroArt(h.heroCardId) || "standard";
    const options = [{ code: "standard", nom: t("Standard"), image: base }]
        .concat(arts.map((a) => ({ code: a.code, nom: a.nom, image: `${base}_${a.code}` })));
    poser(zone,
        el("div", { class: "tb-entete" },
            el("b", { class: "mvl" }, nomAffiche(h)),
            el("span", { class: "tb-compte" }, t("Art de la carte") + " · " + t("mêmes valeurs de jeu")),
            el("button", { class: "tb-mode", onclick: fermerCartesHeros }, "‹ " + t("Retour au roster")),
        ),
        el("div", { class: "tb-cartes-grille tb-arts" },
            ...options.map((o) => el("div", { class: "tb-carte" + (o.code === choix ? " choisie" : "") },
                el("img", {
                    src: cardImageUrl(o.image), loading: "lazy", alt: o.nom,
                    onmouseenter: () => loupe(o.image),
                    onmouseleave: () => loupe(null),
                    onclick: () => {
                        prefs.setHeroArt(h.heroCardId, o.code);
                        loupe(null);
                        ouvrirArtsHeros(h);
                        rendreScene(h);
                    },
                }),
                el("span", { class: "tb-carte-etiquette" }, o.nom + (o.code === choix ? " ✓" : "")),
            )),
        ),
    );
    zone.hidden = false;
    basculerVueCartes(true);
}

function fermerCartesHeros() {
    const zone = document.getElementById("tb-vue-cartes");
    if (zone) zone.hidden = true;
    loupe(null);
    basculerVueCartes(false);
}

/** Cache ou rend le roster et ses filtres pendant que les cartes sont là. */
function basculerVueCartes(actif) {
    const droite = document.querySelector(".tb-droite");
    if (droite) droite.classList.toggle("vue-cartes", actif);
}

/** La carte survolée, en grand sur la scène. `null` la retire. */
function loupe(cardId) {
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    let boite = scene.querySelector(".tb-loupe");
    if (!cardId) {
        if (boite) boite.remove();
        scene.classList.remove("loupe-ouverte");
        return;
    }
    if (!boite) {
        boite = el("div", { class: "tb-loupe" });
        scene.append(boite);
    }
    poser(boite, el("img", { src: cardImageUrl(cardId), alt: "" }));
    scene.classList.add("loupe-ouverte");
}

/** La fiche encyclopédique d'un héros, repliée au pied de sa scène. */
function bioDuHeros(h) {
    const info = HEROS_INFO[h.heroCardId];
    if (!info) return null;
    const en = langueActuelle() === "en";
    const champ = (fr, versionEn) => (en && versionEn) || fr;
    return pliBio(t("Biographie"), [
        el("p", { class: "hh-bio" }, champ(info.bio, info.bioEn)),
        info.civil ? detailRow(t("Identité civile"), champ(info.civil, info.civilEn)) : null,
        info.base ? detailRow(t("Base"), champ(info.base, info.baseEn)) : null,
        info.equipes ? detailRow(t("Équipes"), champ(info.equipes, info.equipesEn)) : null,
        info.ennemis ? detailRow(t("Ennemis"), champ(info.ennemis, info.ennemisEn)) : null,
        info.apparition ? detailRow(t("Première apparition"), info.apparition) : null,
    ]);
}

/** Les sièges de l'équipe, en bas de la colonne de droite. */
function rendreEquipe() {
    const zone = document.getElementById("tb-equipe");
    if (!zone) return;
    const sieges = [];
    for (let i = 0; i < state.playerCount; i++) {
        const pl = state.players[i];
        const pilotable = !(enLigne() && i > 0);
        sieges.push(el("button", {
            class: "tb-siege" + (state.activeSlot === i ? " actif" : "") + (pl.hero ? " plein" : "") + (pilotable ? "" : " salon-invite"),
            disabled: pilotable ? undefined : "",
            title: pilotable ? (pl.hero ? pl.hero.name : t("Joueur") + " " + (i + 1)) : t("Ce joueur choisit depuis son propre écran"),
            onclick: () => {
                if (!pilotable) return;
                state.activeSlot = i;
                rendreEquipe();
                // Chaque étape a sa scène : les héros la remplissent avec le
                // héros du siège, l'arsenal avec son deck.
                if (state.step === 1) { rendreSceneDeck(); rendreOutilsDeck(); loadDecks(i); }
                else rendreScene(herosDuSiegeActif());
            },
        },
            pl.hero ? portraitHeros(pl.hero) : el("span", { class: "plus" }, "+"),
            el("span", { class: "tb-siege-nom" }, state.step === 1 && pl.deck
                ? cleanNomDeck(pl.deck.name)
                : (pl.hero ? pl.hero.name : t("Joueur") + " " + (i + 1))),
        ));
    }
    poser(zone,
        el("span", { class: "tb-equipe-k" }, t("Ton équipe")),
        ...sieges,
    );
}

/** Recruter : le geste de la carte qui surgit, l'onomatopée, puis la scène. */
function recruter(h, portraitEl) {
    assignHero(state.activeSlot, h);
    autoAdvanceSlot();
    herosSurvole = null;
    // La scène d'abord (elle se reconstruit), la carte qui surgit ensuite,
    // par-dessus : dans l'autre ordre, la reconstruction l'emportait.
    rendreScene(herosDuSiegeActif());
    rendreEquipe();
    const scene = document.getElementById("tb-scene");
    if (scene) {
        const eclair = el("div", { class: "tb-eclair" },
            el("img", { src: cardImageUrl(picIdHeros(h.heroCardId)), alt: "" }),
            el("span", { class: "ono" }, onomatopee(h)),
        );
        scene.append(eclair);
        eclair.addEventListener("animationend", (ev) => { if (ev.target === eclair) eclair.remove(); });
        setTimeout(() => eclair.remove(), 2800);   // filet, un peu apres la fin de l'animation
    }
    document.querySelectorAll(".tb-port").forEach((b) => {
        b.classList.toggle("chosen", activePlayers().some((p) => p.hero && p.hero.id === b.dataset.hero));
    });
    // La barre du bas suit (Continuer s'allume) sans reconstruire l'écran.
    const nav = document.querySelector(".nav");
    if (nav) nav.replaceWith(navBar());
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
        // Le nom ET les traits des deux faces (voir `recherche` dans
        // catalog.js) : « avenger » ne rend que les Avengers, « genius » que
        // les alter-ego savants.
        (!q || h.recherche.includes(q)) &&
        (!f.vague || String(h.vague) === f.vague) &&
        (!f.fav || favs.includes(h.id)) &&
        // Le homebrew est masqué par défaut et s'affiche seul quand on le coche.
        (!!h.homebrew === f.homebrew));
    const compte = document.getElementById("tb-compte");
    if (compte) compte.textContent = list.length + " " + t("héros");
    if (!list.length) {
        grid.replaceChildren(el("div", { class: "empty-state" }, t("Aucun héros trouvé")));
        return;
    }
    grid.replaceChildren(...list.map((h) => {
        const chosen = activePlayers().some((p) => p.hero && p.hero.id === h.id);
        return el("button", {
            class: "tb-port" + (chosen ? " chosen" : ""),
            "data-hero": h.id,
            title: nomAffiche(h),
            onclick: (e) => recruter(h, e.currentTarget),
            onmouseenter: () => { herosSurvole = h; rendreScene(h); },
            onmouseleave: () => { herosSurvole = null; rendreScene(herosDuSiegeActif()); },
            onfocus: () => { herosSurvole = h; rendreScene(h); },
        },
            portraitHeros(h),
            el("span", { class: "tb-port-nom" }, nomAffiche(h)),
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
            el("span", {
                class: "hc-deck",
                title: t("Voir le deck"),
                onclick: (e) => { e.stopPropagation(); e.preventDefault(); ouvrirDeckDuHeros(h); },
            }, "▤"),
        );
    }));
}

/** Apercu du deck de base d'un heros, depuis sa vignette. La modale porte le
 *  bouton « Modifier », qui ouvre le deck-builder charge sur ce deck. */
async function ouvrirDeckDuHeros(h) {
    await cards.load();
    let decks = [];
    try { decks = await catalog.decksForHero(h); } catch (e) { return; }
    const base = decks.find((d) => d.source === "base") || decks[0];
    if (base) showDeckCards(base.deck, h, base.id);
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
    }, 160);
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
    // alphabétique. Quatre origines mélangées : rééditions d'extension
    // (vrais codes de carte), promos « Play-and-Share » de FFG,
    // collections fan-made « DesignHacker », et les re-skins livrés PAR un
    // pack fan-made (Gwenpool, Howard the Duck, Ms. America). Sinister
    // Motives (27020-22) est volontairement absent : visuel identique au
    // jeu de base.
    //
    // ⚠ N'inscrire une collection ICI que si ses TROIS images existent dans
    // assets/pics/ : sans elles la vignette part en repli silencieux. Un
    // relevé du 31/08/2026 a trouvé ~40 triplets de re-skins déclarés dans
    // data/cards.json (full_link vers 01088/89/90) dont les images ne sont
    // PAS livrées — luke_cage 62025-27 par exemple : ils restent donc hors
    // de cette liste tant que les images manquent.
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
    { code: "gwenpool", nom: "Gwenpool", apercu: "gp016" },
    { code: "hk", nom: "Hawkeye", apercu: "01089_hk" },
    { code: "howard", nom: "Howard the Duck", apercu: "hd019" },
    { code: "hu", nom: "Hulk", apercu: "01089_hu" },
    { code: "im", nom: "Iron Man", apercu: "01089_im" },
    { code: "ekaug_jj", nom: "Jessica Jones", apercu: "01089_ekaug_jj" },
    { code: "dh_miles", nom: "Miles Morales", apercu: "01089_dh_miles" },
    { code: "ms_america", nom: "Ms. America", apercu: "ma028" },
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
/** Apercu d'un deck, toutes cartes visibles.
 *  `hero` et `deckId` sont facultatifs : quand ils sont fournis, la modale
 *  gagne un bouton qui ouvre le deck-builder DEJA CHARGE sur ce deck-la
 *  (parametre `?deck=`, voir js/deckbuilder/app.js). Sans eux, la modale reste
 *  un simple apercu, comme avant. */
/* Ouvrir et fermer une modale sans que rien ne bouge a l'ecran.
 *
 * Deux barres de defilement s'en melaient :
 *
 * 1. Celle du PANNEAU. Elle apparait des que les cartes depassent 88vh, prend
 *    sa largeur au contenu, et la grille en `auto-fill` se recompose : les
 *    cartes changent de colonne, la modale a l'air de sauter. `scrollbar-gutter`
 *    la reserve en permanence (voir prepare.css), donc plus rien ne bouge.
 *
 * 2. Celle de la PAGE. On la bloque le temps de la modale, sinon la molette
 *    fait defiler l'ecran derriere. Mais la retirer decale de sa largeur tout
 *    ce qui est centre — la modale comprise. On rend donc au document, en
 *    marge, exactement la largeur qu'on lui prend.
 */
let _modalesOuvertes = 0;

function ouvrirModale(overlay) {
    if (_modalesOuvertes === 0) {
        // ⚠ LA MARGE VA SUR L'OVERLAY, PAS SUR <html>. L'overlay est en
        // `position:fixed` : il se cale sur la fenetre, que le document ait
        // une marge ou non. Poser la compensation sur <html> ne le recentrait
        // donc pas, et la modale sautait de la moitie de la barre au moment ou
        // on la bloquait. La variable est lue par .deck-modal (prepare.css).
        const barre = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty("--barre-defilement", barre + "px");
        document.documentElement.style.overflow = "hidden";
    }
    _modalesOuvertes += 1;
    document.body.append(overlay);
}

function fermerModale(overlay) {
    // `isConnected` : sans lui, deux fermetures de suite (le clic dehors qui
    // suit le bouton) decompteraient deux fois et libereraient la page trop
    // tot, ou jamais.
    if (!overlay || !overlay.isConnected) return;
    overlay.remove();
    _modalesOuvertes = Math.max(0, _modalesOuvertes - 1);
    if (_modalesOuvertes === 0) {
        document.documentElement.style.overflow = "";
        document.documentElement.style.removeProperty("--barre-defilement");
    }
}

function showDeckCards(deck, hero, deckId) {
    const ids = [...(deck.hero || []).flatMap((x) => String(x).split(",")), ...(deck.hero_deck || []), ...(deck.player_deck || [])];
    const counts = {};
    for (const id of ids) counts[id] = (counts[id] || 0) + 1;
    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) { hideHover(); fermerModale(overlay); } } },
        el("div", { class: "deck-modal-panel" },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, deck.name || "Deck"),
                el("span", { class: "dm-sub" }, ids.length + " " + t("cartes")),
                hero ? el("button", {
                    class: "dm-edit",
                    title: t("Ouvrir ce deck dans l’éditeur"),
                    onclick: (e) => {
                        e.stopPropagation();
                        const q = "/deck-builder.html?hero=" + encodeURIComponent(hero.id) +
                            (deckId ? "&deck=" + encodeURIComponent(deckId) : "");
                        window.open(q, "_blank");
                    },
                }, t("Modifier")) : null,
                el("button", { class: "dm-close", onclick: () => { hideHover(); fermerModale(overlay); } }, "✕"),
            ),
            el("div", { class: "dm-grid" }, ...Object.keys(counts).map((id) =>
                el("div", { class: "dm-card" },
                    el("img", { src: cardImageUrl(id), loading: "lazy", onmouseenter: (e) => showCardHover(id, e.currentTarget), onmouseleave: scheduleHide }),
                    counts[id] > 1 ? el("span", { class: "dm-count" }, "x" + counts[id]) : null,
                ))),
        ));
    ouvrirModale(overlay);
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
            fermerModale(overlay);
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

    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) fermerModale(overlay); } },
        el("div", { class: "deck-modal-panel" },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, `${t("Decks MarvelCDB")} — ${p.hero.name}`),
                compte,
                el("button", { class: "dm-close", onclick: () => fermerModale(overlay) }, "✕"),
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
    ouvrirModale(overlay);
}

/* ---- Étape 2, l'arsenal : un joueur à la fois -------------------------------
   Avant, les quatre joueurs empilaient leurs blocs de decks sur une page qui
   défilait. Ici, un seul siège à la fois : sa scène à gauche, ses decks à
   droite, et la rangée des sièges en bas pour passer de l'un à l'autre. */

function stepDecks() {
    // En ligne, l'hôte ne pilote que son siège : les invités choisissent
    // depuis le leur. On revient donc toujours sur le siège 0.
    if (enLigne()) state.activeSlot = 0;
    const wrap = el("section", { class: "step team-b arsenal" },
        el("div", { class: "tb-scene", id: "tb-scene" }),
    );
    const droite = el("div", { class: "tb-droite" },
        el("div", { class: "tb-entete" },
            el("b", { class: "mvl" }, t("Decks")),
            el("span", { class: "tb-compte", id: "tb-compte" }, ""),
            el("span", { class: "tb-mode" }, navStatus()),
        ),
        el("div", { class: "hero-grid tb-roster tb-roster-deck", id: "deck-liste" },
            el("div", { class: "loading" }, t("Chargement des decks..."))),
        el("div", { class: "tb-arsenal-outils", id: "deck-outils" }),
        el("div", { class: "tb-equipe", id: "tb-equipe" }),
    );
    wrap.append(droite);
    Promise.resolve().then(() => {
        rendreSceneDeck();
        rendreOutilsDeck();
        rendreEquipe();
        loadDecks(state.activeSlot);
    });
    return wrap;
}

/** La moitié gauche : le héros du siège actif, et ce que son deck contient. */
function rendreSceneDeck() {
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    const p = state.players[state.activeSlot];
    const h = p && p.hero;
    if (!h) {
        poser(scene,
            el("div", { class: "tb-art vide" }),
            el("div", { class: "tb-trame" }),
            el("div", { class: "tb-nomg" }, el("small", {}, t("Arsenal")), t("Aucun héros")));
        return;
    }
    const st = p.deck ? deckStats(p.deck) : null;
    const aspects = st ? Object.keys(st.asp).filter((x) => x !== "basic") : [];
    poser(scene,
        // Scan anglais même en français : le scan FR porte un filigrane, très
        // visible à cette taille. Demande de l'utilisateur.
        h.lie
            ? el("div", { class: "tb-art" }, portraitDuo(h, "", cardImageUrlHd))
            : el("div", { class: "tb-art", style: { backgroundImage: `url("${cardImageUrlHd(picIdHeros(h.heroCardId))}")` } }),
        el("div", { class: "tb-trame" }),
        el("div", { class: "tb-nomg" },
            el("small", {}, t("Arsenal de")),
            nomAffiche(h)),
        el("div", { class: "tb-tampons" },
            p.deck ? el("span", { class: "tampon jaune" }, cleanNomDeck(p.deck.name) || t("Deck de base")) : null,
            st ? el("span", { class: "tampon" }, st.total + " " + t("cartes")) : null,
            ...aspects.map((x) => el("span", {
                class: "tampon aspect",
                style: { background: ASPECTS[x] || "#555", borderColor: "#111" },
            }, x)),
        ),
    );
    ajusterNomGeant(scene);
}

/** Sous la liste : importer, parcourir, construire, et les cosmétiques. */
function rendreOutilsDeck() {
    const zone = document.getElementById("deck-outils");
    if (!zone) return;
    const i = state.activeSlot;
    const p = state.players[i];
    if (!p || !p.hero) { poser(zone); return; }
    const cosmetiques = [blocIdentiteHeros(p, i), blocArtHeros(p.hero), blocRessources(p.hero)].filter(Boolean);
    poser(zone,
        el("div", { class: "tb-menace-ligne" },
            el("input", { class: "search tb-search", id: "mcdb-" + i, placeholder: t("Colle une URL ou un ID marvelcdb...") }),
            el("button", { class: "tampon", onclick: () => doImport(i) }, "Import"),
            el("button", {
                class: "tampon",
                title: t("Parcourir les decks publiés sur MarvelCDB"),
                onclick: () => ouvrirPanneauCdb(i),
            }, t("Decks MarvelCDB")),
            el("button", {
                class: "tampon",
                title: t("Construire un deck personnalisé pour ce héros"),
                onclick: () => { window.open("/deck-builder.html?hero=" + encodeURIComponent(p.hero.id), "_blank"); },
            }, t("Éditeur de deck")),
            el("span", { class: "mcdb-status", id: "mcdb-st-" + i }),
        ),
        // Identité, art alternatif, arts des ressources : du cosmétique (sauf
        // l'identité, qui change les traits), replié pour ne pas enterrer les
        // decks sous quarante vignettes.
        cosmetiques.length
            ? el("details", { class: "tb-cosmetiques" },
                el("summary", {}, t("Identité et arts")),
                ...cosmetiques)
            : null,
    );
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
            rendreSceneDeck();
        }
    }
    const box = document.getElementById("deck-liste");
    // Le siège a pu changer pendant la lecture : on ne peint pas la liste d'un
    // joueur dans l'écran d'un autre.
    if (!box || i !== state.activeSlot) return;
    const compte = document.getElementById("tb-compte");
    if (compte) compte.textContent = decks.length + " " + t("decks");

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
            class: "tb-deck" + (on ? " chosen" : ""),
            onclick: () => {
                p.deck = dk.deck; p.deckSource = dk.source; p.deckAuto = false;
                // « campagne » n'existe que sur cet ecran-ci : le retenir comme
                // dernier deck du heros ne designerait plus rien demain.
                if (dk.source !== "campagne") prefs.setLastDeck(p.hero.heroCardId, dk.id);
                loadDecks(i);
                rendreSceneDeck();
                rendreEquipe();
                const nav = document.querySelector(".nav");
                if (nav) nav.replaceWith(navBar());
            },
        },
            el("div", { class: "do-name" }, cleanNomDeck(dk.name)),
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
                el("span", { class: "do-view", onclick: (e) => { e.stopPropagation(); e.preventDefault(); showDeckCards(dk.deck, p.hero, dk.id); } }, t("Voir les cartes")),
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

/* ---- Étape 3, la cible : même mise en scène, en rouge ----------------------
   À gauche le méchant en scène, à droite les boîtes d'extension, la grille des
   scénarios, puis le NIVEAU DE MENACE (qui n'a plus son étape) et la table qui
   se compose. Voir stepTeam() : les deux écrans partagent leurs classes. */

/** Le cri du méchant quand on verrouille la cible. Repli : « RAAAH ! ». */
const CRIS_MECHANTS = {
    rhino: "RAAAH !", klaw: "BWAAAM !", ultron: "I AM ULTRON !",
    green_goblin: "HA HA HA !", risky_business: "HA HA HA !", mutagen_formula: "HA HA HA !",
    wrecking_crew: "WRECK IT !", crossbones: "BOOM !", absorbing_man: "CRUNCH !", taskmaster: "COPIED !",
    zola: "SUBJECT !", red_skull: "HAIL HYDRA !", kang: "TIME OUT !", thanos: "INEVITABLE !",
    hela: "DEATH !", loki: "TRICKED !", ronan: "JUDGMENT !", drang: "RAID !", collector: "MINE !",
    nebula: "UPGRADE !", sandman: "FWOOSH !", venom: "WE ARE VENOM !", mysterio: "ILLUSION !",
    sinister_six: "SIX !", venom_goblin: "GRAAAH !", doctor_octopus: "TENTACLES !",
    sabretooth: "SNIKT !", project_wideawake: "SENTINEL !", master_mold: "MOLD !",
    mansion_attack: "ATTACK !", magneto: "VRRMM !", morlock_siege: "SIEGE !", on_the_run: "RUN !",
    juggernaut: "UNSTOPPABLE !", mister_sinister: "SINISTER !", stryfe: "STRYFE !",
    apocalypse: "APOCALYPSE !", dark_beast: "BEAST !", en_sabah_nur: "SURVIVE !",
    hydra_patrol: "HAIL HYDRA !", hydra_assault: "HAIL HYDRA !", the_hood: "HOOD !",
    mojo: "RATINGS !", spiral: "SPIRAL !", brood: "SKREEE !",
};
function criDuMechant(sc) {
    return CRIS_MECHANTS[sc.id] || "RAAAH !";
}

function stepScenario() {
    const wrap = el("section", { class: "step team-b eux" },
        el("div", { class: "tb-scene", id: "tb-scene" }),
    );
    const droite = el("div", { class: "tb-droite" },
        el("div", { class: "tb-entete" },
            el("b", { class: "mvl" }, t("Scénarios")),
            el("span", { class: "tb-compte", id: "tb-compte" }, ""),
            el("span", { class: "tb-mode" }, navStatus()),
        ),
        el("div", { class: "ext-tabs", id: "ext-tabs" }, el("div", { class: "loading" }, "...")),
        el("div", { class: "hero-grid tb-roster tb-roster-scn", id: "scn-grid" }),
        // Le niveau de menace, ici même : c'est en voyant le méchant qu'on
        // décide de la difficulté, pas un écran plus loin.
        el("div", { class: "tb-menace", id: "tb-menace" }),
        el("div", { class: "tb-equipe", id: "tb-equipe" }),
    );
    wrap.append(droite);
    loadExtTabs();
    Promise.resolve().then(() => {
        rendreSceneMechant(state.scenario);
        rendreMenace();
        rendreTable();
    });
    return wrap;
}

/** La moitié gauche : le méchant en scène, ses chiffres imprimés, ses livrets. */
function rendreSceneMechant(sc) {
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    if (!sc) {
        poser(scene,
            el("div", { class: "tb-art vide" }),
            el("div", { class: "tb-trame" }),
            el("div", { class: "tb-nomg" }, el("small", {}, t("Méchant")), t("Choisis un méchant")),
        );
        return;
    }
    const carte = cards.get((sc.villainCards || [])[0] || sc.tileImage);
    const d = (carte && carte.desc) || {};
    // Les valeurs imprimées sur la carte : « 14* » veut dire 14 par joueur.
    const pv = String(d.HP || "").replace("*", "");
    const parJoueur = String(d.HP || "").includes("*");
    const multi = (sc.villainCards || []).length > 1;
    poser(scene,
        el("div", { class: "tb-art", style: { backgroundImage: `url("${cardImageUrlHd(sc.tileImage)}")` } }),
        el("div", { class: "tb-trame" }),
        el("div", { class: "tb-nomg" },
            el("small", {}, (sc.extension || "").replace(/^\d+\.\s*/, "")),
            sc.name),
        el("div", { class: "tb-tampons" },
            pv ? el("span", { class: "tampon rouge" }, t("PV") + " " + pv + (parJoueur ? " / " + t("joueur") : "")) : null,
            d.ATK ? el("span", { class: "tampon" }, t("ATQ") + " " + d.ATK) : null,
            d.SCH ? el("span", { class: "tampon" }, t("MEN") + " " + d.SCH) : null,
            multi
                ? el("span", { class: "tampon" }, sc.villainCards.length + " " + t("méchants"))
                : (sc.villains.length ? el("span", { class: "tampon" }, sc.villains.length + " " + t(sc.villains.length > 1 ? "stades" : "stade")) : null),
            sc.schemes.length ? el("span", { class: "tampon" }, sc.schemes.length + " " + t(sc.schemes.length > 1 ? "manigances" : "manigance")) : null,
            sc.hasExpertVariant ? el("span", { class: "tampon rouge" }, "Expert") : null,
        ),
        // La règle d'un défi n'est PAS décorative : elle change la partie.
        // Elle s'affiche, quand les livrets et la biographie se replient.
        regleDuDefi(sc),
        el("div", { class: "tb-bas" }, bioDuMechant(sc), documentsDeLaCible(sc)),
    );
    scene.classList.toggle("bio-ouverte", bioDepliee && !!scene.querySelector(".tb-bio"));
    ajusterNomGeant(scene);
}

/** La fiche d'un méchant, par l'identifiant de sa PREMIÈRE carte, sinon par
 *  son NOM.
 *
 *  ⚠ LE REPLI PAR LE NOM EST CE QUI REND LEUR FICHE AUX DÉFIS (constat de
 *  l'utilisateur, 08/09/2026 : « surtout les méchants n'avaient pas vraiment
 *  de phrase »). Un scénario-défi désigne souvent une AUTRE étape du même
 *  méchant que le scénario ordinaire (« Two for One » commence Rhino à
 *  01095, la fiche est sous 01094) : vingt-quatre scènes s'affichaient sans
 *  biographie alors qu'elle existait. La table nom -> fiche se construit une
 *  fois, depuis les cartes que les clés de MECHANTS_INFO désignent. */
let fichesMechantsParNom = null;
function ficheDuMechant(cardId) {
    const directe = MECHANTS_INFO[cardId];
    if (directe) return directe;
    if (!fichesMechantsParNom) {
        fichesMechantsParNom = new Map();
        for (const cle of Object.keys(MECHANTS_INFO)) {
            const carte = cards.get(cle);
            const nom = nomPropre(carte && carte.name);
            if (nom && !fichesMechantsParNom.has(nom)) fichesMechantsParNom.set(nom, MECHANTS_INFO[cle]);
        }
    }
    const carte = cards.get(cardId);
    return fichesMechantsParNom.get(nomPropre(carte && carte.name)) || null;
}
/** « * Rhino » et « Rhino » sont le même méchant. */
function nomPropre(nom) {
    return String(nom || "").replace(/^\*\s*/, "").trim().toLowerCase();
}

/** La fiche encyclopédique d'un méchant, repliée au pied de sa scène. */
function bioDuMechant(sc) {
    const info = ficheDuMechant((sc.villainCards || [])[0]);
    const en = langueActuelle() === "en";
    return pliBio(t("Biographie"), [
        info ? el("p", { class: "hh-bio" }, (en && info.bioEn) || info.bio) : null,
        detailRow(t("Méchant(s)"), sc.villainNames.length ? sc.villainNames.join(", ") : t("Pas de méchant fixe")),
        detailRow(t("Sets requis"), sc.mandatoryEncounterSets.map(titleize).join(", ") || "-"),
        detailRow(t("Sets recommandés"), sc.recommendedModularSets.map(titleize).join(", ") || "-"),
    ]);
}

/** Le bandeau d'un scénario-défi : sa règle spéciale, en clair. */
function regleDuDefi(sc) {
    if (!sc.challenges || !sc.challenges.length) return null;
    const info = DEFIS_INFO[sc.challenges[0]];
    if (!info) return null;
    const en = langueActuelle() === "en";
    return el("div", { class: "tb-defi" },
        el("b", {}, t("Règle du défi")),
        el("span", {}, (en && info.regleEn) || info.regle),
        info.contrainte ? el("span", { class: "tb-defi-c" }, (en && info.contrainteEn) || info.contrainte) : null,
    );
}

/** Verrouiller une cible : le cri, puis la scène et la table. */
function verrouillerCible(sc) {
    selectScenario(sc);
    rendreSceneMechant(sc);
    rendreMenace();
    rendreTable();
    document.querySelectorAll(".tb-port").forEach((b) => {
        b.classList.toggle("chosen", b.dataset.scn === sc.id);
    });
    const scene = document.getElementById("tb-scene");
    if (scene) {
        const cri = criDuMechant(sc);
        const eclair = el("div", { class: "tb-eclair" },
            el("img", { src: cardImageUrl((sc.villainCards || [])[0] || sc.tileImage), alt: "" }),
            el("span", { class: "ono rouge" }, cri),
        );
        scene.append(eclair);
        eclair.addEventListener("animationend", (ev) => { if (ev.target === eclair) eclair.remove(); });
        setTimeout(() => eclair.remove(), 2800);   // filet, un peu apres la fin de l'animation
    }
    const nav = document.querySelector(".nav");
    if (nav) nav.replaceWith(navBar());
}

/** Le niveau de menace, sous la grille : règles en tampons, sets en chips. */
function rendreMenace() {
    const zone = document.getElementById("tb-menace");
    if (!zone) return;
    const sc = state.scenario;
    if (!sc) {
        poser(zone,el("div", { class: "tb-menace-vide" }, t("Choisis un méchant pour régler la menace.")));
        return;
    }
    const d = state.difficulty;
    const regle = (libelle, actif, action) => el("button", {
        class: "tampon" + (actif ? " on" : ""),
        onclick: () => { action(); rendreMenace(); rendreTable(); },
    }, libelle);

    const heroique = el("div", { class: "tb-heroique" },
        el("span", { class: "tb-menace-k" }, t("Héroïque")),
        el("input", {
            type: "range", min: "0", max: "8", value: String(d.heroic),
            oninput: (e) => {
                d.heroic = +e.target.value;
                const n = zone.querySelector(".tb-heroique b");
                if (n) n.textContent = d.heroic > 0 ? String(d.heroic) : "0";
            },
        }),
        el("b", {}, d.heroic > 0 ? String(d.heroic) : "0"),
    );

    poser(zone,
        el("div", { class: "tb-menace-ligne" },
            el("span", { class: "tb-menace-k" }, t("Menace")),
            regle("Standard", d.base === "standard", () => { d.base = "standard"; }),
            sc.hasExpertVariant ? regle("Expert", d.base === "expert", () => { d.base = "expert"; }) : null,
            regle("Skirmish", d.skirmish, () => { d.skirmish = !d.skirmish; }),
            heroique,
        ),
        el("div", { class: "tb-menace-ligne" },
            el("span", { class: "tb-menace-k" }, t("Sets modulaires")),
            regle(t("Recommandés"), d.modularConfig === "recommended", () => { d.modularConfig = "recommended"; applyModularConfig(); }),
            regle(t("Personnalisés"), d.modularConfig === "custom", () => { d.modularConfig = "custom"; }),
            regle(t("Aléatoire"), d.modularConfig === "random", () => { d.modularConfig = "random"; applyModularConfig(); }),
        ),
        el("div", { class: "mod-chips", id: "modular-box" }),
        estBataille() ? blocSecondeTable() : null,
    );
    renderModular();
}

/** La table qui se compose : l'équipe, puis la cible verrouillée. */
function rendreTable() {
    const zone = document.getElementById("tb-equipe");
    if (!zone) return;
    const membres = activePlayers().filter((p) => p.hero).map((p) => el("div", {
        class: "tb-siege plein petit",
        title: p.hero.name,
    }, portraitHeros(p.hero), el("span", { class: "tb-siege-nom" }, p.hero.name)));
    const sc = state.scenario;
    poser(zone,
        el("span", { class: "tb-equipe-k" }, t("Face à face")),
        ...membres,
        el("span", { class: "tb-vs mvl" }, "VS"),
        // Un scénario à plusieurs méchants (Wrecking Crew) : un siège par
        // méchant, en rangée, même taille que ceux des héros. Demande de
        // l'utilisateur, 7 septembre 2026.
        ...(sc && mechantsDe(sc).length > 1
            ? mechantsDe(sc).map((id) => {
                const carte = cards.get(id);
                // Sans le symbole d'unicite qui ouvre le nom de la carte (« ✦ Wrecker »).
                const nom = ((carte && carte.name) || sc.name).replace(/^\W+\s*/, "");
                return el("div", { class: "tb-siege plein petit eux", title: nom },
                    el("div", { class: "portrait", style: { backgroundImage: `url("${cardImageUrl(id)}")` } }),
                    el("span", { class: "tb-siege-nom" }, nom));
            })
            : [sc
                ? el("div", { class: "tb-siege plein petit eux", title: sc.name },
                    el("div", { class: "portrait", style: { backgroundImage: `url("${cardImageUrl(sc.tileImage)}")` } }),
                    el("span", { class: "tb-siege-nom" }, sc.name))
                : el("div", { class: "tb-siege petit eux" }, el("span", { class: "plus" }, "?"))]),
    );
}

/** Les scenarios de bataille : ceux dont l'adversaire est un LEADER.
 *  La regle se lit dans les DONNEES et non dans une liste de boites ecrite en
 *  dur : une future boite competitive apparaitra sans toucher a ce fichier.
 *  C'est la meme lecon que les aspects, qui etaient enumeres a trois endroits. */
async function scenariosDeBataille() {
    await cards.load();
    const sortie = [];
    for (const ext of await catalog.extensions()) {
        let liste = [];
        try { liste = await catalog.scenariosForExtension(ext.key); } catch (e) { continue; }
        for (const sc of liste) {
            const carte = cards.get((sc.villainCards || [])[0]);
            if (carte && String(carte.type) === "Leader") sortie.push(sc);
        }
    }
    return sortie;
}

function blocSecondeTable() {
    const box = el("div", { class: "cfg-card" },
        el("div", { class: "cfg-head" }, t("Table du camp adverse")),
        el("small", {}, t("Chaque équipe affronte le scénario apporté par l'autre.")),
        el("div", { id: "table2-box" }, el("div", { class: "loading" }, "...")),
    );
    remplirSecondeTable();
    return box;
}

async function remplirSecondeTable() {
    const hote = document.getElementById("table2-box");
    if (!hote) return;
    const liste = await scenariosDeBataille();
    if (!liste.length) {
        hote.replaceChildren(el("small", {}, t("Aucun scénario de bataille dans les données.")));
        return;
    }
    const sel = el("select", {
        class: "cfg-select",
        onchange: (e) => {
            state.scenario2 = liste.find((s) => s.id === e.target.value) || null;
            render();
        },
    });
    sel.append(el("option", { value: "" }, t("Choisir le leader d'en face")));
    for (const sc of liste) {
        const opt = el("option", { value: sc.id }, sc.name + " · " + (sc.extension || ""));
        if (state.scenario2 && state.scenario2.id === sc.id) opt.selected = true;
        sel.append(opt);
    }
    hote.replaceChildren(sel);
}

/** Les documents de l'extension du scénario choisi, à même la bannière : c'est
 *  là qu'on se demande comment se joue une boîte, pas dans une liste de 27.
 *
 *  Rend null tant que le panneau n'a pas fini de charger sa liste, et quand
 *  l'extension n'a pas de livret. L'attente est bornée : le Briefing 03 arrive
 *  plusieurs clics après le chargement de la page. */
function documentsDeLaCible(sc) {
    if (!sc || !sc.extension) return null;
    const livret = livretDExtension(sc.extension);
    const carnet = carnetDExtension(sc.extension);
    if (!livret && !carnet) return null;
    const lien = (fiche, libelle) => fiche
        ? el("a", {
            class: "target-doc",
            href: "/" + encodeURIComponent(fiche.fichier),
            target: "_blank",
            rel: "noopener",
        }, picto("fa-book"), " " + t(libelle))
        : null;
    return el("div", { class: "target-docs" },
        lien(livret, "Livret de règles"),
        lien(carnet, "Carnet de campagne"),
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
    await preselectionDernierScenario();
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
            ? el("div", { class: "box box-defis" }, picto("fa-trophy"))
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
    const compte = document.getElementById("tb-compte");
    if (compte) compte.textContent = scs.length + " " + t("scénarios");
    grid.replaceChildren(...scs.map((sc) => {
        const on = state.scenario && state.scenario.id === sc.id;
        return el("button", {
            class: "tb-port" + (on ? " chosen" : ""),
            "data-scn": sc.id,
            title: sc.name,
            onclick: () => verrouillerCible(sc),
            onmouseenter: () => rendreSceneMechant(sc),
            onmouseleave: () => rendreSceneMechant(state.scenario),
        },
            portraitScenario(sc),
            el("span", { class: "tb-port-nom" }, sc.name),
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

/* ---- Étape 4, le face à face : la splash page -------------------------------
   L'écran est coupé en diagonale, notre camp à gauche sur fond clair, le
   méchant à droite sur fond sombre, chacun en art plein cadre. L'étoile VS est
   posée sur la coupe. Les réglages de la partie sont en tampons sous les noms,
   et le bloc « Avancé » reste replié dans le coin. */
/** Un sous-titre qui répète son titre ne dit rien : on l'efface. */
function sousTitre(texte, titre) {
    const propre = String(texte || "").trim();
    return propre && propre.toLowerCase() !== String(titre || "").trim().toLowerCase() ? propre : "";
}

function stepSummary() {
    const v = validate(state);
    const sc = state.scenario;
    const d = state.difficulty;

    const scene = (idImage, classe) => el("div", {
        class: "fo-scene " + (classe || ""),
        style: { backgroundImage: `url("${cardImageUrl(idImage)}")` },
        onmouseenter: (e) => showCardHover(idImage, e.currentTarget),
        onmouseleave: scheduleHide,
    });

    const heros = el("div", { class: "fo-cards" });
    for (let i = 0; i < state.playerCount; i++) {
        const p = state.players[i];
        heros.append(p.hero
            ? el("div", { class: "fo-card" },
                scene(picIdHeros(p.hero.heroCardId)),
                el("div", { class: "fo-cap" }, nomAffiche(p.hero),
                    el("span", {}, sousTitre(p.deck ? cleanNomDeck(p.deck.name) : t("Deck à choisir"), nomAffiche(p.hero)))),
            )
            : el("div", { class: "fo-empty" }, t("Joueur") + " " + (i + 1)));
    }

    const cartesVilain = sc
        ? ((sc.villainCards && sc.villainCards.length) ? sc.villainCards : [sc.tileImage].filter(Boolean))
        : [];
    const vilain = el("div", { class: "fo-cards villain-cards" });
    (cartesVilain.length ? cartesVilain : [null]).forEach((id) => vilain.append(id
        ? el("div", { class: "fo-card villain" }, scene(id, "villain"))
        : el("div", { class: "fo-empty" }, "?")));

    const reglages = [];
    if (sc) {
        reglages.push(libelleMode(state.mode) + " · " + state.playerCount + (state.playerCount > 1 ? " héros" : " héros"));
        reglages.push(d.base === "expert" ? "Expert" : "Standard");
        if (d.skirmish) reglages.push("Skirmish");
        if (d.heroic > 0) reglages.push(t("Héroïque") + " " + d.heroic);
        const sets = [...sc.mandatoryEncounterSets, ...d.selectedModularSets].map(titleize);
        if (sets.length) reglages.push(sets.join(" · "));
    }

    return el("section", { class: "step face-a-face" },
        el("div", { class: "faceoff" + (state.playerCount > 2 ? " large" : "") },
            el("div", { class: "fo-side heroes-side" },
                heros,
                el("div", { class: "fo-reglages" },
                    ...reglages.map((x) => el("span", { class: "tampon" }, x))),
            ),
            el("div", { class: "fo-vs" },
                el("i", { class: "fo-eclat e1" }), el("i", { class: "fo-eclat e2" }),
                el("i", { class: "fo-eclat e3" }), el("i", { class: "fo-eclat e4" }),
                el("span", {}, "VS")),
            el("div", { class: "fo-side villain-side" },
                vilain,
                sc ? el("div", { class: "fo-nomg" }, sc.name) : el("div", { class: "fo-nomg" }, t("Méchant non défini")),
                sc ? el("div", { class: "fo-vsub" }, sousTitre(sc.villainNames.join(" · "), sc.name)) : null,
            ),
        ),
        !v.ok
            ? el("div", { class: "errors" },
                el("h3", { class: "mvl" }, t("À compléter")),
                ...v.errors.map((e) => el("div", { class: "err", onclick: () => goto(e.step) }, e.message + " >")))
            : null,
        blocAvance(),
    );
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
        }, picto("fa-random")),
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
