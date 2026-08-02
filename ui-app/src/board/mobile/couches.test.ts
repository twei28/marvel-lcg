import { StrictMode, createElement, type ReactNode } from 'react'
import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { depiler, empiler, sommet, useCouches, type Couche } from './couches'

const FOCUS: Couche = { sorte: 'focus', bande: 'heros' }
const CARTE: Couche = { sorte: 'carte', id: '42' }

describe('pile des couches', () => {
  it('est vide au depart', () => {
    expect(sommet([])).toBeUndefined()
    expect(depiler([])).toEqual([])
  })

  it('empile et depile une couche a la fois', () => {
    const pile = empiler(empiler([], FOCUS), CARTE)
    expect(pile).toHaveLength(2)
    expect(sommet(pile)).toEqual(CARTE)
    expect(sommet(depiler(pile))).toEqual(FOCUS)
  })

  it("n'empile pas deux fois la meme couche", () => {
    const pile = empiler(empiler([], FOCUS), FOCUS)
    expect(pile).toHaveLength(1)
  })

  it('ne modifie jamais la pile recue', () => {
    const depart: Couche[] = [FOCUS]
    empiler(depart, CARTE)
    depiler(depart)
    expect(depart).toEqual([FOCUS])
  })
})

// Enveloppe StrictMode : React double-invoque en developpement les fonctions
// passees a un setState pour verifier qu'elles sont pures. Si l'effet de bord
// (pushState) vit dans cette fonction, il se declenche deux fois pour une
// seule ouverture logique et desynchronise la pile de l'historique. C'est le
// cas que les tests ci-dessous verifient.
function enveloppeStrict({ children }: { children: ReactNode }) {
  return createElement(StrictMode, null, children)
}

describe('useCouches relie a l\'historique du navigateur', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('empile une seule entree d\'historique par ouverture, meme sous StrictMode', () => {
    const pushState = vi.spyOn(window.history, 'pushState')
    const { result } = renderHook(() => useCouches(), { wrapper: enveloppeStrict })

    act(() => {
      result.current.ouvrir(FOCUS)
    })

    expect(pushState).toHaveBeenCalledOnce()
    expect(result.current.pile).toEqual([FOCUS])
  })

  it('n\'empile pas d\'entree quand la couche est deja au sommet', () => {
    const pushState = vi.spyOn(window.history, 'pushState')
    const { result } = renderHook(() => useCouches(), { wrapper: enveloppeStrict })

    act(() => {
      result.current.ouvrir(FOCUS)
    })
    pushState.mockClear()

    act(() => {
      result.current.ouvrir(FOCUS)
    })

    expect(pushState).not.toHaveBeenCalled()
    expect(result.current.pile).toEqual([FOCUS])
  })

  it('demande a l\'historique de reculer d\'autant de crans que de couches ouvertes', () => {
    const go = vi.spyOn(window.history, 'go').mockImplementation(() => {})
    const { result } = renderHook(() => useCouches(), { wrapper: enveloppeStrict })

    act(() => {
      result.current.ouvrir(FOCUS)
    })
    act(() => {
      result.current.ouvrir(CARTE)
    })

    act(() => {
      result.current.toutFermer()
    })

    expect(go).toHaveBeenCalledExactlyOnceWith(-2)
  })

  it('ferme via history.back(), jamais en retirant la couche directement', () => {
    const back = vi.spyOn(window.history, 'back').mockImplementation(() => {})
    const { result } = renderHook(() => useCouches(), { wrapper: enveloppeStrict })

    act(() => {
      result.current.ouvrir(FOCUS)
    })
    act(() => {
      result.current.fermer()
    })

    expect(back).toHaveBeenCalledOnce()
    // La pile ne bouge que par popstate : fermer() seul ne la modifie pas.
    expect(result.current.pile).toEqual([FOCUS])
  })

  it('retire la couche du sommet quand le navigateur signale un retour', () => {
    const { result } = renderHook(() => useCouches(), { wrapper: enveloppeStrict })

    act(() => {
      result.current.ouvrir(FOCUS)
    })
    act(() => {
      result.current.ouvrir(CARTE)
    })

    act(() => {
      window.dispatchEvent(new PopStateEvent('popstate'))
    })

    expect(result.current.pile).toEqual([FOCUS])
  })
})
