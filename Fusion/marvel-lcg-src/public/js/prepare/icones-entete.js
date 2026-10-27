// icones-entete.js : les boutons d'outils de l'en-tête en ICÔNES SEULES (09/10/2026).
//
// Les boutons de la rangée `.reprise-boutons` sont posés par une dizaine de
// scripts (reprise.js, lien-admin.js, panneau-bug.js...), certains classiques,
// d'autres modules, à des moments différents. Plutôt que de les coordonner un à
// un, ce module observe la rangée et met chaque bouton au même format : une
// icône Font Awesome, le libellé gardé pour les lecteurs d'écran et affiché au
// survol (`title`). Il s'installe tout seul à l'import.
"use strict";

/** Pictogramme d'un bouton posé avec un émoji en tête de libellé. */
const ICONE_DE_L_EMOJI = [
    ["🃏", "fa-clone"],
    ["⚙", "fa-cog"],
    ["🖼", "fa-picture-o"],
    ["🎨", "fa-paint-brush"],
    ["💾", "fa-floppy-o"],
    ["📦", "fa-file-archive-o"],
    ["📂", "fa-folder-open"],
    ["🎫", "fa-ticket"],
    ["🧩", "fa-puzzle-piece"],
    ["🐞", "fa-bug"],
    ["🏆", "fa-trophy"],
];

const STYLE = `
.reprise-boutons > button, .reprise-boutons > a, .btn-icone {
  width: 34px; height: 34px; min-width: 34px; min-height: 0; padding: 0 !important;
  display: inline-grid; place-items: center; font-size: 15px; line-height: 1; flex: none;
  position: relative;
}
.reprise-boutons > button i.fa, .reprise-boutons > a i.fa, .btn-icone i.fa { font-size: 15px; margin: 0; }
.rb-libelle {
  position: absolute !important; width: 1px; height: 1px; overflow: hidden;
  clip: rect(0 0 0 0); clip-path: inset(50%); white-space: nowrap;
}
.reprise-boutons { gap: 6px !important; flex-wrap: nowrap; }
.btn-langue.btn-icone, .btn-affichage.btn-icone {
  width: 34px !important; height: 34px !important; min-width: 34px; min-height: 0 !important;
  padding: 0 !important; display: inline-grid; place-items: center; flex: none;
  font-size: 12px !important; font-weight: 800; letter-spacing: .02em;
}
`;

function installerStyle() {
    if (!document.querySelector('link[href*="font-awesome"]')) {
        const lien = document.createElement("link");
        lien.rel = "stylesheet";
        lien.href = "/public/css/font-awesome.css";
        document.head.append(lien);
    }
    if (document.getElementById("style-icones-entete")) return;
    const style = document.createElement("style");
    style.id = "style-icones-entete";
    style.textContent = STYLE;
    document.head.append(style);
}

function icone(classe) {
    const i = document.createElement("i");
    i.className = "fa " + classe;
    i.setAttribute("aria-hidden", "true");
    return i;
}

/** Remplace le contenu d'un bouton par une icône et un libellé masqué. */
export function poserIcone(bouton, classeIcone, libelle) {
    const span = document.createElement("span");
    span.className = "rb-libelle";
    span.textContent = libelle;
    bouton.replaceChildren(icone(classeIcone), span);
    bouton.setAttribute("aria-label", libelle);
    const description = bouton.dataset.description || bouton.title || "";
    bouton.dataset.description = description;
    bouton.title = !description || description.startsWith(libelle) ? (description || libelle) : libelle + " : " + description;
    bouton.classList.add("btn-icone");
}

function classeIconeDe(bouton, texte) {
    const fa = bouton.querySelector("i.fa");
    if (fa) return [...fa.classList].find((c) => c.startsWith("fa-")) || "fa-circle";
    if (bouton.classList.contains("bouton-vue-joueur")) return texte === "Admin" ? "fa-user-secret" : "fa-user";
    const trouve = ICONE_DE_L_EMOJI.find(([emoji]) => texte.startsWith(emoji));
    return trouve ? trouve[1] : null;
}

function libelleDe(texte) {
    return texte.replace(/^[^\p{L}\p{N}]+/u, "").trim();
}

function iconiser(bouton) {
    if (bouton.dataset.iconise === "1") return;
    const texte = (bouton.textContent || "").trim();
    const classe = classeIconeDe(bouton, texte);
    if (!classe) return;
    bouton.dataset.iconise = "1";
    poserIcone(bouton, classe, libelleDe(texte) || texte);
}

function surveiller(rangee) {
    if (rangee.dataset.iconesSurveillees === "1") return;
    rangee.dataset.iconesSurveillees = "1";
    const passer = () => rangee.querySelectorAll(":scope > button, :scope > a").forEach(iconiser);
    passer();
    new MutationObserver(passer).observe(rangee, { childList: true });
}

function demarrer() {
    installerStyle();
    const chercher = () => document.querySelectorAll(".reprise-boutons").forEach(surveiller);
    chercher();
    new MutationObserver(chercher).observe(document.body, { childList: true, subtree: true });
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", demarrer);
else demarrer();
