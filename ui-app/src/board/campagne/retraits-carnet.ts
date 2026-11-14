// Les cartes qui se retirent du carnet de campagne (« Discard this card and remove it from the campaign log » : Tactical
// Scanner 04155-04158). Le moteur efface la clé dans le monde et la dit au descripteur (`campagne_retraits`) ; le carnet
// enregistré, lui, est cumulatif et garderait la carte : on la retire ici, à la fin du scénario.
import type { World } from '../world'

/** Le carnet SANS les clés que la partie vient de retirer. Un moteur plus ancien (champ absent) ne retire rien. */
export function sansRetraits(carnet: Record<string, string>, monde: Pick<World, 'campagne_retraits'>): Record<string, string> {
  const retraits = monde.campagne_retraits ?? []
  if (!retraits.length) return carnet
  const sortie = { ...carnet }
  for (const cle of retraits) delete sortie[cle]
  return sortie
}
