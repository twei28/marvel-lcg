// « L'hôte a-t-il lancé le scénario suivant ? »
//
// Aucune route nouvelle : `/get_campagne_en_cours` dit déjà quel scénario est
// en cours, et l'écran des campagnes réécrit `partieEnCours` AVANT de lancer.
// Un scénario différent du nôtre signifie donc qu'une nouvelle partie a
// démarré, et qu'il est temps de recharger.
//
// Deux cas qui ne sont pas évidents, et que les tests verrouillent :
//
//  - entre la validation de l'hôte et son prochain lancement, `partieEnCours`
//    vaut null et la route rend un scénario VIDE. Recharger là renverrait les
//    distants sur un plateau mort ;
//  - sans scénario courant connu, tout changement paraîtrait en être un, et on
//    rechargerait en boucle.

export function scenarioSuivantLance(
  scenarioCourant: string,
  lu: { id?: string; scenario?: string } | null
): boolean {
  if (!scenarioCourant) return false
  if (!lu?.scenario) return false
  return lu.scenario !== scenarioCourant
}
