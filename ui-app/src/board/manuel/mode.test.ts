import { describe, expect, it } from 'vitest'
import { estEnPause, estModeManuel, leMoteurSeTait } from './mode'
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

describe('reconnaitre une PAUSE d\'une partie ORDINAIRE (tache 3)', () => {
  // ⚠ DISTINCT de `leMoteurSeTait` tout seul : une partie DECLAREE manuelle a
  // aussi `manuel_actif` a vrai en permanence une fois la mise en place
  // terminee (`World.ManualLoop` n'est entree QUE si `rule.mode_manuel` est
  // vraie, cote moteur) -- ce n'est pas une PAUSE, c'est sa nature, et il n'y
  // a rien a « reprendre ». Une pause ad hoc, elle, ne peut survenir QUE sur
  // une partie ORDINAIRE (route `POST /manuel_pause`).
  it('vaut faux sans monde', () => {
    expect(estEnPause(undefined)).toBe(false)
  })

  it('vaut faux en partie ordinaire, hors pause', () => {
    expect(estEnPause({} as World)).toBe(false)
    expect(estEnPause({ manuel_actif: false } as World)).toBe(false)
  })

  it('vaut vrai quand une partie ORDINAIRE est mise en pause', () => {
    expect(estEnPause({ mode_manuel: false, manuel_actif: true } as World)).toBe(true)
    expect(estEnPause({ manuel_actif: true } as World)).toBe(true)
  })

  it('vaut faux en mode manuel DECLARE, meme boucle manuelle entree : '
    + 'ce n\'est pas une pause, c\'est la nature de la partie',
  () => {
    expect(estEnPause({ mode_manuel: true, manuel_actif: true } as World)).toBe(false)
  })
})
