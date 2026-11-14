// credits-createurs.js — la section « Créateurs de contenu fan-made » de
// public/credits.html (26/10/2026). La liste est GÉNÉRÉE à partir du champ
// `custom` des cartes (voir prepare/createurs-fanmade.js), jamais tapée à la main.
"use strict";

import { t } from "/public/js/prepare/langue.js";
import { creditsParCreateur } from "/public/js/prepare/createurs-fanmade.js";
import { chargerCartesBrutes, remplirListeCreateurs } from "/public/js/prepare/section-createurs.js";

function el(balise, attributs, ...enfants) {
    const noeud = document.createElement(balise);
    for (const [k, v] of Object.entries(attributs || {})) noeud.setAttribute(k, v);
    for (const e of enfants) noeud.append(e);
    return noeud;
}

const cible = document.querySelector("[data-createurs-fanmade]");
if (cible) {
    cible.replaceChildren(
        el("h3", {}, t("Créateurs de contenu fan-made")),
        el("p", {}, t("Les héros, campagnes et cartes fan-made de ce jeu sont l'œuvre de ces créateurs. Merci à eux !")),
    );
    const liste = el("div", {}, el("p", {}, t("Chargement…")));
    cible.append(liste);
    chargerCartesBrutes()
        .then((brut) => remplirListeCreateurs(liste, creditsParCreateur(brut), { t, el }))
        .catch(() => liste.replaceChildren(el("p", {}, t("La liste des créateurs est indisponible pour le moment."))));
    cible.append(el("p", {},
        t("Si j'ai oublié de te créditer pour une image, une carte ou un contenu, j'en suis désolé : dis-le-moi via"), " ",
        (() => { const a = el("a", { href: "https://narwhalchampions.com/contact-createurs", target: "_blank", rel: "noopener" }, t("ce formulaire")); return a; })(), " ",
        t("et je corrige au plus vite. Tu peux aussi me demander de retirer tes créations du site par le même formulaire.")));
}
