// LE TEMPS D'ARRÊT SUR LA FACE A DE LA MANIGANCE PRINCIPALE.
//
// Le moteur pose une vraie question avant de retourner une face A
// (`World.ConfirmMainSchemeReveal`, world.py). Elle voyage comme n'importe
// quelle question, avec UNE option nommée `Reveal_Main_Scheme`.
//
// ⚠ CE MODULE EST PUR. Aucune lecture du DOM, aucun rendu : de quoi vérifier
// la règle de reconnaissance sans navigateur.

import type { Demande, Option } from './ask'
import type { World, WorldCard } from './world'

/**
 * Le nom TECHNIQUE de l'option, tel que le moteur le publie. Il ne s'affiche
 * jamais : le panneau pose son propre libellé traduit.
 *
 * ⚠ SANS ESPACE. Le moteur remplace les espaces par des underscores dans les
 * noms d'options publiés : un nom à espaces ne s'apparierait jamais.
 */
export const NOM_OPTION_MANIGANCE = 'Reveal_Main_Scheme'

/**
 * La question de la manigance, ou `undefined` si ce n'est pas ce moment-là.
 *
 * ⚠ EXIGE QU'ELLE SOIT SEULE. Si le moteur propose autre chose en même temps,
 * le joueur a un vrai choix à faire et le panneau n'a pas à s'en emparer.
 */
export function questionDeLaManigance(demande: Demande | undefined): Option | undefined {
  if (!demande) return undefined
  if (demande.options.length !== 1) return undefined
  const seule = demande.options[0]
  return seule && seule.name === NOM_OPTION_MANIGANCE ? seule : undefined
}

/**
 * La manigance à montrer en grand : celle qui est EN JEU à cet instant.
 *
 * Au moment de la question, le moteur n'a pas encore retourné la carte : la
 * zone porte donc la face A. On ne déduit pas son identifiant, on lit la table.
 */
export function maniganceAMontrer(monde: World | undefined): WorldCard | undefined {
  const zone = monde?.area_schemes_main
  if (!Array.isArray(zone)) return undefined
  return zone[0]
}

/** Ce qu'il faut savoir pour décider si l'ouverture reste voilée. */
export type EtatOuverture = {
  /** Le monde dit qu'une question de face A est attendue (`confirm_main_scheme`). */
  confirmAttendue: boolean
  /** `round_id` : 0 pendant la mise en place, 1 au premier round. */
  round: number
  /** La question de la manigance est à l'écran. */
  questionArrivee: boolean
  /** Le voile a déjà été levé une fois dans cette partie. */
  dejaLevee: boolean
}

/**
 * Le voile d'ouverture : la table n'apparaît qu'une fois montée.
 *
 * ⚠ AUCUNE MINUTERIE DE SECOURS, et c'est voulu. Le repli « au bout de N
 * secondes on affiche quand même » masquerait un vrai défaut le jour où la
 * question ne vient pas. La porte est explicite : on ne voile QUE si le monde
 * dit qu'une question est attendue.
 */
export function ouvertureEncoreVoilee(etat: EtatOuverture): boolean {
  if (etat.dejaLevee) return false
  if (!etat.confirmAttendue) return false
  if (etat.round > 0) return false
  return !etat.questionArrivee
}
