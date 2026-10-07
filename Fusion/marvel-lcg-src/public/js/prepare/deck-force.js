// deck-force.js — « d'après notre code ce deck est illégal, mais tu peux forcer ».
//
// ⚠ POURQUOI (07/10/2026). L'import d'un deck marvelcdb REFUSAIT tout deck que
// les règles de construction jugent illégal. Ces règles sont du code écrit à la
// main, pack par pack (Spider-Woman, Fatalis, Ares, Cable…), et chaque erreur
// de notre part bloquait une joueuse sur un deck parfaitement légal (le refus
// de Cable du 22/09/2026). Elle ne doit plus être bloquée par NOTRE erreur.
//
// Le refus devient donc un AVERTISSEMENT que l'on peut passer. Et passer
// envoie, automatiquement, un rapport : le deck complet et les raisons du
// refus. C'est ainsi qu'on saura qui avait raison, la joueuse ou le code.
//
// Le module reste PUR pour tout ce qui se teste (messages, rapport) : Node
// l'exécute tel quel (tools/tests-lanceur/deck-force.test.mjs). Le navigateur
// n'est touché que dans `demanderForcage`, au moment de l'appel.
"use strict";

/** Le texte de la fenêtre de confirmation. `t` traduit, comme partout. */
export function messageDeForcage(hero, problemes, t = (x) => x) {
    return `${t("D’après notre code, ce deck n’est pas légal pour")} ${hero.name} :\n\n`
        + problemes.map((x) => "• " + x).join("\n")
        + `\n\n${t("Tu peux l’importer quand même. Si tu penses que c’est notre code qui se trompe, valide : ton deck et les raisons de notre refus nous seront envoyés automatiquement, pour qu’on vérifie.")}`
        + `\n\n${t("OK : importer et nous le signaler. Annuler : ne pas importer.")}`;
}

/** Les cartes du deck, comptées : « 2 x Jessica Drew ». */
function lignesDeCartes(ids, nomCarte) {
    const compte = new Map();
    for (const brut of ids) {
        const id = String(brut).split(",")[0];
        compte.set(id, (compte.get(id) || 0) + 1);
    }
    return [...compte.entries()].map(([id, n]) => `${n} x ${nomCarte(id) || "?"} (${id})`);
}

/** Le rapport qui part chez nous : { nom, description }. */
export function rapportDeckForce({ hero, deck, problemes, source, ecran, nomCarte }) {
    const description = [
        "Deck forcé : notre code l'a jugé illégal, la joueuse l'a importé quand même.",
        "",
        `Héros : ${hero.name} (${hero.heroCardId})`,
        `Deck : ${deck.name || "(sans nom)"}`,
        `Source : ${source || "inconnue"}`,
        `Écran : ${ecran}`,
        "",
        "Raisons du refus par notre code :",
        ...problemes.map((x) => "- " + x),
        "",
        `Cartes de signature (${(deck.hero_deck || []).length}) :`,
        ...lignesDeCartes(deck.hero_deck || [], nomCarte),
        "",
        `Cartes du deck (${(deck.player_deck || []).length}) :`,
        ...lignesDeCartes(deck.player_deck || [], nomCarte),
    ].join("\n");
    return { nom: "Deck forcé (envoi automatique)", description };
}

/** Envoie le rapport. Silencieux : un envoi raté ne doit jamais gêner l'import. */
async function envoyer(rapport, ecran) {
    try {
        await fetch("/post_rapport_bug", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nom: rapport.nom, description: rapport.description,
                ecran, journal: "", siege: "", capture: "",
            }),
        });
    } catch (e) { /* pas de site derrière, ou hors ligne : rien à faire */ }
}

/**
 * Demande à la joueuse si elle force. Rend `true` si elle valide (le rapport
 * est alors parti), `false` si elle renonce.
 */
export async function demanderForcage({ hero, deck, problemes, source, ecran, nomCarte, t }) {
    if (!window.confirm(messageDeForcage(hero, problemes, t))) return false;
    void envoyer(rapportDeckForce({ hero, deck, problemes, source, ecran, nomCarte }), ecran);
    return true;
}
