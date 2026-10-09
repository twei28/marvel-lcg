// PanneauRecompenses.defaite-continue.test.tsx : une défaite qui fait
// CONTINUER la campagne (Hunting Season, décision du 09/10/2026).
//
// Le livret donne des gains à la défaite des scénarios 1 à 4 (« LOSS : each
// player earns 2 Experience… ») puis passe au suivant. Avant `defaite_continue`,
// une défaite n'ouvrait le panneau que si elle perdait la campagne : les gains
// étaient perdus et le scénario restait à rejouer.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { PanneauRecompenses } from './PanneauRecompenses'
import { CLE_CAMPAGNE } from './contexte'
import { mondeDeTest } from './world-de-test'

const CAMPAGNE = {
  id: 'hs-1',
  code: 'hunting_season',
  nom: 'Ma chasse',
  difficulte: 'standard',
  termines: [],
  carnet: { 'Player 1 Experience': '1' },
}

function definition(defaiteContinue: boolean) {
  return {
    code: 'hunting_season',
    nom: 'Hunting Season',
    cle_extension: 'hs',
    scenarios: [
      {
        id: 'hs_vermin',
        numero: 1,
        nom: 'Vermin',
        ...(defaiteContinue ? { defaite_continue: true } : {}),
        victoire: [{ cle: 'Vermin escaped', type: 'auto', format: 'int', libelle: 'Vermin en fuite' }],
      },
      { id: 'hs_scorpion', numero: 2, nom: 'Scorpion' },
    ],
    victoire_commune: [
      { cle: 'Experience', type: 'auto', format: 'int', parJoueur: true, libelle: 'Expérience disponible' },
    ],
  }
}

let enregistree: { termines?: string[]; carnet?: Record<string, string> } | null = null

function serveur(defaiteContinue: boolean) {
  enregistree = null
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, init?: { body?: string }) => {
      const repondre = (charge: unknown) => ({ ok: true, json: async () => charge })
      if (url.startsWith('/get_campagne_en_cours')) return repondre({ id: 'hs-1', scenario: 'hs_vermin' })
      if (url.startsWith('/get_campagne_definition')) return repondre(definition(defaiteContinue))
      if (url.startsWith('/get_campagne')) return repondre(CAMPAGNE)
      if (url.startsWith('/get_carnet_suggere')) {
        return repondre({
          scenario: 'hs_vermin',
          suggestions: { 'Player 1 Experience': '4', 'Vermin escaped': '1' },
        })
      }
      if (url.startsWith('/save_campagne')) {
        enregistree = JSON.parse(init?.body ?? '{}').campagne
        return repondre({ campagne: enregistree })
      }
      return repondre({})
    })
  )
}

beforeEach(() => {
  window.localStorage.clear()
  window.localStorage.setItem(CLE_CAMPAGNE, JSON.stringify({ id: 'hs-1', scenario: 'hs_vermin' }))
})
afterEach(() => vi.unstubAllGlobals())

describe('defaite_continue : une défaite qui fait avancer la campagne', () => {
  it('le panneau s’ouvre sur la défaite et montre les gains relevés par le moteur', async () => {
    serveur(true)
    const monde = mondeDeTest({ mode_campaign: true })
    render(<PanneauRecompenses monde={monde} gagne={false} siege={0} onTermine={() => {}} />)
    await waitFor(() => expect(screen.getByText('Expérience disponible')).toBeInTheDocument())
    expect(screen.getByText('Vermin en fuite')).toBeInTheDocument()
    expect(screen.getByText(/la campagne continue/)).toBeInTheDocument()
  })

  it('valider marque le scénario comme joué et garde le carnet de la défaite', async () => {
    serveur(true)
    const monde = mondeDeTest({ mode_campaign: true })
    render(<PanneauRecompenses monde={monde} gagne={false} siege={0} onTermine={() => {}} />)
    const bouton = await screen.findByText('Valider et continuer la campagne')
    // Le pré-remplissage arrive dans un effet : attendre la valeur du moteur.
    await screen.findByDisplayValue('4')
    fireEvent.click(bouton)
    await waitFor(() => expect(enregistree).not.toBeNull())
    expect(enregistree?.termines).toEqual(['hs_vermin'])
    expect(enregistree?.carnet?.['Player 1 Experience']).toBe('4')
    expect(enregistree?.carnet?.['Vermin escaped']).toBe('1')
  })

  it('témoin : sans `defaite_continue`, une défaite n’ouvre aucun panneau', async () => {
    serveur(false)
    const monde = mondeDeTest({ mode_campaign: true })
    const { container } = render(<PanneauRecompenses monde={monde} gagne={false} siege={0} onTermine={() => {}} />)
    await new Promise((r) => setTimeout(r, 50))
    expect(screen.queryByText('Expérience disponible')).toBeNull()
    expect(container.querySelector('.camp-recomp')).toBeNull()
  })
})
