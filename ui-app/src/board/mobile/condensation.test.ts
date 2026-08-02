import { describe, expect, it } from 'vitest'
import { condenser, type BudgetBande } from './condensation'
import type { UniteAffichee } from '../zones'

/** Une unite minimale : condenser() ne regarde que le nombre, jamais le contenu. */
function unites(nombre: number): UniteAffichee[] {
  return Array.from({ length: nombre }, (_, index) => ({
    cle: `u${index}`,
    carte: { id: String(index), name: `Carte ${index}`, kind: 'ally', imageUrl: '' },
    attachees: [],
  }))
}

const LARGE: BudgetBande = { largeur: 464, hauteur: 200 }
const ETROIT: BudgetBande = { largeur: 464, hauteur: 72 }
const MINUSCULE: BudgetBande = { largeur: 150, hauteur: 72 }

describe('condenser', () => {
  it('ne dessine rien pour une bande vide', () => {
    const bande = condenser([], LARGE)
    expect(bande.tuiles).toHaveLength(0)
    expect(bande.restantes).toBe(0)
  })

  it('garde la taille de confort quand tout tient', () => {
    const bande = condenser(unites(2), LARGE)
    expect(bande.taille).toBe('confort')
    expect(bande.tuiles).toHaveLength(2)
    expect(bande.restantes).toBe(0)
  })

  it('descend au plancher plutot que de replier', () => {
    // 8 unites ne tiennent pas en confort dans ce budget (capacite 6), mais
    // tiennent au plancher (capacite 8 = 4 colonnes x 2 rangees).
    const bande = condenser(unites(8), LARGE)
    expect(bande.taille).toBe('plancher')
    expect(bande.tuiles).toHaveLength(8)
    expect(bande.restantes).toBe(0)
  })

  it('replie le surplus dans une pastille et reserve sa place', () => {
    const bande = condenser(unites(20), ETROIT)
    expect(bande.taille).toBe('plancher')
    expect(bande.restantes).toBeGreaterThan(0)
    // Une place est reservee a la pastille « +N » : elle ne recouvre pas une tuile.
    expect(bande.tuiles.length + bande.restantes).toBe(20)
  })

  it('ne montre aucune tuile quand une seule place existe', () => {
    const bande = condenser(unites(5), MINUSCULE)
    expect(bande.tuiles).toHaveLength(0)
    expect(bande.restantes).toBe(5)
  })

  it('conserve toujours l\'invariant tuiles + restantes = total', () => {
    for (const nombre of [1, 3, 7, 12, 40]) {
      for (const budget of [LARGE, ETROIT, MINUSCULE]) {
        const bande = condenser(unites(nombre), budget)
        expect(bande.tuiles.length + bande.restantes).toBe(nombre)
        expect(bande.restantes).toBeGreaterThanOrEqual(0)
      }
    }
  })
})
