// Galerie des hauts faits. Lit /get_achievements : le moteur y calcule la
// progression a partir de ses propres statistiques et du journal des parties.
"use strict";

const FAMILLES = {
    progression: { nom: "Progression", icone: "▲" },
    exploit: { nom: "Exploits", icone: "✦" },
    defi: { nom: "Défis", icone: "◆" },
};

const etat = { hautsFaits: [], filtre: "" };
const $ = (s) => document.querySelector(s);

function el(balise, attrs, ...enfants) {
    const n = document.createElement(balise);
    for (const [k, v] of Object.entries(attrs || {})) {
        if (v === undefined || v === null) continue;
        if (k === "class") n.className = v;
        else n.setAttribute(k, v);
    }
    for (const e of enfants.flat(9)) {
        if (e === null || e === undefined || e === false) continue;
        n.append(e.nodeType ? e : document.createTextNode(String(e)));
    }
    return n;
}

function date(horodatage) {
    if (!horodatage) return "";
    return new Date(horodatage * 1000).toLocaleDateString();
}

function rendreFiltres() {
    const zone = $("#hf-filtres");
    zone.replaceChildren();
    const entrees = [["", "Tous"], ...Object.entries(FAMILLES).map(([k, v]) => [k, v.nom])];
    for (const [cle, libelle] of entrees) {
        zone.append(el("button", {
            class: "hf-filtre" + (etat.filtre === cle ? " est-actif" : ""),
            onclick: null,
        }, libelle));
        zone.lastChild.onclick = () => { etat.filtre = cle; rendreFiltres(); rendreGrille(); };
    }
}

function rendreGrille() {
    const zone = $("#hf-grille");
    zone.replaceChildren();
    const liste = etat.hautsFaits.filter((h) => !etat.filtre || h.famille === etat.filtre);
    if (!liste.length) {
        zone.append(el("p", { class: "hf-vide" }, "Aucun haut fait dans cette catégorie."));
        return;
    }
    for (const h of liste) {
        // Un haut fait « par héros » est acquis autant de fois qu'il y a de héros.
        const nbHeros = Object.keys(h.heros || {}).length;
        const debloque = h.par_heros ? nbHeros > 0 : !!h.debloque;
        const part = h.seuil ? Math.min(1, h.valeur / h.seuil) : 0;

        zone.append(el("article", { class: `hf-carte f-${h.famille}${debloque ? " est-debloque" : ""}` },
            el("div", { class: "hf-titre" },
                el("span", {}, FAMILLES[h.famille] ? FAMILLES[h.famille].icone : "•"),
                h.titre),
            el("div", { class: "hf-desc" }, h.description),
            !h.par_heros && h.seuil > 1
                ? el("div", { class: "hf-jauge" }, el("span", { style: `width:${Math.round(part * 100)}%` }))
                : null,
            el("div", { class: "hf-chiffres" },
                el("span", {}, h.par_heros
                    ? `${nbHeros} héros`
                    : (h.seuil > 1 ? `${h.valeur} / ${h.seuil}` : (debloque ? "obtenu" : "à débloquer"))),
                el("span", {}, debloque && h.debloque ? date(h.debloque) : ""),
            ),
        ));
    }
}

function rendreScore() {
    const total = etat.hautsFaits.length;
    const acquis = etat.hautsFaits.filter((h) =>
        h.par_heros ? Object.keys(h.heros || {}).length > 0 : !!h.debloque).length;
    $("#hf-score").textContent = `${acquis} / ${total} débloqués`;
}

async function demarrer() {
    try {
        const r = await fetch("/get_achievements");
        const data = await r.json();
        etat.hautsFaits = data.hauts_faits || [];
    } catch (e) {
        $("#hf-grille").textContent = "Impossible de charger les hauts faits : " + e.message;
        return;
    }
    rendreFiltres();
    rendreScore();
    rendreGrille();
}

demarrer();
