import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { renderHook } from '@testing-library/react'
import {
  CADENCE_RETOUR_MS,
  adresseApresPartie,
  estInviteDeTable,
  hoteEnPreparation,
  useRetourAuSalon,
} from './retour-salon'

const atterrissages: string[] = []
vi.mock('./quitter-la-table', async (original) => ({
  ...(await original<typeof import('./quitter-la-table')>()),
  atterrir: (url: string) => {
    atterrissages.push(url)
  },
}))

describe('retour au salon en fin de partie', () => {
  it('seul un invité d’une table répartie retourne à son salon', () => {
    expect(adresseApresPartie({ siege: 2, multi: true, spectateur: false })).toBe('/salon.html?p=2')
    // L'hôte, le solo et le spectateur gardent l'assistant.
    expect(adresseApresPartie({ siege: 0, multi: true, spectateur: false })).toBe('/prepare.html')
    expect(adresseApresPartie({ siege: 1, multi: false, spectateur: false })).toBe('/prepare.html')
    expect(estInviteDeTable({ siege: 1, multi: true, spectateur: true })).toBe(false)
  })

  it('seul un CHANGEMENT du compteur dit que l’hôte prépare ; une lecture manquée ne conclut rien', () => {
    expect(hoteEnPreparation(3, 3)).toBe(false)
    expect(hoteEnPreparation(3, 4)).toBe(true)
    expect(hoteEnPreparation(undefined, 4)).toBe(false)
    expect(hoteEnPreparation(3, undefined)).toBe(false)
  })
})

describe('useRetourAuSalon', () => {
  let compteur = 0
  beforeEach(() => {
    vi.useFakeTimers()
    atterrissages.length = 0
    compteur = 5
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => ({ ok: true, json: async () => ({ n: compteur }) }))
    )
  })
  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
  })

  it('ramène l’invité au salon dès que l’hôte rouvre la préparation, pas avant', async () => {
    renderHook(() => useRetourAuSalon(true, 2))
    await vi.advanceTimersByTimeAsync(CADENCE_RETOUR_MS * 2)
    expect(atterrissages).toEqual([])
    compteur = 6
    await vi.advanceTimersByTimeAsync(CADENCE_RETOUR_MS)
    expect(atterrissages).toEqual(['/salon.html?p=2'])
  })

  it('ne sonde rien hors de l’écran de fin', async () => {
    renderHook(() => useRetourAuSalon(false, 2))
    await vi.advanceTimersByTimeAsync(CADENCE_RETOUR_MS * 3)
    expect(fetch).not.toHaveBeenCalled()
  })
})
