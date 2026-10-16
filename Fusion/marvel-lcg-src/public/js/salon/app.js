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
import { cardImageUrlEn, cardImageUrlHd, oublierDecksSauvegardes } from "/public/js/prepare/api.js";
import { t, boutonLangue } from "/public/js/prepare/langue.js";
import { cards } from "/public/js/prepare/cards.js";
import { boutonAffichage } from "/public/js/prepare/affichage.js";
import { poserIcone } from "/public/js/prepare/icones-entete.js";
import { urlNarval } from "/public/js/prepare/narval.js";
import { versDeckMoteur } from "/public/js/marvelcdb/conversion.js";
import { chargerDeck, lireLien } from "/public/js/marvelcdb/sources.js";
import { validerDeck, choisiesDuDeck } from "/public/js/deckbuilder/regles.js";
import { demanderForcage } from "/public/js/prepare/deck-force.js";
import {
    decisionSalon, memoriserRepere, relireRepere, oublierRepere,
    memoriserDernierChoix, relireDernierChoix,
} from "/public/js/salon/bascule.js";
import {
    herosTirables, scenariosTirables, tirer, creerBandeau, caseHeros, caseScenario, lireRoue, publierRoue,
} from "/public/js/prepare/roue.js";

const siege = Number(new URLSearchParams(location.search).get("p") ?? "-1");

// `propose` : le deck de la manche d'avant, pré-coché mais PAS encore envoyé
// (13/10/2026, « un clic sur Je suis prêt suffit pour rejouer pareil »).
const etat = { hero: null, deckChoisi: null, propose: null };

// ⚠ LES DEUX SIGNAUX QUI DISENT « CETTE PARTIE EST LA MIENNE », et aucun des
// deux ne tient seul (voir bascule.js) :
//   - `monChoix` : l'identifiant de la carte heros que cet invite a choisi.
//     Aveugle quand on rejoue une manche avec LE MEME heros.
//   - `debutAuChoix` : le repere de la partie qui tournait au moment du choix.
//     Aveugle au rechargement s'il etait releve a l'arrivee — d'ou le fait
//     qu'il soit releve AU MOMENT DU CHOIX et retenu AVEC lui.
let monChoix = "";
let debutAuChoix = null;
// CAMPAGNE : il n'y a rien a choisir, l'equipe est fixee par le livret. Le
// heros ne peut alors PAS servir de signal (il est le meme a toutes les
// manches) ; la fraicheur decide seule.
let sansChoix = false;
// Depuis quand ce salon attend-il ? Sert au seul cas qu'aucun signal ne
// tranche : un invite sans repere, arrive apres le lancement.
let attenteDepuis = Date.now();
// Ce qui est affiche dans la zone d'avertissement, pour ne PAS la repeindre a
// chaque sondage (voir montrerAvertissement).
let avertissementAffiche = null;

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

/** Le bandeau d'attente, DANS la scène : visible dès que HÉROS ET DECK sont
 *  choisis. Sans lui, l'invité reste devant la grille sans savoir s'il a fini
 *  quelque chose. Il n'a effectivement plus rien à faire : le salon bascule
 *  tout seul vers le plateau quand l'hôte lance (voir surveillerLeLancement).
 *  Il porte aussi l'équipe en formation (voir sonderEquipe). */
let attenteVisible = false;
function bandeauAttente(pret) {
    const zone = $("#salon-attente");
    if (!zone) return;
    attenteVisible = !!pret;
    // ⚠ L'ÉQUIPE ET LE MÉCHANT DE L'HÔTE RESTENT VISIBLES AVANT D'ÊTRE PRÊT
    // (13/10/2026, décision 3 de .planning/todos/2026-10-13-inviter-un-connecte.md) :
    // l'invité voit, au fur et à mesure, contre qui l'hôte a choisi de jouer.
    // Seuls le titre et la phrase changent quand il est prêt.
    zone.classList.add("est-visible");
    $("#salon-b").classList.add("en-attente");
    // Le titre est traduit ICI et non dans le HTML : sinon un joueur en
    // anglais lirait « Tu es prêt » en dur au milieu du reste traduit.
    const titre = zone.querySelector("b");
    if (titre) titre.firstChild.textContent = pret ? t("Tu es prêt") : t("L’équipe");
    const points = zone.querySelector(".points");
    if (points) points.hidden = !pret;
    const detail = $("#salon-attente-detail");
    if (detail) {
        detail.textContent = pret
            ? t("En attente du lancement de la partie par l’hôte.")
            : t("Choisis ton héros, puis ton deck.");
    }
    sonderEquipe();
}

/* ---------------- Envoi du choix ---------------- */

async function envoyerChoix(deck) {
    // ⚠ LE REPÈRE SE RELÈVE AVANT L'ENVOI, ET C'EST TOUT LE SUJET (ronde 2 du
    // 21/09/2026). Relevé APRÈS, il y avait une course : si l'hôte lançait
    // entre l'envoi et la lecture, on retenait le repère de la partie NEUVE et
    // l'invité ne basculait jamais dedans. La première version couvrait cette
    // course par une clause de réserve qui rouvrait le cas 7 en grand ; ici la
    // course n'existe plus, donc la clause non plus. Relevé avant, le pire est
    // de retenir un repère d'un instant trop vieux — ce qui fait basculer,
    // c'est-à-dire exactement le bon sens de l'erreur.
    const table = await lireLaTable();
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
    etat.propose = null;
    monChoix = etat.hero.heroCardId;
    memoriserDernierChoix(window.localStorage, siege, etat.hero.heroCardId, deck.id, Date.now());
    // Le repère relevé plus haut est retenu AVEC le choix : c'est ce qui le
    // fait survivre au rechargement, là où `/new` aura vidé `choix_sieges`.
    //
    // ⚠ ET SI LA TABLE N'A PAS RÉPONDU, ON NE RETIENT RIEN. Un repère inventé
    // (une chaîne vide, par exemple) différerait de celui de l'ancienne partie
    // et provoquerait une bascule immédiate dessus — exactement le défaut qu'on
    // ferme. Sans repère, la règle attend et finit par PROPOSER, ce qui laisse
    // le dernier mot à l'invité.
    if (table) {
        debutAuChoix = table.debut;
        memoriserRepere(window.localStorage, siege, monChoix, debutAuChoix, Date.now());
    }
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

async function importerMarvelcdb(saisie) {
    const { id } = lireLien(saisie);
    if (!id) throw new Error(t("URL/ID marvelcdb invalide."));
    const trouve = await chargerDeck(saisie);
    if (!trouve) throw new Error(t("Deck introuvable sur marvelcdb ni mc4db") + " (ID " + id + "). "
        + t("Vérifie que le deck est public."));
    const data = trouve.data;
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
        // Nos regles peuvent se tromper : l'invite peut forcer, et forcer nous
        // envoie le deck et les raisons du refus (voir prepare/deck-force.js).
        const force = await demanderForcage({
            hero: etat.hero, deck, problemes: verdict.problemes, source: `marvelcdb ${id}`,
            ecran: "salon", nomCarte: (cid) => { const c = cards.get(cid); return c && c.name; }, t,
        });
        if (!force) throw new Error(t("Import annulé."));
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
        el("small", {}, t("Le deck doit être public sur marvelcdb ou mc4db. Celui d’un autre héros marche : seules ses cartes d’aspect sont reprises.")),
    );
}

/* ---------------- Habillage : la même grammaire que l'assistant ---------------- */

const ASPECTS = {
    aggression: "#d83b32", justice: "#efc34a", leadership: "#2f7de1", protection: "#35a865",
    basic: "#9aa0aa", pool: "#a34ad9", determination: "#965cc4",
};

const idBase = (heroCardId) => String(heroCardId || "").split(",")[0];

function portrait(cardId, cls) {
    return el("div", {
        class: "portrait " + (cls || ""),
        style: cardId ? { backgroundImage: `url(${cardImageUrlEn(cardId)})` } : {},
    });
}

/** Un héros à deux identités (Cloak & Dagger) partage sa tuile en diagonale. */
function portraitHeros(hero) {
    if (hero && hero.lie) {
        return el("div", { class: "portrait-duo" },
            portrait(hero.heroCardId, "duo duo-a"),
            portrait(hero.lie.heroCardId, "duo duo-b"));
    }
    return portrait(hero && hero.heroCardId);
}

function nomHeros(hero) {
    if (!hero) return "";
    if (hero.lie) {
        const nomDeck = String((hero.deck && hero.deck.name) || "").replace(/^\*\s*/, "").trim();
        return nomDeck || hero.name;
    }
    return hero.name;
}

function portraitScenario(sc) {
    const ids = (sc && sc.villainCards) || [];
    if (ids.length < 2) {
        return el("div", { class: "portrait", style: { backgroundImage: `url("${cardImageUrlEn(sc.tileImage)}")` } });
    }
    const n = Math.min(ids.length, 4);
    return el("div", { class: `portrait portrait-multi n${n}` },
        ...ids.slice(0, 4).map((id) => el("i", { style: { backgroundImage: `url("${cardImageUrlEn(id)}")` } })));
}

function barreAspects(deck) {
    const parAspect = {};
    for (const id of ((deck && deck.player_deck) || [])) {
        const a = cards.aspectOf(id) || "basic";
        parAspect[a] = (parAspect[a] || 0) + 1;
    }
    const ordre = ["aggression", "justice", "leadership", "protection", "basic", "pool"];
    return el("div", { class: "aspect-bar" },
        ...ordre.filter((a) => parAspect[a]).map((a) => el("span", {
            class: "seg", style: { background: ASPECTS[a], flex: parAspect[a] }, title: a + " : " + parAspect[a],
        })));
}

/** Le nom géant ne se coupe jamais : c'est sa taille qui cède. */
function ajusterNom() {
    const scene = $("#tb-scene");
    const nom = scene && scene.querySelector(".tb-nomg");
    if (!nom) return;
    nom.style.fontSize = "";
    const mesurer = () => {
        let taille = parseFloat(getComputedStyle(nom).fontSize);
        while (taille > 28 && (nom.scrollWidth > nom.clientWidth + 1 || nom.offsetHeight > scene.clientHeight * 0.4)) {
            taille -= 4;
            nom.style.fontSize = taille + "px";
        }
    };
    requestAnimationFrame(() => requestAnimationFrame(mesurer));
}

/** La scène : l'art, le nom, ou l'invitation à choisir. `libre` remplace le
 *  texte par défaut quand il n'y a pas de héros (campagne). */
function rendreScene(hero, libre = null) {
    const fond = $("#salon-fond");
    if (!fond) return;
    const petit = `${t("Joueur")} ${siege + 1}`;
    if (!hero) {
        fond.replaceChildren(
            el("div", { class: "tb-art vide" }),
            el("div", { class: "tb-trame" }),
            el("div", { class: "tb-nomg" },
                el("small", {}, (libre && libre.petit) || petit),
                (libre && libre.grand) || t("Choisis un héros")),
        );
        ajusterNom();
        return;
    }
    const traits = [...new Set([...(hero.traits || []), ...(hero.traitsAlterEgo || [])])].slice(0, 4).join(" · ");
    fond.replaceChildren(
        // Scan anglais même en français : le scan FR porte un filigrane, très
        // visible à cette taille (même choix que l'assistant).
        hero.lie
            ? el("div", { class: "tb-art" }, portraitHeros(hero))
            : el("div", { class: "tb-art", style: { backgroundImage: `url("${cardImageUrlHd(idBase(hero.heroCardId))}")` } }),
        el("div", { class: "tb-trame" }),
        el("div", { class: "tb-nomg" }, el("small", {}, traits || petit), nomHeros(hero)),
    );
    ajusterNom();
}

/** Les deux étapes, dans l'en-tête, comme « 1 Équipe › 2 Decks » de l'assistant. */
let etapeActuelle = 1;
function majEtapes() {
    const barre = $("#salon-barre");
    if (!barre) return;
    barre.querySelectorAll(".pstep").forEach((bouton, i) => {
        const fait = i + 1 < etapeActuelle && !!etat.hero;
        bouton.classList.toggle("active", i + 1 === etapeActuelle);
        bouton.classList.toggle("done", fait);
        bouton.querySelector(".pnum").textContent = fait ? "\u2713" : String(i + 1);
        bouton.disabled = i === 1 && !etat.hero;
    });
    $("#salon-titre").textContent = etapeActuelle === 1 ? t("Héros") : t("Decks");
}

function retourAuxHeros() {
    etat.hero = null;
    etat.deckChoisi = null;
    etat.propose = null;
    bandeauAttente(false);
    rendreHeros();
}

function construireBarre() {
    const barre = $("#salon-barre");
    const galerie = el("a", { class: "btn ghost salon-galerie", href: "/galerie.html", target: "_blank", rel: "noopener" });
    poserIcone(galerie, "fa-clone", t("Parcourir les cartes"));
    const etape = (i, libelle, action) => el("button", { class: "pstep", onclick: action },
        el("span", { class: "pnum" }, String(i)),
        el("span", { class: "plabel" }, libelle));
    barre.replaceChildren(
        el("span", { class: "brand" },
            el("img", { class: "brand-narwhal", src: urlNarval(), alt: "NarwhalChampions" })),
        el("div", { class: "salon-barre-outils" },
            boutonLangue("btn ghost btn-langue"), boutonAffichage("btn ghost"), galerie),
        el("div", { class: "steps" },
            etape(1, t("Héros"), () => { if (etapeActuelle !== 1) retourAuxHeros(); }),
            el("span", { class: "psep", "aria-hidden": "true" }, "\u203a"),
            etape(2, t("Decks"), () => { if (etat.hero) rendreDecks(); })),
    );
    majEtapes();
}

/* ---------------- Les decks du compte de l'invité (13/10/2026) ----------------
   Décision 3 : l'invité venu par une invitation (il a un compte) retrouve SES
   decks. Le moteur ne les rend qu'à celui qui tient ce siège, et le site
   seulement si ce siège a été pris par une invitation acceptée : un invité
   arrivé par un simple lien n'en a pas, et rien ne change pour lui. */

let decksDuCompte = null;     // {invite, decks:[{id, deck}]}, lu une fois

async function lireDecksDuCompte() {
    if (decksDuCompte) return decksDuCompte;
    try {
        const reponse = await fetch(`get_decks_invite?p=${siege}`, { cache: "no-store" });
        const brut = reponse.ok ? await reponse.json() : null;
        decksDuCompte = {
            invite: String((brut && brut.invite) || ""),
            decks: Array.isArray(brut && brut.decks) ? brut.decks : [],
        };
    } catch (e) {
        // Table muette : on réessaiera au prochain passage sur les decks.
        return { invite: "", decks: [] };
    }
    return decksDuCompte;
}

/** Les decks du compte qui vont à ce héros, au format des options du salon. */
async function decksDuCompteDuHeros(hero) {
    const { decks } = await lireDecksDuCompte();
    return decks
        .filter((d) => d && d.deck && d.deck.hero && String(d.deck.hero[0] || "").split(",")[0] === hero.heroCardId)
        .map((d) => ({ id: d.id, name: d.deck.name || d.id, source: "compte", deck: d.deck, aspects: d.deck.aspects || [] }));
}

/** Choisir un deck du compte : la table de l'hôte n'en a pas de copie, on la
 *  lui enregistre (comme un import MarvelCDB), puis on envoie le choix. */
async function choisirDeckDuCompte(dk) {
    const nom = `compte-${dk.id}-siege${siege}`.replace(/[^a-zA-Z0-9_-]+/g, "_").slice(0, 60);
    statut(t("Envoi de ton deck…"));
    try {
        const reponse = await fetch("/save_deck", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ file_name: nom, deck: dk.deck }),
        });
        const rep = await reponse.json().catch(() => ({}));
        if (!reponse.ok || rep.error) throw new Error(rep.error || "refus");
    } catch (e) {
        statut(t("Le serveur a refusé le deck."), true);
        return;
    }
    oublierDecksSauvegardes();
    await envoyerChoix({ id: nom, name: dk.name, source: "saved", deck: dk.deck });
}

/* ---------------- Rendu ---------------- */

async function rendreDecks() {
    etapeActuelle = 2;
    majEtapes();
    rendreScene(etat.hero);
    const [duCompte, communs] = await Promise.all([
        decksDuCompteDuHeros(etat.hero),
        catalog.decksForHero(etat.hero),
    ]);
    // Les copies déjà enregistrées chez l'hôte (« compte-… ») ne se montrent
    // qu'une fois, sous leur forme « Ton deck ».
    const decks = [...duCompte, ...communs.filter((d) => !String(d.id).startsWith(`compte-`))];
    // Le joueur a pu revenir aux héros pendant la lecture.
    if (etapeActuelle !== 2) return;
    $("#tb-compte").textContent = decks.length + " " + t("decks");
    const option = (dk) => {
        // Un deck du compte est enregistré chez l'hôte sous `compte-<id>-siegeN`.
        const copie = dk.source === "compte" ? `compte-${dk.id}-siege${siege}`.replace(/[^a-zA-Z0-9_-]+/g, "_").slice(0, 60) : dk.id;
        const choisi = (etat.deckChoisi && etat.deckChoisi.id === copie)
            || (!etat.deckChoisi && etat.propose && etat.propose.id === copie);
        const taille = ((dk.deck && dk.deck.player_deck) || []).length;
        return el("button", {
            class: `tb-deck salon-deck${choisi ? " chosen est-choisi" : ""}`,
            onclick: () => (dk.source === "compte" ? choisirDeckDuCompte(dk) : envoyerChoix(dk)),
        },
            el("div", { class: "do-name" }, dk.name),
            el("div", { class: "do-tags" },
                dk.source === "compte" ? el("span", { class: "tag salon-tag-compte" }, t("Ton deck")) : null,
                dk.aspects && dk.aspects.length
                    ? dk.aspects.map((a) => el("span", { class: "tag asp", style: { background: ASPECTS[a] || "#555" } }, a))
                    : el("span", { class: "tag" }, t("Deck de base"))),
            barreAspects(dk.deck),
            taille ? el("div", { class: "do-foot" }, el("span", { class: "do-size" }, taille + " " + t("cartes"))) : null,
        );
    };
    // La manche d'avant, pré-cochée : un seul clic pour rejouer pareil.
    const propose = !etat.deckChoisi && etat.propose ? etat.propose : null;
    // ⚠ `replaceChildren` ECRIT « null » en toutes lettres (vu en essai le
    // 13/10/2026) : le bandeau absent est filtre, pas passe tel quel.
    $("#salon-choix").replaceChildren(...[
        el("button", { class: "salon-retour", onclick: retourAuxHeros }, `← ${t("Changer de héros")}`),
        propose ? el("div", { class: "salon-rejouer" },
            el("p", {}, `${t("Comme la partie d’avant")} : ${nomHeros(etat.hero)} — ${propose.name}`),
            el("button", { class: "salon-pret", onclick: () => envoyerChoix(propose) }, t("Je suis prêt"))) : null,
        el("div", { class: "hero-grid tb-roster tb-roster-deck" }, ...decks.map(option)),
        champImport(),
    ].filter(Boolean));
}

async function rendreHeros() {
    etapeActuelle = 1;
    majEtapes();
    rendreScene(etat.hero);
    const heroes = await catalog.heroes();
    if (etapeActuelle !== 1) return;
    $("#tb-compte").textContent = heroes.length + " " + t("héros");
    $("#salon-choix").replaceChildren(
        el("div", { class: "hero-grid tb-roster", id: "salon-grille" },
            ...heroes.map((h) => el("button", {
                class: "tb-port salon-hero",
                title: nomHeros(h),
                "data-hero": h.id,
                onclick: () => { etat.hero = h; rendreDecks(); },
                onmouseenter: () => rendreScene(h),
                onfocus: () => rendreScene(h),
                onmouseleave: () => rendreScene(etat.hero),
            },
                portraitHeros(h),
                el("span", { class: "tb-port-nom" }, nomHeros(h)),
            ))),
    );
}

/* ---------------- L'équipe en formation (09/10/2026) ----------------
   Pendant l'attente, la scène montre qui est assis où et contre qui on joue.
   `/get_equipe_salon` ne rend que des identifiants de cartes héros et le
   scénario : jamais un deck. Gardée par le cookie de siège côté serveur. */

let equipeAffichee = "";
let tousLesScenarios = null;

async function scenarioPar(id) {
    if (!id) return null;
    if (!tousLesScenarios) {
        try { tousLesScenarios = await catalog.tousLesScenarios(); } catch (e) { return null; }
    }
    return tousLesScenarios.find((sc) => sc.id === id || (sc.scenarioIds || []).includes(id)) || null;
}

async function sonderEquipe() {
    if (sansChoix || document.hidden) return;
    let brut = { nombre: 0, sieges: {}, scenario: "" };
    try {
        const reponse = await fetch(`get_equipe_salon?p=${siege}`, { cache: "no-store" });
        if (reponse.ok) brut = await reponse.json();
    } catch (e) { /* on montre au moins ma propre place */ }
    const mien = etat.hero ? etat.hero.heroCardId : "";
    const empreinte = JSON.stringify([brut, mien]);
    if (empreinte === equipeAffichee) return;
    const heroes = await catalog.heroes();
    const scenario = await scenarioPar(brut.scenario);
    const nombre = Math.max(Number(brut.nombre) || 0, siege + 1);
    const places = [];
    for (let p = 0; p < nombre; p++) {
        const id = p === siege ? mien : String((brut.sieges || {})[String(p)] || "");
        const hero = id ? heroes.find((h) => h.heroCardId === id) : null;
        places.push(el("div", { class: "salon-place" + (hero ? "" : " attend") + (p === siege ? " moi" : "") },
            el("div", { class: "tb-siege" }, hero ? portraitHeros(hero) : el("span", { class: "plus" }, "?")),
            el("small", {}, `${t("Joueur")} ${p + 1}`, el("i", {}, hero ? nomHeros(hero) : t("Choisit…"))),
        ));
    }
    places.push(el("span", { class: "salon-contre", "aria-hidden": "true" }, "VS"));
    places.push(el("div", { class: "salon-place mechant" + (scenario ? "" : " attend") },
        el("div", { class: "tb-siege" }, scenario ? portraitScenario(scenario) : el("span", { class: "plus" }, "?")),
        el("small", {}, t("Méchant"), el("i", {}, scenario ? scenario.name : t("Pas encore choisi"))),
    ));
    equipeAffichee = empreinte;
    $("#salon-equipe").replaceChildren(...places);
}

/* ---------------- Bascule vers le plateau ---------------- */

// ⚠ CE QUE CETTE BOUCLE REGARDAIT, ET POURQUOI C'ÉTAIT FAUX. Elle basculait dès
// que `/get_play_scene_name` rendait autre chose qu'une chaîne vide, sur
// l'hypothèse — écrite noir sur blanc dans son commentaire — que la table est
// VIDE avant que l'hôte lance. Elle ne l'est pas : le moteur rend le nom de
// scène dès qu'un monde existe, et il en existe un jusqu'au redémarrage. Le
// 20/09/2026, deux fois dans la même soirée, des invités ont été expédiés dans
// la partie PRÉCÉDENTE avant d'avoir choisi leur héros, et y sont restés
// bloqués sur « Connexion à la partie… ».
//
// La question juste n'est pas « une partie tourne-t-elle ? » mais « la partie
// qui tourne est-elle la MIENNE ? ». Elle se tranche sur DEUX faits, et aucun
// des deux ne suffit seul — le héros de mon siège, et la fraîcheur de la
// partie. Les règles sont dans bascule.js, éprouvées à part.

/** Interroge la table. Rend `{enJeu, heros, debut}`, ou null si elle n'a pas
 *  répondu — auquel cas on ne conclut RIEN. */
async function lireLaTable() {
    try {
        const reponse = await fetch(`get_heros_du_siege?p=${siege}`, { cache: "no-store" });
        if (!reponse.ok) return null;
        const brut = await reponse.json();
        return {
            enJeu: !!brut.en_jeu,
            heros: String(brut.heros || ""),
            debut: String(brut.debut || ""),
        };
    } catch (e) {
        /* serveur momentanément injoignable : on réessaiera au tour suivant */
        return null;
    }
}

/** Le statut ordinaire, RECALCULÉ et non mémorisé : un texte mis de côté avant
 *  un avertissement serait périmé dès que l'invité change d'avis entre-temps. */
function statutNormal() {
    if (sansChoix) return t("L’équipe est fixée par la campagne : il n’y a rien à choisir.");
    if (etat.hero && etat.propose && !etat.deckChoisi) {
        return t("Ton héros et ton deck de la partie d’avant sont prêts : clique sur « Je suis prêt », ou change.");
    }
    if (etat.hero && etat.deckChoisi) {
        return `${t("Ton choix actuel")} : ${etat.hero.name} — ${etat.deckChoisi.name}. `
            + t("Tu peux encore changer d’avis.");
    }
    return t("Choisis ton héros, puis ton deck. L’hôte lancera quand tout le monde aura choisi.");
}

/** Le nom lisible d'un héros, à partir de l'identifiant de sa carte. */
async function nomDuHeros(heroCardId) {
    try {
        const heroes = await catalog.heroes();
        const trouve = heroes.find((h) => h.heroCardId === heroCardId);
        return trouve ? trouve.name : "";
    } catch (e) {
        return "";
    }
}

function zoneAvertissement() {
    let zone = $("#salon-avertissement");
    if (!zone) {
        zone = el("div", { id: "salon-avertissement", class: "salon-avertissement" });
        $("#salon-statut").after(zone);
    }
    return zone;
}

/** Dire ce qui se passe, ET offrir une sortie.
 *
 *  ⚠ UN MESSAGE SANS SORTIE EST UNE IMPASSE. L'ancien code envoyait l'invité
 *  au mauvais endroit ; un message honnête qui ne l'envoie nulle part n'est un
 *  progrès qu'à moitié. Chaque avertissement porte donc, quand il y a quelque
 *  part où aller, le bouton qui y mène — et la grille des héros reste
 *  disponible en dessous dans tous les cas.
 */
function montrerAvertissement(texte, bouton) {
    // ⚠ ON NE TOUCHE AU DOM QUE SI QUELQUE CHOSE A CHANGE (ronde 2 du
    // 21/09/2026). La première version repeignait à CHAQUE sondage, donc
    // toutes les deux secondes. Trois dégâts, tous visibles à l'usage :
    //   - `statut(statutNormal())` effaçait en moins de deux secondes tous les
    //     messages transitoires — « Import en cours… », « Import impossible. »,
    //     « Ce siège n'est pas le tien. », « Serveur injoignable. » ;
    //   - `bandeauAttente(...)` éteignait le bandeau que `rendreCampagne`
    //     venait d'allumer, et remplaçait « Aucun héros n'est prévu pour ce
    //     siège » par le texte générique de la campagne ;
    //   - `replaceChildren` reconstruisait le bouton sous le doigt : un clic à
    //     cheval sur un sondage ne déclenchait rien.
    const cle = texte ? `${texte}|${bouton ? bouton.libelle : ""}` : null;
    if (cle === avertissementAffiche) return;
    const zone = zoneAvertissement();
    if (!texte) {
        zone.replaceChildren();
        zone.classList.remove("est-visible");
        // On ne rend le statut ordinaire QUE si on l'avait remplacé : sinon on
        // écraserait ce que le reste de la page vient d'écrire.
        statut(statutNormal());
        bandeauAttente(!sansChoix && !!(etat.hero && etat.deckChoisi));
        avertissementAffiche = null;
        return;
    }
    zone.classList.add("est-visible");
    zone.replaceChildren(
        el("p", {}, texte),
        bouton ? el("button", { class: "salon-avertissement-bouton", onclick: bouton.action },
            bouton.libelle) : null,
    );
    bandeauAttente(false);
    avertissementAffiche = cle;
}

/** Partir vers le plateau.
 *
 *  ⚠ LE REPÈRE N'EST EFFACÉ QUE SI LE SALON A RECONNU LA PARTIE (ronde 2 du
 *  21/09/2026). La première version l'effaçait aussi quand le clic venait d'une
 *  simple PROPOSITION : un invité qui acceptait à tort revenait au salon sans
 *  repère et ne basculait plus jamais tout seul de la soirée. */
function allerAuPlateau(reconnue) {
    if (reconnue) oublierRepere(window.localStorage, siege);
    // `multi=1` : partie REPARTIE, un client par siege. Le plateau s'en sert
    // pour NE PAS s'annoncer en hot-seat, sinon l'hote reserverait tous les
    // sieges et verrait les mains de tout le monde.
    location.href = `/app/board.html?p=${siege}&multi=1`;
}

async function direLancementSansMoi(heros) {
    if (!heros) {
        // Personne à ce siège dans la partie qui vient de commencer : il n'y a
        // nulle part où aller, et c'est l'hôte qui doit agir.
        montrerAvertissement(
            t("L’hôte a lancé la partie sans ce siège. Préviens-le : il peut la relancer en t’attendant."),
            null);
        return;
    }
    // Ce siège tient quelqu'un d'autre : l'hôte a changé le héros. L'invité n'a
    // pas à rester dehors pour autant.
    const nom = await nomDuHeros(heros);
    montrerAvertissement(
        `${t("La partie a commencé, et ton siège n’y joue pas le héros que tu avais choisi.")}`
        + (nom ? ` ${t("Il joue")} ${nom}.` : ""),
        { libelle: nom ? `${t("Rejoindre avec")} ${nom}` : t("Rejoindre quand même"),
          // La partie est bien la nouvelle : le repère a servi.
          action: () => allerAuPlateau(true) });
}

function proposerDeRejoindre() {
    // ⚠ LE SEUL CAS QU'AUCUN SIGNAL NE TRANCHE : ce navigateur n'a pas de
    // repère (données effacées, autre appareil), donc on ne sait pas si la
    // partie qui tourne a commencé avant ou après. On ne force rien et on ne
    // laisse pas non plus devant un écran muet : c'est l'invité qui décide.
    montrerAvertissement(
        t("Une partie est en cours sur cette table. Impossible de savoir d’ici si c’est la tienne : "
            + "si l’hôte vient de lancer, rejoins-la ; sinon, attends encore un peu."),
        // On ne sait PAS si c'est la sienne : on garde son repère, pour qu'un
        // retour au salon le laisse basculer tout seul plus tard.
        { libelle: t("Rejoindre cette partie"), action: () => allerAuPlateau(false) });
}

async function sonderLeLancement() {
    // ⚠ RIEN QUAND PERSONNE NE REGARDE (16/09/2026). Cette boucle et celle
    // de l'assistant pesaient 61 % du trafic vers les tables, et leurs
    // appels empechaient le faucheur de fermer une table oubliee : il juge
    // l'inactivite sur la date du journal du moteur, que chaque requete
    // fait vivre. Ici on garde les deux secondes — on attend vraiment le
    // lancement — mais seulement tant que l'onglet est visible.
    if (document.hidden) return;
    const table = await lireLaTable();
    if (!table) return;

    // CAMPAGNE : le repère n'a pas pu être relevé « au moment du choix »,
    // puisqu'il n'y a pas de choix. On le relève donc à la première réponse de
    // la table et on le retient, pour qu'il survive au rechargement exactement
    // comme celui d'un invité ordinaire.
    if (sansChoix && debutAuChoix == null) {
        debutAuChoix = table.debut;
        memoriserRepere(window.localStorage, siege, "", debutAuChoix, Date.now());
    }

    const quoi = decisionSalon({
        monChoix, sansChoix, debutAuChoix,
        enJeu: table.enJeu, heros: table.heros, debut: table.debut,
        attenteDepuis, maintenant: Date.now(),
    });
    if (quoi === "basculer") { allerAuPlateau(true); return; }
    if (quoi === "sans-toi") { await direLancementSansMoi(table.heros); return; }
    if (quoi === "proposer") { proposerDeRejoindre(); return; }
    montrerAvertissement(null);
}

function surveillerLeLancement() {
    // Un premier sondage TOUT DE SUITE : l'invité qui recharge sa page après le
    // lancement doit repartir vers sa partie sans attendre un battement.
    sonderLeLancement();
    setInterval(sonderLeLancement, 2000);
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

async function rendreCampagne(campagne) {
    const membre = (campagne.equipe || [])[siege];
    const nom = membre ? (membre.nomHeros || membre.heros) : null;
    const heroes = await catalog.heroes().catch(() => []);
    const hero = membre ? heroes.find((h) => h.id === membre.heros || h.heroCardId === membre.heros) : null;
    $("#salon-barre .steps").hidden = true;
    $("#salon-titre").textContent = t("Campagne en cours");
    $("#tb-compte").textContent = "";
    rendreScene(hero || null, { grand: nom || campagne.nom || t("Campagne en cours") });
    $("#salon-choix").replaceChildren(el("div", { class: "salon-campagne" },
        el("h2", {}, campagne.nom || t("Campagne en cours")),
        nom
            ? el("p", { class: "salon-campagne-heros" },
                el("b", {}, t("Tu tiens")), " ", nom)
            : el("p", { class: "salon-campagne-heros" },
                t("Aucun héros n’est prévu pour ce siège dans cette campagne.")),
    ));
    if (nom) {
        statut(t("L’équipe est fixée par la campagne : il n’y a rien à choisir."));
        bandeauAttente(true);
    } else {
        statut(t("Aucun héros n’est prévu pour ce siège dans cette campagne."), true);
    }
}

/* ---------------- La roue de « Partie au hasard » (08/10/2026) ----------------
   L'hôte tire et publie (`/set_roue`) ; ici on anime ce qu'on lit, et on ne
   relance que SON héros (décision 8 de .planning/todos/2026-10-08-roue-du-hasard.md).
   Quand son bandeau s'arrête, le héros tiré devient celui du siège et l'invité
   passe au choix du deck. */

const roue = {
    v: 0,
    nombre: 0,
    vus: { heros: {}, scenario: 0 },
    bandeaux: [],
    bandeauScn: null,
    bouton: null,
    animations: 0,
    actuelle: null,
    tousHeros: [],
    tousScenarios: [],
};

// LE CLIC DE LA ROUE, écrit ICI et pas importé de sons.js : ce module-là pose
// à son chargement le son de survol de toute la page, que le salon n'a jamais
// eu. Même son, même réglage partagé (`marvel-board-sons`, volume en %).
let dernierClic = -Infinity;
function clicRoue() {
    const maintenant = performance.now();
    if (maintenant - dernierClic < 45 || document.visibilityState !== "visible") return;
    dernierClic = maintenant;
    try {
        if (localStorage.getItem("marvel-board-sons") === "off") return;
        const brut = Number(localStorage.getItem("marvel-board-volume-sons") ?? 20);
        const audio = new Audio("/survol.wav");
        audio.volume = Math.min(1, Math.max(0, (Number.isFinite(brut) ? brut : 20) / 100) * 0.3);
        const p = audio.play();
        if (p && p.catch) p.catch(() => {});
    } catch (e) { /* audio indisponible : le silence suffit */ }
}

const herosDeLaRoue = () => herosTirables(roue.tousHeros, { fanmade: !!(roue.actuelle && roue.actuelle.fanmade) });
const casesHerosRoue = () => herosDeLaRoue().map(caseHeros);
const casesScnRoue = () => scenariosTirables(roue.tousScenarios, { fanmade: !!(roue.actuelle && roue.actuelle.fanmade) })
    .map(caseScenario);

function majBoutonRoue() {
    if (roue.bouton) roue.bouton.disabled = roue.animations > 0;
}

async function animerRoue(promesse) {
    roue.animations += 1;
    majBoutonRoue();
    try { return await promesse; } finally { roue.animations -= 1; majBoutonRoue(); }
}

function fermerRoue() {
    const section = $("#salon-roue");
    section.hidden = true;
    section.replaceChildren();
    roue.v = 0;
    roue.nombre = 0;
    roue.vus = { heros: {}, scenario: 0 };
    roue.bandeaux = [];
    roue.bandeauScn = null;
    roue.bouton = null;
    roue.actuelle = null;
}

function construireRoue(nombre) {
    roue.nombre = nombre;
    roue.bandeaux = Array.from({ length: nombre }, () => creerBandeau({ surClic: clicRoue }));
    roue.bandeauScn = creerBandeau({ surClic: clicRoue });
    roue.bouton = el("button", { class: "salon-roue-bouton", onclick: relancerMonHeros }, t("Relancer mon héros"));
    const ligne = (titre, bandeau, extra, moi) => el("div", { class: "roue-ligne" + (moi ? " est-moi" : "") },
        el("b", { class: "roue-titre" }, titre), bandeau.element, extra || el("span"));
    $("#salon-roue").replaceChildren(
        el("h2", {}, t("Partie au hasard")),
        el("p", { class: "roue-aide" }, t("L’hôte lance la roue : ton héros est tiré au sort.")),
        ...roue.bandeaux.map((b, p) => ligne(`${t("Joueur")} ${p + 1}`, b, p === siege ? roue.bouton : null, p === siege)),
        ligne(t("Scénario"), roue.bandeauScn, null, false),
    );
    $("#salon-roue").hidden = false;
}

async function monHerosTire(heroId) {
    const hero = roue.tousHeros.find((h) => h.id === heroId);
    if (!hero) return;
    if (!etat.hero || etat.hero.id !== hero.id) {
        etat.hero = hero;
        etat.deckChoisi = null;
        bandeauAttente(false);
    }
    statut(t("La roue t’a donné ce héros : choisis ton deck."));
    await rendreDecks();
}

async function sonderRoue() {
    if (sansChoix || document.hidden) return;
    const lue = await lireRoue();
    if (!lue) {
        if (roue.nombre) fermerRoue();
        return;
    }
    if (lue.v === roue.v) return;
    if (!Number.isInteger(lue.nombre) || siege >= lue.nombre) return;
    roue.v = lue.v;
    roue.actuelle = lue;
    if (!roue.tousHeros.length) {
        const [h, s] = await Promise.all([catalog.heroes(), catalog.tousLesScenarios()]);
        roue.tousHeros = h;
        roue.tousScenarios = s;
    }
    if (roue.nombre !== lue.nombre) construireRoue(lue.nombre);
    // Les bandeaux s'arrêtent l'un après l'autre, comme chez l'hôte.
    const attentes = [];
    for (let p = 0; p < lue.nombre; p++) {
        const e = (lue.heros || {})[String(p)];
        if (!e || e.n === roue.vus.heros[String(p)]) continue;
        const premier = roue.vus.heros[String(p)] === undefined;
        roue.vus.heros[String(p)] = e.n;
        const hero = roue.tousHeros.find((h) => h.id === e.id);
        if (!hero) continue;
        const fin = animerRoue(roue.bandeaux[p].tourner(casesHerosRoue(), caseHeros(hero), premier ? 2600 + 400 * p : 2600));
        if (p === siege) attentes.push(fin.then(() => monHerosTire(e.id)));
    }
    const s = lue.scenario;
    if (s && s.n !== roue.vus.scenario) {
        const premier = !roue.vus.scenario;
        roue.vus.scenario = s.n;
        const sc = roue.tousScenarios.find((x) => x.id === s.id);
        if (sc) void animerRoue(roue.bandeauScn.tourner(casesScnRoue(), caseScenario(sc), premier ? 2600 + 400 * lue.nombre : 2600));
    }
    await Promise.all(attentes);
}

async function relancerMonHeros() {
    if (!roue.actuelle || roue.animations) return;
    const autres = Object.entries(roue.actuelle.heros || {})
        .filter(([p]) => Number(p) !== siege).map(([, e]) => e.id);
    const moi = (roue.actuelle.heros || {})[String(siege)];
    const pool = herosDeLaRoue();
    const h = tirer(pool, { exclus: moi ? [...autres, moi.id] : autres }) || tirer(pool, { exclus: autres });
    if (!h) return;
    roue.bouton.disabled = true;
    const ok = await publierRoue({ quoi: "heros", p: siege, id: h.id });
    if (!ok) {
        statut(t("Choix refusé par le serveur."), true);
        majBoutonRoue();
        return;
    }
    await sonderRoue();
}

function boucleRoue() {
    // Vite quand une roue est ouverte (on veut voir les relances), lentement
    // sinon : la plupart des parties n'en ont pas.
    const suivant = () => setTimeout(boucleRoue, roue.nombre ? 1000 : 2000);
    sonderRoue().then(suivant, suivant);
}

/* ---------------- Démarrage ---------------- */

async function reprendreChoixExistant() {
    // ⚠ LA MÉMOIRE DE CE NAVIGATEUR A DÉJÀ ÉTÉ RELUE par `demarrer`, et elle
    // est la SEULE trace qui survive au lancement : `/new` vide `choix_sieges`
    // côté serveur — et c'est voulu, sans quoi la partie suivante repartirait
    // avec les choix de la précédente. Ici on ne fait que compléter ce que le
    // serveur sait encore. Voir bascule.js.
    try {
        const reponse = await fetch("get_choix_sieges?");
        const brut = await reponse.json();
        const dejaChoisi = (brut.sieges || {})[String(siege)];
        // Le serveur a encore le choix : c'est lui qui fait foi sur le HÉROS.
        // ⚠ MAIS PAS SUR LE REPÈRE, qu'il ne connaît pas : celui de la mémoire
        // reste le bon, puisqu'il date du moment où ce choix a été fait.
        if (dejaChoisi) monChoix = String(dejaChoisi.hero_card_id || "");
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

/** La manche d'avant : héros et deck pré-cochés, rien n'est envoyé. L'invité
 *  confirme d'un clic sur « Je suis prêt », ou change. */
async function reprendreDernierChoix() {
    const dernier = relireDernierChoix(window.localStorage, siege, Date.now());
    if (!dernier) return;
    try {
        const heroes = await catalog.heroes();
        const hero = heroes.find((h) => h.heroCardId === dernier.heros);
        if (!hero) return;
        const decks = await catalog.decksForHero(hero);
        const deck = decks.find((d) => d.id === dernier.deck);
        if (!deck) return;
        etat.hero = hero;
        etat.propose = deck;
        statut(t("Ton héros et ton deck de la partie d’avant sont prêts : clique sur « Je suis prêt », ou change."));
    } catch (e) {
        /* catalogue indisponible : on repart de la grille */
    }
}

async function demarrer() {
    construireBarre();
    if (!Number.isInteger(siege) || siege < 0) {
        statut(t("Ouvre ton lien personnel : c’est lui qui réserve ton siège."), true);
        return;
    }
    // Libellé affiché = index technique + 1. Voir salon-etat.js.
    $("#salon-entete").textContent = `${t("Tu es le")} ${t("Joueur")} ${siege + 1}`;
    // ⚠ ET LE TITRE DE L'ONGLET AUSSI. Il etait le dernier texte francais en
    // dur de cet ecran : tout le corps etait deja retraduit ici, le `<title>`
    // ne l'etait pas. Un invite anglophone lisait « choisis ton heros » dans
    // son onglet pendant que la page, elle, parlait anglais.
    document.title = t("Marvel Champions — choisis ton héros");

    // ⚠ LE REPÈRE SE RELIT ICI, AVANT TOUT LE RESTE, CAMPAGNE COMPRISE
    // (ronde 2 du 21/09/2026). Il était relu dans `reprendreChoixExistant`, où
    // la branche campagne ne passe jamais : le repère de campagne était donc
    // écrit et jamais relu, et un invité de campagne qui rechargeait sa page
    // après le lancement ne basculait pas — il attendait, puis devait cliquer.
    const memoire = relireRepere(window.localStorage, siege, Date.now());
    if (memoire) {
        monChoix = memoire.heros;
        debutAuChoix = memoire.debut;
    }

    // La campagne ensuite : s'il y en a une, il n'y a aucun choix a reprendre
    // ni a proposer, et `reprendreChoixExistant` n'aurait rien a trouver.
    const campagne = await campagneEnCours();
    if (campagne) {
        // ⚠ LA CAMPAGNE PASSE PAR LA MEME REGLE, et c'est la correction du
        // 21/09. Elle gardait l'ancien signal — « une partie tourne, j'y vais »
        // — donc le defaut du 20/09 entier. Et le heros ne pouvait pas l'en
        // sortir : l'equipe est fixee par le livret, le siege N tient TOUJOURS
        // le meme heros, donc comparer les heros aurait GARANTI la bascule
        // immediate sur la manche precedente. Seule la fraicheur tranche ici,
        // et elle y suffit : la question est « une partie a-t-elle demarre
        // depuis que je suis arrive ? ».
        sansChoix = true;
        await rendreCampagne(campagne);
        surveillerLeLancement();
        return;
    }

    statut(t("Choisis ton héros, puis ton deck. L’hôte lancera quand tout le monde aura choisi."));

    await reprendreChoixExistant();
    if (!etat.deckChoisi) await reprendreDernierChoix();
    if (!etat.deckChoisi) bandeauAttente(false);
    if (etat.hero) await rendreDecks();
    else await rendreHeros();

    surveillerLeLancement();
    setInterval(sonderEquipe, 2000);
    boucleRoue();
}

demarrer();
