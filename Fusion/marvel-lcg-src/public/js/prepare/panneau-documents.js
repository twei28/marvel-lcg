// panneau-documents.js — bouton « 📖 Documents » sur l'écran de préparation,
// qui ouvre la liste des livrets de règles et des carnets de campagne. Un clic
// ouvre le PDF dans un nouvel onglet, dans la visionneuse du navigateur.
//
// ⚠ MODULE, pas un script classique comme panneau-joueurs.js et lien-admin.js.
// C'est délibéré : il lui faut `catalog.extensions()`, qui donne le nom de
// chaque extension. Sans lui il faudrait tenir à la main une table de 27
// titres, qui se périmerait au premier PDF ajouté.
//
// Le moteur ne classe rien (voir get_documents dans server_get.py) : il rend
// une liste de fichiers, et tout le tri se fait ici, à partir du nom. C'est
// possible parce que le numéro mcNN d'un fichier EST celui que porte son
// extension dans sets_info.json — « 32. Mutant Genesis » ↔ mc32.

"use strict";
import { catalog } from "/public/js/prepare/catalog.js";
import { t, langueActuelle, enregistrerTraductions } from "/public/js/prepare/langue.js";

/* Les seuls titres qu'on écrit à la main : les documents du Set de base, qui
   sont trois pour une seule extension et que « Set de base — Règles » ne
   distinguerait pas. Tous les autres se nomment tout seuls. */
const TITRES = {
    "mc01_learn_to_play.pdf": {
        ordre: 1,
        titre: "Apprendre à jouer",
        titreEn: "Learn to Play",
        detail: "24 p.",
        detailEn: "24 pp.",
    },
    "mc01_rules_reference_v18.pdf": {
        ordre: 2,
        titre: "Guide de référence des règles (v1.8, anglais)",
        titreEn: "Rules Reference (v1.8)",
        detail: "71 p. · le document qui tranche",
        detailEn: "71 pp. · the document that settles arguments",
    },
    "mc01_guide_de_reference_fr.pdf": {
        ordre: 3,
        // Édition 2021 : elle a plusieurs versions de retard sur l'anglaise.
        // Le dire dans le libellé, sinon on l'oppose de bonne foi à la bonne.
        titre: "Guide de référence (français, édition 2021)",
        titreEn: "Rules Reference (French, 2021 edition)",
        detail: "plus ancien que la v1.8 anglaise",
        detailEn: "older than the English v1.8",
    },
};

/* Les chaines de cet ecran, declarees a langue.js plutot qu'ajoutees au
   dictionnaire commun : elles ne servent qu'ici. */
enregistrerTraductions({
    "Documents": "Documents",
    "Livrets de règles et carnets de campagne": "Rulebooks and campaign logs",
    "Règles": "Rules",
    "Carnets de campagne": "Campaign logs",
    "Aucun document installé.": "No documents installed.",
    "Carnet de campagne": "Campaign log",
    "Livret de règles": "Rulebook",
});
const enAnglais = () => langueActuelle() === "en";

/** « 9.2 Mo », pour que personne n'ouvre 30 Mo sans le savoir. */
function poids(octets) {
    const mo = octets / (1024 * 1024);
    return (mo >= 10 ? Math.round(mo) : mo.toFixed(1)) + " Mo";
}

/** Un carnet de campagne se reconnaît à son nom : `campaign-log`,
 *  `campaign_log`, `campaignlog`… d'où le tiret et le souligné optionnels. */
const estCarnet = (fichier) => /campaign[-_]?log/i.test(fichier);

/** Le numéro mcNN en tête de nom, ou null. */
function numeroDeFichier(fichier) {
    const m = /^mc(\d+)/i.exec(fichier);
    return m ? parseInt(m[1], 10) : null;
}

/** Le nom d'extension porté par la clé de sets_info (« 32. Mutant Genesis »). */
function nomDExtension(cle) {
    return String(cle).replace(/^\d+\.\s*/, "");
}

/** Repli quand un PDF déposé à la main ne correspond à aucune extension :
 *  on nettoie son nom de fichier plutôt que de le cacher. */
function titreDeSecours(fichier) {
    return fichier
        .replace(/\.pdf$/i, "")
        .replace(/^mc\d+[_-]?/i, "")
        .replace(/[-_]+/g, " ")
        .replace(/\b(compressed|web|website|insert|v\d+)\b/gi, "")
        .replace(/\s+/g, " ")
        .trim()
        .replace(/^\w/, (c) => c.toUpperCase()) || fichier;
}

const normaliser = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, "");

/** L'extension d'un document, par son NOM d'abord.
 *
 *  ⚠ Le numero mcNN est celui de l'EDITEUR, et sets_info porte celui du
 *  projet : les deux coincident souvent, mais pas toujours. mc03 est The
 *  Wrecking Crew, que sets_info numerote 7 ; mc10 est The Rise of Red Skull,
 *  numerote 4. S'y fier donnait « Captain America » et « Hulk » sur des
 *  livrets qui n'ont rien a voir.
 *
 *  On cherche donc le nom d'extension dans le nom de fichier, avec et sans
 *  son « the » initial (« mc02_green_goblin » ne contient pas « the green
 *  goblin »), et on garde la correspondance LA PLUS LONGUE pour qu'un nom
 *  court inclus par hasard ne l'emporte pas.
 *
 *  Le numero ne sert qu'en dernier recours, pour les fichiers qui ne nomment
 *  rien : mc55_rulebook-web.pdf et ses pareils. */
function extensionDuFichier(fichier, extensions) {
    const nom = normaliser(fichier.replace(/\.pdf$/i, ""));
    let trouvee = null;
    let meilleur = 0;
    for (const e of extensions) {
        const complet = nomDExtension(e.key);
        for (const variante of [complet, complet.replace(/^The\s+/i, "")]) {
            const n = normaliser(variante);
            if (n.length > 3 && n.length > meilleur && nom.includes(n)) {
                trouvee = e;
                meilleur = n.length;
            }
        }
    }
    if (trouvee) return trouvee;
    const numero = numeroDeFichier(fichier);
    if (numero == null) return null;
    return extensions.find((e) => parseInt(String(e.key), 10) === numero) || null;
}

/** Décrit chaque fichier : le GROUPE dont il relève (son extension) et la
 *  LIGNE qui le désigne à l'intérieur.
 *
 *  Le classement est par extension, et non par catégorie : les règles d'une
 *  campagne et son carnet doivent se suivre. Séparés en deux sections, il
 *  fallait descendre huit lignes plus bas pour trouver le carnet du livret
 *  qu'on venait d'ouvrir. */
function decrire(documents, extensions) {
    const en = enAnglais();
    return documents.map((d) => {
        const fichier = d.fichier;
        const numero = numeroDeFichier(fichier);
        const ext = extensionDuFichier(fichier, extensions);
        const carnet = estCarnet(fichier);
        const forcee = TITRES[fichier];
        const type = carnet ? t("Carnet de campagne") : t("Règles");
        return {
            fichier,
            // Le groupe porte le nom de la boite ; la ligne ne redit donc que
            // ce qui distingue le document a l'interieur.
            groupe: ext ? nomDExtension(ext.key) : titreDeSecours(fichier),
            ligne: forcee ? (en ? forcee.titreEn : forcee.titre) : type,
            detail: (forcee ? ((en ? forcee.detailEn : forcee.detail) + " · ") : "") + poids(d.octets),
            section: carnet ? "campagne" : "regles",
            code: ext ? ext.code : "",
            numero: numero == null ? 9999 : numero,
            ordre: forcee && forcee.ordre ? forcee.ordre : 0,
        };
    }).sort((a, b) => a.numero - b.numero
        || a.ordre - b.ordre
        // Les regles avant le carnet, a l'interieur d'une meme boite.
        || (a.section === b.section ? 0 : a.section === "regles" ? -1 : 1)
        || a.ligne.localeCompare(b.ligne));
}

/* ---------------- Rendu ---------------- */

let panneau = null;
let ouvert = false;

function styles() {
    if (document.getElementById("pd-styles")) return;
    const style = document.createElement("style");
    style.id = "pd-styles";
    style.textContent = `
.pd-panneau[hidden]{display:none!important}
.pd-panneau{position:fixed;top:124px;right:12px;z-index:901;width:360px;
  max-width:calc(100vw - 24px);max-height:74vh;display:flex;flex-direction:column;
  border:1px solid #666;border-radius:10px;background:#1c1c1c;color:#ddd;
  box-shadow:0 10px 30px rgba(0,0,0,.5);font-size:.85rem}
.pd-titre{display:flex;justify-content:space-between;align-items:center;gap:8px;
  padding:9px 12px;border-bottom:1px solid #333;font-weight:700}
.pd-fermer{background:none;border:0;color:#999;cursor:pointer;font-size:1rem;padding:0 2px}
.pd-fermer:hover{color:#fff}
.pd-corps{overflow-y:auto;padding:4px 0 8px}
.pd-section{color:#8a8a8a;font-size:.72rem;text-transform:uppercase;font-weight:800;
  letter-spacing:.06em;padding:10px 12px 4px}
.pd-lien{display:flex;flex-direction:column;gap:1px;padding:6px 12px;
  color:#ddd;text-decoration:none;border-left:3px solid transparent}
.pd-lien:hover{background:#262626;border-left-color:#e62429}
.pd-lien b{font-weight:600}
.pd-lien small{color:#8f8f8f;font-size:.74rem}
.pd-vide{padding:14px 12px;color:#8f8f8f}`;
    document.head.append(style);
}

function construire(fiches) {
    styles();
    panneau = document.createElement("div");
    panneau.className = "pd-panneau";
    panneau.hidden = true;

    const titre = document.createElement("div");
    titre.className = "pd-titre";
    const nom = document.createElement("span");
    nom.textContent = "📖 " + t("Documents");
    const fermer = document.createElement("button");
    fermer.className = "pd-fermer";
    fermer.type = "button";
    fermer.textContent = "✕";
    fermer.addEventListener("click", () => basculer(false));
    titre.append(nom, fermer);

    const corps = document.createElement("div");
    corps.className = "pd-corps";
    // Un en-tete par boite, dans l'ordre de parution, et sous lui ses
    // documents : les regles d'abord, le carnet juste apres.
    let groupeCourant = null;
    for (const f of fiches) {
        if (f.groupe !== groupeCourant) {
            groupeCourant = f.groupe;
            const entete = document.createElement("div");
            entete.className = "pd-section";
            entete.textContent = groupeCourant;
            corps.append(entete);
        }
        const a = document.createElement("a");
        a.className = "pd-lien";
        // `encodeURIComponent` et pas `encodeURI` : un nom de fichier peut
        // contenir une parenthese ou une espace, et le moteur ne retient
        // de toute facon que le nom de base.
        a.href = "/" + encodeURIComponent(f.fichier);
        a.target = "_blank";
        a.rel = "noopener";
        const b = document.createElement("b");
        b.textContent = f.ligne;
        const petit = document.createElement("small");
        petit.textContent = f.detail;
        a.append(b, petit);
        corps.append(a);
    }
    if (!fiches.length) {
        const vide = document.createElement("div");
        vide.className = "pd-vide";
        vide.textContent = t("Aucun document installé.");
        corps.append(vide);
    }
    panneau.append(titre, corps);
    document.body.append(panneau);
}

function basculer(veut) {
    ouvert = !!veut;
    panneau.hidden = !ouvert;
}

/** La rangée de boutons de l'en-tête, créée par le premier module qui arrive.
 *  Même repli que panneau-joueurs.js : si rien ne l'a créée, on la crée. */
function rangeeBoutons() {
    let rangee = document.querySelector(".reprise-boutons");
    if (rangee) return rangee;
    const style = document.createElement("style");
    style.textContent =
        ".reprise-boutons{display:flex;gap:8px;align-items:center;flex-wrap:wrap}" +
        ".reprise-boutons.est-flottante{position:fixed;top:82px;right:12px;z-index:900;justify-content:flex-end}" +
        ".reprise-boutons button{padding:7px 13px;border-radius:8px;border:1px solid #666;" +
        "background:#2e2e2e;color:#ddd;font-weight:700;cursor:pointer;font-size:.85rem}" +
        ".reprise-boutons button:hover{background:#3d3d3d}";
    document.head.append(style);
    rangee = document.createElement("div");
    rangee.className = "reprise-boutons";
    const etapes = document.querySelector("header.progress .steps");
    if (etapes) etapes.parentElement.insertBefore(rangee, etapes);
    else { rangee.classList.add("est-flottante"); document.body.append(rangee); }
    return rangee;
}

/** L'adresse d'un document, pour qui veut y renvoyer d'ailleurs (le lien
 *  contextuel de la tuile du méchant, dans app.js). */
export function adresseDuDocument(fichier) {
    return "/" + encodeURIComponent(fichier);
}

/** Le livret de règles d'une extension, désigné par sa clé sets_info.
 *  Rend null tant que la liste n'est pas chargée, ou si l'extension n'a
 *  pas de livret : l'appelant n'affiche alors aucun lien. */
let _fiches = null;
export function livretDExtension(cleExtension) {
    if (!_fiches) return null;
    const numero = parseInt(String(cleExtension), 10);
    if (Number.isNaN(numero)) return null;
    return _fiches.find((f) => f.numero === numero && f.section === "regles") || null;
}

/** Le carnet de campagne d'une extension, quand elle en a un. */
export function carnetDExtension(cleExtension) {
    if (!_fiches) return null;
    const numero = parseInt(String(cleExtension), 10);
    if (Number.isNaN(numero)) return null;
    return _fiches.find((f) => f.numero === numero && f.section === "campagne") || null;
}

/* ---------------- Démarrage ---------------- */

(async function () {
    let documents;
    try {
        const r = await fetch("/get_documents");
        if (!r.ok) return;                       // moteur d'une version antérieure
        documents = (await r.json()).documents || [];
    } catch (e) {
        return;
    }
    // Aucun PDF installé : pas de bouton. Un bouton qui n'ouvre qu'une liste
    // vide vaut moins que pas de bouton du tout.
    if (!documents.length) return;

    const extensions = await catalog.extensions().catch(() => []);
    _fiches = decrire(documents, extensions);
    construire(_fiches);

    const bouton = document.createElement("button");
    bouton.type = "button";
    bouton.textContent = "📖 " + t("Documents");
    bouton.title = t("Livrets de règles et carnets de campagne");
    bouton.addEventListener("click", () => basculer(!ouvert));
    rangeeBoutons().append(bouton);
})();
