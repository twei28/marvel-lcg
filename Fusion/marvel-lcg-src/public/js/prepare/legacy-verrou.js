// legacy-verrou.js — ce qui est ouvert, ce qui est fermé, et pourquoi.
//
// Le troisième et dernier module pur de Legacy. `legacy.js` dit quels paliers
// sont franchis ; `legacy-catalogue.js` fabrique les paliers ; celui-ci répond
// à la seule question que l'écran pose des centaines de fois : « ce héros, ce
// scénario, je peux le prendre ? et sinon, qu'est-ce qu'il me faut ? ».
//
// ⚠ AUCUNE ENTRÉE-SORTIE, comme les deux autres : on lui passe l'état, il
// rend des tables de consultation. L'écran ne calcule rien, il lit.
"use strict";

import { cleNom, condition } from "./legacy.js";

/** Le libellé d'une étape, court, pour la ligne de condition. */
function nomCourt(etape, t) {
    return etape.nom || `${t("Vague")} ${etape.vague}`;
}

/** Fabrique le verrou à partir de l'état du mode (voir `legacy-fiche.etat`)
 *  et de la liste des héros du catalogue.
 *
 *  Rend :
 *    heros(h)      -> { ouvert, etiquette, condition, achetable }
 *    scenario(sc)  -> { ouvert, etiquette, condition }
 *
 *  ⚠ DEUX TEXTES, PAS UN. `etiquette` est court (« Vague 4 · The Mad Titan's
 *  Shadow », « 1 jeton ») et s'écrit SUR la vignette ; `condition` est la
 *  phrase entière, pour l'infobulle et le bandeau. Écrire la phrase entière
 *  sur soixante vignettes couvrait les portraits et se répétait soixante fois,
 *  vu sur un vrai rendu.
 *    prochaine     -> l'étape en cours (ouverte, pas encore franchie), ou null
 *                     quand tout est franchi
 *    jetons        -> { gagnes, depenses, restants }
 */
export function fabriquerVerrou(etat, heros, t = (x) => x) {
    const etapes = (etat.parcours && etat.parcours.etapes) || [];
    const parVague = new Map(etapes.map((e) => [e.vague, e]));
    // La marche à franchir maintenant : la première ouverte et non franchie.
    // C'est elle que toute condition cite, quel que soit l'éloignement de ce
    // qu'on regarde : on ne peut rien faire d'autre avant.
    const prochaine = etapes.find((e) => e.ouvert && !e.franchi) || null;
    const jetons = (etat.parcours && etat.parcours.jetons) || { gagnes: 0, depenses: 0, restants: 0 };
    const achetes = new Set((etat.fiche && etat.fiche.jetonsDepenses) || []);

    /** « Vague 3 · The Galaxy's Most Wanted. D'abord : bats Klaw et gagne avec
     *  Thor. » On nomme la boîte visée, puis ce qui manque MAINTENANT. */
    function phrasePourVague(vague) {
        const cible = parVague.get(vague);
        const morceaux = [];
        if (cible) morceaux.push(nomCourt(cible, t));
        if (prochaine) {
            const quoi = condition(prochaine, t);
            if (quoi) morceaux.push(`${t("D'abord")} : ${quoi}`);
        }
        return morceaux.join(". ");
    }

    const cacheHeros = new Map();
    function verrouHeros(h) {
        const cle = h.heroCardId || h.id;
        if (cacheHeros.has(cle)) return cacheHeros.get(cle);
        let sortie;
        if (h.homebrew || h.vague === null || h.vague === undefined) {
            // Fan-made : ni libre ni verrouillé, il s'achète.
            const ouvert = achetes.has(String(h.heroCardId));
            sortie = ouvert
                ? { ouvert: true, etiquette: "", condition: "", achetable: false }
                : { ouvert: false, achetable: jetons.restants > 0,
                    etiquette: t("1 jeton"),
                    condition: jetons.restants > 0
                        ? t("1 jeton : clique pour le débloquer")
                        : t("1 jeton. Gagne d'abord avec un héros officiel.") };
        } else {
            const etape = parVague.get(h.vague);
            const ouvert = !!(etape && etape.ouvert);
            sortie = { ouvert, achetable: false,
                       etiquette: ouvert ? "" : (etape ? nomCourt(etape, t) : ""),
                       condition: ouvert ? "" : phrasePourVague(h.vague) };
        }
        cacheHeros.set(cle, sortie);
        return sortie;
    }

    // Les scénarios se retrouvent par leur nom, comme dans l'historique.
    const vagueDuScenario = new Map();
    for (const palier of etat.paliers || []) {
        for (const s of palier.scenarios || []) vagueDuScenario.set(cleNom(s.nom), palier.vague);
    }
    function verrouScenario(sc) {
        const vague = vagueDuScenario.get(cleNom(sc.name));
        // Un scénario hors vague (défi, fan-made, variante) n'est pas dans le
        // parcours : il reste libre, on n'invente pas de règle pour lui.
        if (vague === undefined) return { ouvert: true, etiquette: "", condition: "" };
        const etape = parVague.get(vague);
        const ouvert = !!(etape && etape.ouvert);
        return { ouvert, etiquette: ouvert ? "" : (etape ? nomCourt(etape, t) : ""),
                 condition: ouvert ? "" : phrasePourVague(vague) };
    }

    return { heros: verrouHeros, scenario: verrouScenario, prochaine, jetons,
             vagueOuverte: (etat.parcours && etat.parcours.vagueOuverte) || 0 };
}
