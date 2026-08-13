// galerie/app.js — galerie de cartes (page autonome /galerie.html).
//
// Données : /get_cards_json (objet { groupe: [cartes] }, cartes "full_link"
// résolues comme dans js/module/card_statistics.js) et /get_sets_json pour
// l'ordre et le libellé des extensions. Images : même convention que le reste
// du site, cardImageUrl() de js/prepare/api.js ("/<pic_id ou card_id>",
// résolu sans extension par le serveur).
//
// Rendu incrémental : la grille peut dépasser 4000 cartes, on n'ajoute que
// TAILLE_PAGE cellules à la fois ; un IntersectionObserver sur la sentinelle
// déclenche la suite au défilement (le bouton « Afficher plus » reste en
// secours et pour la navigation clavier).
"use strict";

import { cardImageUrl } from "/public/js/prepare/api.js";
import { t, boutonLangue, enregistrerTraductions, langueActuelle } from "/public/js/prepare/langue.js";
import { picIdLangue } from "/public/js/prepare/scans-fr.js";
import { carteFr } from "/public/js/prepare/cartes-fr.js";

/** Image d'une carte dans la langue de l'interface : le scan français quand il
 *  existe, l'anglais sinon (repli assuré par le serveur). Voir scans-fr.js. */
const imageCarte = (imageId) => cardImageUrl(picIdLangue(imageId));

/* ------------------------------------------------------------ libellés -- */
// Libellés propres à la galerie (clé FR source -> anglais). Enregistrés ici,
// PAS dans dico-en.js (fichier partagé en cours de modification ailleurs).
enregistrerTraductions({
    "Galerie de cartes": "Card gallery",
    "Préparation": "Preparation",
    "Retour à la préparation de partie": "Back to game preparation",
    "Rechercher (nom, texte, trait)": "Search (name, text, trait)",
    "Tous les types": "All types",
    "Toutes les extensions": "All expansions",
    "Sets fan-made (custom) inclus dans la liste": "Include fan-made (custom) sets",
    "Aucune carte trouvée": "No card found",
    "Afficher plus": "Show more",
    "Chargement…": "Loading…",
    "Impossible de charger les cartes. Le serveur du jeu est-il lancé ?":
        "Could not load the cards. Is the game server running?",
    "Voir sur marvelcdb ↗": "View on marvelcdb ↗",
    "Fermer": "Close",
    "Extension": "Expansion",
    "Set": "Set",
    "Unique": "Unique",
    /* Types de carte (FR officiels FFG) */
    "Héros": "Hero",
    "Alter ego": "Alter-Ego",
    "Allié": "Ally",
    "Événement": "Event",
    "Amélioration": "Upgrade",
    "Soutien": "Support",
    "Ressource": "Resource",
    "Méchant": "Villain",
    "Sbire": "Minion",
    "Traîtrise": "Treachery",
    "Attachement": "Attachment",
    "Manigance annexe": "Side Scheme",
    "Manigance principale": "Main Scheme",
    "Manigance de joueur": "Player Side Scheme",
    "Environnement": "Environment",
    "État": "Status",
    "Preuve": "Evidence",
    "Défi": "Challenge",
    "Encart": "Insert",
    /* Stats (abréviations FR officielles) */
    "Coût": "Cost",
    "PV": "HP",
    "INT": "THW",
    "ATT": "ATK",
    "MAN": "SCH",
    "DÉF": "DEF",
    "RÉC": "REC",
    "Cartes en main": "Hand size",
    "Menace initiale": "Starting threat",
    "Escalade": "Escalation",
    "Phase": "Stage",
});

/* Ordre d'affichage des types dans le filtre + libellé FR. */
const TYPES = [
    ["Hero", "Héros"],
    ["AlterEgo", "Alter ego"],
    ["Ally", "Allié"],
    ["Event", "Événement"],
    ["Upgrade", "Amélioration"],
    ["Support", "Soutien"],
    ["Resource", "Ressource"],
    ["PlayerSideScheme", "Manigance de joueur"],
    ["Villain", "Méchant"],
    ["Minion", "Sbire"],
    ["Treachery", "Traîtrise"],
    ["Attachment", "Attachement"],
    ["SideScheme", "Manigance annexe"],
    ["MainScheme", "Manigance principale"],
    ["Environment", "Environnement"],
    ["Obligation", "Obligation"],
    ["Status", "État"],
    ["Evidence", "Preuve"],
    ["Challenge", "Défi"],
    ["Leader", "Leader"],
    ["Insert", "Encart"],
];
const TYPE_FR = new Map(TYPES);
function libelleType(code) {
    return t(TYPE_FR.get(code) || code);
}

/* Stats affichées dans l'aperçu (ordre + libellé FR de la clé desc). */
const STATS = [
    ["Cost", "Coût"],
    ["StartingThreat", "Menace initiale"],
    ["HP", "PV"],
    ["THW", "INT"],
    ["ATK", "ATT"],
    ["SCH", "MAN"],
    ["DEF", "DÉF"],
    ["REC", "RÉC"],
    ["HS", "Cartes en main"],
    ["Boost", "Boost"],
    ["Stage", "Phase"],
    ["EscalationThreat", "Escalade"],
];

const TAILLE_PAGE = 60;
const RX_MARVELCDB = /^\d{5}[a-z]?$/;

/* --------------------------------------------------------------- utils -- */
function el(tag, attrs, ...enfants) {
    const noeud = document.createElement(tag);
    if (attrs) {
        for (const [cle, valeur] of Object.entries(attrs)) {
            if (cle === "onclick") noeud.addEventListener("click", valeur);
            else noeud.setAttribute(cle, valeur);
        }
    }
    for (const enfant of enfants) {
        if (enfant == null) continue;
        noeud.append(enfant.nodeType ? enfant : document.createTextNode(String(enfant)));
    }
    return noeud;
}

/** Minuscules sans accents, pour une recherche tolérante. */
function normaliser(texte) {
    return String(texte).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function sansHtml(texte) {
    return String(texte || "").replace(/<[^>]*>/g, " ");
}

/** "* Spider-Man" -> { nom: "Spider-Man", unique: true } (l'étoile marque
    l'unicité dans les données du moteur). */
function nomAffiche(name) {
    const brut = String(name || "");
    const unique = brut.startsWith("* ");
    return { nom: unique ? brut.slice(2) : brut, unique };
}

function litJoli(trait) {
    return String(trait).replace(/_/g, " ").toLowerCase();
}

/* ------------------------------------------------------------- données -- */
let toutes = [];        // toutes les cartes affichables, dans l'ordre des sets
let filtrees = [];      // sous-ensemble après filtres
let setsOrdonnes = [];  // [{ cle: "1. Core Set", groupe: "core", fanMade }]

async function chargerDonnees() {
    const [reponseCartes, reponseSets] = await Promise.all([
        fetch("get_cards_json?"),
        fetch("get_sets_json?"),
    ]);
    if (!reponseCartes.ok) throw new Error("HTTP " + reponseCartes.status);
    const cartesParGroupe = await reponseCartes.json();
    const sets = reponseSets.ok ? await reponseSets.json() : {};

    // Extension de chaque groupe : get_sets_json = { "1. Core Set": { name:
    // "core", ... } } ; la clé lisible sert de libellé, "name" relie au groupe
    // de get_cards_json. Ordre = préfixe numérique de la clé.
    const groupeVersSet = new Map();
    for (const [cle, info] of Object.entries(sets)) {
        if (info && info.name) groupeVersSet.set(info.name, cle);
    }
    const rangDeSet = (cle) => {
        const m = /^(\d+)\./.exec(cle);
        return m ? Number(m[1]) : 500;
    };

    // Même critère que js/prepare/catalog.js : fan-made = groupe sans
    // extension connue, ou extension dont la clé contient "Custom".
    const estFanMade = (cleSet) => !cleSet || /custom/i.test(cleSet);

    // Passe 1 : index des cartes "pleines" (avec leurs propres données),
    // pour résoudre ensuite full_link / ability_link (réimpressions),
    // comme le fait js/module/card_statistics.js.
    // Le francais des cartes fan-made sans scan FR (cartes-fr.js) : on traduit
    // ICI, une fois, pour que la recherche et l'affichage voient la meme carte.
    for (const [groupe, cartes] of Object.entries(cartesParGroupe)) {
        cartesParGroupe[groupe] = cartes.map(carteFr);
    }

    const parId = new Map();
    for (const cartes of Object.values(cartesParGroupe)) {
        for (const carte of cartes) {
            if (!("full_link" in carte)) parId.set(carte.card_id, carte);
        }
    }

    // Passe 2 : liste finale, groupes ordonnés par extension.
    const groupes = Object.keys(cartesParGroupe).sort((a, b) => {
        const ca = groupeVersSet.get(a) || "";
        const cb = groupeVersSet.get(b) || "";
        return rangDeSet(ca) - rangDeSet(cb) || ca.localeCompare(cb);
    });

    for (const groupe of groupes) {
        // Groupe "" = objets techniques du moteur (pions génériques), sans
        // intérêt dans une galerie.
        if (groupe === "") continue;
        const cleSet = groupeVersSet.get(groupe) || "";
        const fanMade = estFanMade(cleSet);
        setsOrdonnes.push({ cle: cleSet, groupe, fanMade });

        for (const brute of cartesParGroupe[groupe]) {
            const source = "full_link" in brute ? parId.get(brute.full_link) : brute;
            if (!source || !source.name) continue;
            let texte = source.text;
            if ("ability_link" in source) {
                const liee = parId.get(source.ability_link);
                if (liee && liee.text) texte = liee.text;
            }
            const desc = source.desc || {};
            const traits = Array.isArray(source.traits) ? source.traits : [];
            const carte = {
                id: brute.card_id,
                // L'image est toujours celle de la carte du groupe (une
                // réimpression a son propre scan), pic_id prioritaire.
                imageId: brute.pic_id || brute.card_id,
                type: source.type || "",
                name: source.name,
                subtitle: source.subtitle || "",
                text: texte || "",
                desc,
                traits,
                setName: source.set_name || "",
                cleSet,
                fanMade,
                recherche: "",
            };
            carte.recherche = normaliser(
                [carte.name, carte.subtitle, sansHtml(carte.text), traits.join(" ")].join(" "));
            toutes.push(carte);
        }
    }
}

/* -------------------------------------------------------------- entête -- */
const grille = document.getElementById("grille");
const champRecherche = document.getElementById("champ-recherche");
const selectType = document.getElementById("select-type");
const selectSet = document.getElementById("select-set");
const toggleFan = document.getElementById("toggle-fanmade");
const compteur = document.getElementById("compteur");
const vide = document.getElementById("vide");
const sentinelle = document.getElementById("sentinelle");
const btnPlus = document.getElementById("btn-plus");

function monterEntete() {
    document.title = t("Galerie de cartes") + " · Marvel Champions";
    document.documentElement.lang = langueActuelle();
    document.getElementById("titre-page").textContent = t("Galerie de cartes");
    const retour = document.getElementById("lien-retour");
    retour.textContent = "← " + t("Préparation");
    retour.title = t("Retour à la préparation de partie");
    document.getElementById("zone-langue").append(boutonLangue());
}

function monterFiltres() {
    champRecherche.placeholder = t("Rechercher (nom, texte, trait)");
    champRecherche.setAttribute("aria-label", t("Rechercher (nom, texte, trait)"));

    const typesPresents = new Set(toutes.map((c) => c.type));
    selectType.append(el("option", { value: "" }, t("Tous les types")));
    for (const [code] of TYPES) {
        if (typesPresents.has(code)) {
            selectType.append(el("option", { value: code }, libelleType(code)));
        }
    }

    selectSet.append(el("option", { value: "" }, t("Toutes les extensions")));
    for (const s of setsOrdonnes) {
        if (!s.cle) continue;
        selectSet.append(el("option", { value: s.cle }, s.cle));
    }

    document.querySelector("#label-fanmade span").textContent = "Fan-made";
    document.getElementById("label-fanmade").title =
        t("Sets fan-made (custom) inclus dans la liste");

    let minuterie = 0;
    champRecherche.addEventListener("input", () => {
        clearTimeout(minuterie);
        minuterie = setTimeout(appliquerFiltres, 150);
    });
    selectType.addEventListener("change", appliquerFiltres);
    selectSet.addEventListener("change", appliquerFiltres);
    toggleFan.addEventListener("change", appliquerFiltres);
    document.getElementById("filtres").hidden = false;
}

/* ------------------------------------------------------------- filtres -- */
function appliquerFiltres() {
    const q = normaliser(champRecherche.value.trim());
    const type = selectType.value;
    const cleSet = selectSet.value;
    const avecFanMade = toggleFan.checked;

    filtrees = toutes.filter((c) => {
        if (type && c.type !== type) return false;
        if (cleSet) {
            // Choisir explicitement une extension custom l'affiche, même
            // si l'interrupteur Fan-made est éteint.
            if (c.cleSet !== cleSet) return false;
        } else if (!avecFanMade && c.fanMade) {
            return false;
        }
        if (q && !c.recherche.includes(q)) return false;
        return true;
    });
    redessiner();
}

function texteCompteur(n, total) {
    if (langueActuelle() === "en") {
        return `${n} card${n === 1 ? "" : "s"} (of ${total})`;
    }
    return `${n} carte${n === 1 ? "" : "s"} (sur ${total})`;
}

/* --------------------------------------------------------------- grille -- */
let nbRendues = 0;

function celluleCarte(carte) {
    const { nom } = nomAffiche(carte.name);
    const cellule = el("figure", {
        class: "g-carte",
        tabindex: "0",
        role: "button",
        "aria-label": nom,
        onclick: () => ouvrirApercu(carte),
    },
        el("img", { src: imageCarte(carte.imageId), alt: nom, loading: "lazy", decoding: "async" }),
        el("figcaption", null, nom));
    cellule.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); ouvrirApercu(carte); }
    });
    return cellule;
}

function rendreSuite() {
    const tranche = filtrees.slice(nbRendues, nbRendues + TAILLE_PAGE);
    const fragment = document.createDocumentFragment();
    for (const carte of tranche) fragment.append(celluleCarte(carte));
    grille.append(fragment);
    nbRendues += tranche.length;
    sentinelle.hidden = nbRendues >= filtrees.length;
}

function redessiner() {
    grille.replaceChildren();
    nbRendues = 0;
    compteur.textContent = texteCompteur(filtrees.length, toutes.length);
    vide.hidden = filtrees.length > 0;
    vide.textContent = t("Aucune carte trouvée");
    rendreSuite();
}

function monterRenduIncremental() {
    btnPlus.textContent = t("Afficher plus");
    btnPlus.addEventListener("click", rendreSuite);
    if ("IntersectionObserver" in window) {
        const observateur = new IntersectionObserver((entrees) => {
            if (entrees.some((e) => e.isIntersecting) && !sentinelle.hidden) {
                rendreSuite();
                // Ré-observer : si la sentinelle reste dans la marge après le
                // lot, aucun nouveau franchissement n'aurait lieu sinon.
                observateur.unobserve(sentinelle);
                observateur.observe(sentinelle);
            }
        }, { rootMargin: "600px" });
        observateur.observe(sentinelle);
    }
}

/* -------------------------------------------------------------- aperçu -- */
let voile = null;

function fermerApercu() {
    if (voile) { voile.remove(); voile = null; }
}
document.addEventListener("keydown", (e) => { if (e.key === "Escape") fermerApercu(); });

function ouvrirApercu(carte) {
    fermerApercu();
    const { nom, unique } = nomAffiche(carte.name);

    const infos = el("div", { class: "infos" },
        el("h2", null, nom + (unique ? " ◆" : ""),
            el("button", { onclick: fermerApercu, "aria-label": t("Fermer") }, "×")));
    if (carte.subtitle) infos.append(el("div", { class: "sous-titre" }, carte.subtitle));

    const meta = [libelleType(carte.type)];
    if (unique) meta.push(t("Unique"));
    if (carte.setName) meta.push(t("Set") + " : " + carte.setName);
    if (carte.cleSet) meta.push(t("Extension") + " : " + carte.cleSet);
    infos.append(el("div", { class: "meta" }, meta.join("  ·  ")));

    if (carte.traits.length) {
        infos.append(el("div", { class: "traits" }, carte.traits.map(litJoli).join(" · ")));
    }

    const puces = [];
    for (const [cle, libelleFr] of STATS) {
        if (carte.desc && carte.desc[cle] !== undefined && carte.desc[cle] !== "") {
            puces.push(el("span", null, t(libelleFr), el("b", null, String(carte.desc[cle]))));
        }
    }
    if (puces.length) infos.append(el("div", { class: "g-stats" }, ...puces));

    if (carte.text) {
        // Le texte de carte vient du serveur du jeu et contient du balisage
        // léger (<b>, <i>...) : on le rend tel quel, comme le plateau.
        const texte = el("div", { class: "texte" });
        texte.innerHTML = carte.text;
        infos.append(texte);
    }

    if (RX_MARVELCDB.test(carte.id)) {
        infos.append(el("a", {
            class: "lien-cdb",
            href: "https://fr.marvelcdb.com/card/" + carte.id,
            target: "_blank",
            rel: "noopener noreferrer",
        }, t("Voir sur marvelcdb ↗")));
    }

    const panneau = el("div", { class: "g-apercu" },
        el("img", { src: imageCarte(carte.imageId), alt: nom }),
        infos);
    voile = el("div", { class: "g-voile", onclick: (e) => { if (e.target === voile) fermerApercu(); } },
        panneau);
    document.body.append(voile);
}

/* ------------------------------------------------------------ démarrage -- */
async function demarrer() {
    monterEntete();
    const chargement = document.getElementById("chargement");
    chargement.textContent = t("Chargement…");
    try {
        await chargerDonnees();
    } catch (erreur) {
        chargement.textContent =
            t("Impossible de charger les cartes. Le serveur du jeu est-il lancé ?");
        return;
    }
    chargement.remove();
    monterFiltres();
    monterRenduIncremental();
    appliquerFiltres();
}

demarrer();
