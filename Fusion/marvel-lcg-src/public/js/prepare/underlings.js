// underlings.js — les scénarios à VILAIN INTERCHANGEABLE, réunis en une tuile.
//
// Fear No Evil (18/09/2026) : cinq manigances principales se jouent avec
// n'importe lequel des cinq vilains « underling ». Décision de l'utilisateur :
// UNE tuile par manigance, et au clic une modale qui propose le vilain, comme
// la modale des variantes d'un héros. Sous le capot, chaque couple reste un
// scénario complet `<manigance>_<vilain>` (data/scenarios/), que le moteur, le
// harnais et l'autoplay consomment tels quels : le lanceur ne fait que
// REPLIER ces fichiers sous une tuile, puis choisir lequel envoyer.
//
// Déclaration dans data/sets_info.json, sur l'extension :
//   "manigances": ["art_museum_heist", ...],
//   "underlings": ["hammerhead", "bullseye", ...]
// Un scénario `<manigance>_<underling>` présent dans `scenarios` rejoint la
// tuile de sa manigance ; les autres scénarios de l'extension (Kingpin, à
// manigance fixe) gardent leur tuile.
//
// Module PUR (ni DOM ni import), testé par
// `node --test tools/tests-lanceur/underlings.test.mjs`.
"use strict";

/** « Art Museum Heist (Hammerhead) » -> « Art Museum Heist ». */
export function nomDeManigance(nom) {
    return String(nom || "").replace(/\s*\([^)]*\)\s*$/, "").trim();
}

/** « Art Museum Heist (Hammerhead) » -> « Hammerhead » (repli : l'id titré). */
export function nomDuVilain(nom, underlingId) {
    const m = /\(([^)]*)\)\s*$/.exec(String(nom || ""));
    if (m && m[1]) return m[1].trim();
    return String(underlingId || "").split("_").map((x) => x.charAt(0).toUpperCase() + x.slice(1)).join(" ");
}

/**
 * Replie les scénarios `<manigance>_<underling>` en une tuile par manigance.
 *
 * `scenarios` : la liste du catalogue (chaque élément a `id`, `name`,
 * `villainCards`...). `ext` : l'extension (`manigances`, `underlings`).
 * `memoire` : { manigance -> underling } (dernier choix sur cet appareil).
 * Renvoie une NOUVELLE liste, dans l'ordre du catalogue : la tuile prend la
 * place du premier scénario de sa manigance et porte `underlings`
 * (ordre de `ext.underlings`), `scenarioIds`, et `courant` (le scénario que
 * la tuile montre : celui de la mémoire, sinon celui du TOUR DE RÔLE). Une
 * manigance qui n'a qu'un seul vilain porté a quand même sa tuile : aucune
 * modale ne s'ouvrira pour elle (jamais de modale à un seul choix).
 *
 * ⚠ SANS MÉMOIRE, CHAQUE AFFAIRE MONTRE UN VILAIN DIFFÉRENT (19/09/2026).
 * Prendre le premier de la liste donnait cinq fois le même portrait sur la
 * rangée — cinq Hammerhead — et l'utilisateur l'a signalé : « je n'aime pas
 * qu'on voie toujours le même méchant sur chaque scénario (même si on peut
 * choisir) ». On décale donc d'une place par manigance : la rangée montre les
 * cinq vilains, et le choix reste entier au clic. Le décalage est calculé sur
 * le RANG DE LA MANIGANCE, donc stable d'un affichage à l'autre : la tuile ne
 * change pas de portrait sous les yeux du joueur.
 */
export function regrouperUnderlings(scenarios, ext, memoire) {
    const manigances = (ext && ext.manigances) || [];
    const underlings = (ext && ext.underlings) || [];
    if (!manigances.length || !underlings.length) return scenarios.slice();
    const parId = new Map(scenarios.map((sc) => [sc.id, sc]));
    const tuiles = new Map();
    for (const [rang, manigance] of manigances.entries()) {
        const choix = [];
        for (const u of underlings) {
            const sc = parId.get(`${manigance}_${u}`);
            if (!sc) continue;
            choix.push({ id: u, scenarioId: sc.id, nom: nomDuVilain(sc.name, u), villainCardId: (sc.villainCards || [])[0] || sc.tileImage, scenario: sc });
        }
        if (!choix.length) continue;
        const voulu = memoire && memoire[manigance];
        const courant = choix.find((c) => c.id === voulu) || choix[rang % choix.length];
        tuiles.set(manigance, {
            ...courant.scenario,
            id: manigance,
            name: nomDeManigance(courant.scenario.name),
            interchangeable: true,
            manigance,
            underlings: choix,
            scenarioIds: choix.map((c) => c.scenarioId),
            courant,
        });
    }
    const vues = new Set();
    const out = [];
    for (const sc of scenarios) {
        const m = manigances.find((x) => underlings.some((u) => sc.id === `${x}_${u}`));
        if (!m) { out.push(sc); continue; }
        if (vues.has(m)) continue;
        vues.add(m);
        out.push(tuiles.get(m));
    }
    return out;
}

/** Le scénario concret d'une tuile pour un vilain donné (repli : le courant). */
export function scenarioDuVilain(tuile, underlingId) {
    if (!tuile || !tuile.underlings) return tuile || null;
    const c = tuile.underlings.find((x) => x.id === underlingId) || tuile.courant;
    return c ? c.scenario : null;
}

/** Une tuile « contient » un scénario si c'est l'un de ses couples. */
export function tuileContient(tuile, scenarioId) {
    if (!tuile) return false;
    if (tuile.id === scenarioId) return true;
    return !!(tuile.scenarioIds && tuile.scenarioIds.includes(scenarioId));
}
