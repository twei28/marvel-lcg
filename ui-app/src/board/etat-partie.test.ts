import { describe, expect, it } from 'vitest'
import { libellePhase, libelleQuiAgit, libelleRound } from './etat-partie'
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

  it('en manuel, aucun repère de phase : le moteur se tait, sa phase ne veut plus rien dire', () => {
    // Constat du 06/10/2026 (lot 7) : après « Fin du round », la barre
    // affichait « ROUND 1 Init Finished », la phase brute où reste une partie
    // manuelle déclarée après sa mise en place.
    expect(libellePhase({ ...monde('Init Finished'), manuel_actif: true } as World)).toBe('')
    expect(libellePhase({ ...monde('Player 1 Turn'), manuel_actif: true } as World)).toBe('')
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

describe('libelleQuiAgit', () => {
  const etat = (aNous: boolean, demande = true) =>
    ({ aNous, connecte: true, demande: demande ? {} : undefined }) as Parameters<
      typeof libelleQuiAgit
    >[1]

  it('dit « À toi de jouer » quand le moteur attend le joueur local', () => {
    expect(libelleQuiAgit(monde('Player 1 Turn'), etat(true))).toBe('À toi de jouer')
  })

  it('nomme le héros attendu quand ce n’est pas notre tour', () => {
    expect(libelleQuiAgit(monde('Player 2 Turn'), etat(false))).toBe('En attente de Hulk')
  })

  it('dit que le méchant agit pendant sa phase', () => {
    expect(libelleQuiAgit(monde('Enemy Activation'), etat(false))).toBe('Le méchant agit')
  })

  it('reste muet sans monde ou hors connexion', () => {
    expect(libelleQuiAgit(undefined, etat(true))).toBe('')
    expect(
      libelleQuiAgit(monde('Player 1 Turn'), { aNous: true, connecte: false, demande: {} } as never)
    ).toBe('')
  })
})
