// Pré-remplissage du panneau de récompenses : d'où vient chaque valeur.
//
// Trois sources, dans cet ordre strict :
//
//   1. le MOTEUR, quand la boîte a un collecteur `WriteCampaignLogAtGameOver`
//      (mts, mut_gen, next_evol, aoa). Il relève son propre état à la fin de
//      partie : il n'y a rien de plus sûr, et rien à redeviner ;
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
  /** Nombre de héros de la campagne : les clés « Player N » en dépendent. */
  total: number
}

export function preRemplir({
  champs,
  monde,
  carnet,
  suggestions,
  total,
}: EntreePreRemplissage): Record<string, string> {
  const sortie: Record<string, string> = {}
  for (const champ of champs) {
    if (!conditionRemplie(champ, monde)) continue
    const joueurs = champ.parJoueur ? [...Array(total).keys()] : [0]
    for (const joueurId of joueurs) {
      // Un héros éliminé ne participe à AUCUNE étape de victoire (livret p17).
      if (champ.parJoueur && joueurElimine(monde, joueurId)) continue
      const cle = cleCarnet(champ, joueurId)
      const duMoteur = champ.type === 'auto' ? suggestions[cle] : undefined
      const detectee = champ.type === 'auto' ? detecter(champ, monde, joueurId) : undefined
      const valeur = duMoteur ?? detectee ?? carnet?.[cle]
      if (valeur !== undefined) sortie[cle] = valeur
    }
  }
  return sortie
}
