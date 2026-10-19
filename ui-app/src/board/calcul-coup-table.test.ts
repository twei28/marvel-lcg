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
  it('une ligne PAR SOURCE quand le jeu connaît l’origine du bonus (19/10/2026)', () => {
    const e = { ...attaque, base: 6, baseImprimee: 2, defense: 0, montant: 7, bonus: [{ source: 'Camouflé', valeur: 2, source_id: 11 }, { source: 'Fusil Laser', valeur: 2, source_id: 12 }] }
    expect(calculCoupTable(e)).toBe('ATQ 2 + 2 Camouflé + 2 Fusil Laser + Boost 1 = 7 dégâts')
  })
  it('ce que les sources n’expliquent pas reste « Bonus » ; le ★ d’un boost est nommé', () => {
    const e = { ...attaque, base: 5, baseImprimee: 2, defense: 0, montant: 6, bonus: [{ source: 'Fusil Laser', valeur: 2, source_id: 12 }] }
    expect(calculCoupTable(e)).toBe('ATQ 2 + 2 Fusil Laser + 1 Bonus + Boost 1 = 6 dégâts')
    const etoile = { ...attaque, base: 4, baseImprimee: 2, defense: 0, montant: 5, bonus: [{ source: 'Assaut', valeur: 2, source_id: 5 }] }
    expect(calculCoupTable(etoile)).toBe('ATQ 2 + 2 Assaut + Boost 1 = 5 dégâts')
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
