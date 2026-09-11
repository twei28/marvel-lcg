// Le drapeau « design essai » : la nouvelle barre et le nouvel assistant ne
// s'affichent que pour qui l'a demandé. Deux portes : l'URL du plateau
// (?design=essai, pour l'activer sur un téléphone sans fouiller les menus) et
// le réglage mémorisé, comme les autres préférences du plateau. Éteint, le
// plateau est celui d'aujourd'hui, à l'octet près.

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
  it('est éteint par défaut', () => {
    expect(lireDesignEssai('', stockage())).toBe(false)
    expect(lireDesignEssai('?p=0', stockage())).toBe(false)
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

  it('reste éteint si le stockage refuse', () => {
    const casse = {
      getItem: () => {
        throw new Error('refusé')
      },
      setItem: () => {
        throw new Error('refusé')
      },
    }
    expect(lireDesignEssai('?design=essai', casse)).toBe(true)
    expect(lireDesignEssai('', casse)).toBe(false)
  })
})
