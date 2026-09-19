// app.js — l'éditeur de palettes de héros, réservé au compte auteur.
//
// Demande de l'utilisateur, 18/09/2026 : « pour chaque personnage, on a une
// couleur en bas à droite de l'écran, et certaines ne sont pas correctes. Un
// mode disponible que pour moi, où je peux mettre le hex principal, secondaire
// et tertiaire de chaque personnage. »
//
// ⚠ CE SCRIPT NE DÉCIDE DE RIEN. Il demande `/get_site_admin` pour afficher un
// message honnête et griser ce qui ne servirait à rien, mais c'est le moteur
// qui refuse l'écriture : `/save_palette_heros` rend 403 à qui n'est pas
// l'administrateur du site, assis au siège 0. Un invité qui lirait ce fichier
// n'y gagne rien.
//
// ⚠ LES CORRECTIONS NE TOUCHENT PAS LE RELEVÉ GÉNÉRÉ. Elles vont dans
// `data/palettes-heros-corrections.json`, posé par-dessus
// `data/palettes-heros.json` : `outils/palettes-heros.py` peut être relancé
// sans effacer le travail à la main.
//
// ⚠ UNE IDENTITÉ, PAS UNE FACE. Les deux faces d'un héros partagent leur
// palette : se transformer ne doit pas faire sauter la couleur du fond. On
// écrit donc toutes les faces d'un coup.

"use strict";

import {
    hexVersRgb, rgbVersHex, fondDe, grouperParIdentite, couleursDepuisChamps, memePalette,
} from "/public/js/palettes/couleurs.js";

const PLATEAU_SOMBRE = "#101218";
const MESSAGE = document.getElementById("message");
const LISTE = document.getElementById("liste");
const AVANCEMENT = document.getElementById("avancement");
const RECHERCHE = document.getElementById("recherche");
const SEULEMENT_CORRIGES = document.getElementById("seulement-corriges");
const MODELE = document.getElementById("modele-ligne");

/** État de la page. `generees` sert à proposer le retour à la couleur mesurée. */
const etat = {
    administrateur: false,
    generees: new Map(),     // identité -> couleurs mesurées
    corrections: new Set(),  // identités corrigées à la main
    lignes: [],              // { identite, cartes, nom, noeud, champs, ... }
};

async function json(url) {
    const reponse = await fetch(url, { cache: "no-store" });
    if (!reponse.ok) throw new Error(url + " → HTTP " + reponse.status);
    const type = reponse.headers.get("content-type") || "";
    if (!type.includes("json")) {
        // ⚠ Le moteur sert une IMAGE pour tout chemin inconnu : un 200 ne
        // prouve pas que la route existe. Même piège que le halo du plateau.
        throw new Error(
            `La route ${url} n'existe pas sur ce serveur (il a répondu « ${type} »). ` +
            "Il tourne sans doute sur une version d'avant cet éditeur.");
    }
    return reponse.json();
}

/** Le nom lisible de chaque identité, tiré du catalogue des cartes. */
function nomsDesCartes(cartesParGroupe) {
    const noms = new Map();
    for (const cartes of Object.values(cartesParGroupe || {})) {
        if (!Array.isArray(cartes)) continue;
        for (const carte of cartes) {
            if (!carte || !carte.card_id || !carte.name) continue;
            noms.set(String(carte.card_id), String(carte.name).replace(/^\* /, ""));
        }
    }
    return noms;
}

/** Ce que la ligne enverrait au serveur, ou l'erreur qui l'en empêche. */
function lectureDe(ligne) {
    const champs = ligne.champs.map((champ) => champ.value);
    return couleursDepuisChamps(champs);
}

function rafraichirApercu(ligne) {
    const lu = lectureDe(ligne);
    const couleurs = lu.erreur ? ligne.couleurs : lu.couleurs;
    ligne.apercu.style.background = fondDe(couleurs, PLATEAU_SOMBRE);
    for (const champ of ligne.champs) {
        const valeur = String(champ.value || "").trim();
        champ.classList.toggle("p-faute", valeur !== "" && hexVersRgb(valeur) === null);
    }
    const genere = etat.generees.get(ligne.identite) || [];
    const modifiee = !lu.erreur && !memePalette(lu.couleurs, ligne.couleurs);
    ligne.noeud.classList.toggle("p-modifiee", modifiee);
    ligne.enregistrer.disabled = !etat.administrateur || Boolean(lu.erreur) || !modifiee;
    ligne.annuler.hidden = !etat.corrections.has(ligne.identite) || genere.length === 0;
    ligne.annuler.disabled = !etat.administrateur;
    if (lu.erreur === "hex") dire(ligne, "hex incomplet", "p-echec");
    else if (lu.erreur === "trou") dire(ligne, "un trou au milieu", "p-echec");
    else if (lu.erreur === "vide") dire(ligne, "au moins une couleur", "p-echec");
    else if (modifiee) dire(ligne, "modifiée, pas encore enregistrée", "");
    else dire(ligne, "", "");
}

function dire(ligne, texte, classe) {
    ligne.retour.textContent = texte;
    ligne.retour.className = "p-retour-serveur" + (classe ? " " + classe : "");
}

function poserCouleurs(ligne, couleurs) {
    ligne.couleurs = couleurs.map((c) => [c[0], c[1], c[2]]);
    ligne.champs.forEach((champ, rang) => {
        const couleur = couleurs[rang];
        champ.value = couleur ? rgbVersHex(couleur) : "";
    });
    ligne.pastilles.forEach((pastille, rang) => {
        const couleur = couleurs[rang];
        pastille.value = couleur ? rgbVersHex(couleur) : "#000000";
    });
    ligne.noeud.classList.toggle("p-corrigee", etat.corrections.has(ligne.identite));
    ligne.etat.textContent = etat.corrections.has(ligne.identite)
        ? "corrigée à la main" : "mesurée sur le contour des cartes";
    rafraichirApercu(ligne);
}

async function enregistrer(ligne) {
    const lu = lectureDe(ligne);
    if (lu.erreur) return;
    await envoyer(ligne, { cartes: ligne.cartes, couleurs: lu.couleurs }, () => {
        etat.corrections.add(ligne.identite);
        poserCouleurs(ligne, lu.couleurs);
        dire(ligne, "enregistrée", "p-ok");
    });
}

async function revenirAuMesure(ligne) {
    const genere = etat.generees.get(ligne.identite);
    if (!genere || genere.length === 0) return;
    await envoyer(ligne, { cartes: ligne.cartes, oublier: true }, () => {
        etat.corrections.delete(ligne.identite);
        poserCouleurs(ligne, genere);
        dire(ligne, "revenue à la couleur mesurée", "p-ok");
    });
}

async function envoyer(ligne, corps, apres) {
    ligne.enregistrer.disabled = true;
    ligne.annuler.disabled = true;
    dire(ligne, "envoi…", "");
    try {
        const reponse = await fetch("/save_palette_heros", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(corps),
        });
        if (reponse.status === 403) {
            dire(ligne, "refusé : réservé au compte auteur", "p-echec");
            return;
        }
        if (!reponse.ok) {
            dire(ligne, "refusé (HTTP " + reponse.status + ")", "p-echec");
            return;
        }
        const data = await reponse.json();
        apres();
        compter(data && data.corrigees);
    } catch (erreur) {
        // ⚠ On ne fait PAS comme si c'était enregistré : la ligne garde sa
        // valeur d'avant, et le message dit que rien n'est parti.
        dire(ligne, "réseau : rien n'a été enregistré", "p-echec");
    } finally {
        ligne.enregistrer.disabled = !etat.administrateur;
        ligne.annuler.disabled = !etat.administrateur;
        rafraichirApercu(ligne);
    }
}

function compter(corrigees) {
    const total = etat.lignes.length;
    const nb = typeof corrigees === "number" ? corrigees : etat.corrections.size;
    AVANCEMENT.textContent = total
        ? `${total} identités · ${etat.corrections.size} corrigée(s)` + (nb ? "" : "")
        : "";
}

function filtrer() {
    const cherche = (RECHERCHE.value || "").trim().toLowerCase();
    const seulement = SEULEMENT_CORRIGES.checked;
    for (const ligne of etat.lignes) {
        const parNom = !cherche
            || ligne.nom.toLowerCase().includes(cherche)
            || ligne.identite.toLowerCase().includes(cherche);
        const parEtat = !seulement || etat.corrections.has(ligne.identite);
        ligne.noeud.hidden = !(parNom && parEtat);
    }
}

function construireLigne(groupe, nom) {
    const noeud = MODELE.content.firstElementChild.cloneNode(true);
    const ligne = {
        identite: groupe.identite,
        cartes: groupe.cartes,
        nom,
        noeud,
        couleurs: groupe.couleurs,
        champs: Array.from(noeud.querySelectorAll(".p-hex")),
        pastilles: Array.from(noeud.querySelectorAll(".p-pastille")),
        apercu: noeud.querySelector(".p-apercu"),
        etat: noeud.querySelector(".p-etat"),
        retour: noeud.querySelector(".p-retour-serveur"),
        enregistrer: noeud.querySelector(".p-enregistrer"),
        annuler: noeud.querySelector(".p-annuler"),
    };
    noeud.querySelector(".p-nom").textContent = nom;
    noeud.querySelector(".p-cartes").textContent = groupe.cartes.join(" · ");
    const scan = noeud.querySelector(".p-scan");
    scan.src = "/" + groupe.cartes[0];
    scan.alt = nom;

    ligne.champs.forEach((champ, rang) => {
        champ.addEventListener("input", () => {
            const rgb = hexVersRgb(champ.value);
            if (rgb) ligne.pastilles[rang].value = rgbVersHex(rgb);
            rafraichirApercu(ligne);
        });
    });
    ligne.pastilles.forEach((pastille, rang) => {
        pastille.addEventListener("input", () => {
            ligne.champs[rang].value = pastille.value;
            rafraichirApercu(ligne);
        });
    });
    ligne.enregistrer.addEventListener("click", () => { void enregistrer(ligne); });
    ligne.annuler.addEventListener("click", () => { void revenirAuMesure(ligne); });
    return ligne;
}

async function charger() {
    const [releve, cartesParGroupe, admin] = await Promise.all([
        json("/get_palettes_heros"),
        json("get_cards_json?"),
        json("/get_site_admin").catch(() => ({ url: "" })),
    ]);

    etat.administrateur = Boolean(admin && admin.url);
    const palettes = (releve && releve.palettes) || {};
    const corrections = (releve && releve.corrections) || {};
    const noms = nomsDesCartes(cartesParGroupe);

    // Le relevé GÉNÉRÉ seul : palettes corrigées retirées de la vue, pour que
    // « Couleur mesurée » sache à quoi revenir.
    const genereesParCarte = Object.assign({}, palettes);
    for (const carte of Object.keys(corrections)) delete genereesParCarte[carte];
    for (const [identite, groupe] of grouperParIdentite(genereesParCarte)) {
        etat.generees.set(identite, groupe.couleurs);
    }
    for (const carte of Object.keys(corrections)) {
        etat.corrections.add(carte.replace(/[a-z]$/, ""));
    }

    const groupes = Array.from(grouperParIdentite(palettes).values());
    groupes.sort((a, b) => a.identite.localeCompare(b.identite, "fr", { numeric: true }));

    const fragment = document.createDocumentFragment();
    for (const groupe of groupes) {
        const nom = noms.get(groupe.cartes[0]) || groupe.identite;
        const ligne = construireLigne(groupe, nom);
        etat.lignes.push(ligne);
        fragment.append(ligne.noeud);
    }
    LISTE.append(fragment);
    for (const ligne of etat.lignes) poserCouleurs(ligne, ligne.couleurs);

    LISTE.hidden = false;
    compter();
    if (!etat.administrateur) {
        MESSAGE.textContent =
            "Lecture seule : cette page ne sert qu'au compte auteur, connecté depuis le "
            + "site et assis à son propre siège. Le moteur refusera toute écriture.";
        MESSAGE.className = "p-message p-alerte";
    } else {
        MESSAGE.hidden = true;
    }
}

RECHERCHE.addEventListener("input", filtrer);
SEULEMENT_CORRIGES.addEventListener("change", filtrer);

charger().catch((erreur) => {
    MESSAGE.textContent = String((erreur && erreur.message) || erreur);
    MESSAGE.className = "p-message p-echec";
    MESSAGE.hidden = false;
});
