// app.js — le SALON : l'invité choisit SON héros et SON deck, depuis son siège.
//
// Page volontairement à l'écart du wizard (public/js/prepare/app.js, 1850
// lignes) : on ne veut prendre aucun risque sur le chemin SOLO, qui sert tous
// les jours. Seule la couche DONNÉES est partagée (catalog / api / cards),
// pas l'interface.
//
// Le siège vient de l'URL (?p=N), posée par /claim_seat qui a aussi déposé le
// cookie seat_token_<N>. C'est le cookie qui fait foi côté serveur : l'URL
// seule ne donne aucun droit.
"use strict";
import { catalog } from "/public/js/prepare/catalog.js";
import { cardImageUrl } from "/public/js/prepare/api.js";
import { t, boutonLangue } from "/public/js/prepare/langue.js";

const siege = Number(new URLSearchParams(location.search).get("p") ?? "-1");

const etat = { hero: null, deckChoisi: null };

const $ = (sel) => document.querySelector(sel);

function el(tag, attrs = {}, ...enfants) {
    const n = document.createElement(tag);
    for (const [cle, valeur] of Object.entries(attrs)) {
        if (cle === "class") n.className = valeur;
        else if (cle.startsWith("on")) n[cle] = valeur;
        else if (valeur != null) n.setAttribute(cle, valeur);
    }
    for (const enfant of enfants.flat()) {
        if (enfant != null) n.append(enfant.nodeType ? enfant : document.createTextNode(enfant));
    }
    return n;
}

function statut(texte, erreur = false) {
    const zone = $("#salon-statut");
    zone.textContent = texte;
    zone.classList.toggle("est-erreur", erreur);
}

/** Le bandeau d'attente : visible dès que HÉROS ET DECK sont choisis.
 *  Sans lui, l'invité reste devant la grille sans savoir s'il a fini quelque
 *  chose. Il n'a effectivement plus rien à faire : le salon bascule tout seul
 *  vers le plateau quand l'hôte lance (voir surveillerLeLancement). */
function bandeauAttente(pret) {
    const zone = $("#salon-attente");
    if (!zone) return;
    zone.classList.toggle("est-visible", !!pret);
    if (pret) {
        // Le titre est traduit ICI et non dans le HTML : sinon un joueur en
        // anglais lirait « Tu es prêt » en dur au milieu du reste traduit.
        const titre = zone.querySelector("b");
        if (titre) titre.firstChild.textContent = t("Tu es prêt");
        const detail = $("#salon-attente-detail");
        if (detail) detail.textContent = t("En attente du lancement de la partie par l’hôte.");
    }
}

/* ---------------- Envoi du choix ---------------- */

async function envoyerChoix(deck) {
    try {
        const reponse = await fetch("/set_choix_siege", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                p: siege,
                hero_card_id: etat.hero.heroCardId,
                deck_id: deck.id,
                deck_source: deck.source,
            }),
        });
        if (reponse.status === 403) {
            statut(t("Ce siège n’est pas le tien. Ouvre ton lien personnel."), true);
            return;
        }
        if (!reponse.ok) {
            statut(t("Choix refusé par le serveur."), true);
            return;
        }
    } catch (e) {
        statut(t("Serveur injoignable. Réessaie dans un instant."), true);
        return;
    }
    etat.deckChoisi = deck;
    statut(`${t("Choix envoyé")} : ${etat.hero.name} — ${deck.name}. ${t("Tu peux encore changer d’avis.")}`);
    bandeauAttente(true);
    rendreDecks();
}

/* ---------------- Rendu ---------------- */

async function rendreDecks() {
    const decks = await catalog.decksForHero(etat.hero);
    $("#salon-choix").replaceChildren(
        el("button", {
            class: "salon-retour",
            onclick: () => { etat.hero = null; etat.deckChoisi = null; bandeauAttente(false); rendreHeros(); },
        }, `← ${t("Changer de héros")}`),
        el("h2", {}, `${etat.hero.name} — ${t("choisis ton deck")}`),
        ...decks.map((dk) => el("button", {
            class: `salon-deck${etat.deckChoisi && etat.deckChoisi.id === dk.id ? " est-choisi" : ""}`,
            onclick: () => envoyerChoix(dk),
        },
            el("b", {}, dk.name),
            el("span", {}, (dk.aspects && dk.aspects.length ? dk.aspects.join(" + ") : t("Deck de base")))
        ))
    );
}

async function rendreHeros() {
    const heroes = await catalog.heroes();
    $("#salon-choix").replaceChildren(
        el("h2", {}, t("Choisis ton héros")),
        el("div", { class: "salon-grille" },
            ...heroes.map((h) => el("button", {
                class: "salon-hero",
                onclick: () => { etat.hero = h; rendreDecks(); },
            },
                el("img", { src: cardImageUrl(h.heroCardId), loading: "lazy", alt: h.name }),
                el("span", {}, h.name)
            ))
        )
    );
}

/* ---------------- Bascule vers le plateau ---------------- */

// Quand l'hôte lance, /get_play_scene_name cesse de rendre une chaîne vide.
// C'est le signal le moins coûteux : aucune route à ajouter.
function surveillerLeLancement() {
    setInterval(async () => {
        try {
            const reponse = await fetch("get_play_scene_name?");
            const nom = (await reponse.text()).trim();
            if (nom) location.href = `/app/board.html?p=${siege}`;
        } catch (e) {
            /* serveur momentanément injoignable : on réessaiera au tour suivant */
        }
    }, 2000);
}

/* ---------------- Démarrage ---------------- */

async function reprendreChoixExistant() {
    try {
        const reponse = await fetch("get_choix_sieges?");
        const brut = await reponse.json();
        const dejaChoisi = (brut.sieges || {})[String(siege)];
        if (!dejaChoisi) return;
        const heroes = await catalog.heroes();
        const hero = heroes.find((h) => h.heroCardId === dejaChoisi.hero_card_id);
        if (!hero) return;
        etat.hero = hero;
        const decks = await catalog.decksForHero(hero);
        etat.deckChoisi = decks.find((d) => d.id === dejaChoisi.deck_id) || null;
        if (etat.deckChoisi) {
            statut(`${t("Ton choix actuel")} : ${hero.name} — ${etat.deckChoisi.name}. ${t("Tu peux encore changer d’avis.")}`);
            bandeauAttente(true);
        }
    } catch (e) {
        /* pas de choix repris : on repart de la grille */
    }
}

async function demarrer() {
    if (!Number.isInteger(siege) || siege < 0) {
        statut(t("Ouvre ton lien personnel : c’est lui qui réserve ton siège."), true);
        return;
    }
    // Libellé affiché = index technique + 1. Voir salon-etat.js.
    $("#salon-entete").textContent = `${t("Tu es le")} ${t("Joueur")} ${siege + 1}`;
    // Bouton 🌐 FR/EN, comme le wizard et le plateau (guide §11).
    $("#salon-entete").append(" ", boutonLangue("salon-langue"));
    statut(t("Choisis ton héros, puis ton deck. L’hôte lancera quand tout le monde aura choisi."));

    await reprendreChoixExistant();
    if (etat.hero) await rendreDecks();
    else await rendreHeros();

    surveillerLeLancement();
}

demarrer();
