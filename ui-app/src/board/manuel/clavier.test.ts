import { describe, expect, it } from 'vitest'
import { creerEtatTouches, interpreterTouche } from './clavier'

const VILAIN = { genre: 'carte', id: 7, jetonNaturel: 'degats' } as const
const MANIGANCE = { genre: 'carte', id: 9, jetonNaturel: 'menace' } as const
const DECK = { genre: 'pile', zone: 'PlayerDeck' } as const

describe('les touches du mode manuel', () => {
  it('F retourne la carte survolee', () => {
    expect(interpreterTouche({ cle: 'f', majuscule: false }, VILAIN))
      .toEqual({ geste: 'retourner', id: 7 })
  })

  it('Q incline la carte survolee', () => {
    expect(interpreterTouche({ cle: 'q', majuscule: false }, VILAIN))
      .toEqual({ geste: 'incliner', id: 7 })
  })

  it('R melange la pile survolee', () => {
    expect(interpreterTouche({ cle: 'r', majuscule: false }, DECK))
      .toEqual({ geste: 'melanger', zone: 'PlayerDeck' })
  })

  it('R ne melange pas une carte', () => {
    expect(interpreterTouche({ cle: 'r', majuscule: false }, VILAIN)).toBeUndefined()
  })

  it('un chiffre sur une pile prend ce nombre de cartes', () => {
    expect(interpreterTouche({ cle: '5', majuscule: false }, DECK))
      .toEqual({ geste: 'piocher', zone: 'PlayerDeck', nombre: 5 })
  })

  it('un chiffre sur un personnage pose des degats', () => {
    expect(interpreterTouche({ cle: '3', majuscule: false }, VILAIN))
      .toEqual({ geste: 'jetons', id: 7, nature: 'degats', nombre: 3 })
  })

  it('un chiffre sur une manigance pose de la menace', () => {
    expect(interpreterTouche({ cle: '3', majuscule: false }, MANIGANCE))
      .toEqual({ geste: 'jetons', id: 9, nature: 'menace', nombre: 3 })
  })

  it('Maj plus chiffre retire autant', () => {
    expect(interpreterTouche({ cle: '3', majuscule: true }, VILAIN))
      .toEqual({ geste: 'jetons', id: 7, nature: 'degats', nombre: -3 })
  })

  it('ne devine pas le jeton d une carte qui n en a pas', () => {
    const evenement = { genre: 'carte', id: 4, jetonNaturel: 'aucun' } as const
    expect(interpreterTouche({ cle: '3', majuscule: false }, evenement)).toBeUndefined()
  })

  it('ignore une touche inconnue', () => {
    expect(interpreterTouche({ cle: 'z', majuscule: false }, VILAIN)).toBeUndefined()
  })
})

describe("l'etat des touches enfoncees (pour la tache 5)", () => {
  it('retient une touche enfoncee', () => {
    const etat = creerEtatTouches()
    etat.enregistrer({ key: 'Shift', type: 'keydown' })
    expect(etat.estEnfoncee('shift')).toBe(true)
  })

  it('oublie une touche relachee', () => {
    const etat = creerEtatTouches()
    etat.enregistrer({ key: 'Shift', type: 'keydown' })
    etat.enregistrer({ key: 'Shift', type: 'keyup' })
    expect(etat.estEnfoncee('shift')).toBe(false)
  })

  it('ignore la casse', () => {
    const etat = creerEtatTouches()
    etat.enregistrer({ key: 'A', type: 'keydown' })
    expect(etat.estEnfoncee('a')).toBe(true)
  })

  it('vaut faux avant toute touche', () => {
    const etat = creerEtatTouches()
    expect(etat.estEnfoncee('shift')).toBe(false)
  })
})
