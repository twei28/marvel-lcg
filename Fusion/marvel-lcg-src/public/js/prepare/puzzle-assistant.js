// puzzle-assistant.js : l'ASSISTANT de création de puzzle (E5, docs/puzzle/PLAN.md).
//
// Une modale ORANGE plein écran, un écran par étape, barre de progression, Retour / Passer /
// Suivant. Toute étape est facultative : le brouillon (puzzle-brouillon.js) part avec des valeurs
// par défaut raisonnables. Le bouton « Tester » envoie le puzzle au moteur (/new_puzzle) puis
// ouvre le plateau.
//
// Ouvert depuis le panneau « Puzzles » (puzzles.js), débranché du site jusqu'à la livraison.
"use strict";
import { api, cardImageUrl, fileName } from "/public/js/prepare/api.js?v=dfcc19da";
import { cards } from "/public/js/prepare/cards.js";
import { catalog } from "/public/js/prepare/catalog.js";
import { t } from "/public/js/prepare/langue.js";
import { brouillonVide, brouillonVersPuzzle, erreursDuBrouillon, joueurVide } from "/public/js/prepare/puzzle-brouillon.js";

const ORANGE = "#f08a24";

function el(tag, attrs, ...enfants) {
    const noeud = document.createElement(tag);
    for (const [cle, valeur] of Object.entries(attrs || {})) {
        if (cle.startsWith("on")) noeud.addEventListener(cle.slice(2), valeur);
        else if (cle === "style") noeud.style.cssText = valeur;
        else if (valeur !== false && valeur !== null && valeur !== undefined) noeud.setAttribute(cle, valeur === true ? "" : valeur);
    }
    for (const enfant of enfants.flat()) {
        if (enfant == null || enfant === false) continue;
        noeud.append(enfant.nodeType ? enfant : document.createTextNode(String(enfant)));
    }
    return noeud;
}

const style = document.createElement("style");
style.textContent = `
  .pa-fond { position: fixed; inset: 0; z-index: 960; background: rgba(12,6,0,.9); display: flex;
    align-items: stretch; justify-content: center; color: #f3e3d0; font-family: inherit; }
  .pa-boite { width: min(980px, 100vw); display: flex; flex-direction: column; background: #1d1208;
    border-left: 2px solid ${ORANGE}; border-right: 2px solid ${ORANGE}; }
  .pa-tete { padding: 14px 20px 10px; border-bottom: 1px solid #5a3510; }
  .pa-titre { margin: 0 0 8px; font-size: 1.15rem; color: ${ORANGE}; }
  .pa-barre { display: flex; gap: 4px; }
  .pa-barre span { flex: 1; height: 6px; border-radius: 3px; background: #4a2d10; }
  .pa-barre span.fait { background: ${ORANGE}; }
  .pa-barre span.ici { background: #ffc27a; }
  .pa-corps { flex: 1; overflow: auto; padding: 18px 20px; }
  .pa-corps h3 { margin: 0 0 4px; color: #fff; }
  .pa-aide { margin: 0 0 14px; color: #c9a77c; font-size: .85rem; }
  .pa-pied { display: flex; gap: 10px; padding: 12px 20px; border-top: 1px solid #5a3510; align-items: center; }
  .pa-pied .espace { flex: 1; }
  .pa-bouton { padding: 9px 18px; border-radius: 8px; border: 1px solid ${ORANGE}; background: #2e1b08;
    color: #ffd9aa; font-weight: 700; cursor: pointer; }
  .pa-bouton:hover { background: #4a2a0c; }
  .pa-bouton.principal { background: ${ORANGE}; color: #1d1208; }
  .pa-bouton.discret { border-color: #6b4a26; color: #c9a77c; font-weight: 400; }
  .pa-bouton[disabled] { opacity: .45; cursor: default; }
  .pa-choix { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .pa-choix button { padding: 8px 16px; border-radius: 8px; border: 1px solid #6b4a26; background: #2a1a0a;
    color: #f3e3d0; cursor: pointer; }
  .pa-choix button.actif { border-color: ${ORANGE}; background: #5a3310; color: #fff; }
  .pa-recherche { width: 100%; box-sizing: border-box; padding: 8px 10px; margin-bottom: 10px; border-radius: 8px;
    border: 1px solid #6b4a26; background: #120a03; color: #f3e3d0; }
  .pa-grille { display: grid; grid-template-columns: repeat(auto-fill, minmax(104px, 1fr)); gap: 10px; }
  .pa-carte { border: 2px solid transparent; border-radius: 10px; padding: 4px; background: #2a1a0a; cursor: pointer;
    text-align: center; font-size: .78rem; color: #e8d2b4; }
  .pa-carte img { width: 100%; aspect-ratio: 5 / 7; object-fit: cover; border-radius: 6px; background: #3a2410; }
  .pa-carte.actif { border-color: ${ORANGE}; }
  .pa-heros { border: 1px solid #5a3510; border-radius: 10px; padding: 12px; margin-bottom: 14px; }
  .pa-heros h4 { margin: 0 0 8px; color: ${ORANGE}; }
  .pa-champ { display: grid; gap: 4px; margin-bottom: 12px; }
  .pa-champ label { color: #c9a77c; font-size: .85rem; }
  .pa-champ input[type=range] { width: 100%; accent-color: ${ORANGE}; }
  .pa-erreurs { color: #ff9a8a; font-size: .85rem; margin: 0; padding-left: 18px; }
  .pa-onglets { display: flex; gap: 6px; margin-bottom: 12px; flex-wrap: wrap; }
  .pa-zones { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px; }
  .pa-zone { border: 1px solid #5a3510; border-radius: 10px; padding: 8px; min-height: 80px; }
  .pa-zone h4 { margin: 0 0 6px; color: ${ORANGE}; font-size: .9rem; display: flex; justify-content: space-between; align-items: center; }
  .pa-ligne { display: flex; gap: 6px; align-items: center; padding: 3px 0; font-size: .8rem; border-bottom: 1px solid #2f1d0b; }
  .pa-ligne img { width: 28px; height: 39px; object-fit: cover; border-radius: 3px; background: #3a2410; flex: none; }
  .pa-ligne .nom { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .pa-mini { padding: 2px 7px; border-radius: 6px; border: 1px solid #6b4a26; background: #2a1a0a; color: #ffd9aa; cursor: pointer; font-size: .75rem; }
  .pa-mini:hover { background: #4a2a0c; }
  .pa-mini.actif { background: ${ORANGE}; color: #1d1208; border-color: ${ORANGE}; }
  .pa-resultats { display: grid; grid-template-columns: repeat(auto-fill, minmax(92px, 1fr)); gap: 8px; max-height: 260px; overflow: auto; margin-bottom: 14px; }
  .pa-etat { border: 1px solid #5a3510; border-radius: 10px; padding: 8px 10px; margin-bottom: 10px; display: flex; gap: 10px; align-items: flex-start; }
  .pa-etat img { width: 56px; aspect-ratio: 5 / 7; object-fit: cover; border-radius: 5px; flex: none; }
  .pa-etat .corps { flex: 1; display: grid; gap: 6px; }
  .pa-etat .rangee { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; font-size: .8rem; color: #c9a77c; }
  .pa-texte { width: 100%; box-sizing: border-box; padding: 8px 10px; border-radius: 8px; border: 1px solid #6b4a26; background: #120a03; color: #f3e3d0; font: inherit; }
  textarea.pa-texte { min-height: 110px; resize: vertical; }
  @media (max-width: 720px) { .pa-zones { grid-template-columns: 1fr; } }
`;
document.head.append(style);

// ------------------------------------------------------------------ données
async function chargerDonnees() {
    await cards.load();
    const [heros, extensions] = await Promise.all([catalog.heroes(), catalog.extensions()]);
    return { heros, extensions };
}

/** Le deck de départ d'un héros : cartes de signature + moitié d'aspect, la main de départ en tête. */
export function deckParDefaut(hero) {
    const d = hero.deck || {};
    const toutes = [...(d.hero_deck || []), ...(d.player_deck || [])];
    const taille = Number(hero.handSize) || 5;
    return { main: toutes.slice(0, taille), deck: toutes.slice(taille) };
}

/** Le deck de rencontre d'un scénario : ses cartes propres + celles de ses sets, dans l'ordre listé. */
export async function rencontreDuScenario(scenario) {
    const cartes = [...(scenario.encounters || [])];
    const sets = [...(scenario.encounter_sets || []), ...(scenario.modular_sets || [])];
    for (const nom of sets) {
        try { cartes.push(...((await api.encounterSet(nom)).encounters || [])); } catch (e) { /* set absent : on continue */ }
    }
    return cartes;
}

function choisirHeros(brouillon, siege, hero) {
    const joueur = brouillon.players[siege];
    const { main, deck } = deckParDefaut(hero);
    // Départ en alter-ego (seconde face de l'entrée « recto,verso »), comme les puzzles officiels.
    joueur.identity = String(hero.deck.hero[0]).split(",").pop();
    joueur.heroId = hero.id;
    joueur.deckName = hero.name;
    joueur.hand = main;
    joueur.deck = deck;
}

// ------------------------------------------------------------------ étapes
// Chaque étape rend un noeud et lit / écrit `ctx.brouillon`. `redessiner` refait l'écran.
const ETAPES = [
    {
        titre: "Qui joue ?",
        aide: "Combien de héros, et lesquels. Leur deck de départ est proposé : tu le changeras plus loin.",
        rendre(ctx) {
            const b = ctx.brouillon;
            const nombre = el("div", { class: "pa-choix" }, [1, 2, 3, 4].map((n) =>
                el("button", {
                    class: b.players.length === n ? "actif" : "",
                    onclick: () => {
                        while (b.players.length < n) b.players.push(joueurVide());
                        b.players.length = n;
                        ctx.redessiner();
                    },
                }, n === 1 ? t("1 héros") : `${n} ${t("héros")}`)));
            const blocs = b.players.map((joueur, siege) => {
                const recherche = el("input", { class: "pa-recherche", placeholder: t("Chercher un héros..."), type: "search" });
                const grille = el("div", { class: "pa-grille" });
                const remplir = () => {
                    const q = recherche.value.trim().toLowerCase();
                    const liste = ctx.donnees.heros.filter((h) => !q || h.name.toLowerCase().includes(q)).slice(0, 60);
                    grille.replaceChildren(...liste.map((h) => el("div", {
                        class: "pa-carte" + (joueur.heroId === h.id ? " actif" : ""),
                        onclick: () => { choisirHeros(b, siege, h); ctx.redessiner(); },
                    }, el("img", { src: cardImageUrl(h.heroCardId), alt: h.name, loading: "lazy" }), h.name)));
                };
                recherche.addEventListener("input", remplir);
                remplir();
                return el("div", { class: "pa-heros" },
                    el("h4", {}, `${t("Héros")} ${siege + 1}${joueur.deckName ? " : " + joueur.deckName : ""}`),
                    recherche, grille);
            });
            return el("div", {}, nombre, blocs);
        },
    },
    {
        titre: "L'ennemi",
        aide: "Le méchant et son scénario. Les cartes de rencontre du scénario sont ajoutées au deck de rencontre.",
        rendre(ctx) {
            const b = ctx.brouillon;
            const mode = el("div", { class: "pa-choix" },
                [[false, "Standard"], [true, "Expert"]].map(([expert, nom]) => el("button", {
                    class: b.expert === expert ? "actif" : "",
                    onclick: () => { b.expert = expert; ctx.redessiner(); },
                }, nom)));
            const recherche = el("input", { class: "pa-recherche", placeholder: t("Chercher un scénario..."), type: "search" });
            const grille = el("div", { class: "pa-grille" });
            const scenarios = ctx.donnees.extensions.flatMap((e) => e.scenarios.map((s) => fileName(s)))
                .filter((n, i, tous) => !/_expert$/.test(n) && tous.indexOf(n) === i);
            const remplir = () => {
                const q = recherche.value.trim().toLowerCase();
                grille.replaceChildren(...scenarios.filter((n) => !q || n.toLowerCase().includes(q)).slice(0, 80).map((nom) =>
                    el("div", {
                        class: "pa-carte" + (b.scenario === nom ? " actif" : ""),
                        onclick: async () => {
                            const sc = await api.scenario(b.expert && scenarios.includes(nom + "_expert") ? nom + "_expert" : nom);
                            b.scenario = nom;
                            b.villain = sc.villain || [];
                            b.schemes = sc.schemes || [];
                            b.setAside = sc.set_aside || [];
                            b.encounterDeck = await rencontreDuScenario(sc);
                            b.villainStage = 0;
                            b.schemeStage = 0;
                            ctx.redessiner();
                        },
                    }, el("img", { src: ctx.imageMechant(nom), alt: nom, loading: "lazy" }), nom.replace(/_/g, " "))));
            };
            recherche.addEventListener("input", remplir);
            remplir();
            return el("div", {}, mode, recherche, grille);
        },
    },
    {
        titre: "L'état de la menace",
        aide: "Où en est le méchant, et où en est son complot. Laisse tel quel pour une partie qui commence.",
        rendre(ctx) {
            const b = ctx.brouillon;
            if (!b.villain.length) return el("p", { class: "pa-aide" }, t("Choisis d'abord un méchant (étape précédente)."));
            const fiche = cards.get(b.villain[b.villainStage || 0]);
            // « 14* » : 14 par joueur ; sans astérisque, valeur fixe.
            const brut = String((fiche && (fiche.hp ?? (fiche.desc && fiche.desc.HP))) ?? "");
            const pvMax = (parseInt(brut, 10) || 20) * (brut.includes("*") ? b.players.length : 1);
            const pv = b.villainState.health ?? pvMax;
            const sortiePv = el("strong", {}, `${pv} / ${pvMax}`);
            const curseurPv = el("input", {
                type: "range", min: 1, max: pvMax, value: pv,
                oninput: (e) => { b.villainState.health = Number(e.target.value); if (b.villainState.health === pvMax) delete b.villainState.health; sortiePv.textContent = `${e.target.value} / ${pvMax}`; },
            });
            const menace = b.schemeState.threat ?? 0;
            const sortieMenace = el("strong", {}, String(menace));
            const curseurMenace = el("input", {
                type: "range", min: 0, max: 40, value: menace,
                oninput: (e) => { b.schemeState.threat = Number(e.target.value) || undefined; sortieMenace.textContent = e.target.value; },
            });
            const stade = (cle, liste, libelle) => liste.length > 1 && el("div", { class: "pa-champ" },
                el("label", {}, libelle),
                el("div", { class: "pa-choix" }, liste.map((_, i) => el("button", {
                    class: (b[cle] || 0) === i ? "actif" : "",
                    onclick: () => { b[cle] = i; if (cle === "villainStage") delete b.villainState.health; ctx.redessiner(); },
                }, `${t("Stade")} ${i + 1}`))));
            return el("div", {},
                stade("villainStage", b.villain, t("Stade du méchant")),
                el("div", { class: "pa-champ" }, el("label", {}, t("Points de vie du méchant")), curseurPv, sortiePv),
                stade("schemeStage", b.schemes, t("Stade du complot principal")),
                el("div", { class: "pa-champ" }, el("label", {}, t("Menace sur le complot principal")), curseurMenace, sortieMenace));
        },
    },
];


// ------------------------------------------------------------------ outils d'écran
const TYPES_PAR_GENRE = {
    ally: ["Ally"], support: ["Support"], minion: ["Minion"], side_scheme: ["SideScheme"],
    environment: ["Environment"], upgrade: ["Upgrade", "Attachment"],
};
const NOM_GENRE = {
    ally: "Allié", support: "Soutien", minion: "Sbire", side_scheme: "Complot annexe",
    environment: "Environnement", upgrade: "Amélioration",
};

function nomCarte(id) {
    const c = cards.get(id);
    return c && c.name ? String(c.name).replace(/^\*\s*/, "") : String(id);
}

/** Cartes du catalogue dont le nom contient `q`, limitées aux `types` (ou toutes). */
function chercherCartes(q, types, limite = 60) {
    const texte = q.trim().toLowerCase();
    const vus = new Set();
    const trouvees = [];
    for (const c of cards.all()) {
        if (types && !types.includes(c.type)) continue;
        if (!c.name || c.name === "not implemented" || /^(rule_|minion$)/.test(c.card_id)) continue;
        if (texte && !String(c.name).toLowerCase().includes(texte)) continue;
        if (vus.has(c.card_id)) continue;
        vus.add(c.card_id);
        trouvees.push(c);
        if (trouvees.length >= limite) break;
    }
    return trouvees;
}

/** Une recherche de carte : champ + résultats cliquables. `surChoix(carte)`. */
function selecteurCarte(types, surChoix, invite) {
    const champ = el("input", { class: "pa-recherche", type: "search", placeholder: invite || t("Chercher une carte...") });
    const zone = el("div", { class: "pa-resultats" });
    const remplir = () => {
        if (!champ.value.trim()) { zone.replaceChildren(el("span", { class: "pa-aide" }, t("Tape un nom pour chercher."))); return; }
        zone.replaceChildren(...chercherCartes(champ.value, types).map((c) => el("div", {
            class: "pa-carte", onclick: () => surChoix(c),
        }, el("img", { src: cardImageUrl(c.card_id), alt: c.name, loading: "lazy" }), String(c.name).replace(/^\*\s*/, ""))));
    };
    champ.addEventListener("input", remplir);
    remplir();
    return el("div", {}, champ, zone);
}

function pas(valeur, min, max, change) {
    const sortie = el("strong", { style: "min-width:2ch;text-align:center" }, String(valeur));
    const maj = (v) => { const n = Math.max(min, Math.min(max, v)); sortie.textContent = String(n); change(n); valeur = n; };
    return el("span", { class: "rangee" },
        el("button", { class: "pa-mini", onclick: () => maj(valeur - 1) }, "−"), sortie,
        el("button", { class: "pa-mini", onclick: () => maj(valeur + 1) }, "+"));
}

function melanger(liste) {
    for (let i = liste.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [liste[i], liste[j]] = [liste[j], liste[i]];
    }
}

function ongletsHeros(ctx, cle) {
    const b = ctx.brouillon;
    if (b.players.length < 2) return null;
    return el("div", { class: "pa-onglets" }, b.players.map((j, i) => el("button", {
        class: "pa-mini" + ((ctx[cle] || 0) === i ? " actif" : ""),
        onclick: () => { ctx[cle] = i; ctx.redessiner(); },
    }, `${t("Héros")} ${i + 1}${j.deckName ? " : " + j.deckName : ""}`)));
}

/** PV maximum d'une carte du catalogue (« 3 », « 14* » = par joueur). */
function pvMax(id, nbJoueurs) {
    const c = cards.get(id);
    const brut = String((c && (c.hp ?? (c.desc && c.desc.HP))) ?? "");
    const n = parseInt(brut, 10);
    return Number.isFinite(n) ? n * (brut.includes("*") ? nbJoueurs : 1) : 0;
}

// ------------------------------------------------------------------ étapes 4 à 9
const ZONES = [["hand", "Main"], ["deck", "Deck (dessus en premier)"], ["discard", "Défausse"]];

function etapeCartes(ctx) {
    const b = ctx.brouillon;
    const siege = Math.min(ctx.siegeCartes || 0, b.players.length - 1);
    const joueur = b.players[siege];
    if (!joueur.identity) return el("p", { class: "pa-aide" }, t("Choisis d'abord un héros (étape 1)."));
    ctx.zoneAjout = ctx.zoneAjout || "hand";
    const colonnes = ZONES.map(([cle, nom]) => {
        const liste = joueur[cle];
        const lignes = liste.map((id, i) => el("div", { class: "pa-ligne" },
            el("img", { src: cardImageUrl(id), alt: "" }),
            el("span", { class: "nom", title: nomCarte(id) }, nomCarte(id)),
            cle !== "hand" && el("button", { class: "pa-mini", title: t("Monter"), onclick: () => { if (i) { [liste[i - 1], liste[i]] = [liste[i], liste[i - 1]]; ctx.redessiner(); } } }, "▲"),
            cle !== "hand" && el("button", { class: "pa-mini", title: t("Descendre"), onclick: () => { if (i < liste.length - 1) { [liste[i + 1], liste[i]] = [liste[i], liste[i + 1]]; ctx.redessiner(); } } }, "▼"),
            el("select", { class: "pa-mini", title: t("Déplacer vers"), onchange: (e) => {
                if (!e.target.value) return;
                liste.splice(i, 1);
                joueur[e.target.value].push(id);
                ctx.redessiner();
            } }, el("option", { value: "" }, "→"), ZONES.filter(([z]) => z !== cle).map(([z, n]) => el("option", { value: z }, t(n.split(" ")[0])))),
            el("button", { class: "pa-mini", title: t("Retirer"), onclick: () => { liste.splice(i, 1); ctx.redessiner(); } }, "✕")));
        return el("div", { class: "pa-zone" },
            el("h4", {}, `${t(nom)} · ${liste.length}`,
                cle === "deck" && el("button", { class: "pa-mini", onclick: () => { melanger(liste); ctx.redessiner(); } }, t("Mélanger"))),
            lignes);
    });
    const cible = el("div", { class: "pa-onglets" }, el("span", { class: "pa-aide", style: "margin:0" }, t("Ajouter à :")),
        ZONES.map(([cle, nom]) => el("button", { class: "pa-mini" + (ctx.zoneAjout === cle ? " actif" : ""), onclick: () => { ctx.zoneAjout = cle; ctx.redessiner(); } }, t(nom.split(" ")[0]))));
    return el("div", {}, ongletsHeros(ctx, "siegeCartes"), el("div", { class: "pa-zones" }, colonnes), cible,
        selecteurCarte(null, (c) => { joueur[ctx.zoneAjout].push(c.card_id); ctx.redessiner(); }));
}

function etapeEnJeu(ctx) {
    const b = ctx.brouillon;
    ctx.genreAjout = ctx.genreAjout || "ally";
    const genres = el("div", { class: "pa-onglets" }, Object.keys(NOM_GENRE).map((g) => el("button", {
        class: "pa-mini" + (ctx.genreAjout === g ? " actif" : ""), onclick: () => { ctx.genreAjout = g; ctx.redessiner(); },
    }, t(NOM_GENRE[g]))));
    const porteurs = () => [
        ...b.players.map((j, i) => ({ ref: "h" + i, nom: `${t("Héros")} ${i + 1}` })),
        { ref: "v", nom: t("Méchant") },
        ...b.enJeu.map((c, i) => ({ host: i, nom: nomCarte(c.card) })).filter((_, i) => b.enJeu[i].kind !== "upgrade"),
    ];
    const reglages = el("div", { class: "pa-onglets" });
    if (["ally", "support", "minion", "upgrade"].includes(ctx.genreAjout) && b.players.length > 1) {
        reglages.append(el("span", { class: "pa-aide", style: "margin:0" }, t("Pour le héros :")),
            ...b.players.map((_, i) => el("button", { class: "pa-mini" + ((ctx.siegeAjout || 0) === i ? " actif" : ""), onclick: () => { ctx.siegeAjout = i; ctx.redessiner(); } }, String(i + 1))));
    }
    if (ctx.genreAjout === "upgrade") {
        const options = porteurs();
        ctx.porteurAjout = Math.min(ctx.porteurAjout || 0, options.length - 1);
        reglages.append(el("span", { class: "pa-aide", style: "margin:0" }, t("Posée sur :")),
            el("select", { class: "pa-mini", onchange: (e) => { ctx.porteurAjout = Number(e.target.value); } },
                options.map((o, i) => el("option", { value: i, selected: i === ctx.porteurAjout }, o.nom))));
    }
    const ajouter = (c) => {
        const carte = { kind: ctx.genreAjout, card: c.card_id, siege: ctx.siegeAjout || 0, state: {} };
        if (carte.kind === "minion") carte.engaged = true;
        if (carte.kind === "upgrade") {
            const hote = porteurs()[ctx.porteurAjout || 0];
            if (hote.ref) carte.hostRef = hote.ref; else carte.host = hote.host;
        }
        b.enJeu.push(carte);
        ctx.redessiner();
    };
    const liste = b.enJeu.map((c, i) => el("div", { class: "pa-ligne" },
        el("img", { src: cardImageUrl(c.card), alt: "" }),
        el("span", { class: "nom" }, `${nomCarte(c.card)} · ${t(NOM_GENRE[c.kind])}${b.players.length > 1 && c.kind !== "side_scheme" && c.kind !== "environment" ? " · " + t("héros") + " " + (c.siege + 1) : ""}`),
        el("button", { class: "pa-mini", onclick: () => {
            // Retirer une carte retire aussi ses améliorations, et recale les indices des porteurs.
            const retirees = new Set([i]);
            b.enJeu.forEach((x, k) => { if (x.kind === "upgrade" && retirees.has(x.host)) retirees.add(k); });
            const recale = (k) => k - [...retirees].filter((r) => r < k).length;
            b.enJeu = b.enJeu.filter((_, k) => !retirees.has(k)).map((x) => (x.host !== undefined ? { ...x, host: recale(x.host) } : x));
            ctx.redessiner();
        } }, "✕")));
    return el("div", {}, genres, reglages, selecteurCarte(TYPES_PAR_GENRE[ctx.genreAjout], ajouter),
        el("div", { class: "pa-zone" }, el("h4", {}, `${t("Cartes en jeu")} · ${b.enJeu.length}`),
            liste.length ? liste : el("span", { class: "pa-aide" }, t("Rien pour l'instant."))));
}

const ETATS_FR = { Confused: "Désorienté", Stunned: "Sonné", Tough: "Coriace", Exposed: "Exposé", Cloaked: "Camouflé", Dazed: "Étourdi", Intensified: "Intensifié" };

function ficheEtat(ctx, { id, titre, etat, max, complot, nbEtats }) {
    const rangees = [];
    if (max) {
        const pv = etat.health ?? max;
        rangees.push(el("div", { class: "rangee" }, t("PV"), pas(pv, 0, max, (n) => { if (n >= max) delete etat.health; else etat.health = n; }), `/ ${max}`));
    }
    if (complot) {
        rangees.push(el("div", { class: "rangee" }, t("Menace"), pas(etat.threat || 0, 0, 99, (n) => { if (n) etat.threat = n; else delete etat.threat; })));
    }
    rangees.push(el("div", { class: "rangee" }, el("button", {
        class: "pa-mini" + (etat.exhausted ? " actif" : ""),
        onclick: () => { if (etat.exhausted) delete etat.exhausted; else etat.exhausted = true; ctx.redessiner(); },
    }, t("Épuisé"))));
    if (nbEtats !== false) {
        const statuses = new Map((etat.statuses || []).map(([n, v]) => [n, v]));
        rangees.push(el("div", { class: "rangee" }, ["Confused", "Stunned", "Tough", "Exposed", "Cloaked", "Dazed", "Intensified"].map((nom) =>
            el("span", { class: "rangee" }, t(ETATS_FR[nom]), pas(statuses.get(nom) || 0, 0, 5, (n) => {
                if (n) statuses.set(nom, n); else statuses.delete(nom);
                etat.statuses = [...statuses.entries()];
                if (!etat.statuses.length) delete etat.statuses;
            })))));
    }
    const compteurs = new Map((etat.counters || []).map(([n, v]) => [n, v]));
    const nom = el("input", { class: "pa-texte", style: "width:120px", placeholder: t("compteur") });
    rangees.push(el("div", { class: "rangee" }, [...compteurs.entries()].map(([n, v]) => el("span", { class: "pa-mini" }, `${n} ${v}`)),
        nom, el("button", { class: "pa-mini", onclick: () => {
            const n = nom.value.trim();
            if (!n) return;
            compteurs.set(n, (compteurs.get(n) || 0) + 1);
            etat.counters = [...compteurs.entries()];
            ctx.redessiner();
        } }, "+1"),
        compteurs.size > 0 && el("button", { class: "pa-mini", onclick: () => { delete etat.counters; ctx.redessiner(); } }, t("Vider"))));
    return el("div", { class: "pa-etat" }, el("img", { src: cardImageUrl(id), alt: "" }),
        el("div", { class: "corps" }, el("strong", {}, titre), rangees));
}

function etapeEtats(ctx) {
    const b = ctx.brouillon;
    const n = b.players.length;
    const fiches = [];
    b.players.forEach((j, i) => {
        if (j.identity) fiches.push(ficheEtat(ctx, { id: j.identity, titre: `${nomCarte(j.identity)} (${t("héros")} ${i + 1})`, etat: j.state, max: pvMax(j.identity, n) }));
    });
    if (b.villain.length) {
        const id = b.villain[b.villainStage || 0];
        fiches.push(ficheEtat(ctx, { id, titre: nomCarte(id), etat: b.villainState, max: pvMax(id, n) }));
    }
    b.enJeu.forEach((c) => {
        fiches.push(ficheEtat(ctx, {
            id: c.card, titre: nomCarte(c.card), etat: c.state, max: pvMax(c.card, n),
            complot: c.kind === "side_scheme", nbEtats: !["side_scheme", "environment", "upgrade"].includes(c.kind),
        }));
    });
    return fiches.length ? el("div", {}, fiches) : el("p", { class: "pa-aide" }, t("Rien à régler pour l'instant."));
}

function etapeObjectifs(ctx) {
    const b = ctx.brouillon;
    const a = (kind) => b.objectives.some((o) => o.kind === kind);
    const basculer = (kind, objet) => {
        if (a(kind) && kind !== "complete_scheme" && kind !== "free_text") b.objectives = b.objectives.filter((o) => o.kind !== kind);
        else b.objectives.push(objet || { kind });
        ctx.redessiner();
    };
    const lignes = [
        el("div", { class: "pa-choix" },
            el("button", { class: a("defeat_villain") ? "actif" : "", onclick: () => basculer("defeat_villain") }, t("Vaincre le méchant")),
            el("button", { class: a("survive") ? "actif" : "", onclick: () => basculer("survive") }, t("Survivre jusqu'à la fin du round"))),
    ];
    const complots = [
        ...b.schemes.slice(0, 1).map((s) => ({ id: s.split(",").pop(), nom: nomCarte(s.split(",")[0]) })),
        ...b.enJeu.filter((c) => c.kind === "side_scheme").map((c) => ({ id: c.card, nom: nomCarte(c.card) })),
    ];
    if (complots.length) {
        lignes.push(el("div", { class: "pa-champ" }, el("label", {}, t("Terminer un complot")),
            el("div", { class: "pa-choix" }, complots.map((c) => el("button", {
                class: b.objectives.some((o) => o.kind === "complete_scheme" && o.target === c.id) ? "actif" : "",
                onclick: () => {
                    const present = b.objectives.some((o) => o.kind === "complete_scheme" && o.target === c.id);
                    b.objectives = present ? b.objectives.filter((o) => !(o.kind === "complete_scheme" && o.target === c.id))
                        : [...b.objectives, { kind: "complete_scheme", target: c.id }];
                    ctx.redessiner();
                },
            }, c.nom)))));
    }
    const libre = el("input", { class: "pa-texte", placeholder: t("Objectif libre, par exemple : finir sans dégât sur Peter") });
    lignes.push(el("div", { class: "pa-champ" }, el("label", {}, t("Objectif libre (tu le valides à la main en jouant)")), libre,
        el("button", { class: "pa-mini", style: "justify-self:start", onclick: () => { if (libre.value.trim()) { b.objectives.push({ kind: "free_text", text: libre.value.trim() }); ctx.redessiner(); } } }, t("Ajouter"))));
    const mode = el("div", { class: "pa-choix" }, [["all", "Tous requis"], ["any", "Un seul suffit"]].map(([v, nom]) => el("button", {
        class: b.objectivesMode === v ? "actif" : "", onclick: () => { b.objectivesMode = v; ctx.redessiner(); } }, t(nom))));
    const liste = b.objectives.map((o, i) => el("div", { class: "pa-ligne" },
        el("span", { class: "nom" }, o.text || ({ defeat_villain: t("Vaincre le méchant"), survive: t("Survivre jusqu'à la fin du round"), complete_scheme: `${t("Terminer le complot")} ${nomCarte(o.target)}` })[o.kind]),
        el("button", { class: "pa-mini", onclick: () => { b.objectives.splice(i, 1); ctx.redessiner(); } }, "✕")));
    return el("div", {}, ...lignes, b.objectives.length > 1 && mode, el("div", { class: "pa-zone" }, el("h4", {}, t("Objectifs choisis")),
        liste.length ? liste : el("span", { class: "pa-aide" }, t("Aucun : le puzzle finit comme une partie normale."))));
}

function etapePresentation(ctx) {
    const b = ctx.brouillon;
    const titre = el("input", { class: "pa-texte", maxlength: 80, value: b.title, placeholder: t("Titre du puzzle"),
        oninput: (e) => { b.title = e.target.value; } });
    const histoire = el("textarea", { class: "pa-texte", maxlength: 2000, placeholder: t("L'histoire, l'énoncé : ce que le joueur doit savoir."),
        oninput: (e) => { b.description = e.target.value; } }, b.description);
    const etoiles = el("div", { class: "pa-choix" }, [0, 1, 2, 3, 4, 5].map((n) => el("button", {
        class: b.difficulty === n ? "actif" : "", onclick: () => { b.difficulty = n; ctx.redessiner(); } }, n ? "★".repeat(n) : t("Non précisée"))));
    const indice = el("input", { class: "pa-texte", maxlength: 500, placeholder: t("Un indice (dévoilé au besoin)") });
    const indices = b.hints.map((h, i) => el("div", { class: "pa-ligne" }, el("span", { class: "nom" }, h),
        el("button", { class: "pa-mini", onclick: () => { b.hints.splice(i, 1); ctx.redessiner(); } }, "✕")));
    const blocs = [
        el("div", { class: "pa-champ" }, el("label", {}, t("Titre")), titre),
        el("div", { class: "pa-champ" }, el("label", {}, t("Histoire")), histoire),
        el("div", { class: "pa-champ" }, el("label", {}, t("Difficulté")), etoiles),
        el("div", { class: "pa-champ" }, el("label", {}, t("Indices")), indices, indice,
            el("button", { class: "pa-mini", style: "justify-self:start", onclick: () => { if (indice.value.trim() && b.hints.length < 10) { b.hints.push(indice.value.trim()); ctx.redessiner(); } } }, t("Ajouter un indice"))),
    ];
    if (b.players.length > 1) {
        blocs.push(el("div", { class: "pa-champ" }, el("label", {}, t("Premier joueur")),
            el("div", { class: "pa-choix" }, b.players.map((_, i) => el("button", {
                class: b.firstPlayer === i ? "actif" : "", onclick: () => { b.firstPlayer = i; ctx.redessiner(); } }, `${t("Héros")} ${i + 1}`)))));
    }
    blocs.push(el("div", { class: "pa-champ" }, el("label", {}, t("Le puzzle commence...")),
        el("div", { class: "pa-choix" }, [["", "au début de la phase joueur"], ["villain", "à la phase du méchant"], ["end_round", "à la fin du round"]].map(([v, nom]) => el("button", {
            class: (b.startPhase || "") === v ? "actif" : "", onclick: () => { b.startPhase = v; ctx.redessiner(); } }, t(nom))))));
    return el("div", {}, ...blocs);
}

ETAPES.push(
    { titre: "Les cartes des héros", aide: "La main, le deck (dessus en premier) et la défausse de chaque héros. Ajoute des cartes par recherche, change leur ordre avec les flèches.", rendre: etapeCartes },
    { titre: "Ce qui est en jeu", aide: "Alliés, soutiens, améliorations, sbires engagés, complots annexes, environnement déjà posés sur la table.", rendre: etapeEnJeu },
    { titre: "Les états", aide: "Les points de vie, les cartes d'état, les compteurs et l'épuisement de chaque carte.", rendre: etapeEtats },
    { titre: "L'objectif", aide: "Ce qu'il faut réussir. Laisse vide pour une partie normale.", rendre: etapeObjectifs },
    { titre: "Présentation et test", aide: "Le titre, l'histoire, la difficulté et le moment de départ. Puis teste ton puzzle.", rendre: etapePresentation },
);

// ------------------------------------------------------------------ brouillon enregistré
// Le brouillon est gardé dans le navigateur à chaque étape (jamais envoyé nulle part). Tout accès
// est protégé : le stockage peut être vide, bloqué ou refuser d'écrire.
const CLE_BROUILLON = "mc-puzzle-brouillon";
function lireBrouillonEnregistre() {
    try {
        const brut = localStorage.getItem(CLE_BROUILLON);
        const donnees = brut ? JSON.parse(brut) : null;
        return donnees && donnees.brouillon && Array.isArray(donnees.brouillon.players) ? donnees : null;
    } catch (e) { return null; }
}
function enregistrerBrouillon(brouillon, etape) {
    try { localStorage.setItem(CLE_BROUILLON, JSON.stringify({ brouillon, etape })); } catch (e) { /* tant pis */ }
}
function oublierBrouillon() {
    try { localStorage.removeItem(CLE_BROUILLON); } catch (e) { /* rien */ }
}

// ------------------------------------------------------------------ ouverture
export async function ouvrirAssistant() {
    document.querySelector(".pa-fond")?.remove();
    const ctx = {
        brouillon: brouillonVide(), donnees: null, etape: 0,
        // Illustration d'un scénario : la carte de son premier méchant.
        imageMechant: (nom) => {
            const id = ctx.villainDe?.[nom];
            return id ? cardImageUrl(id) : "";
        },
        redessiner: () => dessiner(),
    };
    const corps = el("div", { class: "pa-corps" }, t("Chargement..."));
    const barre = el("div", { class: "pa-barre" });
    const sous = el("p", { class: "pa-aide" });
    const titre = el("h2", { class: "pa-titre" });
    const erreurs = el("ul", { class: "pa-erreurs" });
    const retour = el("button", { class: "pa-bouton discret", onclick: () => { ctx.etape = Math.max(0, ctx.etape - 1); dessiner(); } }, t("Retour"));
    const passer = el("button", { class: "pa-bouton discret", onclick: () => { ctx.etape += 1; dessiner(); } }, t("Passer"));
    const suivant = el("button", { class: "pa-bouton principal", onclick: () => { ctx.etape += 1; dessiner(); } }, t("Suivant"));
    const tester = el("button", {
        class: "pa-bouton principal",
        onclick: async (e) => {
            const problemes = erreursDuBrouillon(ctx.brouillon);
            erreurs.replaceChildren(...problemes.map((p) => el("li", {}, t(p))));
            if (problemes.length) return;
            e.currentTarget.disabled = true;
            const puzzle = brouillonVersPuzzle(ctx.brouillon);
            const r = await fetch("/new_puzzle?" + JSON.stringify(puzzle)).catch(() => null);
            if (r && r.ok) window.location.href = "/app/board.html";
            else { e.currentTarget.disabled = false; erreurs.replaceChildren(el("li", {}, t("Le moteur a refusé ce puzzle."))); }
        },
    }, t("Tester ce puzzle"));
    const fermer = el("button", { class: "pa-bouton discret", onclick: () => fond.remove() }, t("Fermer"));
    const fond = el("div", { class: "pa-fond" },
        el("div", { class: "pa-boite" },
            el("div", { class: "pa-tete" }, titre, barre),
            corps,
            el("div", { class: "pa-pied" }, fermer, erreurs, el("span", { class: "espace" }), retour, passer, suivant, tester)));
    document.body.append(fond);

    function dessiner() {
        const total = ETAPES.length;
        const derniere = ctx.etape >= total - 1;
        ctx.etape = Math.min(ctx.etape, total - 1);
        const etape = ETAPES[ctx.etape];
        enregistrerBrouillon(ctx.brouillon, ctx.etape);
        titre.textContent = `🧩 ${t("Créer un puzzle")} · ${t(etape.titre)} (${ctx.etape + 1}/${total})`;
        barre.replaceChildren(...ETAPES.map((_, i) => el("span", { class: i < ctx.etape ? "fait" : i === ctx.etape ? "ici" : "" })));
        sous.textContent = t(etape.aide);
        corps.replaceChildren(el("h3", {}, t(etape.titre)), sous, etape.rendre(ctx));
        retour.disabled = ctx.etape === 0;
        passer.style.display = derniere ? "none" : "";
        suivant.style.display = derniere ? "none" : "";
    }

    try {
        ctx.donnees = await chargerDonnees();
        const enregistre = lireBrouillonEnregistre();
        if (enregistre) {
            // Un brouillon attend : on laisse le choix avant de dessiner la première étape.
            await new Promise((fini) => {
                corps.replaceChildren(el("h3", {}, t("Un brouillon t'attend")),
                    el("p", { class: "pa-aide" }, t("Tu as un puzzle commencé dans ce navigateur.")),
                    el("div", { class: "pa-choix" },
                        el("button", { class: "actif", onclick: () => { ctx.brouillon = enregistre.brouillon; ctx.etape = enregistre.etape || 0; fini(); } }, t("Reprendre mon brouillon")),
                        el("button", { onclick: () => { oublierBrouillon(); fini(); } }, t("Repartir de zéro"))));
            });
        }
        ctx.villainDe = {};
        for (const e of ctx.donnees.extensions) {
            for (const s of e.scenarios) ctx.villainDe[fileName(s)] = null;
        }
        // Le méchant de chaque scénario, pour son illustration (lu en tâche de fond).
        Promise.all(Object.keys(ctx.villainDe).slice(0, 400).map(async (nom) => {
            try { ctx.villainDe[nom] = ((await api.scenario(nom)).villain || [])[0] || null; } catch (e) { /* sans image */ }
        })).then(() => { if (ETAPES[ctx.etape].titre === "L'ennemi") dessiner(); });
        dessiner();
    } catch (e) {
        corps.replaceChildren(el("p", {}, t("Impossible de charger les données.")));
    }
    return fond;
}
