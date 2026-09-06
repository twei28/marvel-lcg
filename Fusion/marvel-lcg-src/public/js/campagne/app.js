// app.js — l'ecran des campagnes.
//
// Trois vues, une seule a la fois :
//   liste    : les campagnes du joueur + « Nouvelle campagne »
//   creation : choix de la boite, du nom, de la difficulte, du nombre de heros
//   campagne : LE scenario courant, plein ecran, et rien d'autre
//
// Le parti pris de la vue « campagne » : on ne montre pas les cinq mechants en
// vitrine. Une campagne se joue dans l'ordre, donc on affiche l'etape en cours
// comme le livret la presente — la planche d'intro, la page de regles, ce qui
// est en jeu — et un seul bouton pour y aller. Les reglages sont imposes par
// le livret : ni sets modulaires, ni difficulte a rechoisir.
"use strict";

import { apiCampagne, pageLivretUrl } from "/public/js/campagne/api-campagne.js";
import { lireBrouillon, ecrireBrouillon, effacerBrouillon } from "/public/js/campagne/brouillon.js";
import { catalog } from "/public/js/prepare/catalog.js";
import { cards } from "/public/js/prepare/cards.js";
import { cardImageUrl, extensionImageUrl } from "/public/js/prepare/api.js";
import { t, langueActuelle, synchroniserLangueServeur, boutonLangue } from "/public/js/prepare/langue.js";
import { launch } from "/public/js/prepare/launcher.js";

const root = document.getElementById("app");

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

const etat = {
    vue: "liste",
    campagnes: [],
    boites: [],
    campagne: null,      // la campagne ouverte
    definition: null,    // la definition de sa boite
    scenarios: [],       // objets scenario du catalogue, dans l'ordre du livret
    creation: null,      // brouillon en cours de saisie
    erreur: "",
    occupe: false,
};

/* ----------------------------------------------------------------- outils -- */

const nomBoite = (def) => (langueActuelle() === "en" ? (def.nom_en || def.nom) : def.nom) || def.code;

/** Le scenario a jouer : le premier de la definition qui n'est pas termine. */
function indexCourant(campagne, definition) {
    const faits = new Set(campagne.termines || []);
    const i = definition.scenarios.findIndex((s) => !faits.has(s.id));
    return i === -1 ? definition.scenarios.length : i;
}

const estTerminee = (campagne, definition) => indexCourant(campagne, definition) >= definition.scenarios.length;

/** Portrait d'un heros de l'equipe (carte identite face heros). */
function portraitHeros(membre) {
    const id = (membre.identite && membre.identite[0]) || membre.carteHeros || "";
    return el("div", {
        class: "cmp-portrait",
        title: membre.nomHeros || membre.heros || "",
        style: id ? { backgroundImage: `url("${cardImageUrl(id)}")` } : {},
    });
}

/** Une page de livret, cliquable pour l'agrandir. */
function pageLivret(code, fichier, classe) {
    const img = el("img", { class: "cmp-page " + (classe || ""), src: pageLivretUrl(code, fichier), alt: "", loading: "lazy" });
    img.onerror = () => img.remove();
    img.onclick = () => {
        const loupe = el("div", { class: "cmp-loupe", onclick: () => loupe.remove() }, el("img", { src: img.src, alt: "" }));
        document.body.append(loupe);
    };
    return img;
}

function bandeauErreur() {
    if (!etat.erreur) return null;
    return el("div", { class: "cmp-erreur" }, etat.erreur,
        el("button", { class: "cmp-erreur-x", onclick: () => { etat.erreur = ""; rendre(); } }, "×"));
}

async function proteger(action) {
    if (etat.occupe) return;
    etat.occupe = true;
    etat.erreur = "";
    rendre();
    try {
        await action();
    } catch (e) {
        etat.erreur = String(e && e.message ? e.message : e);
    }
    etat.occupe = false;
    rendre();
}

/* ------------------------------------------------------------------ entete -- */

function entete(sousTitre, retour) {
    // Le titre de l'onglet etait ecrit en dur dans campagne.html, donc en
    // francais meme avec l'interface en anglais. On le pose ici, ou t() existe.
    document.title = t("Campagnes") + " — Marvel Champions";
    return el("header", { class: "cmp-entete" },
        el("a", { class: "cmp-marque", href: retour || "/prepare.html" },
            el("span", { class: "cmp-marque-retour" }, "<"),
            el("span", { class: "cmp-marque-bloc" },
                el("img", { class: "cmp-marque-logo", src: "/mvc_logo.svg", alt: "Marvel Champions" }),
                el("span", { class: "cmp-marque-sous" }, sousTitre),
            ),
        ),
        boutonLangue("btn ghost cmp-langue"),
    );
}

/* ------------------------------------------------------------- vue « liste » -- */

function vueListe() {
    const cartes = etat.campagnes.map((c) => {
        const def = etat.boites.find((b) => b.code === c.code);
        const total = def ? def.nb_scenarios : (c.termines || []).length;
        const faits = (c.termines || []).length;
        const finie = total > 0 && faits >= total;
        return el("article", { class: "cmp-carte cut" + (finie ? " finie" : "") },
            el("button", {
                class: "cmp-carte-ouvrir",
                onclick: () => proteger(() => ouvrirCampagne(c.id)),
            },
                el("div", {
                    class: "cmp-carte-illus",
                    style: def && def.cle_extension
                        ? { backgroundImage: `url("${extensionImageUrl(def.cle_extension)}")` } : {},
                }),
                el("div", { class: "cmp-carte-corps" },
                    el("h2", { class: "cmp-carte-nom mvl" }, c.nom || c.code),
                    el("div", { class: "cmp-carte-boite" }, def ? nomBoite(def) : c.code),
                    el("div", { class: "cmp-carte-equipe" }, (c.equipe || []).map(portraitHeros)),
                    el("div", { class: "cmp-carte-etat" },
                        el("span", { class: "cmp-jauge" },
                            el("span", { class: "cmp-jauge-plein", style: { width: total ? (100 * faits / total) + "%" : "0%" } })),
                        el("span", {}, finie ? t("Campagne terminée") : (t("Étape") + " " + (faits + 1) + " / " + total)),
                    ),
                    el("div", { class: "cmp-carte-meta" },
                        (c.difficulte === "expert" ? t("Campagne experte") : t("Standard")),
                        c.derniere_activite ? " · " + String(c.derniere_activite).replace("T", " ") : "",
                    ),
                ),
            ),
            el("button", {
                class: "cmp-carte-suppr",
                title: t("Supprimer cette campagne"),
                onclick: () => {
                    if (!window.confirm(t("Supprimer définitivement la campagne") + " « " + (c.nom || c.id) + " » ?")) return;
                    proteger(async () => {
                        await apiCampagne.supprimer(c.id);
                        etat.campagnes = await apiCampagne.liste();
                    });
                },
            }, "×"),
        );
    });

    return el("div", { class: "cmp-page-liste" },
        entete(t("Campagnes")),
        el("main", { class: "cmp-corps" },
            bandeauErreur(),
            el("div", { class: "cmp-titre-rangee" },
                el("h1", { class: "cmp-titre mvl" }, t("Campagnes")),
                el("button", { class: "btn primary", onclick: () => { etat.vue = "creation"; etat.creation = null; rendre(); } },
                    t("Nouvelle campagne")),
            ),
            cartes.length
                ? el("div", { class: "cmp-grille" }, cartes)
                : el("p", { class: "cmp-vide" }, t("Aucune campagne en cours. Une campagne enchaîne les scénarios d'une boîte dans l'ordre : ce que vous y gagnez vous suit d'un scénario au suivant.")),
        ),
    );
}

/* ---------------------------------------------------------- vue « creation » -- */

function vueCreation() {
    const c = etat.creation || (etat.creation = {
        code: etat.boites[0] ? etat.boites[0].code : "",
        nom: "",
        difficulte: "standard",
        nbJoueurs: 1,
    });
    const boite = etat.boites.find((b) => b.code === c.code);
    if (boite && !c.nom) c.nom = nomBoite(boite);

    const choixBoite = el("div", { class: "cmp-boites" }, etat.boites.map((b) => el("button", {
        class: "cmp-boite cut" + (b.code === c.code ? " sel" : ""),
        onclick: () => { c.code = b.code; c.nom = nomBoite(b); rendre(); },
    },
        el("div", { class: "cmp-boite-illus", style: b.cle_extension ? { backgroundImage: `url("${extensionImageUrl(b.cle_extension)}")` } : {} }),
        el("div", { class: "cmp-boite-nom mvl" }, nomBoite(b)),
        el("div", { class: "cmp-boite-nb" }, b.nb_scenarios + " " + t("scénarios")),
    )));

    const champ = (libelle, aide, controle) => el("div", { class: "cmp-champ" },
        el("label", { class: "cmp-champ-k" }, libelle),
        controle,
        aide ? el("p", { class: "cmp-champ-aide" }, aide) : null);

    return el("div", { class: "cmp-page-creation" },
        entete(t("Nouvelle campagne")),
        el("main", { class: "cmp-corps" },
            bandeauErreur(),
            el("div", { class: "cmp-titre-rangee" },
                el("h1", { class: "cmp-titre mvl" }, t("Nouvelle campagne")),
                el("button", { class: "btn ghost", onclick: () => { etat.vue = "liste"; rendre(); } }, t("Retour")),
            ),
            champ(t("Boîte"), boite ? boite.resume : "", choixBoite),
            el("div", { class: "cmp-reglages" },
                champ(t("Nom de la campagne"), t("Pour la retrouver dans la liste."),
                    el("input", { class: "cmp-saisie", type: "text", value: c.nom, maxlength: "60",
                        oninput: (e) => { c.nom = e.target.value; } })),
                champ(t("Difficulté"), t("Choisie une seule fois : elle vaut pour les cinq scénarios."),
                    el("div", { class: "cmp-segments" },
                        el("button", { class: "cmp-segment" + (c.difficulte === "standard" ? " sel" : ""),
                            onclick: () => { c.difficulte = "standard"; rendre(); } }, t("Standard")),
                        el("button", { class: "cmp-segment" + (c.difficulte === "expert" ? " sel" : ""),
                            onclick: () => { c.difficulte = "expert"; rendre(); } }, t("Campagne experte")),
                    )),
                champ(t("Nombre de héros"), t("Figé pour toute la campagne, comme les identités."),
                    el("div", { class: "cmp-segments" }, [1, 2, 3, 4].map((n) => el("button", {
                        class: "cmp-segment" + (c.nbJoueurs === n ? " sel" : ""),
                        onclick: () => { c.nbJoueurs = n; rendre(); },
                    }, String(n))))),
            ),
            c.difficulte === "expert"
                ? el("p", { class: "cmp-note" }, t("Campagne experte : les PV restants sont reportés d'un scénario au suivant, chaque héros pioche dans son propre jeu d'obligations, et perdre le dernier scénario perd la campagne."))
                : null,
            el("div", { class: "cmp-actions" },
                el("button", {
                    class: "btn launch",
                    disabled: (!c.code || !String(c.nom).trim()) || undefined,
                    onclick: () => {
                        ecrireBrouillon({
                            code: c.code,
                            nom: String(c.nom).trim(),
                            difficulte: c.difficulte,
                            nbJoueurs: c.nbJoueurs,
                        });
                        window.location.href = "/prepare.html?campagne";
                    },
                }, t("Choisir l'équipe")),
            ),
        ),
    );
}

/* ------------------------------------------------------------ le Marche -- */

// Une seule boite a un Marche, « Galaxy's Most Wanted », et c'est sa definition
// qui le dit (bloc `marche`) : rien n'est en dur ici. Entre deux scenarios,
// chaque heros depense les unites gagnees pour ajouter des cartes a son deck.
// Elles y restent jusqu'a la fin de la campagne (livret p.5), et c'est le
// moteur qui les y remet a chaque mise en place, depuis le carnet.

/** Cout en unites lu sur la carte : le livret l'ecrit dans son texte. */
function coutEnUnites(carte) {
    const m = /Unit Cost (\d+)/i.exec((carte && carte.text) || "");
    return m ? parseInt(m[1], 10) : null;
}

/** Les cartes du Marche, dans l'ordre des identifiants du livret. */
function cartesDuMarche(marche) {
    const sortie = [];
    const de = parseInt(marche.premiere_carte, 10);
    const a = parseInt(marche.derniere_carte, 10);
    for (let id = de; id <= a; id++) {
        const cle = String(id);
        const carte = cards.get(cle);
        const cout = coutEnUnites(carte);
        if (carte && cout !== null) sortie.push({ id: cle, carte, cout });
    }
    return sortie;
}

const cleJoueur = (cle, i) => "Player " + (i + 1) + " " + cle;
const listeCarnet = (campagne, cle) => String((campagne.carnet || {})[cle] || "").split(";").filter(Boolean);
const entierCarnet = (campagne, cle) => parseInt((campagne.carnet || {})[cle] || "0", 10) || 0;

/* ------------------------------------------- cartes imposees par le carnet -- */

/** Tous les champs de victoire d'une definition, scenarios et communs melanges. */
function champsDeVictoire(definition) {
    const champs = [];
    for (const s of definition.scenarios || []) champs.push(...(s.victoire || []));
    champs.push(...(definition.victoire_commune || []));
    champs.push(...(definition.victoire_commune_expert || []));
    return champs;
}

/**
 * Les cartes que le carnet EXIGE dans un deck, et qui n'y sont plus.
 *
 * Une carte gagnee en campagne vit d'ordinaire AU CARNET, pas dans le deck
 * enregistre : le moteur la repose a chaque mise en place depuis la cle du
 * carnet (les ameliorations Tech de trors, le materiel S.H.I.E.L.D. de sm, les
 * allies de campagne d'aoa, les cartes du Marche de gmw). Personne ne peut donc
 * la retirer de son deck — elle n'y a jamais ete — et le livret est tenu par
 * construction.
 *
 * Une seule recompense fait l'inverse et CHERCHE la carte dans le deck du
 * joueur : « Planning Ahead » (sm, Reputation 17), ou le livret dit « Each
 * player chooses one card from their deck », puis, au scenario suivant, « each
 * player searches their deck and discard pile for 1 copy of the card recorded
 * in their Planning Ahead section ». Mesure faite a la sonde, avec temoin :
 * carte notee presente dans le deck, elle arrive EN MAIN a la mise en place ;
 * carte notee absente, il ne se passe RIEN — aucune erreur, aucun message, la
 * recompense de la Reputation 17 disparait en silence.
 *
 * D'ou ce controle, au retour de « Modifier les decks » et jamais avant : c'est
 * le seul moment ou un deck de campagne change. Les champs concernes le disent
 * dans les donnees (`"deck": "requis"`), comme tout le reste du format.
 *
 * Rend la liste des manquants : { siege, cle, libelle, carte }.
 */
function cartesRequisesManquantes(campagne, definition, equipe) {
    const manquants = [];
    for (const champ of champsDeVictoire(definition)) {
        if (champ.deck !== "requis") continue;
        equipe.forEach((membre, i) => {
            // parJoueur seulement : une carte imposee designe le deck d'UN
            // joueur. `verifier_campagnes.py` refuse la forme globale.
            const cle = champ.parJoueur ? cleJoueur(champ.cle, i) : champ.cle;
            const notees = champ.format === "liste"
                ? listeCarnet(campagne, cle)
                : [String((campagne.carnet || {})[cle] || "")].filter(Boolean);
            if (!notees.length) return;
            const deck = (membre && membre.deck) || {};
            const dedans = new Set([...(deck.hero_deck || []), ...(deck.player_deck || [])]);
            for (const carte of notees) {
                if (!dedans.has(carte)) {
                    manquants.push({ siege: i, cle, libelle: champ.libelle || champ.cle, carte });
                }
            }
        });
    }
    return manquants;
}

/** « 01058 » -> « Backflip (01058) », pour que le refus soit lisible. */
function nomDeCarte(id) {
    const c = cards.get(id);
    return (c && c.name ? c.name + " (" + id + ")" : id);
}

/**
 * Les cartes deja prises, TOUTE L'EQUIPE CONFONDUE.
 *
 * Livret p.5, derniere phrase de la section : « Only one copy of each card
 * from The Market can be used during a campaign FOR THE PLAYERS AS A GROUP. »
 * Ce n'est donc pas une limite par joueur : si un heros prend Brainstorm,
 * elle sort du Marche pour tous. A quatre, les 28 cartes se partagent.
 */
function cartesDejaPrises(campagne, marche) {
    const prises = new Set();
    const equipe = campagne.equipe || [];
    for (let i = 0; i < Math.max(equipe.length, 4); i++) {
        for (const id of listeCarnet(campagne, cleJoueur(marche.cle_cartes, i))) prises.add(id);
    }
    return prises;
}

/** Achete `entree` pour le siege `i`, puis enregistre. */
async function acheterAuMarche(campagne, marche, i, entree) {
    const cleU = cleJoueur(marche.cle_unites, i);
    const cleC = cleJoueur(marche.cle_cartes, i);
    const solde = entierCarnet(campagne, cleU);
    const deja = listeCarnet(campagne, cleC);
    if (entree.cout > solde) throw new Error(t("Pas assez d'unités."));
    if (cartesDejaPrises(campagne, marche).has(entree.id)) {
        throw new Error(t("Cette carte du Marché est déjà prise par l'équipe."));
    }
    campagne.carnet = { ...(campagne.carnet || {}) };
    campagne.carnet[cleU] = String(solde - entree.cout);
    campagne.carnet[cleC] = [...deja, entree.id].join(";");
    etat.campagne = await apiCampagne.enregistrer(campagne);
    etat.campagnes = await apiCampagne.liste();
}

function vueMarche(campagne, definition) {
    const marche = definition.marche;
    const catalogue = cartesDuMarche(marche);
    const equipe = campagne.equipe || [];

    const prises = cartesDejaPrises(campagne, marche);

    const colonnes = equipe.map((membre, i) => {
        const solde = entierCarnet(campagne, cleJoueur(marche.cle_unites, i));
        const deja = listeCarnet(campagne, cleJoueur(marche.cle_cartes, i));
        const vignettes = catalogue.map((entree) => {
            // Prise par l'equipe : hors de portee pour tout le monde. Le
            // libelle distingue « la mienne » de « celle d'un coequipier ».
            const achetee = prises.has(entree.id);
            const aMoi = deja.includes(entree.id);
            const abordable = entree.cout <= solde;
            return el("button", {
                class: "cmp-marche-carte" + (achetee ? " achetee" : "") + (!achetee && !abordable ? " trop-chere" : ""),
                disabled: (achetee || !abordable) || undefined,
                title: entree.carte.name + " — " + entree.cout + " " + t("unités"),
                onclick: () => proteger(() => acheterAuMarche(campagne, marche, i, entree)),
            },
                el("img", { src: cardImageUrl(entree.id), alt: entree.carte.name, loading: "lazy" }),
                el("span", { class: "cmp-marche-cout" }, String(entree.cout)),
                achetee ? el("span", { class: "cmp-marche-tag" + (aMoi ? "" : " ailleurs") },
                    aMoi ? t("Dans le deck") : t("Prise")) : null,
            );
        });
        return el("section", { class: "cmp-marche-colonne" },
            el("h2", { class: "cmp-marche-heros mvl" }, membre.nomHeros || membre.heros || (t("Joueur") + " " + (i + 1))),
            el("div", { class: "cmp-marche-solde" },
                el("strong", {}, String(solde)), " ", t("unités non dépensées"),
                deja.length ? el("span", { class: "cmp-marche-compte" }, " · " + deja.length + " " + t("carte(s) achetée(s)")) : null),
            el("div", { class: "cmp-marche-grille" }, vignettes),
        );
    });

    return el("div", { class: "cmp-page-campagne" },
        entete(t("Campagne")),
        el("main", { class: "cmp-corps" },
            bandeauErreur(),
            el("div", { class: "cmp-titre-rangee" },
                el("h1", { class: "cmp-titre mvl" }, marche.titre || t("Le Marché")),
                el("button", { class: "btn ghost", onclick: () => { etat.vue = "campagne"; rendre(); } }, t("Retour")),
            ),
            el("p", { class: "cmp-champ-aide" }, marche.aide || ""),
            colonnes.length ? el("div", { class: "cmp-marche" }, colonnes)
                : el("p", { class: "cmp-vide" }, t("Aucune équipe : commencez la campagne d'abord.")),
        ),
    );
}

/* ----------------------------------------------------------- vue « enquete » -- */

/**
 * La grille de deduction du carnet officiel d'Agents of S.H.I.E.L.D.
 *
 * Livret p.5 : « The campaign log contains a list of all possible combinations
 * of means, motive, and opportunity, with each combination implicating one of
 * the board members. By gathering evidence cards, the players narrow down the
 * remaining possible combinations, one of which is secreted in the A.I.M.
 * envelope. »
 *
 * Vingt-sept combinaisons, neuf par membre, relevees une a une sur
 * `mc50_agents_of_shield_campaign_log.pdf` et rangees dans `enquete` de
 * `data/campagnes/aos.json` — c'est de la donnee imprimee, pas une regle a
 * deviner.
 *
 * Le geste du livret est de RAYER : chaque preuve obtenue elimine toutes les
 * combinaisons qui la contiennent, puisque la taupe, elle, est faite des
 * preuves restees dans l'enveloppe A.I.M. Ici le rayage est DEDUIT du carnet
 * (`Evidence Gained`) au lieu d'etre coche a la main : le joueur ne peut pas
 * se tromper, et rien a enregistrer.
 *
 * Ce que l'ecran ne sait pas, et ne doit pas savoir : quelles preuves sont
 * dans l'enveloppe A.I.M. Le serveur les garde (`_sans_secret`), donc meme en
 * lisant le code de cette page on n'apprend rien.
 */
function preuvesObtenues(campagne, enquete) {
    const gagnees = new Set(listeCarnet(campagne, enquete.cle_preuves));
    return enquete.preuves.map((p) => ({ ...p, obtenue: gagnees.has(p.id) }));
}

/** Une combinaison tombe des qu'elle contient UNE preuve obtenue. */
function combinaisonsDeMembre(membre, obtenues) {
    return membre.combinaisons.map((brut) => {
        const ids = brut.split(";");
        return { ids, eliminee: ids.some((id) => obtenues.has(id)) };
    });
}

const nomPreuve = (p) => (langueActuelle() === "en" ? (p.nom_en || p.nom) : p.nom);

function pastillePreuve(preuve, eliminee) {
    // La teinte est posee sur `background`, pas sur une propriete
    // personnalisee : `el()` applique les styles par `Object.assign`, qui
    // ignore silencieusement les cles `--*` (il faut `setProperty`). Avec
    // `--teinte`, le fond restait transparent et le texte sombre du CSS
    // devenait illisible sur le fond noir de la page.
    return el("span", {
        class: "cmp-enq-pastille" + (eliminee ? " eliminee" : ""),
        style: { background: preuve ? preuve.teinte : "#8b8b8b" },
        title: preuve ? nomPreuve(preuve) : "",
    }, preuve ? preuve.court : "?");
}

function vueEnquete(campagne, definition) {
    const enquete = definition.enquete;
    const preuves = preuvesObtenues(campagne, enquete);
    const parId = new Map(preuves.map((p) => [p.id, p]));
    const obtenues = new Set(preuves.filter((p) => p.obtenue).map((p) => p.id));

    let restantesEnTout = 0;

    const blocs = enquete.membres.map((membre) => {
        const lignes = combinaisonsDeMembre(membre, obtenues);
        const restantes = lignes.filter((l) => !l.eliminee).length;
        restantesEnTout += restantes;
        return el("section", {
            class: "cmp-enq-bloc" + (restantes === 0 ? " disculpe" : ""),
        },
            el("h2", { class: "cmp-enq-membre mvl" }, membre.nom),
            el("p", { class: "cmp-enq-compte" },
                restantes === 0
                    ? t("Mis hors de cause")
                    : restantes + " " + (restantes > 1 ? t("combinaisons possibles") : t("combinaison possible"))),
            el("div", { class: "cmp-enq-entetes" },
                enquete.series.map((serie) => el("span", { class: "cmp-enq-entete" }, t(serie.libelle)))),
            el("div", { class: "cmp-enq-lignes" },
                lignes.map((ligne) => el("div", {
                    class: "cmp-enq-ligne" + (ligne.eliminee ? " eliminee" : ""),
                }, ligne.ids.map((id) => pastillePreuve(parId.get(id), ligne.eliminee))))),
        );
    });

    // La legende montre les neuf cartes : elles existent toutes, les connaitre
    // ne revele rien. Ce qui compte est de distinguer celles qu'on TIENT.
    const legende = enquete.series.map((serie) => el("div", { class: "cmp-enq-serie" },
        el("h3", { class: "cmp-enq-serie-titre" }, t(serie.libelle)),
        el("div", { class: "cmp-enq-cartes" },
            preuves.filter((p) => p.serie === serie.cle).map((p) => el("figure", {
                class: "cmp-enq-carte" + (p.obtenue ? " obtenue" : ""),
                title: nomPreuve(p),
            },
                el("img", { src: cardImageUrl(p.id), alt: nomPreuve(p), loading: "lazy" }),
                el("figcaption", {}, nomPreuve(p)),
            ))),
    ));

    const nbObtenues = preuves.filter((p) => p.obtenue).length;

    return el("div", { class: "cmp-page-campagne" },
        entete(t("Campagne")),
        el("main", { class: "cmp-corps" },
            bandeauErreur(),
            el("div", { class: "cmp-titre-rangee" },
                el("h1", { class: "cmp-titre mvl" }, enquete.titre || t("L'enquête")),
                el("button", { class: "btn ghost", onclick: () => { etat.vue = "campagne"; rendre(); } }, t("Retour")),
            ),
            el("p", { class: "cmp-champ-aide" }, enquete.aide || ""),
            el("p", { class: "cmp-enq-bilan" },
                nbObtenues + " " + (nbObtenues > 1 ? t("preuves obtenues") : t("preuve obtenue")),
                " · ",
                restantesEnTout === 1
                    ? el("strong", {}, t("une seule combinaison tient encore : la taupe est démasquée."))
                    : restantesEnTout + " " + t("combinaisons encore possibles")),
            el("div", { class: "cmp-enq-grille" }, blocs),
            el("div", { class: "cmp-enq-legende" },
                el("h2", { class: "cmp-enq-legende-titre" }, t("Les neuf preuves")),
                el("div", { class: "cmp-enq-series" }, legende)),
        ),
    );
}

/* ---------------------------------------------------------- vue « campagne » -- */

function vueCampagne() {
    const campagne = etat.campagne;
    const definition = etat.definition;
    const index = indexCourant(campagne, definition);
    // Perdue au dernier scenario : elle est finie, elle aussi, et il ne reste
    // rien a lancer. Le drapeau est pose par le panneau de recompenses du
    // plateau, seul endroit qui sache si le livret la donne pour perdue.
    const perdue = Boolean(campagne.perdue);
    const finie = perdue || estTerminee(campagne, definition);
    const scenario = finie ? definition.scenarios[definition.scenarios.length - 1] : definition.scenarios[index];
    const duCatalogue = etat.scenarios.find((s) => s.id === scenario.id);

    const enCours = campagne.partieEnCours && campagne.partieEnCours.scenario === scenario.id;
    const tentatives = (campagne.tentatives || {})[scenario.id] || 0;

    const barre = el("div", { class: "cmp-barre" },
        el("button", { class: "btn ghost", onclick: () => proteger(async () => {
            etat.campagne = null; etat.vue = "liste";
            etat.campagnes = await apiCampagne.liste();
        }) }, t("Toutes les campagnes")),
        el("div", { class: "cmp-barre-id" },
            el("strong", { class: "cmp-barre-nom mvl" }, campagne.nom),
            el("span", { class: "cmp-barre-boite" }, nomBoite(definition),
                campagne.difficulte === "expert" ? " · " + t("Campagne experte") : ""),
        ),
        el("div", { class: "cmp-barre-equipe" }, (campagne.equipe || []).map(portraitHeros)),
        el("div", { class: "cmp-barre-etape" },
            el("span", { class: "cmp-jauge" },
                el("span", { class: "cmp-jauge-plein", style: { width: (100 * (campagne.termines || []).length / definition.scenarios.length) + "%" } })),
            el("span", {}, perdue ? t("Campagne perdue")
                : finie ? t("Campagne terminée")
                : (t("Étape") + " " + (index + 1) + " / " + definition.scenarios.length)),
        ),
    );

    if (finie) return el("div", { class: "cmp-page-campagne" }, entete(t("Campagne")), barre,
        el("main", { class: "cmp-corps" }, bandeauErreur(), vueConclusion(campagne, definition, perdue)));

    const pages = scenario.pages || {};
    const intro = (pages.intro || []).map((f) => pageLivret(definition.code, f, "cmp-page-bd"));
    const regles = (pages.regles || []).map((f) => pageLivret(definition.code, f, "cmp-page-regles"));
    // `pages_regles` etait documente au format des campagnes et lu par AUCUN
    // code : les pages de regles valables pour toute la boite, mode expert
    // compris, dormaient sur le disque. Quatre fichiers concernes avant meme
    // qu'on en ajoute, trois pour trors et un pour sm. Constate le 10/8/2026.
    const reglesCampagne = (definition.pages_regles || [])
        .map((f) => pageLivret(definition.code, f, "cmp-page-regles"));

    const sets = duCatalogue
        ? [...(duCatalogue.rawJson.encounter_sets || []), ...(duCatalogue.rawJson.modular_sets || [])]
        : [];

    const colonneRecit = el("section", { class: "cmp-recit" },
        el("div", { class: "cmp-chapo" },
            el("span", { class: "cmp-chapo-k" }, t("Scénario") + " " + scenario.numero + " / " + definition.scenarios.length),
            el("h1", { class: "cmp-chapo-nom mvl" }, langueActuelle() === "en" ? scenario.nom : (scenario.nom_fr || scenario.nom)),
        ),
        intro.length ? el("div", { class: "cmp-bd" }, intro) : null,
        el("p", { class: "cmp-resume" }, scenario.resume),
    );

    const colonneMission = el("aside", { class: "cmp-mission" },
        el("div", { class: "cmp-bloc" },
            el("h2", { class: "cmp-bloc-t" }, t("Ce qui est en jeu")),
            el("p", { class: "cmp-enjeu" }, scenario.enjeu || ""),
        ),
        el("div", { class: "cmp-bloc" },
            el("h2", { class: "cmp-bloc-t" }, t("Mise en place")),
            el("p", { class: "cmp-bloc-aide" }, t("Imposée par le livret : le jeu la met en place pour toi, y compris ce que la campagne a déjà ajouté.")),
            sets.length ? el("ul", { class: "cmp-sets" }, sets.map((s) => el("li", {}, titreSet(s)))) : null,
            regles,
        ),
        reglesCampagne.length ? el("div", { class: "cmp-bloc" },
            el("h2", { class: "cmp-bloc-t" }, t("Règles de la campagne")),
            el("p", { class: "cmp-bloc-aide" },
                t("Les pages du livret qui valent pour toute la campagne, mode expert compris.")),
            reglesCampagne,
        ) : null,
        el("div", { class: "cmp-lancer" },
            tentatives ? el("p", { class: "cmp-tentatives" },
                tentatives === 1 ? t("Une tentative déjà jouée sur ce scénario.")
                    : (tentatives + " " + t("tentatives déjà jouées sur ce scénario."))) : null,
            enCours
                ? el("a", { class: "btn launch", href: "/app/board.html" }, t("Reprendre le scénario en cours"))
                : el("button", { class: "btn launch", onclick: () => proteger(() => lancerScenario(scenario)) },
                    t("Lancer le scénario")),
            // Le livret l'autorise a chaque scenario, et le jeu le refusait :
            // « each player must use their chosen identity for the entire
            // campaign, but they are free to change aspects and alter the
            // contents of their deck between scenarios ». Mutant Genesis en
            // fait meme un pilier, le role-building. On repasse par l'ecran de
            // preparation, seul endroit qui sait choisir un deck, et l'identite
            // est verifiee au retour.
            // Le Marche n'existe que pour la boite qui le declare.
            (definition.marche && !enCours) ? el("button", {
                class: "btn ghost",
                onclick: () => { etat.vue = "marche"; rendre(); },
            }, definition.marche.titre || t("Le Marché")) : null,
            // L'enquete, elle, reste consultable meme partie en cours : on ne
            // touche a rien en la lisant, et c'est justement pendant qu'on
            // joue qu'on veut savoir quelles combinaisons tiennent encore.
            definition.enquete ? el("button", {
                class: "btn ghost",
                onclick: () => { etat.vue = "enquete"; rendre(); },
            }, definition.enquete.titre || t("L'enquête")) : null,
            enCours ? null : el("button", {
                class: "btn ghost",
                onclick: () => {
                    ecrireBrouillon({
                        modifie: etat.campagne.id,
                        code: definition.code,
                        nom: etat.campagne.nom,
                        difficulte: etat.campagne.difficulte,
                        nbJoueurs: (etat.campagne.equipe || []).length || 1,
                        identites: (etat.campagne.equipe || []).map((m) => m.nomHeros || m.heros),
                        // L'equipe part AVEC, pour que l'ecran de preparation
                        // la remette en place au lieu de repartir d'une page
                        // blanche. Sous une AUTRE cle que `equipe` : c'est
                        // l'arrivee de `equipe` qui signale, au retour, que la
                        // preparation a valide quelque chose. Les confondre
                        // ferait enregistrer une modification que personne
                        // n'aurait faite, au premier passage sur cet ecran.
                        equipeActuelle: etat.campagne.equipe || [],
                    });
                    window.location.href = "/prepare.html?campagne";
                },
            }, t("Modifier les decks")),
            enCours ? el("button", {
                class: "btn ghost",
                onclick: () => {
                    if (!window.confirm(t("Abandonner la partie en cours et refaire ce scénario depuis le début ?"))) return;
                    proteger(async () => {
                        etat.campagne.partieEnCours = null;
                        etat.campagne = await apiCampagne.enregistrer(etat.campagne);
                    });
                },
            }, t("Abandonner et recommencer")) : null,
        ),
    );

    return el("div", { class: "cmp-page-campagne" },
        entete(t("Campagne")),
        barre,
        el("main", { class: "cmp-corps cmp-corps-scenario" },
            bandeauErreur(),
            el("div", { class: "cmp-duo" }, colonneRecit, colonneMission),
        ),
    );
}

/**
 * Le score final que le livret fait noter A LA FIN, et nulle part ailleurs.
 *
 * Sinister Motives, p.5 et p.17 (encart VICTORY du scenario 5, sous
 * « Optional ») : « Using the "Conditions" section of the reputation track,
 * calculate your group's total reputation value, then mark that number of
 * nodes. In the "Final Reputation Score" section of the campaign log, record a
 * value equal to the number of nodes marked on the reputation track. »
 *
 * Sa place est donc le BILAN, pas le carnet : aucune mise en place ne le relit,
 * et l'inscrire au carnet aurait demande une cle que le moteur ne connait pas —
 * `verifier_campagnes.py` la refuserait, a juste titre. Il vit dans la campagne,
 * sous `scoreFinal`.
 *
 * Le total de depart est la piste cumulee du carnet ; la saisie n'ajoute que le
 * dernier calcul, celui de la partie qu'on vient de gagner. Facultatif de bout
 * en bout : tant que rien n'est enregistre, le bilan propose, il n'exige pas.
 *
 * Rien de tout cela n'est en dur : une boite sans bloc `bilan` n'affiche rien.
 */
function blocScoreFinal(campagne, definition) {
    const bilan = definition.bilan;
    if (!bilan) return null;
    const acquis = typeof campagne.scoreFinal === "number";
    const base = entierCarnet(campagne, bilan.cle);

    if (acquis) {
        return el("div", { class: "cmp-bilan-score" },
            el("div", { class: "cmp-bilan-score-t" }, bilan.titre),
            el("div", { class: "cmp-bilan-score-v mvl" }, String(campagne.scoreFinal)),
            bilan.aide ? el("p", { class: "cmp-bloc-aide" }, bilan.aide) : null,
        );
    }

    const saisie = el("input", {
        class: "cmp-saisie cmp-saisie-score", type: "number", min: "0", step: "1", value: "0",
    });
    return el("div", { class: "cmp-bilan-score" },
        el("div", { class: "cmp-bilan-score-t" }, bilan.titre),
        bilan.aide ? el("p", { class: "cmp-bloc-aide" }, bilan.aide) : null,
        el("label", { class: "cmp-bilan-score-l" },
            el("span", {}, (bilan.libelle_ajout || t("Dernier calcul")) + " : "),
            saisie,
        ),
        bilan.aide_ajout ? el("p", { class: "cmp-bloc-aide" }, bilan.aide_ajout) : null,
        el("p", { class: "cmp-bilan-score-base" },
            t("Piste cumulée au carnet") + " : " + base),
        el("button", {
            class: "btn launch cmp-bilan-score-ok",
            onclick: () => proteger(async () => {
                const ajout = parseInt(saisie.value, 10);
                etat.campagne.scoreFinal = base + (Number.isFinite(ajout) && ajout > 0 ? ajout : 0);
                etat.campagne = await apiCampagne.enregistrer(etat.campagne);
                rendre();
            }),
        }, t("Enregistrer le score")),
    );
}

function vueConclusion(campagne, definition, perdue) {
    const dernier = definition.scenarios[definition.scenarios.length - 1];
    // Pas de planche d'epilogue sur une defaite : celle du livret raconte la
    // victoire, la montrer ici raconterait le contraire de ce qui s'est passe.
    const epilogue = perdue ? []
        : ((dernier.pages || {}).epilogue || []).map((f) => pageLivret(definition.code, f, "cmp-page-bd"));
    const totalTentatives = Object.values(campagne.tentatives || {}).reduce((a, b) => a + b, 0);
    const defaite = (dernier.defaite || {});

    return el("section", { class: "cmp-conclusion" + (perdue ? " perdue" : "") },
        el("div", { class: "cmp-chapo" },
            el("span", { class: "cmp-chapo-k" }, perdue ? t("Campagne perdue") : t("Campagne terminée")),
            el("h1", { class: "cmp-chapo-nom mvl" }, campagne.nom),
        ),
        perdue && defaite.texte ? el("p", { class: "cmp-resume" }, defaite.texte) : null,
        epilogue.length ? el("div", { class: "cmp-bd" }, epilogue) : null,
        el("div", { class: "cmp-bilan" },
            ligneBilan(t("Boîte"), nomBoite(definition)),
            ligneBilan(t("Difficulté"), campagne.difficulte === "expert" ? t("Campagne experte") : t("Standard")),
            ligneBilan(t("Équipe"), (campagne.equipe || []).map((m) => m.nomHeros || m.heros).join(", ")),
            ligneBilan(t("Scénarios gagnés"), (campagne.termines || []).length + " / " + definition.scenarios.length),
            totalTentatives ? ligneBilan(t("Parties jouées en tout"), String(totalTentatives)) : null,
        ),
        perdue ? null : blocScoreFinal(campagne, definition),
        el("div", { class: "cmp-actions" },
            el("button", { class: "btn ghost", onclick: () => proteger(async () => {
                etat.campagne = null; etat.vue = "liste";
                etat.campagnes = await apiCampagne.liste();
            }) }, t("Toutes les campagnes")),
        ),
    );
}

function ligneBilan(k, v) {
    return el("div", { class: "cmp-bilan-l" },
        el("span", { class: "cmp-bilan-k" }, k),
        el("span", { class: "cmp-bilan-v" }, v));
}

/** "hydra_assault" -> "Hydra Assault" */
function titreSet(nom) {
    return String(nom).replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

/* --------------------------------------------------------------- actions -- */

async function ouvrirCampagne(id) {
    const campagne = await apiCampagne.charger(id);
    const definition = await apiCampagne.definition(campagne.code);
    await cards.load();
    const scenarios = await catalog.scenariosForExtension(definition.cle_extension);
    etat.campagne = campagne;
    etat.definition = definition;
    etat.scenarios = scenarios;
    etat.vue = "campagne";
}

/**
 * Lance le scenario courant.
 *
 * On reconstruit l'etat attendu par launcher.js plutot que d'en dupliquer la
 * logique : c'est lui qui sait composer le NewGameDescriptor, et il ne doit
 * exister qu'UNE facon de demarrer une partie. Les sets modulaires viennent du
 * fichier de scenario, jamais d'un choix : c'est tout l'interet du mode.
 */
async function lancerScenario(scenario) {
    const campagne = etat.campagne;
    const duCatalogue = etat.scenarios.find((s) => s.id === scenario.id);
    if (!duCatalogue) throw new Error(t("Scénario introuvable dans le catalogue :") + " " + scenario.id);

    const joueurs = (campagne.equipe || []).map((m) => ({
        deck: m.deck,
        hero: { name: m.nomHeros || m.heros },
        identity: m.identite ? { hero: m.identite } : null,
    }));

    // La partie est rattachee a la campagne AVANT de partir : si le joueur
    // ferme l'onglet en plein scenario, on saura le lui proposer en reprise.
    campagne.partieEnCours = { scenario: scenario.id, depuis: new Date().toISOString() };
    campagne.tentatives = campagne.tentatives || {};
    campagne.tentatives[scenario.id] = (campagne.tentatives[scenario.id] || 0) + 1;
    etat.campagne = await apiCampagne.enregistrer(campagne);

    // Le PLATEAU n'a aucun moyen de deviner qu'il joue une campagne : la partie
    // qu'il affiche ressemble a n'importe quelle autre. On le lui dit ici, et
    // c'est le panneau de recompenses qui effacera la cle une fois le scenario
    // reporte au carnet (voir ui-app/src/board/campagne/contexte.ts).
    try {
        window.localStorage.setItem("mc-campagne-partie",
            JSON.stringify({ id: etat.campagne.id, scenario: scenario.id }));
    } catch (e) { /* stockage indisponible : le scenario se joue, sans report */ }

    await launch({
        mode: { id: "campaign" },
        scenario: duCatalogue,
        players: joueurs,
        playerCount: joueurs.length,
        premierJoueur: 0,
        seed: null,
        timeoutSecondes: 0,
        reglesV16: true,
        difficulty: {
            base: campagne.difficulte === "expert" ? "expert" : "standard",
            skirmish: false,
            heroic: 0,
            // Imposes par le livret : exactement ceux du fichier de scenario.
            selectedModularSets: duCatalogue.rawJson.modular_sets || [],
        },
        campaignLog: campagne.carnet || {},
    });
}

/* ----------------------------------------------------------------- rendu -- */

// La police Marvel (MarvelRegular-Dj83.ttf) ne contient que A-Z majuscules,
// le point et l'espace : TRENTE caracteres, aucun accent. Un « â » n'y est donc
// pas rendu du tout, il retombe sur Arial Narrow au milieu du mot, et
// « L'Avenement de Crane Rouge » s'affiche moitie dans une police, moitie dans
// l'autre. On retire les accents des seuls textes affiches en police Marvel.
//
// Le meme correctif existe dans prepare/app.js depuis sa refonte ; cet ecran-ci
// utilise la meme classe `.mvl` sans jamais l'avoir applique, et c'est le nom
// des campagnes qui l'a montre. Signale en jeu le 10/8/2026.
//
// On ne touche PAS aux donnees : data/campagnes/*.json garde ses accents, qui
// restent justes partout ailleurs (resumes, infobulles, autres polices).
function sansAccents(texte) {
    return String(texte).normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function corrigerTextesMarvel() {
    document.querySelectorAll(".mvl").forEach((element) => {
        const parcours = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
        let noeud;
        while ((noeud = parcours.nextNode())) {
            const nu = sansAccents(noeud.nodeValue);
            if (nu !== noeud.nodeValue) noeud.nodeValue = nu;
        }
    });
}

function rendre() {
    if (etat.vue === "marche" && etat.campagne && etat.definition && etat.definition.marche)
        root.replaceChildren(vueMarche(etat.campagne, etat.definition));
    else if (etat.vue === "enquete" && etat.campagne && etat.definition && etat.definition.enquete)
        root.replaceChildren(vueEnquete(etat.campagne, etat.definition));
    else if (etat.vue === "campagne" && etat.campagne && etat.definition) root.replaceChildren(vueCampagne());
    else if (etat.vue === "creation") root.replaceChildren(vueCreation());
    else root.replaceChildren(vueListe());
    // Apres CHAQUE rendu : replaceChildren remet des noeuds neufs, un passage
    // unique au chargement ne tiendrait pas.
    corrigerTextesMarvel();
}

(async () => {
    synchroniserLangueServeur();
    try {
        etat.boites = await apiCampagne.boites();
        etat.campagnes = await apiCampagne.liste();
        await cards.load();
    } catch (e) {
        etat.erreur = t("Impossible de charger les campagnes :") + " " + e.message;
    }

    // Retour de l'ecran de preparation avec une equipe : on finit la creation.
    const brouillon = lireBrouillon();
    // Retour d'une MODIFICATION de decks : on ne cree rien, on remplace
    // l'equipe d'une campagne existante. L'identite ne doit pas avoir bouge —
    // c'est la seule chose que le livret interdit de changer — et on refuse
    // plutot que de laisser une campagne changer de heros en silence.
    if (brouillon && brouillon.modifie && brouillon.equipe && brouillon.equipe.length) {
        try {
            const campagne = (etat.campagnes || []).find((c) => c.id === brouillon.modifie);
            if (!campagne) throw new Error(t("Campagne introuvable."));
            const avant = (campagne.equipe || []).map((m) => m.nomHeros || m.heros).join("|");
            const apres = brouillon.equipe.map((m) => m.nomHeros || m.heros).join("|");
            if (avant !== apres) {
                throw new Error(t("Les identités ont changé : elles sont figées pour toute la campagne. Rien n'a été modifié."));
            }
            // Deuxieme refus, apres celui des identites : une carte que le
            // carnet impose au deck ne doit pas en sortir. Le livret sm la
            // fait chercher DANS le deck au scenario suivant, et sans elle la
            // recompense disparait sans un mot (mesure au §11 de CAMPAGNES.md).
            const definition = await apiCampagne.definition(campagne.code);
            const manquants = cartesRequisesManquantes(campagne, definition, brouillon.equipe);
            if (manquants.length) {
                const detail = manquants
                    .map((m) => nomDeCarte(m.carte) + " — " + m.libelle
                        + " (" + t("héros") + " " + (m.siege + 1) + ")")
                    .join(" · ");
                throw new Error(t("Une carte inscrite au carnet a quitté le deck : elle doit y rester pour tout le reste de la campagne. Rien n'a été modifié.")
                    + " " + detail);
            }
            campagne.equipe = brouillon.equipe;
            effacerBrouillon();
            etat.campagne = await apiCampagne.enregistrer(campagne);
            etat.campagnes = await apiCampagne.liste();
            await ouvrirCampagne(campagne.id);
        } catch (e) {
            effacerBrouillon();
            etat.erreur = e.message;
        }
    } else if (brouillon && brouillon.equipe && brouillon.equipe.length) {
        try {
            const campagne = await apiCampagne.enregistrer({
                code: brouillon.code,
                nom: brouillon.nom,
                difficulte: brouillon.difficulte,
                equipe: brouillon.equipe,
                termines: [],
                carnet: {},
                tentatives: {},
                partieEnCours: null,
                creee: new Date().toISOString(),
            });
            effacerBrouillon();
            etat.campagnes = await apiCampagne.liste();
            await ouvrirCampagne(campagne.id);
        } catch (e) {
            etat.erreur = t("La campagne n'a pas pu être créée :") + " " + e.message;
        }
    } else if (brouillon) {
        // Creation abandonnee en route : on ne garde pas un brouillon mort.
        effacerBrouillon();
    }

    rendre();
})();
