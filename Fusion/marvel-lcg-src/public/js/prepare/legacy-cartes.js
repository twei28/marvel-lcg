// legacy-cartes.js — quelles CARTES on a déjà, en Legacy.
//
// Le quatrième module pur de Legacy. Les trois autres parlent de héros et de
// scénarios ; celui-ci parle des cartes de joueur, pour le deck-building.
// L'idée est celle de l'utilisateur (13/09/2026) : « proposer pour le
// deck-building que les cartes disponibles jusqu'à cette boîte ». On construit
// avec ce qu'on a.
//
// La chaîne : chaque carte connaît son PAQUET (`package_name`, la clé de
// cards.json), chaque paquet est une extension (`name` dans sets_info.json),
// chaque extension a une vague (BORNES_VAGUES, par `vagueDeLExtension`), et le
// parcours dit quelles vagues sont ouvertes. Une carte est disponible quand la
// vague de son paquet est ouverte.
//
// ⚠ CE QUI N'A PAS DE VAGUE RESTE LIBRE : les cartes fan-made, les paquets
// hors boîte. On n'invente pas de règle pour ce qui n'est dans aucun palier,
// même principe que pour les scénarios.
//
// ⚠ AUCUNE ENTRÉE-SORTIE : on passe l'état, les extensions et une fonction
// « paquet d'une carte », il rend des tables de consultation.
"use strict";

import { vagueDeLExtension } from "./catalog.js";

/** Fabrique la disponibilité.
 *
 *  `extensions` : ce que rend `catalog.extensions()` ({ key, code }).
 *  `paquetDe(id)` : le paquet d'une carte, ou "" si inconnu.
 *
 *  Rend :
 *    carte(id)   -> { ouvert, etiquette }   étiquette = la boîte qui manque
 *    deck(deck)  -> { ouvert, manquantes }  manquantes = les ids fermés
 */
export function fabriquerDisponibilite(etat, extensions, paquetDe, t = (x) => x) {
    const etapes = (etat.parcours && etat.parcours.etapes) || [];
    const ouverte = new Map(etapes.map((e) => [e.vague, !!e.ouvert]));
    const nomVague = new Map(etapes.map((e) => [e.vague, e.nom || `${t("Vague")} ${e.vague}`]));
    // paquet (name de sets_info) -> vague, calculé une fois pour 140 paquets.
    const vagueDuPaquet = new Map();
    for (const ext of extensions || []) {
        if (!ext || !ext.code) continue;
        vagueDuPaquet.set(String(ext.code), vagueDeLExtension(ext.key));
    }
    const cache = new Map();
    function carte(id) {
        const cle = String(id || "").split(",")[0];
        if (cache.has(cle)) return cache.get(cle);
        const paquet = String(paquetDe(cle) || "");
        const vague = vagueDuPaquet.get(paquet);
        let sortie;
        if (vague === null || vague === undefined) {
            sortie = { ouvert: true, etiquette: "" };
        } else {
            const ok = ouverte.get(vague) === true;
            sortie = { ouvert: ok, etiquette: ok ? "" : (nomVague.get(vague) || `${t("Vague")} ${vague}`) };
        }
        cache.set(cle, sortie);
        return sortie;
    }
    /** Un deck est jouable quand TOUTES ses cartes le sont. Les cartes du
     *  héros (identité, signature) viennent de son paquet : si le héros est
     *  ouvert, elles le sont, mais on les vérifie quand même, ça ne coûte
     *  rien et ça ne ment jamais. */
    function deck(d) {
        const ids = [
            ...((d && d.hero) || []).flatMap((x) => String(x).split(",")),
            ...((d && d.hero_deck) || []),
            ...((d && d.player_deck) || []),
        ];
        const manquantes = [...new Set(ids.map((x) => String(x).split(",")[0]).filter((x) => x && !carte(x).ouvert))];
        return { ouvert: manquantes.length === 0, manquantes };
    }
    return { carte, deck };
}
