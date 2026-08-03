import { StrictMode, createElement, type ReactNode } from 'react'
import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  depiler,
  empiler,
  remplacerSommet,
  sommet,
  useCoucheCarte,
  useCouches,
  useCouchesBoard,
  type Couche,
} from './couches'

const FOCUS: Couche = { sorte: 'focus', bande: 'heros' }
const CARTE: Couche = { sorte: 'carte', id: '42' }
const SELECTEUR: Couche = { sorte: 'selecteur' }

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
    remplacerSommet(depart, CARTE)
    expect(depart).toEqual([FOCUS])
  })

  it('echange la couche du sommet sans changer la profondeur', () => {
    const pile = remplacerSommet([FOCUS, CARTE], SELECTEUR)
    expect(pile).toEqual([FOCUS, SELECTEUR])
  })

  it('ne remplace rien sur une pile vide, ni par la couche deja au sommet', () => {
    expect(remplacerSommet([], SELECTEUR)).toEqual([])
    const pile: Couche[] = [FOCUS, CARTE]
    expect(remplacerSommet(pile, CARTE)).toBe(pile)
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

  it('vide la pile immediatement au toutFermer, sans attendre les popstate', () => {
    // history.go(-n) ne declenche PAS forcement n popstate : jsdom (et des
    // navigateurs reels) coalescent un saut de plusieurs crans en un seul
    // evenement. Si la pile ne se videait qu'au fil des popstate, elle
    // resterait a moitie pleine ici : c'est le bug que ce test verrouille.
    vi.spyOn(window.history, 'go').mockImplementation(() => {})
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

    expect(result.current.pile).toEqual([])
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

describe('useCoucheCarte : le menu d\'actions dans la pile', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  /**
   * Le menu appartient a board.tsx : on simule sa prop `carteFocalisee` et le
   * `defocaliser` qu'il fournit, exactement comme le fait PlateauMobile.
   */
  function monter() {
    const fermerMenu = vi.fn()
    const { result, rerender } = renderHook(
      ({ carte }: { carte: number | undefined }) => {
        const couches = useCouches()
        useCoucheCarte(carte, couches, fermerMenu)
        return couches
      },
      { wrapper: enveloppeStrict, initialProps: { carte: undefined as number | undefined } }
    )
    return { result, rerender, fermerMenu }
  }

  it('empile une couche « carte » a l\'ouverture du menu, une seule fois', () => {
    const pushState = vi.spyOn(window.history, 'pushState')
    const { result, rerender } = monter()

    act(() => {
      rerender({ carte: 42 })
    })

    expect(result.current.pile).toEqual([{ sorte: 'carte', id: '42' }])
    expect(pushState).toHaveBeenCalledOnce()
  })

  it('le Retour depile la couche ET demande la fermeture du menu', () => {
    const { result, rerender, fermerMenu } = monter()

    act(() => {
      rerender({ carte: 42 })
    })
    act(() => {
      window.dispatchEvent(new PopStateEvent('popstate'))
    })

    expect(result.current.pile).toEqual([])
    expect(fermerMenu).toHaveBeenCalledOnce()
  })

  it('ne rouvre pas la couche apres un Retour, meme si le menu tarde a se fermer', () => {
    const { result, rerender } = monter()

    act(() => {
      rerender({ carte: 42 })
    })
    act(() => {
      window.dispatchEvent(new PopStateEvent('popstate'))
    })
    // Le menu est encore ouvert cote board.tsx : rien ne doit se reempiler.
    act(() => {
      rerender({ carte: 42 })
    })

    expect(result.current.pile).toEqual([])
  })

  it('depile quand board.tsx ferme le menu de lui-meme', () => {
    const back = vi.spyOn(window.history, 'back')
    const { rerender } = monter()

    act(() => {
      rerender({ carte: 42 })
    })
    act(() => {
      rerender({ carte: undefined })
    })

    expect(back).toHaveBeenCalledOnce()
  })

  it('laisse la feuille de focus sous le menu de carte', () => {
    const { result, rerender } = monter()

    act(() => {
      result.current.ouvrir(FOCUS)
    })
    act(() => {
      rerender({ carte: 42 })
    })

    expect(result.current.pile).toEqual([FOCUS, { sorte: 'carte', id: '42' }])
  })
})

describe('useCouchesBoard : le selecteur de cibles dans la pile', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  type Etat = { carte: number | undefined; selecteur: boolean }

  /**
   * Les deux panneaux appartiennent a board.tsx : on simule ses deux props et
   * les deux fermetures qu'il fournit, exactement comme le fait PlateauMobile.
   */
  function monter() {
    const fermerMenu = vi.fn()
    const fermerSelecteur = vi.fn()
    const { result, rerender } = renderHook(
      ({ carte, selecteur }: Etat) => {
        const couches = useCouches()
        useCouchesBoard(carte, selecteur, couches, fermerMenu, fermerSelecteur)
        return couches
      },
      {
        wrapper: enveloppeStrict,
        initialProps: { carte: undefined, selecteur: false } as Etat,
      }
    )
    return { result, rerender, fermerMenu, fermerSelecteur }
  }

  it('empile une couche « selecteur » quand le ciblage hors table s\'ouvre', () => {
    const pushState = vi.spyOn(window.history, 'pushState')
    const { result, rerender } = monter()

    act(() => {
      rerender({ carte: undefined, selecteur: true })
    })

    expect(result.current.pile).toEqual([SELECTEUR])
    expect(pushState).toHaveBeenCalledOnce()
  })

  it('remplace le menu par le selecteur sans pousser de seconde entree', () => {
    const back = vi.spyOn(window.history, 'back').mockImplementation(() => {})
    const pushState = vi.spyOn(window.history, 'pushState')
    const { result, rerender } = monter()

    act(() => {
      rerender({ carte: 42, selecteur: false })
    })
    // Choisir une capacite a cibles : board.tsx cache le menu et montre le
    // selecteur dans le MEME rendu. Une seule couche est visible, donc une
    // seule entree d'historique, et surtout aucun back() qui croiserait un
    // pushState dans le meme tick.
    act(() => {
      rerender({ carte: undefined, selecteur: true })
    })

    expect(result.current.pile).toEqual([SELECTEUR])
    expect(pushState).toHaveBeenCalledOnce()
    expect(back).not.toHaveBeenCalled()
  })

  it('le Retour sur le selecteur abandonne le ciblage au lieu de quitter la partie', () => {
    const { result, rerender, fermerMenu, fermerSelecteur } = monter()

    act(() => {
      rerender({ carte: 42, selecteur: false })
    })
    act(() => {
      rerender({ carte: undefined, selecteur: true })
    })
    act(() => {
      window.dispatchEvent(new PopStateEvent('popstate'))
    })

    expect(result.current.pile).toEqual([])
    expect(fermerSelecteur).toHaveBeenCalledOnce()
    expect(fermerMenu).not.toHaveBeenCalled()
  })

  it('rend la couche au menu quand le ciblage est abandonne', () => {
    const back = vi.spyOn(window.history, 'back').mockImplementation(() => {})
    const pushState = vi.spyOn(window.history, 'pushState')
    const { result, rerender } = monter()

    act(() => {
      rerender({ carte: undefined, selecteur: true })
    })
    act(() => {
      rerender({ carte: 42, selecteur: false })
    })

    expect(result.current.pile).toEqual([CARTE])
    expect(pushState).toHaveBeenCalledOnce()
    expect(back).not.toHaveBeenCalled()
  })

  it('depile quand board.tsx ferme le selecteur de lui-meme', () => {
    const back = vi.spyOn(window.history, 'back')
    const { rerender } = monter()

    act(() => {
      rerender({ carte: undefined, selecteur: true })
    })
    act(() => {
      rerender({ carte: undefined, selecteur: false })
    })

    expect(back).toHaveBeenCalledOnce()
  })

  it('laisse la feuille de focus sous le selecteur', () => {
    const { result, rerender } = monter()

    act(() => {
      result.current.ouvrir(FOCUS)
    })
    act(() => {
      rerender({ carte: undefined, selecteur: true })
    })

    expect(result.current.pile).toEqual([FOCUS, SELECTEUR])
  })
})
