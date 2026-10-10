import { act, fireEvent, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { World } from '../world'
import { EVENEMENT_REPONSE_ENVOYEE } from '../moteur'
import { ecrireReglageTelephone } from './reglages-telephone'
import {
  MOTIFS,
  estMonTour,
  oublierGeste,
  pvDuHeros,
  useEcranAllume,
  useVerrouPortrait,
  useVibrationsDePartie,
  vibrer,
} from './telephone'

const monde = (phase: string, pv: number): World =>
  ({ render_id: 1, round_id: 1, phase, players: [{ area_hero: [{ info: { health: pv } }] }] }) as unknown as World

let vibrate: ReturnType<typeof vi.fn>

beforeEach(() => {
  window.localStorage.clear()
  vibrate = vi.fn(() => true)
  Object.defineProperty(navigator, 'vibrate', { value: vibrate, configurable: true })
  oublierGeste()
})

describe('vibrer', () => {
  it('vibre selon le motif du moment', () => {
    expect(vibrer('tour')).toBe(true)
    expect(vibrate).toHaveBeenCalledWith(MOTIFS.tour)
  })

  it('se tait quand l interrupteur des reglages est coupe', () => {
    ecrireReglageTelephone('vibrations', false)
    expect(vibrer('attaque')).toBe(false)
    expect(vibrate).not.toHaveBeenCalled()
  })
})

describe('les moments de la partie', () => {
  it('lit le tour et les PV du siege (Player N Turn, N a partir de 1)', () => {
    expect(estMonTour(monde('Player 1 Turn', 10), 0)).toBe(true)
    expect(estMonTour(monde('Player 2 Turn', 10), 0)).toBe(false)
    expect(pvDuHeros(monde('Player 1 Turn', 7), 0)).toBe(7)
    expect(pvDuHeros(undefined, 0)).toBeUndefined()
  })

  it('le premier etat ne vibre pas ; ton tour, puis une attaque subie, vibrent', () => {
    const { rerender } = renderHook(({ m }) => useVibrationsDePartie(m, 0, true), {
      initialProps: { m: monde('Player 1 Turn', 10) },
    })
    expect(vibrate).not.toHaveBeenCalled()
    rerender({ m: monde('Villain Phase', 10) })
    expect(vibrate).not.toHaveBeenCalled()
    rerender({ m: monde('Villain Phase', 7) })
    expect(vibrate).toHaveBeenLastCalledWith(MOTIFS.attaque)
    rerender({ m: monde('Player 1 Turn', 7) })
    expect(vibrate).toHaveBeenLastCalledWith(MOTIFS.tour)
    // Des PV qui remontent (soin) ne vibrent pas.
    vibrate.mockClear()
    rerender({ m: monde('Player 1 Turn', 9) })
    expect(vibrate).not.toHaveBeenCalled()
  })

  it('une reponse envoyee apres un geste vibre (validation) ; sans geste, non', () => {
    renderHook(() => useVibrationsDePartie(monde('Player 1 Turn', 10), 0, true))
    act(() => {
      window.dispatchEvent(new CustomEvent(EVENEMENT_REPONSE_ENVOYEE))
    })
    expect(vibrate).not.toHaveBeenCalled()
    fireEvent.pointerDown(document.body)
    act(() => {
      window.dispatchEvent(new CustomEvent(EVENEMENT_REPONSE_ENVOYEE))
    })
    expect(vibrate).toHaveBeenCalledWith(MOTIFS.validation)
  })

  it('inactif (PC, spectateur) : rien ne vibre', () => {
    const { rerender } = renderHook(({ m }) => useVibrationsDePartie(m, 0, false), {
      initialProps: { m: monde('Villain Phase', 10) },
    })
    rerender({ m: monde('Player 1 Turn', 4) })
    expect(vibrate).not.toHaveBeenCalled()
  })
})

describe('useEcranAllume', () => {
  afterEach(() => {
    Object.defineProperty(navigator, 'wakeLock', { value: undefined, configurable: true })
  })

  it('demande le verrou d ecran, le relache au demontage', async () => {
    const release = vi.fn(() => Promise.resolve())
    const request = vi.fn(() => Promise.resolve({ release }))
    Object.defineProperty(navigator, 'wakeLock', { value: { request }, configurable: true })
    const { unmount } = renderHook(() => useEcranAllume(true))
    await act(async () => {})
    expect(request).toHaveBeenCalledWith('screen')
    unmount()
    expect(release).toHaveBeenCalledTimes(1)
  })

  it('inactif ou sans API : ne demande rien, ne leve pas', () => {
    const request = vi.fn(() => Promise.resolve({ release: () => Promise.resolve() }))
    Object.defineProperty(navigator, 'wakeLock', { value: { request }, configurable: true })
    renderHook(() => useEcranAllume(false))
    expect(request).not.toHaveBeenCalled()
    Object.defineProperty(navigator, 'wakeLock', { value: undefined, configurable: true })
    expect(() => renderHook(() => useEcranAllume(true))).not.toThrow()
  })
})

describe('useVerrouPortrait', () => {
  const orientation = (couche: boolean) =>
    vi.spyOn(window, 'matchMedia').mockImplementation(
      (requete: string) =>
        ({
          matches: requete.includes('landscape') ? couche : false,
          media: requete,
          addEventListener: () => {},
          removeEventListener: () => {},
        }) as unknown as MediaQueryList
    )
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('telephone couche et verrou actif : on demande de le remettre droit', () => {
    orientation(true)
    expect(renderHook(() => useVerrouPortrait(true, true)).result.current.tourner).toBe(true)
  })

  it('verrou coupe, ou telephone debout, ou PC : rien', () => {
    orientation(true)
    expect(renderHook(() => useVerrouPortrait(true, false)).result.current.tourner).toBe(false)
    expect(renderHook(() => useVerrouPortrait(false, true)).result.current.tourner).toBe(false)
    vi.restoreAllMocks()
    orientation(false)
    expect(renderHook(() => useVerrouPortrait(true, true)).result.current.tourner).toBe(false)
  })
})
