// section-createurs.js — le volet « Créateurs de contenu fan-made » (26/10/2026).
//
// Posé sous les remerciements de l'accueil (prepare/app.js, blocRemerciements) et
// dans public/credits.html. La liste vient de `creditsParCreateur` : elle se lit
// sur le champ `custom` des cartes, jamais à la main. Elle ne se charge qu'à
// l'ouverture du volet (cards.json est lourd, l'accueil n'en a pas besoin pour
// s'afficher).
"use strict";

import { creditsParCreateur } from "./createurs-fanmade.js";

if (typeof document !== "undefined" && !document.getElementById("style-createurs-fanmade")) {
    const style = document.createElement("style");
    style.id = "style-createurs-fanmade";
    style.textContent = `
      .createurs-volet { margin: 8px auto; max-width: 46rem; text-align: left; }
      .createurs-volet > summary { cursor: pointer; text-align: center; font-weight: 600; }
      .createurs-volet ul.createurs-fanmade { margin: 8px 0 0; padding-left: 1.2em; font-size: 12px; line-height: 1.5; }
      .createurs-volet li { margin: 2px 0; overflow-wrap: anywhere; }
    `;
    document.head.appendChild(style);
}

let _brut = null;
/** cards.json tel que le sert le moteur : { pack: [cartes] }. Un seul chargement. */
export function chargerCartesBrutes() {
    if (!_brut) {
        _brut = fetch("/get_cards_json?")
            .then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
            .catch((err) => { _brut = null; throw err; });
    }
    return _brut;
}

/** Remplit `conteneur` avec la liste des créateurs : un `<li>` par créateur, son nom
 *  en gras puis ses contenus. `t` : la traduction du site, `el` : le fabricant d'éléments. */
export function remplirListeCreateurs(conteneur, credits, { t, el }) {
    if (!credits.length) {
        conteneur.replaceChildren(el("p", {}, t("Aucun créateur fan-made trouvé.")));
        return;
    }
    conteneur.replaceChildren(
        el("ul", { class: "createurs-fanmade" },
            ...credits.map((c) => el("li", {}, el("b", {}, c.createur), " : " + c.contenus.join(", ")))),
    );
}

/** Le volet repliable de l'accueil. Chargement à la première ouverture. */
export function voletCreateurs({ t, el }) {
    const corps = el("div", { class: "createurs-corps" });
    const volet = el("details", { class: "createurs-volet" },
        el("summary", {}, t("Créateurs de contenu fan-made")),
        corps,
    );
    let demande = false;
    volet.addEventListener("toggle", () => {
        if (!volet.open || demande) return;
        demande = true;
        corps.replaceChildren(el("p", {}, t("Chargement…")));
        chargerCartesBrutes()
            .then((brut) => remplirListeCreateurs(corps, creditsParCreateur(brut), { t, el }))
            .catch(() => {
                demande = false;
                corps.replaceChildren(el("p", {}, t("La liste des créateurs est indisponible pour le moment.")));
            });
    });
    return volet;
}
