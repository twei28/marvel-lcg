// Le drapeau « design essai » : la nouvelle barre, le nouveau bandeau et le
// nouvel assistant.
//
// Il est le DEFAUT depuis le 11/09/2026 (decision de l'utilisateur, apres
// essai) : c'est desormais l'ancien plateau qu'il faut demander, par
// ?design=classique ou en decochant la ligne dans Options. Le choix reste
// memorise par navigateur, comme les animations et les sons.

import { describe, expect, it } from 'vitest'
import { CLE_DESIGN_ESSAI, lireDesignEssai } from './design-essai'

function stockage(initial: Record<string, string> = {}) {
  const valeurs = new Map(Object.entries(initial))
  return {
    getItem: (cle: string) => valeurs.get(cle) ?? null,
    setItem: (cle: string, valeur: string) => void valeurs.set(cle, valeur),
    valeurs,
  }
}

describe('lireDesignEssai', () => {
  it('est allumé par défaut', () => {
    expect(lireDesignEssai('', stockage())).toBe(true)
    expect(lireDesignEssai('?p=0', stockage())).toBe(true)
  })

  it('suit le réglage mémorisé', () => {
    expect(lireDesignEssai('?p=0', stockage({ [CLE_DESIGN_ESSAI]: 'on' }))).toBe(true)
    expect(lireDesignEssai('?p=0', stockage({ [CLE_DESIGN_ESSAI]: 'off' }))).toBe(false)
  })

  it('?design=essai l’allume et le mémorise', () => {
    const memoire = stockage()
    expect(lireDesignEssai('?p=0&design=essai', memoire)).toBe(true)
    expect(memoire.valeurs.get(CLE_DESIGN_ESSAI)).toBe('on')
  })

  it('?design=classique l’éteint et le mémorise', () => {
    const memoire = stockage({ [CLE_DESIGN_ESSAI]: 'on' })
    expect(lireDesignEssai('?design=classique', memoire)).toBe(false)
    expect(memoire.valeurs.get(CLE_DESIGN_ESSAI)).toBe('off')
  })

  it('reste allumé si le stockage refuse', () => {
    const casse = {
      getItem: () => {
        throw new Error('refusé')
      },
      setItem: () => {
        throw new Error('refusé')
      },
    }
    expect(lireDesignEssai('?design=essai', casse)).toBe(true)
    expect(lireDesignEssai('', casse)).toBe(true)
  })
})
