// roue.js — « Partie au hasard » : le tirage et le bandeau qui défile.
//
// Décisions de l'utilisateur, une à une, le 08/10/2026 :
// .planning/todos/2026-10-08-roue-du-hasard.md. Une case = un héros ou un
// scénario jouable seul ; officiels par défaut, une seule case « fan-made »
// pour les deux ; jamais deux fois le même héros ; un bandeau façon machine à
// sous qui ralentit avec des clics et s'arrête sous un repère.
//
// Partagé par l'écran de préparation (l'hôte) et le salon (les invités) : les
// fonctions de tirage sont PURES et exportées pour être éprouvées seules
// (ui-check/tests/roue-hasard.spec.ts) ; le bandeau ne sait rien du jeu, il
// reçoit des cases { id, image, nom } et anime celle qu'on lui dit.
"use strict";

import { cardImageUrlEn } from "/public/js/prepare/api.js";

/** Un scénario qui n'a pas sa place sur la roue : les défis (règles du mois
 *  par-dessus un scénario), les variantes Expert (la difficulté se choisit
 *  APRÈS, sur l'écran du scénario) et les versions compétitives de Synthezoid
 *  Smackdown, qui se jouent joueurs contre joueurs. */
export function horsRoue(sc) {
    if (!sc || !sc.id) return true;
    const id = String(sc.id);
    if (sc.extension === "defis") return true;
    if (sc.challenges && sc.challenges.length) return true;
    if (/^24\d{2}_/.test(id)) return true;
    return id.endsWith("_expert") || id.endsWith("_competitive");
}

/** Les héros qu'on peut tirer. `verrou` : celui de Legacy, ou rien. */
export function herosTirables(heros, { fanmade = false, verrou = null } = {}) {
    return (heros || []).filter((h) => h && h.id
        && (fanmade || !h.homebrew)
        && (!verrou || verrou.heros(h).ouvert));
}

/** Les scénarios qu'on peut tirer, toutes boîtes confondues. */
export function scenariosTirables(scenarios, { fanmade = false, verrou = null } = {}) {
    const vus = new Set();
    return (scenarios || []).filter((sc) => {
        if (horsRoue(sc) || vus.has(sc.id)) return false;
        vus.add(sc.id);
        return (fanmade || !sc.homebrew) && (!verrou || verrou.scenario(sc).ouvert);
    });
}

/** Une case au hasard, hors des identifiants `exclus`. null si rien ne reste. */
export function tirer(pool, { exclus = [], aleatoire = Math.random } = {}) {
    const interdits = new Set(exclus);
    const reste = (pool || []).filter((x) => !interdits.has(x.id));
    if (!reste.length) return null;
    return reste[Math.min(reste.length - 1, Math.floor(aleatoire() * reste.length))];
}

/** `n` cases DIFFÉRENTES, hors `exclus`. Moins de `n` si le pool s'épuise. */
export function tirerPlusieurs(pool, n, { exclus = [], aleatoire = Math.random } = {}) {
    const pris = [...exclus];
    const sortie = [];
    for (let i = 0; i < n; i++) {
        const x = tirer(pool, { exclus: pris, aleatoire });
        if (!x) break;
        sortie.push(x);
        pris.push(x.id);
    }
    return sortie;
}

/** Ce qui défile : `avant` cases au hasard, le gagnant, puis `apres` cases
 *  pour que la droite du bandeau ne soit pas vide à l'arrêt. `depart`, s'il
 *  est donné, ouvre la bande : une relance repart de ce qu'on voyait. */
export function bande(pool, gagnant, { avant = 34, apres = 4, depart = null, aleatoire = Math.random } = {}) {
    const auHasard = () => (pool.length ? pool[Math.floor(aleatoire() * pool.length) % pool.length] : gagnant);
    const cases = [];
    if (depart) cases.push(auHasard(), auHasard(), depart);
    while (cases.length < avant) cases.push(auHasard());
    const indexGagnant = cases.length;
    cases.push(gagnant);
    for (let i = 0; i < apres; i++) cases.push(auHasard());
    return { cases, indexGagnant, indexDepart: 2 };
}

/** Ralentissement de la machine à sous : vite au départ, lent à l'arrivée. */
export function avancement(t) {
    const x = Math.min(1, Math.max(0, t));
    return 1 - Math.pow(1 - x, 3);
}

/* ---------------- Le bandeau ---------------- */

/** Pas d'animation : mouvement réduit demandé, ou affichage sobre. */
export function sansMouvement() {
    try {
        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return true;
    } catch (e) { /* navigateur ancien : on anime */ }
    return document.documentElement.dataset.affichage === "sobre";
}

function caseDom(item) {
    const n = document.createElement("div");
    n.className = "roue-case";
    if (item && item.image) n.style.backgroundImage = `url("${cardImageUrlEn(item.image)}")`;
    const nom = document.createElement("span");
    nom.className = "roue-case-nom";
    nom.textContent = (item && item.nom) || "";
    n.append(nom);
    return n;
}

/**
 * Un bandeau. `surClic` est appelé chaque fois qu'une case passe sous le
 * repère (le son). Rend { element, tourner(pool, gagnant, duree), poser(item),
 * actuel() }. `tourner` rend une promesse résolue à l'arrêt.
 */
export function creerBandeau({ surClic = () => {} } = {}) {
    const fenetre = document.createElement("div");
    fenetre.className = "roue-fenetre";
    const piste = document.createElement("div");
    piste.className = "roue-piste";
    const repere = document.createElement("div");
    repere.className = "roue-repere";
    fenetre.append(piste, repere);

    let actuel = null;
    let jeton = 0;

    const largeurCase = () => {
        const c = piste.firstElementChild;
        if (!c) return 0;
        const style = getComputedStyle(piste);
        const gap = parseFloat(style.columnGap || style.gap || "0") || 0;
        return c.getBoundingClientRect().width + gap;
    };
    // Décalage qui met la case `i` sous le repère, au centre de la fenêtre.
    const decalage = (i, pas) => fenetre.clientWidth / 2 - (i * pas + (pas - gapDe()) / 2);
    const gapDe = () => {
        const style = getComputedStyle(piste);
        return parseFloat(style.columnGap || style.gap || "0") || 0;
    };

    function poser(item) {
        jeton++;
        actuel = item;
        piste.replaceChildren(caseDom(item));
        piste.style.transform = "";
        fenetre.classList.add("est-pose");
        fenetre.classList.remove("en-cours");
    }

    function tourner(pool, gagnant, duree = 4000) {
        const moi = ++jeton;
        if (!gagnant) return Promise.resolve(null);
        if (sansMouvement() || duree <= 0) {
            poser(gagnant);
            surClic();
            return Promise.resolve(gagnant);
        }
        fenetre.classList.remove("est-pose");
        fenetre.classList.add("en-cours");
        const { cases, indexGagnant, indexDepart } = bande(pool, gagnant, { depart: actuel });
        piste.replaceChildren(...cases.map(caseDom));
        const pas = largeurCase();
        if (!pas) { poser(gagnant); return Promise.resolve(gagnant); }
        const x0 = decalage(indexDepart, pas);
        const x1 = decalage(indexGagnant, pas);
        piste.style.transform = `translateX(${x0}px)`;
        let derniereCase = indexDepart;
        const debut = performance.now();
        return new Promise((resoudre) => {
            const image = (maintenant) => {
                if (moi !== jeton) { resoudre(null); return; }
                const t = (maintenant - debut) / duree;
                const x = x0 + (x1 - x0) * avancement(t);
                piste.style.transform = `translateX(${x}px)`;
                const sousRepere = Math.round((fenetre.clientWidth / 2 - x - (pas - gapDe()) / 2) / pas);
                if (sousRepere !== derniereCase) { derniereCase = sousRepere; surClic(); }
                if (t < 1) { requestAnimationFrame(image); return; }
                actuel = gagnant;
                fenetre.classList.remove("en-cours");
                fenetre.classList.add("est-arrete");
                resoudre(gagnant);
            };
            requestAnimationFrame(image);
        });
    }

    return {
        element: fenetre,
        tourner,
        poser,
        actuel: () => actuel,
    };
}

/** Case de bandeau pour un héros du catalogue. */
export function caseHeros(h) {
    return h ? { id: h.id, image: h.heroCardId, nom: h.name } : null;
}

/** Case de bandeau pour un scénario du catalogue. */
export function caseScenario(sc) {
    if (!sc) return null;
    const image = ((sc.villainCards || [])[0] || sc.tileImage || "").split(",")[0];
    return { id: sc.id, image, nom: sc.name };
}

/* ---------------- Le partage en ligne ---------------- */

/** Lit la roue du salon. null si aucune, ou table muette. */
export async function lireRoue() {
    try {
        const r = await fetch("get_roue?", { cache: "no-store" });
        if (!r.ok) return null;
        const brut = await r.json();
        return brut && brut.roue ? brut.roue : null;
    } catch (e) {
        return null;
    }
}

/** Publie un lancer. Rend la roue à jour, ou null en cas de refus. */
export async function publierRoue(corps) {
    try {
        const r = await fetch("/set_roue", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(corps),
        });
        if (!r.ok) return null;
        const brut = await r.json();
        return brut.roue || null;
    } catch (e) {
        return null;
    }
}
