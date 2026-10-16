// Éditeur de deck : construction de decks SANS passer par marvelcdb.
//
// Refonte du 09/10/2026 (maquette validée, décisions dans
// .planning/todos/2026-10-09-editeur-de-deck-refonte.md) : filtres à gauche,
// grille au centre, deck à droite avec aperçu, résumé et onglets Liste /
// Statistiques / Pioche.
//
// Réutilise les modules de la préparation (api/cards/catalog) : mêmes données,
// mêmes images, même format de deck que deck/starter/*.json.
//
// Sauvegarde :
//   - brouillon AUTOMATIQUE, même invalide -> localStorage (mc-deckbuilder-drafts) ;
//   - deck fini -> POST /save_deck (deck/custom/), proposé ensuite dans
//     l'assistant. Un deck invalide ne s'enregistre pas, donc ne se joue pas.
//
// La légalité est celle de regles.js (validerDeck), la même que la préparation.
"use strict";
import { cardImageUrl } from "/public/js/prepare/api.js";
import { cards } from "/public/js/prepare/cards.js";
import { nomAvecAuteur, auteurUnique } from "/public/js/prepare/auteur.js";
import { catalog, vagueDeLExtension, titreDeVague } from "/public/js/prepare/catalog.js";
// LEGACY (13/09/2026) : en mode Legacy, on construit avec ce qu'on a. Les
// cartes des boîtes pas encore ouvertes restent visibles, grisées, et ne
// s'ajoutent pas. Voir legacy-cartes.js.
import { etat as etatLegacy } from "/public/js/prepare/legacy-fiche.js";
import { fabriquerDisponibilite } from "/public/js/prepare/legacy-cartes.js";
import { t, synchroniserLangueServeur, langueActuelle, boutonLangue, enregistrerTraductions } from "/public/js/prepare/langue.js";
import { boutonAffichage } from "/public/js/prepare/affichage.js";
import { urlNarval } from "/public/js/prepare/narval.js";
import { nomFr, texteFr } from "/public/js/prepare/cartes-fr.js";
import { NOMS_FR } from "/public/js/prepare/noms-fr.js";
import { correspondRecherche } from "/public/js/deckbuilder/recherche.js";
import { versionsDe, versionDansLeDeck, changerVersion } from "/public/js/deckbuilder/arts-reeditions.js";
import { poserTraduction } from "/public/js/traduction/poser.js";
import { estTel, suivreTel, enteteTel, feuilleDansHistorique } from "/public/js/tel-pages.js";
import {
    filtresVides, passeFiltres, aspectsParDefaut, comparateur, grouperDeck, courbeDesCouts,
    nombreFiltresActifs, COUTS, PALIERS_STAT, STATS, cleStat,
} from "/public/js/deckbuilder/filtres.js";
import { construirePaquet, melanger, probasParTour } from "/public/js/deckbuilder/pioche.js";
import { cartesFautives } from "/public/js/deckbuilder/fautives.js";
import { DICO_EN_DECKBUILDER } from "/public/js/deckbuilder/dico-en.js";
// Les règles de construction vivent dans regles.js : l'écran de préparation les
// applique AUSSI, quand on colle un lien MarvelCDB sur un autre héros.
import {
    ASPECTS, CLASSES_NEUTRES, estStanLee, estSignature,
    estCarteJoueur, estCarteSignature, maxParDeck, validerDeck, choisiesDuDeck, reglesAspect,
} from "/public/js/deckbuilder/regles.js";

enregistrerTraductions(DICO_EN_DECKBUILDER);

/** Les quatre ressources : lettre du moteur (`desc.RES`), glyphe de la police
 *  ChampionsIcons (P poing, M cerveau, E éclair, W étoile), nom, couleur. */
const RESSOURCES = [
    { lettre: "R", glyphe: "P", nom: "physique", couleur: "#e74c3c" },
    { lettre: "B", glyphe: "M", nom: "mentale", couleur: "#3498db" },
    { lettre: "Y", glyphe: "E", nom: "énergie", couleur: "#f1c40f" },
    { lettre: "G", glyphe: "W", nom: "libre", couleur: "#2ecc71" },
];
const RESSOURCE_PAR_LETTRE = Object.fromEntries(RESSOURCES.map((r) => [r.lettre, r]));

/** Mots-clés des cartes joueur (vocabulaire officiel FR, forme anglaise pour
 *  les cartes non traduites). Seuls ceux présents dans le pool sont proposés. */
const MOTS_CLES = [
    ["Riposte", /\briposte\b|\bretaliate\b/i],
    ["Perçant", /\bperçant\b|\bpiercing\b/i],
    ["À distance", /\bà distance\b|\branged\b/i],
    ["Déferlement", /\bdéferlement\b|\boverkill\b/i],
    ["Restreint", /\brestreint\b|\brestricted\b/i],
    ["Utilisations", /\butilisations?\b|\buses\b/i],
    ["Ténacité", /\bténacité\b|\btoughness\b/i],
    ["Permanent", /\bpermanent\b/i],
    ["Mise en place", /\bmise en place\b|\bsetup\b/i],
    ["Temporaire", /\btemporaire\b|\btemporary\b/i],
    ["Aérien", /\baérien\b|\baerial\b/i],
    ["Robuste", /\brobuste\b|\bstalwart\b/i],
    ["Solide", /\bsolide\b|\bsteady\b/i],
    ["Alliance", /\balliance\b/i],
    ["En Équipe", /\ben équipe\b|\bteam-up\b/i],
    ["Percée", /\bpercée\b|\bbreakthrough\b/i],
    ["Garde", /\bgarde\b|\bguard\b/i],
];

const TYPES = [
    { cle: "Ally", libelle: "Allié", groupe: "Alliés", icone: "fa-user" },
    { cle: "Event", libelle: "Événement", groupe: "Événements", icone: "fa-bolt" },
    { cle: "Upgrade", libelle: "Amélioration", groupe: "Améliorations", icone: "fa-arrow-up" },
    { cle: "Support", libelle: "Soutien", groupe: "Soutiens", icone: "fa-building" },
    { cle: "Resource", libelle: "Ressource", groupe: "Ressources", icone: "fa-diamond" },
];
const TYPE_PAR_CLE = Object.fromEntries(TYPES.map((x) => [x.cle, x]));
const NOMS_ASPECTS_FR = { Aggression: "Agressivité", Basic: "Basique", Campaign: "Campagne", Hero: "Signature" };

const CLE_BROUILLONS = "mc-deckbuilder-drafts";
const CLE_REPLIES = "mc-deckbuilder-filtres-replies";
const BROUILLONS_PAR_HEROS = 10;
const LIMITE_GRILLE = 400;

function ressourcesDe(carte) {
    return String((carte.desc && carte.desc.RES) || "").toUpperCase().split("").filter((l) => l in RESSOURCE_PAR_LETTRE);
}
function iconeRessource(lettre) {
    const r = RESSOURCE_PAR_LETTRE[lettre];
    if (!r) return null;
    return el("i", { class: "icone-res", style: `--res:${r.couleur}`, title: t(r.nom), "aria-label": t(r.nom) }, r.glyphe);
}
function motsClesDe(carte) {
    const texte = `${texteFr(carte) || ""} ${carte.text || ""}`;
    return MOTS_CLES.filter(([, re]) => re.test(texte)).map(([nom]) => nom);
}
function libelleType(type) { return TYPE_PAR_CLE[type] ? t(TYPE_PAR_CLE[type].libelle) : type; }
// Double aspect (« Aggression;Justice », pack tmnt_aspect_dual) : la ligne prend la
// couleur du PREMIER aspect imprime, le libelle nomme les deux (« Agressivité / Justice »).
function classeCss(aspect) { return String(aspect).split(";")[0].replace(/[^a-z]/gi, "").toLowerCase(); }
function labelAspect(aspect) {
    if (String(aspect).includes(";")) return String(aspect).split(";").map((a) => labelAspect(a.trim())).join(" / ");
    const brut = String(aspect).replace(/^'/, "");
    return NOMS_ASPECTS_FR[aspect] ? t(NOMS_ASPECTS_FR[aspect]) : brut;
}
const sansEtoile = (nom) => String(nom || "").replace(/^\*\s*/, "");
/** Nom affiché : français officiel quand on joue en français (cartes-fr.js,
 *  sinon noms-fr.js, y compris pour une réédition), anglais sinon. */
function nomCarte(c) {
    if (!c) return "";
    let nom = nomFr(c);
    if (langueActuelle() === "fr" && nom === c.name) nom = NOMS_FR[c.card_id] || NOMS_FR[c.full_link_id] || nom;
    return sansEtoile(nom);
}

/** Créateur d'un aspect FAN-MADE (Determination, Venomized) : la seule valeur
 *  `custom` de toutes ses cartes. Vide pour les aspects officiels. */
let _auteurParAspect = null;
function auteurDeLAspect(aspect) {
    if (!_auteurParAspect) {
        const toutes = cards.all();
        if (!toutes.length) return "";
        const parClasse = new Map();
        for (const c of toutes) {
            const cl = c && c.class;
            if (!cl) continue;
            if (!parClasse.has(cl)) parClasse.set(cl, []);
            parClasse.get(cl).push(c.custom);
        }
        _auteurParAspect = new Map();
        for (const [cl, customs] of parClasse) {
            const a = auteurUnique(customs);
            if (a) _auteurParAspect.set(cl, a);
        }
    }
    return _auteurParAspect.get(aspect) || "";
}

const etat = {
    heroes: [],
    hero: null,
    nomDeck: "",
    // cardId -> nombre de copies choisies (player_deck uniquement).
    choisies: new Map(),
    filtres: filtresVides(),
    brouillonId: null,
    // Legacy : null hors du mode ; sinon la disponibilité (voir demarrer).
    legacy: null,
    // Carte d'origine -> version (illustration) retenue dans la grille.
    arts: new Map(),
    triGrille: "aspect",
    triDeck: "type",
    onglet: "liste",
    kitOuvert: false,
    problemesOuverts: false,
    sectionsOuvertes: new Set(["aspects", "types", "couts"]),
    apercu: null,
    epingle: null,
    pioche: { mode: "alter", main: [], reste: [], signature: "" },
    sources: [],
    partir: "",
};

function dispoCarte(id) {
    return etat.legacy ? etat.legacy.carte(id) : { ouvert: true, etiquette: "" };
}

/* ---------------- Données ---------------- */

/* Stan Lee — « Marvelous » : son deck doit contenir 15 cartes signature
   empruntées à d'autres héros. Il est donc le seul héros pour qui les cartes de
   classe « Hero » sont sélectionnables ici. */
const _pools = new Map();
async function poolJoueur(avecSignature = false) {
    if (_pools.has(avecSignature)) return _pools.get(avecSignature);
    const cs = await cards.load();
    // Signatures des héros RETIRÉS du jeu (`metadata.indisponible`) : plus
    // empruntables, même par Stan Lee.
    const masques = await catalog.setsMasques();
    const vus = new Map(); // titre+class+type -> première carte (dédoublonne les réimpressions)
    for (const id of Object.keys(cs.const_card_dict)) {
        const c = cs.const_card_dict[id];
        if (c && c.set_name && masques.has(c.set_name)) continue;
        const garde = estCarteJoueur(c) || (avecSignature && estCarteSignature(c));
        if (!garde) continue;
        const cle = `${c.name}|${c.class}|${c.type}`;
        if (!vus.has(cle)) vus.set(cle, { id: String(c.id ?? id).split(",")[0] || id, carte: c });
    }
    const pool = [...vus.values()];
    _pools.set(avecSignature, pool);
    return pool;
}
function poolCourant() { return _pools.get(estStanLee(etat.hero)) || []; }

/** Héros dont proviennent les cartes signature choisies, par nombre de copies. */
function herosEmpruntes() {
    const parHero = new Map();
    for (const [id, n] of etat.choisies) {
        if (!estSignature(cards.get(id))) continue;
        for (const h of etat.heroes) {
            if ((h.deck.hero_deck || []).includes(id)) {
                parHero.set(h, (parHero.get(h) || 0) + n);
                break;
            }
        }
    }
    return [...parHero.entries()].sort((a, b) => b[1] - a[1]).map(([h]) => h);
}

/** Les cartes du héros (kit), sans Stan Lee qui les choisit lui-même. */
function kitDuHeros() {
    if (!etat.hero || estStanLee(etat.hero)) return [];
    return (etat.hero.deck.hero_deck || []).map((id) => String(id).split(",")[0]);
}

/** Faces héros et alter ego, pour la taille de main. */
function faces() {
    const ids = String((etat.hero && etat.hero.deck.hero && etat.hero.deck.hero[0]) || "").split(",");
    const c = ids.map((id) => cards.get(id)).filter(Boolean);
    return {
        heros: c.find((x) => x.type === "Hero") || c[0] || null,
        alter: c.find((x) => x.type === "AlterEgo") || c[1] || null,
    };
}
function tailleDeMain(face) {
    const n = Number(face && face.desc && (face.desc.HS ?? face.desc.HND ?? face.desc.Hand));
    return Number.isFinite(n) && n > 0 ? n : 5;
}

/* ---------------- Validation ---------------- */

function valider() {
    if (!etat.hero) return { ok: false, problemes: [t("Choisis un héros")], total: 0, signature: 0, aspects: [] };
    const r = validerDeck({ hero: etat.hero, choisies: etat.choisies, carte: (id) => cards.get(id), t });
    if (!etat.nomDeck.trim()) { r.problemes.push(t("Donne un nom au deck")); r.ok = false; }
    return r;
}

/* ---------------- Deck JSON ---------------- */

function deckJson() {
    const base = etat.hero.deck;
    const marvelous = estStanLee(etat.hero);
    const player_deck = [];
    const empruntees = [];
    for (const [id, n] of etat.choisies) {
        const cible = marvelous && estSignature(cards.get(id)) ? empruntees : player_deck;
        for (let i = 0; i < n; i++) cible.push(id);
    }
    // Marvelous : l'obligation et le némésis viennent du héros le plus emprunté.
    const source = marvelous ? herosEmpruntes()[0] : null;
    return {
        version: base.version || "0.5.8",
        name: etat.nomDeck.trim() || etat.hero.name,
        metadata: { url: "" },
        hero: base.hero,
        hero_deck: marvelous ? empruntees : (base.hero_deck || []),
        set_aside: base.set_aside || [],
        obligations: (source ? source.deck.obligations : base.obligations) || [],
        nemesis_set: (source ? source.deck.nemesis_set : base.nemesis_set) || [],
        player_deck,
    };
}

function chargerDepuisDeck(d, nom) {
    etat.choisies.clear();
    for (const [id, n] of choisiesDuDeck(etat.hero, d)) etat.choisies.set(id, n);
    etat.nomDeck = nom ?? (d.name || "");
}

/* ---------------- Brouillons (localStorage) ---------------- */

function lireBrouillons() {
    try { return JSON.parse(window.localStorage.getItem(CLE_BROUILLONS) || "{}"); }
    catch { return {}; }
}
function ecrireBrouillons(b) {
    try { window.localStorage.setItem(CLE_BROUILLONS, JSON.stringify(b)); } catch { /* stockage indisponible */ }
}
/** Brouillon automatique : gardé même invalide, dix au plus par héros. */
function sauverBrouillon() {
    if (!etat.hero || !etat.choisies.size) return;
    const b = lireBrouillons();
    const id = etat.brouillonId || `d${Date.now()}`;
    etat.brouillonId = id;
    b[id] = { heroId: etat.hero.id, deck: deckJson(), updated: Date.now() };
    const siens = Object.entries(b).filter(([, x]) => x.heroId === etat.hero.id).sort((x, y) => y[1].updated - x[1].updated);
    for (const [vieux] of siens.slice(BROUILLONS_PAR_HEROS)) delete b[vieux];
    ecrireBrouillons(b);
}
let _minuteurBrouillon = null;
function programmerBrouillon() {
    clearTimeout(_minuteurBrouillon);
    _minuteurBrouillon = setTimeout(() => { sauverBrouillon(); rendrePartir(); }, 600);
}

/* ---------------- Outils DOM ---------------- */

const $ = (sel) => document.querySelector(sel);
function remplacer(zone, ...enfants) {
    zone.replaceChildren(...enfants.flat(9).filter((e) => e != null && e !== false));
}
function el(tag, attrs = {}, ...enfants) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
        if (k === "class") n.className = v;
        else if (k.startsWith("on")) n[k] = v;
        else if (v !== undefined && v !== null && v !== false) n.setAttribute(k, v === true ? "" : v);
    }
    for (const e of enfants.flat(9)) if (e != null && e !== false) n.append(e.nodeType ? e : document.createTextNode(e));
    return n;
}
function statut(texte, erreur = false) {
    const zone = $("#db-status");
    zone.textContent = texte;
    zone.classList.toggle("est-erreur", erreur);
}

/** Petite fenêtre « Oui / Annuler » dans le style de la page. */
function confirmer(question, oui) {
    return new Promise((resoudre) => {
        const modale = $("#db-modale");
        const fermer = (r) => { modale.hidden = true; remplacer(modale); resoudre(r); };
        remplacer(modale, el("div", { class: "db-modale-boite", role: "dialog", "aria-modal": "true" },
            el("p", {}, question),
            el("div", {},
                el("button", { type: "button", onclick: () => fermer(false) }, t("Annuler")),
                el("button", { type: "button", class: "db-oui", onclick: () => fermer(true) }, oui))));
        modale.onclick = (e) => { if (e.target === modale) fermer(false); };
        modale.hidden = false;
        modale.querySelector(".db-oui").focus();
    });
}

/* ---------------- En-tête (celui de la préparation) ---------------- */

function rendreEnTete() {
    document.title = t("Éditeur de deck") + " — Marvel Champions";
    document.documentElement.lang = langueActuelle();
    const selHero = el("select", { id: "db-hero", class: "db-heros", "aria-label": t("Héros") },
        el("option", { value: "" }, t("— Héros —")),
        etat.heroes.map((h) => el("option", { value: h.id, selected: etat.hero && etat.hero.id === h.id }, h.name)));
    selHero.onchange = async () => {
        const nouveau = etat.heroes.find((h) => h.id === selHero.value) || null;
        if (etat.choisies.size && !(await confirmer(t("Changer de héros vide le deck en cours. Continuer ?"), t("Changer")))) {
            selHero.value = etat.hero ? etat.hero.id : "";
            return;
        }
        etat.hero = nouveau;
        etat.choisies.clear();
        etat.brouillonId = null;
        etat.epingle = null;
        etat.apercu = null;
        etat.nomDeck = etat.hero ? `${etat.hero.name} custom` : "";
        $("#db-nom").value = etat.nomDeck;
        await chargerSources();
        reglerFiltresParDefaut();
        rendreToutEtFiltres();
    };
    const retour = el("a", { class: "brand", href: "/prepare.html", title: t("Préparation"), "aria-label": t("Préparation") },
        el("span", { class: "brand-back" }, "<"),
        el("span", { class: "brand-lockup logo" }, el("img", { class: "brand-narwhal", src: urlNarval(), alt: "" })));
    // Téléphone (zone 2 de la refonte du 09/10/2026) : l'en-tête fin à burger,
    // le héros sur sa propre ligne, pleine largeur. L'en-tête du PC reste dans
    // le DOM, masqué par tel-pages.css, et redevient visible dès 768 px.
    const ancien = document.querySelector("body > .tp-entete");
    if (ancien) ancien.remove();
    if (estTel()) {
        const entete = enteteTel({ titre: t("Éditeur de deck"), ici: "/deck-builder.html" });
        entete.append(el("div", { class: "tp-rang2" }, selHero));
        document.body.prepend(entete);
        remplacer($("#db-entete"));
        return;
    }
    remplacer($("#db-entete"),
        retour,
        boutonLangue("btn ghost btn-langue"),
        boutonAffichage("btn ghost"),
        el("span", { class: "db-titre" }, t("Éditeur de deck")),
        selHero,
        el("span", { class: "db-heros-aspects", id: "db-heros-aspects" }),
        el("span", { class: "db-esp" }),
        el("a", { class: "db-retour-prep", href: "/prepare.html" }, t("← Préparation")));
}

/* ---------------- Filtres ---------------- */

function basculer(set, valeur) { set.has(valeur) ? set.delete(valeur) : set.add(valeur); }
function changerFiltres() { rendreFiltres(); rendreGrille(); rendreMobile(); }

const SECTIONS = [
    { cle: "aspects", titre: "Aspects", rail: "fa-adjust" },
    { cle: "types", titre: "Types", rail: "fa-th-large" },
    { cle: "couts", titre: "Coûts", rail: "fa-circle-o" },
    { cle: "ressources", titre: "Ressources", rail: "fa-bolt" },
    { cle: "mots", titre: "Mots-clés", rail: "fa-tag" },
    { cle: "traits", titre: "Traits", rail: "fa-tags" },
    { cle: "packs", titre: "Pack", rail: "fa-archive" },
    { cle: "stats", titre: "ATK · THW · DEF · PV", rail: "fa-signal" },
];

/** Combien de valeurs sont cochées dans une section (repère du rail). */
function nombreDansSection(cle) {
    const f = etat.filtres;
    if (cle === "aspects") return f.aspects.size;
    if (cle === "types") return f.types.size;
    if (cle === "couts") return f.couts.size;
    if (cle === "ressources") return f.ressources.size;
    if (cle === "mots") return f.motsCles.size;
    if (cle === "traits") return f.traits.size;
    if (cle === "packs") return f.packs.size;
    if (cle === "stats") return STATS.reduce((s, x) => s + f.stats[x.cle].size, 0) + (f.unique ? 1 : 0);
    return 0;
}

function section(cle, titre, ...corps) {
    const ouverte = etat.sectionsOuvertes.has(cle);
    const nb = nombreDansSection(cle);
    return el("div", { class: `db-sec${ouverte ? "" : " est-ferme"}`, "data-section": cle },
        el("h3", {}, el("button", {
            type: "button", "aria-expanded": ouverte ? "true" : "false",
            onclick: () => { basculer(etat.sectionsOuvertes, cle); rendreFiltres(); },
        }, el("span", {}, t(titre), nb ? el("span", { class: "db-sec-nb" }, ` ${nb}`) : null), el("span", {}, ouverte ? "▾" : "▸"))),
        el("div", { class: "db-sec-corps" }, ...corps));
}

function chip(texte, actif, onclick, classe = "", attrs = {}) {
    return el("button", { type: "button", class: `db-chip${classe ? " " + classe : ""}${actif ? " est-actif" : ""}`, "aria-pressed": actif ? "true" : "false", onclick, ...attrs }, texte);
}

/** Aspects proposés : signatures pour Stan Lee, puis les aspects du jeu (les
 *  fan-made seulement si l'interrupteur est mis), puis les classes neutres. */
function aspectsProposes() {
    const f = etat.filtres;
    return [...(estStanLee(etat.hero) ? ["Hero"] : []),
        ...ASPECTS.filter((a) => f.fanMade || !auteurDeLAspect(a)),
        ...CLASSES_NEUTRES];
}

function traitsDuPool() {
    const vus = new Map();
    for (const { carte } of poolCourant()) {
        if (!etat.filtres.fanMade && carte.custom) continue;
        for (const tr of carte.traits || []) {
            const propre = String(tr).replace(/\.$/, "");
            const cle = propre.toUpperCase();
            if (!vus.has(cle)) vus.set(cle, propre);
        }
    }
    return [...vus.values()].sort((a, b) => a.localeCompare(b));
}

function motsClesDuPool() {
    const presents = new Set();
    for (const { carte } of poolCourant()) for (const mot of motsClesDe(carte)) presents.add(mot);
    return MOTS_CLES.map(([nom]) => nom).filter((nom) => presents.has(nom));
}

/** Packs du pool, groupés par vague ; le fan-made en dernier. */
function packsDuPool() {
    const sets = cards.sets() || {};
    const parCode = new Map();
    for (const [cle, s] of Object.entries(sets)) if (s && s.name) parCode.set(s.name, cle);
    const vus = new Map();
    for (const { carte } of poolCourant()) {
        const code = carte.package_name;
        if (!code || vus.has(code)) continue;
        const cle = parCode.get(code);
        const fan = !!carte.custom;
        const vague = !fan && cle ? vagueDeLExtension(cle) : null;
        vus.set(code, {
            code, fan, vague, rang: cle ? parseInt(cle, 10) : 999,
            nom: cle ? cle.replace(/^\d+\.\s*/, "") : code,
        });
    }
    const groupes = new Map();
    for (const p of [...vus.values()].sort((a, b) => a.rang - b.rang || a.nom.localeCompare(b.nom))) {
        if (p.fan && !etat.filtres.fanMade) continue;
        const titre = p.fan ? t("Fan-made")
            : p.vague ? `${t("Vague")} ${p.vague}${titreDeVague(p.vague) ? " · " + titreDeVague(p.vague) : ""}`
            : t("Autres");
        if (!groupes.has(titre)) groupes.set(titre, []);
        groupes.get(titre).push(p);
    }
    return groupes;
}

let _recherchePack = "";
function rendreFiltres() {
    const f = etat.filtres;
    const zone = $("#db-filtres");
    const ancienPack = zone.querySelector(".db-pack-recherche");
    const focusPack = ancienPack && document.activeElement === ancienPack;
    const packs = packsDuPool();
    const recherche = _recherchePack.toLowerCase();
    remplacer(zone,
        section("aspects", "Aspects", el("div", { class: "db-chips" },
            aspectsProposes().map((a) => chip(
                nomAvecAuteur(labelAspect(a), auteurDeLAspect(a), true),
                f.aspects.has(a), () => { basculer(f.aspects, a); changerFiltres(); },
                `aspect-${classeCss(a)}`, { "data-aspect": a })))),
        section("types", "Types", el("div", { class: "db-chips" },
            TYPES.map((ty) => chip([el("i", { class: `fa ${ty.icone}`, "aria-hidden": "true" }), t(ty.libelle)],
                f.types.has(ty.cle), () => { basculer(f.types, ty.cle); changerFiltres(); }, "", { "data-type": ty.cle })))),
        section("couts", "Coûts", el("div", { class: "db-chips" },
            COUTS.map((c) => chip(c, f.couts.has(c), () => { basculer(f.couts, c); changerFiltres(); }, "rond", { "data-cout": c, title: `${t("Coût")} ${c}` })))),
        section("ressources", "Ressources", el("div", { class: "db-chips" },
            RESSOURCES.map((r) => chip([iconeRessource(r.lettre), t(r.nom)], f.ressources.has(r.lettre),
                () => { basculer(f.ressources, r.lettre); changerFiltres(); }, "", { title: `${t("Génère")} ${t(r.nom)}` })))),
        section("mots", "Mots-clés", el("div", { class: "db-chips" },
            motsClesDuPool().map((mot) => chip(t(mot), f.motsCles.has(mot), () => { basculer(f.motsCles, mot); changerFiltres(); })))),
        section("traits", "Traits",
            el("div", { class: "db-traits-tete" },
                el("input", {
                    class: "db-champ db-trait-champ", type: "text", list: "db-traits-liste", placeholder: t("Ajouter un trait…"),
                    onchange: (e) => {
                        const v = e.target.value.trim();
                        if (!v) return;
                        const connu = traitsDuPool().find((x) => x.toLowerCase() === v.toLowerCase());
                        f.traits.add(connu || v);
                        changerFiltres();
                        const champ = $("#db-filtres .db-trait-champ");
                        if (champ) champ.focus();
                    },
                }),
                el("div", { class: "db-etet-ou", role: "group", "aria-label": t("Combinaison des traits") },
                    ["ou", "et"].map((m) => el("button", {
                        type: "button", class: f.traitsMode === m ? "est-actif" : "", "aria-pressed": f.traitsMode === m ? "true" : "false",
                        title: m === "ou" ? t("Au moins un des traits") : t("Tous les traits"),
                        onclick: () => { f.traitsMode = m; changerFiltres(); },
                    }, m === "ou" ? t("OU") : t("ET"))))),
            el("datalist", { id: "db-traits-liste" }, traitsDuPool().map((tr) => el("option", { value: tr }))),
            el("div", { class: "db-chips" }, [...f.traits].map((tr) => el("span", { class: "db-tag" }, tr,
                el("button", { type: "button", "aria-label": `${t("Retirer")} ${tr}`, onclick: () => { f.traits.delete(tr); changerFiltres(); } }, "×"))))),
        section("packs", "Pack",
            el("input", {
                class: "db-champ db-pack-recherche", type: "search", placeholder: t("Chercher un pack…"), value: _recherchePack,
                oninput: (e) => { _recherchePack = e.target.value; rendreFiltres(); },
            }),
            el("div", { class: "db-packs" }, [...packs.entries()].map(([titre, liste]) => {
                const visibles = liste.filter((p) => !recherche || p.nom.toLowerCase().includes(recherche) || titre.toLowerCase().includes(recherche));
                if (!visibles.length) return null;
                return [el("h4", {}, titre), visibles.map((p) => el("label", { class: "db-pack" },
                    el("input", { type: "checkbox", checked: f.packs.has(p.code), onchange: () => { basculer(f.packs, p.code); changerFiltres(); } }),
                    p.nom))];
            }))),
        section("stats", "ATK · THW · DEF · PV",
            STATS.filter((s) => poolCourant().some(({ carte }) => cleStat((carte.desc || {})[s.desc]) !== "")).map((s) =>
                el("div", { class: "db-stat-rangee" }, el("b", {}, t(s.libelle)),
                    el("div", { class: "db-chips" }, PALIERS_STAT.map((p) => chip(p, f.stats[s.cle].has(p),
                        () => { basculer(f.stats[s.cle], p); changerFiltres(); }, "rond"))))),
            el("div", { class: "db-chips" }, chip(t("Unique seulement"), f.unique, () => { f.unique = !f.unique; changerFiltres(); }))),
        el("div", { class: "db-sec" }, el("label", { class: "db-inter" },
            el("input", { type: "checkbox", id: "db-fanmade", checked: f.fanMade, onchange: (e) => {
                f.fanMade = e.target.checked;
                if (!f.fanMade) for (const a of [...f.aspects]) if (auteurDeLAspect(a)) f.aspects.delete(a);
                changerFiltres();
            } }),
            el("i", { "aria-hidden": "true" }), t("Afficher le fan-made"))),
    );
    if (focusPack) {
        const champ = zone.querySelector(".db-pack-recherche");
        champ.focus();
        champ.setSelectionRange(champ.value.length, champ.value.length);
    }
    rendreRail();
}

function rendreRail() {
    remplacer($("#db-rail"),
        SECTIONS.map((s) => {
            const nb = nombreDansSection(s.cle);
            return el("button", {
                type: "button", class: nb ? "est-actif" : "", title: t(s.titre), "aria-label": t(s.titre),
                onclick: () => ouvrirSection(s.cle),
            }, el("i", { class: `fa ${s.rail}`, "aria-hidden": "true" }), nb ? el("span", { class: "db-rail-nb" }, String(nb)) : null);
        }),
        el("button", { type: "button", class: etat.filtres.fanMade ? "est-actif" : "", title: t("Afficher le fan-made"), "aria-label": t("Afficher le fan-made"),
            onclick: () => ouvrirSection(null) }, "FM"));
}

const largeurPortable = () => window.matchMedia("(max-width: 1599px)").matches;

/** Depuis le rail : ouvre la section demandée, dans la colonne ou en panneau. */
function ouvrirSection(cle) {
    if (cle) etat.sectionsOuvertes.add(cle);
    if (largeurPortable()) document.body.classList.add("db-panneau-filtres");
    else replierFiltres(false);
    rendreFiltres();
    const cible = cle && document.querySelector(`#db-filtres [data-section="${cle}"]`);
    if (cible) cible.scrollIntoView({ block: "nearest" });
}

function replierFiltres(replies) {
    document.body.classList.toggle("db-filtres-replies", replies);
    try { localStorage.setItem(CLE_REPLIES, replies ? "1" : "0"); } catch { /* préférence non critique */ }
}

/** Filtres de départ : aspects du deck + Basique, fan-made affiché seulement
 *  si le héros ou le deck en contient. Rien n'est gardé d'une visite à l'autre. */
function reglerFiltresParDefaut() {
    const texte = etat.filtres.texte;
    etat.filtres = filtresVides();
    etat.filtres.texte = texte;
    if (!etat.hero) return;
    const v = valider();
    etat.filtres.aspects = aspectsParDefaut(v.aspects, estStanLee(etat.hero));
    const heroCarte = cards.get(etat.hero.heroCardId);
    etat.filtres.fanMade = !!(heroCarte && heroCarte.custom)
        || [...etat.choisies.keys()].some((id) => { const c = cards.get(id); return c && c.custom; });
}

/* ---------------- Grille ---------------- */

const ctxFiltres = {
    ressourcesDe,
    motsClesDe,
    correspondTexte: (carte, texte) => correspondRecherche(carte, texte,
        { nomsFr: NOMS_FR, nomAffiche: nomFr(carte), texteAffiche: texteFr(carte) }),
};

/** La version affichée d'une carte réimprimée : celle du deck, sinon celle
 *  choisie, sinon l'origine. Anglais seulement : en français, l'origine et la
 *  réédition ont le MÊME scan (assets/pics-fr). */
function versionMontree(idPool, cartePool) {
    const versions = langueActuelle() === "fr" ? [] : versionsDe(cartePool.full_link_id || idPool);
    const id = versions.length ? (versionDansLeDeck(idPool, etat.choisies) || etat.arts.get(versions[0]) || versions[0]) : idPool;
    return { id, versions };
}

/** Même carte, quelle que soit l'impression : la clé de dédoublonnage du pool. */
const cleImpression = (c) => `${c.name}|${c.class}|${c.type}`;

async function rendreGrille() {
    const pool = await poolJoueur(estStanLee(etat.hero));
    if (!document.querySelector("#db-filtres .db-chip")) rendreFiltres();
    const tri = comparateur(etat.triGrille, nomCarte);
    const passent = pool.filter((x) => passeFiltres(x.carte, etat.filtres, ctxFiltres))
        .sort((a, b) => tri(a.carte, b.carte));
    const visibles = passent.slice(0, LIMITE_GRILLE);
    const stan = estStanLee(etat.hero);
    // Une carte du deck peut être une AUTRE impression que celle du pool (le
    // pool garde la première rencontrée) : la tuile montre alors celle du deck,
    // et son compte, au lieu d'un zéro trompeur.
    const duDeck = new Map();
    for (const [id, n] of etat.choisies) {
        const c = cards.get(id);
        if (!c) continue;
        const cle = cleImpression(c);
        const deja = duDeck.get(cle);
        duDeck.set(cle, { id: deja ? deja.id : id, n: (deja ? deja.n : 0) + n });
    }
    remplacer($("#db-grille"),
        visibles.length ? visibles.map(({ id: idPool, carte: cartePool }) => {
            const enDeck = duDeck.get(cleImpression(cartePool));
            const id = enDeck ? enDeck.id : versionMontree(idPool, cartePool).id;
            const carte = cards.get(id) || cartePool;
            const n = enDeck ? enDeck.n : 0;
            const max = /^\*/.test(String(carte.name || "")) ? 1 : maxParDeck(carte);
            const dispo = dispoCarte(id);
            const plein = n >= max;
            return el("div", {
                class: `db-carte${n ? " est-choisie" : ""}${plein ? " est-max" : ""}${dispo.ouvert ? "" : " est-verrou"}`,
                "data-carte": id, tabindex: "0",
                title: dispo.ouvert ? nomCarte(carte) : `${t("Pas encore débloquée")} : ${dispo.etiquette}`,
            },
                el("img", { src: cardImageUrl(id), loading: "lazy", alt: nomCarte(carte) }),
                n ? el("span", { class: "db-badge" }, `${n}/${max}`) : null,
                stan && estSignature(carte) ? el("span", { class: "db-stan" }, `${t("Signature")} · Stan Lee`) : null,
                carte.custom ? el("span", { class: "db-badge-custom", title: `${t("Carte fan-made")} : ${carte.custom}` }, t("CUSTOM")) : null,
                dispo.ouvert ? null : el("span", { class: "db-verrou" }, `🔒 ${dispo.etiquette}`),
                el("div", { class: "db-carte-boutons" },
                    el("button", { type: "button", "data-action": "moins", "aria-label": t("Retirer un exemplaire"), disabled: n === 0 }, "−"),
                    el("button", { type: "button", "data-action": "plus", "aria-label": t("Ajouter un exemplaire"), disabled: !dispo.ouvert || plein }, "+")),
            );
        }) : el("p", { class: "db-vide-grille" }, t("Aucune carte ne correspond à ces filtres.")));
    remplacer($("#db-grille-info"), el("b", {}, String(passent.length)), ` ${t("cartes")}`,
        passent.length > LIMITE_GRILLE ? ` (${LIMITE_GRILLE} ${t("affichées")})` : null);
    rendreEtiquettes();
}

/** Les filtres actifs en étiquettes, chacune retire son groupe d'un clic. */
function rendreEtiquettes() {
    const f = etat.filtres;
    const tags = [];
    const tag = (texte, vider) => tags.push(el("button", { type: "button", title: t("Retirer ce filtre"), onclick: () => { vider(); changerFiltres(); } }, `${texte} ×`));
    if (f.aspects.size) tag([...f.aspects].map(labelAspect).join(", "), () => f.aspects.clear());
    if (f.types.size) tag([...f.types].map(libelleType).join(", "), () => f.types.clear());
    if (f.couts.size) tag(`${t("Coût")} ${[...f.couts].join(", ")}`, () => f.couts.clear());
    if (f.ressources.size) tag([...f.ressources].map((l) => t(RESSOURCE_PAR_LETTRE[l].nom)).join(", "), () => f.ressources.clear());
    if (f.motsCles.size) tag([...f.motsCles].map(t).join(", "), () => f.motsCles.clear());
    if (f.traits.size) tag([...f.traits].join(f.traitsMode === "et" ? " + " : " / "), () => f.traits.clear());
    if (f.packs.size) tag(`${t("Pack")} (${f.packs.size})`, () => f.packs.clear());
    for (const s of STATS) if (f.stats[s.cle].size) tag(`${t(s.libelle)} ${[...f.stats[s.cle]].join(", ")}`, () => f.stats[s.cle].clear());
    if (f.unique) tag(t("Unique"), () => { f.unique = false; });
    remplacer($("#db-etiquettes"), tags);
}

function ajouter(id) {
    const c = cards.get(id);
    if (!c) return;
    // ⚠ LA GATE EST ICI : clic, bouton, deck chargé, tout passe par `ajouter`,
    // et une carte fermée (Legacy) ne rentre par aucune porte.
    const dispo = dispoCarte(id);
    if (!dispo.ouvert) { statut(`${t("Pas encore débloquée")} : ${dispo.etiquette}`, true); return; }
    const n = etat.choisies.get(id) || 0;
    const max = /^\*/.test(String(c.name || "")) ? 1 : maxParDeck(c);
    if (n >= max) { statut(`Maximum ${max} ${t("exemplaires de")} « ${nomCarte(c)} »`, true); return; }
    etat.choisies.set(id, n + 1);
    statut("");
    changement();
}
function retirer(id) {
    const n = etat.choisies.get(id) || 0;
    if (!n) return;
    if (n <= 1) etat.choisies.delete(id); else etat.choisies.set(id, n - 1);
    statut("");
    changement();
}
function changement() {
    programmerBrouillon();
    rendreTout();
}

function installerGrille() {
    const grille = $("#db-grille");
    grille.addEventListener("click", (e) => {
        const tuile = e.target.closest(".db-carte");
        if (!tuile) return;
        const id = tuile.getAttribute("data-carte");
        const bouton = e.target.closest("button[data-action]");
        if (bouton) { if (bouton.dataset.action === "moins") retirer(id); else ajouter(id); return; }
        ajouter(id);
    });
    grille.addEventListener("contextmenu", (e) => {
        const tuile = e.target.closest(".db-carte");
        if (!tuile) return;
        e.preventDefault();
        retirer(tuile.getAttribute("data-carte"));
    });
    grille.addEventListener("keydown", (e) => {
        const tuile = e.target.closest(".db-carte");
        if (!tuile || e.target !== tuile) return;
        if (e.key === "Enter" || e.key === "+") { e.preventDefault(); ajouter(tuile.getAttribute("data-carte")); }
        if (e.key === "Delete" || e.key === "-") { e.preventDefault(); retirer(tuile.getAttribute("data-carte")); }
    });
}

/* ---------------- Aperçu ---------------- */

function idApercu() {
    if (etat.epingle) return etat.epingle;
    if (etat.apercu) return etat.apercu;
    return etat.hero ? etat.hero.heroCardId : null;
}

function rendreApercu() {
    const zone = $("#db-apercu");
    const id = idApercu();
    if (!id) {
        remplacer(zone);
        remplacer($("#db-arts"));
        return;
    }
    const carte = cards.get(id);
    const url = cardImageUrl(id);
    const cadre = el("div", { class: "db-apercu-cadre" }, el("img", { src: url, alt: carte ? nomCarte(carte) : id }));
    remplacer(zone, cadre,
        etat.epingle ? el("button", { type: "button", class: "db-epingle", title: t("Libérer l’aperçu"),
            onclick: () => { etat.epingle = null; rendreApercu(); rendreDeck(); } }, `${t("Épinglée")} ✕`) : null);
    void poserTraduction(cadre, url, id, carte ? carte.traits : []);
    rendreArts(id);
}

/** Les illustrations d'une carte réimprimée, sous forme de vignettes à côté de
 *  l'aperçu. En choisir une y passe aussi les copies du deck : même carte pour
 *  le moteur (`full_link`), seule l'image change. */
function rendreArts(id) {
    const versions = langueActuelle() === "fr" ? [] : versionsDe(id);
    if (versions.length < 2) { remplacer($("#db-arts")); return; }
    remplacer($("#db-arts"), el("span", {}, t("ARTS")),
        versions.map((v) => {
            const dispo = dispoCarte(v);
            return el("img", {
                src: cardImageUrl(v), alt: v, "data-version": v,
                class: `${v === id ? "est-active" : ""}${dispo.ouvert ? "" : " est-verrou"}`,
                title: dispo.ouvert ? t("Choisir cette illustration") : `${t("Pas encore débloquée")} : ${dispo.etiquette}`,
                onclick: () => {
                    if (!dispo.ouvert) return;
                    etat.arts.set(versions[0], v);
                    changerVersion(etat.choisies, v);
                    if (etat.epingle) etat.epingle = v;
                    etat.apercu = v;
                    rendreApercu();
                    changement();
                },
            });
        }));
}

function installerApercu() {
    document.addEventListener("mouseover", (e) => {
        if (etat.epingle) return;
        const cible = e.target.closest?.("[data-carte]");
        if (!cible) return;
        const id = cible.getAttribute("data-carte");
        if (!id || id === etat.apercu) return;
        etat.apercu = id;
        rendreApercu();
        if (etat.onglet === "pioche") rendreDeck();
    });
}

/* ---------------- Colonne du deck ---------------- */

function lignesDuDeck() {
    return [...etat.choisies.entries()].map(([id, n]) => ({ id, n, carte: cards.get(id) })).filter((x) => x.carte);
}
function lignesDuKit() {
    const compte = new Map();
    for (const id of kitDuHeros()) compte.set(id, (compte.get(id) || 0) + 1);
    return [...compte.entries()].map(([id, n]) => ({ id, n, carte: cards.get(id) })).filter((x) => x.carte);
}

function rendreResume(v) {
    const zone = $("#db-resume");
    if (!etat.hero) { remplacer(zone); return; }
    const kit = v.signature || 0;
    const choisies = v.total - kit;
    const courbe = courbeDesCouts([...lignesDuKit(), ...lignesDuDeck()]);
    const haut = Math.max(1, ...courbe.map((x) => x.total));
    remplacer(zone, el("div", { class: "db-resume" },
        el("div", { class: "db-total" }, el("b", {}, kit ? `${choisies} + ${kit} = ${v.total}` : String(v.total)), ` / 40–50 ${t("cartes")}`),
        el("button", {
            type: "button", class: `db-valide ${v.ok ? "est-ok" : "est-ko"}`, "aria-expanded": etat.problemesOuverts ? "true" : "false",
            onclick: () => { etat.problemesOuverts = !etat.problemesOuverts; rendreResume(valider()); },
        }, v.ok ? `✓ ${t("VALIDE")}` : `${v.problemes.length} ${v.problemes.length > 1 ? t("problèmes") : t("problème")}`),
        !v.ok && etat.problemesOuverts ? el("div", { class: "db-problemes" }, v.problemes.map((p) => el("span", {}, `• ${p}`))) : null,
        (v.quotaMax || (v.imposees || []).length) ? el("div", { class: "db-notes" },
            v.quotaMax ? el("span", {}, `+ ${v.horsAspect}/${v.quotaMax} ${t("hors aspect")}`) : null,
            // Cartes qu'un ASPECT impose (Venomized) : le moteur les tire au
            // montage de la partie, elles ne comptent pas dans les 40-50.
            (v.imposees || []).map((x) => el("span", {}, `+ ${x.nombre} ${t("carte(s)")} ${x.set} (${t("coût")} ${x.cout})`))) : null,
        el("div", { class: "db-histo", "aria-label": t("Courbe des coûts") }, courbe.map((x) => el("div", {},
            el("em", {}, String(x.total)),
            el("i", { style: `height:${Math.round((34 * x.total) / haut) + 2}px` }),
            x.palier))),
    ));
}

function rendreOnglets() {
    const onglets = [["liste", "Liste"], ["stats", "Statistiques"], ["pioche", "Pioche"]];
    remplacer($("#db-onglets"), onglets.map(([cle, libelle]) => el("button", {
        type: "button", role: "tab", "aria-selected": etat.onglet === cle ? "true" : "false", "data-onglet": cle,
        onclick: () => { etat.onglet = cle; rendreOnglets(); rendreDeck(); },
    }, t(libelle))));
}

function libelleGroupe(cle, valeur) {
    if (cle === "type") return TYPE_PAR_CLE[valeur] ? t(TYPE_PAR_CLE[valeur].groupe) : valeur;
    if (cle === "cout") return valeur === "—" ? t("Sans coût") : `${t("Coût")} ${valeur}`;
    if (cle === "aspect") return labelAspect(valeur);
    if (cle === "pack") return valeur;
    return t("Cartes");
}

function rendreListe(v) {
    const fautives = cartesFautives({ choisies: etat.choisies, carte: (id) => cards.get(id), verdict: v, regle: reglesAspect(etat.hero, t) });
    const lignes = lignesDuDeck();
    const kit = lignesDuKit();
    const totalKit = kit.reduce((s, l) => s + l.n, 0);
    const tri = el("select", { "aria-label": t("Trier le deck"), onchange: (e) => { etat.triDeck = e.target.value; rendreDeck(); } },
        [["type", "type"], ["cout", "coût"], ["aspect", "aspect"], ["nom", "nom"], ["pack", "pack"]].map(([cle, lib]) =>
            el("option", { value: cle, selected: etat.triDeck === cle }, t(lib))));
    return [
        el("div", { class: "db-liste-barre" }, el("label", {}, `${t("Tri :")} `, tri), el("span", {}, t("survol = aperçu"))),
        totalKit ? el("button", { type: "button", class: "db-kit", "aria-expanded": etat.kitOuvert ? "true" : "false",
            onclick: () => { etat.kitOuvert = !etat.kitOuvert; rendreDeck(); } },
            el("span", {}, `+${totalKit} ${t("cartes du héros")}`), el("span", {}, etat.kitOuvert ? `▾ ${t("masquer")}` : `▸ ${t("voir")}`)) : null,
        totalKit && etat.kitOuvert ? el("div", { class: "db-kit-liste" }, kit.sort((a, b) => comparateur("type", nomCarte)(a.carte, b.carte))
            .map(({ id, n, carte }) => el("span", { "data-carte": id }, el("b", {}, carte.cost ?? "–"), nomCarte(carte), n > 1 ? ` ×${n}` : ""))) : null,
        lignes.length ? grouperDeck(lignes, etat.triDeck, libelleGroupe, nomCarte).map((g) => el("div", { class: "db-grp" },
            el("h4", {}, el("span", {}, g.titre), el("span", {}, String(g.total))),
            g.lignes.map(({ id, n, carte }) => {
                const max = /^\*/.test(String(carte.name || "")) ? 1 : maxParDeck(carte);
                return el("div", {
                    class: `db-ligne aspect-${classeCss(carte.class)}${fautives.has(id) ? " est-fautive" : ""}${etat.epingle === id ? " est-epinglee" : ""}`,
                    "data-carte": id,
                },
                    el("span", { class: "db-ligne-cout" }, carte.cost ?? "–"),
                    el("button", { type: "button", class: "db-ligne-nom", title: t("Épingler l’aperçu"),
                        onclick: () => { etat.epingle = etat.epingle === id ? null : id; etat.apercu = id; rendreApercu(); rendreDeck(); } }, nomCarte(carte)),
                    carte.custom ? el("span", { class: "db-badge-custom", title: `${t("Carte fan-made")} : ${carte.custom}` }, t("CUSTOM")) : null,
                    el("button", { type: "button", class: "db-pm", "aria-label": t("Retirer un exemplaire"), onclick: () => retirer(id) }, "−"),
                    el("span", { class: "db-ligne-n" }, `×${n}`),
                    el("button", { type: "button", class: "db-pm", "aria-label": t("Ajouter un exemplaire"), disabled: n >= max, onclick: () => ajouter(id) }, "+"));
            }))) : el("p", { class: "db-vide" }, t("Ton deck est vide : clique une carte de la grille pour l’ajouter.")),
    ];
}

function rendreStats() {
    const lignes = [...lignesDuKit(), ...lignesDuDeck()];
    if (!lignes.length) return el("p", { class: "db-vide" }, t("Ton deck est vide."));
    const ressources = { R: 0, B: 0, Y: 0, G: 0 };
    const parType = new Map();
    for (const { n, carte } of lignes) {
        for (const l of ressourcesDe(carte)) ressources[l] += n;
        parType.set(carte.type, (parType.get(carte.type) || 0) + n);
    }
    const parAspect = new Map();
    for (const { n, carte } of lignesDuDeck()) parAspect.set(carte.class, (parAspect.get(carte.class) || 0) + n);
    const maxAspect = Math.max(1, ...parAspect.values());
    return el("div", { class: "db-stats" },
        el("div", {}, el("h5", {}, t("Ressources générées")),
            el("div", { class: "db-stats-res" }, Object.entries(ressources).filter(([, x]) => x > 0).map(([l, x]) =>
                el("span", { class: "db-stat-res", style: `--res:${RESSOURCE_PAR_LETTRE[l].couleur}`, title: t(RESSOURCE_PAR_LETTRE[l].nom) }, iconeRessource(l), String(x))))),
        parAspect.size ? el("div", {}, el("h5", {}, t("Répartition par aspect")),
            [...parAspect.entries()].sort((a, b) => b[1] - a[1]).map(([a, x]) => el("div", { class: `db-barre-asp aspect-${classeCss(a)}` },
                el("span", {}, labelAspect(a)), el("i", { style: `width:${Math.round((140 * x) / maxAspect)}px` }), el("b", {}, String(x))))) : null,
        el("div", {}, el("h5", {}, t("Types")),
            el("div", { class: "db-types" }, [...parType.entries()].sort((a, b) => b[1] - a[1]).map(([ty, x]) => el("span", {}, `${x} ${libelleType(ty)}`)))),
    );
}

function paquetCourant() { return construirePaquet(kitDuHeros(), etat.choisies); }
function nouvelleMain() {
    const { heros, alter } = faces();
    const taille = tailleDeMain(etat.pioche.mode === "heros" ? heros : alter);
    const paquet = melanger(paquetCourant());
    etat.pioche.main = paquet.slice(0, taille);
    etat.pioche.reste = paquet.slice(taille);
    etat.pioche.signature = JSON.stringify([...etat.choisies]) + etat.pioche.mode;
}

function rendrePioche() {
    const paquet = paquetCourant();
    if (!paquet.length) return el("p", { class: "db-vide" }, t("Ton deck est vide."));
    if (etat.pioche.signature !== JSON.stringify([...etat.choisies]) + etat.pioche.mode) nouvelleMain();
    const { heros, alter } = faces();
    const tailleAlter = tailleDeMain(alter);
    const tailleHeros = tailleDeMain(heros);
    const taille = etat.pioche.mode === "heros" ? tailleHeros : tailleAlter;
    const id = etat.epingle || etat.apercu;
    const k = id ? paquet.filter((x) => x === id).length : 0;
    const carte = id ? cards.get(id) : null;
    const mode = (m) => { etat.pioche.mode = m; nouvelleMain(); rendreDeck(); };
    return el("div", { class: "db-pioche" },
        el("div", { class: "db-pboutons" },
            el("button", { type: "button", class: etat.pioche.mode === "alter" ? "est-actif" : "", onclick: () => mode("alter") }, `${t("Alter ego")} (${tailleAlter})`),
            el("button", { type: "button", class: etat.pioche.mode === "heros" ? "est-actif" : "", onclick: () => mode("heros") }, `${t("Héros")} (${tailleHeros})`)),
        el("div", { class: "db-main" }, etat.pioche.main.map((x) => el("img", { src: cardImageUrl(x), alt: nomCarte(cards.get(x) || { name: x }), "data-carte": x, loading: "lazy" }))),
        el("div", { class: "db-pboutons" },
            el("button", { type: "button", disabled: !etat.pioche.reste.length, onclick: () => {
                etat.pioche.main.push(etat.pioche.reste.shift()); rendreDeck();
            } }, t("Piocher 1")),
            el("button", { type: "button", onclick: () => { nouvelleMain(); rendreDeck(); } }, t("Nouvelle main"))),
        el("div", { class: "db-reste" }, `${etat.pioche.reste.length} ${t("cartes restantes dans le paquet")}`),
        el("div", { class: "db-proba" },
            k && carte ? [
                el("h5", {}, `${nomCarte(carte)} (×${k}) : ${t("chance de l’avoir")}`),
                probasParTour(paquet.length, k, taille).map(({ tour, proba }) => el("div", {},
                    el("span", {}, tour === 1 ? t("En main de départ") : `${t("Au tour")} ${tour}`),
                    el("b", {}, `${Math.round(proba * 100)} %`))),
                el("p", {}, t("En supposant une main entièrement rejouée à chaque tour.")),
            ] : el("p", {}, t("Survole une carte du deck pour voir ses chances de la piocher."))));
}

function rendreDeck() {
    const zone = $("#db-deck");
    if (!etat.hero) { remplacer(zone, el("p", { class: "db-vide" }, t("Choisis d’abord un héros."))); return; }
    const v = valider();
    remplacer(zone, etat.onglet === "stats" ? rendreStats() : etat.onglet === "pioche" ? rendrePioche() : rendreListe(v));
}

function rendreMobile() {
    const v = valider();
    const n = nombreFiltresActifs(etat.filtres);
    $("#db-mob-filtres").textContent = n ? `${t("Filtres")} (${n})` : t("Filtres");
    $("#db-mob-deck").textContent = `${t("Deck")} (${v.total || 0}) ${v.ok ? "✓" : ""}`.trim();
}

function rendreTout() {
    const v = valider();
    rendreResume(v);
    rendreDeck();
    rendreGrille();
    rendreMobile();
    const aspects = $("#db-heros-aspects");
    if (aspects) aspects.textContent = (v.aspects || []).map(labelAspect).join(" · ");
    $("#db-save-game").disabled = !v.ok;
    $("#db-save-game").title = v.ok ? `${t("Enregistrer dans le jeu")} (Ctrl+S)` : t("Le deck doit être valide pour être enregistré");
}
function rendreToutEtFiltres() { rendreFiltres(); rendreApercu(); rendreTout(); rendrePartir(); }

/* ---------------- « Partir de » ---------------- */

async function chargerSources() {
    if (!etat.hero) { etat.sources = []; rendrePartir(); return; }
    let decks = await catalog.decksForHero(etat.hero);
    // Legacy : un deck tout fait qui contient une carte fermée est caché.
    if (etat.legacy) decks = decks.filter((d) => etat.legacy.deck(d.deck).ouvert);
    etat.sources = decks;
    rendrePartir();
}

function rendrePartir() {
    const sel = $("#db-partir");
    const brouillons = Object.entries(lireBrouillons())
        .filter(([, x]) => etat.hero && x.heroId === etat.hero.id)
        .sort((a, b) => b[1].updated - a[1].updated);
    remplacer(sel,
        el("option", { value: "", selected: !etat.partir }, t("— choisir —")),
        el("option", { value: "vide", selected: etat.partir === "vide" }, t("Deck vide")),
        etat.sources.length ? el("optgroup", { label: t("Decks") }, etat.sources.map((d, i) => el("option", {
            value: `deck:${i}`, selected: etat.partir === `deck:${i}`,
        }, `${d.source === "base" ? t("Base : ") : ""}${d.name}`))) : null,
        brouillons.length ? el("optgroup", { label: t("Brouillons") }, brouillons.map(([id, x]) => el("option", {
            value: `brouillon:${id}`, selected: etat.partir === `brouillon:${id}`,
        }, `${x.deck.name} (${new Date(x.updated).toLocaleString(langueActuelle() === "fr" ? "fr-FR" : "en-GB", { dateStyle: "short", timeStyle: "short" })})`))) : null,
    );
}

async function partirDe(valeur) {
    if (!valeur) return;
    if (etat.choisies.size && !(await confirmer(t("Remplacer ton deck actuel ?"), t("Remplacer")))) { rendrePartir(); return; }
    etat.partir = valeur;
    if (valeur === "vide") {
        etat.choisies.clear();
        etat.brouillonId = null;
    } else if (valeur.startsWith("deck:")) {
        const d = etat.sources[Number(valeur.slice(5))];
        if (!d) return;
        // Un deck de base ou un package est en lecture seule côté jeu : on le
        // renomme « (copie) » ; un deck sauvegardé garde son nom.
        chargerDepuisDeck(d.deck, d.source === "saved" ? d.name : `${d.name} (${t("copie")})`);
        etat.brouillonId = null;
    } else if (valeur.startsWith("brouillon:")) {
        const id = valeur.slice(10);
        const x = lireBrouillons()[id];
        if (!x) return;
        chargerDepuisDeck(x.deck);
        etat.brouillonId = id;
    }
    $("#db-nom").value = etat.nomDeck;
    etat.epingle = null;
    reglerFiltresParDefaut();
    rendreToutEtFiltres();
}

/* ---------------- Enregistrer, exporter, importer ---------------- */

async function sauverDansLeJeu() {
    const v = valider();
    if (!v.ok) {
        etat.problemesOuverts = true;
        rendreResume(v);
        statut(t("Le deck doit être valide pour être enregistré."), true);
        return;
    }
    const deck = deckJson();
    statut(t("Sauvegarde…"));
    try {
        const r = await fetch("/save_deck", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ file_name: deck.name, deck }),
        });
        const rep = await r.json();
        if (!r.ok || rep.error) throw new Error(rep.error || `HTTP ${r.status}`);
        statut(t("Sauvegardé dans le jeu ✔ — il apparaît maintenant dans la préparation de partie (étape Decks)."));
    } catch (e) {
        statut(`${t("Échec de la sauvegarde :")} ${e.message}`, true);
    }
}

function exporter() {
    if (!etat.hero) return;
    const deck = deckJson();
    const blob = new Blob([JSON.stringify(deck, null, 4)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${deck.name.replace(/[^a-zA-Z0-9_-]+/g, "_")}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

async function importer(fichier) {
    let d;
    try { d = JSON.parse(await fichier.text()); }
    catch { statut(t("Ce fichier n’est pas un deck lisible."), true); return; }
    const idHeros = String((d && d.hero && d.hero[0]) || "").split(",")[0];
    const hero = etat.heroes.find((h) => h.heroCardId === idHeros);
    if (!hero || !Array.isArray(d.player_deck)) { statut(t("Ce deck n’est pour aucun héros connu."), true); return; }
    if (etat.choisies.size && !(await confirmer(t("Remplacer ton deck actuel ?"), t("Remplacer")))) return;
    const autreHeros = !etat.hero || etat.hero.id !== hero.id;
    etat.hero = hero;
    chargerDepuisDeck(d, d.name || `${hero.name} custom`);
    etat.brouillonId = null;
    etat.partir = "";
    etat.epingle = null;
    $("#db-nom").value = etat.nomDeck;
    if (autreHeros) { rendreEnTete(); await chargerSources(); }
    reglerFiltresParDefaut();
    rendreToutEtFiltres();
    statut(`${t("Deck importé :")} ${etat.nomDeck}`);
}

/* ---------------- Clavier et panneaux ---------------- */

let fermetureTel = null;

function fermerPanneaux() {
    // Au téléphone, le panneau ouvert est inscrit dans l'historique : on recule.
    if (fermetureTel) { const f = fermetureTel; fermetureTel = null; f(); return true; }
    const ouvert = document.body.classList.contains("db-panneau-filtres") || document.body.classList.contains("db-panneau-deck");
    document.body.classList.remove("db-panneau-filtres", "db-panneau-deck");
    return ouvert;
}

/** Barre du bas : ouvre le panneau des filtres ou du deck. Au téléphone, il
 *  glisse depuis son bord et Retour Android le referme. */
function ouvrirPanneau(nom) {
    document.body.classList.remove("db-panneau-filtres", "db-panneau-deck");
    document.body.classList.add("db-panneau-" + nom);
    if (estTel() && !fermetureTel) {
        fermetureTel = feuilleDansHistorique(() => {
            fermetureTel = null;
            document.body.classList.remove("db-panneau-filtres", "db-panneau-deck");
        });
    }
}

function installerClavier() {
    document.addEventListener("keydown", (e) => {
        const champ = e.target.closest?.("input, select, textarea");
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
            e.preventDefault();
            sauverDansLeJeu();
            return;
        }
        if (e.key === "/" && !champ) {
            e.preventDefault();
            $("#db-recherche").focus();
            return;
        }
        if (e.key === "Escape") {
            if (!$("#db-modale").hidden) return;
            if (fermerPanneaux()) return;
            if (!$("#db-aide-texte").hidden) { basculerAide(false); return; }
            if (etat.epingle) { etat.epingle = null; rendreApercu(); rendreDeck(); return; }
            const recherche = $("#db-recherche");
            if (recherche.value) { recherche.value = ""; etat.filtres.texte = ""; rendreGrille(); rendreMobile(); }
        }
    });
}

function basculerAide(ouvrir) {
    const zone = $("#db-aide-texte");
    zone.hidden = !ouvrir;
    $("#db-aide").setAttribute("aria-expanded", ouvrir ? "true" : "false");
    if (!ouvrir) return;
    const ligne = (code, texte) => el("li", {}, el("code", {}, code), ` ${texte}`);
    remplacer(zone,
        el("div", {}, t("Tape un nom (français ou anglais) ou un texte de carte, ou combine ces raccourcis :")),
        el("ul", {},
            ligne("t:avenger", t("trait")),
            ligne("c:2  c>=3  c:x", t("coût")),
            ligne("a:protection", t("aspect")),
            ligne(langueActuelle() === "fr" ? "ty:allié" : "ty:ally", t("type")),
            ligne("atk>=2  thw:1  pv>=3", t("statistiques")),
            ligne("p:core", t("pack")),
            ligne(langueActuelle() === "fr" ? "u:oui" : "u:yes", t("cartes uniques")),
            ligne('t:"s.h.i.e.l.d"', t("guillemets pour un mot composé"))),
        el("div", {}, t("Raccourcis : / pour chercher, Échap pour vider, Ctrl+S pour enregistrer. Clic droit sur une carte : retirer un exemplaire.")));
}

/* ---------------- Démarrage ---------------- */

/** Le bandeau Legacy au-dessus de la grille. Posé seulement avec le drapeau. */
function poserBandeLegacy(e) {
    const etape = ((e.parcours && e.parcours.etapes) || []).find((x) => x.ouvert && !x.franchi);
    const ou = etape ? etape.nom : t("Tout est débloqué. Bravo.");
    remplacer($("#db-legacy-zone"), el("div", { class: "db-legacy" },
        el("b", {}, "Legacy"),
        el("span", {}, `${t("Vague ouverte")} : ${ou}`),
        el("span", {}, t("Seules les cartes des boîtes déjà ouvertes s'ajoutent au deck."))));
}

function traduirePageStatique() {
    $("#db-ftitre").textContent = t("Filtres");
    $("#db-recherche").placeholder = t("Rechercher (nom FR ou EN, texte, ou t:avenger c:2 atk>=2)");
    $("#db-aide").title = t("Aide de la recherche");
    $("#db-aide").setAttribute("aria-label", t("Aide de la recherche"));
    $("#db-tri-libelle").textContent = t("Tri :");
    remplacer($("#db-tri-grille"), [["aspect", "aspect puis coût"], ["nom", "nom"], ["cout", "coût"], ["type", "type"], ["pack", "pack"]]
        .map(([cle, lib]) => el("option", { value: cle, selected: etat.triGrille === cle }, t(lib))));
    $("#db-astuce").textContent = t("Clic gauche +1 · clic droit −1");
    $("#db-nom").placeholder = t("Nom du deck…");
    $("#db-partir-libelle").textContent = t("Partir de :");
    const titre = (sel, texte) => { $(sel).title = texte; $(sel).setAttribute("aria-label", texte); };
    titre("#db-save-game", `${t("Enregistrer dans le jeu")} (Ctrl+S)`);
    titre("#db-export", t("Exporter le deck (fichier JSON)"));
    titre("#db-import", t("Importer un deck (fichier JSON)"));
    document.querySelectorAll(".db-fermer-panneau").forEach((b) => b.setAttribute("aria-label", t("Fermer")));
}

function installerCommandes() {
    $("#db-recherche").addEventListener("input", (e) => { etat.filtres.texte = e.target.value; rendreGrille(); rendreMobile(); });
    $("#db-aide").onclick = () => basculerAide($("#db-aide-texte").hidden);
    $("#db-tri-grille").onchange = (e) => { etat.triGrille = e.target.value; rendreGrille(); };
    $("#db-nom").oninput = (e) => { etat.nomDeck = e.target.value; programmerBrouillon(); rendreResume(valider()); rendreMobile(); $("#db-save-game").disabled = !valider().ok; };
    $("#db-partir").onchange = (e) => partirDe(e.target.value);
    $("#db-save-game").onclick = sauverDansLeJeu;
    $("#db-export").onclick = exporter;
    $("#db-import").onclick = () => $("#db-import-fichier").click();
    $("#db-import-fichier").onchange = (e) => { const f = e.target.files && e.target.files[0]; e.target.value = ""; if (f) importer(f); };
    $("#db-replier").onclick = () => { replierFiltres(true); rendreFiltres(); };
    document.querySelectorAll(".db-fermer-panneau").forEach((b) => { b.onclick = () => fermerPanneaux(); });
    $("#db-mob-filtres").onclick = () => ouvrirPanneau("filtres");
    $("#db-mob-deck").onclick = () => ouvrirPanneau("deck");
    suivreTel(() => { if (etat.heroes.length) rendreEnTete(); });
    let replies = false;
    try { replies = localStorage.getItem(CLE_REPLIES) === "1"; } catch { /* préférence non critique */ }
    document.body.classList.toggle("db-filtres-replies", replies);
}

async function demarrer() {
    synchroniserLangueServeur();
    traduirePageStatique();
    installerCommandes();
    installerGrille();
    installerApercu();
    installerClavier();
    rendreOnglets();
    statut(t("Chargement des cartes…"));
    await cards.load();
    etat.heroes = await catalog.heroes();
    const params = new URLSearchParams(window.location.search);
    const heroParam = params.get("hero");
    if (heroParam) etat.hero = etat.heroes.find((h) => h.id === heroParam) || null;
    // `?legacy=1` : ouvert depuis le mode Legacy de l'assistant. Sans le
    // drapeau, rien n'est verrouillé : le jeu libre ne l'est jamais.
    if (params.get("legacy") === "1") {
        const e = await etatLegacy(t);
        const extensions = await catalog.extensions();
        etat.legacy = fabriquerDisponibilite(e, extensions,
            (id) => { const c = cards.get(id); return c ? c.package_name : ""; }, t);
        poserBandeLegacy(e);
    }
    if (etat.hero) etat.nomDeck = `${etat.hero.name} custom`;
    rendreEnTete();
    await chargerSources();
    // `?deck=<id>` ouvre l'éditeur DÉJÀ CHARGÉ (identifiants de
    // catalog.decksForHero : id du héros, nom de fichier, « aspect:<libellé> »).
    const deckParam = params.get("deck");
    if (deckParam && etat.hero) {
        const i = etat.sources.findIndex((d) => String(d.id) === deckParam);
        if (i >= 0) {
            const d = etat.sources[i];
            chargerDepuisDeck(d.deck, d.source === "saved" ? d.name : `${d.name} (${t("copie")})`);
            etat.partir = `deck:${i}`;
        }
    }
    $("#db-nom").value = etat.nomDeck;
    await poolJoueur(estStanLee(etat.hero));
    reglerFiltresParDefaut();
    rendreToutEtFiltres();
    statut("");
}

demarrer().catch((e) => statut(`${t("Échec du chargement :")} ${e.message}`, true));
