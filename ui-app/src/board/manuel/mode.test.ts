import { describe, expect, it } from 'vitest'
import { estModeManuel, leMoteurSeTait } from './mode'
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

  it('vaut vrai quand le moteur le dit, meme pendant la mise en place', () => {
    // La REGLE est vraie des la creation de la partie : `estModeManuel` ne
    // doit RIEN savoir du silence du moteur, seulement de la nature de la
    // partie (tache 8 bis).
    expect(estModeManuel({ mode_manuel: true } as World)).toBe(true)
    expect(estModeManuel({ mode_manuel: true, manuel_actif: false } as World)).toBe(true)
  })
})

describe('reconnaitre que le moteur s\'est tu (tache 8 bis)', () => {
  it('vaut faux sans monde', () => {
    expect(leMoteurSeTait(undefined)).toBe(false)
  })

  it('vaut faux en partie ordinaire', () => {
    expect(leMoteurSeTait({} as World)).toBe(false)
  })

  it('vaut faux PENDANT LA MISE EN PLACE d\'une partie manuelle : la regle est '
    + 'deja vraie, mais la boucle manuelle n\'a pas encore pris la main',
  () => {
    expect(leMoteurSeTait({ mode_manuel: true } as World)).toBe(false)
    expect(leMoteurSeTait({ mode_manuel: true, manuel_actif: false } as World)).toBe(false)
  })

  it('vaut vrai une fois la boucle manuelle entree', () => {
    expect(leMoteurSeTait({ mode_manuel: true, manuel_actif: true } as World)).toBe(true)
  })
})
