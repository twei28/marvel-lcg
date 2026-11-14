import { describe, expect, it } from 'vitest'
import { sansRetraits } from './retraits-carnet'

describe('sansRetraits', () => {
  const carnet = { 'Player 1 Tech Upgrade': '04156', 'Player 2 Tech Upgrade': '04156', 'Player 1 Basic Upgrade': '04160a' }

  it('retire la clé du joueur qui a utilisé la carte, pas celle de l\'autre joueur', () => {
    expect(sansRetraits(carnet, { campagne_retraits: ['Player 1 Tech Upgrade'] })).toEqual({
      'Player 2 Tech Upgrade': '04156',
      'Player 1 Basic Upgrade': '04160a',
    })
  })

  it('ne touche pas au carnet d\'origine', () => {
    sansRetraits(carnet, { campagne_retraits: ['Player 1 Tech Upgrade'] })
    expect(carnet['Player 1 Tech Upgrade']).toBe('04156')
  })

  it('un moteur sans le champ, ou sans retrait, rend le carnet tel quel', () => {
    expect(sansRetraits(carnet, {})).toBe(carnet)
    expect(sansRetraits(carnet, { campagne_retraits: [] })).toBe(carnet)
  })

  it('une clé retirée qui n\'est pas au carnet ne fait rien', () => {
    expect(sansRetraits(carnet, { campagne_retraits: ['Player 3 Tech Upgrade'] })).toEqual(carnet)
  })
})
