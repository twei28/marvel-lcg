// Rapport du 29/10/2026 (Gambit 48021) : « il me rouvre la fenetre a chaque fois, alors que j'ai deja choisi, et il n'en
// montre que deux ». Voir lots-regardes.ts.
import { describe, expect, it } from 'vitest'
import { avecVues, idsRegardes, lotDejaVu } from './lots-regardes'

const groupe = (...ids: string[]) => ({ cartes: ids.map((id) => ({ id })) })

describe('lotDejaVu', () => {
  it('un lot dont toutes les cartes ont ete fermees est deja vu', () => {
    expect(lotDejaVu(['a', 'b', 'c'], new Set(['a', 'b', 'c']))).toBe(true)
  })

  it('Gambit : 3 cartes fermees, puis 2 restantes apres le choix : rien de nouveau', () => {
    const vues = avecVues(new Set(), idsRegardes([groupe('a', 'b', 'c')]))
    expect(lotDejaVu(idsRegardes([groupe('a', 'c')]), vues)).toBe(true)
  })

  it('une carte jamais montree rouvre la fenetre', () => {
    expect(lotDejaVu(['a', 'z'], new Set(['a', 'b']))).toBe(false)
  })

  it('rien n\'a ete ferme : le lot est a montrer', () => {
    expect(lotDejaVu(['a', 'b'], new Set())).toBe(false)
  })
})

describe('avecVues', () => {
  it('rend une nouvelle table sans modifier l\'ancienne', () => {
    const avant = new Set(['a'])
    const apres = avecVues(avant, ['b'])
    expect([...avant]).toEqual(['a'])
    expect([...apres].sort()).toEqual(['a', 'b'])
  })
})

describe('idsRegardes', () => {
  it('met les groupes a plat, dans l\'ordre', () => {
    expect(idsRegardes([groupe('a', 'b'), groupe('c')])).toEqual(['a', 'b', 'c'])
  })
})
