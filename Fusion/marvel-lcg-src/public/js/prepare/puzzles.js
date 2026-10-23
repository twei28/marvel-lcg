// puzzles.js — les puzzles du moteur exposés dans le wizard moderne.
//
// Un puzzle est une position de départ scriptée (fichier puzzle/*.json) : le
// moteur la met en place via /load_puzzle puis on joue normalement sur le
// plateau. Ce module ajoute un bouton « 🧩 Puzzles » à côté des boutons
// Reprendre/Stats (reprise.js) et un panneau listant les puzzles disponibles.
//
// Côté serveur (routes existantes du moteur) : /list_puzzle_files,
// /get_puzzle_json?<chemin>, /load_puzzle?<chemin>.
"use strict";
import { cardImageUrl } from "/public/js/prepare/api.js?v=dfcc19da";
import { cards } from "/public/js/prepare/cards.js";
import { t } from "/public/js/prepare/langue.js";
import { ouvrirAssistant } from "/public/js/prepare/puzzle-assistant.js";

function el(tag, attrs, ...enfants) {
    const noeud = document.createElement(tag);
    if (attrs) {
        for (const [cle, valeur] of Object.entries(attrs)) {
            if (cle === "onclick") noeud.addEventListener("click", valeur);
            else if (cle === "style") noeud.style.cssText = valeur;
            else noeud.setAttribute(cle, valeur);
        }
    }
    for (const enfant of enfants) {
        if (enfant == null) continue;
        noeud.append(enfant.nodeType ? enfant : document.createTextNode(String(enfant)));
    }
    return noeud;
}

async function lireJson(url) {
    try {
        const reponse = await fetch(url, { cache: "no-store" });
        if (!reponse.ok) return undefined;
        return await reponse.json();
    } catch (e) {
        return undefined;
    }
}

function nomCarte(id) {
    const c = id ? cards.get(String(id).split(",")[0]) : null;
    return c && c.name ? String(c.name).replace(/^\*\s*/, "") : String(id || "");
}

// ---------------------------------------------------------------- style --
const style = document.createElement("style");
style.textContent = `
  .puzzles-panneau { position: fixed; inset: 0; z-index: 950; display: flex;
    align-items: center; justify-content: center; background: rgba(0,0,0,.72); }
  .puzzles-boite { width: min(680px, 92vw); max-height: 84vh; overflow: auto;
    background: #1c1c1e; border: 1px solid #555; border-radius: 12px;
    padding: 18px 20px; color: #ddd; }
  .puzzles-boite h2 { margin: 0 0 4px; font-size: 1.15rem; color: #fff; }
  .puzzles-note { font-size: .8rem; color: #999; margin: 0 0 14px; }
  .puzzle-ligne { display: flex; gap: 12px; align-items: center;
    border: 1px solid #444; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; }
  .puzzle-art { width: 52px; height: 72px; border-radius: 6px; object-fit: cover;
    background: #333; flex: none; }
  .puzzle-infos { flex: 1; min-width: 0; }
  .puzzle-titre { font-weight: 700; color: #fff; }
  .puzzle-sous { font-size: .8rem; color: #aaa; }
  .puzzle-comment { font-size: .78rem; color: #888; margin-top: 3px;
    overflow: hidden; text-overflow: ellipsis; display: -webkit-box;
    -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
  .puzzle-jouer { padding: 8px 16px; border-radius: 8px; border: 1px solid #7a5;
    background: #2c4a2c; color: #dfd; font-weight: 700; cursor: pointer; flex: none; }
  .puzzle-jouer:hover { background: #3a5f3a; }
  .puzzles-fermer { margin-top: 6px; padding: 7px 14px; border-radius: 8px;
    border: 1px solid #666; background: #2e2e2e; color: #ddd; cursor: pointer; }
`;
document.head.append(style);

// ---------------------------------------------------------------- panneau --
async function ouvrirPanneau() {
    document.querySelector(".puzzles-panneau")?.remove();
    const liste = el("div", {}, el("div", { style: "color:#999" }, t("Chargement des puzzles...")));
    const panneau = el("div", { class: "puzzles-panneau", onclick: (e) => { if (e.target === panneau) panneau.remove(); } },
        el("div", { class: "puzzles-boite" },
            el("h2", {}, "🧩 Puzzles"),
            el("p", { class: "puzzles-note" },
                t("Une position de départ imposée : à toi de trouver la meilleure suite de coups.")),
            liste,
            el("button", { class: "puzzle-jouer", style: "margin-right:8px", onclick: () => { panneau.remove(); ouvrirAssistant(); } }, "🧩 " + t("Créer un puzzle")),
            el("button", { class: "puzzles-fermer", onclick: () => panneau.remove() }, t("Fermer")),
        ),
    );
    document.body.append(panneau);

    const fichiers = (await lireJson("/list_puzzle_files")) || [];
    try { await cards.load(); } catch (e) { /* les noms retomberont sur les ids */ }
    if (!fichiers.length) {
        liste.replaceChildren(el("div", { style: "color:#999" }, t("Aucun puzzle disponible.")));
        return;
    }
    const lignes = await Promise.all(fichiers.map(async (chemin) => {
        const info = (await lireJson("/get_puzzle_json?" + chemin)) || {};
        const mechant = nomCarte(info.villain);
        const heros = (info.players || []).map(nomCarte).join(", ");
        const art = info.cover || info.villain;
        return el("div", { class: "puzzle-ligne" },
            el("img", {
                class: "puzzle-art",
                src: art ? cardImageUrl(String(art).split(",")[0]) : "",
                alt: mechant, loading: "lazy",
            }),
            el("div", { class: "puzzle-infos" },
                el("div", { class: "puzzle-titre" }, heros || chemin.replace(/^.*\//, "")),
                el("div", { class: "puzzle-sous" },
                    t("contre") + " " + (mechant || "?") + (info.author ? " · " + t("par") + " " + info.author : "")),
                info.comment ? el("div", { class: "puzzle-comment", title: info.comment }, info.comment) : null,
            ),
            el("button", {
                class: "puzzle-jouer",
                onclick: async (e) => {
                    e.currentTarget.disabled = true;
                    e.currentTarget.textContent = "...";
                    const r = await fetch("/load_puzzle?" + chemin).catch(() => null);
                    if (r && r.ok) window.location.href = "/app/board.html";
                    else {
                        e.currentTarget.disabled = false;
                        e.currentTarget.textContent = t("Jouer");
                        alert(t("Impossible de lancer ce puzzle."));
                    }
                },
            }, t("Jouer")),
        );
    }));
    liste.replaceChildren(...lignes);
}

// ---------------------------------------------------------------- bouton --
function installerBouton() {
    // Rejoint la rangée de boutons de reprise.js si elle existe déjà,
    // sinon crée la même rangée (reprise.js s'y greffera pareil).
    let rangee = document.querySelector(".reprise-boutons");
    if (!rangee) {
        rangee = el("div", { class: "reprise-boutons" });
        const etapes = document.querySelector("header.progress .steps");
        if (etapes) etapes.parentElement.insertBefore(rangee, etapes);
        else { rangee.classList.add("est-flottante"); document.body.append(rangee); }
    }
    rangee.append(el("button", { onclick: ouvrirPanneau, title: t("Jouer un puzzle : position imposée à résoudre") }, "🧩 Puzzles"));
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installerBouton);
} else {
    installerBouton();
}
