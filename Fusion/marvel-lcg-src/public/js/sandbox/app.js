// Bac a sable — panneau de test des cartes, a ouvrir a cote du plateau.
//
// Il ne redessine PAS le jeu : il pilote la partie en cours en deposant des
// commandes `Puzzle.*` via POST /sandbox_command. Le moteur les execute sur son
// propre fil, au moment ou il attend une decision du joueur (voir
// DeviceManager.QueueSandboxCommands).
//
// Les cartes se visent par leur NOM : FindOrCreateFace ne resout pas les
// identifiants et fabriquerait un doublon detache.
"use strict";
import { cards } from "/public/js/prepare/cards.js";
import { catalog } from "/public/js/prepare/catalog.js";

const TYPES_POSABLES = ["Ally", "Event", "Support", "Upgrade", "Resource",
    "Minion", "SideScheme", "Environment", "Attachment", "Treachery", "Villain"];

const etat = {
    onglet: "deck",
    recherche: "",
    heros: [],
    deck: [],       // cartes du deck du heros de la partie
    catalogue: [],  // toutes les cartes posables
    cible: "",      // nom de la carte visee par les boutons de triche
};

const $ = (s) => document.querySelector(s);

/* ---------------- Trace ---------------- */

function tracer(texte, genre = "info") {
    const zone = $("#sb-trace");
    const ligne = document.createElement("div");
    ligne.className = `sb-ligne-${genre}`;
    const h = new Date().toLocaleTimeString();
    ligne.textContent = `${h}  ${texte}`;
    zone.prepend(ligne);
}

/* ---------------- Moteur ---------------- */

async function envoyer(...commandes) {
    tracer("→ " + commandes.join(" ; "));
    try {
        const r = await fetch("/sandbox_command", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ commands: commandes }),
        });
        const data = await r.json().catch(() => ({}));
        if (!r.ok) {
            tracer("✗ " + (data.error || `HTTP ${r.status}`), "ko");
            return false;
        }
        tracer(`✓ ${data.count} commande(s) transmise(s)`, "ok");
        return true;
    } catch (e) {
        tracer("✗ " + e.message, "ko");
        return false;
    }
}

/** Echappe une chaine pour l'inserer dans une commande Python. */
function q(texte) {
    return "'" + String(texte).replace(/\\/g, "\\\\").replace(/'/g, "\\'") + "'";
}

/* ---------------- Donnees ---------------- */

function nomPropre(c) {
    return String((c && c.name) || "").replace(/^\*\s*/, "").trim();
}

async function chargerCatalogue() {
    const cs = await cards.load();
    const vus = new Map();
    for (const id of Object.keys(cs.const_card_dict)) {
        const c = cs.const_card_dict[id];
        if (!c || !TYPES_POSABLES.includes(String(c.type).replace(/ /g, ""))) continue;
        const nom = nomPropre(c);
        if (!nom || vus.has(nom)) continue;
        vus.set(nom, { id: String(c.id ?? id).split(",")[0] || id, nom, carte: c });
    }
    etat.catalogue = [...vus.values()].sort((a, b) => a.nom.localeCompare(b.nom));
}

/** Deck du heros de la partie en cours, devine depuis le nom de scene. */
async function chargerDeck() {
    let scene = "";
    try {
        scene = await (await fetch("/get_play_scene_name")).text();
    } catch (e) { /* pas de partie */ }
    $("#sb-etat").textContent = scene ? `partie : ${scene}` : "aucune partie détectée";

    const heros = await catalog.heroes();
    etat.heros = heros;
    // « rescue-rhino-(0)-(123) » -> on retient le premier segment.
    const cle = (scene.split("-")[0] || "").toLowerCase();
    const trouve = heros.find((h) => h.id.replace(/_/g, "").startsWith(cle.replace(/[^a-z]/g, "")))
        || heros.find((h) => h.name.toLowerCase().replace(/[^a-z]/g, "") === cle.replace(/[^a-z]/g, ""));

    const ids = new Set();
    if (trouve) {
        for (const x of [...(trouve.deck.hero_deck || []), ...(trouve.deck.player_deck || []),
                         ...(trouve.deck.obligations || []), ...(trouve.deck.nemesis_set || [])]) {
            ids.add(String(x).split(",")[0]);
        }
        tracer(`deck chargé : ${trouve.name} (${ids.size} cartes distinctes)`);
    } else {
        tracer("héros de la partie non identifié — onglet Deck vide", "ko");
    }
    const vus = new Map();
    for (const id of ids) {
        const c = cards.get(id);
        if (!c) continue;
        const nom = nomPropre(c);
        if (nom && !vus.has(nom)) vus.set(nom, { id, nom, carte: c });
    }
    etat.deck = [...vus.values()].sort((a, b) => a.nom.localeCompare(b.nom));
}

/* ---------------- Rendu ---------------- */

function rendreOnglets() {
    const zone = $("#sb-onglets");
    zone.replaceChildren();
    for (const [cle, libelle] of [["deck", `Deck (${etat.deck.length})`],
                                 ["tout", `Toutes les cartes (${etat.catalogue.length})`]]) {
        const b = document.createElement("button");
        b.className = "sb-onglet" + (etat.onglet === cle ? " est-actif" : "");
        b.textContent = libelle;
        b.onclick = () => { etat.onglet = cle; rendreOnglets(); rendreGrille(); };
        zone.append(b);
    }
}

function listeCourante() {
    const source = etat.onglet === "deck" ? etat.deck : etat.catalogue;
    const q2 = etat.recherche.toLowerCase();
    if (!q2) return source.slice(0, 400);
    return source.filter((x) => x.nom.toLowerCase().includes(q2)).slice(0, 400);
}

function rendreGrille() {
    const zone = $("#sb-grille");
    zone.replaceChildren();
    for (const { id, nom } of listeCourante()) {
        const b = document.createElement("button");
        b.className = "sb-carte";
        b.title = `Poser « ${nom} » en jeu`;
        const img = document.createElement("img");
        img.src = "/" + id;
        img.loading = "lazy";
        img.alt = nom;
        const t = document.createElement("b");
        t.textContent = nom;
        b.append(img, t);
        // On vise par IDENTIFIANT, pas par nom : `IsName` reconnait les
        // identifiants (via IsCardId), donc une carte deja en jeu ou dans un
        // deck est retrouvee — et si elle n'existe nulle part, `CreateCard` sait
        // la fabriquer a partir de son identifiant, jamais a partir d'un nom.
        b.onclick = async () => {
            await envoyer(`Puzzle.PutIntoPlay(${q(id)})`);
            etat.cible = id;
            rendreCibles();
        };
        zone.append(b);
    }
}

function rendreCibles() {
    const zone = $("#sb-cibles");
    zone.replaceChildren();
    const champ = document.createElement("input");
    champ.className = "sb-cible";
    champ.placeholder = "Carte visée (nom exact)";
    champ.value = etat.cible;
    champ.oninput = (e) => { etat.cible = e.target.value; };
    zone.append(champ);
}

function rendreBoutons() {
    const zone = $("#sb-boutons");
    zone.replaceChildren();

    const valeur = document.createElement("input");
    valeur.className = "sb-champ";
    valeur.type = "number";
    valeur.value = "3";
    valeur.title = "Valeur utilisée par les boutons chiffrés";

    const ajouter = (libelle, faire, titre) => {
        const b = document.createElement("button");
        b.className = "sb-bouton";
        b.textContent = libelle;
        if (titre) b.title = titre;
        b.onclick = () => faire(Number(valeur.value) || 0);
        zone.append(b);
    };

    const cible = () => q(etat.cible);
    zone.append(valeur);

    ajouter("dégâts", (v) => envoyer(`Puzzle.Damage(${cible()}, ${v})`));
    ajouter("soin", (v) => envoyer(`Puzzle.Heal(${cible()}, ${v})`));
    ajouter("menace =", (v) => envoyer(`Puzzle.SetThreat(${cible()}, ${v})`),
        "Fixe la menace du complot visé");
    ajouter("+ menace", (v) => envoyer(`Puzzle.PlaceThreat(${cible()}, ${v})`));
    ajouter("compteurs", (v) => envoyer(`Puzzle.Counter(${cible()}, 'counter', ${v})`));

    ajouter("préparer", () => envoyer(`Puzzle.Ready(${cible()})`));
    ajouter("épuiser", () => envoyer(`Puzzle.Exhaust(${cible()})`));
    ajouter("étourdir", () => envoyer(`Puzzle.Stun(${cible()})`));
    ajouter("confondre", () => envoyer(`Puzzle.Confuse(${cible()})`));
    ajouter("coriace", () => envoyer(`Puzzle.Tough(${cible()})`));
    ajouter("défausser", () => envoyer(`Puzzle.Discard(${cible()})`));
    ajouter("retirer du jeu", () => envoyer(`Puzzle.Remove(${cible()})`));
    ajouter("révéler", () => envoyer(`Puzzle.Reveal(${cible()})`));

    ajouter("changer de forme", () => envoyer(`Puzzle.ChangeForm(${cible()})`),
        "Vise l'identité par son nom (ex. Pepper Potts)");
    ajouter("piocher", (v) => envoyer(`Puzzle.Draw(${v})`));
    ajouter("en main", () => envoyer(`Puzzle.Gain(${cible()})`),
        "Ajoute la carte visée à la main — pour la jouer normalement, en payant");

    ajouter("décor vilain", () => remplirCoteVilain(),
        "Pose deux sbires et deux complots annexes pour avoir des cibles");
}

/** Pose de quoi tester : des sbires a frapper, des complots a contrecarrer.
 *  Cartes du Core Set, disponibles quel que soit le scenario, visees par
 *  identifiant (seule forme que `CreateCard` sait fabriquer). */
const DECOR_VILAIN = [
    "01107",  // Breakin' & Takin'      (complot annexe)
    "01109",  // Bomb Scare             (complot annexe)
    "01120",  // Armored Guard          (sbire)
    "01126",  // Illegal Arms Factory   (complot annexe)
];

async function remplirCoteVilain() {
    tracer("mise en place du décor vilain…");
    for (const nom of DECOR_VILAIN) {
        await envoyer(`Puzzle.PutIntoPlay(${q(nom)})`);
    }
}

/* ---------------- Demarrage ---------------- */

/** Consigne laissee par l'assistant en mode bac a sable : les cartes a poser au
 *  demarrage. On l'execute ICI parce que cette page survit a la navigation vers
 *  le plateau, contrairement a l'assistant. Le moteur ne draine sa file que
 *  lorsqu'il attend une decision : on reessaie donc jusqu'a ce que ce soit le
 *  cas, plutot que de parier sur un delai fixe. */
const CLE_GARNISSAGE = "mc_sandbox_garnir";

async function garnirSiDemande() {
    let ids;
    try {
        const brut = window.localStorage.getItem(CLE_GARNISSAGE);
        if (!brut) return;
        ids = JSON.parse(brut);
        window.localStorage.removeItem(CLE_GARNISSAGE);
    } catch (e) { return; }
    if (!Array.isArray(ids) || !ids.length) return;

    tracer(`garnissage du côté vilain : ${ids.length} carte(s)…`);
    for (const id of ids) {
        const c = cards.get(id);
        tracer(`  ${id} ${c ? nomPropre(c) : ""}`);
    }
    // La partie doit avoir fini sa mise en place ; on laisse quelques essais.
    for (let essai = 0; essai < 10; essai++) {
        const ok = await envoyer(...ids.map((id) => `Puzzle.PutIntoPlay(${q(id)})`));
        if (ok) return;
        await new Promise((r) => setTimeout(r, 1500));
    }
    tracer("garnissage abandonné : la partie n'était pas prête", "ko");
}

async function demarrer() {
    $("#sb-recherche").oninput = (e) => { etat.recherche = e.target.value; rendreGrille(); };
    $("#sb-limites").onchange = (e) => {
        tracer(e.target.checked
            ? "limites levées (à implémenter côté moteur)"
            : "limites rétablies");
    };
    rendreCibles();
    rendreBoutons();
    tracer("chargement du catalogue…");
    await chargerCatalogue();
    await chargerDeck();
    rendreOnglets();
    rendreGrille();
    tracer("prêt — clique une carte pour la poser en jeu", "ok");
    await garnirSiDemande();
}

demarrer();
