// bascule.js — la seule question du salon : LA partie qui tourne est-elle la MIENNE ?
//
// ⚠ POURQUOI CE MODULE EXISTE. Le 20/09/2026, deux fois dans la même soirée,
// des invités ont été expédiés dans la partie PRÉCÉDENTE avant d'avoir choisi
// leur héros, et y sont restés bloqués sur « Connexion à la partie… ».
// `surveillerLeLancement` basculait dès que `/get_play_scene_name` rendait
// autre chose qu'une chaîne vide, sur l'hypothèse — écrite noir sur blanc en
// commentaire — que la table est VIDE avant le lancement. Elle ne l'est pas :
// le moteur rend le nom de scène dès qu'un monde existe, et il en existe un
// jusqu'au redémarrage. Le chemin le plus emprunté d'une soirée — jouer, écran
// de fin, « Retour au menu », relancer — laisse toujours la manche précédente
// chargée.
//
// ⚠⚠ ET LE HÉROS SEUL NE SUFFIT PAS (ronde de correction du 21/09/2026). La
// première version de ce module basculait dès que le héros du siège valait
// celui qu'on venait de choisir. Elle rouvrait le défaut en grand sur le cas le
// plus banal qui soit : REJOUER UNE MANCHE AVEC LE MÊME HÉROS. Entre deux
// manches, le moteur porte encore le monde de la précédente, avec le héros de
// l'invité à son siège ; `/new` ayant vidé `choix_sieges`, l'invité re-choisit,
// reprend le même héros — et son siège « tient son héros » dans l'ANCIENNE
// partie. Aucune mémoire n'est en cause : le choix est refait en direct.
//
// IL FAUT DONC DEUX SIGNAUX, et aucun des deux ne tient seul :
//   - LE HÉROS, qui dit « ce siège est à moi » — aveugle quand le héros ne
//     change pas d'une manche à l'autre ;
//   - LA FRAÎCHEUR, qui dit « cette partie a commencé APRÈS que je me suis
//     posé » — aveugle au rechargement si on la relève à l'arrivée, ce qui
//     avait fait écarter le compteur de génération.
// Ensemble ils tiennent : le repère est relevé AU MOMENT DU CHOIX et voyage
// avec lui dans la mémoire de l'invité, donc il survit au rechargement.
//
// ⚠ RÈGLES PURES, SANS AUCUN EFFET DE BORD : c'est ce qui les rend éprouvables
// sans moteur (ui-check/tests/bascule-salon.spec.ts), comme les règles de
// cadence du sondage de l'assistant.
"use strict";

/** Délai avant de PROPOSER de rejoindre une partie qu'on ne sait pas dater.
 *
 *  ⚠ CE N'EST PAS LE CAS ORDINAIRE, c'est le résidu : un invité dont le
 *  navigateur n'a aucun repère (données effacées, autre appareil) et qui arrive
 *  APRÈS le lancement. Il ne peut pas savoir si la partie qui tourne est la
 *  sienne. Le délai évite de lui poser la question pendant qu'il choisit
 *  tranquillement, alors que l'hôte n'a simplement pas encore cliqué. */
export const DELAI_PROPOSITION = 45000;

/** Durée de validité du repère mémorisé dans le navigateur de l'invité.
 *
 *  ⚠ POURQUOI CE N'EST PAS « POUR TOUJOURS ». Un repère oublié dans un
 *  navigateur vaudrait pour la soirée suivante et ferait prendre la partie de
 *  la veille pour une partie neuve. Six heures couvrent très largement une
 *  attente de salon sans jamais traverser deux soirées. */
export const DUREE_MEMOIRE = 6 * 60 * 60 * 1000;

/**
 * Que doit faire le salon, maintenant ?
 *
 * @param {object} etat
 * @param {string}  etat.monChoix   identifiant de la carte héros que CET invité a
 *   choisi (`heroCardId`), ou "" tant qu'il n'a rien choisi.
 * @param {boolean} etat.sansChoix  vrai en CAMPAGNE, où il n'y a rien à choisir :
 *   l'équipe est fixée par le livret. La fraîcheur décide alors seule — le héros
 *   ne peut pas servir de signal, puisqu'il est le MÊME à toutes les manches.
 * @param {?string} etat.debutAuChoix  repère de la partie qui tournait au moment
 *   où cet invité s'est posé, ou null s'il n'en a aucun.
 * @param {boolean} etat.enJeu      une partie tourne-t-elle sur la table ?
 * @param {string}  etat.heros      identifiant de la carte héros que tient MON siège
 *   dans cette partie, ou "" si ce siège n'y a pas de héros.
 * @param {string}  etat.debut      repère de la partie en cours.
 * @param {?number} etat.attenteDepuis  depuis quand ce salon attend (date).
 * @param {number}  etat.maintenant date courante.
 * @returns {"attendre"|"basculer"|"sans-toi"|"proposer"}
 */
export function decisionSalon({
    monChoix, sansChoix, debutAuChoix, enJeu, heros, debut, attenteDepuis, maintenant,
}) {
    // Rien ne tourne : l'hôte n'a pas lancé, ou la table est neuve.
    if (!enJeu) return "attendre";

    // ⚠ TANT QUE L'INVITÉ N'A RIEN CHOISI, IL N'EST DANS AUCUNE PARTIE. C'est
    // la première barrière contre le défaut du 20/09 : l'invité qui arrive sur
    // une table portant encore la manche précédente reste devant sa grille de
    // héros au lieu d'être expédié dedans. En campagne il n'y a rien à choisir,
    // donc cette barrière-là ne s'applique pas.
    if (!sansChoix && !monChoix) return "attendre";

    const delaiEcoule = attenteDepuis != null
        && maintenant - attenteDepuis >= DELAI_PROPOSITION;

    // Aucun repère : on ne sait pas dater ce qui tourne, donc on n'affirme
    // rien. Après un délai franc, on PROPOSE, et c'est l'invité qui tranche.
    if (debutAuChoix == null) return delaiEcoule ? "proposer" : "attendre";

    // ⚠ LE SIGNAL QUI FERME LE CAS DE LA MANCHE REJOUÉE. Le repère n'a pas
    // bougé : ce qui tourne est LA PARTIE QUI TOURNAIT DÉJÀ quand je me suis
    // posé. Quel que soit le héros qu'elle porte à mon siège, ce n'est pas la
    // mienne, et LE TEMPS N'Y CHANGE RIEN.
    //
    // ⚠⚠ IL Y AVAIT ICI UNE « CLAUSE DE RÉSERVE », ET ELLE ROUVRAIT LE CAS 7
    // SOUS FORME DE BOUTON (ronde 2 du 21/09/2026). Passé 45 s, elle proposait
    // de rejoindre — c'est-à-dire, dans le scénario exact du cas 7, d'aller sur
    // la manche PRÉCÉDENTE, à chaque soirée où l'hôte tarde un peu. En campagne
    // c'était pire : `sansChoix` la satisfaisait seul, sans aucun contrôle de
    // héros, donc TOUT invité s'y voyait offrir la manche d'hier.
    //
    // Son motif (« j'ai peut-être perdu mon repère ») ne tenait pas : un repère
    // perdu laisse `debutAuChoix` à null, et c'est la branche du dessus.
    // `debut === debutAuChoix` est au contraire la PREUVE POSITIVE que la
    // partie qui tourne précède mon choix.
    //
    // Le seul cas réel qu'elle couvrait était une course de moins d'une seconde
    // entre l'envoi du choix et la lecture qui suivait. Il est fermé ailleurs,
    // et mieux : le salon relève son repère AVANT d'envoyer son choix.
    if (debut === debutAuChoix) return "attendre";

    // Une partie a commencé DEPUIS que je me suis posé.
    // En campagne, cela suffit : l'équipe est fixée par le livret, il n'y a
    // aucun choix à reconnaître, et la seule question était « une partie
    // a-t-elle démarré depuis que je suis arrivé ? ».
    if (sansChoix) return "basculer";
    if (heros && heros === monChoix) return "basculer";

    // Elle a commencé, et mon siège n'y tient pas mon héros. Cette fois on peut
    // l'AFFIRMER, sans délai et sans devinette : l'hôte a lancé sans ce siège,
    // ou en a changé le héros.
    return "sans-toi";
}

/* ---------------- Le repère de l'invité, dans SON navigateur --------------- */
//
// ⚠ POURQUOI IL EST CÔTÉ CLIENT. `/new` VIDE `choix_sieges` côté serveur, et
// c'est voulu : sans cela la partie suivante repartirait avec les choix de la
// précédente. Un invité qui recharge sa page APRÈS le lancement ne peut donc
// plus rien apprendre du serveur. Et un archivage serveur des choix « déjà
// joués » ne servirait à rien : il collerait à l'ancienne partie et porterait
// exactement le même angle mort que le héros seul. Ce qui distingue « moi » de
// « celui qui était assis là avant moi », c'est le repère DE FRAÎCHEUR relevé
// au moment où je me suis posé — et lui ne peut venir que d'ici.

/** La ligne de mémoire d'un siège. Une par siège : deux invités sur le même
 *  poste (deux onglets, un parent et son enfant) ne se marchent pas dessus. */
export function cleRepere(siege) {
    return `mc-salon-repere-${siege}`;
}

/** Retient le héros choisi ET le repère de ce qui tournait à cet instant.
 *  En campagne, `heroCardId` vaut "" : seul le repère compte.
 *  Un stockage indisponible (navigation privée stricte) fait perdre la mémoire,
 *  jamais la page. */
export function memoriserRepere(stockage, siege, heroCardId, debut, maintenant) {
    try {
        stockage.setItem(cleRepere(siege), JSON.stringify({
            h: String(heroCardId || ""), d: String(debut || ""), t: maintenant,
        }));
    } catch (e) { /* stockage refusé : on continue sans mémoire */ }
}

/** Relit le repère de ce siège : `{heros, debut}`, ou null s'il n'y en a pas
 *  ou s'il a passé l'âge (voir DUREE_MEMOIRE). */
export function relireRepere(stockage, siege, maintenant) {
    try {
        const brut = stockage.getItem(cleRepere(siege));
        if (!brut) return null;
        const { h, d, t } = JSON.parse(brut);
        if (typeof t !== "number" || typeof d !== "string") return null;
        if (maintenant - t > DUREE_MEMOIRE) return null;
        return { heros: String(h || ""), debut: d };
    } catch (e) {
        return null;
    }
}

/** Efface la ligne d'un siège : le repère a servi, il ne doit pas traîner
 *  jusqu'à la soirée suivante. */
export function oublierRepere(stockage, siege) {
    try {
        stockage.removeItem(cleRepere(siege));
    } catch (e) { /* stockage refusé : rien à effacer de toute façon */ }
}
