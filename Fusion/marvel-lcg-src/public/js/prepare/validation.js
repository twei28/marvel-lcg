// validation.js — règles de validation avant lancement.
"use strict";
import { t } from "/public/js/prepare/langue.js";
import { nombreMaxDeSets } from "/public/js/prepare/difficulte-logique.js";

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
        const modularSelected = [...selected].filter((s) => !mandatory.includes(s));
        // Les règles permettent plus de sets que la boîte n'en recommande (Règles de référence 1.7) et les
        // propositions VillainTheory en prennent jusqu'à 7 : le plafond suit `nombreMaxDeSets`.
        const maximum = nombreMaxDeSets(state.scenario);
        if (modularSelected.length > maximum) {
            errors.push({ code: "TOO_MANY_MODULAR", message: `${t("Trop de sets modulaires")} (${modularSelected.length}/${maximum})`, step: 3 });
        }
    }

    return { ok: errors.length === 0, errors };
}
