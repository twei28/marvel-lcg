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
      .createurs-bouton { display: block; margin: 8px auto 0; cursor: pointer; }
      .createurs-fanmade { margin: 0; padding-left: 1.2em; font-size: 12px; line-height: 1.5; max-height: 60vh; overflow-y: auto; }
      .createurs-fanmade li { margin: 2px 0; overflow-wrap: anywhere; }
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

/** Le bouton de l'accueil qui ouvre la liste dans une modale (27/10/2026,
 *  remplace l'ancien `<details>` repliable : son contenu dépliait EN PLACE,
 *  par-dessus le reste de l'accueil (logo compris) — moche, signalé par
 *  l'utilisateur. Même modale que le reste du site (`.deck-modal`,
 *  `ouvrirModale`/`fermerModale` de prepare/app.js), fermable par la croix,
 *  un clic dehors, ou la poignée sur téléphone. Chargement à la première
 *  ouverture seulement (chargerCartesBrutes est déjà mémoïsée). */
export function voletCreateurs({ t, el, ouvrirModale, fermerModale }) {
    return el("button", { class: "tampon createurs-bouton", onclick: () => ouvrirModaleCreateurs({ t, el, ouvrirModale, fermerModale }) },
        t("Créateurs de contenu fan-made"));
}

export function ouvrirModaleCreateurs({ t, el, ouvrirModale, fermerModale }) {
    const corps = el("div", {}, el("p", {}, t("Chargement…")));
    const overlay = el("div", { class: "deck-modal", onclick: (e) => { if (e.target === overlay) fermerModale(overlay); } },
        el("div", { class: "deck-modal-panel" },
            el("div", { class: "dm-head" },
                el("b", { class: "mvl" }, t("Créateurs de contenu fan-made")),
                el("button", { class: "dm-close", onclick: () => fermerModale(overlay) }, "✕"),
            ),
            corps,
        ),
    );
    ouvrirModale(overlay);
    chargerCartesBrutes()
        .then((brut) => remplirListeCreateurs(corps, creditsParCreateur(brut), { t, el }))
        .catch(() => corps.replaceChildren(el("p", {}, t("La liste des créateurs est indisponible pour le moment."))));
}
