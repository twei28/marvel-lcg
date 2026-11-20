// defausse-fin-tour.ts — la défausse FACULTATIVE de la fin de tour ne s'ouvre plus en fenêtre.
//
// Inventaire des fenêtres du 19/11/2026 (demande nicodede62, « trop de pop-ups ») : à CHAQUE « Fin du tour », le moteur
// demande « défausse autant de cartes que tu veux » (`player_phase.py`, `MayDiscardHandCardsAndDrawUpToMax("End Phase")`,
// de 0 à toute la main). L'écran l'affichait en fenêtre au milieu du plateau, avec un seul bouton mal nommé (« SCIENTIFIQUE »,
// le nom imprimé de la capacité de Peter Parker). Presque personne ne défausse : choix de l'utilisateur, la question est
// répondue d'office par « aucune carte », et le réglage « Proposer de défausser en fin de tour » (éteint par défaut) la remet.
// Quand la main dépasse sa taille maximale, la défausse est OBLIGATOIRE (minimum > 0) : la question reste posée.
import type { Demande, Option, Reponse } from './ask'

const CLE = 'marvel-board-defausse-fin-tour'

/**
 * Le joueur veut-il qu'on lui propose de défausser en fin de tour ? Défaut : OUI (20/11/2026 : le jeu ne répond plus à la place du
 * joueur, même par « aucune carte » ; l'automatisme n'existe que si le joueur l'a choisi lui-même, réglage éteint).
 */
export function lireProposerDefausseFinTour(): boolean {
  try {
    return window.localStorage.getItem(CLE) !== 'off'
  } catch {
    return true
  }
}

export function ecrireProposerDefausseFinTour(actif: boolean): void {
  try {
    window.localStorage.setItem(CLE, actif ? 'on' : 'off')
  } catch {
    /* préférence non critique */
  }
}

/** L'option de défausse de fin de phase du joueur (« End Phase »), quelle que soit sa borne. */
export function estDefausseFinDePhase(option: Pick<Option, 'name' | 'is_search'>): boolean {
  return option.name === 'End Phase' && option.is_search
}

/** La réponse « ne rien défausser » à envoyer d'office, ou `undefined` quand le joueur doit répondre lui-même. */
export function reponseDefausseFacultative(demande: Demande | undefined, proposer: boolean): Reponse | undefined {
  if (proposer || !demande) return undefined
  const jouables = demande.options.filter((o) => o.failure_reason === '')
  if (jouables.length !== 1) return undefined
  const option = jouables[0]!
  if (!estDefausseFinDePhase(option) || option.target_num_range[0] !== 0) return undefined
  return { id: option.id, targets: [], resources: [] }
}
