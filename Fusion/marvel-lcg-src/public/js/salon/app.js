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
import { demanderForcage } from "/public/js/prepare/deck-force.js";
import {
    decisionSalon, memoriserRepere, relireRepere, oublierRepere,
} from "/public/js/salon/bascule.js";

const siege = Number(new URLSearchParams(location.search).get("p") ?? "-1");

const etat = { hero: null, deckChoisi: null };

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
    monChoix = etat.hero.heroCardId;
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
