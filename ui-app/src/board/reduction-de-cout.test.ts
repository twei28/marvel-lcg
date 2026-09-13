// Un moyen de paiement qui REDUIT le cout au lieu de fournir des ressources.
//
// Star-Lord (17001a) : « Interrupt : quand vous jouez une carte de votre main,
// donnez-vous 1 carte rencontre face cachee → reduisez de 3 le cout de cette
// carte. » Le moteur en fait un moyen de paiement ordinaire, mais son
// `res_text` n'est PAS une suite d'icones : c'est « -3 »
// (`Resources.color_text`, game/element/resources.py:55).
//
// `valeurMoyen` ne comptait que les lettres de couleur et retombait sur son
// repli « au moins 1 », donc la reduction de 3 valait UNE ressource : Element
// Gun (cout 3) restait bloquee a 1/3 et le joueur devait payer 2 de plus.
// Signale en partie par Yarro le 13/09/2026.
import { describe, expect, it } from 'vitest'
import { valeurMoyen, valeurPayee, type Paiement } from './ask'

const paiement = (...moyens: Array<[number, string]>): Paiement =>
  ({
    cost: '3',
    payment: moyens.map(([effect_id, res_text]) => ({ effect_id, res_text })),
    rule: [],
  }) as unknown as Paiement

describe('valeurMoyen', () => {
  it('compte les icones d une carte a ressources', () => {
    expect(valeurMoyen('B')).toBe(1)
    expect(valeurMoyen('BB')).toBe(2)
    expect(valeurMoyen('RRR')).toBe(3)
  })

  it('lit une REDUCTION de cout, ecrite en negatif', () => {
    expect(valeurMoyen('-3')).toBe(3) // Star-Lord
    expect(valeurMoyen('-1')).toBe(1)
    expect(valeurMoyen('-2')).toBe(2)
  })

  it('garde son repli a 1 pour un moyen sans texte lisible', () => {
    expect(valeurMoyen('')).toBe(1)
    expect(valeurMoyen('???')).toBe(1)
  })

  // Un « +3 » n'existe pas cote moteur, mais le repli ne doit pas se laisser
  // prendre par un signe quelconque : seule la forme negative est une reduction.
  it('ne prend pas un nombre positif pour une reduction', () => {
    expect(valeurMoyen('3')).toBe(1)
  })
})

describe('valeurPayee', () => {
  it('la reduction de Star-Lord paie les 3 ressources d Element Gun', () => {
    expect(valeurPayee(paiement([7, '-3']), [7])).toBe(3)
  })

  it('une reduction se cumule avec de vraies ressources', () => {
    expect(valeurPayee(paiement([7, '-3'], [9, 'BB']), [7, 9])).toBe(5)
  })
})
