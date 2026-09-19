// cards.js — réutilise le module existant CardStatistics pour les métadonnées
// de cartes (nom, type, PV, aspect via `class`, traits, desc brut…).
"use strict";
import { CardStatistics } from "/public/js/module/card_statistics.js";

const _cs = new CardStatistics();
let _loaded = null;

export const cards = {
    /** Charge une seule fois cards.json + sets_info (retry si échec réseau). */
    async load() {
        if (_loaded) return _loaded;
        const p = _cs.loadAllCards(false, true).then(() => _cs);
        p.catch(() => { if (_loaded === p) _loaded = null; }); // ne pas cacher un échec
        _loaded = p;
        return p;
    },
    /** Objet Card par id (gère les ids recto/verso "aaa,bbb"). */
    get(cardId) {
        if (!cardId) return null;
        const id = String(cardId).split(",")[0];
        return _cs.const_card_dict[id] || null;
    },
    /** Toutes les cartes chargees. Sert a batir des index (auteur par set) une
     *  seule fois, plutot qu'a chercher carte par carte. */
    all() { return Object.values(_cs.const_card_dict || {}); },
    /** sets_info (SetInfo par extension). */
    sets() { return _cs.sets_json; },
    /** Aspect lisible depuis une carte (champ `class`). */
    aspectOf(cardId) {
        const c = this.get(cardId);
        return c && c.class ? c.class.toLowerCase() : "";
    },
    /** Taille de main d'un héros (dans desc : HND / Hand). */
    handSizeOf(cardId) {
        const c = this.get(cardId);
        if (!c || !c.desc) return undefined;
        return c.desc.HND ?? c.desc.Hand ?? c.desc.HandSize ?? undefined;
    },
};
