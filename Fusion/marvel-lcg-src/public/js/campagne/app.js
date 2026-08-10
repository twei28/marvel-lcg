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

/* ---------------------------------------------------------- vue « campagne » -- */

function vueCampagne() {
    const campagne = etat.campagne;
    const definition = etat.definition;
    const index = indexCourant(campagne, definition);
    const finie = estTerminee(campagne, definition);
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
            el("span", {}, finie ? t("Campagne terminée")
                : (t("Étape") + " " + (index + 1) + " / " + definition.scenarios.length)),
        ),
    );

    if (finie) return el("div", { class: "cmp-page-campagne" }, entete(t("Campagne")), barre,
        el("main", { class: "cmp-corps" }, bandeauErreur(), vueConclusion(campagne, definition)));

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

function vueConclusion(campagne, definition) {
    const dernier = definition.scenarios[definition.scenarios.length - 1];
    const epilogue = ((dernier.pages || {}).epilogue || []).map((f) => pageLivret(definition.code, f, "cmp-page-bd"));
    const totalTentatives = Object.values(campagne.tentatives || {}).reduce((a, b) => a + b, 0);

    return el("section", { class: "cmp-conclusion" },
        el("div", { class: "cmp-chapo" },
            el("span", { class: "cmp-chapo-k" }, t("Campagne terminée")),
            el("h1", { class: "cmp-chapo-nom mvl" }, campagne.nom),
        ),
        epilogue.length ? el("div", { class: "cmp-bd" }, epilogue) : null,
        el("div", { class: "cmp-bilan" },
            ligneBilan(t("Boîte"), nomBoite(definition)),
            ligneBilan(t("Difficulté"), campagne.difficulte === "expert" ? t("Campagne experte") : t("Standard")),
            ligneBilan(t("Équipe"), (campagne.equipe || []).map((m) => m.nomHeros || m.heros).join(", ")),
            ligneBilan(t("Scénarios gagnés"), (campagne.termines || []).length + " / " + definition.scenarios.length),
            totalTentatives ? ligneBilan(t("Parties jouées en tout"), String(totalTentatives)) : null,
        ),
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
    if (etat.vue === "campagne" && etat.campagne && etat.definition) root.replaceChildren(vueCampagne());
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
