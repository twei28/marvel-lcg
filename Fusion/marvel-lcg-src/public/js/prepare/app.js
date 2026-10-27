// app.js - Assistant "Preparer une partie" : briefing Marvel Champions.
"use strict";
import { cardImageUrl, cardImageUrlEn, cardImageUrlHd, extensionImageUrl, oublierDecksSauvegardes } from "/public/js/prepare/api.js?v=564d4a13";
import { REPLIQUES, choisirReplique, classeTaille } from "./repliques-heros.js";
import { cards } from "/public/js/prepare/cards.js";
import { catalog, titleize, nomSetRencontre, titreDeVague } from "/public/js/prepare/catalog.js";
import { nomExtension, titreDeBoite } from "/public/js/prepare/titres-extensions.js";
import { validate } from "/public/js/prepare/validation.js";
import { launch } from "/public/js/prepare/launcher.js?v=99722e8b";
import { prefs } from "/public/js/prepare/prefs.js";
import { STANDARD, cleHeros, codeAlterEgoAffiche } from "/public/js/prepare/arts-heros-choix.js";
// Arts alternatifs des cartes de deck (TMNT) : la fenêtre « arts alternatifs ? » à la sélection d'un deck.
import { proposerArtsCartes } from "/public/js/prepare/arts-cartes-fenetre.js";
import { picIdDeCarte } from "/public/js/prepare/arts-cartes-stockage.js";
import { serieDuHeros } from "/public/js/prepare/arts-cartes-choix.js";
import { poserTraduction } from "/public/js/traduction/poser.js";
import { versionsDe, deckDeLaVersion, optionsDuHeros, cleIdentite, apercuVersion } from "/public/js/prepare/variantes.js";
import { regrouperUnderlings, faceB, scenarioDuVilain, tuileContient } from "/public/js/prepare/underlings.js";
import { aDeckDeBase } from "/public/js/prepare/catalog.js";
import { nomAvecAuteur, createursDeTout, auteurConnuDeLExtension } from "/public/js/prepare/auteur.js";
// LEGACY (13/09/2026) : la fiche du compte, et le verrou qui dit ce qui est
// ouvert. Tout le calcul vit dans ces modules ; ici on ne fait que lire.
import { etat as etatLegacy, activer as activerLegacy, acheter as acheterLegacy } from "/public/js/prepare/legacy-fiche.js";
import { fabriquerVerrou } from "/public/js/prepare/legacy-verrou.js";
import { fabriquerDisponibilite } from "/public/js/prepare/legacy-cartes.js";
// Panneau « Documents ». Importe ICI plutot que pose en balise dans
// prepare.html : deux URL differentes (avec et sans ?v=) chargeraient le
// module deux fois et poseraient deux boutons dans l'en-tete.
import { livretDExtension, carnetDExtension } from "/public/js/prepare/panneau-documents.js";
// Sons de l'interface. Ils ne se posent QUE sur des clics : les fonctions
// centrales (assignHero, selectScenario) sont aussi appelees a la reprise de
// session et par le tirage aleatoire, et un son s'y jouerait tout seul au
// chargement de la page.
import { jouerSon, jouerReplique, jouerClicRoue, SON, couperSurvolPendant } from "/public/js/prepare/sons.js";
// L'intention du survol des héros : la scène garde le héros regardé le temps d'atteindre son bouton « Voir ses cartes ».
import { creerSurvolHeros } from "/public/js/prepare/survol-heros.js";
import { voletCreateurs } from "/public/js/prepare/section-createurs.js";
import { herosTirables, scenariosTirables, tirer, tirerPlusieurs, creerBandeau, caseHeros, caseScenario,
         lireRoue, publierRoue } from "/public/js/prepare/roue.js";
import { boutonLangue, synchroniserLangueServeur, t, langueActuelle,
         langueDejaChoisie, retenirLangue, basculerLangue, enregistrerTraductions } from "/public/js/prepare/langue.js";
import { DICO_TEL_EN } from "/public/js/prepare/dico-tel-en.js";
import { estTel, suivreTel, installerHistorique, noterEcran, reculerVers,
         brancherBandeau, ajouterPoignee } from "/public/js/prepare/tel.js";
import { montrerTableFermee } from "/public/js/prepare/table-fermee.js";
import { ouvrirFeuille } from "/public/js/tel-pages.js";
import { affichageActuel, boutonAffichage, appliquerAffichage, synchroniserAffichage, choisirAffichage, epurePermis, verifierEpurePermis } from "/public/js/prepare/affichage.js";
import { CLE_MODE_PHASE, CLE_PHASE_MODE_VU, CLE_PHASE_CHOIX_VU, VERSION_CHOIX_PHASE, MODES as MODES_PHASE, normaliser as normaliserModePhase,
         doitProposerLeChoix as doitProposerLaPhase, doitProposerLeChoixSurAppareil as doitProposerLaPhaseSurAppareil, modeAEcrire as modePhaseAEcrire,
         CLE_JEU_AU_DOIGT, REQUETE_TABLETTE as REQUETE_TABLETTE_PHASE, estTablette as estTablettePhase, choixInitial as choixInitialPhase,
         migrerPhaseTroisChoix, PHASE_IMAGES_VISIBLES } from "/public/js/prepare/phase-mode-choix.js";
import { faconParDefaut, lanceEnManuel, AUTO as FACON_AUTO, MANUEL as FACON_MANUEL } from "/public/js/prepare/facon-de-jouer.js";
import { roueTeinte, teinteActuelle, choisirTeinte, synchroniserTeinte } from "/public/js/prepare/teinte.js";
// ⚠ MEME ADRESSE que la balise de prepare.html (`?v=1` compris) : une autre
// adresse chargerait le module une seconde fois.
import { appliquerTeintePage } from "/public/js/teinte-page.js?v=1";
import { sauverDeck, supprimerDeck, decksSauvegardesPourHeros } from "/public/js/prepare/decks-serveur.js";
import { NIVEAUX_STANDARD, libelleNiveau, niveauDuScenario } from "/public/js/prepare/niveau-standard.js";
import { proposerIntense, chargerTexteFr as texteIntenseFr, texteSansBalises, CARTE_INTENSE } from "/public/js/prepare/intense-combatants.js";
import { urlNarval } from "/public/js/prepare/narval.js";
import { DEFIS_INFO } from "/public/js/prepare/defis-info.js";
import { HEROS_INFO } from "/public/js/prepare/heros-info.js";
import { GENRES, nouveautesTriees } from "/public/js/prepare/nouveautes.js";
import { MECHANTS_INFO } from "/public/js/prepare/mechants-info.js";
import { etatSalon } from "/public/js/prepare/salon-etat.js";
import { appliquerTutoriel } from "/public/js/prepare/tutoriel-etat.js";
import { versDeckMoteur, ecartDeConversion } from "/public/js/marvelcdb/conversion.js";
import { chargerHeros } from "/public/js/marvelcdb/index.js";
import { chargerDeck, lireLien } from "/public/js/marvelcdb/sources.js";
import { lireO8d, versSlots, indexParNom } from "/public/js/marvelcdb/octgn.js";
import { demanderForcage } from "/public/js/prepare/deck-force.js";
import { filtrer, aspectsPresents, tagsPresents, aDesRangs } from "/public/js/marvelcdb/filtres.js";
import { lireFavoris, basculerFavori } from "/public/js/marvelcdb/favoris.js";
import { validerDeck, choisiesDuDeck } from "/public/js/deckbuilder/regles.js";
import { lireBrouillon, ecrireBrouillon } from "/public/js/campagne/brouillon.js";
import { marquerTablette } from "/public/js/tablette.js";

// Tablette (24/10/2026, decision 11) : <html data-tablette> et ses cibles de 44 px (css/tablette-pages.css).
marquerTablette();

// SURVOL : il n'existe pas sur un ecran tactile.
//
// Releve par l'utilisateur sur son telephone le 11/09/2026 : toucher une
// boite d'extension pour changer de vilain ouvrait sa grande fiche et ne la
// refermait JAMAIS. La boite changeait bien dessous, mais la fiche recouvrait
// l'ecran, alors « ca ne fonctionne pas ».
//
// Cause : un doigt declenche `mouseenter`, mais jamais `mouseleave` — il n'y
// a pas de curseur qui s'en va. Tout panneau ouvert au survol et referme a la
// sortie reste donc colle. `(hover: hover)` distingue les appareils qui ont un
// vrai survol ; lu une seule fois, au chargement.
const SANS_SURVOL = !window.matchMedia("(hover: hover)").matches;

/** Un gestionnaire de survol, ou rien du tout sur un ecran tactile. */
const auSurvol = (fn) => (SANS_SURVOL ? undefined : fn);

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
    // Le SIXIEME aspect. Le moteur peint ses cartes en rgb(38,38,44)
    // (image_creator.py), mais une pastille a #26262c serait indistinguable du
    // fond sombre de l'ecran : on garde la teinte et on monte la luminosite,
    // exactement comme le lisere du plateau (board.css). Une couleur, partout.
    venomized: "#6b6b7a",
};
// ⚠ `aide` : LA PHRASE QUI EXPLIQUE LE MODE, montrée au survol (et toujours
// visible sur un écran tactile, qui n'a pas de survol : voir `.acc-aide` dans
// prepare.css). Textes arrêtés avec l'utilisateur le 13/09/2026 : une phrase,
// pas deux, écrite pour quelqu'un qui ne connaît pas encore le jeu. Celle de
// Bataille reprend le nom que lui donne le livret (mc56 p.14, « competitive
// mode »).
const MODES = [
    { id: "solo", label: "Solo", desc: t("1 héros"), players: 1, fixed: true, mark: "1",
      aide: t("Tu joues un seul héros contre le méchant.") },
    { id: "hotseat", label: t("Coop locale"), desc: t("2 à 4 héros"), players: 2, min: 2, max: 4, mark: "4",
      aide: t("À plusieurs sur le même écran, ou seul avec plusieurs héros.") },
    { id: "campaign", label: t("Campagne"), desc: "Progression", players: 1, min: 1, max: 4, mark: "C",
      aide: t("Tu enchaînes les scénarios d'une boîte, dans l'ordre.") },
    // Bac a sable : partie normale (mêmes règles, mêmes choix), mais le plateau
    // démarre garni côté vilain et le panneau de triche s'ouvre à côté.
    { id: "sandbox", label: t("Bac à sable"), desc: t("Test des cartes"), players: 1, fixed: true, mark: "T",
      aide: t("Mêmes règles, mais tu poses et retires ce que tu veux.") },
    // Puzzle (24/10/2026, demande de l'utilisateur) : on cree un puzzle comme on lance une partie classique (heros, deck, mechant,
    // scenario), puis le plateau s'ouvre en EDITEUR : bac a sable + table manuelle, et un bouton « Enregistrer le puzzle ».
    // Resoudre un puzzle (par code, mes puzzles) reste dans le panneau « Puzzles » (puzzles.js).
    // `fixed` : pas de boutons de nombre sur la tuile ; le clic ouvre le panneau « Puzzles » (creer avec 1 a 4 heros, resoudre par code,
    // mes puzzles). Le panneau relance `partir` avec le nombre de heros (`window.creerPuzzle`).
    { id: "puzzle", label: t("Puzzle"), desc: t("Créer ou résoudre"), players: 1, min: 1, max: 4, fixed: true, mark: "P",
      aide: t("Crée un puzzle en arrangeant le plateau à ta main, ou résous celui d'un autre avec son code.") },
    // Bataille : le mode competitif de Civil War et Synthezoid Smackdown. Deux
    // equipes s'affrontent, chacune face au leader prepare par l'autre. Le
    // livret (mc56 p.14) n'en connait que deux formats, 1v1 et 2v2 : d'ou 2 ou
    // 4 joueurs, et le camp deduit du siege plutot que demande.
    { id: "bataille", label: t("Bataille"), desc: t("2 équipes, 1v1 ou 2v2"), players: 2, min: 2, max: 4, mark: "B",
      aide: t("Le mode compétitif de Civil War, joueurs contre joueurs.") },
    // Legacy (13/09/2026) : on commence avec la seule boîte de base et on ouvre
    // la suite en gagnant. Ce n'est pas un mode de jeu au sens du moteur : une
    // partie Legacy est une partie Solo ou Coop locale ordinaire, jouée sur
    // une grille VERROUILLÉE. `partir` pose `state.legacy` et bascule sur le
    // vrai mode selon le nombre de héros. Spec : .planning/todos/2026-09-13-mode-legacy.md
    { id: "legacy", label: "Legacy", desc: t("Boîte par boîte"), players: 1, min: 1, max: 4, mark: "L",
      aide: t("Tu commences avec la boîte de base et tu débloques la suite en gagnant.") },
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

/** `url` : la fonction qui donne l'image.
 *
 *  ⚠ L'ANGLAIS PAR DÉFAUT, MÊME EN FRANÇAIS (17/09/2026, demande de
 *  l'utilisateur). Le scan FR porte un filigrane qui salit l'illustration ;
 *  l'anglais non. Ces portraits sont là pour RECONNAÎTRE un personnage, pas
 *  pour lire son texte : c'est l'image qui compte, et les grandes scènes
 *  étaient déjà en anglais pour cette raison. Le français restait aux seules
 *  vignettes, d'où deux versions d'un même héros sur le même écran. */
function portrait(cardId, cls, url = cardImageUrlEn) {
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
function portraitDuo(hero, cls, url = cardImageUrlEn) {
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
/** MC×DC (22/10/2026) : la tuile montre la MANIGANCE ANNEXE (affaire), pas le vilain. Les cartes manigance sont EN PAYSAGE ; le serveur
 *  les sert tournees de 90° (cartes du jeu) : on les remet a l'endroit (rotation CSS dans un conteneur `cq`). null = pas une tuile d'affaire. */
function portraitAffaire(ext, sc) {
    if (!ext || !ext.tuileManigance) return null;
    const id = sc.interchangeable ? sc.tileImage : ((ext.tuileManiganceScenarios || []).includes(sc.id) ? faceB((sc.schemes || [])[0]) : "");
    if (!id) return null;
    return el("div", { class: "portrait pivote" }, el("i", { style: { backgroundImage: `url("${cardImageUrlEn(id)}")` } }));
}
function portraitScenario(sc, cls) {
    const ids = mechantsDe(sc);
    if (ids.length < 2) {
        return el("div", { class: "portrait " + (cls || ""), style: { backgroundImage: `url("${cardImageUrlEn(sc.tileImage)}")` } });
    }
    const n = Math.min(ids.length, 4);
    return el("div", { class: `portrait portrait-multi n${n} ` + (cls || "") },
        ...ids.slice(0, 4).map((id) => el("i", { style: { backgroundImage: `url("${cardImageUrlEn(id)}")` } })));
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
    const nom = hero.lie ? (cleanNomDeck(hero.deck && hero.deck.name) || hero.name) : hero.name;
    return nomAvecAuteur(nom, hero.auteur, hero.homebrew);
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
    // Parcours sequentiel : vrai quand on rouvre un heros depuis le recapitulatif.
    modifDeck: false,
    // homebrew : decoche = uniquement les heros officiels, coche = uniquement
    // les fan-made (Stan Lee, Hulk (Rainy), Thor (Jane Foster)).
    heroFilters: { q: "", vague: "", fav: false, homebrew: false },
    // Legacy : null hors du mode ; sinon { etat, verrou } (voir entrerLegacy).
    legacy: null,
    scenario: null,
    // Bataille : le scenario pose devant la SECONDE equipe. Chaque equipe
    // affronte celui apporte par l'autre (mc56 p.14, etape 4).
    scenario2: null,
    extensionTab: null,
    difficulty: {
        base: "standard",
        // Le NIVEAU du set Standard (I, II ou III). Axe SEPARE de `base`, qui
        // choisit la variante Expert du scenario : dans le jeu, Expert
        // s'AJOUTE au Standard, il ne le remplace pas (rhino_expert declare
        // ["standard", "expert"]). Voir niveau-standard.js.
        standard: "standard",
        skirmish: false,
        heroic: 0,
        modularConfig: "recommended",
        selectedModularSets: [],
        scenarioOptions: {},
        // te201 Intense Combatants, environnement OPTIONNEL des scenarios TMNT :
        // decoche par defaut (decision du 16/10/2026). Voir intense-combatants.js.
        intenseCombatants: false,
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
    // Façon de jouer de CETTE partie ; le défaut vient des Réglages du plateau.
    modeManuel: lanceEnManuel(faconParDefaut(window.localStorage)),
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

/**
 * COOP LOCALE : UN HEROS APRES L'AUTRE (backlog 9, 20/10/2026).
 * Vrai : a plusieurs heros sur le meme poste, chaque deck doit etre CHOISI
 * (un clic) puis VALIDE, heros par heros ; plus aucun deck de base n'est pose
 * d'office. Faux : l'ancien comportement (deck de base ou dernier deck utilise,
 * Continuer ouvert des l'arrivee). Les trois questions encore ouvertes
 * (retour arriere, recapitulatif, deck de base explicite) sont dans
 * `.planning/todos/2026-10-20-backlog-9-questions.md` ; le comportement actuel
 * est le plus simple de chacune.
 */
const COOP_DECKS_SEQUENTIELS = true;

/** Ce parcours s'applique-t-il ? Coop locale (2 a 4 heros, meme poste) ; ni solo,
 *  ni salon en ligne, ni creation d'equipe de campagne (decks deja fixes). */
function decksSequentiels() {
    return COOP_DECKS_SEQUENTIELS && state.playerCount > 1 && !enLigne() && !creationCampagne();
}

/** Le deck de ce siege est-il VALIDE ? (sans objet hors parcours sequentiel) */
function deckValide(p) { return !!(p && p.deck && p.deckValide); }

/** Le deck est-il montre comme choisi ? Hors parcours sequentiel, le deck pose
 *  par defaut compte ; en parcours sequentiel, seul un deck CLIQUE compte. */
function deckAffiche(p) {
    return !!(p && p.deck && (!decksSequentiels() || p.deckChoisi));
}

/** Le recapitulatif des decks est-il a l'ecran ? Tous les decks sont valides et
 *  aucun heros n'est rouvert par « Modifier ». */
function enRecap() {
    return decksSequentiels() && premierSiegeAValider() < 0 && !state.modifDeck;
}

/** Premier siege dont le deck n'est pas encore valide, ou -1. */
function premierSiegeAValider() {
    return activePlayers().findIndex((p) => !deckValide(p));
}

function stepComplete(step) {
    const active = activePlayers();
    switch (step) {
        // En multi, les sieges des invites sont remplis par le SALON : bloquer
        // la navigation dessus condamnerait l'hote a attendre sur l'ecran des
        // heros sans rien pouvoir faire. Seul son propre siege le retient ; le
        // LANCEMENT, lui, attend tout le monde (validate + salon.prete).
        case 0: return !!state.mode && (enLigne() ? !!active[0] && !!active[0].hero : active.every((p) => p.hero));
        case 1:
            if (decksSequentiels()) return active.every(deckValide);
            return enLigne() ? !!active[0] && !!active[0].deck : active.every((p) => p.deck);
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
    if (state.step === 0 && !creationCampagne()) {
        if (reculerVers("accueil")) return;
        hideHover(); state.accueil = true; render(); return;
    }
    if (reculerVers("e" + (state.step - 1))) return;
    goto(state.step - 1);
};

async function randomize() {
    if (state.step === 0) {
        const tous = await catalog.heroes();
        // Legacy : le hasard ne pioche que dans ce qui est débloqué.
        const heroes = state.legacy ? tous.filter((h) => state.legacy.verrou.heros(h).ouvert) : tous;
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
        if (estBataille()) {
            const tous = await catalog.scenariosForExtension(state.extensionTab);
            const scs = state.legacy ? tous.filter((sc) => state.legacy.verrou.scenario(sc).ouvert) : tous;
            if (scs.length) selectScenario(rnd(scs));
        } else if (!isCampaignMode()) {
            // TOUTES LES BOÎTES (décision 11 de la roue, 08/10/2026) : le tirage
            // ne se limite plus à l'onglet ouvert, et suit la case « fan-made »
            // de la roue. En Legacy, c'est le verrou qui fait le tri.
            const verrou = state.legacy ? state.legacy.verrou : null;
            const pool = scenariosTirables(await catalog.tousLesScenarios(),
                { fanmade: state.legacy ? true : roueFanmade(), verrou });
            const sc = tirer(pool, { exclus: state.scenario ? [state.scenario.id] : [] });
            if (sc) {
                state.extensionTab = sc.extension;
                selectScenario(sc);
            }
        }
        render();
    }
}

function assignHero(slotIndex, hero) {
    const p = state.players[slotIndex];
    p.hero = hero;
    // Modale du héros (11/09/2026) : le dernier choix fait pour ce héros sur
    // cet appareil est repris d'office (version du deck, identité). Une
    // version disparue retombe sur la base, jamais sur un clic cassé.
    const memoire = prefs.variantes(hero.id);
    p.version = (memoire.version && versionsDe(hero).some((v) => v.id === memoire.version)) ? memoire.version : hero.id;
    p.deck = deckDeLaVersion(hero, p.version);
    p.identity = memoire.identite
        ? ((hero.variants || []).find((v) => cleIdentite(v) === memoire.identite) || null)
        : null;
    p.deckSource = "base";
    // Deck posé automatiquement : l'étape Decks pourra le remplacer par le
    // dernier deck utilisé pour ce héros (mémoire des choix).
    p.deckAuto = true;
    // Parcours sequentiel : un nouveau heros repart sans deck choisi ni valide.
    p.deckChoisi = false;
    p.deckValide = false;
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
        // ⚠ ET L'IDENTITE REPART A ZERO (21/09/2026). `identity` est l'identite
        // ALTERNATIVE choisie a l'etape des decks ; `launcher.js` la prefere au
        // heros du deck (`hero: (p.identity && p.identity.hero) || p.deck.hero`).
        // Laissee en place, celle d'un heros precedent partait au moteur sans
        // que personne ne l'ait choisie — et depuis que le salon verifie que son
        // siege tient bien SON heros, l'invite ne s'y reconnaitrait plus et
        // resterait dehors. Un choix venu du salon n'a jamais d'identite
        // alternative : le salon n'en propose pas.
        joueur.identity = null;
    }
}

// ⚠ LE SONDAGE DU SALON ETAIT LE PREMIER CONSOMMATEUR DU SERVEUR (16/09/2026).
// Mesure sur les journaux de Caddy, 3,2 heures : `/get_choix_sieges` pesait
// 5917 requetes, soit 61 % de TOUT le trafic vers les tables, et une toutes
// les deux secondes par client — y compris en solo, y compris onglet cache,
// y compris quand rien ne bouge. A cent joueurs, cela ferait cinquante
// requetes par seconde, chacune reveillant un processus Python, pour apprendre
// que rien n'a change.
//
// ⚠ ET CELA EMPECHAIT LES TABLES DE S'ETEINDRE. Le faucheur juge l'inactivite
// sur la date du journal du moteur ; ces appels l'ecrivaient sans arret. Un
// onglet oublie faisait vivre une table jusqu'au minuteur des huit heures.
//
// Trois regles, donc : rien quand personne ne regarde, vite quand on attend
// quelqu'un, lentement le reste du temps.
export const SONDAGE_ATTENTE_MS = 2000;
export const SONDAGE_CALME_MS = 15000;
// Table declaree fermee : on ne martele plus, mais on ne renonce pas non plus.
// Un redemarrage du site rend la table joignable au bout de quelques secondes,
// et le bandeau doit alors s'effacer tout seul — d'ou ce battement lent.
export const SONDAGE_INJOIGNABLE_MS = 30000;

/** Le delai avant le prochain sondage, ou 0 pour « ne sonde pas ».
 *
 *  Fonction PURE et exportee : c'est la seule decision de cette boucle qu'on
 *  puisse eprouver sans faire tourner de minuteur. */
export function cadenceSondage({ cache, enAttente, injoignable }) {
    if (cache) return 0;
    if (injoignable) return SONDAGE_INJOIGNABLE_MS;
    return enAttente ? SONDAGE_ATTENTE_MS : SONDAGE_CALME_MS;
}

// Le temps qu'on laisse a une table avant de la declarer fermee. Un
// redemarrage du site coupe les tables une dizaine de secondes : en dessous de
// ce delai, on annoncerait une table morte qui revient, ce qui est pire que le
// silence d'aujourd'hui.
export const DELAI_TABLE_FERMEE_MS = 30000;

/** La table est-elle a declarer fermee ?
 *
 *  PURE, comme `cadenceSondage`, et pour la meme raison : c'est la decision
 *  qu'il faut pouvoir eprouver, pas le minuteur qui la porte. `premierEchec`
 *  est l'instant du premier sondage rate depuis le dernier qui a reussi, ou
 *  `null` quand tout va bien. */
export function tableFermee({ premierEchec, maintenant, delai = DELAI_TABLE_FERMEE_MS }) {
    if (!premierEchec) return false;
    return maintenant - premierEchec >= delai;
}

/** L'instant du premier sondage rate depuis le dernier qui a reussi. */
let premierEchecSondage = null;

/** Note le sort du dernier sondage et met le bandeau a jour.
 *
 *  ⚠ UN 502 N'EST PAS UNE EXCEPTION. `fetch` le rend comme une reponse
 *  normale ; c'est `res.json()` qui trebuchait ensuite sur la page d'erreur
 *  HTML de Caddy, et le `catch` muet effacait tout. On juge donc `res.ok`. */
function noterSondage(reussi) {
    if (reussi) premierEchecSondage = null;
    else if (premierEchecSondage === null) premierEchecSondage = Date.now();
    const fermee = tableFermee({ premierEchec: premierEchecSondage, maintenant: Date.now() });
    montrerTableFermee(fermee);
    return fermee;
}

/** Vrai quand la table est declaree fermee : la boucle s'en sert pour ralentir. */
function tableDeclareeFermee() {
    return tableFermee({ premierEchec: premierEchecSondage, maintenant: Date.now() });
}

async function sonderSalon() {
    let brut;
    try {
        const res = await fetch("get_choix_sieges?");
        if (!res.ok) throw new Error("HTTP " + res.status);
        brut = await res.json();
    } catch (e) {
        noterSondage(false);
        return;
    }
    noterSondage(true);
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
    // Web of Deceit joue Standard III : l'ecran doit le MONTRER, pas afficher
    // « Standard I » sur une partie qui n'en est pas une.
    state.difficulty.standard = niveauDuScenario(sc.rawJson);
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

/* ======================= MODE TÉLÉPHONE (< 768 px) ==========================
   Refonte du 09/10/2026 (.planning/todos/2026-10-09-mode-telephone-refonte.md).
   Au-dessus de 768 px, RIEN de ce bloc ne s'exécute : le PC reste identique.
   Les briques génériques (historique, bandeau, poignée) sont dans tel.js. */

/** La clé d'historique de l'écran affiché. */
function cleEcranTel() { return state.accueil ? "accueil" : "e" + state.step; }

function pileTelReinit() { /* la pile se reconstruit seule au prochain rendu */ }

/** Retour du système : on rejoue l'écran dont la clé est donnée. */
function appliquerCleTel(cle) {
    hideHover();
    if (cle === "accueil") state.accueil = true;
    else { state.accueil = false; state.step = Math.min(LAST_STEP, Math.max(0, parseInt(cle.slice(1), 10) || 0)); }
    render();
}

let menuTelOuvert = false;
/** L'héros qu'on regarde sans l'avoir choisi (toucher = aperçu, Choisir = valide). */
let herosApercuTel = null;
/** Idem pour le méchant : { sc, concret } ou null. */
let mechantApercuTel = null;

/** En-tête fin : logo, langue (un toucher), burger ; dessous, les étapes
 *  (sauf sur l'accueil, `etapes: false`). */
function enteteTel({ etapes = true } = {}) {
    document.title = t("Préparation de mission") + " — Marvel Champions";
    const fermer = () => { menuTelOuvert = false; majMenuTel(); };
    const lien = (href, libelle, icone) => el("a", { class: "tel-lien", href }, picto(icone), " ", t(libelle));
    const panneau = el("nav", { class: "tel-menu", id: "tel-menu", "aria-label": t("Menu") },
        el("button", { class: "tel-lien", type: "button", onclick: () => { fermer(); hideHover(); state.accueil = true; render(); } },
            picto("fa-home"), " ", t("Mode de jeu")),
        lien("/campagne.html", "Campagne", "fa-book"),
        lien("/galerie.html", "Galerie", "fa-th"),
        lien("/deck-builder.html", "Éditeur de deck", "fa-pencil"),
        boutonAffichage("btn ghost tel-affichage"),
    );
    const voile = el("div", { class: "tel-voile", id: "tel-voile", onclick: fermer });
    const entete = el("header", { class: "progress tel-entete" },
        el("div", { class: "tel-rang" },
            el("a", { class: "brand", href: "main", "aria-label": t("Accueil du jeu") },
                el("img", { class: "brand-narwhal", src: urlNarval(), alt: "NarwhalChampions" })),
            el("div", { class: "spacer" }),
            boutonLangue("btn ghost btn-langue tel-langue"),
            el("button", {
                class: "tel-burger", id: "tel-burger", type: "button",
                "aria-label": t("Menu"), "aria-expanded": menuTelOuvert ? "true" : "false",
                onclick: () => { menuTelOuvert = !menuTelOuvert; majMenuTel(); },
            }, picto("fa-bars")),
        ),
        !etapes ? null : el("div", { class: "steps tel-etapes" }, STEPS.map((label, i) => {
            const done = i < state.step && stepComplete(i);
            const cls = "pstep" + (i === state.step && !state.accueil ? " active" : "") + (done ? " done" : "");
            return el("button", { class: cls, onclick: () => { menuTelOuvert = false; gotoTel(i); } },
                el("span", { class: "pnum" }, done ? "✓" : String(i + 1)),
                el("span", { class: "plabel" }, label));
        })),
        voile,
        panneau,
    );
    // Les outils annexes (Reprendre, Stats, Documents, Bug...) vivent dans le
    // menu : le nœud est vivant, on le DÉPLACE (écouteurs conservés).
    const rangee = document.querySelector(".reprise-boutons");
    if (rangee) {
        rangee.classList.remove("est-flottante");
        rangee.querySelectorAll(".btn-langue, .btn-affichage").forEach((n) => n.remove());
        panneau.append(rangee);
    }
    majMenuTel(entete);
    return entete;
}

function majMenuTel(entete) {
    const racine = entete || document.querySelector(".tel-entete");
    if (!racine) return;
    racine.classList.toggle("menu-ouvert", menuTelOuvert);
    const b = racine.querySelector("#tel-burger");
    if (b) b.setAttribute("aria-expanded", menuTelOuvert ? "true" : "false");
}

/** Une étape cliquée dans la barre : en arrière, on recule dans l'historique. */
function gotoTel(i) {
    if (i < state.step && i === state.step - 1 && reculerVers("e" + i)) return;
    goto(i);
}

/**
 * Parcours sequentiel : valide le deck du siege actif, puis passe au heros
 * suivant (ou rend la main a « Continuer » apres le dernier).
 */
function validerDeckSiege() {
    const p = state.players[state.activeSlot];
    if (p && p.deckChoisi) p.deckValide = true;
    const k = premierSiegeAValider();
    if (k >= 0) state.activeSlot = k;
    else state.modifDeck = false;   // tout est valide : retour au recapitulatif
    rendreSceneDeck(); rendreOutilsDeck(); rendreEquipe();
    loadDecks(state.activeSlot);
    majNav();
}

/** Heros suivant, sans rien valider (le deck du siege actif l'est deja). */
function heroSuivantSequentiel() {
    const k = premierSiegeAValider();
    if (k < 0) return;
    state.activeSlot = k;
    rendreSceneDeck(); rendreOutilsDeck(); rendreEquipe();
    loadDecks(k);
    majNav();
}

/** Le bouton de l'etape Decks en parcours sequentiel, ou null quand tous les
 *  decks sont valides (alors c'est « Continuer »). */
function boutonDeckSequentiel() {
    if (state.step !== 1 || !decksSequentiels()) return null;
    if (premierSiegeAValider() < 0) {
        if (!state.modifDeck) return null;
        return el("button", {
            class: "btn primary", id: "btn-retour-recap",
            onclick: () => { state.modifDeck = false; rendreSceneDeck(); rendreOutilsDeck(); rendreEquipe(); loadDecks(state.activeSlot); majNav(); },
        }, t("Retour au récapitulatif"));
    }
    const p = state.players[state.activeSlot];
    const nom = p && p.hero ? nomAffiche(p.hero) : "";
    if (deckValide(p)) {
        return el("button", {
            class: "btn primary", id: "btn-heros-suivant",
            onclick: () => { jouerSon(SON.etapeSuivante); heroSuivantSequentiel(); },
        }, t("Héros suivant"));
    }
    return el("button", {
        class: "btn primary", id: "btn-valider-deck",
        disabled: !(p && p.deckChoisi) || undefined,
        title: p && p.deckChoisi ? undefined : t("Un deck doit d'abord être choisi"),
        onclick: () => { jouerSon(SON.etapeSuivante); validerDeckSiege(); },
    }, t("Valider le deck de") + " " + nom);
}

/** Le bouton principal de la barre du bas : Continuer, Valider ou Lancer. */
function boutonPrincipalNav() {
    const seq = boutonDeckSequentiel();
    if (seq) return seq;
    return state.step < LAST_STEP
        ? el("button", {
            class: "btn primary",
            disabled: !canContinue() || undefined,
            onclick: () => { jouerSon(SON.etapeSuivante); next(); },
        }, t("Continuer"))
        : creationCampagne()
            ? el("button", {
                class: "btn launch",
                disabled: !stepComplete(1) || undefined,
                onclick: validerEquipeCampagne,
            }, BROUILLON_CAMPAGNE.modifie ? t("Valider les decks") : t("Valider l'équipe"))
            : el("button", {
                class: "btn launch",
                disabled: (!validate(state).ok || (enLigne() && !state.salon.prete)) || undefined,
                onclick: () => { jouerSon(SON.lancement); doLaunch(); },
            }, t("Lancer la partie"));
}

/** Barre du bas : les pastilles de l'équipe, puis Retour, Aléatoire, Continuer. */
function navBarTel() {
    const showRandom = [0, 2].includes(state.step);
    return el("footer", { class: "nav tel-nav" },
        state.step <= 2 ? el("div", { class: "tel-equipe-rang" },
            el("div", { class: "tb-equipe", id: "tb-equipe" }),
            el("div", { class: "nav-status" }, navStatus())) : el("div", { class: "nav-status" }, navStatus()),
        el("div", { class: "tel-actions" },
            el("button", {
                class: "btn ghost tel-retour", "aria-label": t("Retour"),
                disabled: (state.step === 0 && creationCampagne()) || undefined,
                onclick: () => { jouerSon(SON.etapePrecedente); prev(); },
            }, picto("fa-chevron-left")),
            showRandom
                ? el("button", { class: "btn ghost", onclick: () => { jouerSon(SON.aleatoire); randomize(); } },
                    picto("fa-random"), " ", t("Aléatoire"))
                : null,
            boutonPrincipalNav(),
        ),
    );
}

/** Remplace la barre du bas (Continuer s'allume sans reconstruire l'écran). */
function majNav() {
    document.querySelectorAll(".tb-mode").forEach((s) => { s.textContent = navStatus(); });
    const nav = document.querySelector(".nav");
    if (!nav) return;
    nav.replaceWith(navBar());
    if (estTel() && state.step <= 2) {
        if (state.step === 2) rendreTable(); else rendreEquipe();
    }
}

/** Dans le bandeau : le contenu commun aux trois étapes. `art` est le nœud
 *  d'image, `actions` les boutons (Choisir en premier). */
function poserBandeauTel(scene, { art, titre, sous, tampons, actions }) {
    poser(scene,
        art,
        el("div", { class: "tb-trame" }),
        el("div", { class: "ts-contenu" },
            el("div", { class: "ts-tampons" }, ...(tampons || [])),
            el("div", { class: "ts-ligne" },
                el("div", { class: "ts-titre" },
                    el("b", { class: "mvl" }, titre),
                    sous ? el("small", {}, sous) : null),
                el("div", { class: "ts-actions" }, ...(actions || []).filter(Boolean)),
            ),
        ),
    );
}

const boutonBandeau = (libelle, classe, action, icone) => el("button", {
    type: "button", class: "ts-btn " + classe, onclick: action,
}, icone ? picto(icone) : null, icone ? " " : null, libelle);

/** La feuille « Fiche » : l'essentiel d'un héros ou d'un méchant. */
function feuilleTel(classe, ...contenu) {
    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) fermerModale(overlay); } },
        el("div", { class: "deck-modal-panel vh-panel " + classe }, ...contenu));
    ouvrirModale(overlay);
    return overlay;
}

/** Une carte en grand, dans une feuille basse (toucher sur une vignette). */
function ouvrirCarteGrande(id) {
    const overlay = feuilleTel("carte-grande",
        el("img", { class: "cg-image", src: cardImageUrlHd(id), alt: "", onclick: () => fermerModale(overlay) }));
}

/** Le bandeau du héros (étape 1). `h` : le héros montré, `choisi` : s'il est posé. */
function rendreSceneTel(h) {
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    if (!h) {
        poserBandeauTel(scene, {
            art: el("div", { class: "tb-art vide" }),
            titre: t("Choisis un héros"),
            sous: t("Siège") + " " + (state.activeSlot + 1),
        });
        return;
    }
    const siege = siegeDuHeros(h);
    const choisi = activePlayers().some((p) => p.hero && p.hero.id === h.id);
    const traits = [...new Set([...(h.traits || []), ...(h.traitsAlterEgo || [])])].slice(0, 3).join(" · ");
    const options = optionsDuHeros(h, contexteVariantes(h));
    poserBandeauTel(scene, {
        art: h.lie
            ? el("div", { class: "tb-art" }, portraitDuo(h, "", cardImageUrlHd))
            : el("div", { class: "tb-art", style: { backgroundImage: `url("${cardImageUrlHd(picIdHeros(h.heroCardId))}")` } }),
        titre: nomAffiche(h),
        sous: traits,
        tampons: [
            pvAffiches(h) ? el("span", { class: "tampon jaune" }, t("PV") + " " + pvAffiches(h)) : null,
            h.handSize != null ? el("span", { class: "tampon" }, t("Main") + " " + h.handSize) : null,
        ],
        actions: [
            choisi
                ? boutonBandeau(t("Choisi"), "jaune est-choisi", () => {}, "fa-check")
                : boutonBandeau(t("Choisir"), "jaune", () => recruterVraiment(h, null)),
            choisi && !options.aucune
                ? boutonBandeau(t("Art"), "", () => ouvrirModaleVariantes(siege, h), "fa-eye") : null,
            boutonBandeau(t("Fiche"), "", () => ouvrirFicheHeros(h, null), "fa-info"),
        ],
    });
}

/** Le bandeau des decks (étape 2). */
function rendreSceneDeckTel() {
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    const p = state.players[state.activeSlot];
    const h = p && p.hero;
    if (!h) {
        poserBandeauTel(scene, { art: el("div", { class: "tb-art vide" }), titre: t("Aucun héros"), sous: t("Arsenal") });
        return;
    }
    const st = deckAffiche(p) ? deckStats(p.deck) : null;
    const aspects = st ? Object.keys(st.asp).filter((x) => x !== "basic") : [];
    const options = optionsDuHeros(h, contexteVariantes(h));
    poserBandeauTel(scene, {
        art: h.lie
            ? el("div", { class: "tb-art" }, portraitDuo(h, "", cardImageUrlHd))
            : el("div", { class: "tb-art", style: { backgroundImage: `url("${cardImageUrlHd(picIdHeros(h.heroCardId))}")` } }),
        titre: nomAffiche(h),
        sous: p.deck ? cleanNomDeck(p.deck.name) : t("Deck de base"),
        tampons: [
            st ? el("span", { class: "tampon" }, st.total + " " + t("cartes")) : null,
            ...aspects.map((x) => el("span", { class: "tampon aspect", style: { background: ASPECTS[x] || "#555", borderColor: "#111" } }, x)),
        ],
        actions: [
            options.aucune ? null : boutonBandeau(t("Art"), "jaune", () => ouvrirModaleVariantes(state.activeSlot, h), "fa-eye"),
            p.deck ? boutonBandeau(t("Cartes"), "", () => showDeckCards(p.deck, h, null), "fa-th") : null,
        ],
    });
}

/** Le bandeau du méchant (étape 3). `sc` : le scénario montré (concret). */
function rendreSceneMechantTel(sc) {
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    if (!sc) {
        poserBandeauTel(scene, { art: el("div", { class: "tb-art vide" }), titre: t("Choisis un méchant"), sous: t("Méchant") });
        return;
    }
    const carte = cards.get((sc.villainCards || [])[0] || sc.tileImage);
    const d = (carte && carte.desc) || {};
    const pv = String(d.HP || "").replace("*", "");
    const parJoueur = String(d.HP || "").includes("*");
    const apercu = mechantApercuTel;
    const choisi = !!state.scenario && state.scenario.id === sc.id;
    poserBandeauTel(scene, {
        art: el("div", { class: "tb-art", style: { backgroundImage: `url("${cardImageUrlHd(sc.tileImage)}")` } }),
        titre: sc.name,
        sous: nomExtension(sc.extension, langueActuelle()),
        tampons: [
            pv ? el("span", { class: "tampon rouge" }, t("PV") + " " + pv + (parJoueur ? " / " + t("joueur") : "")) : null,
            d.ATK ? el("span", { class: "tampon" }, t("ATQ") + " " + d.ATK) : null,
            d.SCH ? el("span", { class: "tampon" }, t("MEN") + " " + d.SCH) : null,
        ],
        actions: [
            choisi
                ? boutonBandeau(t("Choisi"), "jaune est-choisi", () => {}, "fa-check")
                : boutonBandeau(t("Choisir"), "jaune", () => choisirMechantTel(apercu || { sc, concret: sc })),
            boutonBandeau(t("Fiche"), "", () => ouvrirFicheMechant(sc), "fa-info"),
        ],
    });
}

function choisirMechantTel({ sc, concret }) {
    const plusieurs = sc.interchangeable && sc.underlings && sc.underlings.length > 1;
    if (plusieurs) ouvrirModaleUnderling(sc);
    else verrouillerCible(concret);
}

function ouvrirFicheMechant(sc) {
    const overlay = feuilleTel("fiche-heros fiche-mechant",
        el("div", { class: "fh-art", style: { backgroundImage: `url("${cardImageUrlHd(sc.tileImage)}")` } }),
        el("div", { class: "dm-head" },
            el("b", { class: "mvl" }, sc.name),
            el("span", { class: "dm-sub" }, nomExtension(sc.extension, langueActuelle()))),
        regleDuDefi(sc),
        bioDepliee_(bioDuMechant(sc)),
        documentsDeLaCible(sc),
        el("div", { class: "vh-actions" },
            el("button", { class: "tampon jaune", onclick: () => fermerModale(overlay) }, t("Fermer"))),
    );
}

/** La feuille d'import marvelcdb : champ, Import, Decks MarvelCDB. */
function ouvrirFeuilleImport(i) {
    const overlay = feuilleTel("feuille-import",
        el("div", { class: "dm-head" }, el("b", { class: "mvl" }, t("Importer un deck"))),
        el("input", { class: "search tb-search", id: "mcdb-" + i, placeholder: t("Colle une URL ou un ID marvelcdb ou mc4db...") }),
        el("span", { class: "mcdb-status", id: "mcdb-st-" + i }),
        el("div", { class: "vh-actions" },
            el("button", { class: "tampon", onclick: () => { fermerModale(overlay); ouvrirPanneauCdb(i); } }, t("Decks MarvelCDB")),
            el("button", { class: "tampon", onclick: () => document.getElementById("o8d-" + i).click() }, t("Fichier OCTGN (.o8d)")),
            el("button", { class: "tampon jaune", onclick: async () => { if (await doImport(i)) fermerModale(overlay); } }, t("Import")),
        ),
        el("input", {
            type: "file", id: "o8d-" + i, accept: ".o8d,.xml,text/xml", hidden: true,
            onchange: async (e) => {
                const f = e.target.files && e.target.files[0]; e.target.value = "";
                if (f && (await doImport(i, f))) fermerModale(overlay);
            },
        }),
    );
}

function render() {
    if (state.accueil && estTel()) {
        // Téléphone (zone 2 de la refonte du 09/10/2026) : l'en-tête fin, sans
        // les étapes, puis le gros bouton Jouer et les vignettes.
        document.title = t("Préparation de mission") + " — Marvel Champions";
        root.replaceChildren(
            enteteTel({ etapes: false }),
            el("div", { class: "layout accueil-layout" },
                el("main", { class: "stage accueil-stage" }, accueilView()),
            ),
        );
    } else if (state.accueil) {
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
        // FR / EN, MÊME SANS EN-TÊTE.
        // ⚠ C'est ICI que la question de la langue est posée à la première
        // connexion, et sa modale PROMET « tu peux changer à tout moment : le
        // bouton FR / EN, en haut de l'écran ». Sans en-tête, ce bouton
        // n'existait nulle part sur cet écran : le joueur fermait la modale et
        // ne trouvait rien. Signalé par l'utilisateur le 14/09/2026.
        // Il rejoint la rangée flottante, celle que ce commentaire décrit
        // justement comme l'abri des outils quand l'en-tête est absent.
        if (rangee && !rangee.querySelector(".btn-langue")) {
            rangee.prepend(boutonLangue("btn ghost btn-langue"));
        }
        // Le réglage d'affichage suit le bouton de langue, ici comme dans l'en-tête.
        if (rangee && !rangee.querySelector(".btn-affichage")) {
            rangee.querySelector(".btn-langue").after(boutonAffichage("btn ghost"));
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
    root.classList.toggle("tel-assistant", estTel() && !state.accueil);
    if (estTel() && !state.accueil) brancherBandeau();
    noterEcran(cleEcranTel());
    fixMarvelText();
    ajusterGrilles();
    surveillerGrilles();
    publierEquipeHote();
}

/** Dit au salon des invités qui joue quoi, SANS les decks (route gardée côté
 *  serveur, voir `set_equipe_hote`). Les sièges des invités se publient d'eux
 *  mêmes : on ne donne ici que ceux que l'hôte a posés. L'empreinte évite de
 *  réémettre à chaque rendu. */
let derniereEquipePubliee = "";
function publierEquipeHote() {
    if (!enLigne() || state.accueil) return;
    const heros = {};
    activePlayers().forEach((p, i) => {
        if (p.hero && !p.duSalon) heros[String(i)] = p.hero.heroCardId;
    });
    const corps = JSON.stringify({
        nombre: state.playerCount,
        heros,
        scenario: state.scenario ? state.scenario.id : "",
    });
    if (corps === derniereEquipePubliee) return;
    derniereEquipePubliee = corps;
    fetch("/set_equipe_hote", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: corps,
    }).then((r) => { if (!r.ok) derniereEquipePubliee = ""; }, () => { derniereEquipePubliee = ""; });
}

function progressBar() {
    if (estTel()) return enteteTel();
    // Le titre de l'onglet est ecrit en dur en ANGLAIS dans prepare.html, donc
    // faux des qu'on joue en francais. On le repose ici, ou t() existe.
    document.title = t("Préparation de mission") + " — Marvel Champions";
    const entete = el("header", { class: "progress" },
        el("a", { class: "brand", href: "main" },
            el("span", { class: "brand-back" }, "<"),
            el("span", { class: "brand-lockup logo" },
                // Le narval, mascotte du site (image de l'utilisateur, 13/09/2026),
                // a cote du logo officiel. Le meme sert d'icone d'onglet et
                // d'icone de l'appli sur telephone.
                // ⚠ SANS EXTENSION : le moteur sert les images par leur NOM
                // (server_files.py), en cherchant .webp/.jpg/.png dans les
                // dossiers d'images puis assets/textures. « /narwhal.png »
                // repondait 404 ; « /narwhal » trouve assets/textures/narwhal.png,
                // exactement comme « /01001a » trouve un scan de carte.
                el("img", { class: "brand-narwhal", src: urlNarval(), alt: "NarwhalChampions" }),
            ),
            // Le titre de la page, comme sur les autres pages (17/10/2026) : visible seulement
            // dans l'Épuré, où l'en-tête est le même partout.
            el("span", { class: "brand-titre" }, t("Préparation")),
        ),
        boutonLangue("btn ghost btn-langue"),
        boutonAffichage("btn ghost"),
        el("div", { class: "steps" }, STEPS.flatMap((label, i) => {
            const done = i < state.step && stepComplete(i);
            const cls = "pstep" + (i === state.step && !state.accueil ? " active" : "") + (done ? " done" : "");
            // Numerotees (demande du 09/10/2026), la coche remplace le numero d'une etape faite.
            const bouton = el("button", { class: cls, onclick: () => goto(i) },
                el("span", { class: "pnum" }, done ? "\u2713" : String(i + 1)),
                el("span", { class: "plabel" }, label));
            return i ? [el("span", { class: "psep", "aria-hidden": "true" }, "\u203a"), bouton] : [bouton];
        })),
    );
    // Adopte la rangee d'outils (Reprendre/Stats/Puzzles/Galerie) creee par
    // les scripts annexes : le header est reconstruit a chaque rendu, on
    // DEPLACE donc le noeud vivant (listeners conserves) a cote du bouton
    // langue plutot que de le laisser flotter par-dessus les etapes.
    const rangee = document.querySelector(".reprise-boutons");
    if (rangee) {
        rangee.classList.remove("est-flottante");
        // ⚠ LE FR/EN EN DOUBLE (16/09/2026, signalé sur capture : deux boutons
        // « EN » côte à côte). L'écran SANS en-tête pose son propre bouton de
        // langue dans cette rangée, parce que la modale du premier passage
        // promet « le bouton FR / EN, en haut de l'écran » et qu'il n'existait
        // nulle part là-bas. Mais la rangée est un nœud VIVANT, déplacé d'un
        // écran à l'autre : en revenant sur un écran AVEC en-tête, elle
        // apportait ce bouton juste à côté de celui que l'en-tête venait de
        // dessiner. On retire donc celui de la rangée ; l'écran sans en-tête
        // le reposera de lui-même au prochain passage.
        const langueEnTrop = rangee.querySelector(".btn-langue");
        if (langueEnTrop) langueEnTrop.remove();
        const affichageEnTrop = rangee.querySelector(".btn-affichage");
        if (affichageEnTrop) affichageEnTrop.remove();
        entete.insertBefore(rangee, entete.querySelector(".steps"));
    }
    return entete;
}

function navBar() {
    if (estTel()) return navBarTel();
    const showRandom = [0, 2].includes(state.step);
    return el("footer", { class: "nav" },
        el("button", {
            class: "btn ghost",
            disabled: (state.step === 0 && creationCampagne()) || undefined,
            onclick: () => { jouerSon(SON.etapePrecedente); prev(); },
        }, t("Retour")),
        el("div", { class: "nav-status" }, navStatus()),
        el("div", { class: "spacer" }),
        showRandom
            ? el("button", {
                class: "btn ghost",
                onclick: () => { jouerSon(SON.aleatoire); randomize(); },
            }, t("Aléatoire"))
            : el("span"),
        boutonDeckSequentiel() || (state.step < LAST_STEP
            ? el("button", {
                class: "btn primary",
                disabled: !canContinue() || undefined,
                onclick: () => { jouerSon(SON.etapeSuivante); next(); },
            }, t("Continuer"))
            : creationCampagne()
                ? el("button", {
                    class: "btn launch",
                    disabled: !stepComplete(1) || undefined,
                    onclick: validerEquipeCampagne,
                }, BROUILLON_CAMPAGNE.modifie ? t("Valider les decks") : t("Valider l'équipe"))
                : el("button", {
                    class: "btn launch",
                    disabled: (!validate(state).ok || (enLigne() && !state.salon.prete)) || undefined,
                    onclick: () => { jouerSon(SON.lancement); doLaunch(); },
                }, t("Lancer la partie"))),
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
        p.deckChoisi = true; p.deckValide = true;
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
    if (state.legacy) return "Legacy";
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
                jouerSon(SON.mode);
                if (tuile.distant !== null) state.coopEnLigne = tuile.distant;
                // La campagne n'est plus un mode du wizard : elle a son écran,
                // qui impose l'ordre des scénarios, les sets et la difficulté.
                if (m.id === "campaign") { window.location.href = "/campagne.html"; return; }
                const wasCampaign = isCampaignMode();
                state.mode = m;
                // Le catalogue de scénarios diffère en campagne : on repart d'une cible vierge.
                if ((m.id === "campaign") !== wasCampaign) state.scenario = null;
                state.playerCount = (m.fixed && m.id !== "puzzle") ? 1 : Math.max(m.min || 1, Math.min(m.max || 4, state.playerCount));
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

/* ---------------- Inviter un connecte (13/10/2026) ----------------
   Demande de l'utilisateur : a cote des liens, « Inviter quelqu'un de
   connecte ». Chaque siege libre propose les DEUX (decision 6) : un ami sans
   compte garde son lien. L'etat de chaque invite se suit en direct sous son
   nom (decision 4). Decisions : .planning/todos/2026-10-13-inviter-un-connecte.md.
   Tout passe par le moteur (get_connectes, post_inviter,
   get_invitations_envoyees), qui relaie au site et ne repond qu'au siege 0. */

const invitationsHote = {
    ouvert: false,
    actif: false,          // un site est-il derriere cette table ?
    connectes: [],
    envoyees: {},          // siege -> {invite, etat}
    choisi: {},            // siege -> pseudo selectionne dans la liste
    erreur: {},            // siege -> message
    empreinte: "",
    minuteur: null,
};

async function sonderInvitationsHote() {
    const avant = invitationsHote.empreinte;
    try {
        const r = await fetch("get_connectes?", { cache: "no-store" });
        const b = await r.json();
        invitationsHote.actif = !!(b && b.actif);
        invitationsHote.connectes = Array.isArray(b && b.connectes) ? b.connectes : [];
    } catch (e) { /* table muette : on garde ce qu'on avait */ }
    try {
        const r = await fetch("get_invitations_envoyees?", { cache: "no-store" });
        const b = await r.json();
        invitationsHote.envoyees = (b && b.sieges) || {};
    } catch (e) { /* idem */ }
    // ⚠ ON NE REPEINT QUE SI QUELQUE CHOSE A CHANGE : `render()` reconstruit
    // tout l'assistant, et une liste deroulante ouverte se refermerait sous les
    // doigts de l'hote toutes les trois secondes.
    invitationsHote.empreinte = JSON.stringify([invitationsHote.actif, invitationsHote.connectes, invitationsHote.envoyees]);
    if (invitationsHote.empreinte !== avant) render();
}

function boucleInvitationsHote() {
    clearTimeout(invitationsHote.minuteur);
    const suivant = () => {
        invitationsHote.minuteur = setTimeout(async () => {
            if (!invitationsHote.ouvert) return;
            if (!document.hidden) await sonderInvitationsHote();
            suivant();
        }, 3000);
    };
    suivant();
}

async function ouvrirInvitations() {
    invitationsHote.ouvert = true;
    // Les cles servent aux liens ET disent au moteur qu'on monte une table
    // ordinaire (`table_ordinaire`, voir get_liens_sieges).
    if (!liensInvites.cles) await genererLiens();
    await sonderInvitationsHote();
    render();
    boucleInvitationsHote();
}

async function inviterAuSiege(p, pseudo) {
    invitationsHote.erreur[p] = "";
    if (!pseudo) return;
    try {
        const r = await fetch("post_inviter", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ a: pseudo, siege: p }),
        });
        if (!r.ok) invitationsHote.erreur[p] = t("Invitation impossible : ce joueur n’est plus connecté.");
    } catch (e) {
        invitationsHote.erreur[p] = t("Invitation impossible : ce joueur n’est plus connecté.");
    }
    invitationsHote.empreinte = "";
    await sonderInvitationsHote();
    render();
}

/** Ce que l'hote lit sous le siege `p` : {texte, classe, relancer}. Null : siege libre. */
function etatDuSiege(p) {
    const inv = invitationsHote.envoyees[String(p)];
    const choix = state.salon.choixParSiege.get(p);
    const joueur = state.players[p];
    const qui = inv ? inv.invite + " · " : "";
    if (choix && joueur && joueur.hero) {
        return { texte: `${qui}${joueur.hero.name} · ${t("prêt")}`, classe: "est-pret" };
    }
    if (!inv) return null;
    if (inv.etat === "envoyee") return { texte: `${qui}${t("Invité…")}`, classe: "est-attente" };
    if (inv.etat === "acceptee") return { texte: `${qui}${t("A rejoint · choisit son héros")}`, classe: "est-attente" };
    if (inv.etat === "refusee") return { texte: `${qui}${t("A refusé")}`, classe: "est-refus", relancer: inv.invite };
    return { texte: `${qui}${t("Sans réponse")}`, classe: "est-refus", relancer: inv.invite };
}

function ligneDuSiege(p) {
    const url = lienDuSiege(p);
    const etat = etatDuSiege(p);
    const boutonCopier = el("button", {
        class: "liens-copier" + (liensInvites.copie === p ? " ok" : ""),
        title: url,
        onclick: async () => {
            try {
                await navigator.clipboard.writeText(url);
                liensInvites.copie = p;
            } catch (e) {
                // Presse-papier refuse : le lien reste lisible dans la bulle.
                liensInvites.copie = -1;
                window.prompt(t("Copie ce lien :"), url);
            }
            render();
        },
    }, liensInvites.copie === p ? t("Copié") : t("Copier le lien"));

    // Siege occupe ou en attente de reponse : l'etat, et rien a choisir.
    const libre = !etat || etat.relancer;
    const inviter = [];
    if (libre && invitationsHote.actif) {
        const proposes = invitationsHote.connectes;
        const choisi = invitationsHote.choisi[p] || (etat && etat.relancer) || "";
        const liste = el("select", {
            class: "invit-liste",
            onchange: (ev) => { invitationsHote.choisi[p] = ev.target.value; },
        },
            el("option", { value: "" }, proposes.length ? t("Choisir un joueur connecté") : t("Personne n’est connecté")),
            ...proposes.map((pseudo) => el("option", { value: pseudo, selected: pseudo === choisi }, pseudo)));
        inviter.push(liste, el("button", {
            class: "liens-bouton invit-bouton",
            disabled: !proposes.length,
            onclick: () => inviterAuSiege(p, invitationsHote.choisi[p] || choisi),
        }, etat && etat.relancer ? t("Réinviter") : t("Inviter")));
    }
    return el("div", { class: "liens-ligne invit-ligne" },
        el("span", { class: "liens-qui" }, t("Joueur") + " " + (p + 1)),
        etat ? el("span", { class: "invit-etat " + etat.classe }, etat.texte) : null,
        ...inviter,
        // Un siege deja pris n'a plus besoin de son lien.
        etat && !etat.relancer ? null : boutonCopier,
        invitationsHote.erreur[p] ? el("small", { class: "liens-erreur" }, invitationsHote.erreur[p]) : null,
    );
}

function blocLiens() {
    // A un seul heros il n'y a personne a inviter : le bouton mentirait.
    if (state.playerCount < 2) return null;

    if (!invitationsHote.ouvert) {
        return el("div", { class: "liens-invites" },
            el("div", { class: "invit-entrees" },
                el("button", { class: "liens-bouton", onclick: ouvrirInvitations }, t("Créer des liens")),
                el("button", { class: "liens-bouton", onclick: ouvrirInvitations }, t("Inviter quelqu’un de connecté"))),
            liensInvites.erreur
                ? el("small", { class: "liens-erreur" }, liensInvites.erreur)
                : null,
        );
    }

    const bloc = el("div", { class: "liens-invites ouvert" });
    // Un siege par INVITE, et le nombre suit celui des heros choisis : le
    // siege 0 est celui de l'hote, deja devant son ecran.
    for (let p = 1; p < state.playerCount; p += 1) bloc.append(ligneDuSiege(p));
    bloc.append(el("small", { class: "liens-aide" },
        invitationsHote.actif
            ? t("Invite un joueur connecté, ou envoie un lien à un ami sans compte. Chacun choisit son héros et son deck de son côté.")
            : t("Un lien par personne, à envoyer. Chacun choisit son héros et son deck depuis le sien.")));
    if (liensInvites.erreur) bloc.append(el("small", { class: "liens-erreur" }, liensInvites.erreur));
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
        el("span", {}, t("Choisis seulement TON héros et TON deck. Les autres joueurs choisissent les leurs de leur côté, par ton lien ou ton invitation.")),
        el("ul", { class: "salon-sieges" }, ...lignes),
    );
}

/** « Dans quelle langue veux-tu tes cartes ? », posée une seule fois.
 *
 *  Demandée par l'utilisateur le 13/09/2026. Le jeu part en français pour tout
 *  le monde sans avoir rien demandé ; ceux qui préfèrent l'anglais ne savent
 *  pas forcément que le bouton FR/EN existe.
 *
 *  ⚠ ELLE DIT QU'ON PEUT CHANGER, et le montre : la phrase nomme le bouton
 *  FR/EN et sa place. Une question posée une fois sans porte de sortie
 *  inquiète plus qu'elle n'aide.
 *
 *  ⚠ ET ELLE NE SE FERME PAS EN CLIQUANT À CÔTÉ, à la différence des autres
 *  modales de cet écran : un clic distrait vaudrait réponse, et la question ne
 *  reviendrait jamais. On répond par l'un des deux drapeaux, point.
 */
const CLE_DOS_CARTES = "marvel-board-dos-cartes";
function lireDosCartes() {
    try { return localStorage.getItem(CLE_DOS_CARTES) === "narwhal" ? "narwhal" : "officiels"; }
    catch (e) { return "officiels"; }
}
function choixDosCartes() {
    const boutons = [];
    const choisir = (valeur) => {
        try { localStorage.setItem(CLE_DOS_CARTES, valeur); } catch (e) { /* preference non critique */ }
        boutons.forEach((b) => b.classList.toggle("on", b.dataset.dos === valeur));
    };
    const bouton = (valeur, titre, image) => {
        const b = el("button", {
            class: "lg-dos" + (lireDosCartes() === valeur ? " on" : ""),
            "data-dos": valeur,
            onclick: () => choisir(valeur),
        }, el("img", { src: "/scan/" + image, alt: "" }), el("b", {}, titre));
        boutons.push(b);
        return b;
    };
    return el("div", { class: "lg-dos-bloc" },
        el("span", { class: "dm-sub" }, "Dos de cartes · Card backs"),
        el("div", { class: "lg-dos-grille" },
            bouton("officiels", "Officiels Marvel · Official Marvel", "player"),
            bouton("narwhal", "NarwhalChampions", "player-narwhal"),
        ),
        el("div", { class: "vh-note" },
            "Modifiable ensuite dans les réglages du plateau · Can be changed later in the board settings."),
    );
}

function demanderLaLangue() {
    return new Promise((resolve) => {
        const choisir = async (langue) => {
            const recharger = await retenirLangue(langue);
            fermerModale(overlay);
            if (recharger) location.reload(); else resolve();
        };
        const carte = (code, titre, sous) => el("button", {
            class: "lg-choix" + (langueActuelle() === code ? " on" : ""),
            onclick: () => { void choisir(code); },
        }, el("b", {}, titre), el("small", {}, sous));
        const overlay = el("div", { class: "deck-modal langue-modal" },
            el("div", { class: "deck-modal-panel vh-panel" },
                // ⚠ LE SEUL ECRAN DU JEU QUI PARLE LES DEUX LANGUES A LA FOIS
                // (16/09/2026). Partout ailleurs, `t()` traduit selon la langue
                // choisie. Ici, personne n'a encore choisi : la langue vaut
                // « fr » par defaut, et un anglophone lisait donc la question
                // en francais, avec ses explications. On ne traduit pas, on
                // ECRIT LES DEUX, comme un panneau d'aeroport.
                el("div", { class: "dm-head" },
                    el("b", { class: "mvl" }, "Bienvenue · Welcome"),
                    el("span", { class: "dm-sub" },
                        "Dans quelle langue veux-tu tes cartes ? · Which language do you want your cards in?"),
                ),
                el("div", { class: "lg-choix-grille" },
                    // Chaque carte decrit SA langue, dans SA langue : `t()` n'a
                    // rien a faire ici non plus.
                    carte("fr", "Français", "Cartes, interface et récit de la partie en français."),
                    carte("en", "English", "Cards, interface and game log in English."),
                ),
                // LE DOS DES CARTES (12/10/2026) : officiels par defaut, ou ceux
                // de NarwhalChampions. Un clic retient le choix sans fermer la
                // fenetre (c'est la langue qui la ferme). Meme cle que le plateau
                // (ui-app/src/board/dos-cartes.ts), modifiable dans ses reglages.
                choixDosCartes(),
                // ⚠ CE QUE LA LANGUE NE PEUT PAS FAIRE, DIT AVANT LE CHOIX
                // (16/09/2026). Tous les scans n'existent pas dans les deux
                // langues : la carte reste alors en anglais, et c'est
                // l'infobulle qui la traduit. Le decouvrir en pleine partie
                // ressemble a un defaut ; le lire ici, a une regle.
                el("div", { class: "vh-note" },
                    "Une carte sans scan dans la langue choisie reste affichée en anglais : quand on l'agrandit, sa traduction est posée sur son texte."),
                el("div", { class: "vh-note lg-en" },
                    "A card with no scan in the chosen language stays in English: when enlarged, its translation is laid over its text."),
                el("div", { class: "vh-note" },
                    "Tu peux changer à tout moment : le bouton FR / EN, en haut de l'écran."),
                el("div", { class: "vh-note lg-en" },
                    "You can switch at any time: the FR / EN button at the top of the screen."),
            ),
        );
        ouvrirModale(overlay);
    });
}

/** « Choisis ton affichage » : la fenêtre d'Options (Normal, Coloré, Sobre, et la couleur du fond).
 *
 *  ⚠ ELLE NE S'IMPOSE PLUS À LA PREMIÈRE VISITE (18/10/2026, demande de l'utilisateur : « vire le choix au
 *  début, les gens sont en Normal et peuvent à la limite changer dans les options ») et SANS IMAGES d'aperçu
 *  (retirées le même jour). Elle ne s'ouvre que par la tuile « Options ».
 *
 *  ⚠ On ne la ferme pas en cliquant à côté : un clic distrait vaudrait réponse.
 */
async function demanderLAffichage({ rouvert = false } = {}) {
    // L'épuré n'est proposé qu'à l'administrateur (16/10/2026) : on attend la réponse du serveur.
    await verifierEpurePermis();
    return new Promise((resolve) => {
        // Les cartes SE CHOISISSENT, elles ne ferment plus : la roue de la
        // couleur du fond vit dans la meme fenetre (choix de l'utilisateur,
        // 04/10/2026), et c'est « Valider » qui ferme le tout.
        let choixAffichage = rouvert ? affichageActuel() : "epure";
        let choixTeinte = teinteActuelle();
        const cartes = [];
        const carte = (valeur, titre, sous) => {
            const bouton = el("button", {
                class: "af-choix" + (valeur === choixAffichage ? " on" : ""),
                "aria-pressed": valeur === choixAffichage ? "true" : "false",
                onclick: () => {
                    choixAffichage = valeur;
                    for (const c of cartes) {
                        const on = c.dataset.valeur === valeur;
                        c.classList.toggle("on", on);
                        c.setAttribute("aria-pressed", on ? "true" : "false");
                    }
                },
            },
                el("b", {}, titre),
                el("small", {}, sous));
            bouton.dataset.valeur = valeur;
            cartes.push(bouton);
            return bouton;
        };
        const valider = () => {
            choisirAffichage(choixAffichage);
            if (choixTeinte) choisirTeinte(choixTeinte);
            // La page elle-meme prend la teinte tout de suite (« partout »).
            appliquerTeintePage(teinteActuelle());
            fermerModale(overlay);
            resolve();
        };
        const overlay = el("div", { class: "deck-modal affichage-modal" },
            el("div", { class: "deck-modal-panel vh-panel" },
                el("div", { class: "dm-head" },
                    el("b", { class: "mvl" }, t("Choisis ton affichage")),
                ),
                el("div", { class: "af-choix-grille" },
                    // Normal (valeur epure, celui de départ), Coloré (valeur normal), Sobre (18/10/2026).
                    epurePermis() ? carte("epure", t("Normal"), t("Fond sombre, panneaux bleus biseautés, titres en Bangers et rouge Marvel en touche.")) : null,
                    carte("normal", t("Coloré"), t("Couleurs du héros, animations.")),
                    carte("sobre", t("Sobre"), t("Fond gris, sans couleurs ni animations, plus reposant.")),
                ),
                el("div", { class: "af-teinte" },
                    el("b", {}, t("Couleur du fond")),
                    el("small", {}, t("Des teintes douces pour la table, les bandeaux et les panneaux.")),
                    roueTeinte(choixTeinte, (teinte) => { choixTeinte = teinte; }),
                ),
                el("div", { class: "vh-note" },
                    t("Tu pourras changer à tout moment : bouton Affichage en haut de cette page, ou Réglages en partie.")),
                el("div", { class: "af-valider" },
                    rouvert ? el("button", { class: "btn ghost", onclick: () => { fermerModale(overlay); resolve(); } }, t("Annuler")) : null,
                    el("button", { class: "btn primary", onclick: valider }, t("Valider"))),
            ),
        );
        ouvrirModale(overlay);
    });
}

/** « Choisis ta phase du méchant », posée une seule fois (05/10/2026).
 *
 *  Demandée par l'utilisateur : présenter, à la première connexion et à tout
 *  joueur qui ne les a pas encore vus, les trois façons de vivre la phase du
 *  méchant, « un petit peu comme pour le mode sobre et le mode normal », avec
 *  une image chacune. Les images sont de vraies captures du plateau.
 *
 *  ⚠ Depuis le 19/10/2026 les trois cartes s'appellent « Guidée » (valeur
 *  rangée `detaille`, inchangée), « Plateau animé » et « Accéléré », sans images (drapeau
 *  `PHASE_IMAGES_VISIBLES`, phase-mode-choix.js) : une courte description à la place.
 *
 *  ⚠ « D'un coup » dit son prix : on voit beaucoup moins, donc beaucoup moins
 *  de chances de repérer un défaut. Le choix se fait en connaissance de cause.
 *
 *  ⚠ Même règle que la langue et l'affichage : on ne la ferme pas en cliquant
 *  à côté, un clic distrait vaudrait « j'ai vu » et elle ne reviendrait jamais.
 */
function demanderLaPhaseDuMechant() {
    return new Promise((resolve) => {
        // Passage unique aux trois choix (19/10/2026) : avant de lire quoi que ce soit.
        try { migrerPhaseTroisChoix(localStorage); } catch (e) { /* stockage indisponible */ }
        let brutAvant = null;
        try { brutAvant = localStorage.getItem(CLE_MODE_PHASE); } catch (e) { /* stockage indisponible */ }
        let reglageDoigt = null;
        try { reglageDoigt = localStorage.getItem(CLE_JEU_AU_DOIGT); } catch (e) { /* stockage indisponible */ }
        const surTablette = estTablettePhase(reglageDoigt, window.matchMedia?.(REQUETE_TABLETTE_PHASE).matches);
        let choix = choixInitialPhase(brutAvant, surTablette);
        const cartes = [];
        const dossiers = { "detaille": "etape", "sur-table": "sur-table", "instantane": "d-un-coup" };
        const NOMBRE = 4;
        // Une seule grande visionneuse, au-dessus de laquelle on choisit le mode :
        // les captures sont des tables entieres, trop petites a un tiers de largeur.
        let dossier = dossiers[choix] || "etape";
        let i = 0;
        let minuteur = null;
        const src = (k) => `/public/img/phase-modes/${dossier}-${k + 1}.jpg`;
        const img = el("img", { src: PHASE_IMAGES_VISIBLES ? src(0) : "", alt: "", loading: "eager" });
        const points = Array.from({ length: NOMBRE }, () => el("span", { class: "pm-point" }));
        const dessiner = () => {
            img.src = src(i);
            points.forEach((p, n) => p.classList.toggle("on", n === i));
        };
        const aller = (k) => { i = (k + NOMBRE) % NOMBRE; dessiner(); };
        const arreter = () => { if (minuteur !== null) { clearInterval(minuteur); minuteur = null; } };
        const reduit = typeof matchMedia === "function" && matchMedia("(prefers-reduced-motion: reduce)").matches;
        const demarrer = () => { arreter(); if (!reduit) minuteur = setInterval(() => aller(i + 1), 3200); };
        if (PHASE_IMAGES_VISIBLES) for (const d of Object.values(dossiers)) for (let k = 0; k < NOMBRE; k++) { const pre = new Image(); pre.src = `/public/img/phase-modes/${d}-${k + 1}.jpg`; }
        const choisir = (valeur) => {
            choix = valeur;
            for (const c of cartes) {
                const on = c.dataset.valeur === valeur;
                c.classList.toggle("on", on);
                c.setAttribute("aria-pressed", on ? "true" : "false");
            }
            dossier = dossiers[valeur];
            i = 0;
            if (PHASE_IMAGES_VISIBLES) { dessiner(); demarrer(); }
        };
        const fleche = (sens, texte, nom) => el("button", {
            class: "pm-fleche pm-fleche-" + (sens < 0 ? "g" : "d"),
            type: "button",
            "aria-label": nom,
            onclick: () => { arreter(); aller(i + sens); },
        }, texte);
        const visionneuse = el("div", { class: "pm-carrousel" },
            img,
            fleche(-1, "‹", t("Image précédente")),
            fleche(1, "›", t("Image suivante")),
            el("div", { class: "pm-points" }, ...points));
        const carte = (valeur, titre, sous, note) => {
            const bouton = el("div", {
                class: "af-choix" + (valeur === choix ? " on" : ""),
                role: "button",
                tabindex: "0",
                "aria-pressed": valeur === choix ? "true" : "false",
                onclick: () => choisir(valeur),
                onkeydown: (e) => {
                    if (e.target !== bouton) return;
                    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choisir(valeur); }
                },
            },
                el("b", {}, titre),
                el("small", {}, sous),
                note ? el("small", { class: "pm-note" }, note) : null);
            bouton.dataset.valeur = valeur;
            cartes.push(bouton);
            return bouton;
        };
        const valider = () => {
            const aEcrire = modePhaseAEcrire(brutAvant, choix, surTablette);
            try {
                if (aEcrire) localStorage.setItem(CLE_MODE_PHASE, aEcrire);
                localStorage.setItem(CLE_PHASE_MODE_VU, "1");
                localStorage.setItem(CLE_PHASE_CHOIX_VU, VERSION_CHOIX_PHASE);
            } catch (e) { /* stockage refuse : la fenetre reviendra, c'est tout */ }
            arreter();
            fermerModale(overlay);
            resolve();
        };
        const overlay = el("div", { class: "deck-modal affichage-modal phase-modal" },
            el("div", { class: "deck-modal-panel vh-panel" },
                el("div", { class: "dm-head" },
                    el("b", { class: "mvl" }, t("Choix de la phase du méchant")),
                    el("span", { class: "dm-sub" }, t("Trois façons de vivre la phase du méchant, du plus détaillé au plus rapide.")),
                ),
                el("div", { class: "af-choix-grille" },
                    carte("detaille", t("Guidée"),
                        t("Un guide compact accompagne chaque étape de la phase du méchant, une étape à la fois.")),
                    carte("sur-table", t("Plateau animé"),
                        t("La phase du méchant se joue sur le plateau : les cartes bougent, un trait relie l'attaquant à sa cible et la validation se fait à côté de l'action.")),
                    carte("instantane", t("Accéléré"),
                        t("La phase du méchant se résout d'un seul coup, sans s'arrêter. Un bilan de fin de phase raconte ce qui s'est passé.")),
                ),
                PHASE_IMAGES_VISIBLES ? visionneuse : null,
                el("div", { class: "vh-note" },
                    t("Modifiable à tout moment : Réglages en partie, onglet Jeu.")),
                el("div", { class: "af-valider" },
                    el("button", { class: "btn primary", onclick: valider }, t("Valider"))),
            ),
        );
        if (PHASE_IMAGES_VISIBLES) { dessiner(); demarrer(); }
        ouvrirModale(overlay);
    });
}

/* ---- LEGACY ---------------------------------------------------------------
   Entrer dans le mode, poser la question de l'activation, tenir le verrou.
   Les règles sont dans legacy.js, la fiche dans legacy-fiche.js, le verrou
   dans legacy-verrou.js : ici, seulement ce qui touche l'écran. */

/** Recharge l'état et le verrou depuis le moteur. À appeler après un achat. */
async function rafraichirLegacy() {
    const e = await etatLegacy(t);
    const heroes = await catalog.heroes();
    // Les CARTES aussi (idée de l'utilisateur, 13/09/2026) : on construit
    // avec ce qu'on a. `dispo.deck(d)` dit si un deck tout fait est jouable.
    await cards.load();
    const extensions = await catalog.extensions();
    const paquetDe = (id) => { const c = cards.get(id); return c ? c.package_name : ""; };
    state.legacy = { etat: e, verrou: fabriquerVerrou(e, heroes, t),
                     dispo: fabriquerDisponibilite(e, extensions, paquetDe, t) };
    return state.legacy;
}

/** La tuile Legacy : on pose la question une fois, puis on entre. */
const CLE_LEGACY_EXPLIQUE = "marvel-legacy-explique";

/** « Le mode Legacy », la modale d'explication.
 *
 *  Demandee le 16/09/2026 : « une modale quand on commence le mode legacy qui
 *  explique exactement ce que ca fait, qui s'ouvre a chaque fois, sauf qu'il y
 *  a un truc qu'on peut cocher en disant ne plus afficher ».
 *
 *  ⚠ ELLE PASSE AVANT LA QUESTION DE L'ACTIVATION. « Reprendre mes parties
 *  passees ou repartir de zero » est un choix qui ne se refait pas : le poser
 *  avant d'avoir explique le mode, c'est le poser a l'aveugle.
 *
 *  ⚠ ET ELLE NE SE FERME QUE PAR OK, comme la modale de langue : un clic
 *  distrait a cote vaudrait « j'ai lu ».
 *
 *  La case cochee vit dans le localStorage, donc PAR NAVIGATEUR et non par
 *  compte. C'est le meme choix que pour la langue et les preferences du
 *  plateau : le site ne stocke pas de preferences d'affichage.
 */
function expliquerLegacy() {
    return new Promise((resolve) => {
        let vu = false;
        try { vu = localStorage.getItem(CLE_LEGACY_EXPLIQUE) === "1"; }
        catch (err) { vu = false; }
        if (vu) { resolve(); return; }

        const coche = el("input", { type: "checkbox", id: "lg-plus-jamais" });
        const point = (fort, suite) => el("li", {}, el("b", {}, t(fort)), " " + t(suite));
        const valider = () => {
            if (coche.checked) {
                try { localStorage.setItem(CLE_LEGACY_EXPLIQUE, "1"); }
                catch (err) { /* sans stockage, elle reviendra : tant pis */ }
            }
            fermerModale(overlay);
            resolve();
        };
        const overlay = el("div", { class: "deck-modal legacy-explique" },
            el("div", { class: "deck-modal-panel vh-panel" },
                el("div", { class: "dm-head" },
                    el("b", { class: "mvl" }, t("Le mode Legacy")),
                ),
                el("p", {}, t("Tu reprends le jeu depuis son origine. Au départ, seule la boîte de base est ouverte : tout le reste, héros, scénarios et cartes, attend derrière.")),
                el("ul", { class: "lg-regles" },
                    point("Pour ouvrir la boîte suivante :", "bats tous les méchants de la boîte en cours. Une victoire par méchant suffit, en normal comme en expert."),
                    point("Les héros rapportent des jetons :", "ta première victoire avec un héros officiel en donne un, deux si elle est prise en expert. Ils n'ouvrent aucune boîte."),
                    point("Les jetons achètent les héros fan-made,", "un jeton par héros, quand tu veux."),
                    point("À plusieurs, tout le monde coche :", "une victoire en équipe compte pour chaque héros de la table, et pour le méchant."),
                    point("Une boîte fermée l'est vraiment :", "ses héros, ses scénarios et ses cartes restent hors de portée, éditeur de deck compris. La condition est écrite sous chaque vignette grisée."),
                ),
                el("p", { class: "vh-note" }, t("Le jeu libre n'est jamais verrouillé : reviens à l'accueil et tout est là.")),
                el("div", { class: "vh-actions lg-actions" },
                    el("label", { class: "lg-plus-jamais", for: "lg-plus-jamais" },
                        coche, " " + t("Ne plus afficher ceci")),
                    el("button", { class: "tampon", onclick: valider }, "OK"),
                ),
            ),
        );
        ouvrirModale(overlay);
    });
}

async function entrerLegacy(nombre) {
    await expliquerLegacy();
    const e = await etatLegacy(t);
    if (!e.fiche.actif) {
        const repartir = await demanderDepartLegacy();
        if (repartir === null) return;            // a renoncé
        await activerLegacy(repartir);
    }
    await rafraichirLegacy();
    const n = Math.max(1, Math.min(4, nombre || 1));
    state.mode = n === 1 ? MODES.find((m) => m.id === "solo") : MODES.find((m) => m.id === "hotseat");
    state.coopEnLigne = false;
    state.playerCount = n;
    state.activeSlot = 0;
    state.scenario = null;
    // On ne masque pas les fan-made : ils se voient grisés, avec leur prix.
    state.heroFilters.homebrew = false;
    goto(0);
}

/** « Tes parties déjà jouées comptent-elles ? » Rend true (repartir de zéro),
 *  false (reprendre), ou null si on referme sans répondre.
 *
 *  ⚠ CE CHOIX NE SE REFAIT PAS, et la modale le dit. Reprendre ses parties
 *  passées peut ouvrir d'un coup plusieurs vagues ; repartir de zéro est le
 *  vrai parcours. Les deux sont légitimes, aucun n'est le défaut. */
function demanderDepartLegacy() {
    return new Promise((resolve) => {
        const finir = (valeur) => { hideHover(); fermerModale(overlay); resolve(valeur); };
        const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) finir(null); } },
            el("div", { class: "deck-modal-panel vh-panel" },
                el("div", { class: "dm-head" },
                    el("b", { class: "mvl" }, "Legacy"),
                    el("span", { class: "dm-sub" }, t("Tes parties déjà jouées comptent-elles ?")),
                ),
                el("div", { class: "legacy-choix" },
                    el("button", { onclick: () => finir(false) },
                        el("b", {}, t("Reprendre mes parties passées")),
                        el("small", {}, t("Tout ce que tu as déjà gagné est acquis. Tu repars d'où tu en es."))),
                    el("button", { onclick: () => finir(true) },
                        el("b", {}, t("Repartir de zéro")),
                        el("small", {}, t("Seules les parties jouées à partir de maintenant comptent. Le vrai parcours."))),
                ),
                el("div", { class: "vh-note" }, t("Ce choix ne se refait pas.")),
                el("div", { class: "vh-actions" },
                    el("button", { class: "tampon", onclick: () => finir(null) }, t("Annuler")),
                ),
            ),
        );
        ouvrirModale(overlay);
    });
}

/** Le bandeau en tête de l'étape : où on en est, et combien de jetons. */
function bandeLegacy() {
    if (!state.legacy) return null;
    const v = state.legacy.verrou;
    const suite = v.prochaine
        ? `${t("Pour ouvrir la suite")} : ${conditionLegacy(v.prochaine)}`
        : t("Tout est débloqué. Bravo.");
    // ⚠ CE QUI BLOQUE ET CE QUI RAPPORTE SE DISENT SUR DEUX LIGNES (16/09/2026).
    // Depuis que seuls les mechants ouvrent la vague suivante, les heros n'ont
    // plus rien a faire dans la phrase de condition : les y laisser ferait
    // croire a une exigence. Ils gardent pourtant un interet, et c'est le seul
    // endroit qui le dit.
    const sansVictoire = (v.prochaine && v.prochaine.herosRestants) || [];
    return el("div", { class: "legacy-bande" },
        el("b", {}, "Legacy"),
        el("span", {}, `${t("Vague ouverte")} : ${v.prochaine ? v.prochaine.nom : v.vagueOuverte}`),
        el("span", { class: "legacy-jetons" }, `${v.jetons.restants} ${t("jeton(s)")}`),
        el("span", { class: "legacy-suite" }, suite),
        sansVictoire.length
            ? el("span", { class: "legacy-bonus" },
                `${sansVictoire.length} ${t("héros de cette boîte n'ont pas encore gagné")} : `
                + `${sansVictoire.length} ${t("jeton(s) à prendre")}`)
            : null,
        el("span", { class: "legacy-regle" },
            t("Seuls les méchants ouvrent la vague suivante. Les héros, eux, rapportent les jetons.")),
    );
}

/** La phrase de condition d'une étape, dans la langue de l'écran. */
function conditionLegacy(etape) {
    // ⚠ CETTE FONCTION DOUBLE `legacy.condition()`, et c'est voulu : le module
    // pur ne connait pas `t()`. Les deux doivent donc changer ENSEMBLE, sans
    // quoi l'ecran continuerait d'exiger des heros que la regle a liberes
    // (16/09/2026).
    const noms = (liste) => liste.map((x) => x.nom || x.id);
    const vilains = noms(etape.vilainsRestants || []);
    if (!vilains.length) return "";
    return vilains.length <= 3
        ? `${t("bats")} ${vilains.join(", ")}`
        : `${t("bats")} ${vilains.length} ${t("méchants")}`;
}

/** Un clic sur un héros fan-made grisé : l'acheter, si on a de quoi. */
async function acheterHerosLegacy(h, portraitEl) {
    const v = state.legacy && state.legacy.verrou.heros(h);
    if (!v || v.ouvert || !v.achetable) return;
    const oui = await confirmerLegacy(t("Débloquer ce héros pour 1 jeton ?"), nomAffiche(h));
    if (!oui) return;
    const r = await acheterLegacy(h.heroCardId, t);
    if (!r.ok) { alert(r.raison || "?"); return; }
    await rafraichirLegacy();
    await refreshHeroGrid();
    const bande = document.querySelector(".legacy-bande");
    if (bande) bande.replaceWith(bandeLegacy());
    recruterVraiment(h, portraitEl);
}

function confirmerLegacy(question, detail) {
    return new Promise((resolve) => {
        const finir = (valeur) => { hideHover(); fermerModale(overlay); resolve(valeur); };
        const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) finir(false); } },
            el("div", { class: "deck-modal-panel vh-panel" },
                el("div", { class: "dm-head" },
                    el("b", { class: "mvl" }, detail),
                    el("span", { class: "dm-sub" }, question),
                ),
                el("div", { class: "vh-actions" },
                    el("button", { class: "tampon", onclick: () => finir(false) }, t("Annuler")),
                    el("button", { class: "tampon jaune", onclick: () => finir(true) }, t("Débloquer")),
                ),
            ),
        );
        ouvrirModale(overlay);
    });
}

/**
 * L'accueil au téléphone (zone 2 de la refonte du 09/10/2026) : un gros bouton
 * « Jouer » qui ouvre, en feuille basse, les façons de jouer (les mêmes tuiles
 * que le PC, nombre de héros compris), puis des vignettes vers le reste du jeu.
 */
function accueilTel(tuiles, partir) {
    const ouvrirModes = () => {
        let fermer = () => {};
        const choisir = (tuile, n) => fermer(() => partir(tuile, n));
        const lignes = tuiles.filter((tu) => tu.mode.id !== "campaign").map((tuile) => {
            const m = tuile.mode;
            const nombres = [];
            if (!m.fixed) {
                for (let n = (m.min || 1); n <= (m.max || 4); n++) {
                    if (m.id === "bataille" && n % 2 !== 0) continue;
                    nombres.push(el("button", {
                        class: "acc-nombre", type: "button", title: n + " " + t("héros"),
                        onclick: (e) => { e.stopPropagation(); choisir(tuile, n); },
                    }, m.id === "bataille" ? (n / 2) + "v" + (n / 2) : String(n)));
                }
            }
            return el("div", { class: "acc-tel-mode" },
                el("button", { class: "acc-tel-mode-nom", type: "button", onclick: () => choisir(tuile, null) },
                    el("b", { class: "mvl" }, tuile.libelle),
                    el("small", {}, tuile.detail)),
                nombres.length ? el("div", { class: "acc-nombres" }, el("small", {}, t("héros")), ...nombres) : null);
        });
        fermer = ouvrirFeuille({
            classe: "acc-tel-feuille",
            titre: el("h2", { class: "acc-tel-feuille-titre mvl" }, t("Comment veux-tu jouer ?")),
            contenu: lignes,
        });
    };
    const campagne = tuiles.find((tu) => tu.mode.id === "campaign");
    const vignette = (libelle, detail, icone, action) => el(typeof action === "string" ? "a" : "button", {
        class: "acc-tel-vignette cut",
        ...(typeof action === "string" ? { href: action } : { type: "button", onclick: action }),
    }, picto(icone), el("b", { class: "mvl" }, libelle), el("small", {}, detail));
    return el("section", { class: "step accueil acc-tel" },
        el("div", { class: "acc-tel-titre" },
            el("img", { class: "acc-narwhal", src: urlNarval(), alt: "NarwhalChampions" }),
            el("h1", { class: "affiche" }, "Narwhal", el("br"), "Champions")),
        el("button", { class: "acc-tel-jouer cut", type: "button", onclick: () => { jouerSon(SON.mode); ouvrirModes(); } },
            el("b", { class: "mvl" }, t("Jouer")),
            el("small", {}, t("Solo, coop, bataille, au hasard..."))),
        el("div", { class: "acc-tel-vignettes" },
            campagne ? vignette(campagne.libelle, campagne.detail, "fa-book", () => partir(campagne, null)) : null,
            vignette(t("Galerie"), t("Toutes les cartes"), "fa-th", "/galerie.html"),
            vignette(t("Éditeur de deck"), t("Construire un deck"), "fa-pencil", "/deck-builder.html"),
            vignette(t("Mises à jour"), t("Ce qui a changé"), "fa-bullhorn", () => ouvrirNouveautes()),
            vignette(t("Options"), t("Affichage, couleurs"), "fa-cog", () => demanderLAffichage({ rouvert: true })),
        ),
        blocRemerciements(),
    );
}

/** Sous la grille de l'accueil (12/10/2026, demande de l'utilisateur) : le
 *  merci a l'auteur du moteur d'origine et la mention legale COMPLETE, lisibles
 *  (pas la ligne grise du pied). `data-mention-complete` retire le pied en
 *  doublon (mention-legale.js). Texte de la mention valide mot pour mot. */
function blocRemerciements() {
    return el("div", { class: "acc-merci", "data-mention-complete": "" },
        el("p", {},
            t("Merci à Irefrixs, auteur du moteur d'origine sur lequel repose ce jeu."), " ",
            el("a", { href: "https://github.com/irefrixs/marvel-lcg", target: "_blank", rel: "noopener" }, "GitHub")),
        el("p", {},
            t("Merci aussi aux sites où nous avons trouvé images et informations :"), " ",
            el("a", { href: "https://marvelcdb.com/", target: "_blank", rel: "noopener" }, "MarvelCDB"), " · ",
            el("a", { href: "https://hallofheroeslcg.com/", target: "_blank", rel: "noopener" }, "Hall of Heroes"), " · ",
            el("a", { href: "https://mc4db.merlindumesnil.net/", target: "_blank", rel: "noopener" }, "MC4DB"), ". ",
            t("Et à tous les créateurs de fan-made, ainsi qu'à ma maman.")),
        voletCreateurs({ t, el, ouvrirModale, fermerModale }),
        el("p", {},
            t("Si j'ai oublié de te créditer pour une image, une carte ou un contenu, j'en suis désolé : dis-le-moi via"), " ",
            el("a", { href: "https://narwhalchampions.com/contact-createurs", target: "_blank", rel: "noopener" }, t("ce formulaire")), " ",
            t("et je corrige au plus vite. Tu peux aussi me demander de retirer tes créations du site par le même formulaire.")),
        el("p", {}, t("Projet de fans, gratuit et non officiel. Marvel Champions: The Card Game est un jeu de Fantasy Flight Games (Asmodee). Les personnages et illustrations Marvel appartiennent à Marvel. Ce site n'est ni affilié à ces sociétés ni approuvé par elles. Il sert de vitrine et d'outil de jeu : il faut posséder le jeu pour l'utiliser.")),
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
            tuiles.push({ mode: m, distant: false, mark: m.mark, libelle: m.label,
                          detail: m.desc, aide: m.aide, cle: m.id });
            tuiles.push({ mode: m, distant: true, mark: "@", libelle: t("Coop en ligne"),
                          detail: t("2 à 4 héros, chacun choisit le sien"),
                          aide: t("Chacun sur son écran. Tu envoies un lien, ils rejoignent."),
                          cle: m.id + "-en-ligne" });
            continue;
        }
        tuiles.push({ mode: m, distant: null, mark: m.mark, libelle: m.label,
                      detail: m.desc, aide: m.aide, cle: m.id });
    }
    // PARTIE AU HASARD (08/10/2026) : pas un mode du moteur, une façon de
    // remplir l'équipe et la cible. Elle repart sur Solo ou Coop selon le
    // nombre de héros choisi sur la tuile.
    tuiles.push({ mode: { id: "hasard", min: 1, max: 4 }, distant: null, mark: "?",
                  libelle: t("Partie au hasard"), detail: t("Héros et scénario tirés au sort"),
                  aide: t("Une roue tire les héros et le scénario dans toutes les boîtes. Tu choisis ensuite les decks et la difficulté."),
                  cle: "hasard" });

    const partir = (tuile, nombre) => {
        const m = tuile.mode;
        // Le seul passage pour choisir un mode : la grande tuile ET les boutons
        // de nombre y aboutissent, d'où un seul appel au son.
        jouerSon(SON.mode);
        if (tuile.cle === "hasard") { void ouvrirRoue(nombre || 1); return; }
        // Puzzle : sans nombre de heros, le clic ouvre le panneau (puzzles.js) ; avec un nombre, c'est la creation qui demarre.
        if (m.id === "puzzle") window.creerPuzzle = (n) => partir(tuile, n);
        if (m.id === "puzzle" && !nombre) {
            if (typeof window.ouvrirPanneauPuzzles === "function") { window.ouvrirPanneauPuzzles(); return; }
            nombre = 1;
        }
        if (tuile.distant !== null) state.coopEnLigne = tuile.distant;
        if (m.id === "campaign") { window.location.href = "/campagne.html"; return; }
        // On quitte Legacy dès qu'on choisit autre chose : le jeu libre n'est
        // jamais verrouillé.
        state.legacy = null;
        if (m.id === "legacy") { void entrerLegacy(nombre); return; }
        const wasCampaign = isCampaignMode();
        state.mode = m;
        if ((m.id === "campaign") !== wasCampaign) state.scenario = null;
        state.playerCount = (m.fixed && m.id !== "puzzle") ? 1
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
        //
        // L'AIDE : une phrase qui dit ce que fait le mode, dans une bulle au
        // survol. `aria-describedby` la relie au bouton, donc un lecteur
        // d'écran l'annonce APRÈS le nom du mode, comme une précision, sans
        // l'écraser. Sur un écran tactile, qui n'a pas de survol, la même
        // phrase reste visible en permanence : voir `.acc-aide` dans
        // prepare.css.
        // ⚠ LA BULLE EST DEHORS, PAS DANS LE BOUTON. Les tuiles portent la
        // classe `cut`, donc un `clip-path` pour leur coin coupe : il DECOUPE
        // tout ce qu'elles contiennent. Une bulle placee a l'interieur etait
        // bien la, visible pour le navigateur comme pour les tests, et
        // n'apparaissait a l'ecran nulle part. D'ou l'enveloppe.
        const idAide = "acc-aide-" + tuile.cle;
        grille.append(el("div", { class: "acc-tuile", "data-cle": tuile.cle },
            el("button", {
                class: "acc-mode cut" + (nombres.length ? " avec-nombres" : ""),
                onclick: () => partir(tuile, null),
                ...(tuile.aide ? { "aria-describedby": idAide } : {}),
            },
                el("span", { class: "acc-copy" },
                    // « Partie au hasard » sur deux lignes (17/10/2026) : sur une seule, le titre
                    // touchait les boutons de nombre.
                    tuile.cle === "hasard" && tuile.libelle.includes(" ")
                        ? el("b", { class: "mvl" }, tuile.libelle.slice(0, tuile.libelle.indexOf(" ") + 1), el("br"), tuile.libelle.slice(tuile.libelle.indexOf(" ") + 1))
                        : el("b", { class: "mvl" }, tuile.libelle),
                    el("small", {}, tuile.detail),
                ),
                nombres.length ? el("span", { class: "acc-nombres" },
                    el("small", {}, t("héros")), ...nombres) : null,
            ),
            tuile.aide ? el("span", { class: "acc-aide", id: idAide, role: "tooltip" },
                            tuile.aide) : null,
        ));
    }

    // L'éditeur de deck, sur l'accueil (demande du 16/10/2026) : on ne le trouvait
    // qu'en passant par un héros, puis un bouton de l'étape Decks.
    grille.append(el("div", { class: "acc-tuile", "data-cle": "editeur" },
        el("button", { class: "acc-mode cut acc-editeur-tuile", onclick: () => { window.location.href = "/deck-builder.html"; }, "aria-describedby": "acc-aide-editeur" },
            el("span", { class: "acc-copy" },
                el("b", { class: "mvl" }, t("Éditeur de deck")),
                el("small", {}, t("Construire un deck")),
            ),
        ),
        el("span", { class: "acc-aide", id: "acc-aide-editeur", role: "tooltip" },
           t("Construire ou modifier un deck, puis l'utiliser en partie.")),
    ));

    // ⚠ LES NOUVEAUTES SONT UNE TUILE, PLUS UNE LISTE SOUS LA GRILLE
    // (17/09/2026). Le journal a grossi au point de pousser les modes hors de
    // l'ecran : « tout ne rentre pas sur une page a cause des mises a jour ».
    // Une tuile de plus, au meme format que les modes, et tout le journal
    // derriere, classe par famille.
    grille.append(el("div", { class: "acc-tuile", "data-cle": "nouveautes" },
        el("button", {
            class: "acc-mode cut acc-nouv-tuile",
            // PC : une page à part (nouveautes.html). Le téléphone garde la modale.
            onclick: () => { if (estTel()) ouvrirNouveautes(); else window.location.href = "/nouveautes.html"; },
            "aria-describedby": "acc-aide-nouveautes",
        },
            el("span", { class: "acc-copy" },
                el("b", { class: "mvl" }, t("Mises à jour")),
                el("small", {}, t("Ce qui a changé")),
            ),
        ),
        el("span", { class: "acc-aide", id: "acc-aide-nouveautes", role: "tooltip" },
           t("Tout ce qui a été ajouté ou corrigé, du plus récent au plus ancien.")),
    ));

    // Les options, comme en partie (demande du 15/10/2026) : la fenêtre
    // d'affichage (Normal / Sobre / Épuré, couleur du fond), rouverte à volonté.
    grille.append(el("div", { class: "acc-tuile", "data-cle": "options" },
        el("button", {
            class: "acc-mode cut acc-options-tuile",
            onclick: () => demanderLAffichage({ rouvert: true }),
            "aria-describedby": "acc-aide-options",
        },
            el("span", { class: "acc-copy" },
                el("b", { class: "mvl" }, t("Options")),
                el("small", {}, t("Affichage, couleurs")),
            ),
        ),
        el("span", { class: "acc-aide", id: "acc-aide-options", role: "tooltip" },
           t("Changer l'affichage du site et ses couleurs.")),
    ));

    // L'ORDRE DES TUILES (17/10/2026), trois par rangée : jouer seul ou à plusieurs, puis
    // la progression, puis les modes à part, puis le reste. Une tuile absente
    // (ex. Coop en ligne hors serveur en ligne) laisse simplement la suite remonter.
    const ORDRE = ["solo", "hotseat", "hotseat-en-ligne", "campaign", "legacy", "hasard",
                   "bataille", "sandbox", "editeur", "puzzle", "options", "nouveautes"];
    const rang = (c) => { const i = ORDRE.indexOf(c); return i < 0 ? ORDRE.length : i; };
    [...grille.children]
        .sort((a, b) => rang(a.dataset.cle) - rang(b.dataset.cle))
        .forEach((n) => grille.append(n));

    if (estTel()) return accueilTel(tuiles, partir);

    return el("section", { class: "step accueil" },
        el("div", { class: "acc-entete" },
            // Le narval, mascotte du site. ⚠ SANS EXTENSION : le moteur sert
            // les images par leur NOM (server_files.py). Voir le meme usage
            // dans l'en-tete des etapes, plus haut.
            el("img", { class: "acc-narwhal", src: urlNarval(), alt: "NarwhalChampions" }),
            el("div", { class: "acc-titre" },
                el("div", { class: "recitatif" }, t("Préparation de mission")),
                el("h1", { class: "affiche" }, "Narwhal", el("br"), "Champions"),
                el("p", {}, t("Comment veux-tu jouer ?")),
            ),
        ),
        grille,
        blocRemerciements(),
    );
}

/* ---- Partie au hasard : la roue (08/10/2026) -------------------------------
   Décisions de l'utilisateur, une à une : .planning/todos/2026-10-08-roue-du-hasard.md.
   Un bandeau par héros, qui tournent ensemble et s'arrêtent l'un après
   l'autre, puis celui du scénario. En ligne, l'hôte tire et publie
   (`/set_roue`), chacun anime ce qu'il lit (`/get_roue`) ; un invité ne
   relance que SON héros, depuis le salon (js/salon/app.js). */

const CLE_ROUE_FANMADE = "mc_roue_fanmade";
const SONDAGE_ROUE_MS = 1000;

function roueFanmade() {
    try { return localStorage.getItem(CLE_ROUE_FANMADE) === "oui"; } catch (e) { return false; }
}

function retenirRoueFanmade(oui) {
    try { localStorage.setItem(CLE_ROUE_FANMADE, oui ? "oui" : "non"); } catch (e) { /* stockage indisponible */ }
}

/** Les bandeaux s'arrêtent l'un après l'autre : le héros i, puis le scénario. */
function dureeBandeau(i) {
    return 2600 + 400 * i;
}

async function ouvrirRoue(nombre) {
    // On quitte Legacy, comme pour tout autre mode : le jeu libre n'est
    // jamais verrouillé.
    state.legacy = null;
    const n = Math.max(1, Math.min(4, nombre || 1));
    state.mode = MODES.find((m) => m.id === (n === 1 ? "solo" : "hotseat"));
    state.playerCount = n;
    state.activeSlot = 0;
    const enReseau = n > 1 && enLigne();

    let fanmade = roueFanmade();
    let heros = [], scenarios = [], tousHeros = [];
    const chargerPools = async () => {
        const [h, s] = await Promise.all([catalog.heroes(), catalog.tousLesScenarios()]);
        tousHeros = h;
        heros = herosTirables(h, { fanmade });
        scenarios = scenariosTirables(s, { fanmade });
    };

    const resultats = { heros: [], scenario: null };
    // En ligne : le compteur de lancers déjà animé, par bandeau.
    const vus = { heros: {}, scenario: 0 };
    let animations = 0;

    const bandeauxHeros = Array.from({ length: n }, () => creerBandeau({ surClic: jouerClicRoue }));
    const bandeauScn = creerBandeau({ surClic: jouerClicRoue });
    const message = el("p", { class: "roue-message", role: "status" });
    const continuer = el("button", { class: "btn primary", disabled: true }, t("Continuer"));
    const relances = [];

    const majBoutons = () => {
        const pret = !animations && resultats.scenario
            && (enReseau ? !!resultats.heros[0] : resultats.heros.length === n && resultats.heros.every(Boolean));
        continuer.disabled = !pret;
        relances.forEach((b) => { b.disabled = animations > 0; });
    };
    const animer = async (promesses) => {
        animations += 1;
        majBoutons();
        try { await Promise.all(promesses); } finally { animations -= 1; majBoutons(); }
    };
    const casesHeros = () => heros.map(caseHeros);
    const casesScn = () => scenarios.map(caseScenario);

    const noterVus = (roue) => {
        if (!roue) return;
        Object.entries(roue.heros || {}).forEach(([p, e]) => { vus.heros[p] = e.n; });
        if (roue.scenario) vus.scenario = roue.scenario.n;
    };

    async function toutLancer() {
        const tires = tirerPlusieurs(heros, n);
        const sc = scenarios.length ? tirer(scenarios) : null;
        if (tires.length < n || !sc) {
            message.textContent = t("Pas assez de héros ou de scénarios à tirer.");
            return;
        }
        message.textContent = "";
        resultats.heros = tires;
        resultats.scenario = sc;
        if (enReseau) {
            noterVus(await publierRoue({
                quoi: "tout", nombre: n, fanmade,
                heros: Object.fromEntries(tires.map((h, i) => [String(i), h.id])),
                scenario: sc.id,
            }));
        }
        await animer([
            ...tires.map((h, i) => bandeauxHeros[i].tourner(casesHeros(), caseHeros(h), dureeBandeau(i))),
            bandeauScn.tourner(casesScn(), caseScenario(sc), dureeBandeau(n)),
        ]);
    }

    async function relancerHeros(p) {
        // Jamais le héros d'un autre siège ; et si possible pas celui qu'on a déjà.
        const autres = resultats.heros.map((x, i) => (i !== p && x ? x.id : null)).filter(Boolean);
        const actuel = resultats.heros[p];
        const h = tirer(heros, { exclus: actuel ? [...autres, actuel.id] : autres })
            || tirer(heros, { exclus: autres });
        if (!h) return;
        resultats.heros[p] = h;
        if (enReseau) noterVus(await publierRoue({ quoi: "heros", p, id: h.id }));
        await animer([bandeauxHeros[p].tourner(casesHeros(), caseHeros(h), dureeBandeau(0))]);
    }

    async function relancerScenario() {
        const sc = tirer(scenarios, { exclus: resultats.scenario ? [resultats.scenario.id] : [] })
            || tirer(scenarios);
        if (!sc) return;
        resultats.scenario = sc;
        if (enReseau) noterVus(await publierRoue({ quoi: "scenario", id: sc.id }));
        await animer([bandeauScn.tourner(casesScn(), caseScenario(sc), dureeBandeau(0))]);
    }

    const boutonRelancer = (surClic) => {
        const b = el("button", { class: "btn ghost roue-relancer", onclick: () => { jouerSon(SON.aleatoire); void surClic(); } },
            picto("fa-random"), " ", t("Relancer"));
        relances.push(b);
        return b;
    };

    const ligne = (titre, bandeau, bouton, attente) => el("div", { class: "roue-ligne" },
        el("b", { class: "roue-titre" }, titre),
        bandeau.element,
        bouton || el("span", { class: "roue-relance-ailleurs" }, attente || ""),
    );

    const caseFanmade = el("input", { type: "checkbox", class: "roue-fanmade-case" });
    caseFanmade.checked = fanmade;
    caseFanmade.addEventListener("change", async () => {
        fanmade = caseFanmade.checked;
        retenirRoueFanmade(fanmade);
        await chargerPools();
        await toutLancer();
    });

    let sondage = null;
    const overlay = el("div", { class: "deck-modal roue-modal", role: "dialog", "aria-modal": "true",
                                "aria-label": t("Partie au hasard") });
    const fermer = () => {
        clearInterval(sondage);
        fermerModale(overlay);
    };
    const retour = el("button", { class: "btn ghost", onclick: () => {
        if (enReseau) void publierRoue({ quoi: "fermer" });
        fermer();
    } }, t("Retour"));
    continuer.addEventListener("click", () => {
        if (continuer.disabled) return;
        jouerSon(SON.etapeSuivante);
        for (let p = 0; p < n; p++) {
            if (!enReseau || p === 0) assignHero(p, resultats.heros[p]);
            else state.players[p].hero = null;
        }
        const sc = resultats.scenario;
        state.extensionTab = sc.extension;
        selectScenario(sc);
        fermer();
        state.step = 0;
        goto(1);
    });

    overlay.append(el("div", { class: "deck-modal-panel roue-panel" },
        el("div", { class: "roue-entete" },
            el("b", { class: "mvl roue-nom" }, t("Partie au hasard")),
            el("label", { class: "roue-fanmade" }, caseFanmade, " ", t("Inclure les fan-made")),
        ),
        enReseau ? el("p", { class: "roue-aide" },
            t("Tout le salon voit la roue. Chaque joueur peut relancer son héros depuis son écran.")) : null,
        ...bandeauxHeros.map((b, p) => ligne(
            n > 1 ? `${t("Joueur")} ${p + 1}` : t("Héros"), b,
            (!enReseau || p === 0) ? boutonRelancer(() => relancerHeros(p)) : null,
            t("Il relance depuis son écran"))),
        ligne(t("Scénario"), bandeauScn, boutonRelancer(relancerScenario)),
        message,
        el("div", { class: "roue-actions" }, retour, continuer),
    ));
    ouvrirModale(overlay);
    message.textContent = t("Chargement des héros et des scénarios...");
    await chargerPools();
    if (!overlay.isConnected) return;
    await toutLancer();

    if (enReseau) {
        // Les relances des invités : on anime ce que le salon publie.
        sondage = setInterval(async () => {
            if (!overlay.isConnected) { clearInterval(sondage); return; }
            const roue = await lireRoue();
            if (!roue) return;
            for (let p = 1; p < n; p++) {
                const e = (roue.heros || {})[String(p)];
                if (!e || e.n === vus.heros[String(p)]) continue;
                vus.heros[String(p)] = e.n;
                const h = tousHeros.find((x) => x.id === e.id);
                if (!h) continue;
                resultats.heros[p] = h;
                void animer([bandeauxHeros[p].tourner(casesHeros(), caseHeros(h), dureeBandeau(0))]);
            }
        }, SONDAGE_ROUE_MS);
    }
}

/* ---- Le journal des nouveautés (8 septembre 2026, refondu le 17/09) -------
   ⚠ D'ABORD UNE LISTE SOUS LES TUILES, MAINTENANT UNE TUILE. Les trois
   dernières lignes s'affichaient sur l'accueil, le reste sous « Tout voir » :
   à 69 entrées, le bloc poussait les modes de jeu hors de l'écran. Signalé le
   17/09 : « tout ne rentre pas sur une page à cause des mises à jour ».

   Le contenu vit dans `nouveautes.js`, écrit pour les joueurs ; ici il n'y a
   que la mise en page. */

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

/** Une ligne du journal.
 *
 *  `avecGenre` : l'etiquette de famille. Inutile dans la modale, ou chaque
 *  section porte deja son titre — la repeter a chaque ligne ne dit rien de
 *  plus et vole de la largeur au texte. */
function ligneNouveaute(entree, avecGenre = true) {
    const anglais = langueActuelle() === "en";
    const genre = GENRES[entree.genre];
    return el("li", {},
        el("span", { class: "acc-nouv-date" }, dateCourteNouveaute(entree.date)),
        avecGenre ? el("span", { class: "acc-nouv-genre " + entree.genre },
                       anglais ? genre.en : genre.fr) : null,
        el("span", { class: "acc-nouv-texte" }, anglais ? entree.en : entree.fr),
    );
}

/** Le journal complet, groupe par famille, dans une modale.
 *
 *  ⚠ L'ORDRE DES FAMILLES EST CELUI DE `GENRES`, pas celui des dates : le
 *  joueur vient chercher « ce que je peux jouer » avant « ce qui a ete
 *  repare ». Dans chaque famille, le plus recent d'abord. */
function ouvrirNouveautes() {
    const toutes = nouveautesTriees();
    const sections = [];
    for (const [cle, genre] of Object.entries(GENRES)) {
        const lot = toutes.filter((e) => e.genre === cle);
        if (!lot.length) continue;
        sections.push(el("section", { class: "nouv-famille" },
            el("h3", { class: "nouv-famille-titre " + cle },
               langueActuelle() === "en" ? genre.en : genre.fr,
               el("span", { class: "nouv-compte" }, String(lot.length))),
            el("ul", { class: "acc-nouv-liste" }, lot.map((e) => ligneNouveaute(e, false))),
        ));
    }
    const overlay = el("div", { class: "deck-modal nouveautes-modal" },
        el("div", { class: "deck-modal-panel vh-panel" },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, t("Mises à jour")),
            ),
            el("div", { class: "nouv-corps" }, ...sections),
            el("div", { class: "vh-actions" },
                el("button", { class: "tampon", onclick: () => fermerModale(overlay) }, t("Fermer")),
            ),
        ),
    );
    ouvrirModale(overlay);
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
                jouerSon(SON.mode);
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

/** Le cri de REPLI d'un héros, par identifiant de deck : ne sert plus qu'aux
 *  héros absents de REPLIQUES (repliques-heros.js), qui porte désormais
 *  plusieurs répliques par héros, tirées au sort (11/09/2026). Repli du
 *  repli : « BAM ! ». */
const ONOMATOPEES = {
    harry_osborn: "HA HA HA !",
    /* --- fan-made --- */
    doctor_druid: "MASTER OF THE UNKNOWN !", lady_sif: "FOR ASGARD !", };
/** La réplique qui claque au recrutement : au hasard dans le pool du héros,
 *  jamais la même que la dernière (mémorisée par navigateur, par héros). */
function replique(hero) {
    const pool = REPLIQUES[hero.id] || [ONOMATOPEES[hero.id] || "BAM !"];
    const cle = "narwhal-replique:" + hero.id;
    let derniere;
    try { derniere = localStorage.getItem(cle) || undefined; } catch (_) { /* stockage refusé */ }
    const choisie = choisirReplique(pool, derniere, Math.random) || "BAM !";
    try { localStorage.setItem(cle, choisie); } catch (_) { /* préférence non critique */ }
    return choisie;
}


/** Le héros en scène : celui du siège actif, sauf pendant un survol. */
let herosSurvole = null;

/** Qui est en scène, et quand : voir `survol-heros.js` (le bouton « Voir ses cartes » est dans la scène, pas sur la tuile : la scène ne
 *  doit donc pas changer sous la souris qui va vers lui). Bug du Discord, 26/10/2026. */
const survolHeros = creerSurvolHeros({
    afficher: (h) => { herosSurvole = h; rendreScene(h); },
    revenir: () => { herosSurvole = null; rendreScene(herosDuSiegeActif()); },
});

function herosDuSiegeActif() {
    const p = state.players[state.activeSlot];
    return (p && p.hero) || null;
}

function stepTeam() {
    const wrap = el("section", { class: "step team-b" },
        el("div", {
            class: "tb-scene", id: "tb-scene",
            onmouseenter: estTel() ? undefined : () => survolHeros.entrerDansLaScene(),
            onmouseleave: estTel() ? undefined : () => survolHeros.sortirDeLaScene(),
        }),
    );
    const f = state.heroFilters;
    const droite = el("div", { class: "tb-droite" },
        bandeauEnLigne(),
        creationCampagne() ? el("div", { class: "command-band" }, modeStrip()) : null,
        bandeLegacy(),
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
        // Le merci aux créateurs : rempli par refreshHeroGrid, visible sur le
        // seul filtre fan-made (demande du 18/09/2026).
        el("div", { class: "tb-merci", id: "tb-merci", hidden: true }),
        el("div", { class: "hero-grid tb-roster", id: "hero-grid" }, el("div", { class: "loading" }, t("Chargement des héros..."))),
        estTel() ? null : el("div", { class: "tb-equipe", id: "tb-equipe" }),
    );
    wrap.append(droite);
    herosSurvole = null;
    survolHeros.remettreAZero();
    herosApercuTel = null;
    loadHeroes();
    // La scène et l'équipe se dessinent une fois la section DANS la page :
    // elles se retrouvent par identifiant.
    //
    // ⚠ Si le siège actif a déjà un héros (étape reconstruite par `render()`,
    // ex. après « Valider » dans la fenêtre des variantes), on la FIGE dessus
    // (`geler`, pas `rendreScene`) : sans ça, `remettreAZero()` plus haut
    // dégèlerait une scène que l'utilisateur venait tout juste de figer d'un
    // clic, et le survol suivant l'écraserait aussitôt (signalé le 27/10/2026).
    // Siège encore vide (premier passage sur l'écran) : on laisse le survol
    // libre pour le tout premier choix.
    Promise.resolve().then(() => {
        rendreEquipe();
        const actif = herosDuSiegeActif();
        if (actif) survolHeros.geler(actif);
        else rendreScene(null);
    });
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
        // Les pastilles montent au-dessus du pied de scène quand il prend plus
        // d'une ligne (livret, carnet, biographie) : jamais plus bas que leur
        // place d'origine, pour ne rien déplacer quand tout tient.
        const bas0 = scene.getBoundingClientRect().bottom;
        let plafond = null;
        for (const sel of [".tb-bas", ".tb-tampons", ".tb-defi"]) {
            const bloc = scene.querySelector(sel);
            if (!bloc || bloc.offsetParent === null) continue;
            if (plafond !== null) {
                bloc.style.bottom = "";
                const origine = parseFloat(getComputedStyle(bloc).bottom) || 0;
                const voulu = Math.round(bas0 - plafond + 12);
                if (voulu > origine) bloc.style.bottom = voulu + "px";
            }
            plafond = bloc.getBoundingClientRect().top;
        }
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
    if (estTel()) return rendreSceneTel(h);
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
        ajusterNomGeant(scene);
        return;
    }
    const traits = [...new Set([...(h.traits || []), ...(h.traitsAlterEgo || [])])].slice(0, 4).join(" · ");
    const vague = h.homebrew ? t("Fan-made")
        : (h.vague == null ? "" : (h.vague === 0 ? t("Set de base") : t("Vague") + " " + h.vague));
    poser(scene,
        // Scan anglais même en français : le scan FR porte un filigrane, très
        // visible à cette taille. Demande de l'utilisateur.
        h.lie
            ? el("div", { class: "tb-art" }, portraitDuo(h, "", cardImageUrlHd))
            : el("div", { class: "tb-art", style: { backgroundImage: `url("${cardImageUrlHd(picIdHeros(h.heroCardId))}")` } }),
        el("div", { class: "tb-trame" }),
        el("div", { class: "tb-nomg" },
            el("small", {}, traits || nomExtension(h.extension, langueActuelle())),
            nomAffiche(h)),
        el("div", { class: "tb-tampons" },
            pvAffiches(h) ? el("span", { class: "tampon jaune" }, t("PV") + " " + pvAffiches(h)) : null,
            h.handSize != null ? el("span", { class: "tampon" }, t("Main") + " " + h.handSize) : null,
            vague ? el("span", { class: "tampon" }, vague) : null,
            optionsDuHeros(h, contexteVariantes(h)).aucune ? null : el("button", {
                class: "tampon jaune tb-choix-art",
                title: t("Version, identité, art, ressources : les options de ce héros"),
                onclick: () => ouvrirModaleVariantes(siegeDuHeros(h), h),
            }, t("Variantes")),
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
            onmouseenter: auSurvol(() => loupe(id)),
            onmouseleave: () => loupe(null),
            // Téléphone : pas de loupe au survol, un toucher ouvre la carte en grand.
            onclick: estTel() ? () => ouvrirCarteGrande(id) : undefined,
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
        // Équipes TOUJOURS en anglais, même site en français (demande du
        // 21/10/2026) : ce sont des noms propres (Avengers, X-Men…), pas du
        // texte à traduire. Repli sur la version FR si une fiche plus recente
        // n'a pas encore sa version anglaise.
        info.equipes ? detailRow(t("Équipes"), info.equipesEn || info.equipes) : null,
        info.ennemis ? detailRow(t("Ennemis"), champ(info.ennemis, info.ennemisEn)) : null,
        info.apparition ? detailRow(t("Première apparition"), info.apparition) : null,
        // Auteur du pack fan-made (21/10/2026) : lu sur `custom` de la carte
        // héros elle-même (seule source, déjà posée pack par pack à la
        // création — voir `catalog.js` qui fait pareil pour les scénarios).
        // Absent sur les héros officiels : rien à afficher.
        (() => {
            const carte = cards.get(h.heroCardId);
            const auteur = carte && carte.custom;
            return auteur ? detailRow(t("Pack créé par"), auteur) : null;
        })(),
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
            title: pilotable ? (pl.hero ? nomAffiche(pl.hero) : t("Joueur") + " " + (i + 1)) : t("Ce joueur choisit depuis son propre écran"),
            onclick: () => {
                if (!pilotable) return;
                // Parcours sequentiel : pas de saut en avant, on ne passe au
                // heros suivant qu'apres avoir valide le deck du courant.
                if (state.step === 1 && decksSequentiels()) {
                    if (enRecap()) state.modifDeck = true;
                    const k = premierSiegeAValider();
                    if (k >= 0 && i > k) return;
                }
                state.activeSlot = i;
                herosApercuTel = null;
                rendreEquipe();
                // Chaque étape a sa scène : les héros la remplissent avec le
                // héros du siège, l'arsenal avec son deck.
                if (state.step === 1) { rendreSceneDeck(); rendreOutilsDeck(); loadDecks(i); }
                else {
                    // Même logique de gel qu'un clic sur un héros (27/10/2026) :
                    // changer de siège est aussi un choix délibéré, le survol
                    // des tuiles ne doit pas effacer ce qu'on vient d'afficher.
                    const actif = herosDuSiegeActif();
                    if (actif) survolHeros.geler(actif);
                    else { survolHeros.remettreAZero(); rendreScene(null); }
                }
            },
        },
            pl.hero ? portraitHeros(pl.hero) : el("span", { class: "plus" }, "+"),
            el("span", { class: "tb-siege-nom" }, state.step === 1 && deckAffiche(pl)
                ? cleanNomDeck(pl.deck.name)
                : (pl.hero ? nomAffiche(pl.hero) : t("Joueur") + " " + (i + 1))),
        ));
    }
    poser(zone,
        el("span", { class: "tb-equipe-k" }, t("Ton équipe")),
        ...sieges,
    );
}

/** Recruter : le geste de la carte qui surgit, l'onomatopée, puis la scène. */
/* ---- La fiche du héros au tap (spec mobile du 07/09/2026, §6.2) ----------
   Sans survol (téléphone, tablette), rien ne présente un héros avant de le
   choisir : le tap l'assignait d'un coup. Le PREMIER tap ouvre donc une fiche
   (portrait, traits, PV, biographie, « Voir ses cartes ») ; le second tap sur
   la même tuile, ou le bouton « Choisir ce héros », l'assigne. Sur PC, le
   survol fait déjà ce travail dans la scène : rien ne change. */
let herosPresente = null;

function ouvrirFicheHeros(h, portraitEl) {
    const traits = [...new Set([...(h.traits || []), ...(h.traitsAlterEgo || [])])].slice(0, 4).join(" · ");
    const vague = h.homebrew ? t("Fan-made")
        : (h.vague == null ? "" : (h.vague === 0 ? t("Set de base") : t("Vague") + " " + h.vague));
    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) fermerModale(overlay); } },
        el("div", { class: "deck-modal-panel vh-panel fiche-heros" },
            el("div", { class: "fh-art", style: { backgroundImage: `url("${cardImageUrlHd(picIdHeros(h.heroCardId))}")` } }),
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, nomAffiche(h)),
                el("span", { class: "dm-sub" }, traits),
            ),
            el("div", { class: "tb-tampons fh-tampons" },
                pvAffiches(h) ? el("span", { class: "tampon jaune" }, t("PV") + " " + pvAffiches(h)) : null,
                h.handSize != null ? el("span", { class: "tampon" }, t("Main") + " " + h.handSize) : null,
                vague ? el("span", { class: "tampon" }, vague) : null,
            ),
            bioDepliee_(bioDuHeros(h)),
            el("div", { class: "vh-actions" },
                estTel() ? el("button", {
                    class: "tampon" + (prefs.isFavHero(h.id) ? " on" : ""), onclick: (e) => {
                        const on = prefs.toggleFavHero(h.id);
                        e.currentTarget.classList.toggle("on", on);
                    },
                }, "★ ", t("Favori")) : null,
                estTel() ? el("button", { class: "tampon", onclick: () => { fermerModale(overlay); ouvrirDeckDuHeros(h); } }, t("Deck")) : null,
                el("button", { class: "tampon", onclick: () => { fermerModale(overlay); ouvrirCartesHeros(h); } }, t("Voir ses cartes")),
                el("button", { class: "tampon jaune", onclick: () => { fermerModale(overlay); recruterVraiment(h, portraitEl); } }, t("Choisir ce héros")),
            ),
        ),
    );
    ouvrirModale(overlay);
}

/** Sur la fiche, la biographie est ce qu'on est venu lire : dépliée d'office. */
function bioDepliee_(pli) {
    if (pli) pli.setAttribute("open", "");
    return pli;
}

function recruter(h, portraitEl) {
    if (SANS_SURVOL && herosPresente !== h.id) {
        herosPresente = h.id;
        ouvrirFicheHeros(h, portraitEl);
        return;
    }
    recruterVraiment(h, portraitEl);
}

function recruterVraiment(h, portraitEl) {
    herosPresente = null;
    // Avec variantes, la modale s'ouvre aussitôt : pas de bruit de carte posée
    // par-dessus, la réplique suffit.
    // Sur téléphone, « Options de ce héros » ne s'ouvre plus d'office : le
    // bouton « Art » du bandeau la rend à la demande (décision du 09/10/2026).
    const tel = estTel();
    const avecVariantes = !tel && !optionsDuHeros(h, contexteVariantes(h)).aucune;
    if (!avecVariantes) jouerSon(SON.heros);
    jouerReplique(h.id, "heros");
    const siege = state.activeSlot;
    assignHero(siege, h);
    autoAdvanceSlot();
    herosSurvole = null;
    // La scène d'abord (elle se reconstruit), la carte qui surgit ensuite,
    // par-dessus : dans l'autre ordre, la reconstruction l'emportait.
    if (tel) { herosApercuTel = h; rendreSceneTel(h); }
    else {
        const actif = herosDuSiegeActif();
        // Desktop : la scène se FIGE sur le héros tout juste choisi — geler()
        // l'affiche lui-même, le survol des autres tuiles ne la bougera plus
        // jusqu'au prochain clic. Siège suivant encore vide (multijoueur,
        // tous les héros ne sont pas choisis) : on NE fige PAS sur du vide,
        // sinon plus aucun survol ne marcherait pour choisir le héros suivant.
        if (actif) survolHeros.geler(actif);
        else { survolHeros.remettreAZero(); rendreScene(null); }
    }
    rendreEquipe();
    const jouerEclair = () => {
        const scene = document.getElementById("tb-scene");
        if (!scene || tel) return;
        const cri = replique(h);
        const eclair = el("div", { class: "tb-eclair" },
            el("img", { src: cardImageUrlEn(picIdHeros(h.heroCardId)), alt: "" }),
            // La taille suit la longueur : une courte claque, une longue se lit.
            el("span", { class: ("ono " + classeTaille(cri)).trim() }, cri),
        );
        scene.append(eclair);
        eclair.addEventListener("animationend", (ev) => { if (ev.target === eclair) eclair.remove(); });
        setTimeout(() => eclair.remove(), 2800);   // filet, un peu apres la fin de l'animation
    };
    // La fenêtre « Options du héros » s'ouvre aussitôt et cacherait la carte et sa phrase
    // (17/10/2026) : elles jouent alors à la fermeture de la fenêtre (Valider ou Annuler).
    if (avecVariantes) apresModaleVariantes = jouerEclair;
    else jouerEclair();
    document.querySelectorAll(".tb-port").forEach((b) => {
        b.classList.toggle("chosen", activePlayers().some((p) => p.hero && p.hero.id === b.dataset.hero));
    });
    // La barre du bas suit (Continuer s'allume) sans reconstruire l'écran.
    majNav();
    // Ce héros a des variantes ? La modale s'ouvre tout de suite, pré-remplie
    // de la mémoire. Sans variante, rien : jamais de modale vide.
    if (avecVariantes) ouvrirModaleVariantes(siege, h);
    // Plus d'avance automatique (24/10/2026) : le joueur change d'avis en touchant un autre héros, puis touche « Continuer ».
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
    // Le titre de la boite ne passe PAS par t() : c'est le titre imprime sur
    // la boite, en anglais (NOMS_VAGUES) ou en francais depuis le 29/09/2026
    // (`titreDeBoite`, table `TITRES_FR` de titres-extensions.js).
    // La vague 1 n'a pas de boite : son libelle est de nous, donc traduit.
    const titre = vague === 1 ? t("Les premiers paquets") : titreDeBoite(titreDeVague(vague), langueActuelle());
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

/** Le champ de recherche annonce ce qu'il accepte. Le créateur ne vaut que
 *  pour le fan-made : un héros officiel n'en a pas (18/09/2026). */
function majPlaceholderRecherche(homebrew) {
    const champ = document.querySelector(".tb-search");
    if (!champ) return;
    champ.placeholder = homebrew
        ? t("Rechercher un héros, un trait ou un créateur")
        : t("Rechercher un héros ou un trait");
}

/** La liste COMMUNE des remerciements (demande du 17/10/2026) : tous les créateurs de
 *  héros ET d'extensions fan-made (vilains, sets), la même sur l'écran des héros et sur
 *  celui des méchants. Elle ne dépend ni de la recherche ni de l'onglet : un nouveau
 *  contenu se déclare une fois (champ `custom` des cartes) et paraît partout. */
let _creditsFanmade = null;
function createursFanmadeTous() {
    if (!_creditsFanmade) {
        _creditsFanmade = (async () => {
            const heros = await catalog.heroes();
            const auteurs = [];
            for (const e of await catalog.extensions()) {
                if (/custom/i.test(e.key)) auteurs.push(await auteurDeExtension(e));
            }
            return createursDeTout(heros, auteurs);
        })().catch((err) => { _creditsFanmade = null; throw err; });
    }
    return _creditsFanmade;
}

/** Remplit une ligne de remerciement. Un seul créateur : la phrase passe au singulier,
 *  sinon elle parle de « leur travail » à une personne seule. */
function remplirMerci(merci, noms) {
    merci.hidden = noms.length === 0;
    if (!noms.length) { merci.replaceChildren(); return; }
    merci.replaceChildren(
        t("Un grand merci à") + " ",
        el("b", {}, noms.join(", ")),
        " " + (noms.length === 1
            ? t("pour son travail : ces héros et ces méchants sont les siens.")
            : t("pour leur travail : ces héros et ces méchants sont les leurs.")),
    );
}

/** Sur le filtre fan-made, une ligne remercie tous les créateurs (liste commune, voir
 *  `createursFanmadeTous`). Ailleurs la ligne disparaît. */
async function majMerciCreateurs(homebrew) {
    const merci = document.getElementById("tb-merci");
    if (!merci) return;
    remplirMerci(merci, homebrew ? await createursFanmadeTous() : []);
}

/** La même ligne sur l'écran des méchants, quand son filtre fan-made est coché. */
async function majMerciVilains() {
    const merci = document.getElementById("tb-merci-vilains");
    if (!merci) return;
    remplirMerci(merci, state.extFanmade ? await createursFanmadeTous() : []);
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
    majMerciCreateurs(f.homebrew);
    majPlaceholderRecherche(f.homebrew);
    if (!list.length) {
        grid.replaceChildren(el("div", { class: "empty-state" }, t("Aucun héros trouvé")));
        return;
    }
    grid.replaceChildren(...list.map((h) => {
        const chosen = activePlayers().some((p) => p.hero && p.hero.id === h.id);
        // Legacy : ce qui n'est pas débloqué reste sous les yeux, grisé, avec
        // sa condition. Un fan-made se débloque d'un clic si on a un jeton.
        const verrou = state.legacy ? state.legacy.verrou.heros(h) : null;
        const ferme = !!verrou && !verrou.ouvert;
        return el("button", {
            class: "tb-port" + (chosen ? " chosen" : "") + (ferme ? " est-verrou" : "")
                + (ferme && verrou.achetable ? " est-achetable" : ""),
            "data-hero": h.id,
            "aria-disabled": ferme && !verrou.achetable ? "true" : null,
            title: ferme ? verrou.condition : nomAffiche(h),
            onclick: (e) => {
                // Téléphone : un toucher CHOISIT le héros (24/10/2026) ; on en touche un autre pour changer, puis « Continuer » en bas.
                if (!ferme && estTel()) return recruterVraiment(h, e.currentTarget);
                if (!ferme) return recruter(h, e.currentTarget);
                if (verrou.achetable) return void acheterHerosLegacy(h, e.currentTarget);
            },
            // Téléphone : pas de survol (un doigt ne « quitte » jamais la tuile,
            // et mouseleave re-dessinerait le bandeau en plein toucher).
            onmouseenter: estTel() ? undefined : () => survolHeros.entrer(h),
            onmouseleave: estTel() ? undefined : () => survolHeros.sortir(),
            onfocus: estTel() ? undefined : () => survolHeros.entrerAuClavier(h),
        },
            portraitHeros(h),
            el("span", { class: "tb-port-nom" }, nomAffiche(h)),
            ferme ? el("span", { class: "tb-verrou" }, verrou.etiquette) : null,
            estTel() ? null : el("span", {
                class: "hc-fav" + (prefs.isFavHero(h.id) ? " on" : ""),
                title: t("Favori"),
                onclick: (e) => {
                    e.stopPropagation();
                    e.preventDefault();
                    jouerSon(SON.favori);
                    const on = prefs.toggleFavHero(h.id);
                    e.currentTarget.classList.toggle("on", on);
                },
            }, "★"),
            estTel() ? null : el("span", {
                class: "hc-deck",
                title: t("Voir le deck"),
                onclick: (e) => { e.stopPropagation(); e.preventDefault(); ouvrirDeckDuHeros(h); },
            }, "▤"),
        );
    }));
}

/** Téléphone : un toucher montre le héros dans le bandeau, sans le choisir. */
function apercevoirHerosTel(h, tuile) {
    herosApercuTel = h;
    document.querySelectorAll(".tb-port.apercu").forEach((b) => b.classList.remove("apercu"));
    if (tuile) tuile.classList.add("apercu");
    rendreSceneTel(h);
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

// FILET. Sur un ecran tactile, tout panneau de survol qui s'ouvrirait malgre
// `auSurvol` n'aurait AUCUN moyen de se refermer : il n'existe ni `mouseleave`
// ni touche Echap sous le doigt, et l'utilisateur se retrouve enferme sous une
// carte en plein ecran (constate sur son telephone le 11/09/2026, dans la
// modale d'options du heros).
//
// Le premier contact referme donc ce qui traine. En phase de CAPTURE, pour
// passer avant les gestionnaires des boutons, et sans rien annuler : cela ne
// fait qu'enlever une classe, le clic suit son cours normalement.
if (SANS_SURVOL) {
    document.addEventListener("pointerdown", () => hideHover(), true);
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
        el("div", { class: "hh-name mvl" }, libelleExtension(ext, _auteursExtensions.get(ext.key))),
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
    // Ressources redessinees livrees avec le heros Binary (Galactic Storm, Kajislav, 20/10/2026) ;
    // par defaut pour Binary (collectionDuHeros : meme nom que le heros).
    { code: "binary", nom: "Binary", apercu: "01089_binary" },
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
    { code: "quasar", nom: "Quasar", apercu: "01089_quasar" },  // Galactic Storm (Kajislav), reskins du deck de Quasar
    { code: "dh_quicksilver", nom: "Quicksilver", apercu: "01089_dh_quicksilver" },
    { code: "dh_rocket", nom: "Rocket", apercu: "01089_dh_rocket" },
    { code: "dh_scarletwitch", nom: "Scarlet Witch", apercu: "01089_dh_scarletwitch" },
    { code: "sh", nom: "She-Hulk", apercu: "01089_sh" },
    { code: "dh_spectrum", nom: "Spectrum", apercu: "01089_dh_spectrum" },
    { code: "sm", nom: "Spider-Man", apercu: "01089_sm" },
    { code: "sw", nom: "Spider-Woman", apercu: "01089_sw" },
    { code: "dh_starlord", nom: "Star-Lord", apercu: "01089_dh_starlord" },
    { code: "th", nom: "Thor", apercu: "01089_th" },
    { code: "tmnt", nom: "TMNT", apercu: "ub016" },
    { code: "dh_valkyrie", nom: "Valkyrie", apercu: "01089_dh_valkyrie" },
    { code: "dh_venom", nom: "Venom", apercu: "01089_dh_venom" },
    { code: "dh_vision", nom: "Vision", apercu: "01089_dh_vision" },
    { code: "dh_warmachine", nom: "War Machine", apercu: "01089_dh_warmachine" },
    { code: "wa", nom: "Wasp", apercu: "01089_wa" },
    // Re-skins livrés PAR un pack custom fan-made du dépôt (mêmes règles,
    // illustration propre au héros) : chaque pack a ses PROPRES card_id
    // (pas de full_link vers 01088/89/90), ce qui ne change rien pour ce
    // sélecteur, purement cosmétique. Ajoutés le 22/09/2026, images
    // fournies par l'autrice RyCoRan (zip « Resource Cards »).
    { code: "angel", nom: "Angel", apercu: "42034" },
    { code: "beast", nom: "Beast", apercu: "bt025" },
    { code: "gambit", nom: "Gambit", apercu: "37037" },
    { code: "human_torch", nom: "Human Torch", apercu: "ht016" },
    { code: "jubilee", nom: "Jubilee", apercu: "47036" },
    { code: "magneto", nom: "Magneto", apercu: "49044" },
    { code: "the_thing", nom: "The Thing", apercu: "th017" },
    { code: "wave", nom: "Wave", apercu: "65018" },
    // Neuf packs fan-made de fin octobre 2026 (26/10/2026) : arts alternatifs des ressources doubles, par defaut pour leur
    // heros (collectionDuHeros : meme nom que le heros). Aligne avec COLLECTIONS (ui-app/src/board/variantes.ts).
    { code: "batgirl", nom: "Batgirl", apercu: "bg021" },
    { code: "batman", nom: "Batman", apercu: "bm024" },
    { code: "chod", nom: "Ch'od", apercu: "co018" },
    { code: "corsair", nom: "Corsair", apercu: "cr018" },
    { code: "hepzibah", nom: "Hepzibah", apercu: "hz017" },
    { code: "raza", nom: "Raza Longknife", apercu: "rl019" },
    { code: "roz", nom: "Roz", apercu: "rz014" },
    { code: "smasher", nom: "Smasher", apercu: "sz017" },
    { code: "warriors_three", nom: "The Warriors Three", apercu: "wt023" },
    { code: "predator", nom: "Predator", apercu: "pd022" },
];

/* ---- Arts alternatifs des CARTES DE HEROS ------------------------------
   Trois séries : M3T4LB0X (m3t), le zip « Marvel Champions Alt Art » (cb) et
   l'album Flickr de The Rose of Gondolin (rog, rog2).
   Purement cosmétique : la carte reste la même pour le moteur.
   N'ont été retenus que les arts dont les VALEURS et le TEXTE imprimés sont
   identiques à notre carte ; un art affichant autre chose mentirait en pleine partie.
   Ici, seule la face héros du wizard ; le plateau connaît aussi les autres
   faces (alter ego, Touched, SP//dr...).
   Doit rester aligné avec ui-app/src/board/variantes.ts (ARTS_HEROS). */
const ARTS_HEROS = {
    "01001a": [{ code: "m3t", nom: "M3T4LB0X" }, { code: "cb", nom: "Comic" }],
    "01010a": [{ code: "m3t", nom: "M3T4LB0X" }, { code: "cb", nom: "Comic" }],
    "01019a": [{ code: "m3t", nom: "M3T4LB0X" }, { code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "01029a": [{ code: "m3t", nom: "M3T4LB0X" }, { code: "cb", nom: "Comic" }],
    "01040a": [{ code: "cb", nom: "Comic" }],
    "03001a": [{ code: "m3t", nom: "M3T4LB0X" }, { code: "cb", nom: "Comic" }],
    "04001a": [{ code: "m3t", nom: "M3T4LB0X" }, { code: "cb", nom: "Comic" }],
    "04031a": [{ code: "cb", nom: "Comic" }],
    "05001a": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }, { code: "rog2", nom: "Rose of Gondolin 2" }],
    "06001a": [{ code: "cb", nom: "Comic" }],
    "08001a": [{ code: "cb", nom: "Comic" }],
    "09001a": [{ code: "cb", nom: "Comic" }],
    "10001a": [{ code: "cb", nom: "Comic" }],
    "12001a": [{ code: "cb", nom: "Comic" }],
    "13001a": [{ code: "cb", nom: "Comic" }],
    "14001a": [{ code: "cb", nom: "Comic" }],
    "15001a": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }, { code: "rog2", nom: "Rose of Gondolin 2" }],
    "16001a": [{ code: "cb", nom: "Comic" }],
    "16029a": [{ code: "cb", nom: "Comic" }],
    "17001a": [{ code: "cb", nom: "Comic" }],
    "18001a": [{ code: "cb", nom: "Comic" }],
    "19001a": [{ code: "cb", nom: "Comic" }],
    "20001a": [{ code: "cb", nom: "Comic" }],
    "21001a": [{ code: "cb", nom: "Comic" }],
    "21031a": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "22001a": [{ code: "cb", nom: "Comic" }],
    "23001a": [{ code: "cb", nom: "Comic" }],
    "25001a": [{ code: "cb", nom: "Comic" }],
    "26001a": [{ code: "cb", nom: "Comic" }],
    "27001a": [{ code: "cb", nom: "Comic" }],
    "27030a": [{ code: "cb", nom: "Comic" }],
    "28001a": [{ code: "cb", nom: "Comic" }],
    "29001a": [{ code: "cb", nom: "Comic" }],
    "30001a": [{ code: "cb", nom: "Comic" }],
    "31001a": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "32001a": [{ code: "cb", nom: "Comic" }],
    "32030a": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "33001a": [{ code: "cb", nom: "Comic" }],
    "34001a": [{ code: "cb", nom: "Comic" }],
    "35001a": [{ code: "cb", nom: "Comic" }],
    "36001a": [{ code: "cb", nom: "Comic" }],
    "37001a": [{ code: "cb", nom: "Comic" }],
    "38001a": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }, { code: "rog2", nom: "Rose of Gondolin 2" }],
    "40001a": [{ code: "cb", nom: "Comic" }],
    "40037a": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "41001a": [{ code: "cb", nom: "Comic" }],
    "42001a": [{ code: "cb", nom: "Comic" }],
    "43001a": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "44001a": [{ code: "cb", nom: "Comic" }],
    "45001a": [{ code: "cb", nom: "Comic" }],
    "45030a": [{ code: "cb", nom: "Comic" }],
    "46001a": [{ code: "cb", nom: "Comic" }],
    "47001a": [{ code: "cb", nom: "Comic" }],
    "48001a": [{ code: "cb", nom: "Comic" }],
    "49001a": [{ code: "cb", nom: "Comic" }],
    "50001a": [{ code: "cb", nom: "Comic" }],
    "50034a": [{ code: "cb", nom: "Comic" }],
    "51001a": [{ code: "cb", nom: "Comic" }],
    "52001a": [{ code: "cb", nom: "Comic" }],
    "53001a": [{ code: "cb", nom: "Comic" }],
    "54001a": [{ code: "cb", nom: "Comic" }],
    "56001a": [{ code: "cb", nom: "Comic" }],
    "56029a": [{ code: "cb", nom: "Comic" }],
    "58001a": [{ code: "cb", nom: "Comic" }],
    "59001a": [{ code: "cb", nom: "Comic" }],
    "60001a": [{ code: "cb", nom: "Comic" }],
    "60037a": [{ code: "cb", nom: "Comic" }],
    "61001a": [{ code: "cb", nom: "Comic" }],
    "62001a": [{ code: "cb", nom: "Comic" }],
};

/** Arts de la face ALTER EGO (face « b »), par héros : même format que ci-dessus,
 *  clé = numéro du héros sans suffixe. Absent : l'alter ego garde son scan. */
const ARTS_ALTER_EGOS = {
    "01001": [{ code: "cb", nom: "Comic" }],
    "01010": [{ code: "cb", nom: "Comic" }],
    "01019": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "01029": [{ code: "cb", nom: "Comic" }],
    "01040": [{ code: "cb", nom: "Comic" }],
    "03001": [{ code: "cb", nom: "Comic" }],
    "04001": [{ code: "cb", nom: "Comic" }],
    "04031": [{ code: "cb", nom: "Comic" }],
    "05001": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }, { code: "rog2", nom: "Rose of Gondolin 2" }],
    "06001": [{ code: "cb", nom: "Comic" }],
    "08001": [{ code: "cb", nom: "Comic" }],
    "09001": [{ code: "cb", nom: "Comic" }],
    "10001": [{ code: "cb", nom: "Comic" }],
    "12001": [{ code: "cb", nom: "Comic" }],
    "13001": [{ code: "cb", nom: "Comic" }],
    "14001": [{ code: "cb", nom: "Comic" }],
    "15001": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }, { code: "rog2", nom: "Rose of Gondolin 2" }],
    "16001": [{ code: "cb", nom: "Comic" }],
    "16029": [{ code: "cb", nom: "Comic" }],
    "17001": [{ code: "cb", nom: "Comic" }],
    "18001": [{ code: "cb", nom: "Comic" }],
    "19001": [{ code: "cb", nom: "Comic" }],
    "20001": [{ code: "cb", nom: "Comic" }],
    "21001": [{ code: "cb", nom: "Comic" }],
    "21031": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "22001": [{ code: "cb", nom: "Comic" }],
    "25001": [{ code: "cb", nom: "Comic" }],
    "26001": [{ code: "cb", nom: "Comic" }],
    "27001": [{ code: "cb", nom: "Comic" }],
    "27030": [{ code: "cb", nom: "Comic" }],
    "28001": [{ code: "cb", nom: "Comic" }],
    "29001": [{ code: "cb", nom: "Comic" }],
    "30001": [{ code: "cb", nom: "Comic" }],
    "31001": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "32001": [{ code: "cb", nom: "Comic" }],
    "32030": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "33001": [{ code: "cb", nom: "Comic" }],
    "34001": [{ code: "cb", nom: "Comic" }],
    "36001": [{ code: "cb", nom: "Comic" }],
    "37001": [{ code: "cb", nom: "Comic" }],
    "38001": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }, { code: "rog2", nom: "Rose of Gondolin 2" }],
    "40001": [{ code: "cb", nom: "Comic" }],
    "40037": [{ code: "cb", nom: "Comic" }, { code: "rog", nom: "Rose of Gondolin" }],
    "41001": [{ code: "cb", nom: "Comic" }],
    "42001": [{ code: "cb", nom: "Comic" }],
    "43001": [{ code: "cb", nom: "Comic" }],
    "44001": [{ code: "cb", nom: "Comic" }],
    "45001": [{ code: "cb", nom: "Comic" }],
    "45030": [{ code: "cb", nom: "Comic" }],
    "46001": [{ code: "cb", nom: "Comic" }],
    "47001": [{ code: "cb", nom: "Comic" }],
    "48001": [{ code: "cb", nom: "Comic" }],
    "49001": [{ code: "cb", nom: "Comic" }],
    "50001": [{ code: "cb", nom: "Comic" }],
    "50034": [{ code: "cb", nom: "Comic" }],
    "51001": [{ code: "cb", nom: "Comic" }],
    "52001": [{ code: "cb", nom: "Comic" }],
    "53001": [{ code: "cb", nom: "Comic" }],
    "54001": [{ code: "cb", nom: "Comic" }],
    "56001": [{ code: "cb", nom: "Comic" }],
    "56029": [{ code: "cb", nom: "Comic" }],
    "58001": [{ code: "cb", nom: "Comic" }],
    "59001": [{ code: "cb", nom: "Comic" }],
    "60001": [{ code: "cb", nom: "Comic" }],
    "60037": [{ code: "cb", nom: "Comic" }],
    "61001": [{ code: "cb", nom: "Comic" }],
    "62001": [{ code: "cb", nom: "Comic" }],
};


/** Identifiant d'image de la carte de héros, art alternatif choisi compris. */
function picIdHeros(heroCardId) {
    const base = String(heroCardId || "").split(",")[0];
    const arts = ARTS_HEROS[base];
    if (!arts || !arts.length) return base;
    const choix = prefs.heroArt(heroCardId);
    return arts.some((a) => a.code === choix) ? `${base}_${choix}` : base;
}

/** Les trois ressources d'une collection, déduites de son aperçu (Genius).
 *  Préfixe alpha optionnel (« gp016 », « bt025 ») en plus du cas numérique pur
 *  (« 01089 ») : sans lui, les collections à identifiant préfixé (Gwenpool,
 *  Howard the Duck, Ms. America, et les packs custom ajoutés le 22/09/2026 —
 *  Beast, Human Torch, The Thing) tombaient dans le repli à 1 seule carte,
 *  silencieusement, alors que leurs trois images existent bel et bien. */
function tripletRessources(apercu) {
    const m = String(apercu || "").match(/^([a-z]*)(\d+)(_.+)?$/);
    if (!m) return apercu ? [apercu] : [];
    const prefixe = m[1] || "", chiffres = m[2], suffixe = m[3] || "";
    const largeur = chiffres.length, n = parseInt(chiffres, 10);
    const pad = (v) => String(v).padStart(largeur, "0");
    return [prefixe + pad(n - 1) + suffixe, prefixe + pad(n) + suffixe, prefixe + pad(n + 1) + suffixe];
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
function collectionDuHeros(nomHeros, heroCardId) {
    // Un héros TMNT a par défaut les ressources TMNT (règle du 17/10/2026).
    if (serieDuHeros(heroCardId) === "tmnt") return "tmnt";
    const cle = _cleRessource(nomHeros);
    if (!cle) return null;
    const trouvee = COLLECTIONS_RESSOURCES.find((c) => _cleRessource(c.nom) === cle);
    return trouvee ? trouvee.code : null;
}

/* ---- La modale du héros : version, identité, art, ressources ------------
   Idée de l'utilisateur du 11/09/2026 : une seule tuile par héros, et au clic
   tout ce que CE héros a de particulier, au même endroit. Le bloc
   « Identité et arts » de l'étape Decks a disparu : la modale seule décide,
   l'étape Decks n'en garde qu'un rappel et un bouton « Modifier ». Chaque
   héros se souvient de son dernier choix sur cet appareil (prefs.variantes,
   l'art et les ressources gardant leurs clés lues aussi par le plateau). */

/** Ce que le lanceur sait de ce héros, pour `optionsDuHeros` (module pur). */
function contexteVariantes(h) {
    return {
        arts: ARTS_HEROS[String(h.heroCardId || "").split(",")[0]] || [],
        collection: collectionDuHeros(h.name, h.heroCardId),
    };
}

/** Le siège qui joue ce héros, sinon le siège actif. */
function siegeDuHeros(h) {
    const i = state.players.findIndex((p) => p && p.hero && p.hero.id === h.id);
    return i >= 0 ? i : state.activeSlot;
}


/** Une section de la modale : un titre, un sous-titre, des vignettes. */
function sectionVariantes(titre, sous, options, actuel, surChoix) {
    const zone = el("div", { class: "res-art" },
        el("div", { class: "ra-tete" },
            el("span", { class: "ra-titre" }, titre),
            sous ? el("span", { class: "ra-sous" }, sous) : null,
        ),
    );
    const choix = el("div", { class: "ra-choix" });
    options.forEach((o) => {
        const bouton = el("button", {
            class: "ra-option" + (o.code === actuel ? " sel" : ""),
            title: o.nom,
            // `auSurvol` enveloppe le ternaire ENTIER, et non sa seule premiere
            // branche : la passe precedente n'avait protege que le cas `trio`,
            // et l'art alternatif (`apercu`) restait a decouvert. C'est
            // exactement ce que l'utilisateur a vu, capture a l'appui : dans la
            // modale d'options, toucher un art affichait la carte en grand sans
            // aucun moyen d'en sortir.
            onmouseenter: auSurvol(
                o.trio ? (e) => showTrioHover(o.trio, e.currentTarget)
                    : (o.apercu ? (e) => showCardHover(o.apercu, e.currentTarget) : undefined)
            ),
            onmouseleave: auSurvol((o.trio || o.apercu) ? scheduleHide : undefined),
            onclick: () => {
                surChoix(o.code);
                [...choix.children].forEach((b) => b.classList.remove("sel"));
                bouton.classList.add("sel");
            },
        });
        if (o.apercu || o.trio) {
            bouton.append(el("img", { class: "ra-vignette", src: cardImageUrl(o.apercu || o.trio), loading: "lazy", alt: "" }));
        } else {
            bouton.append(el("div", { class: "ra-vignette ra-hasard" }, "?"));
        }
        bouton.append(el("span", {}, o.nom));
        choix.append(bouton);
    });
    zone.append(choix);
    return zone;
}

/** Un carrousel d'arts pour UNE face : grande image, une flèche de chaque côté
 *  (hors de l'image), balayage. `options` : [{ code, nom }], « standard » en
 *  tête. Rend `{ noeud, regler, avancer, deleguer, masquer }` :
 *  - `regler(code, fige)` change l'art montré sans rappeler `surChoix` ;
 *  - `avancer(sens)` passe à l'art voisin, comme un clic sur une flèche ;
 *  - `deleguer(fn)` renvoie les flèches et le balayage vers `fn(sens)` (l'alter
 *    ego qui suit la face héros fait défiler celle-ci) ; `null` pour annuler ;
 *  - `masquer(gauche, droite)` cache une flèche sur ordinateur (une seule paire
 *    pour les deux faces en « même série »). */
function carrouselArts({ titre, picId, options, actuel, inactif, surChoix }) {
    let idx = Math.max(0, options.findIndex((o) => o.code === actuel));
    let figé = !!inactif;
    let delegue = null;
    const image = el("img", { class: "ca-image", alt: "", draggable: "false" });
    // Le cadre a la taille exacte de l'image : la traduction posée (jeu en
    // français, scan HD anglais) s'y place en pourcentages de la carte.
    const cadre = el("div", { class: "ca-cadre" }, image);
    image.addEventListener("load", () => {
        if (image.naturalWidth && image.naturalHeight) cadre.style.aspectRatio = `${image.naturalWidth}/${image.naturalHeight}`;
    });
    let tirage = 0;
    const nom = el("span", { class: "ca-nom" });
    const compteur = el("span", { class: "ca-compteur" });
    const aller = (n) => {
        if (figé || options.length < 2) return;
        idx = (n + options.length) % options.length;
        dessiner();
        surChoix(options[idx].code);
    };
    const pousser = (sens) => (delegue ? delegue(sens) : aller(idx + sens));
    const fleche = (sens, glyphe, libelle) => el("button", {
        type: "button", class: "ca-fleche ca-fleche-" + (sens < 0 ? "g" : "d"),
        "aria-label": libelle, onclick: () => pousser(sens),
    }, glyphe);
    const scene = el("div", { class: "ca-scene", tabindex: "0",
        onkeydown: (e) => {
            if (e.key === "ArrowLeft") { e.preventDefault(); pousser(-1); }
            if (e.key === "ArrowRight") { e.preventDefault(); pousser(1); }
        },
    }, cadre);
    let departX = null;
    scene.addEventListener("pointerdown", (e) => { departX = e.clientX; });
    scene.addEventListener("pointerup", (e) => {
        if (departX === null) return;
        const dx = e.clientX - departX;
        departX = null;
        if (Math.abs(dx) > 40) pousser(dx < 0 ? 1 : -1);
    });
    scene.addEventListener("pointercancel", () => { departX = null; });
    const noeud = el("div", { class: "ca" },
        el("div", { class: "ca-titre" }, titre),
        el("div", { class: "ca-corps" },
            fleche(-1, "\u2039", t("Art précédent")), scene, fleche(1, "\u203A", t("Art suivant"))),
        el("div", { class: "ca-pied" }, nom, compteur),
    );
    function dessiner() {
        const o = options[idx];
        image.src = cardImageUrlHd(o.code === STANDARD ? picId : `${picId}_${o.code}`);
        const ce_tirage = ++tirage;
        const carte = cards.get(picId);
        const temoin = el("div", { class: "ca-cadre-pose" });
        cadre.append(temoin);
        void poserTraduction(temoin, image.src, picId, carte ? carte.traits : [], { scanAnglais: true })
            .then(() => { if (ce_tirage !== tirage) temoin.remove(); });
        for (const ancien of cadre.querySelectorAll(".ca-cadre-pose")) if (ancien !== temoin) ancien.remove();
        nom.textContent = o.nom;
        compteur.textContent = options.length > 1 ? `${idx + 1} / ${options.length}` : "";
        noeud.classList.toggle("ca-seul", options.length < 2 && !delegue);
    }
    dessiner();
    return {
        noeud,
        regler(code, nouveauFige) {
            figé = !!nouveauFige;
            const n = options.findIndex((o) => o.code === code);
            idx = n >= 0 ? n : 0;
            dessiner();
        },
        avancer(sens) { aller(idx + sens); },
        deleguer(fn) { delegue = fn; dessiner(); },
        masquer(gauche, droite) {
            noeud.classList.toggle("ca-sans-g", !!gauche);
            noeud.classList.toggle("ca-sans-d", !!droite);
        },
    };
}

/** La section « Carte de héros » de la modale : un carrousel par face, avec
 *  la case « même série pour les deux ». `choix.art` = face héros,
 *  `choix.artAE` = alter ego (null = il suit le héros). */
function sectionArtsHeros(h, choix, artsHeros, artsAlterEgo) {
    const base = String(h.heroCardId || "").split(",")[0];
    const numero = cleHeros(base);
    const codesAE = artsAlterEgo.map((a) => a.code);
    const liste = (arts) => [{ code: STANDARD, nom: t("Standard") }].concat(arts.map((a) => ({ code: a.code, nom: t(a.nom) })));
    const aUnAlterEgo = artsAlterEgo.length > 0;
    let memes = choix.artAE === null;

    const alterEgoAffiche = () => codeAlterEgoAffiche({ heros: choix.art, alterEgo: choix.artAE }, codesAE);
    const carrouselAE = aUnAlterEgo ? carrouselArts({
        titre: t("Face alter ego"), picId: `${numero}b`, options: liste(artsAlterEgo),
        actuel: alterEgoAffiche(), inactif: memes,
        surChoix: (code) => { choix.artAE = code; },
    }) : null;
    const carrouselHeros = carrouselArts({
        titre: t("Face héros"), picId: base, options: liste(artsHeros), actuel: choix.art,
        surChoix: (code) => {
            choix.art = code;
            if (carrouselAE && memes) carrouselAE.regler(alterEgoAffiche(), true);
        },
    });
    // « Même série » : une seule paire de flèches, à l'extérieur des deux
    // cartes (gauche de la face héros, droite de l'alter ego), qui fait défiler
    // les deux ensemble. Décochée : une paire par carte.
    const paireUnique = (oui) => {
        if (!carrouselAE) return;
        carrouselHeros.masquer(false, oui);
        carrouselAE.masquer(oui, false);
        carrouselAE.deleguer(oui ? (sens) => carrouselHeros.avancer(sens) : null);
    };
    paireUnique(memes);
    const zone = el("div", { class: "res-art ra-carrousels" },
        el("div", { class: "ra-tete" },
            el("span", { class: "ra-titre" }, t("Carte de héros")),
            el("span", { class: "ra-sous" }, t("Art alternatif, mêmes valeurs de jeu")),
        ),
    );
    if (aUnAlterEgo) {
        const case_ = el("input", { type: "checkbox", id: "ca-memes" });
        case_.checked = memes;
        case_.addEventListener("change", () => {
            memes = case_.checked;
            paireUnique(memes);
            if (memes) {
                choix.artAE = null;
                carrouselAE.regler(alterEgoAffiche(), true);
            } else {
                choix.artAE = alterEgoAffiche();
                carrouselAE.regler(choix.artAE, false);
            }
        });
        zone.append(el("label", { class: "ca-memes", for: "ca-memes" }, case_, t("Même série pour les deux faces")));
    }
    const rangee = el("div", { class: "ca-rangee" }, carrouselHeros.noeud, carrouselAE ? carrouselAE.noeud : null);
    if (aUnAlterEgo) {
        // Téléphone : une seule face à la fois, en grand (les onglets sont cachés sur ordinateur).
        const ongletH = el("button", { type: "button", class: "ca-onglet actif" }, t("Face héros"));
        const ongletAE = el("button", { type: "button", class: "ca-onglet" }, t("Face alter ego"));
        const voir = (ae) => {
            rangee.classList.toggle("vue-ae", ae);
            ongletH.classList.toggle("actif", !ae);
            ongletAE.classList.toggle("actif", ae);
        };
        ongletH.addEventListener("click", () => voir(false));
        ongletAE.addEventListener("click", () => voir(true));
        zone.append(el("div", { class: "ca-onglets" }, ongletH, ongletAE));
    }
    zone.append(rangee);
    return zone;
}

/* ---- La modale du vilain interchangeable (Fear No Evil, 18/09/2026) ------
   Une tuile par manigance ; au clic, les vilains « underling » portes pour
   elle, en vignettes (carte du vilain). Le choix envoie le scenario concret
   `<manigance>_<vilain>` et se memorise par manigance (prefs.setUnderling) :
   la tuile montre ensuite ce vilain, et la modale le pre-coche. */
function ouvrirModaleUnderling(tuile) {
    if (!tuile || !tuile.underlings || tuile.underlings.length < 2) return;
    const memoire = prefs.underlingsMemoire()[tuile.manigance];
    const choix = { vilain: (tuile.underlings.find((u) => u.id === memoire) || tuile.courant).id };
    const section = sectionVariantes(t("Vilain de ce scénario"), t("Choisis l'underling que la manigance affronte"),
        tuile.underlings.map((u) => ({ code: u.id, nom: u.nom, apercu: u.villainCardId })),
        choix.vilain, (code) => { choix.vilain = code; });
    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) { hideHover(); fermerModale(overlay); } } },
        el("div", { class: "deck-modal-panel vh-panel vh-compact", style: { "--sections": "1" } },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, tuile.name),
                el("span", { class: "dm-sub" }, t("Vilain de ce scénario")),
            ),
            section,
            el("div", { class: "vh-note" }, t("Mémorisé pour cette manigance sur cet appareil")),
            el("div", { class: "vh-actions" },
                el("button", { class: "tampon", onclick: () => { hideHover(); fermerModale(overlay); } }, t("Annuler")),
                el("button", { class: "tampon jaune", onclick: () => {
                    prefs.setUnderling(tuile.manigance, choix.vilain);
                    hideHover();
                    fermerModale(overlay);
                    verrouillerCible(scenarioDuVilain(tuile, choix.vilain));
                    // La tuile montre desormais le vilain choisi.
                    loadScnGrid();
                } }, t("Choisir")),
            ),
        ),
    );
    document.body.append(overlay);
}

function ouvrirModaleVariantes(i, h) {
    const p = state.players[i];
    if (!p || !h) return;
    const opts = optionsDuHeros(h, contexteVariantes(h));
    if (opts.aucune) return;
    // Le bouton qui apparaît sous la souris ne doit pas jouer le son de survol.
    couperSurvolPendant(400);
    const base = String(h.heroCardId || "").split(",")[0];
    const identites = h.variants || [];
    const choix = {
        version: p.version || h.id,
        identite: p.identity ? cleIdentite(p.identity) : (identites[0] ? cleIdentite(identites[0]) : ""),
        art: prefs.heroArt(h.heroCardId) || STANDARD,
        artAE: prefs.heroArtAlterEgo(h.heroCardId),
    };
    const artsAlterEgo = ARTS_ALTER_EGOS[cleHeros(base)] || [];
    const sections = [];
    if (opts.versions.length) {
        sections.push(sectionVariantes(t("Version du deck de héros"), t("Ce choix change le deck envoyé au jeu"),
            opts.versions.map((v) => ({ code: v.id, nom: t(v.nom), apercu: apercuVersion(h, v) })),
            choix.version, (code) => { choix.version = code; }));
    }
    if (opts.identites.length) {
        sections.push(sectionVariantes(t("Identité"), t("Mêmes capacités — le trait du héros change"),
            opts.identites.map((v) => ({ code: cleIdentite(v), nom: (v.distinctif && v.distinctif[0]) || v.name, apercu: v.heroCardId })),
            choix.identite, (code) => { choix.identite = code; }));
    }
    const avecArts = opts.arts.length > 0;
    if (avecArts) sections.push(sectionArtsHeros(h, choix, opts.arts, artsAlterEgo));
    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) { hideHover(); fermerModale(overlay); } } },
        // `--sections` : sur telephone, la feuille dimensionne ses vignettes
        // pour que TOUTES les sections tiennent sans defiler (prepare.css).
        el("div", { class: "deck-modal-panel vh-panel" + (avecArts ? " vh-arts" : " vh-compact"),
            style: { "--sections": String(sections.length), "--autres": String(sections.length - (avecArts ? 1 : 0)) } },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, nomAffiche(h)),
                el("span", { class: "dm-sub" }, t("Options de ce héros")),
            ),
            ...sections,
            el("div", { class: "vh-note" }, t(prefs.artsSurCompte() ? "Mémorisé pour ce héros sur ton compte" : "Mémorisé pour ce héros sur cet appareil")),
            el("div", { class: "vh-actions" },
                el("button", { class: "tampon", onclick: () => { hideHover(); fermerModale(overlay); } }, t("Annuler")),
                el("button", { class: "tampon jaune", onclick: () => {
                    // Appliquer : le deck de la version, l'identité, puis les
                    // préférences visuelles ; enfin la mémoire.
                    p.version = choix.version;
                    p.deck = deckDeLaVersion(h, choix.version);
                    p.deckSource = "base";
                    p.deckAuto = true;
                    p.deckChoisi = false; p.deckValide = false;
                    p.identity = identites.find((v) => cleIdentite(v) === choix.identite) || null;
                    prefs.setArtsHeros(h.heroCardId, choix.art, choix.artAE);
                    prefs.setVariantes(h.id, { version: choix.version, identite: choix.identite });
                    hideHover();
                    fermerModale(overlay);
                    render();
                } }, t("Valider")),
            ),
        ),
    );
    ouvrirModale(overlay);
}

/** L'art des cartes ressources doubles, à l'étape des decks (12/09/2026 :
 *  l'utilisateur ne voulait plus ce choix dans la modale du héros, « c'est
 *  vraiment dans le truc des decks »). Un choix par héros, mémorisé. */
function ouvrirModaleRessources(i, h) {
    const p = state.players[i];
    if (!p) return;
    let choix = prefs.resourceArt(h.heroCardId, collectionDuHeros(h.name, h.heroCardId));
    const section = sectionVariantes(t("Cartes ressources doubles"), t("Energy · Genius · Strength — même collection"),
        COLLECTIONS_RESSOURCES.map((c) => ({ code: c.code, nom: t(c.nom), trio: c.apercu || "" })),
        choix, (code) => { choix = code; });
    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) { hideHover(); fermerModale(overlay); } } },
        el("div", { class: "deck-modal-panel vh-panel", style: { "--sections": "1" } },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, nomAffiche(h)),
                el("span", { class: "dm-sub" }, t("Ressources : art alternatif")),
            ),
            section,
            el("div", { class: "vh-note" }, t("Mémorisé pour ce héros sur cet appareil")),
            el("div", { class: "vh-actions" },
                el("button", { class: "tampon", onclick: () => { hideHover(); fermerModale(overlay); } }, t("Annuler")),
                el("button", { class: "tampon jaune", onclick: () => {
                    prefs.setResourceArt(h.heroCardId, choix);
                    hideHover();
                    fermerModale(overlay);
                    render();
                } }, t("Valider")),
            ),
        ),
    );
    ouvrirModale(overlay);
}

/** Étape Decks : ce qui a été choisi dans la modale, et « Modifier ». */
function rappelVariantes(p, i) {
    const h = p && p.hero;
    if (!h) return null;
    const opts = optionsDuHeros(h, contexteVariantes(h));
    if (opts.aucune) return null;
    const parts = [];
    if (opts.versions.length) {
        const v = opts.versions.find((x) => x.id === (p.version || h.id));
        if (v) parts.push(t(v.nom));
    }
    if (opts.identites.length) {
        const v = p.identity || opts.identites[0];
        parts.push((v.distinctif && v.distinctif[0]) || v.name);
    }
    if (opts.arts.length) {
        const code = prefs.heroArt(h.heroCardId) || "standard";
        const a = opts.arts.find((x) => x.code === code);
        parts.push(t(a ? a.nom : "Standard"));
    }
    return el("div", { class: "tb-variantes-rappel" },
        el("span", { class: "tb-variantes-texte" }, parts.join(" · ")),
        el("button", { class: "tampon", onclick: () => ouvrirModaleVariantes(i, h) }, t("Modifier")),
    );
}

/* ---- Import marvelcdb ---- */
/** Import d'un deck marvelcdb DANS LE SLOT COURANT.
 *
 * Le héros du slot l'emporte sur celui du deck (09/09/2026). Un deck marvelcdb
 * mêle 15 cartes signature et 25 cartes d'aspect ; les signatures partent à la
 * conversion, et les 25 restantes ne tiennent à personne. Coller le lien d'un
 * deck de Spider-Man sur Iron Man donne donc Iron Man avec cette liste de
 * Justice, ce qui était jusqu'ici impossible : le champ basculait le slot sur
 * Spider-Man sans rien demander.
 *
 * Le héros du deck ne sert plus qu'à deux choses : nommer l'import, et servir
 * de héros de repli si le slot n'en a pas encore.
 */
async function importMarvelcdb(slotIndex, input) {
    const { id } = lireLien(input);
    if (!id) throw new Error(t("URL/ID marvelcdb invalide."));
    const trouve = await chargerDeck(input);
    if (!trouve) throw new Error(t("Deck introuvable sur marvelcdb ni mc4db") + " (ID " + id + "). " + t("Vérifie que le deck est public."));
    return importerDonnees(slotIndex, trouve.data, id, `marvelcdb ${id}`);
}

/** Import d'un fichier OCTGN (.o8d) dans le slot courant : mêmes règles que pour un lien. */
async function importO8d(slotIndex, texte, nomFichier) {
    const deckO8d = lireO8d(texte);
    if (!deckO8d) throw new Error(t("Ce fichier n’est pas un deck OCTGN (.o8d) lisible."));
    await cards.load();
    const parGuid = await tableGuid();
    const { slots, inconnues, total } = versSlots(deckO8d, {
        parGuid,
        existe: (code) => !!cards.get(code),
        parNom: indexParNom(cards.all()),
    });
    if (!Object.keys(slots).length) throw new Error(t("Aucune carte de ce fichier n’existe dans le jeu."));
    // Le héros du fichier, s'il y figure (une carte Héros ou Alter-ego connue du jeu).
    const codeHeros = Object.keys(slots).find((c) => { const k = cards.get(c); return k && /^(Hero|Alter-Ego)$/i.test(k.type || ""); }) || "";
    const nom = String(nomFichier || "").replace(/\.o8d$/i, "").replace(/^[0-9a-f]{8}-/i, "").replace(/_/g, " ").trim();
    const r = await importerDonnees(slotIndex, { name: nom || undefined, hero_code: codeHeros, slots }, "o8d", "octgn " + (nom || "o8d"));
    r.inconnues = inconnues;
    r.total = total;
    return r;
}

/** La table GUID OCTGN -> code, lue une fois (data/octgn_guids.json, voir tools/octgn_guids.py). */
let _tableGuid = null;
async function tableGuid() {
    if (_tableGuid) return _tableGuid;
    try {
        const r = await fetch("/read_file?data/octgn_guids.json");
        _tableGuid = r.ok ? await r.json() : {};
    } catch (e) { _tableGuid = {}; }
    return _tableGuid;
}

/** Le cœur de l'import : un deck {name, hero_code, slots} devient le deck du slot. */
async function importerDonnees(slotIndex, data, id, source) {
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
    const heroDuDeck = heroes.find((h) => memeHero(h.heroCardId))
        || heroes.find((h) => memeHero((h.deck.hero || [])[0]));
    const hero = (state.players[slotIndex] && state.players[slotIndex].hero) || heroDuDeck;
    // Plus de héros du tout : ni dans le slot, ni reconnu dans le deck.
    if (!hero) throw new Error(t("Le héros de ce deck n’est pas disponible dans le jeu."));
    // Nom : celui de marvelcdb, suivi du héros QUAND CE N'EST PAS LE SIEN.
    // Deux imports du même deck sur deux héros portent alors deux noms, ce que
    // la liste des decks sauvegardés ne saurait pas départager autrement.
    const nom = data.name || hero.name;
    const emprunte = !heroDuDeck || heroDuDeck.id !== hero.id;
    // La règle de conversion vit dans public/js/marvelcdb/conversion.js : le
    // panneau de recherche et ce champ « coller un lien » doivent produire
    // EXACTEMENT le même deck, sinon un deck jouable ici serait refusé là.
    const deck = versDeckMoteur(
        { id, nom: emprunte ? `${nom} (${hero.name})` : nom, cartes: data.slots || {} },
        hero.deck,
        (cid) => { const c = cards.get(cid); return (c && c.class) || ""; },
    );
    await verifierOuForcer(hero, deck, source);
    return { hero, deck };
}

/** Les cartes d'aspect d'un héros ne conviennent pas forcément à un autre :
 *  Spider-Woman en exige deux, Fatalis s'interdit les alliés, Ares plafonne ses
 *  emprunts. Le verdict est celui de l'ÉDITEUR DE DECK (js/deckbuilder/regles.js),
 *  pas une seconde règle écrite ici : un deck refusé au collage doit être
 *  exactement un deck que l'éditeur refuserait aussi. */
async function verifierOuForcer(hero, deck, source) {
    const verdict = validerDeck({
        hero, choisies: choisiesDuDeck(hero, deck), carte: (cid) => cards.get(cid), t,
    });
    if (verdict.ok) return;
    // Ni refus sec ni silence (07/10/2026) : nos regles de construction sont du
    // code et peuvent se tromper. La joueuse peut forcer, et forcer nous envoie
    // le deck et les raisons du refus (voir deck-force.js).
    const force = await demanderForcage({
        hero, deck, problemes: verdict.problemes, source, ecran: "préparation",
        nomCarte: (cid) => { const c = cards.get(cid); return c && c.name; }, t,
    });
    if (!force) { const e = new Error(t("Import annulé.")); e.annule = true; throw e; }
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
    // Téléphone : feuille basse, qu'on ferme en tirant la poignée vers le bas.
    const panneau = overlay.querySelector(".deck-modal-panel");
    if (panneau) ajouterPoignee(panneau, () => fermerModale(overlay));
}

/** Ce qui joue quand la fenêtre des options du héros se ferme : la carte qui surgit. */
let apresModaleVariantes = null;

function fermerModale(overlay) {
    // `isConnected` : sans lui, deux fermetures de suite (le clic dehors qui
    // suit le bouton) decompteraient deux fois et libereraient la page trop
    // tot, ou jamais.
    if (!overlay || !overlay.isConnected) return;
    const etaitVariantes = apresModaleVariantes && overlay.querySelector(".vh-panel");
    overlay.remove();
    _modalesOuvertes = Math.max(0, _modalesOuvertes - 1);
    if (etaitVariantes) {
        const suite = apresModaleVariantes;
        apresModaleVariantes = null;
        setTimeout(suite, 120);
    }
    if (_modalesOuvertes === 0) {
        document.documentElement.style.overflow = "";
        document.documentElement.style.removeProperty("--barre-defilement");
    }
}

/** Propose les arts alternatifs des cartes du deck de ce siège (ne fait rien sans carte concernée). */
function proposerArts(p) {
    if (!p || !p.deck || !p.hero) return;
    proposerArtsCartes({
        deck: p.deck, heros: p.hero.heroCardId, el, t, ouvrirModale, fermerModale,
        imageUrl: (pic) => cardImageUrl(pic),
        nomCarte: (cid) => { const c = cards.get(cid); return c ? c.name : cid; },
    });
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
                            (deckId ? "&deck=" + encodeURIComponent(deckId) : "") +
                            (state.legacy ? "&legacy=1" : "");
                        window.open(q, "_blank");
                    },
                }, t("Modifier")) : null,
                el("button", { class: "dm-close", onclick: () => { hideHover(); fermerModale(overlay); } }, "✕"),
            ),
            el("div", { class: "dm-grid" }, ...Object.keys(counts).map((id) =>
                el("div", { class: "dm-card" },
                    el("img", { src: cardImageUrl(picIdDeCarte(id, hero ? hero.heroCardId : "")), loading: "lazy", onmouseenter: auSurvol((e) => showCardHover(id, e.currentTarget)), onmouseleave: auSurvol(scheduleHide),
                        onclick: estTel() ? () => ouvrirCarteGrande(id) : undefined }),
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
    const criteres = { aspect: "", tag: "", texte: "", masquerIncomplets: true, tri: "date" };
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
            p.deck = deck; p.deckSource = "imported"; p.deckAuto = false; p.deckChoisi = true;
            fermerModale(overlay);
            render();
            proposerArts(p);
        };

        return el("div", { class: "cdb-ligne" + (d.jouable ? "" : " incomplet"), onclick: choisir },
            etoile,
            el("div", { class: "cdb-nom" },
                el("b", {}, d.nom),
                // Le rang dans le classement de popularite marvelcdb. Absent
                // pour la grande majorite des decks : le releve ne descend que
                // jusqu'a un certain rang, et ne pas y figurer ne veut PAS dire
                // impopulaire.
                d.rang ? el("span", { class: "cdb-rang", title: t("Rang dans les decks populaires de MarvelCDB") }, "#" + d.rang) : null,
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
                // ⚠ Le tri n'est propose QUE s'il y a de quoi trier : sans le
                // relevé de popularite (tools/marvelcdb_popularite.py jamais
                // lance), un menu « Les plus populaires » ne changerait rien a
                // l'ordre et mentirait au joueur.
                aDesRangs(paquet.decks)
                    ? el("select", { onchange: (e) => { criteres.tri = e.target.value; rendre(); } },
                        opt("date", t("Les plus récents")),
                        opt("populaire", t("Les plus populaires")))
                    : null,
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
    state.modifDeck = false;
    if (enLigne()) state.activeSlot = 0;
    else if (decksSequentiels()) {
        const k = premierSiegeAValider();
        if (k >= 0) state.activeSlot = k;
    }
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
        estTel() ? null : el("div", { class: "tb-equipe", id: "tb-equipe" }),
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
    if (estTel()) return rendreSceneDeckTel();
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    const p = state.players[state.activeSlot];
    const h = p && p.hero;
    if (!h) {
        poser(scene,
            el("div", { class: "tb-art vide" }),
            el("div", { class: "tb-trame" }),
            el("div", { class: "tb-nomg" }, el("small", {}, t("Arsenal")), t("Aucun héros")));
        ajusterNomGeant(scene);
        return;
    }
    const st = deckAffiche(p) ? deckStats(p.deck) : null;
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
            deckAffiche(p) ? el("span", { class: "tampon jaune" }, cleanNomDeck(p.deck.name) || t("Deck de base")) : null,
            (!deckAffiche(p) && decksSequentiels()) ? el("span", { class: "tampon" }, t("Aucun deck choisi")) : null,
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
    if (!p || !p.hero || enRecap()) { poser(zone); return; }
    if (estTel()) {
        // Téléphone : trois gros boutons au-dessus de la liste ; l'import
        // passe dans une feuille basse (le champ n'est plus posé en pleine page).
        poser(zone,
            el("div", { class: "tel-outils" },
                el("button", { class: "tampon jaune", onclick: () => ouvrirFeuilleImport(i) }, picto("fa-download"), " ", t("Importer")),
                el("button", {
                    class: "tampon",
                    onclick: () => { window.open("/deck-builder.html?hero=" + encodeURIComponent(p.hero.id)
                                                 + (state.legacy ? "&legacy=1" : ""), "_blank"); },
                }, picto("fa-pencil"), " ", t("Éditeur de deck")),
                el("button", { class: "tampon", onclick: () => ouvrirModaleRessources(i, p.hero) }, picto("fa-th"), " ", t("Ressources")),
            ),
            rappelVariantes(p, i),
        );
        return;
    }
    poser(zone,
        el("div", { class: "tb-menace-ligne" },
            el("input", { class: "search tb-search", id: "mcdb-" + i, placeholder: t("Colle une URL ou un ID marvelcdb ou mc4db...") }),
            el("button", { class: "tampon", onclick: () => doImport(i) }, "Import"),
            el("button", {
                class: "tampon",
                title: t("Importer un deck OCTGN (fichier .o8d)"),
                onclick: () => document.getElementById("o8d-" + i).click(),
            }, t("Fichier OCTGN (.o8d)")),
            el("input", {
                type: "file", id: "o8d-" + i, accept: ".o8d,.xml,text/xml", hidden: true,
                onchange: async (e) => {
                    const f = e.target.files && e.target.files[0]; e.target.value = "";
                    if (f) await doImport(i, f);
                },
            }),
            el("button", {
                class: "tampon",
                title: t("Parcourir les decks publiés sur MarvelCDB"),
                onclick: () => ouvrirPanneauCdb(i),
            }, t("Decks MarvelCDB")),
            el("button", {
                class: "tampon",
                title: t("Construire un deck personnalisé pour ce héros"),
                onclick: () => { window.open("/deck-builder.html?hero=" + encodeURIComponent(p.hero.id)
                                             + (state.legacy ? "&legacy=1" : ""), "_blank"); },
            }, t("Éditeur de deck")),
            el("button", {
                class: "tampon tb-ressources",
                title: t("Choisir le dessin des cartes Energy, Genius et Strength de ce deck"),
                onclick: () => ouvrirModaleRessources(i, p.hero),
            }, t("Ressources : art alternatif")),
            el("span", { class: "mcdb-status", id: "mcdb-st-" + i }),
        ),
        // Version, identité, art de la carte de héros : dans la modale du
        // héros (11/09/2026), ici un rappel et « Modifier ». Les ressources,
        // elles, ont leur bouton juste au-dessus (12/09/2026).
        rappelVariantes(p, i),
    );
}

async function doImport(i, fichier) {
    const input = document.getElementById("mcdb-" + i);
    const status = document.getElementById("mcdb-st-" + i);
    if (!fichier && (!input || !input.value.trim())) return false;
    if (status) status.textContent = t("Import en cours...");
    try {
        const { hero, deck, inconnues } = fichier
            ? await importO8d(i, await fichier.text(), fichier.name)
            : await importMarvelcdb(i, input.value);
        const p = state.players[i];
        p.hero = hero; p.deck = deck; p.deckSource = "imported"; p.deckAuto = false; p.deckChoisi = true;
        // Les lignes d'un fichier OCTGN qu'aucun GUID ni aucun nom n'a retrouvees : dites, pas tues.
        const manque = (inconnues || []).length
            ? `\n\n${t("Cartes non reprises (inconnues du jeu, souvent les cartes propres à un autre héros) :")} ` + inconnues.map((c) => `${c.qte}× ${c.nom}`).join(", ")
            : "";
        if (window.confirm(`Deck \u00ab ${deck.name} \u00bb ${t("importé")} (${deck.player_deck.length} ${t("cartes")}).${manque}\n\n${t("Le sauvegarder pour plus tard ?")}`)) {
            // ⚠ SUR LE SERVEUR, pas dans le cache du navigateur : un deck range
            // dans le localStorage ne suit pas d'un appareil a l'autre et
            // disparait avec le cache. Voir decks-serveur.js.
            const surLeServeur = await sauverDeck(deck);
            if (!surLeServeur && status) {
                status.textContent = t("Deck gardé sur cet appareil seulement : le serveur n'a pas répondu.");
            }
        }
        render();
        proposerArts(p);
        return true;
    } catch (e) {
        if (status) status.textContent = "";
        if (e && e.annule) return false;
        alert(t("Échec de l’import :") + " " + e.message);
        return false;
    }
}

/** Joueurs dont les paquets d'aspect sont dépliés. Voir loadDecks(). */
const aspectsDeplies = new Set();
/** Meme chose pour la section des decks du tableur. */
const tableurDeplies = new Set();

/** D'ou vient le tableur, en une phrase (info-bulle de la section : ca ne prend
 *  aucune place a l'ecran). Voir aussi credits.html. */
const CREDIT_TABLEUR = "Decks du fichier « Marvel Champions Universal Prebuilt Decks » de acharlie1377 (Austin Charlie), sur BoardGameGeek. Conçus par un joueur : ce ne sont pas les decks officiels des héros.";

/** « Cyclops — Prebuilt » du tableur ne doit pas se confondre avec le deck de depart. */
function nomDeckAffiche(dk) {
    const nom = cleanNomDeck(dk.name);
    if (dk.source !== "tableur") return nom;
    return nom
        .replace(/\s*[—-]\s*Prebuilt\s*$/i, " — " + t("Version tableur"))
        .replace(/\s*[—-]\s*Mutant\s*$/i, " — " + t("Version tableur, mutant"));
}

/** Le panneau recapitulatif : un heros par ligne, son deck, et « Modifier ». */
function rendreRecapDecks() {
    const box = document.getElementById("deck-liste");
    if (!box) return;
    const compte = document.getElementById("tb-compte");
    if (compte) compte.textContent = "";
    box.replaceChildren(el("div", { class: "deck-recap", id: "deck-recap", style: { gridColumn: "1 / -1", display: "flex", flexDirection: "column", gap: "10px" } },
        el("b", { style: { fontSize: "18px", letterSpacing: ".04em", textTransform: "uppercase" } }, t("Récapitulatif des decks")),
        ...activePlayers().map((pl, idx) => el("div", {
            class: "tb-deck recap-ligne", "data-siege": String(idx),
            style: { display: "flex", alignItems: "center", gap: "14px", cursor: "default" },
        },
            el("span", { class: "tb-siege plein petit" }, portraitHeros(pl.hero)),
            el("span", { style: { flex: "1" } },
                el("div", { class: "do-name" }, nomAffiche(pl.hero)),
                el("div", { class: "do-size" }, cleanNomDeck(pl.deck.name) || t("Deck de base"))),
            el("button", {
                type: "button", class: "tampon", "data-modifier": String(idx),
                onclick: () => {
                    state.activeSlot = idx; state.modifDeck = true;
                    rendreSceneDeck(); rendreOutilsDeck(); rendreEquipe(); loadDecks(idx); majNav();
                },
            }, t("Modifier"))))));
}

async function loadDecks(i) {
    if (enRecap()) { rendreSceneDeck(); rendreRecapDecks(); return; }
    const p = state.players[i];
    await cards.load();
    const catDecks = await catalog.decksForHero(p.hero);
    // UN DECK IMPORTE NE SE LISTE QU'UNE FOIS (07/10/2026). Il vit dans
    // deck/serveur-<place>/ : le catalogue le liste deja (toutes les sources de
    // /list_deck), et `decksSauvegardesPourHeros` le rendait une seconde fois.
    // On ne garde ici que ce que le catalogue n'a pas vu (le cache du
    // navigateur, quand le serveur ne repond pas).
    const dejaListes = new Set(catDecks.filter((dk) => dk.source === "saved").map((dk) => dk.deck && dk.deck.name));
    const saved = (await decksSauvegardesPourHeros(p.hero.heroCardId)).filter((d) => !dejaListes.has(d.name)).map((d, idx) => ({
        id: "saved-" + idx, name: d.name || t("Deck importé"), source: "saved", deck: d,
        aspects: [...new Set((d.player_deck || []).map((id) => cards.aspectOf(id)).filter((a) => a && a !== "basic"))],
    }));
    let decks = [...catDecks, ...saved];
    // Legacy : un deck tout fait qui contient une carte d'une boîte pas encore
    // ouverte est CACHÉ (décision de l'utilisateur, 13/09/2026). Le filtrer
    // carte par carte le laisserait sous les 40 obligatoires ; le montrer
    // fermé n'apporterait rien, on ne le débloque pas d'un clic. Le deck de
    // base, lui, vient du paquet du héros : il passe toujours.
    if (state.legacy) decks = decks.filter((d) => state.legacy.dispo.deck(d.deck).ouvert);
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
    // Parcours sequentiel : aucun deck n'est presélectionné, le joueur choisit.
    if (p.deckAuto && decksSequentiels()) p.deckAuto = false;
    else if (p.deckAuto) {
        p.deckAuto = false;
        const dernierId = prefs.lastDeckFor(p.hero.heroCardId);
        let dk = dernierId != null ? decks.find((d) => d.id === dernierId) : null;
        // Sans deck de base (player_deck vide : PROCESSUS-HEROS etape 3), le
        // deck pose a l'assignation ne fait que 15 cartes et ne se joue pas :
        // le premier paquet d'aspect (conseille en tete) prend sa place.
        if (!dk && !aDeckDeBase(p.hero)) {
            dk = decks.find((d) => d.source === "aspect" && verifierDeck(d.deck).length === 0)
                || decks.find((d) => d.source === "aspect") || null;
        }
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
        const on = deckAffiche(p) && p.deckSource === dk.source && p.deck.name === dk.deck.name;
        const st = deckStats(dk.deck);
        // Parcours sequentiel : repere (sans selection) du dernier deck joue avec ce heros.
        const dernierUtilise = decksSequentiels() && dk.source !== "campagne" && String(prefs.lastDeckFor(p.hero.heroCardId)) === String(dk.id);
        // Contrôle de construction : signalé, jamais bloquant.
        const ecarts = verifierDeck(dk.deck);
        const etiquette = dk.source === "base" ? t("Deck de départ")
            : dk.source === "aspect" ? (dk.recommande ? t("Conseillé") : t("Paquet"))
            : dk.source === "tableur" ? t("Tableur")
            : dk.source === "campagne" ? t("En cours")
            : t("Sauvegardé");
        const choisir = () => {
            // Parcours sequentiel : un AUTRE deck sur un heros valide retire sa validation.
            if (decksSequentiels() && p.deckValide && !on) p.deckValide = false;
            p.deck = dk.deck; p.deckSource = dk.source; p.deckAuto = false; p.deckChoisi = true;
            // « campagne » n'existe que sur cet ecran-ci : le retenir comme
            // dernier deck du heros ne designerait plus rien demain.
            if (dk.source !== "campagne") prefs.setLastDeck(p.hero.heroCardId, dk.id);
            loadDecks(i);
            rendreSceneDeck();
            rendreEquipe();
            majNav();
            proposerArts(p);
        };
        const supprimable = dk.source === "saved" && !String(dk.id).startsWith("saved-");
        const supprimer = async () => {
            if (on) { alert(t("Choisis d'abord un autre deck, celui-ci est en cours d'utilisation.")); return; }
            if (!window.confirm(`${t("Supprimer ce deck ?")}\n\n${dk.deck.name}`)) return;
            try { await supprimerDeck(dk.id); } catch (e) { alert(t("Suppression impossible :") + " " + e.message); return; }
            loadDecks(i);
        };
        // Téléphone : une carte empilée par deck. Plus d'élément interactif
        // imbriqué (la carte entière n'est plus un bouton) : deux vrais boutons.
        if (estTel()) {
            return el("article", { class: "tb-deck tel-deck" + (on ? " chosen" : "") },
                el("div", { class: "do-name" }, nomDeckAffiche(dk)),
                el("div", { class: "do-tags" },
                    el("span", { class: "tag" }, etiquette),
                    ...dk.aspects.map((a) => el("span", { class: "tag asp", style: { background: ASPECTS[a] || "#555" } }, a)),
                ),
                aspectBar(st),
                el("div", { class: "do-foot" },
                    el("span", { class: "do-size" }, st.total + " " + t("cartes")),
                    ...(ecarts.length
                        ? [el("span", { class: "do-alerte", title: ecarts.join(" · ") }, "⚠ " + t("Hors règles"))]
                        : [])),
                el("div", { class: "tel-deck-actions" },
                    el("button", { class: "ts-btn", type: "button", onclick: () => showDeckCards(dk.deck, p.hero, dk.id) }, picto("fa-th"), " ", t("Voir les cartes")),
                    ...(supprimable ? [el("button", { class: "ts-btn", type: "button", onclick: supprimer }, t("Supprimer"))] : []),
                    el("button", { class: "ts-btn jaune", type: "button", onclick: choisir }, on ? picto("fa-check") : null, on ? " " : null, on ? t("Choisi") : t("Choisir"))),
            );
        }
        return el("button", {
            class: "tb-deck" + (on ? " chosen" : ""),
            onclick: choisir,
        },
            el("div", { class: "do-name" }, nomDeckAffiche(dk)),
            el("div", { class: "do-tags" },
                el("span", { class: "tag" }, etiquette),
                ...(dernierUtilise ? [el("span", { class: "tag dernier" }, t("Dernier utilisé"))] : []),
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
                ...(supprimable ? [el("span", { class: "do-view", onclick: (e) => { e.stopPropagation(); e.preventDefault(); supprimer(); } }, t("Supprimer"))] : []),
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
    const principaux = decks.filter((dk) => dk.source !== "aspect" && dk.source !== "tableur");
    const aspects = decks.filter((dk) => dk.source === "aspect");
    const duTableur = decks.filter((dk) => dk.source === "tableur");
    const enfants = principaux.map(option);

    // Les decks par heros du tableur : leur propre section repliee, avec
    // l'origine (et l'auteur) dans l'info-bulle, sans rien ajouter a l'ecran.
    if (duTableur.length) {
        const deplieT = tableurDeplies.has(i);
        const listeT = el("div", { class: "deck-aspects" + (deplieT ? " est-deplie" : "") },
            ...duTableur.map(option));
        const bascule = el("button", {
            type: "button",
            class: "deck-aspects-bascule" + (deplieT ? " est-deplie" : ""),
            "aria-expanded": deplieT ? "true" : "false",
            title: t(CREDIT_TABLEUR),
        }, `${t("Decks du tableur")} (${duTableur.length}) ⓘ`);
        bascule.addEventListener("click", () => {
            const ouvert = !tableurDeplies.has(i);
            if (ouvert) tableurDeplies.add(i); else tableurDeplies.delete(i);
            listeT.classList.toggle("est-deplie", ouvert);
            bascule.classList.toggle("est-deplie", ouvert);
            bascule.setAttribute("aria-expanded", ouvert ? "true" : "false");
        });
        enfants.push(bascule, listeT);
    }

    if (aspects.length) {
        // Sans deck de base, les paquets SONT le choix : ils s'ouvrent d'office.
        if (!aDeckDeBase(p.hero)) aspectsDeplies.add(i);
        const deplie = aspectsDeplies.has(i);
        const liste = el("div", { class: "deck-aspects" + (deplie ? " est-deplie" : "") },
            ...aspects.map(option));
        const bascule = el("button", {
            type: "button",
            class: "deck-aspects-bascule" + (deplie ? " est-deplie" : ""),
            "aria-expanded": deplie ? "true" : "false",
        }, `${t("Paquets d’aspect")} (${aspects.length})`);
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
    // Une copie partage le titre ET le sous-titre (RR « Copy »), comme dans
    // deckbuilder/regles.js : les allies « Spider-Woman » de Madame Web, aux
    // sous-titres differents, ne sont pas des copies.
    const personnalisable = deck.player_deck || [];
    const cleCopie = (id) => { const c = cards.get(id); return `${_titre(id)}|${(c && c.subtitle) || ""}`; };
    const parTitre = new Map();
    for (const id of personnalisable) {
        const cle = cleCopie(id);
        parTitre.set(cle, (parTitre.get(cle) || 0) + 1);
    }
    for (const [cle, nombre] of parTitre) {
        const id = personnalisable.find((x) => cleCopie(x) === cle);
        const titre = _titre(id);
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

/** Le cri du méchant quand on verrouille la cible.
 *
 *  ⚠ PAR NOM DE MÉCHANT, PAS PAR SCÉNARIO (constat de l'utilisateur,
 *  08/09/2026 : « surtout les méchants n'avaient pas vraiment de phrase »).
 *  La table était indexée par identifiant de scénario, et la moitié des
 *  identifiants ne correspondaient plus (« kang » pour
 *  the_once_and_future_kang, « collector » pour infiltrate_the_museum) :
 *  les défis, les scénarios fan-made et les vagues récentes tombaient tous
 *  sur « RAAAH ! ». Un scénario porte le cri de son PREMIER méchant ; les
 *  scénarios sans méchant fixe (une bande, une horde) ont leur entrée à
 *  part, par identifiant. Repli : « RAAAH ! ». */
const CRIS_MECHANTS = {
    "rhino": "CHARGE !", "klaw": "SONIC BOOM !", "ultron": "I AM ULTRON !",
    "norman osborn": "HA HA HA !", "green goblin": "PUMPKIN BOMB !", "crossbones": "FOR THE SKULL !",
    "absorbing man": "ABSORBED !", "taskmaster": "COPIED !", "zola": "FOR SCIENCE !", "red skull": "HAIL HYDRA !",
    "wrecker": "WRECK IT !", "kang": "ALL HAIL KANG !", "drang": "FOR BADOON !", "collector": "FOR MY COLLECTION !",
    "nebula": "NO MERCY !", "ronan the accuser": "GUILTY !", "ebony maw": "HEAR ME AND REJOICE !",
    "proxima midnight": "FOR THANOS !", "thanos": "I AM INEVITABLE !", "hela": "HEL AWAITS !", "loki": "MISCHIEF !",
    "the hood": "BANG BANG !", "sandman": "SANDSTORM !", "venom": "WE ARE VENOM !", "mysterio": "SMOKE AND MIRRORS !",
    "doctor octopus": "SUPERIOR !", "venom goblin": "HA HA HISSS !", "sabretooth": "RRRAAAWR !",
    "sentinel": "MUTANT DETECTED !", "master mold": "SENTINELS, RISE !", "magneto": "NEVER AGAIN !", "magog": "FOR MOJO !",
    "spiral": "SIX BLADES !", "mojo": "RATINGS !", "juggernaut": "I'M THE JUGGERNAUT !", "mister sinister": "PERFECTION !",
    "stryfe": "CHAOS !", "unus": "UNTOUCHABLE !", "apocalypse": "THE STRONG SURVIVE !", "dark beast": "EXPERIMENT !",
    "black widow": "WIDOW'S BITE !", "batroc": "ZUT ALORS !", "m.o.d.o.k.": "DESIGNED ONLY FOR KILLING !", "baron zemo": "MASTERS OF EVIL !",
    "enchantress": "ENTHRALLED !", "iron man": "I AM IRON MAN !", "captain marvel": "BINARY !",
    "captain america": "SHIELD BASH !", "spider-woman": "VENOM BLAST !", "she-hulk": "SMASH !", "vision": "PHASE !",
    "the spot": "PORTAL !", "shocker": "VIBRO-SHOCK !", "electro": "ZZZAP !", "the lizard": "HISSS !",
    "vulture": "SCREECH !", "kingpin": "JUST BUSINESS !", "gorr the god butcher": "GODS MUST DIE !",
};
const CRIS_SCENARIOS = {
    the_wrecking_crew: "WRECK IT !", "2423_the_wreckoning": "WRECK IT !", sinister_six: "SINISTER SIX !",
    mansion_attack: "BROTHERHOOD !", morlock_siege: "MARAUDERS !", on_the_run: "MARAUDERS !", four_horsemen: "HORSEMEN, RIDE !",
    thunderbolts: "JUSTICE, LIKE LIGHTNING !", god_of_lies: "SWEET LIES !", hydra_patrol: "HAIL HYDRA !", hydra_assault: "HAIL HYDRA !",
    brood: "SKREEE !",
};
function criDuMechant(sc) {
    if (CRIS_SCENARIOS[sc.id]) return CRIS_SCENARIOS[sc.id];
    const nom = nomPropre((sc.villainNames || [])[0]);
    // « Kang (The Conqueror) » crie comme « Kang » ; « Avalanche A » comme « Avalanche ».
    const racine = nom.replace(/\s*\(.*\)$/, "").replace(/\s+[ab]$/, "");
    return CRIS_MECHANTS[nom] || CRIS_MECHANTS[racine] || "RAAAH !";
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
        el("div", { class: "tb-merci", id: "tb-merci-vilains", hidden: true }),
        el("div", { class: "hero-grid tb-roster tb-roster-scn", id: "scn-grid" }),
        // Le niveau de menace, ici même : c'est en voyant le méchant qu'on
        // décide de la difficulté, pas un écran plus loin.
        el("div", { class: "tb-menace", id: "tb-menace" }),
        estTel() ? null : el("div", { class: "tb-equipe", id: "tb-equipe" }),
    );
    wrap.append(droite);
    mechantApercuTel = null;
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
    if (estTel()) return rendreSceneMechantTel(sc);
    const scene = document.getElementById("tb-scene");
    if (!scene) return;
    if (!sc) {
        poser(scene,
            el("div", { class: "tb-art vide" }),
            el("div", { class: "tb-trame" }),
            el("div", { class: "tb-nomg" }, el("small", {}, t("Méchant")), t("Choisis un méchant")),
        );
        ajusterNomGeant(scene);
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
            el("small", {}, libelleExtension({ key: sc.extension }, _auteursExtensions.get(sc.extension))),
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
        el("div", { class: "tb-bas" }, documentsDeLaCible(sc, true), bioDuMechant(sc)),
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
        detailRow(t("Sets requis"), sc.mandatoryEncounterSets.map(nomSetRencontre).join(", ") || "-"),
        detailRow(t("Sets recommandés"), sc.recommendedModularSets.map(nomSetRencontre).join(", ") || "-"),
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
    jouerSon(SON.cible);
    jouerReplique(sc.id, "mechant");
    selectScenario(sc);
    rendreSceneMechant(sc);
    rendreMenace();
    rendreTable();
    document.querySelectorAll(".tb-port").forEach((b) => {
        // Une tuile de manigance interchangeable porte plusieurs scenarios (data-scns).
        const siens = String(b.dataset.scns || b.dataset.scn || "").split(",");
        b.classList.toggle("chosen", b.dataset.scn === sc.id || siens.includes(sc.id));
    });
    const scene = document.getElementById("tb-scene");
    if (scene) {
        const cri = criDuMechant(sc);
        const eclair = el("div", { class: "tb-eclair" },
            el("img", { src: cardImageUrlHd((sc.villainCards || [])[0] || sc.tileImage), alt: "" }),
            el("span", { class: "ono rouge" }, cri),
        );
        scene.append(eclair);
        eclair.addEventListener("animationend", (ev) => { if (ev.target === eclair) eclair.remove(); });
        setTimeout(() => eclair.remove(), 2800);   // filet, un peu apres la fin de l'animation
    }
    majNav();
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
            // ⚠ TROIS NIVEAUX, PLUS UN SEUL BOUTON (16/09/2026). Les cartes de
            // Standard II et III etaient scriptees depuis toujours et
            // INCHOISISSABLES : celles de Standard II n'avaient jamais ete
            // jouees. Cliquer un niveau repasse aussi en Standard, sinon le
            // joueur en Expert changerait un reglage sans voir son bouton
            // s'allumer.
            ...NIVEAUX_STANDARD.map((niveau) => regle(
                libelleNiveau(niveau),
                d.base === "standard" && d.standard === niveau,
                () => { d.base = "standard"; d.standard = niveau; },
            )),
            // Expert garde le niveau choisi : dans le jeu, il s'ajoute au
            // Standard, il ne le remplace pas.
            sc.hasExpertVariant ? regle("Expert", d.base === "expert", () => { d.base = "expert"; }) : null,
            regle("Skirmish", d.skirmish, () => { d.skirmish = !d.skirmish; }),
            heroique,
        ),
        el("div", { class: "tb-menace-ligne" },
            el("span", { class: "tb-menace-k" }, t("Sets modulaires")),
            regle(t("Recommandés"), d.modularConfig === "recommended", () => { d.modularConfig = "recommended"; applyModularConfig(); }),
            regle(t("Personnalisés"), d.modularConfig === "custom", () => {
                d.modularConfig = "custom";
                // Le choix des sets s'ouvre a DROITE, a la place du mechant (16/10/2026), sur PC.
                if (!estTel()) setTimeout(ouvrirPanneauModulaires, 0);
            }),
            regle(t("Aléatoire"), d.modularConfig === "random", () => { d.modularConfig = "random"; applyModularConfig(); }),
        ),
        el("div", { class: "mod-chips", id: "modular-box" }),
        caseIntenseCombatants(sc),
        estBataille() ? blocSecondeTable() : null,
    );
    renderModular();
}

/**
 * te201 Intense Combatants : la case n'existe que pour un scenario qui joue
 * TMNT Standard ou TMNT Expert (« TMNT Standard and Expert only »). Decochee
 * par defaut ; le lanceur en tire la regle `tmnt_intense_combatants`.
 * L'aide reprend le texte FR de la carte (textes-fr-fanmade).
 */
let texteIntense = null;
function caseIntenseCombatants(sc) {
    if (!sc || !proposerIntense(sc.mandatoryEncounterSets)) return null;
    if (texteIntense === null) {
        texteIntense = "";
        texteIntenseFr().then((txt) => { texteIntense = txt; if (txt) rendreMenace(); });
    }
    const d = state.difficulty;
    // En anglais, le texte imprime de la carte ; en francais, sa traduction.
    const carte = langueActuelle() === "en" ? cards.get(CARTE_INTENSE) : null;
    const texte = carte ? texteSansBalises(carte.text) : texteIntense;
    const regle = texte.search(/Interruption forcée|Forced Interrupt/);
    return el("div", { class: "tb-menace-ligne intense-combatants", title: texte || undefined },
        el("span", { class: "tb-menace-k" }, t("Environnement")),
        el("label", { class: "cj-chk" },
            el("input", {
                type: "checkbox",
                name: "intense-combatants",
                checked: d.intenseCombatants === true || undefined,
                onchange: (e) => { d.intenseCombatants = e.target.checked; },
            }),
            el("span", {}, t("Intense Combatants (environnement optionnel)"))),
        texte
            ? el("span", { class: "tb-menace-vide" }, regle >= 0 ? texte.slice(regle) : texte)
            : null,
    );
}

/** La table qui se compose : l'équipe, puis la cible verrouillée. */
function rendreTable() {
    const zone = document.getElementById("tb-equipe");
    if (!zone) return;
    const membres = activePlayers().filter((p) => p.hero).map((p) => el("div", {
        class: "tb-siege plein petit",
        title: nomAffiche(p.hero),
    }, portraitHeros(p.hero), el("span", { class: "tb-siege-nom" }, nomAffiche(p.hero))));
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
                    // Anglais, comme les portraits de heros juste a cote : ces
                    // deux rangees se lisent ensemble.
                    el("div", { class: "portrait", style: { backgroundImage: `url("${cardImageUrlEn(id)}")` } }),
                    el("span", { class: "tb-siege-nom" }, nom));
            })
            : [sc
                ? el("div", { class: "tb-siege plein petit eux", title: sc.name },
                    el("div", { class: "portrait", style: { backgroundImage: `url("${cardImageUrlEn(sc.tileImage)}")` } }),
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
        const opt = el("option", { value: sc.id }, sc.name + " · " + nomExtension(sc.extension, langueActuelle()));
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
function documentsDeLaCible(sc, enTampons = false) {
    if (!sc || !sc.extension) return null;
    const livret = livretDExtension(sc.extension);
    const carnet = carnetDExtension(sc.extension);
    if (!livret && !carnet) return null;
    const lien = (fiche, libelle) => fiche
        ? el("a", {
            class: enTampons ? "tampon target-doc" : "target-doc",
            href: "/" + encodeURIComponent(fiche.fichier),
            target: "_blank",
            rel: "noopener",
        }, picto("fa-book"), " " + t(libelle))
        : null;
    // Sur la scène du PC, les liens s'alignent dans la rangée du pied de scène,
    // comme « Voir ses cartes » chez le héros.
    if (enTampons) return [lien(livret, "Livret de règles"), lien(carnet, "Carnet de campagne")];
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
    // Le dernier scénario joué est fan-made : le filtre s'allume pour qu'il reste visible.
    state.extFanmade = /custom/i.test(ext.key);
    state.extensionTab = ext.key;
    selectScenario(sc);
    return true;
}

/** Le libelle d'une extension FAN-MADE : « Nom (Createur) », comme pour les heros
 *  (demande du 16/10/2026 : « Custom (Web of Deceit) » devient « Web of Deceit (Gwenpool) »).
 *  Le createur se retrouve par les sets de rencontre de l'extension, a defaut par
 *  l'un de ses heros. Sans createur sur : « Nom » seul. Un officiel ne change pas. */
const _auteursExtensions = new Map();
async function auteurDeExtension(e) {
    if (_auteursExtensions.has(e.key)) return _auteursExtensions.get(e.key);
    const interne = e.key.match(/\((.*)\)\s*$/);
    let auteur = interne ? auteurConnuDeLExtension(interne[1]) : "";
    for (const enc of auteur ? [] : (e.encounters || [])) { auteur = catalog.auteurSetRencontre(enc); if (auteur) break; }
    if (!auteur) {
        const heros = await catalog.heroes();
        const h = heros.find((x) => x.extension === e.key && x.auteur);
        auteur = h ? h.auteur : "";
    }
    _auteursExtensions.set(e.key, auteur);
    return auteur;
}
function libelleExtension(e, auteur) {
    const nom = nomExtension(e.key, langueActuelle());
    const interne = nom.match(/^Custom \((.*)\)$/i);
    return interne ? nomAvecAuteur(interne[1], auteur, true) : nom;
}

async function loadExtTabs() {
    await preselectionDernierScenario();
    // « Weekly Challenges » et « Défis » ne se choisissent plus ici (17/10/2026, demande de l'utilisateur).
    const toutes = (await catalog.extensions()).filter((e) => e.scenarios.length
        && e.key !== "defis" && !/weekly/i.test(e.key));
    const nbFanmade = toutes.filter((e) => /custom/i.test(e.key)).length;
    // Le filtre « Fan-made » (16/10/2026, selection du mechant en trois colonnes) :
    // decoche = les officielles seules, coche = les fan-made seules, comme sur l'ecran des heros.
    // Décoché (19/10/2026) : seulement les boîtes officielles ; coché : seulement les fan-made, comme pour les héros.
    const exts = toutes.filter((e) => /custom/i.test(e.key) === !!state.extFanmade);
    // Si l'onglet courant n'existe plus dans la liste, on le recale.
    const validKeys = new Set(exts.map((e) => e.key));
    if (!state.extensionTab || !validKeys.has(state.extensionTab)) {
        state.extensionTab = exts[0] ? exts[0].key : null;
    }
    const tabs = document.getElementById("ext-tabs");
    if (!tabs) return;
    const auteurs = new Map();
    for (const e of exts) if (/custom/i.test(e.key)) auteurs.set(e.key, await auteurDeExtension(e));
    const filtre = el("button", {
        class: "ext-fanmade" + (state.extFanmade ? " on" : ""),
        "aria-pressed": state.extFanmade ? "true" : "false",
        onclick: () => { state.extFanmade = !state.extFanmade; loadExtTabs(); },
    }, `${t("Fan-made")} (${nbFanmade})`);
    // Le bouton vit dans l'en-tete du panneau (pas dans la grille des boites : il lui
    // volerait une rangee), a cote du compte de scenarios.
    const entete = tabs.parentElement && tabs.parentElement.querySelector(".tb-entete");
    if (entete) {
        entete.querySelectorAll(".ext-fanmade").forEach((x) => x.remove());
        entete.insertBefore(filtre, entete.querySelector(".tb-mode"));
    }
    majMerciVilains();
    tabs.replaceChildren(...exts.map((e) => el("button", {
        class: "ext-tab cut" + (state.extensionTab === e.key ? " on" : ""),
        // Plus de fenetre au survol d'une extension (23/10/2026, demande de l'utilisateur) : ni l'apercu en grand (`showExtHover`) ni
        // l'infobulle du navigateur (« 56. Civil War »).
        "aria-label": e.key === "defis" ? t("Défis") : libelleExtension(e, auteurs.get(e.key)),
        onclick: () => { hideHover(); state.extensionTab = e.key; loadExtTabs(); loadScnGrid(); },
    },
        e.key === "defis" || e.key === "210. Custom (Challenges)" || e.key === "235. Custom (Super Bouffon / Jigsaw)"
            ? el("div", { class: "box box-defis" }, picto(e.key === "235. Custom (Super Bouffon / Jigsaw)" ? "fa-mask" : "fa-trophy"))
            : el("div", { class: "box", style: { backgroundImage: `url("${pochetteBoite(e.key)}")` } }),
        el("span", { class: "exname" }, e.key === "defis" ? t("Défis") : libelleExtension(e, auteurs.get(e.key))),
    )));
    ajusterPochettes();
    loadScnGrid();
}

/** Les boîtes dont on a une pochette recadrée au format commun (outils/pochettes-boites.py, 18/10/2026) :
 *  l'illustration de face, sans liseré de pack ni perspective. Les autres gardent leur image d'origine. */
const POCHETTES_RECADREES = new Set([1, 2, 4, 7, 11, 16, 21, 24, 27, 32, 39, 40, 45, 50, 55, 56, 57, 60, 119, 120, 136, 143, 178, 190, 192, 195]);
function pochetteBoite(cle) {
    const numero = parseInt(String(cle).split(".")[0], 10);
    return POCHETTES_RECADREES.has(numero) && /^\d+\. /.test(cle)
        ? `/public/img/prepare/boites/${numero}.webp`
        : extensionImageUrl(cle);
}

/** Les pochettes remplissent le panneau des boîtes (17/10/2026) : on prend le plus grand nombre
 *  de colonnes qui fait TENIR toutes les boîtes sans défiler, et chaque pochette grandit
 *  d'autant. Refait quand le panneau change de taille. */
let _observePochettes = null;
function ajusterPochettes() {
    const tabs = document.getElementById("ext-tabs");
    if (!tabs) return;
    const n = tabs.querySelectorAll(".ext-tab").length;
    if (!n || window.innerWidth < 900) { tabs.style.removeProperty("grid-template-columns"); return; }
    const cs = getComputedStyle(tabs);
    const L = tabs.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    const H = tabs.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
    if (L <= 0 || H <= 0) return;
    const ECART_X = 6, ECART_Y = 4, RATIO = 0.56;
    let meilleur = 3;
    for (let c = 3; c <= 10; c++) {
        const w = (L - ECART_X * (c - 1)) / c;
        const lignes = Math.ceil(n / c);
        const h = w / RATIO;
        if (lignes * h + ECART_Y * (lignes - 1) <= H) { meilleur = c; break; }
        meilleur = c;
    }
    tabs.style.setProperty("grid-template-columns", `repeat(${meilleur}, minmax(0, 1fr))`, "important");
    if (!_observePochettes && "ResizeObserver" in window) {
        _observePochettes = new ResizeObserver(() => ajusterPochettes());
        _observePochettes.observe(tabs);
    }
}

async function loadScnGrid() {
    let grid = document.getElementById("scn-grid");
    if (!grid) return;
    grid.replaceChildren(el("div", { class: "loading" }, t("Chargement des scénarios...")));
    const bruts = await catalog.scenariosForExtension(state.extensionTab);
    // Fear No Evil : une tuile par manigance a vilain interchangeable, le
    // vilain se choisit dans une modale au clic (decision utilisateur du
    // 18/09/2026). La tuile montre le dernier vilain choisi sur cet appareil.
    const ext = (await catalog.extensions()).find((e) => e.key === state.extensionTab);
    // Les tuiles gardent TOUJOURS leur vilain d'origine (un par tuile) : on n'y applique plus le dernier vilain choisi sur l'appareil
    // (22/10/2026, signalement de Yarro : « les images des scenarios ne sont pas les bonnes »). Le choix reste dans la fenetre des vilains.
    const scs = regrouperUnderlings(bruts, ext || {}, undefined);
    grid = document.getElementById("scn-grid");
    if (!grid) return;
    const compte = document.getElementById("tb-compte");
    if (compte) compte.textContent = scs.length + " " + t("scénarios");
    grid.replaceChildren(...scs.map((sc) => {
        const concret = sc.interchangeable ? sc.courant.scenario : sc;
        const on = state.scenario && tuileContient(sc, state.scenario.id);
        const verrou = state.legacy ? state.legacy.verrou.scenario(concret) : null;
        const ferme = !!verrou && !verrou.ouvert;
        const plusieurs = sc.interchangeable && sc.underlings.length > 1;
        return el("button", {
            class: "tb-port" + (on ? " chosen" : "") + (ferme ? " est-verrou" : ""),
            "data-scn": sc.id,
            "data-scns": (sc.scenarioIds || [sc.id]).join(","),
            "aria-disabled": ferme ? "true" : null,
            title: ferme ? verrou.condition
                : (plusieurs ? sc.name + " · " + sc.underlings.length + " " + t("vilains au choix")
                             : nomAvecAuteur(sc.name, sc.auteur || concret.auteur, sc.homebrew || concret.homebrew)),
            onclick: (e) => {
                if (ferme) return;
                if (estTel()) {
                    // Toucher = CHOISIR le méchant (24/10/2026, comme les héros) : on en touche un autre pour changer,
                    // puis « Continuer » en bas. Plus besoin de remonter au « Choisir » du bandeau.
                    mechantApercuTel = { sc, concret };
                    document.querySelectorAll(".tb-port.apercu").forEach((b) => b.classList.remove("apercu"));
                    e.currentTarget.classList.add("apercu");
                    rendreSceneMechantTel(concret);
                    return choisirMechantTel({ sc, concret });
                }
                if (plusieurs) ouvrirModaleUnderling(sc); else verrouillerCible(concret);
            },
            onmouseenter: estTel() ? undefined : () => rendreSceneMechant(concret),
            onmouseleave: estTel() ? undefined : () => rendreSceneMechant(state.scenario),
        },
            // MC×DC (22/10/2026) : la tuile d'une affaire montre la MANIGANCE ANNEXE (`tuile_manigance`), pas le sous-fifre.
            portraitAffaire(ext, sc) || portraitScenario(
                // One Last Kill : la tuile montre le SOUS-FIFRE (Jigsaw / Hobgoblin), pas le Punisher commun aux deux (22/10/2026).
                ext && ext.tuileSbireScenarios && ext.tuileSbireScenarios[sc.id]
                    ? { ...concret, tileImage: ext.tuileSbireScenarios[sc.id], villainCards: [ext.tuileSbireScenarios[sc.id]] }
                    : concret),
            el("span", { class: "tb-port-nom" }, nomAvecAuteur(sc.name, sc.auteur || concret.auteur, sc.homebrew || concret.homebrew)),
            plusieurs ? el("span", { class: "st-exp" }, sc.underlings.length + " " + t("vilains au choix")) : null,
            ferme ? el("span", { class: "tb-verrou" }, verrou.etiquette) : null,
            (sc.challenges && sc.challenges.length) ? el("span", { class: "st-exp" }, t("DÉFI")) : null,
        );
    }));
    ajusterTuilesMechants();
}

/** Sur ordinateur, les vignettes des méchants grandissent pour remplir la
 *  grille selon leur nombre (3 pour le Set de base), jusqu'à deux fois leur
 *  taille d'origine. Au-delà de ce qui tient, elles gardent leur taille et la
 *  grille défile comme avant. */
const observateurTuiles = typeof ResizeObserver === "function"
    ? new ResizeObserver(() => ajusterTuilesMechants())
    : null;
function ajusterTuilesMechants() {
    const grille = document.getElementById("scn-grid");
    if (!grille || estTel()) return;
    if (observateurTuiles) { observateurTuiles.disconnect(); observateurTuiles.observe(grille); }
    const n = grille.querySelectorAll(".tb-port").length;
    const vider = () => {
        grille.style.removeProperty("--affiche-cible");
        grille.style.removeProperty("--affiche-cible-h");
        grille.style.removeProperty("grid-template-columns");
        grille.style.removeProperty("justify-content");
    };
    if (!n) return vider();
    const cs = getComputedStyle(grille);
    // Écran du méchant en trois colonnes (PC, 17/10/2026) : les cartes de scénario gardent leur
    // rapport 3:2 et prennent la plus grande taille qui fait tenir TOUS les scénarios dans la
    // zone, sans plafond de 2x ; le nombre de colonnes s'adapte au nombre de scénarios.
    if (window.innerWidth >= 900 && grille.closest(".team-b.eux")) {
        const L = grille.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        const H = grille.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
        const gC = parseFloat(cs.columnGap) || 16, gR = parseFloat(cs.rowGap) || 16;
        if (L > 0 && H > 0) {
            let meilleurC = 1, meilleurW = 0;
            for (let c = 1; c <= Math.min(n, 6); c++) {
                const r = Math.ceil(n / c);
                const w = Math.min((L - (c - 1) * gC) / c, ((H - (r - 1) * gR) / r) * 1.5, 640);
                if (w > meilleurW) { meilleurW = w; meilleurC = c; }
            }
            const h = Math.floor(meilleurW / 1.5);
            const cle = meilleurC + "x" + h;
            if (grille.dataset.ajuste !== cle) {
                grille.dataset.ajuste = cle;
                grille.style.setProperty("grid-template-columns", `repeat(${meilleurC}, ${Math.floor(meilleurW)}px)`, "important");
                grille.style.setProperty("grid-auto-rows", h + "px", "important");
                grille.style.setProperty("justify-content", "start");
            }
            return;
        }
    }
    const racine = getComputedStyle(document.documentElement);
    const base = parseFloat(racine.getPropertyValue("--affiche-cible")) || 148;
    const baseH = parseFloat(racine.getPropertyValue("--affiche-cible-h")) || 124;
    const largeur = grille.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    const hauteur = grille.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
    const gapC = parseFloat(cs.columnGap) || 8;
    const gapR = parseFloat(cs.rowGap) || 8;
    let w = 0;
    for (let c = 1; c <= n; c++) {
        const r = Math.ceil(n / c);
        const parLargeur = (largeur - (c - 1) * gapC) / c;
        const parHauteur = ((hauteur - (r - 1) * gapR) / r) * base / baseH;
        w = Math.max(w, Math.min(parLargeur, parHauteur, base * 2));
    }
    w = Math.floor(w);
    if (w <= base) return vider();
    const h = Math.floor(w * baseH / base);
    if (grille.style.getPropertyValue("--affiche-cible") === w + "px") return;
    grille.style.setProperty("--affiche-cible", w + "px");
    grille.style.setProperty("--affiche-cible-h", h + "px");
    grille.style.setProperty("grid-template-columns", `repeat(auto-fill, ${w}px)`);
    grille.style.setProperty("justify-content", "start");
}


function detailRow(k, v) {
    return el("div", { class: "detail-row" },
        el("span", { class: "dr-k" }, k),
        el("span", { class: "dr-v" }, v),
    );
}

/** Le nom d'un set modulaire, suivi de son createur s'il est fan-made. Les
 *  pastilles « recommandes » et « aleatoire » n'ont que le nom de fichier :
 *  le createur se retrouve par l'index du catalogue. */
function nomDuSetModulaire(nomFichier) {
    const auteur = catalog.auteurSetRencontre(nomFichier);
    return nomAvecAuteur(nomSetRencontre(nomFichier), auteur, true);
}

/** PC : le choix des sets modulaires dans un panneau qui prend la place de l'image du mechant (colonne de droite). */
async function ouvrirPanneauModulaires() {
    const ecran = document.querySelector(".team-b.eux");
    if (!ecran) return;
    ecran.querySelectorAll(".pm-droite").forEach((x) => x.remove());
    const d = state.difficulty;
    const sel = new Set(d.selectedModularSets);
    const liste = el("div", { class: "mod-chips pm-liste" }, el("div", { class: "loading" }, t("Chargement des sets modulaires...")));
    const fermer = () => { panneau.remove(); renderModular(); };
    const panneau = el("aside", { class: "pm-droite", role: "dialog", "aria-label": t("Sets modulaires") },
        el("div", { class: "pm-tete" },
            el("b", { class: "mvl" }, t("Sets modulaires")),
            el("button", { class: "pm-fermer", "aria-label": t("Fermer"), onclick: fermer }, "×")),
        liste,
        el("div", { class: "pm-pied" }, el("button", { class: "btn primary", onclick: fermer }, t("Valider"))));
    ecran.append(panneau);
    const tous = (await catalog.encounterSets()).filter((x) => x.kind === "modular");
    liste.replaceChildren(...tous.map((x) => el("span", {
        class: "mod-chip" + (sel.has(x.name) ? " on" : ""),
        onclick: (e) => {
            sel.has(x.name) ? sel.delete(x.name) : sel.add(x.name);
            d.selectedModularSets = [...sel];
            e.currentTarget.classList.toggle("on");
        },
    }, nomAvecAuteur(x.displayName, x.auteur, true))));
}

async function renderModular() {
    await Promise.resolve();
    const box = document.getElementById("modular-box");
    if (!box) return;
    const d = state.difficulty;
    if (d.modularConfig === "recommended") {
        box.replaceChildren(el("div", { class: "mod-chips" },
            ...state.scenario.recommendedModularSets.map((s) => el("span", { class: "mod-chip on" }, nomDuSetModulaire(s))),
            state.scenario.recommendedModularSets.length === 0 ? el("span", { class: "muted" }, t("Aucun set modulaire recommandé.")) : null,
        ));
    } else if (d.modularConfig === "random") {
        box.replaceChildren(el("div", { class: "mod-chips" }, ...d.selectedModularSets.map((s) => el("span", { class: "mod-chip on" }, nomDuSetModulaire(s)))));
    } else if (!estTel() && document.querySelector(".team-b.eux")) {
        // PC : un resume des sets choisis et un bouton, pas la liste entiere (elle
        // ne tient pas dans la colonne du milieu) ; la liste est dans le panneau de droite.
        box.replaceChildren(el("div", { class: "mod-chips" },
            ...d.selectedModularSets.map((n) => el("span", { class: "mod-chip on" }, nomDuSetModulaire(n))),
            el("button", { class: "tampon", onclick: () => ouvrirPanneauModulaires() },
                d.selectedModularSets.length ? t("Modifier les sets") : t("Choisir les sets modulaires"))));
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
            }, nomAvecAuteur(s.displayName, s.auteur, true)))));
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
        // Anglais comme les deux selecteurs : un meme heros ne doit pas changer
        // d'aspect entre l'etape du choix et l'etape finale.
        style: { backgroundImage: `url("${cardImageUrlEn(idImage)}")` },
        onmouseenter: auSurvol((e) => showCardHover(idImage, e.currentTarget)),
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
        reglages.push(d.base === "expert" ? "Expert" : libelleNiveau(d.standard));
        if (d.skirmish) reglages.push("Skirmish");
        if (d.heroic > 0) reglages.push(t("Héroïque") + " " + d.heroic);
        if (d.intenseCombatants === true && proposerIntense(sc.mandatoryEncounterSets)) reglages.push("Intense Combatants");
        const sets = [...sc.mandatoryEncounterSets, ...d.selectedModularSets].map(nomSetRencontre);
        if (sets.length) reglages.push(sets.join(" · "));
    }

    // La couleur PRINCIPALE du méchant teinte son côté (17/10/2026). Palettes déjà servies par
    // /get_palettes_heros ; sans palette, le fond reste celui d'avant.
    const ecranVS = el("section", { class: "step face-a-face" });
    const idVilain = cartesVilain[0];
    if (idVilain) {
        fetch("/get_palettes_heros", { cache: "no-store" }).then((r) => r.json()).then((d) => {
            const pal = (d && d.palettes) || {};
            const c = pal[idVilain] || pal[idVilain + "a"] || pal[String(idVilain).replace(/[a-z]$/, "")];
            if (c && c[0]) ecranVS.style.setProperty("--fo-mechant", "rgb(" + c[0].join(",") + ")");
        }).catch(() => { /* pas de palette : fond habituel */ });
    }
    ecranVS.append(...[
        el("div", { class: "faceoff" + (state.playerCount > 2 ? " large" : "") },
            el("div", { class: "fo-side heroes-side" },
                heros,
                el("div", { class: "fo-reglages" },
                    ...reglages.map((x) => el("span", { class: "tampon" }, x))),
            ),
            document.documentElement.classList.contains("tel")
                ? el("div", { class: "fo-vs fo-vs-texte", "aria-label": "VS" }, "VS")   // téléphone : un VS blanc en Bangers, plus d'éclair (23/10/2026)
                : el("img", { class: "fo-vs", src: "/public/img/prepare/vs.png", alt: "VS", draggable: "false" }),
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
    ].filter(Boolean));
    return ecranVS;
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

    // Façon de jouer : combinable avec Solo, Coop locale et Campagne, donc un
    // CHOIX et non une tuile de mode. En manuel, le moteur pose la table puis se
    // tait ; la fenêtre « On en est où ? » rend la main plus tard.
    const choixFacon = (valeur, libelle) => el("label", { class: "cj-chk" },
        el("input", {
            type: "radio",
            name: "facon-de-jouer",
            checked: (state.modeManuel === true) === (valeur === FACON_MANUEL) || undefined,
            onchange: () => { state.modeManuel = valeur === FACON_MANUEL; },
        }),
        el("span", {}, libelle));
    const manuel = el("div", {},
        choixFacon(FACON_AUTO, t("Automatique : le moteur applique les règles")),
        choixFacon(FACON_MANUEL, t("Manuel façon OCTGN : le moteur pose la table, puis ne joue plus")));

    return el("details", { class: "camp-journal avance" },
        el("summary", {}, t("Avancé")),
        el("div", { class: "cj-body" },
            ligne(t("Seed"), seedRow, t("Même seed + mêmes choix = même partie")),
            ligne(t("Temps par décision (secondes)"), timeoutInput, t("0 = illimité")),
            lignePremierJoueur,
            ligne(t("Règles v16"), v16, null),
            ligne(t("Façon de jouer"), manuel,
                  t("En manuel, tu appliques toutes les règles toi-même")),
        ),
    );
}

enregistrerTraductions(DICO_TEL_EN);
// Mode téléphone : le passage sous/sur 768 px redessine l'écran ; le bouton
// Retour du système rejoue l'écran précédent (voir tel.js).
suivreTel(() => { pileTelReinit(); render(); });
installerHistorique(appliquerCleTel);

(async () => {
    // Revenir a la preparation desarme toujours le coach du mode Decouverte :
    // c'est le seul point de passage commun aux quatre facons de rejoindre le
    // plateau (lancement normal, puzzle, reprise, salon multi), dont trois
    // n'arment jamais rien. Un lancement en mode Decouverte le rearmera juste
    // avant de rediriger (launcher.js). Le coach survit donc a un F5 sur le
    // plateau, mais jamais a un retour ici.
    appliquerTutoriel(window.localStorage, null);
    synchroniserLangueServeur();
    appliquerAffichage();
    // Gardee : la fenetre « Choisis ton affichage », plus bas, attend la
    // reponse du compte pour savoir s'il a deja choisi.
    const syncAffichage = synchroniserAffichage();
    // Les arts alternatifs suivent le compte d'un appareil à l'autre.
    prefs.synchroniserArts().then((change) => { if (change) render(); });
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
    // ⚠ APRES `render()`, ET NON AVANT. La modale se pose sur `document.body` ;
    // posee avant, le premier rendu la balayait. Et on ne la montre pas en
    // creation d'equipe de campagne : on y arrive depuis un autre ecran, la
    // question y tomberait de nulle part.
    if (!langueDejaChoisie() && !creationCampagne()) {
        await demanderLaLangue();
    }
    // Apres la langue : la fenetre parle alors la langue choisie.
    const reponsePreferences = await syncAffichage;
    // La teinte suit le compte comme l'affichage, sur la MEME reponse.
    synchroniserTeinte(reponsePreferences);
    appliquerTeintePage(teinteActuelle());
    // Plus de fenetre « Choisis ton affichage » a la premiere visite (18/10/2026) : tout le monde commence en
    // Normal et peut en changer dans Options (`demanderLAffichage({ rouvert: true })`) ou par le bouton de l'en-tete.
    // Apres l'affichage : une seule fenetre a la fois, et la langue est deja
    // choisie. Chaque joueur la voit une fois, nouveau comme ancien.
    // Le passage unique aux trois choix se fait aussi pour qui n'a plus la fenêtre à voir (19/10/2026).
    try { migrerPhaseTroisChoix(localStorage); } catch (e) { /* stockage indisponible */ }
    let phaseVue = null;
    try { phaseVue = localStorage.getItem(CLE_PHASE_CHOIX_VU); } catch (e) { /* stockage indisponible */ }
    // Sur telephone la phase du mechant est d'office « Guidee » : pas de fenetre (26/10/2026).
    if (!creationCampagne() && doitProposerLaPhaseSurAppareil(phaseVue, estTel())) {
        await demanderLaPhaseDuMechant();
    }
    // L'EQUIPE RESTE ENSEMBLE (13/10/2026) : l'hote qui rouvre la preparation
    // le signale a sa table, et les invites restes sur l'ecran de fin
    // reviennent tout seuls a leur salon. Le moteur ignore l'appel d'une table
    // locale et le refuse a qui ne tient pas le siege 0 : rien a verifier ici.
    if (!creationCampagne()) {
        fetch("/annoncer_preparation", { method: "POST" }).catch(() => { /* table muette : rien a annoncer */ });
    }
    // Le salon ne concerne que le multi, mais on sonde toujours : la reponse
    // dit elle-meme si on y est (multi:false en solo, et tout reste inerte).
    await sonderSalon();
    boucleSalon();
})();

/** La boucle de sondage, reglee par `cadenceSondage`.
 *
 *  ⚠ `setTimeout` ENCHAINE, jamais `setInterval` : la cadence change en cours
 *  de route (on entre dans un salon, on masque l'onglet), et un intervalle fixe
 *  ne se renegocie pas. */
function boucleSalon() {
    let minuteur = null;
    const enAttente = () => !!(state.salon && state.salon.multi && !state.salon.prete);
    const programmer = () => {
        clearTimeout(minuteur);
        const delai = cadenceSondage({
            cache: document.hidden,
            enAttente: enAttente(),
            injoignable: tableDeclareeFermee(),
        });
        if (!delai) return;                       // onglet cache : on se tait
        minuteur = setTimeout(async () => {
            await sonderSalon();
            programmer();
        }, delai);
    };
    // Revenir sur l'onglet doit rattraper tout de suite : quelqu'un a pu
    // rejoindre pendant qu'on regardait ailleurs.
    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) void sonderSalon().then(programmer);
        else clearTimeout(minuteur);
    });
    programmer();
}
