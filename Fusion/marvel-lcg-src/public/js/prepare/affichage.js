// affichage.js : le réglage « Affichage : Normal / Sobre / Épuré » de la préparation.
//
// Le choix vit dans le navigateur (`mc_affichage_v1`, lu aussi par le plateau)
// et, quand il y a un compte, sur le serveur (`/get_preferences`,
// `/save_preferences`). Il se traduit par `data-affichage` sur <html>, que les
// feuilles de style lisent : aucun rechargement n'est nécessaire.
"use strict";

import { CLE_AFFICHAGE, normaliser, suivant, reconcilier, doitProposerLeChoix, poserAttributs, valeurPermise, epurePermis, verifierEpurePermis, NORMAL, SOBRE, EPURE } from "/public/js/prepare/affichage-choix.js";
import { t } from "/public/js/prepare/langue.js";
import { poserIcone } from "/public/js/prepare/icones-entete.js";

/** Ce qui est montré : un « épuré » rangé reste « sobre » pour qui n'y a pas droit. */
export function affichageActuel() {
    try { return valeurPermise(localStorage.getItem(CLE_AFFICHAGE)); }
    catch (e) { return normaliser(null); }
}

/** L'épuré se propose-t-il ici ? (réservé à l'administrateur, voir affichage-choix.js) */
export { epurePermis, verifierEpurePermis };

// Une fois le serveur entendu, les boutons de l'en-tête se redessinent.
verifierEpurePermis().then(() => document.querySelectorAll(".btn-affichage").forEach(dessinerBouton));

export function appliquerAffichage(valeur = affichageActuel()) {
    poserAttributs(document.documentElement, valeur);
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
    // Un seul affichage pour qui a droit à l'épuré (18/10/2026) : le bouton qui fait tourner les modes se cache.
    bouton.hidden = epurePermis();
    const mode = affichageActuel();
    bouton.setAttribute("aria-pressed", mode === NORMAL ? "false" : "true");
    bouton.title = "";
    bouton.dataset.description = mode === EPURE
        ? t("Affichage épuré : gris, sans décor, le strict nécessaire. Cliquer pour revenir à l’affichage normal")
        : mode === SOBRE
            ? (epurePermis()
                ? t("Affichage sobre : fond gris, sans couleurs du héros ni animations. Cliquer pour passer en affichage épuré")
                : t("Affichage sobre : fond gris, sans couleurs du héros ni animations. Cliquer pour revenir à l’affichage normal"))
            : t("Affichage normal. Cliquer pour passer en affichage sobre : fond gris, sans couleurs du héros ni animations");
    poserIcone(bouton, mode === NORMAL ? "fa-eye" : "fa-eye-slash", mode === EPURE ? t("Affichage épuré") : mode === SOBRE ? t("Affichage sobre") : t("Affichage normal"));
}

/** Bouton Normal / Sobre / Épuré, à poser à côté du bouton FR / EN. */
export function boutonAffichage(classe) {
    const bouton = document.createElement("button");
    bouton.type = "button";
    bouton.className = (classe || "") + " btn-affichage";
    dessinerBouton(bouton);
    bouton.addEventListener("click", () => {
        const prochain = suivant(affichageActuel());
        choisirAffichage(prochain === EPURE && !epurePermis() ? NORMAL : prochain);
    });
    return bouton;
}
