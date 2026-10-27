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
import { api, cardImageUrl, extensionImageUrl } from "/public/js/prepare/api.js";

/* La COUVERTURE DU LIVRET d'une campagne, ajoutee le 19/09/2026.
 *
 * `public/stories/<code>/00-couverture.jpg` est la premiere page du livret
 * officiel, rasterisee a 975x975 comme les autres planches. On la met en
 * PREMIERE couche de `background-image` et l'illustration d'extension en
 * seconde : si la couverture manque (une boite portee sans livret), le
 * navigateur n'affiche que la couche du dessous, sans case vide ni requete
 * cassee visible a l'oeil. */
function couvertureCampagne(code, cleExtension) {
    const couches = [];
    const tailles = [];
    if (code) {
        couches.push(`url("${pageLivretUrl(code, "00-couverture.jpg")}")`);
        // `contain` et non `cover` : la couverture est CARREE et les deux
        // encadres ne le sont pas. Recadree en `cover`, elle perd son titre
        // (mesure faite sur The Rise of Red Skull, dont le titre est en bas).
        // Entiere sur fond sombre, la boite se reconnait du premier coup.
        tailles.push("contain");
    }
    if (cleExtension) {
        couches.push(`url("${extensionImageUrl(cleExtension)}")`);
        tailles.push("cover");
    }
    if (!couches.length) return {};
    return {
        backgroundImage: couches.join(", "),
        backgroundSize: tailles.join(", "),
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
    };
}
import { t, langueActuelle, synchroniserLangueServeur, boutonLangue } from "/public/js/prepare/langue.js";
import { launch, URL_PLATEAU } from "/public/js/prepare/launcher.js";
import { validate } from "/public/js/prepare/validation.js";
import { urlNarval } from "/public/js/prepare/narval.js";
import * as OL from "/public/js/campagne/ordre-libre.js";
import * as LP from "/public/js/campagne/livre-pages.js";
import { scenarioDuCatalogueDeLEtape } from "/public/js/campagne/catalogue-carnet.js";
import { estTel, suivreTel, enteteTel, feuilleDansHistorique } from "/public/js/tel-pages.js";
import { installerHistorique, noterEcran, reculerVers } from "/public/js/prepare/tel.js";
import { marquerTablette } from "/public/js/tablette.js";

// Tablette (24/10/2026, decision 11) : <html data-tablette> et ses cibles de 44 px (css/tablette-pages.css).
marquerTablette();

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
    invitation: null,    // {joueurs, cles, erreur, copie} : ecran d'invitation en ligne apres lancement multi-heros
};

/* ----------------------------------------------------------------- outils -- */

const nomBoite = (def) => (langueActuelle() === "en" ? (def.nom_en || def.nom) : def.nom) || def.code;

/** Le scenario a jouer : le premier de la definition qui n'est pas termine. */
function indexCourant(campagne, definition) {
    const faits = new Set(campagne.termines || []);
    const i = definition.scenarios.findIndex((s) => !faits.has(s.id));
    return i === -1 ? definition.scenarios.length : i;
}

const estTerminee = (campagne, definition) => definition.ordre_libre
    ? (campagne.termines || []).includes((OL.scenarioFinal(definition) || {}).id)
    : indexCourant(campagne, definition) >= definition.scenarios.length;

/** Portrait d'un heros de l'equipe (carte identite face heros). */
function portraitHeros(membre) {
    const id = (membre.identite && membre.identite[0]) || membre.carteHeros || "";
    return el("div", {
        class: "cmp-portrait",
        title: membre.nomHeros || membre.heros || "",
        style: id ? { backgroundImage: `url("${cardImageUrl(id)}")` } : {},
    });
}

/** Seule une campagne qui declare `livret_fr` a des pages dans `fr/` : les
 *  autres iraient chercher une page absente a chaque affichage. */
function livretFrancais() {
    return langueActuelle() === "fr" && !!(etat.definition && etat.definition.livret_fr);
}

/** Une page de livret, cliquable pour l'agrandir. */
function pageLivret(code, fichier, classe) {
    // En francais, la page traduite si elle existe ; sinon la page anglaise.
    const francais = livretFrancais();
    const img = el("img", { class: "cmp-page " + (classe || ""), src: pageLivretUrl(code, fichier, francais ? "fr" : ""), alt: "", loading: "lazy" });
    let repli = francais;
    img.onerror = () => {
        if (repli) { repli = false; img.src = pageLivretUrl(code, fichier); return; }
        img.remove();
    };
    img.onclick = () => ouvrirLoupe(img.src);
    return img;
}

function ouvrirLoupe(src) {
    // Au téléphone, Retour Android referme la loupe (feuille dans l'historique).
    const fermer = feuilleDansHistorique(() => loupe.remove());
    const loupe = el("div", { class: "cmp-loupe", onclick: () => fermer() }, el("img", { src, alt: "" }));
    document.body.append(loupe);
}

/* ------------------------------------------------------- le livre ouvert -- */
//
// Les pages du livret en double page, qu'on tourne avec des fleches (ecran et
// clavier), au lieu de les empiler : le bouton Lancer etait sous trois pages.
// Une page a la fois sur un ecran etroit, avec balayage du doigt. Le choix des
// pages par etape vit dans livre-pages.js (pur, teste).
//
// L'ecran se reconstruit en entier a chaque `rendre()` : la page ouverte et
// l'onglet sont gardes ici, par livre (`cle`), pour ne pas revenir au debut a
// chaque clic sur une option.

const _livres = new Map();
const _pagesManquantes = new Set();
let _livreActif = null;
const ECRAN_ETROIT = window.matchMedia("(max-width: 900px)");
const MOINS_D_ANIMATION = window.matchMedia("(prefers-reduced-motion: reduce)");

ECRAN_ETROIT.addEventListener("change", () => { if (_livreActif) _livreActif.redessiner(); });
document.addEventListener("keydown", (e) => {
    const loupe = document.querySelector(".cmp-loupe");
    if (e.key === "Escape" && loupe) { loupe.remove(); return; }
    if (loupe || !_livreActif || !_livreActif.racine.isConnected) return;
    const cible = e.target || {};
    if (/^(INPUT|TEXTAREA|SELECT)$/.test(cible.tagName || "") || cible.isContentEditable) return;
    if (e.key === "ArrowRight") { e.preventDefault(); _livreActif.tourner(1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); _livreActif.tourner(-1); }
});

/** Une page du livre : la version francaise si elle existe, sinon l'anglaise ;
 *  absente des deux, elle sort du livre (couverture d'une boite sans livret). */
function feuilleDuLivre(code, page, quandAbsente) {
    const francais = livretFrancais();
    const img = el("img", {
        class: "cmp-page cmp-page-" + page.classe, alt: "", draggable: "false",
        src: pageLivretUrl(code, page.fichier, francais ? "fr" : ""),
    });
    let repli = francais;
    img.onerror = () => {
        if (repli) { repli = false; img.src = pageLivretUrl(code, page.fichier); return; }
        quandAbsente();
    };
    img.onclick = () => ouvrirLoupe(img.src);
    return el("figure", { class: "cmp-livre-feuille" }, img);
}

function livreOuvert(code, cle, onglets) {
    if (!onglets.length) return null;
    const memo = _livres.get(cle) || { onglet: onglets[0].id, debut: 0 };
    _livres.set(cle, memo);
    const racine = el("section", { class: "cmp-livre" });
    const livre = { racine, tourner, redessiner: () => dessiner(0, null) };
    _livreActif = livre;

    const presentes = (onglet) => onglet.pages.filter((p) => !_pagesManquantes.has(code + "/" + p.fichier));
    const ongletCourant = () => onglets.find((o) => o.id === memo.onglet) || onglets[0];
    const simple = (total) => ECRAN_ETROIT.matches || total <= 1;

    function tourner(sens) {
        const pages = presentes(ongletCourant());
        const un = simple(pages.length);
        const suivant = memo.debut + sens * (un ? 1 : 2);
        if (suivant < 0 || suivant >= pages.length) return;
        // La feuille qui se tourne : celle de droite pour avancer, celle de
        // gauche pour reculer, mesuree AVANT de redessiner.
        const feuilles = racine.querySelectorAll(".cmp-livre-feuille");
        const tournee = sens > 0 ? feuilles[feuilles.length - 1] : feuilles[0];
        memo.debut = suivant;
        dessiner(sens, tournee);
    }

    function dessiner(sens, tournee) {
        const onglet = ongletCourant();
        const pages = presentes(onglet);
        const un = simple(pages.length);
        memo.debut = LP.caler(memo.debut, pages.length, un);
        // Au telephone, la page GLISSE de cote (elle a suivi le doigt) au lieu
        // de pivoter sur une reliure qu'on ne voit pas en page seule.
        const glisse = sens !== 0 && estTel() && !MOINS_D_ANIMATION.matches;
        const avant = tournee && !glisse && !MOINS_D_ANIMATION.matches ? {
            src: tournee.querySelector("img").src,
            boite: tournee.querySelector("img").getBoundingClientRect(),
        } : null;

        const visibles = pages.slice(memo.debut, memo.debut + (un ? 1 : 2));
        const double = el("div", { class: "cmp-livre-double" + (visibles.length === 1 ? " seule" : "")
                + (glisse ? (sens > 0 ? " glisse-avance" : " glisse-recule") : "") },
            visibles.map((p) => feuilleDuLivre(code, p, () => {
                if (_pagesManquantes.has(code + "/" + p.fichier)) return;
                _pagesManquantes.add(code + "/" + p.fichier);
                dessiner(0, null);
            })));
        const fleche = (sens2, signe, libelle, actif) => el("button", {
            class: "cmp-livre-fleche " + (sens2 < 0 ? "gauche" : "droite"),
            "aria-label": libelle, title: libelle,
            disabled: actif ? null : "",
            onclick: () => tourner(sens2),
        }, signe);
        const scene = el("div", { class: "cmp-livre-scene" },
            pages.length ? double : el("p", { class: "cmp-livre-vide" }, t("Pas de page de livret pour cette étape.")),
            fleche(-1, "‹", t("Page précédente"), memo.debut > 0),
            fleche(1, "›", t("Page suivante"), memo.debut + visibles.length < pages.length),
        );
        balayage(scene);

        racine.replaceChildren(
            el("div", { class: "cmp-livre-tete" },
                onglets.length > 1 ? el("div", { class: "cmp-livre-onglets", role: "tablist" }, onglets.map((o) => el("button", {
                    class: "cmp-livre-onglet" + (o === onglet ? " sel" : ""), role: "tab",
                    "aria-selected": o === onglet ? "true" : "false",
                    onclick: () => { memo.onglet = o.id; memo.debut = 0; dessiner(0, null); },
                }, t(o.libelle)))) : el("span", { class: "cmp-livre-titre" }, t(onglet.libelle)),
                el("span", { class: "cmp-livre-compteur" }, LP.compteur(memo.debut, pages.length, un)),
            ),
            scene,
        );

        if (avant) {
            // Une copie de l'ancienne feuille, posee la ou elle etait, pivote
            // sur sa reliure : la nouvelle double page est deja dessous.
            const ici = scene.getBoundingClientRect();
            const copie = el("div", {
                class: "cmp-livre-tourne " + (sens > 0 ? "avance" : "recule"),
                style: {
                    left: (avant.boite.left - ici.left) + "px",
                    top: (avant.boite.top - ici.top) + "px",
                    width: avant.boite.width + "px", height: avant.boite.height + "px",
                },
            }, el("img", { src: avant.src, alt: "" }));
            const fin = () => copie.remove();
            copie.addEventListener("animationend", fin);
            setTimeout(fin, 600);
            scene.append(copie);
        }
    }

    // Balayage du doigt : un geste horizontal franc tourne la page, et le
    // « clic » qui le termine n'ouvre pas la loupe.
    // Au telephone, la page suit le doigt pendant le geste (glissement
    // lateral), puis repart a sa place si le geste ne suffit pas.
    function balayage(scene) {
        let depart = null;
        let avale = false;
        const suivre = (dx) => {
            const double = scene.querySelector(".cmp-livre-double");
            if (!double || !estTel()) return;
            double.classList.remove("glisse-avance", "glisse-recule");
            double.style.transition = dx === null ? "" : "none";
            double.style.transform = dx === null ? "" : "translateX(" + dx + "px)";
        };
        scene.addEventListener("pointerdown", (e) => {
            depart = e.pointerType === "mouse" ? null : { x: e.clientX, y: e.clientY };
        });
        scene.addEventListener("pointermove", (e) => {
            if (!depart) return;
            const dx = e.clientX - depart.x;
            if (Math.abs(dx) > 8 && Math.abs(dx) > 1.5 * Math.abs(e.clientY - depart.y)) suivre(dx);
        });
        scene.addEventListener("pointercancel", () => { depart = null; suivre(null); });
        scene.addEventListener("pointerup", (e) => {
            if (!depart) return;
            const dx = e.clientX - depart.x;
            const dy = e.clientY - depart.y;
            depart = null;
            suivre(null);
            if (Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(dy)) {
                avale = true;
                tourner(dx < 0 ? 1 : -1);
            }
        });
        scene.addEventListener("click", (e) => {
            if (avale) { avale = false; e.stopPropagation(); e.preventDefault(); }
        }, true);
    }

    dessiner(0, null);
    return racine;
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
    // Téléphone (zone 2 de la refonte du 09/10/2026) : l'en-tête fin à burger.
    if (estTel()) return enteteTel({ titre: sousTitre, retour: retour || "/prepare.html", ici: "/campagne.html" });
    return el("header", { class: "cmp-entete" },
        el("a", { class: "cmp-marque", href: retour || "/prepare.html" },
            el("span", { class: "cmp-marque-retour" }, "<"),
            el("img", { class: "cmp-marque-narval", src: urlNarval(), alt: "NarwhalChampions" }),
            el("span", { class: "cmp-marque-bloc" },
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
                    style: couvertureCampagne(c.code, def && def.cle_extension),
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
                : el("p", { class: "cmp-vide" }, t("Aucune campagne en cours. Une campagne enchaîne les scénarios d'une boîte dans l'ordre : ce que tu y gagnes te suit d'un scénario au suivant.")),
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
        el("div", { class: "cmp-boite-illus", style: couvertureCampagne(b.code, b.cle_extension) }),
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
                el("button", { class: "btn ghost", onclick: () => retourVers("liste") }, t("Retour")),
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

/** Cout lu sur la carte : le livret l'ecrit dans son texte (« Unit Cost 2 »
 *  pour gmw, « Experience Cost 2 » pour Hunting Season, via `motif_cout`). */
function coutEnUnites(carte, marche) {
    const motif = new RegExp((marche && marche.motif_cout) || "Unit Cost (\\d+)", "i");
    const m = motif.exec((carte && carte.text) || "");
    return m ? parseInt(m[1], 10) : null;
}

/** Les identifiants du Marche : la liste `cartes` si la boite la donne (ids
 *  non numeriques, « hs164 »), sinon la plage `premiere_carte`..`derniere_carte`. */
function idsDuMarche(marche) {
    if (Array.isArray(marche.cartes)) return marche.cartes.map(String);
    const ids = [];
    const de = parseInt(marche.premiere_carte, 10);
    const a = parseInt(marche.derniere_carte, 10);
    for (let id = de; id <= a; id++) ids.push(String(id));
    return ids;
}

/** Les cartes du Marche, dans l'ordre des identifiants du livret. Une carte
 *  sous `verrous` (id -> cle du carnet) n'y entre qu'une fois la cle notee :
 *  Gibbon, « set aside » jusqu'a la victoire contre Vulture. */
function cartesDuMarche(marche, campagne) {
    const sortie = [];
    const verrous = marche.verrous || {};
    for (const cle of idsDuMarche(marche)) {
        if (verrous[cle] && !entierCarnet(campagne || {}, verrous[cle])) continue;
        const carte = cards.get(cle);
        const cout = coutEnUnites(carte, marche);
        if (carte && cout !== null) sortie.push({ id: cle, carte, cout });
    }
    return sortie;
}

/** Le nom de la monnaie du Marche (« unites », « XP »). */
const uniteMarche = (marche) => (marche && marche.unite) ? t(marche.unite) : t("unités");

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
    if (entree.cout > solde) throw new Error(t("Solde insuffisant pour cette carte."));
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
    const catalogue = cartesDuMarche(marche, campagne);
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
                title: entree.carte.name + " — " + entree.cout + " " + uniteMarche(marche),
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
                el("strong", {}, String(solde)), " ", marche.libelle_solde ? t(marche.libelle_solde) : t("unités non dépensées"),
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
                el("button", { class: "btn ghost", onclick: () => retourVers("campagne") }, t("Retour")),
            ),
            el("p", { class: "cmp-champ-aide" }, marche.aide || ""),
            colonnes.length ? el("div", { class: "cmp-marche" }, colonnes)
                : el("p", { class: "cmp-vide" }, t("Aucune équipe : commencez la campagne d'abord.")),
        ),
    );
}

/* ------------------------------------------- zone et tableau de cooperation -- */

/**
 * La zone de cooperation, le tableau « Cooperation Progress » et le journal des
 * etats, tels que le carnet les garde (Skrull Menace, livret p.22-24).
 *
 * Tout vient de la boite (bloc `cooperation`) et du carnet : l'ecran ne calcule
 * rien, il montre. Les cartes de la zone sont en couleur, les autres en gris ;
 * une case du tableau est verte quand `Cooperation Progress` porte
 * « Carte: exigence » ; une ligne complete a gagne sa carte. Le journal est la
 * colonne par scenario du carnet imprime (p.22-23) : `campagne.historique`,
 * ecrit par le panneau de recompenses a chaque scenario gagne.
 */
const enLangue = (fr, en) => (langueActuelle() === "en" ? (en || fr) : fr);

function vueChoixDeLaZone(campagne, definition) {
    return el("div", { class: "cmp-page-campagne" },
        entete(t("Campagne")),
        el("main", { class: "cmp-corps" },
            bandeauErreur(),
            el("div", { class: "cmp-titre-rangee" },
                el("h1", { class: "cmp-titre mvl" }, t("Cartes de la zone de coopération")),
                el("button", { class: "btn ghost", onclick: () => retourVers("campagne") }, t("Retour"))),
            blocChoixDeLaZone(campagne, definition)));
}

function vueCooperation(campagne, definition) {
    const coop = definition.cooperation;
    const zone = new Set(listeCarnet(campagne, coop.cle_zone));
    const cochees = new Set(listeCarnet(campagne, coop.cle_progres).map((x) => x.trim()));

    const colonnes = coop.colonnes.map((col) => el("section", { class: "cmp-coop-col" },
        el("h2", { class: "cmp-coop-col-t" }, enLangue(col.titre, col.titre_en),
            el("span", { class: "cmp-coop-col-n" }, " " + col.ids.filter((id) => zone.has(id)).length + " / " + col.ids.length)),
        el("div", { class: "cmp-coop-cartes" }, col.ids.map((id) => {
            const presente = zone.has(id);
            const c = cards.get(id);
            return el("div", { class: "cmp-coop-carte" + (presente ? " presente" : " absente"), "data-carte": id,
                title: (c && c.name ? c.name : id) + " — " + (presente ? t("dans la zone") : t("pas encore ralliée")) },
                el("img", { src: cardImageUrl(id), alt: c && c.name ? c.name : id, loading: "lazy" }));
        })),
    ));

    const lignes = coop.tableau.map((ligne) => {
        const faites = ligne.exigences.map((e) => cochees.has(ligne.titre + ": " + e));
        const complete = faites.every(Boolean);
        return el("tr", { class: "cmp-coop-ligne" + (complete ? " complete" : ""), "data-ligne": ligne.carte },
            el("th", { scope: "row" },
                el("span", { class: "cmp-coop-ligne-nom" }, ligne.titre),
                complete ? el("span", { class: "cmp-coop-gagnee" }, " ✔ " + t("gagnée")) : null),
            ligne.exigences.map((e, i) => el("td", { class: "cmp-coop-case" + (faites[i] ? " cochee" : "") },
                el("span", { class: "cmp-coop-coche" }, faites[i] ? "✔" : ""), " " + e)));
    });

    const scenarios = definition.scenarios;
    const historique = campagne.historique || {};
    const journal = el("table", { class: "cmp-coop-journal" },
        el("thead", {}, el("tr", {},
            el("th", {}, ""),
            scenarios.map((s) => el("th", { title: enLangue(s.nom_fr || s.nom, s.nom) }, String(s.numero))),
            el("th", {}, t("Maintenant")))),
        el("tbody", {}, coop.journal.map((j) => el("tr", { "data-cle": j.cle },
            el("th", { scope: "row" }, enLangue(j.libelle, j.libelle_en)),
            scenarios.map((s) => el("td", {}, ((historique[s.id] || {})[j.cle]) || "")),
            el("td", { class: "cmp-coop-now" }, (campagne.carnet || {})[j.cle] || "")))));

    return el("div", { class: "cmp-page-campagne" },
        entete(t("Campagne")),
        el("main", { class: "cmp-corps" },
            bandeauErreur(),
            el("div", { class: "cmp-titre-rangee" },
                el("h1", { class: "cmp-titre mvl" }, enLangue(coop.titre, coop.titre_en)),
                el("button", { class: "btn ghost", onclick: () => retourVers("campagne") }, t("Retour"))),
            el("p", { class: "cmp-champ-aide" }, coop.aide || ""),
            el("h2", { class: "cmp-bloc-t" }, t("Zone de coopération")),
            el("div", { class: "cmp-coop" }, colonnes),
            el("h2", { class: "cmp-bloc-t" }, t("Tableau de coopération")),
            el("table", { class: "cmp-coop-tableau" }, el("tbody", {}, lignes)),
            el("h2", { class: "cmp-bloc-t" }, t("Journal par scénario")),
            el("p", { class: "cmp-champ-aide" }, t("Ce que chaque scénario gagné a laissé au carnet (colonnes 1 à 5), puis l'état actuel.")),
            journal,
        ),
    );
}

/**
 * Le choix des cartes de la zone de cooperation, AVANT la partie (scenarios 2 a 5).
 *
 * Livret p.10 : chaque joueur peut melanger UNE carte de chaque type de la zone a son
 * deck. Le moteur savait le demander par des fenetres de question (le nom seul) ; ici on
 * choisit sur les vignettes, et le carnet garde `Player N Cooperation Deck` (ids, « ; »,
 * ou « none » si on a decide de ne rien prendre). Rien de choisi = le jeu pose ses
 * questions a la mise en place, comme avant. Une carte unique prise par un joueur n'est
 * plus offerte aux autres (le moteur ignore de toute facon un doublon).
 */
function zoneChoisissable(campagne, definition, enCours) {
    const coop = definition.cooperation;
    return Boolean(coop && coop.cle_deck && !enCours && indexCourant(campagne, definition) >= 1
        && listeCarnet(campagne, coop.cle_zone).length);
}

function blocChoixDeLaZone(campagne, definition) {
    const coop = definition.cooperation;
    const zone = new Set(listeCarnet(campagne, coop.cle_zone));
    const equipe = campagne.equipe || [];
    const choixDe = (i) => listeCarnet(campagne, cleJoueur(coop.cle_deck, i)).filter((x) => x !== "none");
    const decide = (i) => listeCarnet(campagne, cleJoueur(coop.cle_deck, i)).length > 0;
    const ecrire = (i, ids) => proteger(async () => {
        etat.campagne.carnet = { ...(etat.campagne.carnet || {}),
            [cleJoueur(coop.cle_deck, i)]: ids.length ? ids.join(";") : "none" };
        etat.campagne = await apiCampagne.enregistrer(etat.campagne);
    });
    const colonnes = coop.colonnes.map((col) => ({ col, dispo: col.ids.filter((id) => zone.has(id)) }))
        .filter((x) => x.dispo.length);

    const sections = equipe.map((membre, i) => {
        const miens = choixDe(i);
        const pris = new Set(equipe.flatMap((_, j) => (j === i ? [] : choixDe(j))));
        const lignes = colonnes.map(({ col, dispo }) => {
            const choisie = dispo.find((id) => miens.includes(id));
            const reste = miens.filter((id) => !dispo.includes(id));
            return el("div", { class: "cmp-zone-ligne", "data-type": col.titre },
                el("span", { class: "cmp-zone-type" }, enLangue(col.titre, col.titre_en)),
                el("div", { class: "cmp-zone-choix" },
                    el("button", { class: "cmp-segment" + (!choisie ? " sel" : ""), "data-aucune": "1",
                        onclick: () => ecrire(i, reste) }, t("Aucune")),
                    dispo.map((id) => {
                        const c = cards.get(id);
                        const ailleurs = pris.has(id);
                        return el("button", {
                            class: "cmp-zone-vignette" + (choisie === id ? " sel" : "") + (ailleurs ? " prise" : ""),
                            "data-carte": id, disabled: ailleurs || undefined,
                            title: (c && c.name ? c.name : id) + (ailleurs ? " — " + t("prise par un autre joueur") : ""),
                            onclick: () => ecrire(i, [...reste, id]),
                        }, el("img", { src: cardImageUrl(id), alt: c && c.name ? c.name : id, loading: "lazy" }));
                    })));
        });
        return el("section", { class: "cmp-zone-joueur", "data-joueur": String(i + 1) },
            el("h3", { class: "cmp-zone-heros" }, membre.nomHeros || membre.heros || (t("Joueur") + " " + (i + 1)),
                el("span", { class: "cmp-zone-etat" }, decide(i) ? "" : " · " + t("pas encore choisi : le jeu posera la question"))),
            lignes);
    });
    return el("div", { class: "cmp-bloc cmp-bloc-zone" },
        el("h2", { class: "cmp-bloc-t" }, t("Zone de coopération : cartes pour ce scénario")),
        el("p", { class: "cmp-bloc-aide" }, t("Chaque joueur peut mélanger à son deck UNE carte de chaque type. Elles lui sont rendues à la fin de la partie.")),
        sections);
}

/**
 * L'Elite du scenario, TIREE ET MONTREE avant le lancement (Skrull Menace, livret p.9 a 17).
 *
 * Aux scenarios 1 a 4 le livret fait tirer UNE Elite au hasard parmi celles jamais tirees : l'ecran fait
 * ce tirage, une fois, le garde au carnet (`Next Skrull Elite` = « <scenario>:<nom> ») et le moteur le lit.
 * Au scenario 5 « the remaining » : toutes celles qui restent, rien a tirer. Une Elite deja tiree dont le
 * sbire n'est pas en pile de victoire revient d'elle-meme (« In another game area »).
 */
function elitesDuScenario(campagne, definition, niveau) {
    const coop = definition.cooperation;
    if (!coop || !coop.elites || !coop.cle_elite_annoncee) return null;
    const carnet = campagne.carnet || {};
    const jamais = coop.elites.filter((e) => !carnet[e.cle]);
    const reviennent = coop.elites.filter((e) => carnet[e.cle] === "In another game area");
    if (niveau >= 5) return { elites: [...reviennent, ...jamais], tirage: false };
    const [n, nom] = String(carnet[coop.cle_elite_annoncee] || "").split(":");
    const annoncee = n === String(niveau) ? jamais.find((e) => e.nom === nom) : null;
    if (annoncee) return { elites: [...reviennent, annoncee], tirage: true };
    if (!jamais.length) return { elites: reviennent, tirage: false };
    // Pas encore tiree : on tire, on garde, et l'ecran se redessine.
    const cle = campagne.id + ":" + niveau;
    if (etat.eliteTiree !== cle) {
        etat.eliteTiree = cle;
        const choix = jamais[Math.floor(Math.random() * jamais.length)];
        setTimeout(() => proteger(async () => {
            etat.campagne.carnet = { ...(etat.campagne.carnet || {}), [coop.cle_elite_annoncee]: niveau + ":" + choix.nom };
            etat.campagne = await apiCampagne.enregistrer(etat.campagne);
        }), 0);
    }
    return { elites: reviennent, tirage: false };
}

function blocEliteDuScenario(campagne, definition, niveau, enCours) {
    if (enCours) return null;
    const r = elitesDuScenario(campagne, definition, niveau);
    if (!r || !r.elites.length) return null;
    return el("div", { class: "cmp-elites" },
        el("span", { class: "cmp-elites-t" }, niveau >= 5 ? t("Elites restantes") : r.elites.length > 1 ? t("Elites de ce scénario") : t("Elite de ce scénario")),
        r.elites.map((e) => el("span", { class: "cmp-elite", "data-elite": e.nom, title: e.nom },
            el("img", { src: cardImageUrl(e.sbire), alt: e.nom, loading: "lazy" }),
            el("span", {}, e.nom))));
}

/** Le Marche se visite-t-il deja ? Hunting Season : « Between each scenario »,
 *  donc pas avant le premier (`ouvert_apres_premier`). */
function marcheOuvert(campagne, definition) {
    if (!definition.marche || !definition.marche.ouvert_apres_premier) return true;
    return (campagne.termines || []).length >= 1;
}

/* ------------------------------------------------- reglages de la campagne -- */

/**
 * Les choix que le livret fait faire AU DEBUT de la campagne et que le moteur
 * relit au carnet (Hunting Season : le mode Hunter, le Master Hunter). La boite
 * les declare (`options_campagne`) ; rien n'est en dur ici. Modifiables tant
 * qu'aucun scenario n'est joue, figes ensuite.
 *   type « case »  : carnet[cle] = "1" ou "0" ;
 *   type « siege » : carnet[cle] = numero du heros (1 a 4).
 */
function blocOptionsCampagne(campagne, definition, enCours) {
    const options = (definition.options_campagne || []).filter((o) =>
        !o.expert_seulement || campagne.difficulte === "expert");
    if (!options.length) return null;
    const figees = enCours || (campagne.termines || []).length > 0;
    const equipe = campagne.equipe || [];
    const poser = (cle, valeur) => proteger(async () => {
        etat.campagne.carnet = { ...(etat.campagne.carnet || {}), [cle]: valeur };
        etat.campagne = await apiCampagne.enregistrer(etat.campagne);
    });
    const lignes = options.map((o) => {
        const valeur = (campagne.carnet || {})[o.cle] || "";
        let controle;
        if (o.type === "siege") {
            const choisi = parseInt(valeur, 10) || 1;
            controle = el("div", { class: "cmp-segments" }, equipe.map((m, i) => el("button", {
                class: "cmp-segment" + (choisi === i + 1 ? " sel" : ""),
                disabled: figees || undefined,
                onclick: () => poser(o.cle, String(i + 1)),
            }, m.nomHeros || m.heros || (t("Joueur") + " " + (i + 1)))));
        } else {
            const coche = valeur === "1";
            controle = el("div", { class: "cmp-segments" },
                el("button", { class: "cmp-segment" + (!coche ? " sel" : ""), disabled: figees || undefined,
                    onclick: () => poser(o.cle, "0") }, t("Non")),
                el("button", { class: "cmp-segment" + (coche ? " sel" : ""), disabled: figees || undefined,
                    onclick: () => poser(o.cle, "1") }, t("Oui")));
        }
        return el("div", { class: "cmp-champ" },
            el("label", { class: "cmp-champ-k" }, t(o.libelle || o.cle)),
            controle,
            o.aide ? el("p", { class: "cmp-champ-aide" }, t(o.aide)) : null);
    });
    return el("div", { class: "cmp-bloc" },
        el("h2", { class: "cmp-bloc-t" }, t("Réglages de la campagne")),
        el("p", { class: "cmp-bloc-aide" }, figees
            ? t("Choisis avant le premier scénario : ils ne changent plus.")
            : t("À choisir avant le premier scénario.")),
        lignes);
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
                el("button", { class: "btn ghost", onclick: () => retourVers("campagne") }, t("Retour")),
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
    if (etat.definition.ordre_libre) return vueCampagneLibre();
    const campagne = etat.campagne;
    const definition = etat.definition;
    const index = indexCourant(campagne, definition);
    // Perdue au dernier scenario : elle est finie, elle aussi, et il ne reste
    // rien a lancer. Le drapeau est pose par le panneau de recompenses du
    // plateau, seul endroit qui sache si le livret la donne pour perdue.
    const perdue = Boolean(campagne.perdue);
    const finie = perdue || estTerminee(campagne, definition);
    const scenario = finie ? definition.scenarios[definition.scenarios.length - 1] : definition.scenarios[index];
    // Le fichier du catalogue peut dependre du carnet (Punisher MC×DC : combats 2 et 3) ; sinon c'est l'id de l'etape.
    const duCatalogue = etat.scenarios.find((s) => s.id === scenarioDuCatalogueDeLEtape(scenario, campagne.carnet, campagne.difficulte === "expert"));

    const enCours = campagne.partieEnCours && campagne.partieEnCours.scenario === scenario.id;
    const tentatives = (campagne.tentatives || {})[scenario.id] || 0;

    const barre = el("div", { class: "cmp-barre" },
        el("button", { class: "btn ghost", onclick: () => reculerVers("liste") || proteger(async () => {
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

    const sets = duCatalogue
        ? [...(duCatalogue.rawJson.encounter_sets || []), ...(duCatalogue.rawJson.modular_sets || [])]
        : [];

    // Le livret en double page : debut de campagne, ou epilogue du scenario
    // precedent puis intro et regles de celui-ci (livre-pages.js), et l'onglet
    // des regles de la campagne. Plus rien d'empile sous le bouton Lancer.
    const livre = livreOuvert(definition.code, campagne.id + ":" + scenario.id,
        LP.ongletsLineaires(definition, { index, finie: false, perdue: false, expert: campagne.difficulte === "expert" }));

    const bandeau = el("div", { class: "cmp-bandeau" },
        el("div", { class: "cmp-bloc" },
            el("h2", { class: "cmp-bloc-t" }, t("Ce qui est en jeu")),
            scenario.resume ? el("p", { class: "cmp-bandeau-resume" }, scenario.resume) : null,
            el("p", { class: "cmp-enjeu" }, scenario.enjeu || ""),
        ),
        el("div", { class: "cmp-bloc" },
            el("h2", { class: "cmp-bloc-t" }, t("Mise en place")),
            el("p", { class: "cmp-bloc-aide" }, t("Imposée par le livret : le jeu la met en place pour toi, y compris ce que la campagne a déjà ajouté.")),
            sets.length ? el("ul", { class: "cmp-sets" }, sets.map(ligneSet)) : null,
            blocEliteDuScenario(campagne, definition, scenario.numero, enCours),
        ),
        blocOptionsCampagne(campagne, definition, enCours),
        blocAssemblee(scenario, enCours),
        el("div", { class: "cmp-bloc cmp-bloc-lancer" },
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
            (definition.marche && !enCours && marcheOuvert(campagne, definition)) ? el("button", {
                class: "btn ghost",
                onclick: () => { etat.vue = "marche"; rendre(); },
            }, definition.marche.titre || t("Le Marché")) : null,
            zoneChoisissable(campagne, definition, enCours) ? el("button", {
                class: "btn ghost", "data-vue": "zone",
                onclick: () => { etat.vue = "zone"; rendre(); },
            }, t("Cartes de la zone")) : null,
            definition.cooperation ? el("button", {
                class: "btn ghost",
                onclick: () => { etat.vue = "cooperation"; rendre(); },
            }, enLangue(definition.cooperation.titre, definition.cooperation.titre_en)) : null,
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
        ),
    );

    return el("div", { class: "cmp-page-campagne avec-livre" },
        entete(t("Campagne")),
        barre,
        el("main", { class: "cmp-corps cmp-corps-livre" },
            bandeauErreur(),
            el("div", { class: "cmp-chapo cmp-chapo-ligne" },
                el("span", { class: "cmp-chapo-k" }, t("Scénario") + " " + scenario.numero + " / " + definition.scenarios.length),
                el("h1", { class: "cmp-chapo-nom mvl" }, langueActuelle() === "en" ? scenario.nom : (scenario.nom_fr || scenario.nom)),
            ),
            livre,
            bandeau,
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
    const livre = livreOuvert(definition.code, campagne.id + ":fin", LP.ongletsLineaires(definition, {
        index: definition.scenarios.length, finie: true, perdue, expert: campagne.difficulte === "expert",
    }));
    const totalTentatives = Object.values(campagne.tentatives || {}).reduce((a, b) => a + b, 0);
    const defaite = (dernier.defaite || {});

    return el("section", { class: "cmp-conclusion" + (perdue ? " perdue" : "") },
        el("div", { class: "cmp-chapo" },
            el("span", { class: "cmp-chapo-k" }, perdue ? t("Campagne perdue") : t("Campagne terminée")),
            el("h1", { class: "cmp-chapo-nom mvl" }, campagne.nom),
        ),
        perdue && defaite.texte ? el("p", { class: "cmp-resume" }, defaite.texte) : null,
        livre,
        el("div", { class: "cmp-bilan" },
            ligneBilan(t("Boîte"), nomBoite(definition)),
            ligneBilan(t("Difficulté"), campagne.difficulte === "expert" ? t("Campagne experte") : t("Standard")),
            ligneBilan(t("Équipe"), (campagne.equipe || []).map((m) => m.nomHeros || m.heros).join(", ")),
            ligneBilan(t("Scénarios gagnés"), (campagne.termines || []).length + " / " + definition.scenarios.length),
            totalTentatives ? ligneBilan(t("Parties jouées en tout"), String(totalTentatives)) : null,
        ),
        perdue ? null : blocScoreFinal(campagne, definition),
        el("div", { class: "cmp-actions" },
            el("button", { class: "btn ghost", onclick: () => reculerVers("liste") || proteger(async () => {
                etat.campagne = null; etat.vue = "liste";
                etat.campagnes = await apiCampagne.liste();
            }) }, t("Toutes les campagnes")),
        ),
    );
}

/* ------------------------------------------- vue « campagne en ordre libre » -- */
//
// Fear No Evil (livret mc60 p. 8-9) ne se joue pas dans l'ordre : cinq affaires
// au choix, chacune contre un vilain UNDERLING, et Kingpin quand tout est
// resolu. Avant CHAQUE partie, deux affaires non resolues progressent au
// hasard ; a trois marques une affaire est perdue. Le livret fait tenir ce
// carnet a la main ; ici le tirage est fait par l'ecran, une fois par partie,
// et garde dans `campagne.tirage` tant que la partie n'est pas lancee, pour
// qu'un rechargement de page ne retire pas une seconde fois.
//
// Les regles pures (tirage, vilains, defaite) sont dans ordre-libre.js, et
// eprouvees par tools/tests-lanceur/ordre-libre.test.mjs.
//
// Une defaite n'ouvre pas le panneau du plateau (rien a reporter en standard) :
// c'est le joueur qui la declare ici, comme il cocherait le carnet papier. En
// campagne experte elle fait progresser l'affaire perdue ; contre Kingpin elle
// retourne un environnement Completed cote Failed, ou perd la campagne.

const nomAffaire = (a) => (langueActuelle() === "en" ? a.nom : (a.nom_fr || a.nom));
const nomVilain = (definition, id) => ((definition.vilains || []).find((v) => v.id === id) || { nom: id }).nom;

function vueCampagneLibre() {
    const campagne = etat.campagne;
    const definition = etat.definition;
    const carnet = campagne.carnet || {};
    const final = OL.scenarioFinal(definition);
    const perdue = Boolean(campagne.perdue);
    const finie = perdue || (campagne.termines || []).includes(final.id);
    const resolues = OL.affaires(definition).length - OL.affairesOuvertes(definition, carnet).length;

    const barre = el("div", { class: "cmp-barre" },
        el("button", { class: "btn ghost", onclick: () => reculerVers("liste") || proteger(async () => {
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
                el("span", { class: "cmp-jauge-plein", style: { width: (100 * (resolues + (finie && !perdue ? 1 : 0)) / definition.scenarios.length) + "%" } })),
            el("span", {}, perdue ? t("Campagne perdue")
                : finie ? t("Campagne terminée")
                : (t("Affaires résolues") + " " + resolues + " / " + OL.affaires(definition).length)),
        ),
    );

    if (finie) return el("div", { class: "cmp-page-campagne" }, entete(t("Campagne")), barre,
        el("main", { class: "cmp-corps" }, bandeauErreur(), vueConclusion(campagne, definition, perdue)));

    const enCours = campagne.partieEnCours || null;
    const tirage = campagne.tirage || null;
    const expert = campagne.difficulte === "expert";

    // Le tableau du carnet : une ligne par affaire, ses trois cases, son vilain.
    const tableau = el("section", { class: "cmp-recit" },
        el("div", { class: "cmp-chapo" },
            el("span", { class: "cmp-chapo-k" }, t("Carnet de campagne")),
            el("h1", { class: "cmp-chapo-nom mvl" }, t("Les affaires")),
        ),
        el("p", { class: "cmp-resume" }, definition.resume),
        el("div", { class: "cmp-affaires" }, OL.affaires(definition).map((a) => ligneAffaire(definition, carnet, a, tirage))),
        el("div", { class: "cmp-affaire" + (OL.kingpinDisponible(definition, carnet) ? " ouverte" : " fermee") },
            el("span", { class: "cmp-affaire-nom" }, nomAffaire(final)),
            el("span", { class: "cmp-affaire-etat" }, OL.kingpinDisponible(definition, carnet)
                ? t("Disponible : toutes les affaires sont résolues")
                : t("Quand les cinq affaires seront résolues")),
        ),
    );

    // Les planches de l'affaire en cours de choix (ou de la partie lancee) :
    // la BD du livret puis sa page de regles, comme la vue lineaire les montre.
    const affaireMontree = enCours
        ? definition.scenarios.find((x) => x.id === enCours.scenario)
        : (OL.kingpinDisponible(definition, carnet) && tirage ? final
            : definition.scenarios.find((x) => x.id === etat.affaireChoisie));
    // La planche d'ouverture du livret (Daredevil entend des sirenes partout).
    // Elle vaut pour la campagne, pas pour une affaire : elle vit donc sur la
    // DEFINITION, sous une cle propre a l'ordre libre (la vue lineaire n'a pas
    // d'endroit ou la mettre).
    //
    // ⚠ APRES le tableau des affaires, jamais avant : posee en tete, elle
    // poussait le carnet — la seule chose qu'on vient lire sur cet ecran —
    // sous la ligne de flottaison (vu a la capture, 19/09/2026).
    if (affaireMontree) {
        tableau.append(el("div", { class: "cmp-chapo" },
            el("span", { class: "cmp-chapo-k" }, t("Le livret")),
            el("h1", { class: "cmp-chapo-nom mvl" }, nomAffaire(affaireMontree)),
        ));
    }
    // Planche d'ouverture, pages de l'affaire montree et regles de la campagne,
    // dans le meme livre ouvert que la vue lineaire.
    const livreLibre = livreOuvert(definition.code, campagne.id + ":" + (affaireMontree ? affaireMontree.id : "ouverture"),
        LP.ongletsLibres(definition, { affaire: affaireMontree, expert }));
    if (livreLibre) tableau.append(livreLibre);

    let action;
    if (enCours) action = blocPartieEnCours(campagne, definition, enCours, expert);
    else if (tirage) action = blocChoixDuScenario(campagne, definition, carnet, tirage);
    else action = blocAvantLaPartie(campagne, definition, carnet);

    const colonneMission = el("aside", { class: "cmp-mission" },
        action,
        el("div", { class: "cmp-bloc" },
            el("h2", { class: "cmp-bloc-t" }, t("Mise en place")),
            el("p", { class: "cmp-bloc-aide" }, t("Imposée par le livret : le jeu la met en place pour toi, y compris ce que la campagne a déjà ajouté.")),
            el("p", { class: "cmp-bloc-aide" }, (definition.expert || {}).note && expert ? definition.expert.note : ""),
        ),
        enCours ? null : el("div", { class: "cmp-lancer" },
            el("button", {
                class: "btn ghost",
                onclick: () => {
                    ecrireBrouillon({
                        modifie: etat.campagne.id,
                        code: definition.code,
                        nom: etat.campagne.nom,
                        difficulte: etat.campagne.difficulte,
                        nbJoueurs: (etat.campagne.equipe || []).length || 1,
                        identites: (etat.campagne.equipe || []).map((m) => m.nomHeros || m.heros),
                        equipeActuelle: etat.campagne.equipe || [],
                    });
                    window.location.href = "/prepare.html?campagne";
                },
            }, t("Modifier les decks")),
        ),
    );

    return el("div", { class: "cmp-page-campagne" },
        entete(t("Campagne")),
        barre,
        el("main", { class: "cmp-corps cmp-corps-scenario" },
            bandeauErreur(),
            el("div", { class: "cmp-duo" }, tableau, colonneMission),
        ),
    );
}

function ligneAffaire(definition, carnet, affaire, tirage) {
    const etatA = OL.etatAffaire(carnet, affaire.id);
    const n = OL.marques(carnet, affaire.id);
    const vilain = OL.vilainDe(carnet, affaire.id);
    const tiree = tirage && (tirage.tirees || []).includes(affaire.id);
    const cases = el("span", { class: "cmp-affaire-cases" },
        [0, 1, 2].map((i) => el("span", { class: "cmp-affaire-case" + (i < n ? " cochee" : "") }, i < n ? "✕" : "")));
    return el("div", { class: "cmp-affaire " + etatA + (tiree ? " tiree" : "") },
        el("span", { class: "cmp-affaire-nom" }, nomAffaire(affaire)),
        cases,
        el("span", { class: "cmp-affaire-etat" },
            etatA === "completed" ? t("Complétée")
                : etatA === "failed" ? t("Échouée")
                : tiree ? t("Vient de progresser") : t("En cours")),
        el("span", { class: "cmp-affaire-vilain" }, vilain ? nomVilain(definition, vilain) : ""),
    );
}

/** Étapes 1 à 3 : le tirage, une fois par partie. */
function blocAvantLaPartie(campagne, definition, carnet) {
    const ouvertes = OL.affairesOuvertes(definition, carnet);
    return el("div", { class: "cmp-bloc" },
        el("h2", { class: "cmp-bloc-t" }, t("Avant la partie")),
        el("p", { class: "cmp-bloc-aide" }, ouvertes.length
            ? t("Deux affaires non résolues sont tirées au hasard et progressent d'une marque (s'il n'en reste qu'une, elle en prend deux). À trois marques, l'affaire est perdue.")
            : t("Toutes les affaires sont résolues : il ne reste que Kingpin.")),
        el("div", { class: "cmp-lancer" },
            el("button", { class: "btn launch", onclick: () => proteger(async () => {
                const resultat = OL.tirerLaProgression(definition, campagne.carnet || {});
                campagne.carnet = resultat.carnet;
                campagne.tirage = { tirees: resultat.tirees, echouees: resultat.echouees, depuis: new Date().toISOString() };
                etat.campagne = await apiCampagne.enregistrer(campagne);
            }) }, ouvertes.length ? t("Tirer la progression") : t("Préparer la partie finale")),
        ),
    );
}

/** Étapes 4 et 5 : le choix de l'affaire puis du vilain, et le lancement. */
function blocChoixDuScenario(campagne, definition, carnet, tirage) {
    const ouvertes = OL.affairesOuvertes(definition, carnet);
    const final = OL.scenarioFinal(definition);
    const kingpin = OL.kingpinDisponible(definition, carnet);
    const compteRendu = el("p", { class: "cmp-bloc-aide" },
        (tirage.tirees || []).length
            ? t("Tirage :") + " " + tirage.tirees.map((id) => nomAffaire(definition.scenarios.find((s) => s.id === id))).join(", ")
                + ((tirage.echouees || []).length ? " · " + t("Échouée à trois marques :") + " "
                    + tirage.echouees.map((id) => nomAffaire(definition.scenarios.find((s) => s.id === id))).join(", ") : "")
            : t("Rien à tirer."));

    if (kingpin) {
        const tentatives = (campagne.tentatives || {})[final.id] || 0;
        return el("div", { class: "cmp-bloc" },
            el("h2", { class: "cmp-bloc-t" }, nomAffaire(final)),
            compteRendu,
            el("p", { class: "cmp-enjeu" }, final.enjeu || ""),
            el("div", { class: "cmp-lancer" },
                tentatives ? el("p", { class: "cmp-tentatives" }, tentatives + " " + t("tentatives déjà jouées sur ce scénario.")) : null,
                el("button", { class: "btn launch", onclick: () => proteger(async () => {
                    campagne.tirage = null;
                    await lancerScenario(final, { catalogue: OL.scenarioDuCatalogue(final, null) });
                }) }, t("Lancer le scénario")),
            ),
        );
    }

    const choisie = ouvertes.find((a) => a.id === etat.affaireChoisie) || null;
    if (!choisie) {
        return el("div", { class: "cmp-bloc" },
            el("h2", { class: "cmp-bloc-t" }, t("Choisir une affaire")),
            compteRendu,
            el("div", { class: "cmp-lancer" }, ouvertes.map((a) => el("button", {
                class: "btn ghost",
                onclick: () => { etat.affaireChoisie = a.id; etat.vilainChoisi = null; rendre(); },
            }, nomAffaire(a) + (OL.marques(carnet, a.id) ? " (" + OL.marques(carnet, a.id) + " / 3)" : "")))),
        );
    }

    const vilains = OL.vilainsPossibles(definition, carnet, choisie.id);
    const vilain = vilains.impose || (vilains.choix.includes(etat.vilainChoisi) ? etat.vilainChoisi : vilains.suggere);
    const tentatives = (campagne.tentatives || {})[choisie.id] || 0;
    return el("div", { class: "cmp-bloc" },
        el("h2", { class: "cmp-bloc-t" }, nomAffaire(choisie)),
        el("p", { class: "cmp-enjeu" }, choisie.enjeu || ""),
        el("p", { class: "cmp-bloc-aide" }, vilains.impose
            ? t("Le vilain de cette affaire est déjà inscrit au carnet :") + " " + nomVilain(definition, vilains.impose)
            : t("Le vilain : l'ordre recommandé du livret propose le premier qui n'est pas encore inscrit au carnet.")),
        vilains.impose ? null : el("div", { class: "cmp-lancer" }, vilains.choix.map((id) => el("button", {
            class: "btn " + (id === vilain ? "launch" : "ghost"),
            onclick: () => { etat.vilainChoisi = id; rendre(); },
        }, nomVilain(definition, id) + (id === vilains.suggere ? " · " + t("recommandé") : "")))),
        // Les portraits du livret (p. 6-7) : ce qu'il faut savoir de chaque
        // sous-fifre avant de le choisir. Repliees par defaut : la colonne est
        // etroite, et on ne les relit pas a chaque partie.
        vilains.impose ? null : el("details", { class: "cmp-vilains" },
            el("summary", {}, t("Qui sont les sous-fifres ?")),
            ...(definition.pages_vilains || []).map((f) => pageLivret(definition.code, f, "cmp-page-regles")),
        ),
        el("div", { class: "cmp-lancer" },
            tentatives ? el("p", { class: "cmp-tentatives" },
                tentatives === 1 ? t("Une tentative déjà jouée sur ce scénario.")
                    : (tentatives + " " + t("tentatives déjà jouées sur ce scénario."))) : null,
            el("button", { class: "btn launch", onclick: () => proteger(async () => {
                campagne.carnet = OL.inscrireLeVilain(campagne.carnet || {}, choisie.id, vilain);
                campagne.tirage = null;
                etat.affaireChoisie = null;
                await lancerScenario(choisie, { catalogue: OL.scenarioDuCatalogue(choisie, vilain), vilain });
            }) }, t("Lancer le scénario") + " · " + nomVilain(definition, vilain)),
            el("button", { class: "btn ghost", onclick: () => { etat.affaireChoisie = null; rendre(); } }, t("Changer d'affaire")),
        ),
    );
}

/** Une partie lancée : reprendre, abandonner, ou déclarer la défaite. */
function blocPartieEnCours(campagne, definition, enCours, expert) {
    const scenario = definition.scenarios.find((s) => s.id === enCours.scenario) || { nom: enCours.scenario };
    const aChoisir = etat.retournement || [];
    return el("div", { class: "cmp-bloc" },
        el("h2", { class: "cmp-bloc-t" }, nomAffaire(scenario) + (enCours.vilain ? " · " + nomVilain(definition, enCours.vilain) : "")),
        el("div", { class: "cmp-lancer" },
            el("a", { class: "btn launch", href: "/app/board.html" }, t("Reprendre le scénario en cours")),
            aChoisir.length
                ? el("div", { class: "cmp-lancer" },
                    el("p", { class: "cmp-bloc-aide" }, t("Campagne experte : choisis l'environnement Complété à retourner côté Échoué, puis rejoue Kingpin.")),
                    aChoisir.map((id) => el("button", { class: "btn ghost", onclick: () => proteger(() => enregistrerLaDefaite(campagne, definition, enCours.scenario, expert, id)) },
                        nomAffaire(definition.scenarios.find((s) => s.id === id)))))
                : el("button", {
                    class: "btn ghost",
                    onclick: () => {
                        if (!window.confirm(t("Déclarer la partie perdue ? Le livret l'inscrit au carnet : en campagne experte, l'affaire progresse d'une marque."))) return;
                        proteger(() => enregistrerLaDefaite(campagne, definition, enCours.scenario, expert, null));
                    },
                }, t("La partie est perdue")),
            el("button", {
                class: "btn ghost",
                onclick: () => {
                    if (!window.confirm(t("Abandonner la partie en cours et refaire ce scénario depuis le début ?"))) return;
                    proteger(async () => {
                        etat.retournement = null;
                        etat.campagne.partieEnCours = null;
                        etat.campagne = await apiCampagne.enregistrer(etat.campagne);
                    });
                },
            }, t("Abandonner et recommencer")),
        ),
    );
}

async function enregistrerLaDefaite(campagne, definition, scenarioId, expert, retournee) {
    const resultat = OL.appliquerLaDefaite(definition, campagne.carnet || {}, scenarioId, expert, retournee);
    if (resultat.aChoisir.length) { etat.retournement = resultat.aChoisir; rendre(); return; }
    etat.retournement = null;
    campagne.carnet = resultat.carnet;
    campagne.partieEnCours = null;
    if (resultat.perdue) campagne.perdue = true;
    etat.campagne = await apiCampagne.enregistrer(campagne);
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

/** Un set de la mise en place, sous le NOM de son fichier (`name`) : l'identifiant
 *  d'un set fan-made porte un prefixe (« hs_feral_instincts »). Le titre deduit
 *  de l'identifiant s'affiche le temps de la lecture, et reste si elle echoue.
 *
 *  ⚠ UN SEUL REESSAI, APRES UN COURT DELAI (21/10/2026, item 18 du backlog) :
 *  au tout premier chargement, cet appel peut partir avant que le cookie
 *  `app_version` (pose par un `get_version` qui tourne en parallele) ne soit
 *  ecrit — le serveur repond alors sa page « Version Mismatch » a la place du
 *  JSON attendu, `res.json()` leve une exception, et sans reessai le nom
 *  recherche n'etait JAMAIS affiche pour le reste de cette visite (identifiant
 *  brut mis en forme a la place, « Hs Feral Instincts »). Le cookie est pose
 *  bien avant 400 ms dans tous les cas observes : un seul reessai suffit. */
const _nomsSets = new Map();
function ligneSet(id) {
    const li = el("li", {}, _nomsSets.get(id) || titreSet(id));
    if (!_nomsSets.has(id)) {
        const appliquer = (json) => {
            if (!json || !json.name) return;
            _nomsSets.set(id, json.name);
            li.textContent = json.name;
        };
        api.encounterSet(id)
            .then(appliquer)
            .catch(() => {
                setTimeout(() => {
                    api.encounterSet(id).then(appliquer).catch(() => undefined);
                }, 400);
            });
    }
    return li;
}

/* --------------------------------------------------------------- actions -- */

async function ouvrirCampagne(id) {
    const campagne = await apiCampagne.charger(id);
    const definition = await apiCampagne.definition(campagne.code);
    await cards.load();
    const scenarios = await catalog.scenariosForExtension(definition.cle_extension, { campagne: true });
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
async function lancerScenario(scenario, options = {}) {
    const campagne = etat.campagne;
    const choixAssemblee = scenario.assemblee ? etat.assembleeChoix : null;
    if (choixAssemblee && choixAssemblee.mode === "rejoindre" && !String(choixAssemblee.code || "").trim()) {
        throw new Error(t("Saisis le code de l'assemblée à rejoindre."));
    }
    // En ordre libre, le fichier du catalogue depend du vilain choisi
    // (`<affaire>_<vilain>`) ou d'un id de catalogue propre au final : l'id de
    // la definition reste celui que le plateau et l'estampille du moteur
    // connaissent, seul le fichier lance change.
    const idCatalogue = options.catalogue
        || scenarioDuCatalogueDeLEtape(scenario, campagne.carnet, campagne.difficulte === "expert");
    const duCatalogue = etat.scenarios.find((s) => s.id === idCatalogue);
    if (!duCatalogue) throw new Error(t("Scénario introuvable dans le catalogue :") + " " + idCatalogue);

    const joueurs = (campagne.equipe || []).map((m) => ({
        deck: m.deck,
        hero: { name: m.nomHeros || m.heros },
        identity: m.identite ? { hero: m.identite } : null,
    }));

    // Meme verification qu'au lancement normal (prepare/app.js) : un deck
    // invalide ne doit jamais partir en silence, meme depuis une campagne.
    const verif = validate({
        playerCount: joueurs.length,
        players: joueurs,
        scenario: duCatalogue,
        difficulty: { selectedModularSets: duCatalogue.rawJson.modular_sets || [] },
    });
    if (!verif.ok) {
        throw new Error(verif.errors.map((e) => e.message).join(" — "));
    }

    // La partie est rattachee a la campagne AVANT de partir : si le joueur
    // ferme l'onglet en plein scenario, on saura le lui proposer en reprise.
    campagne.partieEnCours = { scenario: scenario.id, depuis: new Date().toISOString(), ...(options.vilain ? { vilain: options.vilain } : {}) };
    campagne.tentatives = campagne.tentatives || {};
    campagne.tentatives[scenario.id] = (campagne.tentatives[scenario.id] || 0) + 1;
    etat.campagne = await apiCampagne.enregistrer(campagne);

    // SI le plateau joue une campagne, c'est la regle `mode_campaign` du monde
    // qui le dit (posee par launch() ci-dessous). LAQUELLE : on le lui dit ici,
    // et c'est le panneau de recompenses qui effacera la cle une fois le
    // scenario reporte au carnet (voir ui-app/src/board/campagne/contexte.ts).
    try {
        window.localStorage.setItem("mc-campagne-partie",
            JSON.stringify({ id: etat.campagne.id, scenario: scenario.id }));
    } catch (e) { /* stockage indisponible : le scenario se joue, sans report */ }

    // Plusieurs heros : l'hote ne part PAS directement sur le plateau, il passe
    // d'abord par l'ecran d'invitation (vueInvitation) pour donner les liens de
    // siege a son equipe. Seul (1 heros), rien a inviter : comportement inchange.
    const enLigne = joueurs.length > 1;
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
        // Kingsfall multi-tables : « creer » une assemblee ou en « rejoindre » une avec son code (jamais pour les autres scenarios).
        assemblee: scenario.assemblee && etat.assembleeChoix && etat.assembleeChoix.mode !== "seule" ? { ...etat.assembleeChoix } : null,
    }, { redirect: !enLigne });

    if (enLigne) {
        etat.invitation = { joueurs, cles: null, erreur: "", copie: -1 };
        etat.vue = "invitation";
        chargerLiensInvitationCampagne();
    }
}

/* ------------------------------------------------------- invitation en ligne -- */

/** Les cles de siege pour CETTE partie de campagne, juste lancee (`/new` deja
 *  envoye par `lancerScenario` ci-dessus) : jamais `get_liens_sieges` (voir son
 *  avertissement, 07/10/2026), toujours la jumelle `get_liens_sieges_campagne`,
 *  qui ne marque pas la table comme « ordinaire ». */
async function chargerLiensInvitationCampagne() {
    const inv = etat.invitation;
    if (!inv) return;
    try {
        const res = await fetch("get_liens_sieges_campagne?");
        const brut = await res.json();
        if (!res.ok || !brut.multi || !Array.isArray(brut.cles)) {
            throw new Error(brut.error || "indisponible");
        }
        inv.cles = brut.cles;
    } catch (e) {
        inv.erreur = t("Impossible de récupérer les liens d'invitation.");
    }
    rendre();
}

/** Meme forme de lien que l'assistant de partie ordinaire (`lienDuSiege`,
 *  public/js/prepare/app.js) : `to=salon` envoie l'invite choisir... rien, en
 *  campagne — juste confirmer son siege, l'equipe est deja fixee. */
function lienDeSiegeCampagne(p, cle) {
    return location.origin + "/claim_seat?p=" + p + "&key=" + encodeURIComponent(cle || "") + "&to=salon";
}

function ligneInvitationSiege(p, joueur, cle) {
    const inv = etat.invitation;
    const url = lienDeSiegeCampagne(p, cle);
    return el("div", { class: "liens-ligne" },
        el("span", { class: "liens-qui" }, (joueur.hero && joueur.hero.name) || (t("Joueur") + " " + (p + 1))),
        el("button", {
            class: "liens-copier" + (inv.copie === p ? " ok" : ""),
            title: url,
            onclick: async () => {
                try { await navigator.clipboard.writeText(url); inv.copie = p; }
                catch (e) { inv.copie = -1; window.prompt(t("Copie ce lien :"), url); }
                rendre();
            },
        }, inv.copie === p ? t("Copié") : t("Copier le lien")),
    );
}

function vueInvitation() {
    const inv = etat.invitation;
    const [hote, ...equipe] = inv.joueurs;
    return el("div", { class: "cmp-page-invitation" },
        entete(t("Inviter l'équipe")),
        el("main", { class: "cmp-corps" },
            el("div", { class: "cmp-titre-rangee" },
                el("h1", { class: "cmp-titre mvl" }, t("Inviter l'équipe")),
            ),
            el("p", { class: "cmp-note" },
                t("La partie est lancée. Envoie un lien à chaque coéquipier : son héros est déjà celui fixé par la campagne, il n'a rien à choisir.")),
            inv.erreur ? el("p", { class: "cmp-erreur" }, inv.erreur) : null,
            !inv.erreur && !inv.cles ? el("p", {}, t("Préparation des liens…")) : null,
            inv.cles ? el("div", { class: "liens-invites" },
                ...equipe.map((joueur, i) => ligneInvitationSiege(i + 1, joueur, inv.cles[i + 1])),
            ) : null,
            el("div", { class: "cmp-actions" },
                el("button", {
                    class: "btn launch",
                    onclick: () => { window.location.href = URL_PLATEAU; },
                }, t("Rejoindre le plateau")),
            ),
        ),
    );
}

/**
 * KINGSFALL MULTI-TABLES (22/10/2026) : jouer le combat 4 seul, ou en ASSEMBLEE avec d'autres tables. Decision de l'utilisateur : un CODE d'assemblee partage.
 * La premiere table en CREE une (elle devient l'organisatrice et recoit le code a donner), les autres en REJOIGNENT une en saisissant ce code.
 * Le scenario l'annonce par `assemblee: true` dans `data/campagnes/<code>.json`.
 */
function blocAssemblee(scenario, enCours) {
    if (!scenario.assemblee || enCours) return null;
    const choix = etat.assembleeChoix || (etat.assembleeChoix = { mode: "seule", code: "" });
    const modes = [
        ["seule", t("Une seule table")],
        ["creer", t("Créer une assemblée")],
        ["rejoindre", t("Rejoindre une assemblée")],
    ];
    const champ = el("input", {
        type: "text", id: "cmp-assemblee-code", class: "cmp-assemblee-code", maxlength: "16", autocomplete: "off", spellcheck: "false",
        placeholder: "KING-XXXX", value: choix.code || "", "aria-label": t("Code de l'assemblée"),
        oninput: (e) => { choix.code = e.target.value.toUpperCase(); },
    });
    return el("div", { class: "cmp-bloc cmp-bloc-assemblee" },
        el("h2", { class: "cmp-bloc-t" }, t("Combat à plusieurs tables")),
        el("p", { class: "cmp-bloc-aide" }, t("La Chute du Roi se joue seul, ou en assemblée de 2 à 4 groupes qui s'entraident entre tables.")),
        el("div", { class: "cmp-segments", role: "group", "aria-label": t("Combat à plusieurs tables") },
            modes.map(([mode, libelle]) => el("button", {
                class: "cmp-segment" + (choix.mode === mode ? " sel" : ""), type: "button", "aria-pressed": String(choix.mode === mode),
                onclick: () => { choix.mode = mode; rendre(); },
            }, libelle))),
        choix.mode === "creer" ? el("p", { class: "cmp-bloc-aide" }, t("Tu recevras un code à donner aux autres groupes, dans l'onglet Assemblée du plateau.")) : null,
        choix.mode === "rejoindre" ? el("label", { class: "cmp-assemblee-saisie", for: "cmp-assemblee-code" },
            el("span", {}, t("Code de l'assemblée")), champ) : null,
    );
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

/* ------------------------------------------- Retour Android = vue precedente --
   Zone 2 de la refonte telephone : chaque vue (liste, creation, campagne,
   marche, enquete) est une entree d'historique au telephone. Les boutons
   « Retour » de l'interface reculent dans l'historique quand la vue visee est
   juste derriere : la pile reste propre (meme principe que l'assistant). */
const VUES_DE_CAMPAGNE = ["campagne", "marche", "enquete", "cooperation", "zone"];

function retourVers(vue) {
    if (reculerVers(vue)) return;
    etat.vue = vue;
    rendre();
}

installerHistorique((cle) => {
    if (cle === "liste" || (VUES_DE_CAMPAGNE.includes(cle) && !etat.campagne)) {
        if (etat.vue === "liste") return;
        // La liste s'affiche tout de suite (celle qu'on a), puis se rafraichit
        // sans verrouiller l'ecran : un toucher pendant le rechargement compte.
        etat.vue = "liste";
        etat.campagne = null;
        rendre();
        apiCampagne.liste().then((liste) => {
            etat.campagnes = liste;
            if (etat.vue === "liste") rendre();
        }).catch(() => undefined);
        return;
    }
    etat.vue = cle;
    rendre();
});
suivreTel(() => rendre());

function rendre() {
    if (etat.vue === "invitation" && etat.invitation) root.replaceChildren(vueInvitation());
    else if (etat.vue === "marche" && etat.campagne && etat.definition && etat.definition.marche)
        root.replaceChildren(vueMarche(etat.campagne, etat.definition));
    else if (etat.vue === "zone" && etat.campagne && etat.definition && zoneChoisissable(etat.campagne, etat.definition, false))
        root.replaceChildren(vueChoixDeLaZone(etat.campagne, etat.definition));
    else if (etat.vue === "cooperation" && etat.campagne && etat.definition && etat.definition.cooperation)
        root.replaceChildren(vueCooperation(etat.campagne, etat.definition));
    else if (etat.vue === "enquete" && etat.campagne && etat.definition && etat.definition.enquete)
        root.replaceChildren(vueEnquete(etat.campagne, etat.definition));
    else if (etat.vue === "campagne" && etat.campagne && etat.definition) root.replaceChildren(vueCampagne());
    else if (etat.vue === "creation") root.replaceChildren(vueCreation());
    else root.replaceChildren(vueListe());
    // Apres CHAQUE rendu : replaceChildren remet des noeuds neufs, un passage
    // unique au chargement ne tiendrait pas.
    corrigerTextesMarvel();
    noterEcran(etat.vue);
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
