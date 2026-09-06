// panneau-bug.js — bouton « 🐞 Signaler un bug » et son formulaire, pour les
// écrans HORS PARTIE : préparation, salon, galerie. Le plateau a le sien, qui
// sait joindre le journal de la partie (ui-app/src/board/RapportBug.tsx).
//
// Le rapport part au moteur (/post_rapport_bug), qui le relaie au site avec le
// jeton de la partie ; il arrive sur /admin. Le navigateur ne parle jamais au
// site directement : il est servi depuis p<N>.<domaine> et le site depuis
// <domaine>, la requête serait croisée.
//
// ⚠ SANS SITE DERRIÈRE, ON NE PROMET RIEN. En partie locale il n'y a personne
// à qui envoyer : le formulaire le dit et propose le presse-papier ou un
// fichier, ce que le plateau sait déjà faire. Mieux vaut ça qu'un bouton
// « Envoyer » qui ne mène nulle part.

"use strict";
import { t, enregistrerTraductions } from "/public/js/prepare/langue.js";

enregistrerTraductions({
    "Signaler un bug": "Report a bug",
    "Dis-moi ce qui ne va pas": "Tell me what went wrong",
    "Ton nom": "Your name",
    "Pour pouvoir te répondre": "So I can get back to you",
    "Qu'est-ce qui s'est passé ?": "What happened?",
    "Ce que tu faisais, ce que tu attendais, ce qui est arrivé à la place.":
        "What you were doing, what you expected, what happened instead.",
    "Capture d'écran": "Screenshot",
    "Colle une image avec Ctrl+V, ou choisis un fichier.":
        "Paste an image with Ctrl+V, or pick a file.",
    "Parcourir": "Browse",
    "Retirer l'image": "Remove image",
    "Envoyer": "Send",
    "Envoi...": "Sending...",
    "Merci, c'est envoyé.": "Thanks, it's on its way.",
    "L'envoi a échoué :": "Sending failed:",
    "Aucun site derrière ce jeu : le rapport ne peut pas être envoyé. Copie-le ou télécharge-le, et fais-le moi parvenir.":
        "No site behind this game: the report cannot be sent. Copy or download it and pass it along.",
    "Copier": "Copy",
    "Copié": "Copied",
    "Télécharger": "Download",
    "Il faut un nom et une description.": "A name and a description are required.",
    "trop de rapports, reessaie plus tard": "too many reports, try again later",
    "site injoignable": "site unreachable",
});

/* Réduction de la capture AVANT l'envoi. Une capture d'écran brute pèse
   volontiers 2 à 4 Mo ; réduite à 1600 px de large en JPEG, elle tombe sous le
   demi-mégaoctet sans qu'on perde ce qu'il y a à voir. Sans cette réduction on
   butait sur le plafond de corps du moteur, et l'envoi échouait sans rien dire
   d'utile. */
const LARGEUR_MAX = 1600;

async function reduire(fichier) {
    const image = await createImageBitmap(fichier);
    const facteur = Math.min(1, LARGEUR_MAX / Math.max(image.width, image.height));
    const l = Math.round(image.width * facteur);
    const h = Math.round(image.height * facteur);
    const toile = document.createElement("canvas");
    toile.width = l;
    toile.height = h;
    toile.getContext("2d").drawImage(image, 0, 0, l, h);
    image.close && image.close();
    return toile.toDataURL("image/jpeg", 0.82);
}

/** Le nom de l'écran d'où part le rapport, déduit de l'adresse. */
function ecranCourant() {
    const p = location.pathname.replace(/^\/|\.html$/g, "") || "prepare";
    return ({ prepare: "préparation", salon: "salon", galerie: "galerie" })[p] || p;
}

/** Ce qu'on met dans le presse-papier ou le fichier, faute de site. */
function rapportEnTexte(nom, description, capture) {
    return [
        "# Rapport de bug",
        "Date    : " + new Date().toISOString(),
        "Écran   : " + ecranCourant(),
        "Nom     : " + nom,
        "Adresse : " + location.href,
        "Capture : " + (capture ? "jointe séparément" : "aucune"),
        "",
        description,
    ].join("\n");
}

let panneau = null;
let ouvert = false;
let capture = null;          // data URL de l'image jointe, ou null
let siteActif = false;

function styles() {
    if (document.getElementById("pb-styles")) return;
    const style = document.createElement("style");
    style.id = "pb-styles";
    style.textContent = `
.pb-panneau[hidden]{display:none!important}
.pb-panneau{position:fixed;top:124px;right:12px;z-index:902;width:380px;
  max-width:calc(100vw - 24px);max-height:78vh;display:flex;flex-direction:column;
  border:1px solid #666;border-radius:10px;background:#1c1c1c;color:#ddd;
  box-shadow:0 10px 30px rgba(0,0,0,.5);font-size:.85rem}
.pb-titre{display:flex;justify-content:space-between;align-items:center;gap:8px;
  padding:9px 12px;border-bottom:1px solid #333;font-weight:700}
.pb-fermer{background:none;border:0;color:#999;cursor:pointer;font-size:1rem;padding:0 2px}
.pb-fermer:hover{color:#fff}
.pb-corps{overflow-y:auto;padding:10px 12px 12px;display:flex;flex-direction:column;gap:10px}
.pb-champ{display:flex;flex-direction:column;gap:3px}
.pb-champ label{font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;
  font-weight:800;color:#9aa4b0}
.pb-champ small{color:#8a8a8a;font-size:.72rem}
.pb-panneau input[type=text],.pb-panneau textarea{width:100%;box-sizing:border-box;
  background:#111;border:1px solid #3a3a3a;border-radius:6px;color:#ddd;
  padding:7px 9px;font:inherit}
.pb-panneau textarea{min-height:88px;resize:vertical}
.pb-panneau input[type=text]:focus,.pb-panneau textarea:focus,.pb-zone:focus{
  outline:none;border-color:#e62429}
.pb-zone{border:1px dashed #3f3f3f;border-radius:8px;padding:12px;text-align:center;
  color:#8a8a8a;font-size:.76rem;cursor:pointer;background:#141414}
.pb-zone:hover{border-color:#666;color:#bbb}
.pb-apercu{position:relative}
.pb-apercu img{width:100%;border-radius:6px;border:1px solid #3a3a3a;display:block}
.pb-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.pb-panneau button.pb-bouton{font:inherit;font-weight:700;font-size:.82rem;cursor:pointer;
  border-radius:7px;padding:7px 13px;border:1px solid #666;background:#2e2e2e;color:#ddd}
.pb-panneau button.pb-bouton:hover{background:#3d3d3d}
.pb-panneau button.pb-envoi{border-color:#e62429;background:#e62429;color:#fff}
.pb-panneau button.pb-envoi:hover{filter:brightness(1.12)}
.pb-panneau button.pb-bouton[disabled]{opacity:.5;cursor:default}
.pb-mot{font-size:.78rem;padding:8px 10px;border-radius:6px}
.pb-mot.ok{background:#12301c;color:#7ee2a0;border:1px solid #24603a}
.pb-mot.non{background:#3a1416;color:#ff9a9a;border:1px solid #6d2226}
.pb-mot.info{background:#14212e;color:#9ccaf5;border:1px solid #24455f}`;
    document.head.append(style);
}

function construire() {
    styles();
    panneau = document.createElement("div");
    panneau.className = "pb-panneau";
    panneau.hidden = true;

    const titre = document.createElement("div");
    titre.className = "pb-titre";
    const nomTitre = document.createElement("span");
    nomTitre.textContent = "🐞 " + t("Signaler un bug");
    const fermer = document.createElement("button");
    fermer.className = "pb-fermer";
    fermer.type = "button";
    fermer.textContent = "✕";
    fermer.addEventListener("click", () => basculer(false));
    titre.append(nomTitre, fermer);

    const corps = document.createElement("div");
    corps.className = "pb-corps";

    const champ = (libelle, aide, controle) => {
        const bloc = document.createElement("div");
        bloc.className = "pb-champ";
        const l = document.createElement("label");
        l.textContent = libelle;
        bloc.append(l, controle);
        if (aide) {
            const s = document.createElement("small");
            s.textContent = aide;
            bloc.append(s);
        }
        return bloc;
    };

    const nom = document.createElement("input");
    nom.type = "text";
    nom.maxLength = 80;
    // Le nom est OBLIGATOIRE : sans lui, un rapport d'invité arrive anonyme et
    // il n'y a plus personne à qui demander la précision qui manque.
    nom.placeholder = t("Ton nom");

    const description = document.createElement("textarea");
    description.maxLength = 4000;

    const fichier = document.createElement("input");
    fichier.type = "file";
    fichier.accept = "image/*";
    fichier.hidden = true;

    const zone = document.createElement("div");
    zone.className = "pb-zone";
    zone.tabIndex = 0;
    zone.textContent = t("Colle une image avec Ctrl+V, ou choisis un fichier.");
    zone.addEventListener("click", () => fichier.click());

    const apercu = document.createElement("div");
    apercu.className = "pb-apercu";
    apercu.hidden = true;

    const retirer = document.createElement("button");
    retirer.type = "button";
    retirer.className = "pb-bouton";
    retirer.textContent = t("Retirer l'image");
    retirer.hidden = true;
    retirer.addEventListener("click", () => poserCapture(null));

    async function poserCapture(source) {
        if (!source) {
            capture = null;
            apercu.replaceChildren();
            apercu.hidden = true;
            retirer.hidden = true;
            zone.hidden = false;
            return;
        }
        try {
            capture = await reduire(source);
        } catch (e) {
            capture = null;
            dire("non", t("L'envoi a échoué :") + " image illisible");
            return;
        }
        const img = document.createElement("img");
        img.src = capture;
        apercu.replaceChildren(img);
        apercu.hidden = false;
        retirer.hidden = false;
        zone.hidden = true;
    }

    fichier.addEventListener("change", () => {
        if (fichier.files && fichier.files[0]) poserCapture(fichier.files[0]);
    });

    // Ctrl+V n'importe où dans le panneau ouvert : c'est le geste naturel après
    // un Impr.écran, et l'obliger à passer par « Parcourir » ferait enregistrer
    // un fichier pour rien.
    panneau.addEventListener("paste", (ev) => {
        const items = (ev.clipboardData && ev.clipboardData.items) || [];
        for (const it of items) {
            if (it.type && it.type.startsWith("image/")) {
                const f = it.getAsFile();
                if (f) { ev.preventDefault(); poserCapture(f); return; }
            }
        }
    });

    const mot = document.createElement("div");
    mot.className = "pb-mot info";
    mot.hidden = true;
    function dire(genre, texte) {
        mot.className = "pb-mot " + genre;
        mot.textContent = texte;
        mot.hidden = false;
    }

    const actions = document.createElement("div");
    actions.className = "pb-actions";

    const envoyer = document.createElement("button");
    envoyer.type = "button";
    envoyer.className = "pb-bouton pb-envoi";
    envoyer.textContent = t("Envoyer");

    const copier = document.createElement("button");
    copier.type = "button";
    copier.className = "pb-bouton";
    copier.textContent = t("Copier");

    const telecharger = document.createElement("button");
    telecharger.type = "button";
    telecharger.className = "pb-bouton";
    telecharger.textContent = t("Télécharger");

    function valide() {
        if (!nom.value.trim() || !description.value.trim()) {
            dire("non", t("Il faut un nom et une description."));
            return false;
        }
        return true;
    }

    envoyer.addEventListener("click", async () => {
        if (!valide()) return;
        envoyer.disabled = true;
        envoyer.textContent = t("Envoi...");
        try {
            const r = await fetch("/post_rapport_bug", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    nom: nom.value.trim(),
                    description: description.value.trim(),
                    ecran: ecranCourant(),
                    // Hors partie, il n'y a ni journal ni siège à joindre :
                    // le plateau, lui, remplit les deux.
                    journal: "",
                    siege: "",
                    capture: capture || "",
                }),
            });
            const corpsJson = await r.json().catch(() => ({}));
            if (!r.ok) {
                dire("non", t("L'envoi a échoué :") + " " + t(corpsJson.error || String(r.status)));
            } else {
                dire("ok", t("Merci, c'est envoyé."));
                description.value = "";
                poserCapture(null);
            }
        } catch (e) {
            dire("non", t("L'envoi a échoué :") + " " + e.message);
        }
        envoyer.disabled = false;
        envoyer.textContent = t("Envoyer");
    });

    copier.addEventListener("click", async () => {
        if (!valide()) return;
        try {
            await navigator.clipboard.writeText(
                rapportEnTexte(nom.value.trim(), description.value.trim(), capture));
            copier.textContent = t("Copié");
            setTimeout(() => { copier.textContent = t("Copier"); }, 1600);
        } catch (e) {
            dire("non", t("L'envoi a échoué :") + " presse-papier refusé");
        }
    });

    telecharger.addEventListener("click", () => {
        if (!valide()) return;
        const texte = rapportEnTexte(nom.value.trim(), description.value.trim(), capture);
        const url = URL.createObjectURL(new Blob([texte], { type: "text/plain" }));
        const a = document.createElement("a");
        a.href = url;
        a.download = "rapport-bug.txt";
        a.click();
        URL.revokeObjectURL(url);
    });

    corps.append(
        champ(t("Ton nom"), t("Pour pouvoir te répondre"), nom),
        champ(t("Qu'est-ce qui s'est passé ?"),
              t("Ce que tu faisais, ce que tu attendais, ce qui est arrivé à la place."),
              description),
        champ(t("Capture d'écran"), null, zone),
        apercu, fichier, mot,
    );

    if (siteActif) {
        actions.append(envoyer, retirer);
    } else {
        // Pas de site : on le DIT, et on ne montre que ce qui marche.
        const info = document.createElement("div");
        info.className = "pb-mot info";
        info.textContent = t("Aucun site derrière ce jeu : le rapport ne peut pas être envoyé. Copie-le ou télécharge-le, et fais-le moi parvenir.");
        corps.insertBefore(info, corps.firstChild);
        actions.append(copier, telecharger, retirer);
    }
    corps.append(actions);
    panneau.append(titre, corps);
    document.body.append(panneau);
}

function basculer(veut) {
    ouvert = !!veut;
    panneau.hidden = !ouvert;
    if (ouvert) {
        const premier = panneau.querySelector("input[type=text]");
        if (premier) premier.focus();
    }
}

/** La rangée de boutons de l'en-tête. Même repli que les autres panneaux :
 *  si aucun module ne l'a créée (salon, galerie), on la crée flottante. */
function rangeeBoutons() {
    let rangee = document.querySelector(".reprise-boutons");
    if (rangee) return rangee;
    const style = document.createElement("style");
    style.textContent =
        ".reprise-boutons{display:flex;gap:8px;align-items:center;flex-wrap:wrap}" +
        ".reprise-boutons.est-flottante{position:fixed;top:12px;right:12px;z-index:900;justify-content:flex-end}" +
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

(async function () {
    try {
        const r = await fetch("/get_rapport_actif");
        siteActif = r.ok ? !!(await r.json()).actif : false;
    } catch (e) {
        siteActif = false;
    }
    construire();
    const bouton = document.createElement("button");
    bouton.type = "button";
    bouton.textContent = "🐞 " + t("Signaler un bug");
    bouton.title = t("Dis-moi ce qui ne va pas");
    bouton.addEventListener("click", () => basculer(!ouvert));
    rangeeBoutons().append(bouton);
})();
