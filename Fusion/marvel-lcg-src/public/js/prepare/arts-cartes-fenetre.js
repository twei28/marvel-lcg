// arts-cartes-fenetre.js : la petite fenetre « Choisir des arts alternatifs
// pour les cartes de ce deck ? », posee a la selection d'un deck (existant ou
// importe) quand il contient des cartes a art alternatif.
//
// Deux temps dans la meme fenetre :
//   1. la question Oui / Non, avec la case « Ne plus proposer » ;
//   2. si Oui : toutes les cartes du deck qui ont un art alternatif, chacune
//      avec ses vignettes (officielle / TMNT). Un clic enregistre tout de suite
//      (cle mc_card_art_v1, lue par le plateau et le deck-builder).
//
// La logique est dans arts-cartes-choix.js (pure, testee). Ici, seulement le
// DOM ; les outils de la page (el, modales, traduction, images) arrivent en
// parametre pour ne pas dupliquer app.js.
"use strict";

import { doitProposer, lignesDeChoix, picIdAvecArt, STANDARD } from "./arts-cartes-choix.js";
import { ecrireChoixCartes, lireChoixCartes, lireNePlusProposer, ecrireNePlusProposer } from "./arts-cartes-stockage.js";

/**
 * Propose les arts alternatifs du deck, si le deck en a et que l'utilisateur
 * n'a pas coche « Ne plus proposer ».
 *
 * @param {object} o
 * @param {object} o.deck        deck moteur ({ player_deck, ... })
 * @param {string} o.heros       card_id du heros (« tl001a,tl001b »)
 * @param {Function} o.el        constructeur de noeuds de la page
 * @param {Function} o.t         traduction
 * @param {Function} o.ouvrirModale
 * @param {Function} o.fermerModale
 * @param {Function} o.imageUrl  (picId) -> url de l'image
 * @param {Function} o.nomCarte  (card_id) -> nom affiche
 * @returns {boolean} true si la fenetre a ete ouverte
 */
export function proposerArtsCartes({ deck, heros, el, t, ouvrirModale, fermerModale, imageUrl, nomCarte }) {
    const ids = (deck && deck.player_deck) || [];
    if (!doitProposer(ids, lireNePlusProposer())) return false;

    const corps = el("div", { class: "ac-corps" });
    const panneau = el("div", { class: "deck-modal-panel vh-panel ac-panneau", style: { "--sections": "1" } },
        el("div", { class: "dm-head" },
            el("b", { class: "mvl" }, t("Arts alternatifs")),
            el("span", { class: "dm-sub" }, t("Cartes de ce deck")),
        ),
        corps,
    );
    const overlay = el("div", { class: "deck-modal ac-modal", onclick: (e) => { if (e.target === overlay) fermer(); } }, panneau);
    const fermer = () => fermerModale(overlay);

    const poserQuestion = () => {
        const case_ = el("input", { type: "checkbox", id: "ac-ne-plus" });
        case_.checked = lireNePlusProposer();
        const memoriser = () => ecrireNePlusProposer(case_.checked);
        corps.replaceChildren(
            el("p", { class: "ac-question" }, t("Choisir des arts alternatifs pour les cartes de ce deck ?")),
            el("label", { class: "ac-ne-plus", for: "ac-ne-plus" }, case_, t("Ne plus proposer")),
            el("div", { class: "vh-actions" },
                el("button", { type: "button", class: "tampon", "data-ac": "non", onclick: () => { memoriser(); fermer(); } }, t("Non")),
                el("button", { type: "button", class: "tampon jaune", "data-ac": "oui", onclick: () => { memoriser(); poserCartes(); } }, t("Oui")),
            ),
        );
    };

    const poserCartes = () => {
        const lignes = lignesDeChoix(ids, lireChoixCartes(), heros);
        const grille = el("div", { class: "ac-grille" });
        for (const ligne of lignes) {
            const vignettes = el("div", { class: "ac-vignettes" });
            const marquer = (code) => {
                for (const b of vignettes.children) b.classList.toggle("on", b.getAttribute("data-code") === code);
            };
            for (const code of ligne.codes) {
                vignettes.append(el("button", {
                    type: "button", class: "ac-vignette" + (code === ligne.affiche ? " on" : ""), "data-code": code,
                    title: code === STANDARD ? t("Illustration officielle") : `${t("Illustration")} ${code.toUpperCase()}`,
                    onclick: () => { ecrireChoixCartes({ [ligne.id]: code }); marquer(code); },
                },
                    el("img", { src: imageUrl(picIdAvecArt(ligne.id, code)), alt: "", loading: "lazy" }),
                    el("span", {}, code === STANDARD ? t("Officielle") : code.toUpperCase()),
                ));
            }
            grille.append(el("div", { class: "ac-carte", "data-carte": ligne.id },
                el("div", { class: "ac-nom" }, nomCarte(ligne.id), ligne.exemplaires > 1 ? el("small", {}, ` ×${ligne.exemplaires}`) : null),
                vignettes,
            ));
        }
        corps.replaceChildren(
            el("p", { class: "ac-question" }, t("Touche l'illustration voulue pour chaque carte.")),
            grille,
            el("div", { class: "vh-note" }, t("Mémorisé sur cet appareil. Même carte pour le jeu, seule l'image change.")),
            el("div", { class: "vh-actions" },
                el("button", { type: "button", class: "tampon jaune", "data-ac": "fin", onclick: fermer }, t("Terminer"))),
        );
    };

    poserQuestion();
    ouvrirModale(overlay);
    return true;
}
