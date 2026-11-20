import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import { estRestauration, useRestauration } from './annulation'
import type { World } from './world'

const monde = (restaurations?: number, depuis?: number): World => ({ render_id: 10, restaurations, restaure_depuis_render_id: depuis }) as unknown as World

describe('estRestauration', () => {
  it('vrai seulement quand le compteur MONTE', () => {
    expect(estRestauration(1, 0)).toBe(true)
    expect(estRestauration(3, 2)).toBe(true)
    expect(estRestauration(2, 2)).toBe(false)
  })
  it('jamais au premier rendu (chargement, reconnexion), meme avec un compteur non nul', () => {
    expect(estRestauration(5, undefined)).toBe(false)
    expect(estRestauration(undefined, 1)).toBe(false)
  })
})

afterEach(() => vi.useRealTimers())

describe('useRestauration', () => {
  it('ne signale que le rendu qui voit monter le compteur, puis se tait', () => {
    const { result, rerender } = renderHook(({ m }) => useRestauration(m), { initialProps: { m: monde(0) } })
    expect(result.current.restauree).toBe(false)
    rerender({ m: monde(1, 7) })
    expect(result.current.restauree).toBe(true)
    expect(result.current.depuisRenderId).toBe(7)
    expect(result.current.episode).toBe(1)
    // Quelques instants plus tard, un rendu ordinaire n'est plus une annulation.
    vi.useFakeTimers({ now: Date.now() + 3000 })
    rerender({ m: monde(1, 7) })
    expect(result.current.restauree).toBe(false)
  })
  it('le REJEU (render_id qui recule, compteur a zero) est aussi un retour en arriere', () => {
    const { result, rerender } = renderHook(({ m }) => useRestauration(m), { initialProps: { m: { render_id: 50, restaurations: 0 } as unknown as World } })
    rerender({ m: { render_id: 44, restaurations: 0 } as unknown as World })
    expect(result.current.restauree).toBe(true)
    expect(result.current.depuisRenderId).toBe(44)
    // Un rejeu envoie plusieurs rendus d'affilee : ceux qui suivent de pres sont encore le retour en arriere (meme episode, meme point de reprise).
    rerender({ m: { render_id: 45, restaurations: 0 } as unknown as World })
    expect(result.current.restauree).toBe(true)
    expect(result.current.episode).toBe(1)
    expect(result.current.depuisRenderId).toBe(44)
    vi.useFakeTimers({ now: Date.now() + 3000 })
    rerender({ m: { render_id: 46, restaurations: 0 } as unknown as World })
    expect(result.current.restauree).toBe(false)
  })
  it('« ignorer » (relecture, saut) ne declenche rien, meme si le render_id recule', () => {
    const { result, rerender } = renderHook(({ m, i }) => useRestauration(m, i), { initialProps: { m: { render_id: 50 } as unknown as World, i: true } })
    rerender({ m: { render_id: 10 } as unknown as World, i: true })
    expect(result.current.restauree).toBe(false)
  })
  it('un chargement de page avec un compteur deja non nul n’est pas une annulation', () => {
    const { result } = renderHook(({ m }) => useRestauration(m), { initialProps: { m: monde(4, 9) } })
    expect(result.current.restauree).toBe(false)
  })
  it('un moteur sans le champ ne declenche jamais rien', () => {
    const { result, rerender } = renderHook(({ m }) => useRestauration(m), { initialProps: { m: monde(undefined) } })
    rerender({ m: monde(undefined) })
    expect(result.current.restauree).toBe(false)
  })
})
