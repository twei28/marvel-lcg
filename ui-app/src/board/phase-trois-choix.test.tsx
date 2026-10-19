// Les TROIS choix de la phase du méchant (19/10/2026) : « Guidée » (`tris`), « Plateau animé », « Accéléré ».
// « Étape par étape », « bis » et « Phase dynamique » sont cachés, pas supprimés ; « tris » est
// ouvert à tous (hôte non local compris) et devient le départ.
import { render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ContenuOnglet, type ProprietesReglages } from './FenetreReglages'
import {
  CLE_MIGRATION_PHASE,
  CLE_PRESENTATION_PHASE,
  PHASE_BIS_POUR_TOUS,
  PHASE_BIS_VISIBLE,
  PHASE_TRIS_POUR_TOUS,
  PRESENTATION_PAR_DEFAUT,
  phaseTrisUtilisable,
  presentationProposee,
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

describe('migration unique vers « Guidée » (tris)', () => {
  it('l’ancien « Étape par étape » passe sur tris, une seule fois', () => {
    const s = stockageFaux({ [CLE_PRESENTATION_PHASE]: 'etape' })
    expect(migrerPhaseTroisChoix(s)).toBe(true)
    expect(s.lu(CLE_PRESENTATION_PHASE)).toBe('tris')
    expect(s.lu(CLE_MIGRATION_PHASE)).toBe(VERSION_MIGRATION_PHASE)
    expect(VERSION_MIGRATION_PHASE).toBe('2026-10-19b')
    // un choix fait ensuite n'est plus retouché
    s.setItem(CLE_PRESENTATION_PHASE, 'etape')
    expect(migrerPhaseTroisChoix(s)).toBe(false)
    expect(s.lu(CLE_PRESENTATION_PHASE)).toBe('etape')
  })
  it('bis (déjà migré par erreur à la version précédente) repasse sur tris', () => {
    const s = stockageFaux({ [CLE_PRESENTATION_PHASE]: 'bis', [CLE_MIGRATION_PHASE]: '2026-10-19' })
    expect(migrerPhaseTroisChoix(s)).toBe(true)
    expect(s.lu(CLE_PRESENTATION_PHASE)).toBe('tris')
    const n = stockageFaux({ [CLE_PRESENTATION_PHASE]: 'bis' })
    migrerPhaseTroisChoix(n)
    expect(n.lu(CLE_PRESENTATION_PHASE)).toBe('tris')
  })
  it('« Phase dynamique » et l’ancien mc_phase_bis=non passent aussi sur tris', () => {
    const a = stockageFaux({ [CLE_PRESENTATION_PHASE]: 'dynamique' })
    migrerPhaseTroisChoix(a)
    expect(a.lu(CLE_PRESENTATION_PHASE)).toBe('tris')
    const b = stockageFaux({ mc_phase_bis: 'non' })
    migrerPhaseTroisChoix(b)
    expect(b.lu(CLE_PRESENTATION_PHASE)).toBe('tris')
  })
  it('les modes « Plateau animé » et « Accéléré » sont conservés', () => {
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
  it('un nouveau navigateur est sur tris', () => {
    expect(PRESENTATION_PAR_DEFAUT).toBe('tris')
    expect(lirePresentationPhase()).toBe('tris')
  })
  it('un choix caché (etape, bis, dynamique, ancien « non ») se lit tris', () => {
    expect(PHASE_ETAPE_VISIBLE).toBe(false)
    expect(PHASE_BIS_VISIBLE).toBe(false)
    expect(PHASE_DYNAMIQUE_VISIBLE).toBe(false)
    for (const caché of ['etape', 'bis', 'dynamique']) {
      window.localStorage.setItem(CLE_PRESENTATION_PHASE, caché)
      expect(lirePresentationPhase()).toBe('tris')
    }
    window.localStorage.removeItem(CLE_PRESENTATION_PHASE)
    window.localStorage.setItem('mc_phase_bis', 'non')
    expect(lirePresentationPhase()).toBe('tris')
  })
  it('tris est utilisable sur un hôte non local', () => {
    expect(PHASE_TRIS_POUR_TOUS).toBe(true)
    expect(phaseTrisUtilisable('marvel.exemple.org')).toBe(true)
    expect(presentationProposee('tris')).toBe(true)
  })
})

describe('les réglages', () => {
  const p = (sur: Partial<ProprietesReglages> = {}) =>
    ({
      modePhase: 'detaille',
      changerModePhase: vi.fn(),
      libelleModePhase: (m: string) => (m === 'sur-table' ? 'Plateau animé' : m),
      ...sur,
    }) as unknown as ProprietesReglages
  const choix = () =>
    within(screen.getByText('Phase du méchant').closest('.ligne-option') as HTMLElement)
      .getAllByRole('button')
      .map((b) => b.textContent)
  it('exactement trois choix, Guidée visible sans l’essai de compte ni hôte local', () => {
    expect(PHASE_BIS_POUR_TOUS).toBe(true)
    // pas de serveur d'essais ici : fetch échoue, l'essai vaut faux
    vi.stubGlobal(
      'fetch',
      vi.fn(() => Promise.reject(new Error('hors ligne')))
    )
    render(<ContenuOnglet onglet="jeu" p={p()} />)
    expect(choix()).toEqual(['Guidée', 'Plateau animé', 'Accéléré'])
    vi.unstubAllGlobals()
  })
})
