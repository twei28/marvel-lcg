// Pré-remplissage du panneau de récompenses : d'où vient chaque valeur.
//
// Trois sources, dans cet ordre strict :
//
//   1. le MOTEUR, quand la boîte a un collecteur `WriteCampaignLogAtGameOver`
//      (mts, mut_gen, next_evol, aoa) ET que ce qu'il a écrit vient bien du
//      scénario en cours (voir plus bas — rien n'efface jamais son fichier
//      sortant, donc rien ne garantit qu'il parle de CETTE partie) ;
//   2. les DÉTECTEURS, qui relisent le descripteur de monde. C'est la seule
//      source pour trors et sm, qui n'ont pas de collecteur ;
//   3. le CARNET déjà écrit, parce qu'il est cumulatif et que ce qui y était
//      noté ne doit pas se perdre.
//
// Les champs de type `choix` ne sont jamais pré-remplis par le moteur : ce sont
// les décisions que le livret laisse au joueur, et une décision ne se détecte
// pas. Leur valeur ancienne reste proposée, comme avant.
import type { World } from '../world'
import { cleCarnet, conditionRemplie, detecter, joueurElimine, type ChampVictoire } from './detecteurs'

export type EntreePreRemplissage = {
  champs: ChampVictoire[]
  monde: World
  /** Carnet déjà enregistré pour cette campagne. */
  carnet?: Record<string, string>
  /** Ce que le moteur a relevé à la fin de partie, par clé de carnet. */
  suggestions: Record<string, string>
  /**
   * Scénario qui a produit `suggestions` (estampille du moteur), ou `null`
   * si le fichier sortant est absent ou vide.
   *
   * `WriteCampaignLogAtGameOver` (côté moteur) écrit son carnet à CHAQUE fin
   * de partie des boîtes câblées, victoire comme défaite, et rien ne l'efface
   * jamais. Si un joueur termine un scénario d'une boîte câblée puis, plus
   * tard sur la même place, gagne un scénario d'une AUTRE campagne (câblée ou
   * non), le fichier contient encore les valeurs de la première partie : sans
   * cette comparaison, elles seraient présentées comme « relevées par le jeu »
   * pour un scénario qu'elles ne concernent pas.
   */
  scenarioSuggestions: string | null
  /** Scénario en cours, tel que déposé par l'écran des campagnes (`lireContexte().scenario`). */
  scenarioActuel: string
  /** Nombre de héros de la campagne : les clés « Player N » en dépendent. */
  total: number
}

export function preRemplir({
  champs,
  monde,
  carnet,
  suggestions,
  scenarioSuggestions,
  scenarioActuel,
  total,
}: EntreePreRemplissage): Record<string, string> {
  // Une estampille absente ou différente : on ignore le carnet moteur EN
  // BLOC, comme s'il n'avait rien dit. Un carnet partiellement d'un autre
  // scénario serait pire qu'aucun carnet — voir la documentation du champ
  // ci-dessus.
  const suggestionsUtilisables = scenarioSuggestions !== null && scenarioSuggestions === scenarioActuel
  const sortie: Record<string, string> = {}
  for (const champ of champs) {
    if (!conditionRemplie(champ, monde)) continue
    const joueurs = champ.parJoueur ? [...Array(total).keys()] : [0]
    for (const joueurId of joueurs) {
      // Un héros éliminé ne participe à AUCUNE étape de victoire (livret p17).
      if (champ.parJoueur && joueurElimine(monde, joueurId)) continue
      const cle = cleCarnet(champ, joueurId)
      const duMoteur = champ.type === 'auto' && suggestionsUtilisables ? suggestions[cle] : undefined
      const detectee = champ.type === 'auto' ? detecter(champ, monde, joueurId) : undefined
      const valeur = duMoteur ?? detectee ?? carnet?.[cle]
      if (valeur !== undefined) sortie[cle] = valeur
    }
  }
  return sortie
}
