// bascule.js — la seule question du salon : LA partie qui tourne est-elle la MIENNE ?
//
// ⚠ POURQUOI CE MODULE EXISTE. Le 20/09/2026, deux fois dans la même soirée,
// des invités ont été expédiés dans la partie PRÉCÉDENTE avant d'avoir choisi
// leur héros, et y sont restés bloqués sur « Connexion à la partie… ».
// `surveillerLeLancement` basculait dès que `/get_play_scene_name` rendait
// autre chose qu'une chaîne vide, sur l'hypothèse — écrite noir sur blanc en
// commentaire — que la table est VIDE avant le lancement. Elle ne l'est pas :
// le moteur rend le nom de scène dès qu'un monde existe (server_get.py,
// `get_play_scene_name`), et il en existe un jusqu'au redémarrage. Le chemin le
// plus emprunté d'une soirée — jouer, écran de fin, « Retour au menu »,
// relancer — laisse donc toujours la partie précédente chargée.
//
// La règle juste ne regarde plus « une partie tourne » mais « le héros de MON
// siège, dans la partie en cours, est-il celui que je viens de choisir ? ».
// C'est la seule formulation qui soit insensible à l'ancienne partie encore
// chargée, au rechargement de page, à l'onglet fermé puis rouvert et à deux
// parties d'affilée sur le même scénario.
//
// ⚠ RÈGLES PURES, SANS AUCUN EFFET DE BORD : c'est ce qui les rend éprouvables
// sans moteur (ui-check/tests/bascule-salon.spec.ts), comme les règles de
// cadence du sondage de l'assistant.
"use strict";

/** Délai avant d'oser expliquer que la partie en cours n'est pas la sienne.
 *
 *  ⚠ IL FAUT UN DÉLAI, ET UN DÉLAI FRANC. « Mon siège ne tient pas mon héros »
 *  est EXACTEMENT ce que dit aussi une ancienne partie encore chargée, qui est
 *  le cas ordinaire pendant toute l'attente. Parler trop vite ferait donc dire
 *  au salon, à chaque soirée, que la partie est lancée sans l'invité alors que
 *  l'hôte n'a simplement pas encore cliqué. */
export const DELAI_EXPLICATION = 45000;

/** Durée de validité d'un choix mémorisé dans le navigateur de l'invité.
 *
 *  ⚠ POURQUOI CE N'EST PAS « POUR TOUJOURS ». Un choix oublié dans un
 *  navigateur, plus la partie de la veille encore chargée sur la table,
 *  ramènerait le défaut du 20/09 — plus étroit (il faudrait le même siège ET le
 *  même héros), mais le même. Six heures couvrent très largement une attente de
 *  salon sans jamais traverser deux soirées. */
export const DUREE_MEMOIRE = 6 * 60 * 60 * 1000;

/**
 * Que doit faire le salon, maintenant ?
 *
 * @param {object} etat
 * @param {string}  etat.monChoix   identifiant de la carte héros que CET invité a
 *   choisi (`heroCardId`), ou "" tant qu'il n'a rien choisi.
 * @param {boolean} etat.enJeu      une partie tourne-t-elle sur la table ?
 * @param {string}  etat.heros      identifiant de la carte héros que tient MON siège
 *   dans cette partie, ou "" si ce siège n'y a pas de héros.
 * @param {?number} etat.desaccordDepuis  date du premier sondage où la partie en
 *   cours a dit autre chose que mon choix, ou null si elle n'a rien dit de tel.
 * @param {number}  etat.maintenant date courante.
 * @returns {"attendre"|"basculer"|"expliquer"}
 */
export function decisionSalon({ monChoix, enJeu, heros, desaccordDepuis, maintenant }) {
    // Rien ne tourne : l'hôte n'a pas lancé, ou la table est neuve.
    if (!enJeu) return "attendre";

    // ⚠ TANT QUE L'INVITÉ N'A RIEN CHOISI, IL N'EST DANS AUCUNE PARTIE. C'est
    // ici, et nulle part ailleurs, que se ferme le défaut du 20/09 : l'invité
    // qui arrive sur une table portant encore la manche précédente reste devant
    // sa grille de héros au lieu d'être expédié dedans.
    if (!monChoix) return "attendre";

    // LA question. Mon siège tient mon héros : cette partie est la mienne.
    if (heros && heros === monChoix) return "basculer";

    // Mon siège tient autre chose, ou rien. Deux lectures possibles, et on ne
    // peut pas les départager : soit l'hôte n'a pas encore lancé MA partie (et
    // ce qu'on voit est l'ancienne), soit il a lancé sans ce siège — il avait
    // envoyé trois liens et n'a lancé qu'à deux. Passé un délai franc, on le
    // DIT, sans trancher, plutôt que de laisser l'invité devant un écran muet.
    if (desaccordDepuis != null && maintenant - desaccordDepuis >= DELAI_EXPLICATION) {
        return "expliquer";
    }
    return "attendre";
}

/* ---------------- La mémoire du choix, dans le navigateur de l'invité ------ */
//
// ⚠ POURQUOI ELLE EST NÉCESSAIRE. `/new` VIDE `choix_sieges` côté serveur, et
// c'est voulu : sans cela la partie suivante repartirait avec les choix de la
// précédente. Un invité qui recharge sa page APRÈS le lancement ne peut donc
// plus apprendre du serveur ce qu'il avait choisi, et sans mémoire locale il ne
// saurait pas se reconnaître dans la partie qui tourne.
//
// ⚠ ET ELLE DOIT ÊTRE CÔTÉ CLIENT. Un archivage côté serveur des choix « déjà
// joués » aurait l'air plus propre, mais il rouvrirait le défaut : l'archive de
// l'ancienne partie collerait à l'ancienne partie encore chargée, et un invité
// tout neuf basculerait dedans sans avoir rien choisi. C'est précisément parce
// que le choix vit dans SON navigateur qu'il distingue « moi » de « celui qui
// était assis là avant moi ».

/** La ligne de mémoire d'un siège. Une par siège : deux invités sur le même
 *  poste (deux onglets, un parent et son enfant) ne se marchent pas dessus. */
export function cleChoix(siege) {
    return `mc-salon-choix-${siege}`;
}

/** Retient le héros choisi, avec l'heure à laquelle il l'a été.
 *  Un stockage indisponible (navigation privée stricte) fait perdre la mémoire,
 *  jamais la page : le salon reste jouable, il oubliera seulement au
 *  rechargement. */
export function memoriserChoix(stockage, siege, heroCardId, maintenant) {
    try {
        stockage.setItem(cleChoix(siege), JSON.stringify({ h: String(heroCardId || ""), t: maintenant }));
    } catch (e) { /* stockage refusé : on continue sans mémoire */ }
}

/** Relit le héros choisi pour ce siège, ou "" s'il n'y en a pas ou s'il a
 *  passé l'âge (voir DUREE_MEMOIRE). */
export function relireChoix(stockage, siege, maintenant) {
    try {
        const brut = stockage.getItem(cleChoix(siege));
        if (!brut) return "";
        const { h, t } = JSON.parse(brut);
        if (!h || typeof t !== "number") return "";
        if (maintenant - t > DUREE_MEMOIRE) return "";
        return String(h);
    } catch (e) {
        return "";
    }
}

/** Efface la ligne d'un siège : le choix a servi, il ne doit pas traîner
 *  jusqu'à la soirée suivante. */
export function oublierChoix(stockage, siege) {
    try {
        stockage.removeItem(cleChoix(siege));
    } catch (e) { /* stockage refusé : rien à effacer de toute façon */ }
}
