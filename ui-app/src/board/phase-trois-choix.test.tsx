// Les TROIS choix de la phase du méchant (19/10/2026) : « Étape par étape bis », « Sur la table », « D'un coup ».
// « Étape par étape » (ancien cartouche) et « Phase dynamique » sont cachés, pas supprimés ; « bis » est
// ouvert à tous (sans l'essai de /admin) et devient le départ.
import { render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ContenuOnglet, type ProprietesReglages } from './FenetreReglages'
import {
  CLE_MIGRATION_PHASE,
  CLE_PRESENTATION_PHASE,
  PHASE_BIS_POUR_TOUS,
  PHASE_DYNAMIQUE_VISIBLE,
  PHASE_ETAPE_VISIBLE,
  VERSION_MIGRATION_PHASE,
  lirePresentationPhase,
  migrerPhaseTroisChoix,
} from './phase-presentation'

function stockageFaux(depart: Record<string, string> = {}) {
  const m = new Map(Object.entries(depart))
  return {
    getItem: (k: string) => (m.has(k) ? (m.get(k) as string) : null),
    setItem: (k: string, v: string) => void m.set(k, v),
    lu: (k: string) => m.get(k) ?? null,
  }
}

describe('migration unique vers « bis »', () => {
  it('l’ancien « Étape par étape » passe sur bis, une seule fois', () => {
    const s = stockageFaux({ [CLE_PRESENTATION_PHASE]: 'etape' })
    expect(migrerPhaseTroisChoix(s)).toBe(true)
    expect(s.lu(CLE_PRESENTATION_PHASE)).toBe('bis')
    expect(s.lu(CLE_MIGRATION_PHASE)).toBe(VERSION_MIGRATION_PHASE)
    // un choix fait ensuite n'est plus retouché
    s.setItem(CLE_PRESENTATION_PHASE, 'etape')
    expect(migrerPhaseTroisChoix(s)).toBe(false)
    expect(s.lu(CLE_PRESENTATION_PHASE)).toBe('etape')
  })
  it('« Phase dynamique » et l’ancien mc_phase_bis=non passent aussi sur bis', () => {
    const a = stockageFaux({ [CLE_PRESENTATION_PHASE]: 'dynamique' })
    migrerPhaseTroisChoix(a)
    expect(a.lu(CLE_PRESENTATION_PHASE)).toBe('bis')
    const b = stockageFaux({ mc_phase_bis: 'non' })
    migrerPhaseTroisChoix(b)
    expect(b.lu(CLE_PRESENTATION_PHASE)).toBe('bis')
  })
  it('les modes « Sur la table » et « D’un coup » sont conservés', () => {
    const s = stockageFaux({ 'marvel-board-mode-phase-mechant': 'sur-table', [CLE_PRESENTATION_PHASE]: 'etape' })
    migrerPhaseTroisChoix(s)
    expect(s.lu('marvel-board-mode-phase-mechant')).toBe('sur-table')
    const t = stockageFaux({ 'marvel-board-mode-phase-mechant': 'instantane' })
    migrerPhaseTroisChoix(t)
    expect(t.lu('marvel-board-mode-phase-mechant')).toBe('instantane')
  })
  it('un stockage absent ou refusé ne casse rien', () => {
    expect(migrerPhaseTroisChoix(null)).toBe(false)
    expect(
      migrerPhaseTroisChoix({
        getItem: () => {
          throw new Error('non')
        },
        setItem: () => {},
      })
    ).toBe(false)
  })
})

describe('défaut et repli', () => {
  beforeEach(() => {
    window.localStorage.clear()
  })
  it('un nouveau navigateur est sur bis', () => {
    expect(lirePresentationPhase()).toBe('bis')
  })
  it('un choix caché (etape, dynamique, ancien « non ») se lit bis', () => {
    expect(PHASE_ETAPE_VISIBLE).toBe(false)
    expect(PHASE_DYNAMIQUE_VISIBLE).toBe(false)
    window.localStorage.setItem(CLE_PRESENTATION_PHASE, 'etape')
    expect(lirePresentationPhase()).toBe('bis')
    window.localStorage.setItem(CLE_PRESENTATION_PHASE, 'dynamique')
    expect(lirePresentationPhase()).toBe('bis')
    window.localStorage.removeItem(CLE_PRESENTATION_PHASE)
    window.localStorage.setItem('mc_phase_bis', 'non')
    expect(lirePresentationPhase()).toBe('bis')
  })
})

describe('les réglages', () => {
  const p = (sur: Partial<ProprietesReglages> = {}) =>
    ({
      modePhase: 'detaille',
      changerModePhase: vi.fn(),
      libelleModePhase: (m: string) => (m === 'sur-table' ? 'Sur la table' : m),
      ...sur,
    }) as unknown as ProprietesReglages
  const choix = () =>
    within(screen.getByText('Phase du méchant').closest('.ligne-option') as HTMLElement)
      .getAllByRole('button')
      .map((b) => b.textContent)
  it('exactement trois choix, bis visible sans l’essai de compte', () => {
    expect(PHASE_BIS_POUR_TOUS).toBe(true)
    // pas de serveur d'essais ici : fetch échoue, l'essai vaut faux
    vi.stubGlobal(
      'fetch',
      vi.fn(() => Promise.reject(new Error('hors ligne')))
    )
    render(<ContenuOnglet onglet="jeu" p={p()} />)
    expect(choix()).toEqual(['Étape par étape bis', 'Sur la table', 'D’un coup'])
    vi.unstubAllGlobals()
  })
})
