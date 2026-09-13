// legacy-fiche.js — ce que le mode Legacy retient d'un compte.
//
// Trois choses, et trois seulement, qui NE SE DÉDUISENT PAS de l'historique des
// parties :
//
//   actif          le mode a-t-il été activé, et quand ;
//   depuis         l'instant à partir duquel les parties comptent. Zéro veut
//                  dire « reprendre mes parties passées » ; un instant veut
//                  dire « repartir de zéro ». Choisi UNE FOIS, à l'activation ;
//   jetonsDepenses les héros fan-made achetés.
//
// Et un quatrième champ qui, lui, se déduit : `instantane`, une photo de la
// progression pour l'afficher sans tout recalculer.
//
// ⚠ L'INSTANTANÉ N'EST PAS LA VÉRITÉ, et c'est ce qui rend l'ensemble sûr. La
// vérité est `games_history`, écrit par le moteur à chaque fin de partie.
// L'instantané est jetable : `reconstruire()` le refait à partir de rien. Deux
// sources de vérité finissent toujours par diverger ; celle-ci a le droit de se
// tromper parce qu'on peut la jeter.
"use strict";

import { paliers } from "./legacy-catalogue.js";
import { parcours } from "./legacy.js";

/** Une fiche vierge : le mode n'a jamais été activé. */
export function ficheVide() {
    return { actif: false, depuis: 0, jetonsDepenses: [], instantane: null };
}

/** Remet une fiche quelconque dans la forme attendue.
 *
 *  ⚠ ON NE FAIT CONFIANCE À RIEN de ce qui sort du fichier : il a pu être
 *  écrit par une version précédente, tronqué par une coupure, ou édité à la
 *  main. Un champ manquant vaut sa valeur par défaut, jamais `undefined` qui
 *  se propagerait jusqu'à l'écran. */
export function normaliser(brut) {
    const fiche = ficheVide();
    if (!brut || typeof brut !== "object") return fiche;
    fiche.actif = !!brut.actif;
    const depuis = Number(brut.depuis);
    fiche.depuis = Number.isFinite(depuis) && depuis > 0 ? depuis : 0;
    fiche.jetonsDepenses = Array.isArray(brut.jetonsDepenses)
        ? [...new Set(brut.jetonsDepenses.map(String).filter(Boolean))] : [];
    fiche.instantane = (brut.instantane && typeof brut.instantane === "object")
        ? brut.instantane : null;
    return fiche;
}

/** Lit la fiche du compte. Rend une fiche vierge si rien n'est écrit. */
export async function lire() {
    try {
        const reponse = await fetch("/get_legacy", { cache: "no-store" });
        if (!reponse.ok) return ficheVide();
        return normaliser(await reponse.json());
    } catch (e) {
        // Moteur muet : on ne bloque pas l'écran de préparation pour autant.
        return ficheVide();
    }
}

/** Écrit la fiche. Rend `true` si le moteur l'a acceptée. */
export async function ecrire(fiche) {
    try {
        const reponse = await fetch("/save_legacy", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(normaliser(fiche)),
        });
        return reponse.ok;
    } catch (e) {
        return false;
    }
}

/** L'historique des parties de ce compte. */
export async function historique() {
    try {
        const reponse = await fetch("/get_games_history", { cache: "no-store" });
        if (!reponse.ok) return [];
        const parties = await reponse.json();
        return Array.isArray(parties) ? parties : [];
    } catch (e) {
        return [];
    }
}

/** L'état complet du mode : la fiche, et le parcours qu'elle décrit.
 *
 *  ⚠ LE PARCOURS EST TOUJOURS RECALCULÉ, l'instantané n'est jamais cru sur
 *  parole. Il ne sert qu'à répondre vite à une question sans intérêt pour le
 *  jeu (« où en est ce compte ? », depuis l'extérieur). Faire l'inverse aurait
 *  laissé une photo périmée décider de ce qui est verrouillé.
 */
export async function etat(t = (x) => x) {
    const [fiche, parties, mesPaliers] = await Promise.all([
        lire(), historique(), paliers(t),
    ]);
    return { fiche, paliers: mesPaliers, parcours: parcours(mesPaliers, parties, fiche) };
}

/** Active le mode. `repartirDeZero` choisit le chemin, UNE FOIS.
 *
 *  ⚠ UNE ACTIVATION NE SE REJOUE PAS. Réactiver un mode déjà actif remettrait
 *  la date de départ à aujourd'hui et effacerait tout le parcours de quelqu'un
 *  qui a seulement recliqué. On rend la fiche telle quelle.
 */
export async function activer(repartirDeZero, maintenant = Date.now()) {
    const fiche = await lire();
    if (fiche.actif) return fiche;
    fiche.actif = true;
    // L'historique porte des instants UNIX en SECONDES (`games_history`), pas
    // en millisecondes : diviser ici, une fois, plutôt que partout ailleurs.
    fiche.depuis = repartirDeZero ? Math.floor(maintenant / 1000) : 0;
    await ecrire(fiche);
    return fiche;
}

/** Dépense un jeton sur un héros fan-made.
 *
 *  Rend `{ ok, raison }`. Refuse sans jeton libre, et refuse deux fois le même
 *  héros : sans ce second contrôle, un double clic coûtait deux jetons pour un
 *  seul héros.
 */
export async function acheter(heroId, t = (x) => x) {
    const id = String(heroId || "");
    if (!id) return { ok: false, raison: t("héros inconnu") };
    const { fiche, parcours: p } = await etat(t);
    if (fiche.jetonsDepenses.includes(id)) {
        return { ok: false, raison: t("déjà débloqué") };
    }
    if (p.jetons.restants < 1) return { ok: false, raison: t("aucun jeton") };
    fiche.jetonsDepenses.push(id);
    const ecrit = await ecrire(fiche);
    return ecrit ? { ok: true, fiche } : { ok: false, raison: t("écriture refusée") };
}

/** Refait l'instantané à partir de l'historique, et l'écrit.
 *
 *  L'outil de reconstruction promis par la spec : la fiche peut être perdue,
 *  tronquée ou périmée, tout ce qui compte se retrouve dans `games_history`.
 *  Seuls `depuis` et les jetons dépensés ne s'en déduisent pas, et ceux-là sont
 *  conservés tels quels.
 */
export async function reconstruire(t = (x) => x) {
    const { fiche, parcours: p } = await etat(t);
    fiche.instantane = {
        quand: Math.floor(Date.now() / 1000),
        vagueOuverte: p.vagueOuverte,
        jetons: p.jetons,
        vilainsBattus: [...p.gagnees.scenarios].length,
        herosVainqueurs: [...p.gagnees.heros].length,
    };
    await ecrire(fiche);
    return fiche;
}
