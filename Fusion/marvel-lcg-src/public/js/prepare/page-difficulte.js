// page-difficulte.js — l'étape « Difficulté » du wizard de préparation (30/10/2026).
//
// Entre « Méchant » et « Final » : niveau de menace, sets modulaires (tous, rangés par boîte), propositions
// VillainTheory. Le DOM seul est ici ; la logique pure est dans difficulte-logique.js (testée) et l'état reste
// `state.difficulty` (le lanceur ne change pas).
//
// Le joueur ne touche qu'à `state.difficulty.selectedModularSets` : toute coche passe `modularConfig` à
// « custom », et « Recommandés » / « Aléatoire » le remettent comme avant.
"use strict";

import { NOMS_SETS_FR } from "/public/js/prepare/noms-sets-fr.js";
import {
    basculerSet, combinaisonsDuScenario, difficulteEstimee, estJouable, filtrerGroupes, grouperParBoite,
    libelleDifficulte, nombreMaxDeSets,
} from "/public/js/prepare/difficulte-logique.js";
import { estSetStandard, libelleNiveau } from "/public/js/prepare/niveau-standard.js";

/**
 * @param ctx { state, el, poser, t, catalog, estTel, rendreNiveau, nomExtension, numeroDExtension, langueActuelle,
 *              nomDuSetModulaire, auteurDuSet, appliquerSetsModulaires }
 */
export function construirePageDifficulte(ctx) {
    const { state, el, poser, t, catalog, estTel, langueActuelle } = ctx;
    const d = state.difficulty;
    const sc = state.scenario;
    const tel = estTel();

    const local = { vt: false, recherche: "", onglet: "sets", donnees: null, sets: [], groupes: [], propositions: [] };

    /** Nom d'un set tel que le joueur le lit : français déduit des cartes quand il existe, sinon le nom du fichier. */
    const nomDuSet = (id) => {
        const base = ctx.nomDuSetModulaire(id);
        const fanmade = !!ctx.auteurDuSet(id);
        return langueActuelle() === "fr" && NOMS_SETS_FR[id] && !fanmade ? NOMS_SETS_FR[id] : base;
    };

    const racine = el("section", { class: "step difficulte" + (tel ? " dp-tel" : "") });
    const entete = el("div", { class: "dp-haut" },
        el("b", { class: "mvl dp-titre" }, t("Difficulté et sets modulaires")),
        el("span", { class: "dp-sous" }, sc ? sc.name : ""));
    const gauche = el("div", { class: "dp-pn dp-sets", "data-onglet": "sets" });
    const droite = el("div", { class: "dp-pn dp-reglages", "data-onglet": "niveau" });
    const bas = el("div", { class: "dp-props", "data-onglet": "propositions" });
    const onglets = tel ? el("div", { class: "dp-onglets", role: "tablist" }) : null;

    const choisir = (liste) => {
        d.modularConfig = "custom";
        d.selectedModularSets = liste;
        rafraichir();
    };

    /* ---- colonne de gauche : ce qui sera joué ---- */
    function ligneSet(id, { etiquette, retirable, attenuee, onclick, nom } = {}) {
        return el("div", { class: "dp-set" + (retirable ? " ajoute" : "") + (attenuee ? " attenue" : ""), onclick },
            el("span", { class: "dp-set-nom" }, nom || nomDuSet(id)),
            el("small", {}, etiquette || ""),
            retirable ? el("button", {
                class: "dp-x", "aria-label": t("Retirer"), title: t("Retirer"),
                onclick: (e) => { e.stopPropagation(); choisir(d.selectedModularSets.filter((s) => s !== id)); },
            }, "✕") : null);
    }

    function dessinerGauche() {
        const recommandes = sc.recommendedModularSets;
        const choisis = d.selectedModularSets;
        const obligatoires = sc.mandatoryEncounterSets.filter((s) => !estSetStandard(s) && !/^(standard|expert)/.test(s));
        const ajoutes = choisis.filter((s) => !recommandes.includes(s));
        const maximum = nombreMaxDeSets(sc);
        const trop = choisis.length > maximum;

        poser(gauche,
            el("h4", { class: "dp-k" }, t("Sets de la partie")),
            el("div", { class: "dp-etiq" }, t("Obligatoires")),
            obligatoires.length ? null : ligneSet(null, { etiquette: t("scénario"), nom: sc.name }),
            ...obligatoires.map((s) => ligneSet(s, { etiquette: t("scénario") })),
            ligneSetNiveau(),
            el("div", { class: "dp-etiq" }, t("Recommandés")),
            ...(recommandes.length
                ? recommandes.map((s) => ligneSet(s, {
                    etiquette: choisis.includes(s) ? "" : t("retiré · cliquer pour remettre"),
                    attenuee: !choisis.includes(s),
                    onclick: () => choisir(basculerSet(choisis, s)),
                }))
                : [el("div", { class: "dp-vide" }, t("Aucun set modulaire recommandé."))]),
            el("div", { class: "dp-etiq" }, t("Ajoutés par toi")),
            ...(ajoutes.length
                ? ajoutes.map((s) => ligneSet(s, { retirable: true }))
                : [el("div", { class: "dp-vide" }, t("Coche des sets dans la liste, ou choisis une proposition."))]),
            trop ? el("em", { class: "dp-alerte" }, t("Trop de sets modulaires") + " (" + choisis.length + "/" + maximum + ")") : null,
            el("div", { class: "dp-rapide" },
                el("button", {
                    class: "tampon" + (d.modularConfig === "recommended" ? " on" : ""),
                    onclick: () => { d.modularConfig = "recommended"; ctx.appliquerSetsModulaires(); rafraichir(); },
                }, t("Recommandés")),
                el("button", {
                    class: "tampon" + (d.modularConfig === "random" ? " on" : ""),
                    onclick: () => { d.modularConfig = "random"; ctx.appliquerSetsModulaires(); },
                }, t("Aléatoire"))),
            el("div", { class: "dp-rapide" },
                el("button", {
                    class: "tampon dp-vt" + (local.vt ? " on" : ""), "aria-expanded": local.vt ? "true" : "false",
                    onclick: () => {
                        local.vt = !local.vt;
                        if (tel) { local.onglet = "propositions"; appliquerOnglet(); }
                        dessinerGauche(); dessinerBas();
                    },
                }, t("Sets proposés par VillainTheory"), el("span", { class: "dp-fleche" }, local.vt ? "▴" : "▾"))));
    }

    function ligneSetNiveau() {
        const niveau = libelleNiveau(d.standard) + (d.base === "expert" ? " + Expert" : "");
        return el("div", { class: "dp-set" }, el("span", { class: "dp-set-nom" }, niveau), el("small", {}, t("suit le niveau")));
    }

    /* ---- colonne de droite : niveau, puis tous les sets ---- */
    const zoneNiveau = el("div", { class: "dp-niveau", id: "tb-niveau" });
    const recherche = el("input", {
        class: "search dp-recherche", type: "search", id: "dp-recherche",
        placeholder: t("Chercher un set ou une boîte…"), "aria-label": t("Chercher un set ou une boîte…"),
        oninput: (e) => { local.recherche = e.target.value; dessinerListe(); },
    });
    const liste = el("div", { class: "dp-liste" }, el("div", { class: "loading" }, t("Chargement des sets modulaires...")));

    function dessinerListe() {
        const choisis = new Set(d.selectedModularSets);
        const groupes = filtrerGroupes(local.groupes, local.recherche);
        if (!groupes.length) {
            poser(liste, el("div", { class: "dp-vide" }, local.groupes.length ? t("Aucun set ne correspond.") : t("Chargement des sets modulaires...")));
            return;
        }
        const ouvrir = !!local.recherche.trim();
        poser(liste, ...groupes.map((g) => el("details", { class: "dp-boite", open: ouvrir || g.sets.some((s) => choisis.has(s.name)) || undefined },
            el("summary", {}, g.titre, el("small", {}, " · " + g.sets.length)),
            ...g.sets.map((s) => el("label", { class: "dp-case" + (choisis.has(s.name) ? " on" : "") },
                el("input", {
                    type: "checkbox", name: "set-" + s.name, checked: choisis.has(s.name) || undefined,
                    onchange: () => choisir(basculerSet(d.selectedModularSets, s.name)),
                }),
                el("span", {}, nomDuSet(s.name)),
                sc.recommendedModularSets.includes(s.name) ? el("small", {}, t("recommandé")) : null)))));
    }

    /* ---- propositions VillainTheory ---- */
    function dessinerBas() {
        bas.hidden = !local.vt;
        if (!local.vt) { poser(bas); return; }
        const cartes = local.propositions.filter((c) => !c.defaut);
        poser(bas,
            el("div", { class: "dp-etiq" }, t("Proposés pour") + " " + sc.name + " · VillainTheory", noteDeLaSelection()),
            cartes.length
                ? el("div", { class: "dp-cartes" }, ...cartes.map(carte))
                : el("div", { class: "dp-vide" }, t("Aucune proposition pour ce méchant.")));
    }

    /** « Ta sélection : +1 (Stay Hydrated) », seulement quand elle a une note (voir difficulteEstimee). */
    function noteDeLaSelection() {
        const e = difficulteEstimee(d.selectedModularSets, sc.recommendedModularSets, local.propositions);
        if (e.valeur === null) return null;
        return el("span", { class: "dp-selection" }, " — " + t("ta sélection") + " : " + libelleDifficulte(e.valeur, e.incertain)
            + (e.nom ? " (" + e.nom + ")" : ""));
    }

    function carte(c) {
        const jouable = estJouable(c);
        const choisis = d.selectedModularSets;
        const actif = jouable && c.sets.length === choisis.length && c.sets.every((s) => choisis.includes(s));
        const noms = [...c.sets.map(nomDuSet), ...c.manquants];
        return el("div", { class: "dp-carte" + (jouable ? "" : " grisee") + (actif ? " active" : "") },
            el("header", {},
                el("b", {}, c.nom),
                el("span", { class: "dp-note" }, libelleDifficulte(c.difficulte, c.incertain))),
            el("div", { class: "dp-carte-sets" }, noms.join(" · ")),
            c.recommande ? el("small", { class: "dp-reco" }, "✔ " + t("conseillé par l'auteur")) : null,
            c.speculatif ? el("small", { class: "dp-reco" }, t("spéculatif : set pas encore sorti")) : null,
            el("p", {}, c.note),
            jouable ? null : el("div", { class: "dp-manque" }, t("Absent du jeu") + " : " + c.manquants.join(", ")),
            el("button", {
                class: "tampon" + (actif ? " on" : ""), disabled: jouable ? undefined : true,
                onclick: () => choisir([...c.sets]),
            }, actif ? t("Utilisé") : t("Utiliser")));
    }

    /* ---- téléphone : trois onglets ---- */
    function appliquerOnglet() {
        if (!tel) return;
        racine.dataset.onglet = local.onglet;
        poser(onglets, ...[["sets", "Sets de la partie"], ["niveau", "Niveau"], ["propositions", "Propositions"]].map(([id, nom]) =>
            el("button", {
                class: "tampon" + (local.onglet === id ? " on" : ""), role: "tab", "aria-selected": local.onglet === id ? "true" : "false",
                onclick: () => {
                    local.onglet = id;
                    if (id === "propositions" && !local.vt) { local.vt = true; dessinerGauche(); dessinerBas(); }
                    appliquerOnglet();
                },
            }, t(nom))));
    }

    function rafraichir() {
        dessinerGauche();
        dessinerListe();
        dessinerBas();
    }

    /* ---- assemblage ---- */
    poser(droite,
        zoneNiveau,
        el("h4", { class: "dp-k" }, t("Tous les sets modulaires")),
        recherche,
        liste);
    poser(racine, entete, onglets, gauche, droite, bas);
    bas.hidden = true;
    if (tel) appliquerOnglet();
    ctx.rendreNiveau(zoneNiveau, dessinerGauche);
    dessinerGauche();

    // Données asynchrones : les sets du jeu, leurs boîtes, les propositions.
    (async () => {
        const [tous, exts, vt] = await Promise.all([
            catalog.encounterSets(), catalog.extensions(),
            import("/public/js/prepare/villaintheory.js").catch(() => null),
        ]);
        local.sets = tous.filter((s) => s.kind === "modular");
        const langue = langueActuelle();
        const boiteDe = (nom) => (exts.find((e) => e.encounters.includes(nom)) || {}).key || "";
        local.groupes = grouperParBoite(local.sets, boiteDe,
            (cle) => (cle ? ctx.numeroDExtension(cle) ?? 999 : 9999),
            (cle) => ctx.nomExtension(cle, langue), t("Autres"));
        local.propositions = vt ? combinaisonsDuScenario(sc.id, vt.VILLAINTHEORY) : [];
        rafraichir();
    })();

    return racine;
}
