import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import {
  CLE_MODE,
  REQUETE_MOBILE,
  ecrireReglage,
  lireReglage,
  modeEffectif,
  useModeMobile,
} from './useModeMobile'

/** Une media query évaluée à la main, pour éprouver la règle sans navigateur. */
function correspond(requete: string, largeur: number, hauteur: number): boolean {
  return requete.split(',').some((clause) => {
    const max = /\(max-(width|height):\s*(\d+)px\)/.exec(clause.trim())
    if (!max) return false
    return (max[1] === 'width' ? largeur : hauteur) <= Number(max[2])
  })
}

describe('REQUETE_MOBILE : le petit côté décide', () => {
  it('prend les téléphones, debout comme couchés', () => {
    expect(correspond(REQUETE_MOBILE, 390, 844)).toBe(true)
    expect(correspond(REQUETE_MOBILE, 844, 390)).toBe(true)
  })

  it('LAISSE les tablettes au plateau PC, dans les deux sens', () => {
    expect(correspond(REQUETE_MOBILE, 768, 1024)).toBe(false)
    expect(correspond(REQUETE_MOBILE, 1024, 768)).toBe(false)
  })

  it('laisse un ordinateur au plateau PC', () => {
    expect(correspond(REQUETE_MOBILE, 1440, 900)).toBe(false)
  })
})

describe('modeEffectif', () => {
  it('suit la media query en mode auto', () => {
    expect(modeEffectif('auto', true)).toBe('mobile')
    expect(modeEffectif('auto', false)).toBe('pc')
  })

  it('laisse forcer le mode PC sur un telephone', () => {
    expect(modeEffectif('pc', true)).toBe('pc')
  })

  // Le piege qu'on ferme ici : un reglage `mobile` memorise faisait basculer un
  // PC en bandes, et le panneau qui contient le reglage devenait inatteignable.
  // Aucun retour possible sans vider le localStorage a la main.
  it("n'accepte JAMAIS de rendre un PC en mode telephone", () => {
    expect(modeEffectif('mobile', false)).toBe('pc')
    expect(modeEffectif('auto', false)).toBe('pc')
    expect(modeEffectif('pc', false)).toBe('pc')
  })
})

describe('reglage memorise', () => {
  beforeEach(() => window.localStorage.clear())

  it('vaut auto quand rien n\'est memorise', () => {
    expect(lireReglage()).toBe('auto')
  })

  it('relit ce qui a ete ecrit', () => {
    ecrireReglage('mobile')
    expect(window.localStorage.getItem(CLE_MODE)).toBe('mobile')
    expect(lireReglage()).toBe('mobile')
  })

  it('retombe sur auto devant une valeur inconnue', () => {
    window.localStorage.setItem(CLE_MODE, 'tablette')
    expect(lireReglage()).toBe('auto')
  })
})

describe('useModeMobile', () => {
  const ecouteurs = new Set<(evenement: MediaQueryListEvent) => void>()
  let retraits = 0

  beforeEach(() => {
    ecouteurs.clear()
    retraits = 0
    window.localStorage.clear()
    // Bouchon pilotable : celui de test-setup.ts repond toujours matches: false.
    vi.stubGlobal('matchMedia', (media: string) => ({
      media,
      matches: true,
      addEventListener: (_: string, ecouteur: (evenement: MediaQueryListEvent) => void) => {
        ecouteurs.add(ecouteur)
      },
      removeEventListener: () => {
        retraits += 1
      },
    }))
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('rend le mode mobile quand la media query correspond', () => {
    const { result } = renderHook(() => useModeMobile())
    expect(result.current.mode).toBe('mobile')
  })

  it('laisse le reglage force gagner sur la media query', () => {
    ecrireReglage('pc')
    const { result } = renderHook(() => useModeMobile())
    expect(result.current.mode).toBe('pc')
  })

  it('retire son ecouteur au demontage', () => {
    const { unmount } = renderHook(() => useModeMobile())
    expect(ecouteurs.size).toBe(1)
    unmount()
    expect(retraits).toBe(1)
  })
})
