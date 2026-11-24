// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useFenetreFlottante } from './useFenetreFlottante'

afterEach(() => {
  window.localStorage.clear()
})

const DEFAUT = { largeur: 360, hauteur: 460 }
const MIN = { largeur: 280, hauteur: 280 }
const MAX = { largeur: 720, hauteur: 820 }

describe('useFenetreFlottante', () => {
  it('part de la taille par defaut sans memoire enregistree', () => {
    const { result } = renderHook(() => useFenetreFlottante('cle-test-1', DEFAUT, MIN, MAX))
    expect(result.current.taille).toEqual(DEFAUT)
  })

  it('relit une taille deja enregistree, bornee', () => {
    window.localStorage.setItem('cle-test-2', JSON.stringify({ largeur: 900, hauteur: 100 }))
    const { result } = renderHook(() => useFenetreFlottante('cle-test-2', DEFAUT, MIN, MAX))
    expect(result.current.taille).toEqual({ largeur: MAX.largeur, hauteur: MIN.hauteur })
  })

  it('une valeur abimee dans le stockage retombe sur le defaut', () => {
    window.localStorage.setItem('cle-test-3', 'pas du json valide')
    const { result } = renderHook(() => useFenetreFlottante('cle-test-3', DEFAUT, MIN, MAX))
    expect(result.current.taille).toEqual(DEFAUT)
  })

  it('persiste la taille courante dans localStorage', () => {
    renderHook(() => useFenetreFlottante('cle-test-4', DEFAUT, MIN, MAX))
    expect(JSON.parse(window.localStorage.getItem('cle-test-4') ?? 'null')).toEqual(DEFAUT)
  })

  it('un glisser de la poignee change la taille, bornee', () => {
    const { result } = renderHook(() => useFenetreFlottante('cle-test-5', DEFAUT, MIN, MAX))
    const element = { setPointerCapture: () => {}, releasePointerCapture: () => {} }
    act(() => {
      result.current.poignee.onPointerDown({
        pointerType: 'mouse',
        button: 0,
        clientX: 100,
        clientY: 100,
        pointerId: 1,
        currentTarget: element,
      } as never)
    })
    act(() => {
      result.current.poignee.onPointerMove({ clientX: 150, clientY: 140 } as never)
    })
    expect(result.current.taille).toEqual({ largeur: DEFAUT.largeur + 50, hauteur: DEFAUT.hauteur + 40 })
  })
})
