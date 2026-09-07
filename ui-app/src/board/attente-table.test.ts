// QUI L'ON ATTEND quand le plateau ne bouge plus.
//
// Constat F5 de l'audit du 06/09/2026 : « La suite arrive… » disait la meme
// chose que le moteur soit occupe ou qu'un coequipier soit parti chercher un
// cafe. Le moteur attend l'accuse de CHAQUE client (WaitSync), et rien ne le
// disait a l'ecran.
import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest'
import { act, renderHook } from '@testing-library/react'
import {
  DELAI_SILENCE_TABLE_MS,
  joueurAttendu,
  useTableSilencieuse,
} from './attente-table'

describe('le joueur que le moteur interroge', () => {
  const base = {
    playerId: 0,
    multijoueur: true,
    nomsHerosParJoueur: ['Colossus', 'Spider-Man'],
  }

  it('nomme le joueur interroge quand ce n est pas nous', () => {
    expect(joueurAttendu({ ...base, joueurDemande: 1 })).toEqual({
      numero: 2,
      nom: 'Spider-Man',
    })
  })

  it('ne nomme personne quand c est nous que le moteur interroge', () => {
    expect(joueurAttendu({ ...base, joueurDemande: 0 })).toBeUndefined()
  })

  it('ne nomme personne quand le moteur n interroge personne', () => {
    expect(joueurAttendu({ ...base, joueurDemande: undefined })).toBeUndefined()
  })

  // HOT-SEAT : tous les sieges sont tenus par CE navigateur, qui repond pour
  // chacun d'eux (voir adresseSocket dans moteur.ts). Le moteur n'attend donc
  // jamais quelqu'un d'autre, et annoncer « En attente de Spider-Man » a un
  // joueur qui joue Spider-Man lui-meme serait un contresens.
  it('ne nomme personne en hot-seat, ou l on repond pour tout le monde', () => {
    expect(joueurAttendu({ ...base, multijoueur: false, joueurDemande: 1 })).toBeUndefined()
  })

  // Le nom vient du monde ; il peut manquer (siege vide, monde pas encore lu).
  // On rend alors le numero seul, et l'affichage retombe sur « un autre
  // joueur » plutot que d'inventer un nom.
  it('rend le siege sans nom quand le monde n en donne pas', () => {
    expect(joueurAttendu({ ...base, nomsHerosParJoueur: [], joueurDemande: 1 })).toEqual({
      numero: 2,
      nom: undefined,
    })
  })
})

describe('le silence de la table', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })
  afterEach(() => {
    vi.useRealTimers()
  })

  it('ne dit rien tant que le delai n est pas ecoule', () => {
    const { result } = renderHook(() => useTableSilencieuse(12, true))
    expect(result.current).toBe(false)
    act(() => {
      vi.advanceTimersByTime(DELAI_SILENCE_TABLE_MS - 1)
    })
    expect(result.current).toBe(false)
  })

  it('signale le silence quand plus aucune trame n arrive', () => {
    const { result } = renderHook(() => useTableSilencieuse(12, true))
    act(() => {
      vi.advanceTimersByTime(DELAI_SILENCE_TABLE_MS)
    })
    expect(result.current).toBe(true)
  })

  it('se tait des qu une trame arrive', () => {
    const { result, rerender } = renderHook(
      ({ trame }: { trame: number }) => useTableSilencieuse(trame, true),
      { initialProps: { trame: 12 } }
    )
    act(() => {
      vi.advanceTimersByTime(DELAI_SILENCE_TABLE_MS)
    })
    expect(result.current).toBe(true)
    rerender({ trame: 13 })
    expect(result.current).toBe(false)
  })

  it('ne guette rien quand la table n a aucune raison d attendre', () => {
    const { result } = renderHook(() => useTableSilencieuse(12, false))
    act(() => {
      vi.advanceTimersByTime(DELAI_SILENCE_TABLE_MS * 4)
    })
    expect(result.current).toBe(false)
  })
})
