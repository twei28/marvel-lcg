// affichage.js : le réglage « Affichage : Normal / Sobre » de la préparation.
//
// Le choix vit dans le navigateur (`mc_affichage_v1`, lu aussi par le plateau)
// et, quand il y a un compte, sur le serveur (`/get_preferences`,
// `/save_preferences`). Il se traduit par `data-affichage` sur <html>, que les
// feuilles de style lisent : aucun rechargement n'est nécessaire.
"use strict";

import { CLE_AFFICHAGE, normaliser, inverse, reconcilier, doitProposerLeChoix, SOBRE } from "/public/js/prepare/affichage-choix.js";
import { t } from "/public/js/prepare/langue.js";
import { poserIcone } from "/public/js/prepare/icones-entete.js";

export function affichageActuel() {
    try { return normaliser(localStorage.getItem(CLE_AFFICHAGE)); }
    catch (e) { return normaliser(null); }
}

export function appliquerAffichage(valeur = affichageActuel()) {
    document.documentElement.dataset.affichage = normaliser(valeur);
}

// Vue Player de l'administrateur (lien-admin.js) : ni lu ni écrit sur le compte.
function enVueJoueur() {
    try { return localStorage.getItem("mc_vue_joueur") === "oui"; } catch (e) { return false; }
}

function envoyer(changements) {
    if (enVueJoueur()) return;
    try {
        fetch("/save_preferences", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ changements }),
        }).catch(() => {});
    } catch (e) { /* hors ligne : le navigateur garde le choix */ }
}

export function choisirAffichage(valeur) {
    const choisi = normaliser(valeur);
    try { localStorage.setItem(CLE_AFFICHAGE, choisi); } catch (e) { /* stockage indisponible */ }
    appliquerAffichage(choisi);
    envoyer({ affichage: choisi });
    document.querySelectorAll(".btn-affichage").forEach(dessinerBouton);
}

/** Aligne le navigateur sur le compte au chargement. Sans compte, ne fait rien.
 *  Rend la réponse de `/get_preferences` (ou `null`) : la fenêtre « Choisis ton
 *  affichage » en a besoin pour savoir si le compte a déjà choisi. */
export async function synchroniserAffichage() {
    if (enVueJoueur()) return null;
    let reponse;
    try {
        const r = await fetch("/get_preferences", { cache: "no-store" });
        if (!r.ok) return null;
        reponse = await r.json();
    } catch (e) { return null; }
    const maj = reconcilier(affichageActuel(), reponse);
    if (!maj) return reponse;
    if (maj.affichage !== affichageActuel()) {
        try { localStorage.setItem(CLE_AFFICHAGE, maj.affichage); } catch (e) { /* idem */ }
        appliquerAffichage(maj.affichage);
        document.querySelectorAll(".btn-affichage").forEach(dessinerBouton);
    }
    if (Object.keys(maj.pousser).length) envoyer(maj.pousser);
    return reponse;
}

/** Ce joueur n'a-t-il jamais choisi son affichage ? (voir `doitProposerLeChoix`) */
export function affichageJamaisChoisi(reponse) {
    let brut = null;
    try { brut = localStorage.getItem(CLE_AFFICHAGE); } catch (e) { /* stockage indisponible */ }
    return doitProposerLeChoix(brut, reponse);
}

function dessinerBouton(bouton) {
    const sobre = affichageActuel() === SOBRE;
    bouton.setAttribute("aria-pressed", sobre ? "true" : "false");
    bouton.title = "";
    bouton.dataset.description = sobre
        ? t("Affichage sobre : fond gris, sans couleurs du héros ni animations. Cliquer pour revenir à l’affichage normal")
        : t("Affichage normal. Cliquer pour passer en affichage sobre : fond gris, sans couleurs du héros ni animations");
    poserIcone(bouton, sobre ? "fa-eye-slash" : "fa-eye", sobre ? t("Affichage sobre") : t("Affichage normal"));
}

/** Bouton Normal / Sobre, à poser à côté du bouton FR / EN. */
export function boutonAffichage(classe) {
    const bouton = document.createElement("button");
    bouton.type = "button";
    bouton.className = (classe || "") + " btn-affichage";
    dessinerBouton(bouton);
    bouton.addEventListener("click", () => { choisirAffichage(inverse(affichageActuel())); });
    return bouton;
}
