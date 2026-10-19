import { describe, expect, it } from 'vitest'
import { calculCoupTable } from './calcul-coup-table'
import type { EtapeDeroule } from './deroule-phase'
const attaque: EtapeDeroule = { cle: 'a', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu', base: 2, montant: 1, defense: 2, boosts: [{ cle: 'b', cibleId: 5, nom: 'Boost', apport: 1 }] }
describe('calcul visible du résultat sur table', () => {
  it('montre les boosts et la défense dans une égalité exacte', () => {
    expect(calculCoupTable(attaque)).toBe('ATQ 2 + Boost 1 − DÉF 2 = 1 dégât')
  })
  it('sépare bonus imprimés et réduction de dégâts nommée', () => {
    expect(calculCoupTable({ ...attaque, baseImprimee: 1, montant: 0, reductions: [{ source: 'Barrière énergétique', valeur: 1 }] })).toBe('ATQ 1 + 1 Bonus + Boost 1 − DÉF 2 − 1 Barrière énergétique = 0 dégâts')
  })
  it('ne ment pas sur les dégâts réellement subis après Tenace ou une prévention inconnue', () => {
    expect(calculCoupTable({ ...attaque, defense: 0, montant: 0 })).toBe('ATQ 2 + Boost 1 = 3 → 0 dégâts')
  })
  it('reste muet avant le résultat et ne devine pas les statistiques manquantes', () => {
    expect(calculCoupTable({ ...attaque, etat: 'annonce' })).toBeUndefined()
    expect(calculCoupTable({ ...attaque, base: undefined })).toBeUndefined()
  })
  it('traite les manigances sans soustraire une défense et nomme le boost étoile', () => {
    expect(calculCoupTable({ ...attaque, titre: 'manigance', montant: 3, boosts: [{ ...attaque.boosts[0], etoile: true }] })).toBe('MEN 2 + Boost 1 ★ = 3 menaces')
  })
})
