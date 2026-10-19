import { describe, expect, it } from 'vitest'
import { reglesCachees } from './regles-cachees'
import type { EtapeDeroule } from './deroule-phase'

const base: EtapeDeroule = { cle: 'a', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu', boosts: [] }

describe('règles cachées : une ligne discrète quand elles jouent (T11)', () => {
  it('accélération sur la menace du point 1', () => {
    expect(reglesCachees({ ...base, titre: 'menace', temps: 'menace', acceleration: 1 })).toEqual(['Accélération : +1 menace'])
    expect(reglesCachees({ ...base, titre: 'menace', temps: 'menace', acceleration: 2 })).toEqual(['Accélération : +2 menaces'])
    expect(reglesCachees({ ...base, titre: 'menace', temps: 'menace', acceleration: 0 })).toEqual([])
  })
  it('★ d’un boost, nommé', () => {
    expect(reglesCachees({ ...base, boosts: [{ cle: 'b', cibleId: 1, nom: 'Assaut', apport: 0, etoile: true }] })).toEqual(['★ Assaut : effet de la carte'])
  })
  it('Perforant et Tenace', () => {
    expect(reglesCachees({ ...base, motsCles: { percant: true } })).toEqual(['Perforant : le Tenace est retiré'])
    expect(reglesCachees({ ...base, motsCles: { robuste: true } })).toEqual(['Tenace : défaussé à la place des dégâts'])
  })
  it('un ennemi désorienté attaque quand même', () => {
    expect(reglesCachees({ ...base, desoriente: true, etat: 'annonce' })).toEqual(['Désorienté : n’empêche pas d’attaquer'])
  })
  it('⚠ TÉMOIN : rien quand aucune règle ne joue', () => {
    expect(reglesCachees(base)).toEqual([])
    expect(reglesCachees({ ...base, titre: 'manigance', desoriente: true })).toEqual([])
  })
})
