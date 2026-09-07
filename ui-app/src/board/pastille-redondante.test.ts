// La pastille de type d'une carte doit se taire quand le titre de sa zone dit
// déjà la même chose : dans les zones étroites, elle se posait par-dessus lui.
import { describe, expect, it } from 'vitest'
import { pastilleRedondante } from './zones'
import type { ScanCardProps } from '../components/ScanCard'

const carte = (p: Partial<ScanCardProps>): ScanCardProps =>
  ({ id: '1', name: 'X', kind: 'villain', ...p }) as ScanCardProps

describe('pastilleRedondante', () => {
  it('se tait quand la zone porte exactement le nom du type', () => {
    expect(pastilleRedondante('Méchant', carte({ kind: 'villain' }))).toBe(true)
  })

  it('se tait quand le type est un mot du titre de la zone', () => {
    expect(pastilleRedondante('Alliés, sbires et environnement', carte({ kind: 'environment' }))).toBe(true)
  })

  it('se tait sur une carte face cachée : « Carte » n’apprend rien', () => {
    expect(pastilleRedondante('Deck Rencontre', carte({ facedown: true }))).toBe(true)
  })

  it('se tait quand labelType est vide : le rendu retombe sur le type', () => {
    // Les cartes du méchant portent `labelType: ''`. Avec `??`, la règle
    // comparait une chaîne vide et ne concluait jamais.
    expect(pastilleRedondante('Méchant', carte({ kind: 'villain', labelType: '' }))).toBe(true)
  })

  it('parle quand la zone dit autre chose', () => {
    expect(pastilleRedondante('Ta main', carte({ kind: 'ally' }))).toBe(false)
  })

  it('parle quand le type est plus précis que la zone', () => {
    expect(pastilleRedondante('Héros et soutiens', carte({ kind: 'alter-ego' }))).toBe(false)
  })
})
