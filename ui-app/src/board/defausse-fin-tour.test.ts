// La défausse facultative de fin de tour ne s'ouvre plus en fenêtre (inventaire des fenêtres, 19/11/2026).
import { afterEach, describe, expect, it } from 'vitest'
import type { Demande, Option } from './ask'
import { nomDeCapacite } from './DemandeCentrale'
import { ecrireProposerDefausseFinTour, lireProposerDefausseFinTour, reponseDefausseFacultative } from './defausse-fin-tour'

// La question telle que le moteur l'envoie (relevée sur Spider-Man contre Rhino, « Spider-Man End Phase »).
function finDePhase(mini: number): Option {
  return {
    id: 1, name: 'End Phase', bind_id: 1, bind_player_id: 0, all_legal_targets: [31, 39, 28, 45, 32, 46],
    target_num_range: [mini, 6], target_payment: {}, select_rule: '', target_must_include_traits: [], failure_reason: '',
    is_search: true, is_text_choice: true,
  } as Option
}
const demande = (option: Option): Demande =>
  ({ options: [option], refus: [], prompt_text: 'Spider-Man End Phase', event_name: 'End Turn', show_cancel: false, ability_type: 'Normal' }) as Demande

afterEach(() => window.localStorage.clear())

describe('défausse de fin de tour', () => {
  it('facultative (0 au minimum) : répondue d’office par « aucune carte »', () => {
    expect(reponseDefausseFacultative(demande(finDePhase(0)), false)).toEqual({ id: 1, targets: [], resources: [] })
  })
  it('réglage allumé : la question reste au joueur', () => {
    expect(reponseDefausseFacultative(demande(finDePhase(0)), true)).toBeUndefined()
  })
  it('obligatoire (main trop grande) : la question reste au joueur', () => {
    expect(reponseDefausseFacultative(demande(finDePhase(2)), false)).toBeUndefined()
  })
  it('une autre question n’est jamais répondue', () => {
    expect(reponseDefausseFacultative(demande({ ...finDePhase(0), name: 'Resolve Mulligans' }), false)).toBeUndefined()
  })
  it('la question est proposée par défaut ; l’automatisme n’existe que si le joueur l’éteint lui-même', () => {
    expect(lireProposerDefausseFinTour()).toBe(true)
    ecrireProposerDefausseFinTour(false)
    expect(lireProposerDefausseFinTour()).toBe(false)
    ecrireProposerDefausseFinTour(true)
    expect(lireProposerDefausseFinTour()).toBe(true)
  })
  it('le bouton dit ce qu’il fait, pas « Scientifique » (nom de la capacité de Peter Parker)', () => {
    const texteIdentite = 'Scientifique — Ressource : générez une ressource [mental].'
    expect(nomDeCapacite(finDePhase(2), texteIdentite)).toBe('Défausser et piocher')
  })
})
