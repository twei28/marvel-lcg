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
        if (cle === "onclick") noeud.addEventListener("click", valeur);
        else if (cle === "oninput") noeud.addEventListener("input", valeur);
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
