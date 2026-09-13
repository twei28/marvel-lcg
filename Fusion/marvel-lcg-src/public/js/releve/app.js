// releve/app.js — page de relevé des illustrations (/releve-images.html).
//
// À quoi ça sert : dire QUI est dessiné sur chaque carte. Le moteur lit du
// texte et des mots-clés, il ne voit aucune image ; quatre cartes du set Muse
// parlent pourtant de « la carte qui porte l'image de ton identité ». On relève
// donc à la main, une image à la fois, et le résultat part dans
// data/images_cartes.json (routes /get_images_cartes et /save_images_cartes).
//
// ⚠ RÉSERVÉE À L'ADMINISTRATEUR, et c'est le SERVEUR qui tranche. Cette page
// se contente de demander /get_site_admin pour afficher un message honnête ;
// l'écriture est refusée côté moteur (403) quoi que fasse le navigateur.
//
// ⚠ L'UNITÉ DE TRAVAIL EST L'IMAGE, PAS LA CARTE. 6153 cartes ne portent que
// 5746 illustrations : une réimpression (`full_link`) et une carte qui emprunte
// le scan d'une autre (`pic_id`) montrent la même chose. Les relever deux fois
// serait du travail en double et permettrait deux réponses contradictoires pour
// une seule image. Même résolution que le moteur (cards/images_cartes.py).
//
// ⚠ L'ORDRE ET LES SUGGESTIONS NE SONT PAS DU CONFORT. À la main, 5746 images
// prises au hasard ne se finissent jamais. L'ordre met devant ce qui sert
// vraiment à Muse (les cartes signature d'abord), et les suggestions
// pré-proposent les personnes déduites du set et du nom de la carte : la
// réponse est presque toujours dans les trois premières puces, donc un clic.
"use strict";

/* ------------------------------------------------------------ outils -- */

const $ = (id) => document.getElementById(id);

function normaliser(texte) {
    return String(texte || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

function el(tag, attrs, ...enfants) {
    const noeud = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
        if (k === "class") noeud.className = v;
        else if (k === "text") noeud.textContent = v;
        else if (k.startsWith("on")) noeud.addEventListener(k.slice(2), v);
        else noeud.setAttribute(k, v);
    }
    for (const enfant of enfants) if (enfant) noeud.append(enfant);
    return noeud;
}

/* ------------------------------------------------------------ données -- */

let identites = [];          // [{ id, nom, alias, genre, faces }]
let parIdentite = new Map(); // id -> entrée
let travaux = [];            // [{ imageId, nom, sousTitre, type, setName, rang, suggestions }]
let releve = new Map();      // imageId -> [identiteId]  (ce que le serveur sait)
let index = 0;               // position dans `travaux`
let retenus = [];            // identités cochées sur la carte affichée
let revoirTout = false;

// Rang de travail : ce qui sert le plus à Muse passe devant.
//  0 les cartes signature — le cœur du sujet, 1431 cartes ;
//  1 les autres cartes de joueur, qu'on joue aussi (une amélioration d'aspect
//    peut très bien dessiner le héros) ;
//  2 les cartes de rencontre, que Muse ne regarde pas mais qui serviront aux
//    prochaines cartes maison ;
//  3 le reste (ressources, défis, objets techniques du moteur).
const TYPES_JOUEUR = new Set([
    "Hero", "AlterEgo", "Ally", "Event", "Upgrade", "Support", "Resource", "PlayerSideScheme",
]);
const TYPES_RENCONTRE = new Set([
    "Villain", "Minion", "Treachery", "Attachment", "SideScheme", "MainScheme",
    "Environment", "Obligation", "Leader", "Evidence", "Status", "PlayerMinion",
]);

function rangDe(carte) {
    const classe = String((carte.desc || {}).Class || "");
    // « Hero » dans `Class` = carte signature ; le moteur la nomme
    // IdentitySpecific (game/card/face/base/card_player.py:76).
    if (classe.split(";").includes("Hero")) return 0;
    if (TYPES_JOUEUR.has(carte.type)) return 1;
    if (TYPES_RENCONTRE.has(carte.type)) return 2;
    return 3;
}

/** L'illustration que porte cette carte. Même règle que le moteur :
 *  `pic_id` d'abord, la carte d'origine si c'est une réimpression, son propre
 *  identifiant sinon. */
function idImage(carte) {
    return String(carte.pic_id || carte.full_link || carte.card_id);
}

/** ⚠ `reponse.ok` NE SUFFIT PAS ICI. Le moteur a une route fourre-tout
 *  `/{path:.+}` qui sert une image : une route absente ne renvoie donc pas 404
 *  mais un JPEG en 200, et `reponse.json()` échoue sur un message illisible.
 *  On regarde le type du contenu pour dire la vraie cause : le serveur est trop
 *  vieux pour cette page. */
async function json(url) {
    const reponse = await fetch(url, { cache: "no-store" });
    if (!reponse.ok) throw new Error(url + " → HTTP " + reponse.status);
    const type = reponse.headers.get("content-type") || "";
    if (!type.includes("json")) {
        throw new Error(
            `La route ${url} n'existe pas sur ce serveur (il a répondu « ${type} »). ` +
            "Le moteur date d'avant cette page : relancez-le.");
    }
    return reponse.json();
}

/* --------------------------------------------------------- suggestions -- */

// Index nom normalisé -> identités portant ce nom. ⚠ UNE LISTE, PAS UNE SEULE.
// Cinq personnes s'appellent « Spider-Man » : Peter Parker, Miles Morales,
// Miguel O'Hara, Elliot Tolliver, et le sbire de Civil War. Garder la première
// venue mettait le SBIRE en tête de suggestion sur toutes les cartes signature
// de Peter. Défaut constaté sur le catalogue réel le 13/09/2026.
let parNom = new Map();
// Index (nom, paquet) -> identité : c'est LUI qui tranche entre homonymes. Une
// carte du paquet `core` dont le set s'appelle « Spider-Man » parle du
// Spider-Man dont la carte d'identité est elle aussi dans `core`.
let parNomEtGroupe = new Map();

function construireIndexNoms(groupeDeCarte) {
    parNom = new Map();
    parNomEtGroupe = new Map();
    for (const identite of identites) {
        for (const nom of [identite.nom, ...(identite.alias || [])]) {
            const cle = normaliser(nom);
            if (!cle) continue;
            if (!parNom.has(cle)) parNom.set(cle, []);
            const liste = parNom.get(cle);
            if (!liste.includes(identite.id)) liste.push(identite.id);
            for (const face of identite.faces || []) {
                const groupe = groupeDeCarte.get(String(face));
                if (groupe) parNomEtGroupe.set(cle + "|" + groupe, identite.id);
            }
        }
    }
    // À nom égal, une personne jouable passe devant un adversaire : une carte
    // de joueur parle presque toujours du héros, pas de sa version ennemie.
    for (const liste of parNom.values()) {
        liste.sort((a, b) => {
            const ja = parIdentite.get(a)?.genre === "joueur" ? 0 : 1;
            const jb = parIdentite.get(b)?.genre === "joueur" ? 0 : 1;
            return ja - jb;
        });
    }
}

/** Les personnes probablement dessinées sur cette carte, les plus sûres
 *  d'abord. Ce n'est qu'une PROPOSITION : rien n'est enregistré sans clic.
 *
 *  ⚠ Le `set_name` est de loin le meilleur indice : le catalogue range les
 *  cartes signature de Spider-Man dans le set « Spider-Man », et les cartes de
 *  rencontre de Rhino dans le set « Rhino ». Le nom de la carte vient ensuite
 *  (« Aunt May », « Sandman ») et rattrape les allié·es et les sbires. */
function suggestionsPour(carte, groupe) {
    const trouvees = [];
    const ajouter = (id) => {
        if (id && !trouvees.includes(id)) trouvees.push(id);
    };
    /** Les personnes qui portent ce nom, celle du MÊME PAQUET d'abord.
     *
     *  ⚠ AU PLUS TROIS HOMONYMES. Cinq « Spider-Man » proposés d'affilée
     *  remplissaient toute la rangée et poussaient dehors les vraies autres
     *  pistes : sur « Black Cat », la carte ne suggérait plus Black Cat. */
    const ajouterNom = (nom) => {
        const cle = normaliser(String(nom || "").replace(/^\* /, ""));
        if (!cle) return;
        const duPaquet = parNomEtGroupe.get(cle + "|" + groupe);
        ajouter(duPaquet);
        // Le paquet a tranché : inutile de proposer les autres porteurs du même
        // nom, on SAIT duquel la carte parle. Ils restent trouvables par la
        // recherche pour le cas rare où l'illustration montre l'autre.
        if (duPaquet) return;
        let homonymes = 0;
        for (const id of parNom.get(cle) || []) {
            if (trouvees.includes(id)) continue;
            if (homonymes >= 3) break;
            ajouter(id);
            homonymes += 1;
        }
    };

    ajouterNom(carte.set_name);
    ajouterNom(carte.name);
    // Une carte nommée « Spider-Man's Web-Shooters » ou « Hulk Smash » cite la
    // personne sans lui être égale : on cherche le nom entier dans le titre.
    const nomCarte = normaliser(String(carte.name).replace(/^\* /, ""));
    for (const [nom, liste] of parNom) {
        if (trouvees.length >= 7) break;
        if (nom.length >= 4 && nomCarte.includes(nom)) ajouter(liste[0]);
    }
    return trouvees.slice(0, 9);
}

/* ------------------------------------------------------------ montage -- */

async function charger() {
    const [cartesParGroupe, annuaire, deja] = await Promise.all([
        json("get_cards_json?"),
        json("get_identites"),
        json("get_images_cartes"),
    ]);

    identites = Array.isArray(annuaire.identites) ? annuaire.identites : [];
    if (identites.length === 0) {
        throw new Error(
            "L'annuaire des personnes est vide. Lancez " +
            "`python3 outils/annuaire-identites.py --ecrire` puis rechargez.");
    }
    for (const identite of identites) parIdentite.set(identite.id, identite);
    // Première passe : dans quel paquet vit chaque carte. Les index de noms en
    // ont besoin pour départager les homonymes.
    const groupeDeCarte = new Map();
    for (const [groupe, cartes] of Object.entries(cartesParGroupe)) {
        if (!Array.isArray(cartes)) continue;
        for (const carte of cartes) {
            if (carte && carte.card_id) groupeDeCarte.set(String(carte.card_id), groupe);
        }
    }
    construireIndexNoms(groupeDeCarte);

    for (const [cle, valeur] of Object.entries(deja.cartes || {})) {
        releve.set(String(cle), Array.isArray(valeur) ? valeur.map(String) : []);
    }

    // Une entrée par image. La première carte rencontrée porte le libellé ; les
    // suivantes ne font qu'allonger la liste des cartes qui partagent le scan.
    const parImage = new Map();
    for (const [groupe, cartes] of Object.entries(cartesParGroupe)) {
        if (!Array.isArray(cartes)) continue;
        for (const carte of cartes) {
            if (!carte || !carte.card_id || !carte.name) continue;
            const imageId = idImage(carte);
            const existante = parImage.get(imageId);
            if (existante) {
                if (!existante.cartes.includes(carte.card_id)) existante.cartes.push(carte.card_id);
                existante.rang = Math.min(existante.rang, rangDe(carte));
                continue;
            }
            parImage.set(imageId, {
                imageId,
                cartes: [carte.card_id],
                nom: String(carte.name).replace(/^\* /, ""),
                unique: String(carte.name).startsWith("* "),
                sousTitre: carte.subtitle || "",
                type: carte.type || "",
                setName: carte.set_name || "",
                groupe,
                rang: rangDe(carte),
                suggestions: suggestionsPour(carte, groupe),
            });
        }
    }

    travaux = [...parImage.values()].sort(
        (a, b) => a.rang - b.rang || a.imageId.localeCompare(b.imageId));
}

/* ----------------------------------------------------------- affichage -- */

function aRelever() {
    return travaux.filter((x) => revoirTout || !releve.has(x.imageId));
}

let file = [];   // le sous-ensemble en cours de traitement

function majAvancement() {
    const total = travaux.length;
    const faites = travaux.filter((x) => releve.has(x.imageId)).length;
    const pourcent = total ? Math.round((faites / total) * 100) : 0;
    $("avancement").textContent = `${faites} / ${total} illustrations relevées (${pourcent} %)`;
}

function dessinerSuggestions(tache) {
    const zone = $("suggestions");
    zone.replaceChildren();
    tache.suggestions.forEach((id, rang) => {
        const identite = parIdentite.get(id);
        if (!identite) return;
        zone.append(puce(identite, rang < 9 ? String(rang + 1) : ""));
    });
    if (!zone.children.length) {
        zone.append(el("span", { class: "r-aide", text: "Aucune suggestion : cherchez ci-dessous." }));
    }
}

function puce(identite, touche) {
    const coche = retenus.includes(identite.id);
    const bouton = el("button", {
        type: "button",
        class: "r-puce" + (coche ? " est-cochee" : ""),
        onclick: () => basculer(identite.id),
    });
    bouton.append(el("span", { text: libelle(identite) }));
    if (touche) bouton.append(el("span", { class: "r-touche", text: touche }));
    return bouton;
}

function libelle(identite) {
    const alias = (identite.alias || []).join(", ");
    return alias ? `${identite.nom} / ${alias}` : identite.nom;
}

function dessinerListe() {
    const recherche = normaliser($("recherche").value.trim());
    const liste = $("liste");
    liste.replaceChildren();
    if (recherche.length < 2) return;
    let montrees = 0;
    for (const identite of identites) {
        if (montrees >= 40) break;
        const cible = normaliser(libelle(identite));
        if (!cible.includes(recherche)) continue;
        montrees += 1;
        const coche = retenus.includes(identite.id);
        liste.append(el("button", {
            type: "button",
            class: "r-ligne" + (coche ? " est-cochee" : ""),
            onclick: () => { basculer(identite.id); },
        },
            el("span", { text: (coche ? "✓ " : "") + libelle(identite) }),
            el("span", {
                class: "r-genre",
                text: identite.genre === "joueur" ? "jouable" : "adversaire",
            })));
    }
}

function dessinerRetenus() {
    const zone = $("retenus");
    zone.replaceChildren();
    for (const id of retenus) {
        const identite = parIdentite.get(id);
        if (!identite) continue;
        zone.append(el("span", { class: "r-retenu" },
            el("span", { text: libelle(identite) }),
            el("button", { type: "button", title: "Retirer", text: "×", onclick: () => basculer(id) })));
    }
    $("btn-valider").disabled = retenus.length === 0;
}

function basculer(id) {
    if (retenus.includes(id)) retenus = retenus.filter((x) => x !== id);
    else retenus = [...retenus, id];
    const tache = file[index];
    if (tache) dessinerSuggestions(tache);
    dessinerListe();
    dessinerRetenus();
}

function dessiner() {
    const tache = file[index];
    if (!tache) {
        $("atelier").hidden = true;
        $("message").hidden = false;
        $("message").innerHTML = revoirTout
            ? "<strong>Plus rien à afficher.</strong>"
            : "<strong>Tout est relevé.</strong> Cochez « Revoir aussi les cartes déjà relevées » pour repasser dessus.";
        majAvancement();
        return;
    }
    $("message").hidden = true;
    $("atelier").hidden = false;

    // Le scan haute définition, et TOUJOURS l'anglais : ici on REGARDE
    // l'illustration, c'est tout le travail, et le scan français porte un
    // filigrane qui la salit une fois agrandie (même raison que
    // `cardImageUrlEn` dans js/prepare/api.js). Le texte de la carte ne sert
    // à rien pour dire qui est dessiné dessus.
    // Le moteur retombe seul sur le scan habituel quand la version HD n'existe
    // pas (engine/file/cache.py, LoadImageHD).
    $("scan").src = "/hd/" + encodeURIComponent(tache.imageId);
    $("scan").alt = tache.nom;

    const cartes = tache.cartes.length > 1
        ? ` · ${tache.cartes.length} cartes partagent ce scan` : "";
    $("legende").innerHTML = "";
    $("legende").append(
        el("b", { text: tache.nom + (tache.sousTitre ? " — " + tache.sousTitre : "") }),
        el("br"),
        el("span", { text: `${tache.type || "?"} · ${tache.setName || "sans set"} · ${tache.imageId}${cartes}` }));

    $("position").textContent = `${index + 1} / ${file.length}`;
    $("btn-precedent").disabled = index === 0;
    $("btn-suivant").disabled = index >= file.length - 1;

    retenus = [...(releve.get(tache.imageId) || [])];
    $("recherche").value = "";
    dessinerSuggestions(tache);
    dessinerListe();
    dessinerRetenus();
    majAvancement();
}

/* ---------------------------------------------------------- écriture -- */

let enregistrementEnCours = false;

async function enregistrer(identitesChoisies) {
    const tache = file[index];
    if (!tache || enregistrementEnCours) return;
    enregistrementEnCours = true;
    try {
        const reponse = await fetch("/save_images_cartes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ carte: tache.imageId, identites: identitesChoisies }),
        });
        if (reponse.status === 403) {
            avertir("Écriture refusée : cette page est réservée à l'administrateur.");
            return;
        }
        if (!reponse.ok) {
            avertir("Enregistrement impossible (HTTP " + reponse.status + "). Rien n'est perdu, réessayez.");
            return;
        }
        releve.set(tache.imageId, identitesChoisies);
        avancer();
    } catch (erreur) {
        avertir("Le serveur ne répond pas : " + erreur.message);
    } finally {
        enregistrementEnCours = false;
    }
}

function avertir(texte) {
    const zone = $("avancement");
    const avant = zone.textContent;
    zone.textContent = "⚠ " + texte;
    setTimeout(() => { if (zone.textContent.startsWith("⚠")) zone.textContent = avant; }, 6000);
}

/** Passe à la suivante. ⚠ Quand on ne revoit PAS tout, la carte qu'on vient de
 *  relever sort de la file : rester au même index affiche donc déjà la
 *  suivante, et incrémenter en sauterait une. */
function avancer() {
    if (!revoirTout) {
        file = aRelever();
        if (index >= file.length) index = Math.max(0, file.length - 1);
        dessiner();
        return;
    }
    if (index < file.length - 1) index += 1;
    dessiner();
}

/* ------------------------------------------------------------ clavier -- */

function surTouche(evenement) {
    if (evenement.target === $("recherche")) {
        if (evenement.key === "Escape") { $("recherche").value = ""; dessinerListe(); }
        return;
    }
    const tache = file[index];
    if (!tache) return;
    if (evenement.key >= "1" && evenement.key <= "9") {
        const id = tache.suggestions[Number(evenement.key) - 1];
        if (id) { basculer(id); evenement.preventDefault(); }
    } else if (evenement.key === "0") {
        enregistrer([]);
        evenement.preventDefault();
    } else if (evenement.key === "Enter") {
        if (retenus.length) enregistrer(retenus);
        evenement.preventDefault();
    } else if (evenement.key === "ArrowRight") {
        if (index < file.length - 1) { index += 1; dessiner(); }
        evenement.preventDefault();
    } else if (evenement.key === "ArrowLeft") {
        if (index > 0) { index -= 1; dessiner(); }
        evenement.preventDefault();
    }
}

/* ---------------------------------------------------------- démarrage -- */

async function demarrer() {
    // Le serveur reste seul juge (l'écriture répond 403) ; ceci n'est qu'une
    // politesse, pour ne pas laisser un invité remplir un formulaire inutile.
    try {
        const admin = await json("/get_site_admin");
        if (!admin || !admin.url) {
            $("message").innerHTML =
                "<strong>Page réservée à l'administrateur.</strong><br>" +
                "Le relevé des illustrations se remplit depuis le compte qui héberge le site.";
            return;
        }
    } catch (erreur) {
        // Moteur lancé à la main, sans site devant : on laisse passer, l'écriture
        // ne sera de toute façon acceptée que si le moteur le veut bien.
    }

    try {
        await charger();
    } catch (erreur) {
        $("message").innerHTML = "<strong>Chargement impossible.</strong><br>" + erreur.message;
        return;
    }

    file = aRelever();
    index = 0;

    $("btn-valider").addEventListener("click", () => { if (retenus.length) enregistrer(retenus); });
    $("btn-aucune").addEventListener("click", () => enregistrer([]));
    $("btn-plus-tard").addEventListener("click", () => {
        if (index < file.length - 1) { index += 1; dessiner(); }
    });
    $("btn-precedent").addEventListener("click", () => { if (index > 0) { index -= 1; dessiner(); } });
    $("btn-suivant").addEventListener("click", () => {
        if (index < file.length - 1) { index += 1; dessiner(); }
    });
    $("recherche").addEventListener("input", dessinerListe);
    $("toggle-tout").addEventListener("change", (e) => {
        revoirTout = e.target.checked;
        file = revoirTout ? travaux : aRelever();
        index = 0;
        dessiner();
    });
    document.addEventListener("keydown", surTouche);

    dessiner();
}

demarrer();
