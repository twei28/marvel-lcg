// L'assemblee tenue a jour : relue toutes les quelques secondes, preferee au dernier rendu, rien hors assemblee.
import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { AssembleeExport, World } from './world'

const chargerAssemblee = vi.fn()
vi.mock('./sources', () => ({ chargerAssemblee: (...a: unknown[]) => chargerAssemblee(...a) }))
import { PERIODE_ASSEMBLEE_MS, useAssembleeEnDirect } from './use-assemblee-en-direct'

const etat = (plus: Partial<AssembleeExport> = {}): AssembleeExport => ({
  code: 'KING-7F3A', table: 'p1', organisateur: 'p1', total_jetons: 1, seuil: 4, retournee: false, degats: 0, menace: 0, joueurs: 1,
  groupes: [{ tab: 'p1', joueurs: 1, noms: 'Spider-Man', etat: 0, recus: 0 }], terminee: false, gagnee: false, ...plus,
})
const monde = (a: Partial<AssembleeExport> | undefined) => ({ assemblee: a ?? {} }) as unknown as World

beforeEach(() => {
  vi.useFakeTimers()
  chargerAssemblee.mockReset()
})
afterEach(() => vi.useRealTimers())

describe('useAssembleeEnDirect', () => {
  it("hors assemblee : rien, et le serveur n'est jamais interroge", () => {
    const { result } = renderHook(() => useAssembleeEnDirect(monde(undefined), 0))
    expect(result.current).toBeUndefined()
    act(() => { vi.advanceTimersByTime(PERIODE_ASSEMBLEE_MS * 3) })
    expect(chargerAssemblee).not.toHaveBeenCalled()
  })
  it("en assemblee : montre d'abord le rendu, puis l'etat relu (un autre groupe a rejoint)", async () => {
    chargerAssemblee.mockResolvedValue(etat({ seuil: 8, joueurs: 2, groupes: [...etat().groupes, { tab: 'p2', joueurs: 1, noms: 'Thor', etat: 0, recus: 0 }] }))
    const { result } = renderHook(() => useAssembleeEnDirect(monde(etat()), 0))
    expect(result.current?.groupes).toHaveLength(1)
    await act(async () => { await Promise.resolve() })
    expect(result.current?.groupes).toHaveLength(2)
    expect(result.current?.seuil).toBe(8)
  })
  it('relit a chaque periode', async () => {
    chargerAssemblee.mockResolvedValue(etat())
    renderHook(() => useAssembleeEnDirect(monde(etat()), 0))
    await act(async () => { await Promise.resolve() })
    expect(chargerAssemblee).toHaveBeenCalledTimes(1)
    await act(async () => { vi.advanceTimersByTime(PERIODE_ASSEMBLEE_MS); await Promise.resolve() })
    expect(chargerAssemblee).toHaveBeenCalledTimes(2)
  })
  it("une erreur du serveur garde le dernier etat connu, un autre code est ignore", async () => {
    chargerAssemblee.mockRejectedValueOnce(new Error('503'))
    const { result } = renderHook(() => useAssembleeEnDirect(monde(etat({ degats: 3 })), 0))
    await act(async () => { await Promise.resolve() })
    expect(result.current?.degats).toBe(3)
    chargerAssemblee.mockResolvedValueOnce(etat({ code: 'KING-AUTRE', degats: 9 }))
    await act(async () => { vi.advanceTimersByTime(PERIODE_ASSEMBLEE_MS); await Promise.resolve() })
    expect(result.current?.degats).toBe(3)
  })
})
