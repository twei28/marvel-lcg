import { describe, expect, it } from 'vitest'
import { estModeManuel } from './mode'
import type { World } from '../world'

describe('reconnaitre une partie manuelle', () => {
  it('vaut faux sans monde', () => {
    expect(estModeManuel(undefined)).toBe(false)
  })

  it('vaut faux en partie ordinaire', () => {
    expect(estModeManuel({} as World)).toBe(false)
  })

  it('vaut faux en bac a sable seul', () => {
    expect(estModeManuel({ mode_sandbox: true } as World)).toBe(false)
  })

  it('vaut vrai quand le moteur le dit', () => {
    expect(estModeManuel({ mode_manuel: true } as World)).toBe(true)
  })
})
