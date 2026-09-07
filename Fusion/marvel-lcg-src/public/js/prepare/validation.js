// validation.js — règles de validation avant lancement.
"use strict";
import { t } from "/public/js/prepare/langue.js";

export function validate(state) {
    const errors = [];
    const n = state.playerCount;

    for (let i = 0; i < n; i++) {
        const p = state.players[i];
        if (!p || !p.hero) {
            errors.push({ code: "NO_HERO", message: `${t("Joueur")} ${i + 1} : ${t("aucun héros sélectionné")}`, step: 0 });
        } else if (!p.deck || !p.deck.hero || !p.deck.hero.length) {
            errors.push({ code: "NO_DECK", message: `${t("Joueur")} ${i + 1} : ${t("deck invalide")}`, step: 1 });
        }
    }

    if (!state.scenario) {
        errors.push({ code: "NO_SCENARIO", message: t("Aucun scénario sélectionné"), step: 2 });
    } else {
        const raw = state.scenario.rawJson || {};
        const mandatory = raw.encounter_sets || [];
        const selected = new Set(state.difficulty.selectedModularSets || []);
        // Les sets obligatoires sont toujours inclus au lancement (via encounter_sets),
        // on vérifie surtout le nombre de modulaires vs emplacements du scénario.
        const slots = state.scenario.modularSlots || { min: 0, max: 99 };
        const modularSelected = [...selected].filter((s) => !mandatory.includes(s));
        if (modularSelected.length > slots.max) {
            errors.push({ code: "TOO_MANY_MODULAR", message: `${t("Trop de sets modulaires")} (${modularSelected.length}/${slots.max})`, step: 2 });
        }
    }

    return { ok: errors.length === 0, errors };
}
