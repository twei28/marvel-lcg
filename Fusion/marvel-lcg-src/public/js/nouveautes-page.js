// nouveautes-page.js — la page des mises à jour (17/10/2026).
//
// Remplace la modale de l'accueil sur PC : les nouveautés y étaient en une
// longue liste à faire défiler. Ici, une rangée par famille (Roster, Jeu,
// Correction, Coulisses) : à gauche la famille, à droite ses trois dernières
// mises à jour. Un clic sur la rangée ouvre TOUTES les mises à jour de la
// famille. La famille ouverte est dans l'adresse (#heros), donc « précédent »
// ramène à la vue d'ensemble.
"use strict";

import { GENRES, nouveautesTriees } from "/public/js/prepare/nouveautes.js";
import { t, langueActuelle, synchroniserLangueServeur, boutonLangue } from "/public/js/prepare/langue.js";
import { urlNarval } from "/public/js/prepare/narval.js";

const racine = document.getElementById("app");

function el(tag, props, ...kids) {
    const n = document.createElement(tag);
    if (props) for (const k in props) {
        const v = props[k];
        if (v == null || v === false) continue;
        if (k === "class") n.className = v;
        else if (k.startsWith("on") && typeof v === "function") n.addEventListener(k.slice(2).toLowerCase(), v);
        else n.setAttribute(k, v === true ? "" : v);
    }
    for (const kid of kids.flat()) {
        if (kid == null || kid === false) continue;
        n.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
    }
    return n;
}

const anglais = () => langueActuelle() === "en";
const nomGenre = (cle) => (anglais() ? GENRES[cle].en : GENRES[cle].fr);
const texte = (e) => (anglais() ? e.en : e.fr);

/** « 16 oct. 2026 » : on reconstruit la date à la main, en heure locale (un
 *  `new Date("AAAA-MM-JJ")` serait en UTC et reculerait d'un jour). */
function dateCourte(iso) {
    const [an, mois, jour] = String(iso).split("-").map(Number);
    if (!an || !mois || !jour) return String(iso);
    return new Date(an, mois - 1, jour).toLocaleDateString(anglais() ? "en-GB" : "fr-FR",
        { day: "numeric", month: "short", year: "numeric" });
}

const familles = () => {
    const toutes = nouveautesTriees();
    return Object.keys(GENRES).map((cle) => ({ cle, lot: toutes.filter((e) => e.genre === cle) }))
        .filter((f) => f.lot.length);
};

function entete(retourVersAccueil) {
    document.title = t("Mises à jour") + " — Marvel Champions";
    return el("header", { class: "nv-entete" },
        el("a", { class: "nv-marque", href: retourVersAccueil ? "/prepare.html" : "#" ,
                  onclick: retourVersAccueil ? null : (ev) => { ev.preventDefault(); location.hash = ""; } },
            el("span", { class: "nv-retour" }, "<"),
            el("img", { class: "nv-narval", src: urlNarval(), alt: "NarwhalChampions" }),
            el("span", { class: "nv-sous" }, t("Mises à jour")),
        ),
        boutonLangue("btn ghost nv-langue"),
    );
}

function ligne(e, avecGenre) {
    return el("li", { class: "nv-ligne" },
        el("span", { class: "nv-date" }, dateCourte(e.date)),
        avecGenre ? el("span", { class: "nv-etiquette " + e.genre }, nomGenre(e.genre)) : null,
        el("span", { class: "nv-texte" }, texte(e)),
    );
}

function vueEnsemble() {
    const rangees = familles().map(({ cle, lot }) =>
        el("a", { class: "nv-rangee " + cle, href: "#" + cle,
                  "aria-label": nomGenre(cle) + " — " + t("Tout voir") },
            el("span", { class: "nv-famille" },
                el("b", { class: "nv-famille-nom" }, nomGenre(cle)),
                el("span", { class: "nv-compte" }, lot.length + " " + (lot.length > 1 ? t("mises à jour") : t("mise à jour"))),
                el("span", { class: "nv-voir" }, t("Tout voir") + " ›"),
            ),
            el("ul", { class: "nv-derniers" }, lot.slice(0, 3).map((e) => ligne(e, false))),
        ));
    return el("div", { class: "nv-page" },
        entete(true),
        el("main", { class: "nv-corps" },
            el("h1", { class: "nv-titre" }, t("Mises à jour")),
            el("p", { class: "nv-aide" }, t("Les trois dernières de chaque famille. Touche une famille pour tout voir.")),
            el("div", { class: "nv-rangees" }, rangees),
        ),
    );
}

function vueFamille(cle) {
    const liste = familles();
    const lot = (liste.find((f) => f.cle === cle) || { lot: [] }).lot;
    return el("div", { class: "nv-page" },
        entete(false),
        el("main", { class: "nv-corps nv-detail" },
            el("nav", { class: "nv-onglets", "aria-label": t("Familles") },
                liste.map((f) => el("a", { class: "nv-onglet " + f.cle + (f.cle === cle ? " actif" : ""), href: "#" + f.cle },
                    nomGenre(f.cle), el("span", { class: "nv-compte" }, String(f.lot.length))))),
            el("section", { class: "nv-liste " + cle },
                el("h1", { class: "nv-titre" }, nomGenre(cle)),
                el("ul", { class: "nv-toutes" }, lot.map((e) => ligne(e, false))),
            ),
        ),
    );
}

function dessiner() {
    const cle = decodeURIComponent(location.hash.replace(/^#/, ""));
    racine.replaceChildren(GENRES[cle] ? vueFamille(cle) : vueEnsemble());
    window.scrollTo(0, 0);
}

addEventListener("hashchange", dessiner);
synchroniserLangueServeur();
dessiner();
