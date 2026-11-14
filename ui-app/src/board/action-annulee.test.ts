import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useActionAnnulee } from './action-annulee'

// Rapport du 26/10/2026 : fermer ou abandonner une action avant de l'avoir validee ne disait RIEN (la carte se redressait,
// aucun effet, aucun message). Une action abandonnee cote client, sans reponse envoyee au moteur, le dit maintenant.
type P = { option: string | undefined; demande: object }

describe('useActionAnnulee', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())

  const demandeA = { id: 'a' }
  const demandeB = { id: 'b' }

  it('dit « Action annulee » quand l’action s’eteint sans reponse, sur la meme demande', () => {
    const { result, rerender } = renderHook((p: P) => useActionAnnulee(p.option, p.demande), {
      initialProps: { option: 'Action d’alter ego', demande: demandeA } as P,
    })
    expect(result.current.message).toBeUndefined()
    rerender({ option: undefined, demande: demandeA })
    expect(result.current.message).toBe('Action annulée : Action d’alter ego')
  })

  it('se tait quand une reponse est partie (validation)', () => {
    const { result, rerender } = renderHook((p: P) => useActionAnnulee(p.option, p.demande), {
      initialProps: { option: 'Action d’alter ego', demande: demandeA } as P,
    })
    act(() => result.current.noterReponse())
    rerender({ option: undefined, demande: demandeB })
    expect(result.current.message).toBeUndefined()
  })

  it('se tait quand le moteur pose une autre demande', () => {
    const { result, rerender } = renderHook((p: P) => useActionAnnulee(p.option, p.demande), {
      initialProps: { option: 'Action d’alter ego', demande: demandeA } as P,
    })
    rerender({ option: undefined, demande: demandeB })
    expect(result.current.message).toBeUndefined()
  })

  it('le message disparait tout seul', () => {
    const { result, rerender } = renderHook((p: P) => useActionAnnulee(p.option, p.demande), {
      initialProps: { option: 'Attaquer', demande: demandeA } as P,
    })
    rerender({ option: undefined, demande: demandeA })
    expect(result.current.message).toBe('Action annulée : Attaquer')
    act(() => {
      vi.advanceTimersByTime(4000)
    })
    expect(result.current.message).toBeUndefined()
  })
})
