import { describe, expect, it } from 'vitest'
import { cleLaPlusRecente, indexSpectateur } from './etape-partagee'

describe('etape suivie par le spectateur', () => {
  it('suit le joueur qui a lu le plus recemment', () => {
    expect(cleLaPlusRecente({ 0: { cle: 'menace', t: 10 }, 1: { cle: 'attaque', t: 12 } })).toBe('attaque')
  })
  it('ignore un joueur sans etape', () => {
    expect(cleLaPlusRecente({ 0: { cle: 'menace', t: 10 }, 1: { cle: '', t: 12 } })).toBe('menace')
    expect(cleLaPlusRecente({})).toBeUndefined()
  })
  it('montre l etape du joueur, meme si une suivante est deja connue', () => {
    expect(indexSpectateur(['menace', 'attaque', 'bilan'], 'attaque')).toBe(1)
  })
  it('cle inconnue ou absente : la derniere etape connue', () => {
    expect(indexSpectateur(['menace', 'attaque'], 'ancienne')).toBe(1)
    expect(indexSpectateur(['menace', 'attaque'], undefined)).toBe(1)
    expect(indexSpectateur([], undefined)).toBe(0)
  })
})
