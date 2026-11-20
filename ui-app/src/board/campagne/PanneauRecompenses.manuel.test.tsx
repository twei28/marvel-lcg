// PanneauRecompenses.manuel.test.tsx — le journal de campagne en mode manuel
// (tâche 7).
//
// En mode manuel, le moteur ne surveille plus la table : les cases marquées
// « relevé par le jeu » ne se rempliront plus toutes seules. Elles restent
// déjà CORRIGEABLES dans tous les modes (une autre session l'a décidé : un
// détecteur peut se tromper, mieux vaut une case modifiable qu'une campagne
// faussée — voir l'en-tête de `PanneauRecompenses.tsx`) ; ce qui manque en
// manuel, c'est de le DIRE, pour qu'on ne cherche pas pourquoi rien ne s'est
// rempli tout seul. Ce fichier verrouille seulement l'aide, et que le mode
// ordinaire ne perd rien.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { PanneauRecompenses } from './PanneauRecompenses'
import { CLE_CAMPAGNE } from './contexte'
import { mondeDeTest } from './world-de-test'
import { auBilan, auCarnet } from './parcours-test'

const CAMPAGNE = {
  id: 'trors-1',
  code: 'trors',
  nom: 'Ma campagne',
  difficulte: 'standard',
  termines: [],
  carnet: {},
}

const DEFINITION = {
  code: 'trors',
  nom: 'The Rise of Red Skull',
  cle_extension: 'trors',
  scenarios: [
    {
      id: 'crossbones',
      numero: 1,
      nom: 'Crossbones',
      victoire: [
        {
          cle: 'Delay',
          type: 'auto',
          format: 'int',
          libelle: 'Pions retard',
          detection: 'compteur_manigance',
        },
      ],
    },
  ],
}

function serveurDeCampagne() {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      const repondre = (charge: unknown) => ({ ok: true, json: async () => charge })
      if (url.startsWith('/get_campagne_definition')) return repondre(DEFINITION)
      if (url.startsWith('/get_campagne')) return repondre(CAMPAGNE)
      if (url.startsWith('/get_carnet_suggere')) return repondre({ scenario: null, suggestions: {} })
      if (url.startsWith('/save_carnet_partiel')) return repondre({ carnet: {} })
      return repondre({})
    })
  )
}

beforeEach(() => {
  window.localStorage.clear()
  serveurDeCampagne()
  window.localStorage.setItem(
    CLE_CAMPAGNE,
    JSON.stringify({ id: 'trors-1', scenario: 'crossbones' })
  )
})
afterEach(() => vi.unstubAllGlobals())

describe('le journal de campagne en mode manuel', () => {
  it('affiche une aide disant que les cases relevées par le jeu restent à remplir à la main', async () => {
    const monde = mondeDeTest({ mode_manuel: true })
    render(<PanneauRecompenses monde={monde} gagne siege={0} onTermine={() => {}} />)
    await auBilan()
    await waitFor(() => expect(screen.getByText('Pions retard')).toBeInTheDocument())
    expect(screen.getByText(/mode manuel/i)).toBeInTheDocument()
  })

  it("n'affiche rien de tel en partie ordinaire : le mode ordinaire ne perd rien", async () => {
    const monde = mondeDeTest({ mode_manuel: false })
    render(<PanneauRecompenses monde={monde} gagne siege={0} onTermine={() => {}} />)
    await auBilan()
    await waitFor(() => expect(screen.getByText('Pions retard')).toBeInTheDocument())
    expect(screen.queryByText(/mode manuel/i)).toBeNull()
  })

  it('la case relevée par le jeu reste saisissable en mode manuel, exactement comme en partie ordinaire', async () => {
    const monde = mondeDeTest({ mode_manuel: true })
    render(<PanneauRecompenses monde={monde} gagne siege={0} onTermine={() => {}} />)
    await auCarnet()
    await waitFor(() => expect(screen.getByText('Pions retard')).toBeInTheDocument())
    const champ = screen.getByRole('spinbutton') as HTMLInputElement
    expect(champ.disabled).toBe(false)
  })
})
