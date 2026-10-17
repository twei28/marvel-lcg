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
    coordonneesDansCanvas, moyenneAutour,
} from "/public/js/palettes/couleurs.js";

const PLATEAU_SOMBRE = "#101218";
const MESSAGE = document.getElementById("message");
const LISTE = document.getElementById("liste");
const AVANCEMENT = document.getElementById("avancement");
const RECHERCHE = document.getElementById("recherche");
const ONGLETS = document.getElementById("onglets");
const ETATS = document.getElementById("etats");
const MODELE = document.getElementById("modele-ligne");
const LOUPE = document.getElementById("loupe");
const LOUPE_FOND = document.getElementById("loupe-fond");
const LOUPE_NOM = document.getElementById("loupe-nom");
const LOUPE_FACES = document.getElementById("loupe-faces");
const LOUPE_CIBLES = document.getElementById("loupe-cibles");
const LOUPE_CANVAS = document.getElementById("loupe-canvas");
const LOUPE_APERCU = document.getElementById("loupe-apercu");
const SOUS_CURSEUR = document.getElementById("loupe-sous-curseur");
const SOUS_PASTILLE = document.getElementById("loupe-pastille");
const SOUS_HEX = document.getElementById("loupe-hex");
const LIBELLES_RANG = ["Principale", "Secondaire", "Tertiaire"];

/** La pipette de Chrome, quand le navigateur l'a. Firefox et Safari ne
 *  l'implémentent pas : le bouton reste alors caché, et la pipette sur la
 *  carte agrandie suffit. */
const PIPETTE_ECRAN = typeof window !== "undefined" && "EyeDropper" in window;

/** État de la page. `generees` sert à proposer le retour à la couleur mesurée. */
const etat = {
    administrateur: false,
    loupe: null,             // { ligne, carte, rang, pixels, largeur, hauteur }
    generees: new Map(),     // identité -> couleurs mesurées
    corrections: new Set(),  // identités corrigées à la main
    lignes: [],              // { identite, cartes, nom, noeud, champs, ... }
    type: "heros",           // l'onglet : « heros » ou « mechants »
    montre: "traiter",       // « traiter », « traites » ou « tous »
};

/** Une ligne est TRAITÉE quand l'une de ses cartes a une correction enregistrée : soit
 *  retouchée à la main, soit validée telle quelle avec le bouton « Traité ». C'est le même
 *  fichier de corrections, donc rien de plus à stocker côté serveur. */
const sansLettre = (carte) => String(carte).replace(/[a-z]$/, "");
const estTraitee = (ligne) => ligne.cartes.some((carte) => etat.corrections.has(sansLettre(carte)));
const marquerTraitee = (ligne) => { for (const carte of ligne.cartes) etat.corrections.add(sansLettre(carte)); };
const oublierTraitee = (ligne) => { for (const carte of ligne.cartes) etat.corrections.delete(sansLettre(carte)); };

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

/** Pour chaque carte : son nom, son type et son set. Sert à distinguer les méchants des héros
 *  et à regrouper les phases d'un même méchant. */
function infosDesCartes(cartesParGroupe) {
    const infos = new Map();
    for (const cartes of Object.values(cartesParGroupe || {})) {
        if (!Array.isArray(cartes)) continue;
        for (const carte of cartes) {
            if (!carte || !carte.card_id) continue;
            infos.set(String(carte.card_id), { type: carte.type || "", set: carte.set_name || "" });
        }
    }
    return infos;
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
    // Un méchant n'a que DEUX couleurs : le troisième champ est caché et ignoré.
    const champs = ligne.champs.slice(0, ligne.type === "mechants" ? 2 : 3).map((champ) => champ.value);
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
    ligne.annuler.hidden = !estTraitee(ligne) || genere.length === 0;
    ligne.annuler.disabled = !etat.administrateur;
    ligne.traite.disabled = !etat.administrateur || Boolean(lu.erreur);
    ligne.traite.classList.toggle("p-deja", estTraitee(ligne) && !modifiee);
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
        const couleur = ligne.type === "mechants" && rang > 1 ? null : couleurs[rang];
        champ.value = couleur ? rgbVersHex(couleur) : "";
    });
    ligne.pastilles.forEach((pastille, rang) => {
        const couleur = couleurs[rang];
        pastille.value = couleur ? rgbVersHex(couleur) : "#000000";
    });
    ligne.noeud.classList.toggle("p-corrigee", estTraitee(ligne));
    ligne.etat.textContent = estTraitee(ligne)
        ? "traitée" : "à traiter · mesurée sur le contour des cartes";
    rafraichirApercu(ligne);
}

async function enregistrer(ligne) {
    const lu = lectureDe(ligne);
    if (lu.erreur) return;
    await envoyer(ligne, { cartes: ligne.cartes, couleurs: lu.couleurs }, () => {
        marquerTraitee(ligne);
        poserCouleurs(ligne, lu.couleurs);
        dire(ligne, "enregistrée", "p-ok");
    });
}

/** « Traité » : enregistre les couleurs affichées, même inchangées, et range la ligne. */
async function traiter(ligne) {
    const lu = lectureDe(ligne);
    if (lu.erreur) return;
    await envoyer(ligne, { cartes: ligne.cartes, couleurs: lu.couleurs }, () => {
        marquerTraitee(ligne);
        poserCouleurs(ligne, lu.couleurs);
        dire(ligne, "traitée", "p-ok");
        filtrer();
    });
}

async function revenirAuMesure(ligne) {
    const genere = etat.generees.get(ligne.identite);
    if (!genere || genere.length === 0) return;
    await envoyer(ligne, { cartes: ligne.cartes, oublier: true }, () => {
        oublierTraitee(ligne);
        poserCouleurs(ligne, genere);
        dire(ligne, "revenue à la couleur mesurée", "p-ok");
    });
}

async function envoyer(ligne, corps, apres) {
    ligne.enregistrer.disabled = true;
    ligne.annuler.disabled = true;
    ligne.traite.disabled = true;
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
        ligne.traite.disabled = !etat.administrateur;
        rafraichirApercu(ligne);
    }
}

function compter() {
    const deLOnglet = etat.lignes.filter((l) => l.type === etat.type);
    const traitees = deLOnglet.filter(estTraitee).length;
    AVANCEMENT.textContent = deLOnglet.length
        ? `${traitees} / ${deLOnglet.length} traités · ${deLOnglet.length - traitees} à traiter`
        : "";
    for (const bouton of ONGLETS.querySelectorAll("button")) {
        const lot = etat.lignes.filter((l) => l.type === bouton.dataset.type);
        const reste = lot.filter((l) => !estTraitee(l)).length;
        bouton.textContent = (bouton.dataset.type === "heros" ? "Héros" : "Méchants")
            + (reste ? ` (${reste})` : " ✓");
    }
    const traites = deLOnglet.filter(estTraitee).length;
    ETATS.querySelector('[data-etat="traiter"]').textContent = `À traiter (${deLOnglet.length - traites})`;
    ETATS.querySelector('[data-etat="traites"]').textContent = `Traités (${traites})`;
    ETATS.querySelector('[data-etat="tous"]').textContent = `Tous (${deLOnglet.length})`;
}

function filtrer() {
    const cherche = (RECHERCHE.value || "").trim().toLowerCase();
    let visibles = 0;
    for (const ligne of etat.lignes) {
        const parType = ligne.type === etat.type;
        const parNom = !cherche
            || ligne.nom.toLowerCase().includes(cherche)
            || ligne.identite.toLowerCase().includes(cherche);
        const traitee = estTraitee(ligne);
        const parEtat = etat.montre === "tous" || (etat.montre === "traiter" ? !traitee : traitee);
        const voir = parType && parNom && parEtat;
        ligne.noeud.hidden = !voir;
        if (voir) visibles += 1;
    }
    compter();
    if (!MESSAGE.classList.contains("p-alerte") && !MESSAGE.classList.contains("p-echec")) {
        MESSAGE.hidden = visibles > 0;
        if (!visibles) {
            MESSAGE.textContent = etat.montre === "traiter"
                ? "Rien à traiter ici : tout est fait. « Traités » les ramène pour les changer."
                : "Rien à montrer.";
            MESSAGE.className = "p-message";
        }
    }
}

/* ------------------------------------------------------------- la loupe --
 *
 * Demande du 19/09/2026 : « fais en sorte qu'on puisse agrandir la carte, et
 * je joue sur Chrome, donc il y a la pipette de Chrome à part ».
 *
 * ⚠ LA VIGNETTE NE SUFFIT PAS. Elle fait 52 px de large : on n'y vise pas un
 * détail d'illustration. La pipette travaille donc sur la carte AGRANDIE,
 * dessinée dans un canvas à sa taille réelle.
 *
 * ⚠ LE CANVAS PEUT LIRE SES PIXELS PARCE QUE LE MOTEUR SERT LE SCAN LUI-MÊME.
 * Une image venue d'un autre domaine « salit » le canvas et `getImageData`
 * lève. Ici `/<card_id>` est servi par le moteur, sur la même origine que la
 * page : rien à négocier. Si cela changeait un jour, la pipette de Chrome
 * resterait, elle ne lit pas l'image mais l'écran.
 */

/** Pose une couleur dans un champ de la ligne, et rafraîchit tout ce qui suit. */
function poserChamp(ligne, rang, couleur) {
    ligne.champs[rang].value = rgbVersHex(couleur);
    ligne.pastilles[rang].value = rgbVersHex(couleur);
    rafraichirApercu(ligne);
    if (etat.loupe && etat.loupe.ligne === ligne) rafraichirLoupe();
}

/** Les trois boutons « quelle couleur je remplis », avec leur pastille. */
function dessinerCibles() {
    const loupe = etat.loupe;
    LOUPE_CIBLES.replaceChildren(...LIBELLES_RANG.map((libelle, rang) => {
        const bouton = document.createElement("button");
        bouton.type = "button";
        bouton.className = rang === loupe.rang ? "on" : "";
        const puce = document.createElement("span");
        puce.className = "p-puce";
        const valeur = hexVersRgb(loupe.ligne.champs[rang].value);
        if (valeur) puce.style.background = rgbVersHex(valeur);
        bouton.append(puce, document.createTextNode(`${rang + 1}. ${libelle}`));
        bouton.addEventListener("click", () => { loupe.rang = rang; dessinerCibles(); });
        return bouton;
    }));
}

function rafraichirLoupe() {
    if (!etat.loupe) return;
    const lu = lectureDe(etat.loupe.ligne);
    LOUPE_APERCU.style.background = fondDe(
        lu.erreur ? etat.loupe.ligne.couleurs : lu.couleurs, PLATEAU_SOMBRE);
    dessinerCibles();
}

/** Charge une face dans le canvas et retient ses pixels. */
function dessinerCarte(carte) {
    const image = new Image();
    image.decoding = "async";
    image.addEventListener("load", () => {
        if (!etat.loupe) return;
        LOUPE_CANVAS.width = image.naturalWidth;
        LOUPE_CANVAS.height = image.naturalHeight;
        const ctx = LOUPE_CANVAS.getContext("2d", { willReadFrequently: true });
        ctx.drawImage(image, 0, 0);
        try {
            const donnees = ctx.getImageData(0, 0, LOUPE_CANVAS.width, LOUPE_CANVAS.height);
            etat.loupe.pixels = donnees.data;
            etat.loupe.largeur = donnees.width;
            etat.loupe.hauteur = donnees.height;
        } catch (erreur) {
            // Canvas « sali » : ne devrait pas arriver, le scan vient du moteur.
            // On le DIT plutôt que de laisser une pipette qui ne répond pas.
            etat.loupe.pixels = null;
            SOUS_HEX.textContent = "pipette impossible sur cette image";
        }
    });
    image.addEventListener("error", () => { if (etat.loupe) etat.loupe.pixels = null; });
    image.src = "/" + carte;
    etat.loupe.carte = carte;
    LOUPE_FACES.replaceChildren(...etat.loupe.ligne.cartes.map((id) => {
        const bouton = document.createElement("button");
        bouton.type = "button";
        bouton.textContent = id;
        bouton.className = id === carte ? "on" : "";
        bouton.addEventListener("click", () => dessinerCarte(id));
        return bouton;
    }));
}

function ouvrirLoupe(ligne) {
    etat.loupe = { ligne, carte: ligne.cartes[0], rang: 0, pixels: null, largeur: 0, hauteur: 0 };
    LOUPE_NOM.textContent = ligne.nom;
    LOUPE.hidden = false;
    dessinerCarte(ligne.cartes[0]);
    rafraichirLoupe();
}

function fermerLoupe() {
    etat.loupe = null;
    LOUPE.hidden = true;
    SOUS_CURSEUR.hidden = true;
}

/** La couleur sous le curseur, moyennée sur un petit carré. */
function couleurSousLeCurseur(evenement) {
    const loupe = etat.loupe;
    if (!loupe || !loupe.pixels) return null;
    const point = coordonneesDansCanvas(
        LOUPE_CANVAS.getBoundingClientRect(), loupe.largeur, loupe.hauteur,
        evenement.clientX, evenement.clientY);
    if (!point) return null;
    return moyenneAutour(loupe.pixels, loupe.largeur, loupe.hauteur, point.x, point.y, 2);
}

LOUPE_CANVAS.addEventListener("mousemove", (evenement) => {
    const couleur = couleurSousLeCurseur(evenement);
    if (!couleur) { SOUS_CURSEUR.hidden = true; return; }
    SOUS_CURSEUR.hidden = false;
    SOUS_CURSEUR.style.left = (evenement.clientX + 16) + "px";
    SOUS_CURSEUR.style.top = (evenement.clientY + 16) + "px";
    SOUS_PASTILLE.style.background = rgbVersHex(couleur);
    SOUS_HEX.textContent = rgbVersHex(couleur);
});
LOUPE_CANVAS.addEventListener("mouseleave", () => { SOUS_CURSEUR.hidden = true; });
LOUPE_CANVAS.addEventListener("click", (evenement) => {
    const loupe = etat.loupe;
    const couleur = couleurSousLeCurseur(evenement);
    if (!loupe || !couleur) return;
    poserChamp(loupe.ligne, loupe.rang, couleur);
    // ⚠ ON AVANCE TOUT SEUL. Trois clics remplissent les trois couleurs : c'est
    // la façon dont on relève une carte, du plus dense au plus diffus. Arrivé
    // au bout, on reste sur la troisième plutôt que de repartir au début et
    // d'écraser la principale sans prévenir.
    loupe.rang = Math.min(loupe.rang + 1, LIBELLES_RANG.length - 1);
    dessinerCibles();
});
document.getElementById("loupe-fermer").addEventListener("click", fermerLoupe);
LOUPE_FOND.addEventListener("click", fermerLoupe);
document.addEventListener("keydown", (evenement) => {
    if (!etat.loupe) return;
    if (evenement.key === "Escape") { fermerLoupe(); return; }
    const rang = ["1", "2", "3"].indexOf(evenement.key);
    if (rang >= 0) { etat.loupe.rang = rang; dessinerCibles(); }
});

function construireLigne(groupe, nom, type) {
    const noeud = MODELE.content.firstElementChild.cloneNode(true);
    const ligne = {
        type,
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
        traite: noeud.querySelector(".p-traite"),
        annuler: noeud.querySelector(".p-annuler"),
    };
    noeud.querySelector(".p-nom").textContent = nom;
    if (type === "mechants") noeud.classList.add("p-deux-couleurs");
    noeud.querySelector(".p-cartes").textContent = groupe.cartes.join(" · ");
    const scan = noeud.querySelector(".p-scan");
    scan.src = "/" + groupe.cartes[0];
    scan.alt = nom;
    noeud.querySelector(".p-scan-bouton").addEventListener("click", () => ouvrirLoupe(ligne));

    // La pipette de Chrome : elle prélève n'importe où à l'écran, donc aussi
    // sur une image ouverte à côté. Cachée ailleurs (Firefox, Safari).
    for (const bouton of noeud.querySelectorAll(".p-pipette-ecran")) {
        if (!PIPETTE_ECRAN) continue;
        bouton.hidden = false;
        const rang = Number(bouton.dataset.rang);
        bouton.addEventListener("click", async () => {
            try {
                const choix = await new window.EyeDropper().open();
                const rgb = hexVersRgb(choix && choix.sRGBHex);
                if (rgb) poserChamp(ligne, rang, rgb);
            } catch (erreur) {
                // Échap pendant le prélèvement : ce n'est pas une panne.
            }
        });
    }

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
    ligne.traite.addEventListener("click", () => { void traiter(ligne); });
    ligne.annuler.addEventListener("click", () => { void revenirAuMesure(ligne); });
    return ligne;
}

async function charger() {
    const [releve, cartesParGroupe, admin] = await Promise.all([
        json("/get_palettes_heros"),
        json("get_cards_json?"),
        json("/get_site_admin").catch(() => ({ url: "" })),
    ]);

    // « Vue joueur » (08/10/2026, lien-admin.js) : l'administrateur voit la page comme un joueur.
    let vueJoueur = false;
    try { vueJoueur = localStorage.getItem("mc_vue_joueur") === "oui"; } catch (e) { vueJoueur = false; }
    etat.administrateur = Boolean(admin && admin.url) && !vueJoueur;
    const palettes = (releve && releve.palettes) || {};
    const corrections = (releve && releve.corrections) || {};
    const noms = nomsDesCartes(cartesParGroupe);
    const infos = infosDesCartes(cartesParGroupe);

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

    // Les héros : une ligne par identité (les deux faces ensemble). Les méchants : une ligne
    // par MÉCHANT, toutes ses phases ensemble (regroupées par set), pour que la couleur ne saute
    // pas quand il passe à la phase suivante.
    const estMechant = (carte) => (infos.get(carte) || {}).type === "Villain";
    const heros = {};
    const mechants = new Map();
    for (const [carte, couleurs] of Object.entries(palettes)) {
        if (estMechant(carte)) {
            const set = (infos.get(carte) || {}).set || carte;
            const groupe = mechants.get(set) || { identite: sansLettre(carte), cartes: [], couleurs: [], set };
            groupe.cartes.push(carte);
            if (!groupe.couleurs.length) groupe.couleurs = couleurs.map((c) => [c[0], c[1], c[2]]);
            mechants.set(set, groupe);
        } else {
            heros[carte] = couleurs;
        }
    }
    const groupesHeros = Array.from(grouperParIdentite(heros).values());
    groupesHeros.sort((a, b) => a.identite.localeCompare(b.identite, "fr", { numeric: true }));
    const groupesMechants = Array.from(mechants.values());
    for (const groupe of groupesMechants) groupe.cartes.sort();
    groupesMechants.sort((a, b) => a.cartes[0].localeCompare(b.cartes[0], "fr", { numeric: true }));
    for (const groupe of groupesMechants) {
        // Le relevé « mesuré » d'un méchant, pour « Couleur mesurée ».
        if (!etat.generees.has(groupe.identite) && groupe.cartes.some((c) => genereesParCarte[c])) {
            etat.generees.set(groupe.identite, groupe.couleurs);
        }
    }

    const fragment = document.createDocumentFragment();
    for (const groupe of groupesHeros) {
        const nom = noms.get(groupe.cartes[0]) || groupe.identite;
        const ligne = construireLigne(groupe, nom, "heros");
        etat.lignes.push(ligne);
        fragment.append(ligne.noeud);
    }
    for (const groupe of groupesMechants) {
        const ligne = construireLigne(groupe, groupe.set, "mechants");
        etat.lignes.push(ligne);
        fragment.append(ligne.noeud);
    }
    LISTE.append(fragment);
    for (const ligne of etat.lignes) poserCouleurs(ligne, ligne.couleurs);

    LISTE.hidden = false;
    filtrer();
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
function choisir(zone, cle, valeur) {
    for (const bouton of zone.querySelectorAll("button")) bouton.classList.toggle("on", bouton.dataset[cle] === valeur);
}
ONGLETS.addEventListener("click", (evenement) => {
    const bouton = evenement.target.closest("button");
    if (!bouton) return;
    etat.type = bouton.dataset.type;
    choisir(ONGLETS, "type", etat.type);
    RECHERCHE.placeholder = etat.type === "heros" ? "Chercher un héros…" : "Chercher un méchant…";
    filtrer();
});
ETATS.addEventListener("click", (evenement) => {
    const bouton = evenement.target.closest("button");
    if (!bouton) return;
    etat.montre = bouton.dataset.etat;
    choisir(ETATS, "etat", etat.montre);
    filtrer();
});

charger().catch((erreur) => {
    MESSAGE.textContent = String((erreur && erreur.message) || erreur);
    MESSAGE.className = "p-message p-echec";
    MESSAGE.hidden = false;
});
