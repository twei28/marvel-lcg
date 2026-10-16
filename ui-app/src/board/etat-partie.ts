// etat-partie.ts — où en est la partie, en une ligne pour la barre du haut.
//
// Le moteur publie `round_id` et `phase`, cette dernière en anglais et dans
// ses propres termes (« Player 1 Turn », « Enemy Activation »). La barre du
// haut n'en disait rien : dix boutons, et aucune information de jeu. Cette
// ligne répond à la question qu'on se pose en revenant à l'écran : « on en
// est où ? ».

import { t } from './langue'
import { PHASES_DU_MECHANT_ORDONNEES, type PhaseDuMechant } from './moteur'
import { leMoteurSeTait } from './manuel/mode'
import { traduireMoteur } from './vocabulaire-moteur'
import type { World } from './world'

const ETAPES_DU_MECHANT: Record<PhaseDuMechant, string> = {
  'Main Scheme Place Threat': 'Menace',
  'Enemy Activation': 'Activations',
  'Deal Encounter Cards': 'Distribution',
  'Reveal Encounter Cards': 'Révélation',
}

/** Le nom du héros au siège donné (numéro de joueur du moteur, à partir de 1). */
function nomDuHeros(monde: World, numero: number): string | undefined {
  const joueur = monde.players?.[numero - 1]
  return joueur?.area_hero?.[0]?.name?.replace(/^\W*/, '').trim() || undefined
}

/** Le héros (ou l'alter ego, selon sa face) dont c'est le tour, s'il y en a un. */
export function nomDuHerosDuTour(monde: World | undefined): string | undefined {
  const tour = monde?.phase?.match(/^Player (\d+) Turn$/)
  return monde && tour ? nomDuHeros(monde, Number(tour[1])) : undefined
}

/** La phase en cours, dite au joueur. */
export function libellePhase(monde: World | undefined): string {
  if (!monde) return ''
  // En manuel, le moteur se tait : sa phase est figée (« Init Finished » sur une
  // partie déclarée) et ne dit plus où en est la table. Spec du 18/09 : aucun
  // repère de phase en manuel.
  if (leMoteurSeTait(monde)) return ''
  const phase = monde.phase ?? ''
  const tour = phase.match(/^Player (\d+) Turn$/)
  if (tour) {
    const heros = nomDuHeros(monde, Number(tour[1]))
    return heros ? `${t('Tour de')} ${heros}` : `${t('Tour du joueur')} ${tour[1]}`
  }
  if (phase === 'Player Turn End') return t('Fin du tour')
  if (phase === 'Resolve Mulligans') return t('Mulligans')
  if (phase === 'Initialize') return t('Initialisation')
  if ((PHASES_DU_MECHANT_ORDONNEES as readonly string[]).includes(phase)) {
    return `${t('Phase du méchant')} · ${t(ETAPES_DU_MECHANT[phase as PhaseDuMechant])}`
  }
  return phase ? traduireMoteur(phase) : ''
}

/** « Round 3 », ou rien tant que la partie n'a pas commencé. */
export function libelleRound(monde: World | undefined): string {
  if (!monde || typeof monde.round_id !== 'number' || monde.round_id <= 0) return ''
  return `${t('Round')} ${monde.round_id}`
}

/**
 * Qui doit agir, en trois mots : « À toi de jouer », « En attente de Hulk »,
 * « Le méchant agit ». Le troisième segment du bandeau (design essai) : le
 * round dit où on en est, la phase dit quoi, ce libellé dit QUI. À plusieurs,
 * c'est la question qu'on se pose vraiment en revenant à l'écran.
 */
export function libelleQuiAgit(
  monde: World | undefined,
  etat: { aNous: boolean; connecte: boolean; demande?: unknown }
): string {
  if (!monde || !etat.connecte) return ''
  if (etat.aNous && etat.demande !== undefined) return t('À toi de jouer')
  const phase = monde.phase ?? ''
  if ((PHASES_DU_MECHANT_ORDONNEES as readonly string[]).includes(phase)) {
    return t('Le méchant agit')
  }
  const tour = phase.match(/^Player (\d+) Turn$/)
  if (tour) {
    const heros = nomDuHeros(monde, Number(tour[1]))
    return heros ? `${t('En attente de')} ${heros}` : `${t('En attente du joueur')} ${tour[1]}`
  }
  return ''
}
