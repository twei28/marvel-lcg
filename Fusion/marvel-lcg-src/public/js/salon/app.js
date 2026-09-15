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
import { cardImageUrl, oublierDecksSauvegardes } from "/public/js/prepare/api.js";
import { t, boutonLangue } from "/public/js/prepare/langue.js";
import { cards } from "/public/js/prepare/cards.js";
import { versDeckMoteur } from "/public/js/marvelcdb/conversion.js";
import { validerDeck, choisiesDuDeck } from "/public/js/deckbuilder/regles.js";

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

/* ---------------- Import d'un deck MarvelCDB ---------------- */
//
// L'invite n'a pas de compte et ne verra jamais le constructeur de decks : le
// seul moyen d'apporter SON deck est de coller son lien MarvelCDB. Le deck est
// converti puis ENREGISTRE sur le serveur, parce que le salon ne transmet a
// l'hote qu'un identifiant (`set_choix_siege`), jamais les quarante cartes.

function mcdbId(saisie) {
    const texte = String(saisie || "").trim();
    const avecChemin = texte.match(/(?:decklist|deck)\/(?:view\/)?(\d+)/);
    if (avecChemin) return avecChemin[1];
    const nu = texte.match(/(\d{3,})/);
    return nu ? nu[1] : "";
}

async function mcdbCharger(id) {
    // Les deux formes d'adresse de MarvelCDB : une liste publiee, ou un deck
    // personnel rendu public. On essaie l'une puis l'autre.
    for (const url of [`https://marvelcdb.com/api/public/decklist/${id}.json`,
                       `https://marvelcdb.com/api/public/deck/${id}.json`]) {
        try {
            const r = await fetch(url);
            if (r.ok) return await r.json();
        } catch (e) { /* adresse suivante */ }
    }
    throw new Error(t("Deck introuvable sur marvelcdb") + " (ID " + id + "). "
        + t("Vérifie que le deck est public."));
}

async function importerMarvelcdb(saisie) {
    const id = mcdbId(saisie);
    if (!id) throw new Error(t("URL/ID marvelcdb invalide."));
    const data = await mcdbCharger(id);
    await cards.load();

    // MarvelCDB nomme le heros `hero_code` pour Marvel Champions
    // (`investigator_code` est le champ d'Arkham Horror, et reste vide ici).
    const code = String(data.hero_code || data.investigator_code || "").split(",")[0];
    const codeBase = code.replace(/[a-z]$/, "");
    const memeHero = (autre) => {
        const c = String(autre || "").split(",")[0];
        return c === code || c.replace(/[a-z]$/, "") === codeBase;
    };
    // ⚠ Le heros est DEJA choisi a ce stade, et il l'emporte : la conversion
    // jette les 15 cartes signature du deck marvelcdb et ne garde que les 25
    // cartes d'aspect, qui ne tiennent a personne. Un deck d'un AUTRE heros est
    // donc accepte depuis le 09/09/2026 — le siege garde son heros, il change
    // seulement de pioche. Ce qui reste interdit, c'est une pioche que les
    // regles de construction du heros refusent (verifiee juste apres).
    const emprunte = !memeHero(etat.hero.heroCardId) && !memeHero((etat.hero.deck.hero || [])[0]);
    const nomDeck = data.name || etat.hero.name;

    // Meme conversion que le wizard (public/js/marvelcdb/conversion.js) : un
    // deck jouable cote hote doit l'etre a l'identique cote invite.
    const deck = versDeckMoteur(
        { id, nom: emprunte ? `${nomDeck} (${etat.hero.name})` : nomDeck, cartes: data.slots || {} },
        etat.hero.deck,
        (cid) => { const c = cards.get(cid); return (c && c.class) || ""; },
    );

    // Verdict de l'EDITEUR DE DECK, pas une seconde regle ecrite ici : Spider-Woman
    // exige deux aspects, Fatalis s'interdit les allies, Ares plafonne ses emprunts.
    const verdict = validerDeck({
        hero: etat.hero, choisies: choisiesDuDeck(etat.hero, deck), carte: (cid) => cards.get(cid), t,
    });
    if (!verdict.ok) {
        throw new Error(`${t("Ce deck n’est pas légal pour")} ${etat.hero.name} : `
            + verdict.problemes.join(" ; "));
    }

    // Un nom par siege ET par deck : deux invites qui importent le meme deck
    // ne s'ecrasent pas, et un invite qui change d'avis ne laisse pas trainer
    // le precedent sous le meme nom.
    const nom = `mcdb-${id}-siege${siege}`;
    const reponse = await fetch("/save_deck", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_name: nom, deck }),
    });
    const rep = await reponse.json().catch(() => ({}));
    if (!reponse.ok || rep.error) {
        throw new Error(rep.error || t("Le serveur a refusé le deck."));
    }
    // Notre propre liste date d'avant l'enregistrement : sans cet oubli, le
    // deck fraichement importe n'apparaitrait pas dans la liste ci-dessous.
    oublierDecksSauvegardes();
    return { id: nom, name: deck.name || nom, source: "saved", deck };
}

function champImport() {
    const saisie = el("input", {
        class: "salon-mcdb-champ",
        placeholder: t("Colle une URL ou un ID marvelcdb..."),
    });
    const bouton = el("button", { class: "salon-mcdb-bouton" }, t("Importer"));
    bouton.onclick = async () => {
        if (!saisie.value.trim()) return;
        bouton.disabled = true;
        statut(t("Import en cours…"));
        try {
            const dk = await importerMarvelcdb(saisie.value);
            await envoyerChoix(dk);
        } catch (e) {
            statut(e.message || t("Import impossible."), true);
        } finally {
            bouton.disabled = false;
        }
    };
    saisie.onkeydown = (ev) => { if (ev.key === "Enter") bouton.onclick(); };
    return el("div", { class: "salon-mcdb" },
        el("b", {}, t("Ton propre deck")),
        el("div", { class: "salon-mcdb-ligne" }, saisie, bouton),
        el("small", {}, t("Le deck doit être public sur marvelcdb. Celui d’un autre héros marche : seules ses cartes d’aspect sont reprises.")),
    );
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
        )),
        champImport(),
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
            // `multi=1` : partie REPARTIE, un client par siege. Le plateau s'en
            // sert pour NE PAS s'annoncer en hot-seat, sinon l'hote reserverait
            // tous les sieges et verrait les mains de tout le monde.
            if (nom) location.href = `/app/board.html?p=${siege}&multi=1`;
        } catch (e) {
            /* serveur momentanément injoignable : on réessaiera au tour suivant */
        }
    }, 2000);
}

/* ---------------- Campagne : l'équipe est déjà composée ---------------- */

/**
 * Une campagne attend-elle ?
 *
 * En campagne il n'y a RIEN à choisir : l'équipe a été arrêtée à la création de
 * la campagne, et le livret interdit d'en changer. Le siège N tient le N-ième
 * membre, ce qui est déjà ce que fait le moteur (il reçoit `players` dans cet
 * ordre, voir `lancerScenario` dans js/campagne/app.js).
 *
 * Montrer la grille des héros ici serait donc un mensonge : le choix serait
 * écrasé au lancement, et l'invité jouerait autre chose que ce qu'il a pris.
 */
async function campagneEnCours() {
    try {
        const reponse = await fetch("get_campagne_en_cours?", { cache: "no-store" });
        if (!reponse.ok) return null;
        const brut = await reponse.json();
        return brut && brut.id ? brut : null;
    } catch (e) {
        // Serveur d'une version anterieure, ou route indisponible : on retombe
        // sur le salon ordinaire plutot que de bloquer l'invite.
        return null;
    }
}

function rendreCampagne(campagne) {
    const membre = (campagne.equipe || [])[siege];
    const nom = membre ? (membre.nomHeros || membre.heros) : null;
    $("#salon-choix").replaceChildren(
        el("h2", {}, campagne.nom || t("Campagne en cours")),
        nom
            ? el("p", { class: "salon-campagne-heros" },
                el("b", {}, t("Tu tiens")), " ", nom)
            : el("p", { class: "salon-campagne-heros" },
                t("Aucun héros n’est prévu pour ce siège dans cette campagne.")),
    );
    if (nom) {
        statut(t("L’équipe est fixée par la campagne : il n’y a rien à choisir."));
        bandeauAttente(true);
    } else {
        statut(t("Aucun héros n’est prévu pour ce siège dans cette campagne."), true);
    }
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
    // Le lien vers la galerie est ecrit en francais dans la page : on le
    // retraduit ici, comme le bandeau d'attente juste au-dessus.
    const galerie = document.querySelector(".salon-galerie");
    if (galerie) galerie.textContent = "🃏 " + t("Parcourir les cartes");
    // ⚠ ET LE TITRE DE L'ONGLET AUSSI. Il etait le dernier texte francais en
    // dur de cet ecran : tout le corps etait deja retraduit ici, le `<title>`
    // ne l'etait pas. Un invite anglophone lisait « choisis ton heros » dans
    // son onglet pendant que la page, elle, parlait anglais.
    document.title = t("Marvel Champions — choisis ton héros");
    // La campagne d'abord : s'il y en a une, il n'y a aucun choix a reprendre
    // ni a proposer, et `reprendreChoixExistant` n'aurait rien a trouver.
    const campagne = await campagneEnCours();
    if (campagne) {
        rendreCampagne(campagne);
        surveillerLeLancement();
        return;
    }

    statut(t("Choisis ton héros, puis ton deck. L’hôte lancera quand tout le monde aura choisi."));

    await reprendreChoixExistant();
    if (etat.hero) await rendreDecks();
    else await rendreHeros();

    surveillerLeLancement();
}

demarrer();
