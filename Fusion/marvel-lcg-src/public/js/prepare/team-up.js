// team-up.js — les échanges Team-Up proposés à la mise en place (Rules Reference 1.8, annexe I).
//
// « If a player's deck includes an identity-specific card that is considered to
// "match" (according to the rules for uniqueness) an identity chosen by another
// player during setup, that player may replace the matching card in their deck
// with a card with the Team-Up keyword that names both their own identity and
// the other player's identity. »
//
// Module PUR : il ne fait que calculer les échanges possibles. La question
// (« may ») et l'échange lui-même vivent dans launcher.js.
"use strict";
import { correspondent, estUnique, titreDe } from "../deckbuilder/regles.js";

/** Les faces d'identité d'un deck (« hero » vaut « recto,verso »). */
function facesIdentite(deck, carte) {
    return String(((deck && deck.hero) || [])[0] || "").split(",").map((id) => carte(id)).filter(Boolean);
}

/** L'identité au format de `correspondent` : titre de héros, titre d'alter ego. */
function identite(deck, carte) {
    const faces = facesIdentite(deck, carte);
    const heros = faces.filter((f) => f.type === "Hero").map(titreDe);
    const alters = faces.filter((f) => f.type !== "Hero").map(titreDe);
    return heros.flatMap((t) => (alters.length ? alters : [""]).map((alt) => ({ t, s: "", alt })));
}

/** Tous les noms de l'identité (héros et alter ego), pour lire un mot-clé Team-Up. */
function nomsIdentite(deck, carte) {
    return new Set(facesIdentite(deck, carte).map(titreDe));
}

/** La carte Team-Up nomme-t-elle les deux identités (« Cyclops;Phoenix », variantes séparées par « / ») ? */
function nommeLesDeux(carte, nomsA, nomsB) {
    const brut = String((carte && carte.desc && carte.desc.TeamUp) || "");
    const parts = brut.split(";").map((x) => x.split("/").map((n) => n.trim()).filter(Boolean));
    if (parts.length !== 2) return false;
    const dans = (noms, liste) => liste.some((n) => noms.has(n));
    return (dans(nomsA, parts[0]) && dans(nomsB, parts[1])) || (dans(nomsA, parts[1]) && dans(nomsB, parts[0]));
}

/** Une copie partage le titre ET le sous-titre (RR « Copy »). */
function cleCopie(c) {
    return c ? `${titreDe(c)}|${String(c.subtitle || "").trim()}` : "";
}

function prefixeCommun(a, b) {
    let i = 0;
    while (i < a.length && i < b.length && a[i] === b[i]) i++;
    return i;
}

/**
 * Les échanges possibles, un par carte qui correspond à l'identité d'un AUTRE joueur.
 *
 * @param {Array<{index:number, deck:Object}>} joueurs  deck = { hero, hero_deck, player_deck }
 * @param {Function} carte   (card_id) -> carte du catalogue
 * @param {Iterable<string>} ids  tous les identifiants du catalogue (pour trouver les Team-Up)
 * @returns {Array<{joueur:number, autre:number, retirer:string, ajouter:string}>}
 */
export function echangesTeamUp(joueurs, carte, ids) {
    const teamUps = [...ids].map(String).filter((x) => { const c = carte(x); return c && c.desc && c.desc.TeamUp; });
    const out = [];
    for (const j of joueurs) {
        const deckJ = [...((j.deck && j.deck.hero_deck) || []), ...((j.deck && j.deck.player_deck) || [])];
        const nomsJ = nomsIdentite(j.deck, carte);
        // Deja dans le deck, meme sous un autre numero (reimpression) : rien a proposer.
        const copiesJ = new Set(deckJ.map((d) => cleCopie(carte(d))).filter(Boolean));
        for (const o of joueurs) {
            if (o === j) continue;
            const identiteO = identite(o.deck, carte);
            const nomsO = nomsIdentite(o.deck, carte);
            for (const id of (j.deck && j.deck.hero_deck) || []) {
                const c = carte(id);
                if (!c || !estUnique(c)) continue;
                const u = { t: titreDe(c), s: String(c.subtitle || "").trim(), alt: "" };
                if (!identiteO.some((x) => correspondent(u, x))) continue;
                // Plusieurs cartes peuvent nommer les deux (33023 chez Cyclops, 34023
                // chez Phoenix) : on propose celle du pack du joueur, reconnue au
                // plus long prefixe commun avec la carte remplacee.
                const tu = teamUps
                    .filter((x) => nommeLesDeux(carte(x), nomsJ, nomsO) && !copiesJ.has(cleCopie(carte(x))))
                    .sort((x, y) => prefixeCommun(y, String(id)) - prefixeCommun(x, String(id)))[0];
                if (!tu) continue;
                if (out.some((e) => e.joueur === j.index && e.retirer === String(id))) continue;
                out.push({ joueur: j.index, autre: o.index, retirer: String(id), ajouter: tu });
            }
        }
    }
    return out;
}

/** Le deck après l'échange : une copie, l'original (deck sauvegardé) reste intact. */
export function appliquerEchange(deck, echange) {
    const hero_deck = [...(deck.hero_deck || [])];
    const i = hero_deck.findIndex((d) => String(d) === echange.retirer);
    if (i < 0) return deck;
    hero_deck.splice(i, 1, echange.ajouter);
    return { ...deck, hero_deck };
}
