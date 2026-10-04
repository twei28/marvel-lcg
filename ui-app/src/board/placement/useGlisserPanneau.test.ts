// useGlisserPanneau.test.ts — deplacer un panneau de decision a la poignee.
//
// Demande de l'utilisateur (28/09/2026) : deux panneaux de decision qui
// s'empilent, aucun moyen d'ecarter celui du dessus. Ce hook ajoute un
// decalage manuel par-dessus le placement automatique, remis a zero des
// qu'une nouvelle decision arrive.
import { describe, expect, it } from 'vitest'
import { act, renderHook } from '@testing-library/react'
import { styleAvecDecalage, transformDecalage, useGlisserPanneau } from './useGlisserPanneau'

/** Un PointerEvent React minimal, juste ce que le hook lit. */
function evenement(x: number, y: number, extra: Partial<Record<string, unknown>> = {}) {
  return {
    clientX: x,
    clientY: y,
    pointerId: 1,
    pointerType: 'mouse',
    button: 0,
    currentTarget: {
      setPointerCapture: () => {},
      releasePointerCapture: () => {},
    },
    ...extra,
  } as unknown as Parameters<ReturnType<typeof useGlisserPanneau>['gestes']['onPointerDown']>[0]
}

describe('useGlisserPanneau', () => {
  it('ne bouge pas tant que le seuil de glisser n est pas franchi', () => {
    const { result } = renderHook(() => useGlisserPanneau('decision-1'))
    act(() => result.current.gestes.onPointerDown(evenement(100, 100)))
    act(() => result.current.gestes.onPointerMove(evenement(102, 101)))
    expect(result.current.decalage).toEqual({ dx: 0, dy: 0 })
    expect(result.current.aBouge).toBe(false)
  })

  it('suit le pointeur une fois le seuil franchi', () => {
    const { result } = renderHook(() => useGlisserPanneau('decision-1'))
    act(() => result.current.gestes.onPointerDown(evenement(100, 100)))
    act(() => result.current.gestes.onPointerMove(evenement(140, 70)))
    expect(result.current.decalage).toEqual({ dx: 40, dy: -30 })
    expect(result.current.aBouge).toBe(true)
  })

  it('cumule plusieurs glissers successifs', () => {
    const { result } = renderHook(() => useGlisserPanneau('decision-1'))
    act(() => result.current.gestes.onPointerDown(evenement(100, 100)))
    act(() => result.current.gestes.onPointerMove(evenement(140, 100)))
    act(() => result.current.gestes.onPointerUp(evenement(140, 100)))
    act(() => result.current.gestes.onPointerDown(evenement(140, 100)))
    act(() => result.current.gestes.onPointerMove(evenement(150, 130)))
    expect(result.current.decalage).toEqual({ dx: 50, dy: 30 })
  })

  it('se remet a zero quand la signature change (nouvelle decision)', () => {
    const { result, rerender } = renderHook(({ signature }) => useGlisserPanneau(signature), {
      initialProps: { signature: 'decision-1' },
    })
    act(() => result.current.gestes.onPointerDown(evenement(100, 100)))
    act(() => result.current.gestes.onPointerMove(evenement(140, 130)))
    expect(result.current.aBouge).toBe(true)

    rerender({ signature: 'decision-2' })
    expect(result.current.decalage).toEqual({ dx: 0, dy: 0 })
    expect(result.current.aBouge).toBe(false)
  })

  it('un clic droit ne declenche rien', () => {
    const { result } = renderHook(() => useGlisserPanneau('decision-1'))
    act(() => result.current.gestes.onPointerDown(evenement(100, 100, { button: 2 })))
    act(() => result.current.gestes.onPointerMove(evenement(140, 130)))
    expect(result.current.decalage).toEqual({ dx: 0, dy: 0 })
  })
})

// Signalement Yarro (28/09/2026) : « toutes les fenetres, tous les panneaux »
// -- une vingtaine de composants reutilisent ces deux fonctions plutot que de
// recopier le calcul. Verrouille leur comportement independamment de tout
// composant particulier.
describe('styleAvecDecalage', () => {
  it('ne touche pas le style tant que rien n a bouge', () => {
    const style = { left: '10px', top: '20px' }
    expect(styleAvecDecalage(style, { dx: 0, dy: 0 })).toBe(style)
  })

  it('ajoute le decalage en calc(), sans perdre le reste du style', () => {
    const style = { left: '10px', top: '20px', width: '400px' }
    expect(styleAvecDecalage(style, { dx: 15, dy: -8 })).toEqual({
      left: 'calc(10px + 15px)',
      top: 'calc(20px + -8px)',
      width: '400px',
    })
  })

  it('laisse left/top absents tels quels (usePlacement pas encore mesure)', () => {
    const style = { opacity: 0 }
    expect(styleAvecDecalage(style, { dx: 15, dy: -8 })).toEqual({ opacity: 0 })
  })
})

describe('transformDecalage', () => {
  it('ne pose rien tant que rien n a bouge', () => {
    expect(transformDecalage({ dx: 0, dy: 0 })).toBeUndefined()
  })

  it('pose un translate() une fois deplace', () => {
    expect(transformDecalage({ dx: 12, dy: -4 })).toEqual({ transform: 'translate(12px, -4px)' })
  })
})
