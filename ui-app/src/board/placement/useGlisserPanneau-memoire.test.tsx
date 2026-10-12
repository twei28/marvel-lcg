// La place de la boite de la phase du mechant est retenue (decision 28 du
// 12/10/2026) ; sans `memoire`, rien ne change (remise a zero par signature).
import { afterEach, describe, expect, it } from 'vitest'
import { act, renderHook } from '@testing-library/react'
import { useGlisserPanneau } from './useGlisserPanneau'

const CLE = 'test-boite'

afterEach(() => window.localStorage.clear())

function glisser(gestes: ReturnType<typeof useGlisserPanneau>['gestes'], dx: number, dy: number) {
  const element = document.createElement('div')
  act(() => {
    gestes.onPointerDown({ pointerType: 'mouse', button: 0, clientX: 0, clientY: 0, pointerId: 1, currentTarget: element } as never)
  })
  act(() => {
    window.dispatchEvent(Object.assign(new Event('pointermove'), { clientX: dx, clientY: dy }))
  })
  act(() => {
    window.dispatchEvent(new Event('pointerup'))
  })
}

describe('useGlisserPanneau avec memoire', () => {
  it('retient la place choisie et la relit au montage suivant', () => {
    const premier = renderHook(() => useGlisserPanneau('scene-essai', CLE))
    glisser(premier.result.current.gestes, 40, 25)
    expect(premier.result.current.decalage).toEqual({ dx: 40, dy: 25 })
    premier.unmount()
    const second = renderHook(() => useGlisserPanneau('scene-essai', CLE))
    expect(second.result.current.decalage).toEqual({ dx: 40, dy: 25 })
  })

  it('une nouvelle signature ne remet pas a zero une place retenue', () => {
    const { result, rerender } = renderHook(({ s }) => useGlisserPanneau(s, CLE), { initialProps: { s: 'a' } })
    glisser(result.current.gestes, 10, 10)
    rerender({ s: 'b' })
    expect(result.current.decalage).toEqual({ dx: 10, dy: 10 })
  })

  it('sans memoire : remise a zero a chaque signature, rien en stockage', () => {
    const { result, rerender } = renderHook(({ s }) => useGlisserPanneau(s), { initialProps: { s: 'a' } })
    glisser(result.current.gestes, 10, 10)
    rerender({ s: 'b' })
    expect(result.current.decalage).toEqual({ dx: 0, dy: 0 })
    expect(window.localStorage.length).toBe(0)
  })
})
