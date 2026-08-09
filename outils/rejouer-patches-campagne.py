# -*- coding: utf-8 -*-
"""Ré-applique les patches « campagne » sur l'écran de préparation.

Écrit comme un script plutôt que comme des remplacements à la main : le
déploiement (ui-app/deployer.sh) écrase public/js depuis la copie WSL, et ces
patches ont donc déjà été perdus une fois. Pouvoir les rejouer d'un coup, sur
n'importe laquelle des deux installations, évite de les réécrire.

Usage : python3 patch_prepare.py <dossier public/js/prepare>
Idempotent : un patch déjà présent est signalé et sauté.
"""
import io
import os
import sys

DOSSIER = sys.argv[1] if len(sys.argv) > 1 else "."

PATCHES_APP = [
    # 1. imports + détection du mode création
    (
        'import { lireFavoris, basculerFavori } from "/public/js/marvelcdb/favoris.js";',
        '''import { lireFavoris, basculerFavori } from "/public/js/marvelcdb/favoris.js";
import { lireBrouillon, ecrireBrouillon } from "/public/js/campagne/brouillon.js";

// CREATION D'EQUIPE POUR UNE CAMPAGNE.
//
// Le mode Campagne a son propre ecran (/campagne.html) : boite, difficulte,
// progression, histoire, carnet. Une seule chose lui manque, choisir une
// equipe — et ce selecteur-la vit ici, avec ses identites alternatives, ses
// decks marvelcdb et ses aspects. Plutot que de le dupliquer, l'ecran des
// campagnes nous envoie sur /prepare.html?campagne avec un brouillon, et on
// lui rend l'equipe. Le wizard se reduit alors a ses deux premieres etapes :
// ni mechant, ni menace, ni bouton de lancement — c'est la campagne qui
// impose tout cela.
const BROUILLON_CAMPAGNE = new URLSearchParams(window.location.search).has("campagne")
    ? lireBrouillon()
    : null;
const creationCampagne = () => !!BROUILLON_CAMPAGNE;''',
    ),
    # 2. étapes réduites
    (
        'const STEPS = ["Équipe", "Decks", "Méchant", "Menace", "Final"].map((s) => t(s));',
        'const STEPS = (creationCampagne() ? ["Équipe", "Decks"] : ["Équipe", "Decks", "Méchant", "Menace", "Final"])\n    .map((s) => t(s));',
    ),
    # 3. la tuile Campagne redirige
    (
        '            onclick: () => {\n                const wasCampaign = isCampaignMode();',
        '''            onclick: () => {
                // La campagne n'est plus un mode du wizard : elle a son écran,
                // qui impose l'ordre des scénarios, les sets et la difficulté.
                if (m.id === "campaign") { window.location.href = "/campagne.html"; return; }
                const wasCampaign = isCampaignMode();''',
    ),
    # 4. bandeau au lieu des tuiles, en création
    (
        'function modeStrip() {\n    const strip = el("div", { class: "mode-strip" });',
        '''function modeStrip() {
    const strip = el("div", { class: "mode-strip" });
    // En création d'équipe pour une campagne, le mode et le nombre de héros
    // sont déjà décidés et ne se rediscutent pas : on l'annonce au lieu de
    // proposer des tuiles qui mentiraient.
    if (creationCampagne()) {
        strip.append(el("div", { class: "mode-pill sel campagne-bandeau" },
            el("span", { class: "mode-mark mvl" }, "C"),
            el("span", { class: "mode-copy" },
                el("b", {}, t("Campagne") + " — " + BROUILLON_CAMPAGNE.nom),
                el("small", {}, BROUILLON_CAMPAGNE.nbJoueurs + " " + t("héros") + " · "
                    + (BROUILLON_CAMPAGNE.difficulte === "expert" ? t("Campagne experte") : t("Standard"))
                    + " · " + t("identités figées pour toute la campagne")),
            ),
        ));
        return strip;
    }''',
    ),
    # 5. bouton final
    (
        '''        state.step < LAST_STEP
            ? el("button", { class: "btn primary", disabled: !canContinue() || undefined, onclick: next }, t("Continuer"))
            : el("button", {
                class: "btn launch",
                disabled: (!validate(state).ok || (enLigne() && !state.salon.prete)) || undefined,
                onclick: doLaunch,
            }, t("Lancer la partie")),''',
        '''        state.step < LAST_STEP
            ? el("button", { class: "btn primary", disabled: !canContinue() || undefined, onclick: next },
                t("Continuer"))
            : creationCampagne()
                ? el("button", {
                    class: "btn launch",
                    disabled: !stepComplete(1) || undefined,
                    onclick: validerEquipeCampagne,
                }, t("Valider l'équipe"))
                : el("button", {
                    class: "btn launch",
                    disabled: (!validate(state).ok || (enLigne() && !state.salon.prete)) || undefined,
                    onclick: doLaunch,
                }, t("Lancer la partie")),''',
    ),
    # 6. statut de navigation
    (
        '''    const heroes = activePlayers().filter((p) => p.hero).length;
    const sc = state.scenario ? state.scenario.name : t("Cible inconnue");''',
        '''    const heroes = activePlayers().filter((p) => p.hero).length;
    if (creationCampagne()) {
        return `${heroes}/${state.playerCount} ${t("héros")} - ${t("équipe de campagne")}`;
    }
    const sc = state.scenario ? state.scenario.name : t("Cible inconnue");''',
    ),
    # 7. rendu de l'équipe à l'écran des campagnes
    (
        '''    try { await launch(state); }
    catch (e) { alert(t("Erreur de lancement :") + " " + e.message); }
}''',
        '''    try { await launch(state); }
    catch (e) { alert(t("Erreur de lancement :") + " " + e.message); }
}

/**
 * Rend l'équipe à l'écran des campagnes et s'efface.
 *
 * On fige ici la forme DÉFINITIVE de chaque héros — identité résolue, nom du
 * héros plutôt que titre du deck — pour que la campagne relance ses cinq
 * scénarios sans jamais avoir à redemander quoi que ce soit. Le deck est
 * recopié en entier : c'est ce que le moteur consomme, et une campagne doit
 * survivre à la suppression du deck marvelcdb dont elle est partie.
 */
function validerEquipeCampagne() {
    const brouillon = BROUILLON_CAMPAGNE;
    brouillon.equipe = activePlayers().filter((p) => p && p.deck).map((p) => {
        const identite = (p.identity && p.identity.hero) || p.deck.hero || [];
        const nomHeros = (p.hero && p.hero.name) || p.deck.name || "";
        return {
            heros: (p.hero && p.hero.id) || "",
            nomHeros,
            identite,
            deck: { ...p.deck, hero: identite, name: nomHeros },
        };
    });
    ecrireBrouillon(brouillon);
    window.location.href = "/campagne.html";
}''',
    ),
    # 8. nombre de joueurs figé
    (
        'function playerCountRow() {\n    if (state.mode.fixed) return null;',
        '''function playerCountRow() {
    if (state.mode.fixed) return null;
    // Le nombre de héros d'une campagne est arrêté à sa création : le changer
    // ici produirait une équipe que la campagne refuserait ensuite.
    if (creationCampagne()) return null;''',
    ),
    # 9. amorçage
    (
        '''    appliquerTutoriel(window.localStorage, null);
    synchroniserLangueServeur();
    try {
        await cards.load();''',
        '''    appliquerTutoriel(window.localStorage, null);
    synchroniserLangueServeur();
    if (creationCampagne()) {
        state.mode = MODES.find((m) => m.id === "campaign") || state.mode;
        state.playerCount = Math.max(1, Math.min(4, BROUILLON_CAMPAGNE.nbJoueurs | 0)) || 1;
        state.difficulty.base = BROUILLON_CAMPAGNE.difficulte === "expert" ? "expert" : "standard";
    }
    try {
        await cards.load();''',
    ),
    # 10. marqueur sur les schémas conservés
    (
        '// Schémas de journal de campagne : décrivent les entrées que le joueur reporte',
        '''// PLUS APPELÉ — conservé comme SOURCE. Depuis que la campagne a son écran
// (/campagne.html), la tuile « Campagne » redirige et plus rien ici n'est
// atteignable : isCampaignMode() est désormais toujours faux, donc
// renderCampaignPath, renderCampaignStory, renderCampaignJournal et
// campaignBoxes sont morts avec lui.
//
// On ne les supprime PAS encore : CAMPAIGN_SCHEMAS est le seul endroit du dépôt
// qui décrive les récompenses de campagne de sm, mut_gen, aoa, mts et
// next_evol. Ces schémas doivent être portés en fichiers
// data/campagnes/<code>.json (comme trors) AVANT que ce bloc disparaisse.
// Attention en les portant : le champ « Experimental Weapons » de trors était
// FAUX ici (il listait 04155-04158, les upgrades TECH, au lieu des
// attachements 04072-04075) — vérifier les autres boîtes carte par carte.
//
// Schémas de journal de campagne : décrivent les entrées que le joueur reporte''',
    ),
]

PATCHES_LAUNCHER = [
    (
        '    appliquerTutoriel(window.localStorage, state.mode);',
        '''    appliquerTutoriel(window.localStorage, state.mode);

    // Meme precaution pour la campagne : une partie ORDINAIRE doit desarmer le
    // contexte de campagne, sinon le panneau de recompenses s'ouvrirait a la
    // fin d'une partie qui n'a rien a voir et rattacherait sa victoire au
    // dernier scenario joue. L'ecran des campagnes, lui, pose la cle juste
    // avant d'appeler launch() en mode campagne : elle survit donc.
    if (!state.mode || state.mode.id !== "campaign") {
        try { window.localStorage.removeItem("mc-campagne-partie"); } catch (e) {}
    }''',
    ),
]


def appliquer(chemin, patches):
    texte = io.open(chemin, encoding="utf-8").read()
    poses, deja = 0, 0
    for avant, apres in patches:
        if apres in texte:
            deja += 1
            continue
        if avant not in texte:
            sys.exit("INTROUVABLE dans %s :\n%r" % (chemin, avant[:110]))
        if texte.count(avant) != 1:
            sys.exit("AMBIGU (%d) dans %s :\n%r" % (texte.count(avant), chemin, avant[:110]))
        texte = texte.replace(avant, apres)
        poses += 1
    io.open(chemin, "w", encoding="utf-8").write(texte)
    print("%s : %d pose(s), %d deja present(s)" % (os.path.basename(chemin), poses, deja))


appliquer(os.path.join(DOSSIER, "app.js"), PATCHES_APP)
appliquer(os.path.join(DOSSIER, "launcher.js"), PATCHES_LAUNCHER)
