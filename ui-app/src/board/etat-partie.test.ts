import { describe, expect, it } from 'vitest'
import { libellePhase, libelleRound } from './etat-partie'
import type { World } from './world'

const monde = (phase: string, round = 3): World =>
  ({
    render_id: 1,
    round_id: round,
    phase,
    prompt: '',
    players: [{ area_hero: [{ name: '* Spider-Man' }] }, { area_hero: [{ name: 'Hulk' }] }],
  }) as unknown as World

describe('libellePhase', () => {
  it('nomme le héros dont c’est le tour', () => {
    expect(libellePhase(monde('Player 1 Turn'))).toBe('Tour de Spider-Man')
    expect(libellePhase(monde('Player 2 Turn'))).toBe('Tour de Hulk')
  })

  it('retombe sur le numéro du joueur sans héros connu', () => {
    expect(libellePhase(monde('Player 4 Turn'))).toBe('Tour du joueur 4')
  })

  it('détaille l’étape de la phase du méchant', () => {
    expect(libellePhase(monde('Enemy Activation'))).toBe('Phase du méchant · Activations')
    expect(libellePhase(monde('Main Scheme Place Threat'))).toBe('Phase du méchant · Menace')
  })

  it('reste muet sans monde, et traduit le reste par le vocabulaire moteur', () => {
    expect(libellePhase(undefined)).toBe('')
    expect(libellePhase(monde('End Phase'))).toBe('Fin de phase')
  })
})

describe('libelleRound', () => {
  it('écrit le round, et rien avant le premier', () => {
    expect(libelleRound(monde('Player 1 Turn', 2))).toBe('Round 2')
    expect(libelleRound(monde('Player 1 Turn', 0))).toBe('')
    expect(libelleRound(undefined)).toBe('')
  })
})
