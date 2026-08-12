// Les boutons ne decident rien : ils appellent le module et poussent le
// resultat dehors. Ce qui se teste ici, c'est donc le CHEMIN — que le texte
// parte vraiment au presse-papier, que le fichier porte le bon nom, et qu'un
// refus du navigateur se DISE au lieu de passer pour un succes.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { act, render, renderHook, screen } from '@testing-library/react'
import { BoutonsRapportBug, MessageRapport, useRapportBug, type OutilsRapport } from './RapportBug'
import { CLE_CAMPAGNE } from './campagne/contexte'
import type { World } from './world'

const ZONES = {
  area_schemes_main: [], main_schemes_deck: [], area_schemes_side: [],
  additional_decks: [], additional_discard_piles: [], area_villain: [],
  villain_deck: [], encounter_deck: [], encounter_discard_pile: [],
  area_boost: [], area_environment: [], area_evidence: [], area_rule: [],
  area_processing: [], area_revealing: [], area_resources: [],
  area_removed: [], area_insert: [], area_set_aside: [],
  victory_display: [], area_status_cards: [], players: [],
  active_card_ids: [],
}

const MONDE: World = {
  render_id: 43, round_id: 3, phase: 'Player 1 Turn', prompt: '',
  event_name: 'PlayerOnEvent_Text', ...ZONES,
}

function pressePapier(reponse: 'ok' | 'refus') {
  const ecrire =
    reponse === 'ok'
      ? vi.fn().mockResolvedValue(undefined)
      : vi.fn().mockRejectedValue(new Error('refus'))
  Object.defineProperty(navigator, 'clipboard', { value: { writeText: ecrire }, configurable: true })
  return ecrire
}

const fauxOutils = (): OutilsRapport => ({
  copier: vi.fn().mockResolvedValue(undefined),
  telecharger: vi.fn(),
  message: null,
})

beforeEach(() => {
  window.sessionStorage.clear()
  window.localStorage.clear()
})

describe('les outils de rapport', () => {
  it('copie le texte dans le presse-papier', async () => {
    const ecrire = pressePapier('ok')
    const { result } = renderHook(() => useRapportBug(MONDE, undefined, [], 0))
    await act(async () => {
      await result.current.copier('recent')
    })

    expect(ecrire).toHaveBeenCalledOnce()
    expect(String(ecrire.mock.calls[0]?.[0])).toContain('RAPPORT DE BUG')
    expect(result.current.message).toBe('Rapport copié')
  })

  it('DIT quand le navigateur refuse la copie', async () => {
    pressePapier('refus')
    const { result } = renderHook(() => useRapportBug(MONDE, undefined, [], 0))
    await act(async () => {
      await result.current.copier('recent')
    })

    expect(result.current.message).toBe('Copie refusée par le navigateur')
  })

  it("ne fait rien tant que le monde n'est pas charge", async () => {
    const ecrire = pressePapier('ok')
    const { result } = renderHook(() => useRapportBug(undefined, undefined, [], 0))
    await act(async () => {
      await result.current.copier('recent')
    })

    expect(ecrire).not.toHaveBeenCalled()
  })

  it('inscrit la campagne en cours au rapport', async () => {
    const ecrire = pressePapier('ok')
    window.localStorage.setItem(CLE_CAMPAGNE, JSON.stringify({ id: 'trors-1', scenario: 'crossbones' }))
    const { result } = renderHook(() => useRapportBug(MONDE, undefined, [], 0))
    await act(async () => {
      await result.current.copier('recent')
    })

    expect(String(ecrire.mock.calls[0]?.[0])).toContain('campagne trors-1, scénario crossbones')
  })
})

describe('le panneau', () => {
  it('offre les trois portees et les deux sorties', () => {
    render(<BoutonsRapportBug outils={fauxOutils()} />)

    expect(screen.getByRole('button', { name: /Copier/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Télécharger/ })).toBeInTheDocument()
    const selecteur = screen.getByLabelText(/Profondeur/) as HTMLSelectElement
    expect([...selecteur.options].map((o) => o.value)).toEqual(['recent', 'tour', 'partie'])
  })

  it('passe la portee choisie a la sortie', async () => {
    const outils = fauxOutils()
    render(<BoutonsRapportBug outils={outils} />)

    const selecteur = screen.getByLabelText(/Profondeur/) as HTMLSelectElement
    await act(async () => {
      selecteur.value = 'partie'
      selecteur.dispatchEvent(new Event('change', { bubbles: true }))
    })
    await act(async () => {
      screen.getByRole('button', { name: /Copier/ }).click()
    })

    expect(outils.copier).toHaveBeenCalledWith('partie')
  })

  it('telecharge avec la portee choisie', async () => {
    const outils = fauxOutils()
    render(<BoutonsRapportBug outils={outils} />)
    await act(async () => {
      screen.getByRole('button', { name: /Télécharger/ }).click()
    })
    expect(outils.telecharger).toHaveBeenCalledWith('recent')
  })
})

describe('la confirmation', () => {
  it("ne rend rien quand il n'y a rien a dire", () => {
    const { container } = render(<MessageRapport message={null} />)
    expect(container).toBeEmptyDOMElement()
  })

  it("s'annonce aux lecteurs d'ecran", () => {
    render(<MessageRapport message="Rapport copié" />)
    expect(screen.getByRole('status')).toHaveTextContent('Rapport copié')
  })
})
