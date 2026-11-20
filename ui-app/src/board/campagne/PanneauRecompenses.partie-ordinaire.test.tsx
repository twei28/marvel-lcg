// PanneauRecompenses.partie-ordinaire.test.tsx : une partie ORDINAIRE ne
// s'ouvre jamais sur les récompenses d'une campagne.
//
// Défaut signalé le 07/10/2026 : une campagne était en cours (un scénario
// lancé, jamais validé), le joueur lance une partie normale, d'un autre
// méchant, la gagne, et le panneau « Alliés secourus » s'ouvre : valider
// faisait avancer le scénario de la campagne.
//
// Cause : le contexte de campagne se déduisait d'un état DURABLE, la clé du
// navigateur ou le `partieEnCours` du serveur, qu'aucune partie ordinaire
// n'efface (il sert à reprendre un scénario). Le critère fiable est celui du
// moteur : la règle `mode_campaign`, publiée dans le descripteur du monde, donc
// valable pour tous les sièges et conservée par les sauvegardes.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { PanneauRecompenses } from './PanneauRecompenses'
import { CLE_CAMPAGNE } from './contexte'
import { mondeDeTest } from './world-de-test'
import { auBilan } from './parcours-test'

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
        { cle: 'Delay', type: 'auto', format: 'int', libelle: 'Pions retard', detection: 'compteur_manigance' },
      ],
    },
  ],
}

const appels: string[] = []

/** Un serveur dont `partieEnCours` est resté armé : il désigne toujours Crossbones. */
function serveurAvecCampagnePerimee() {
  appels.length = 0
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      appels.push(url)
      const repondre = (charge: unknown) => ({ ok: true, json: async () => charge })
      if (url.startsWith('/get_campagne_en_cours')) return repondre({ id: 'trors-1', scenario: 'crossbones' })
      if (url.startsWith('/get_campagne_definition')) return repondre(DEFINITION)
      if (url.startsWith('/get_campagne')) return repondre(CAMPAGNE)
      if (url.startsWith('/get_carnet_suggere')) return repondre({ scenario: null, suggestions: {} })
      return repondre({})
    })
  )
}

beforeEach(() => {
  window.localStorage.clear()
  serveurAvecCampagnePerimee()
})
afterEach(() => vi.unstubAllGlobals())

async function laisserLePanneauDecider() {
  // Le panneau décide dans un effet asynchrone : on attend que le réseau soit
  // quiet, sinon un « absent » tardif passerait pour un panneau jamais ouvert.
  await new Promise((r) => setTimeout(r, 30))
}

describe('une partie ordinaire ne reprend pas le contexte d’une campagne', () => {
  it('victoire ordinaire, clé absente, serveur qui désigne une campagne : aucun panneau', async () => {
    const monde = mondeDeTest({ mode_campaign: false })
    const { container } = render(<PanneauRecompenses monde={monde} gagne siege={0} onTermine={() => {}} />)
    await laisserLePanneauDecider()
    expect(screen.queryByText('Pions retard')).toBeNull()
    expect(container.querySelector('.camp-recomp')).toBeNull()
    expect(container.firstChild).toBeNull()
  })

  it('victoire ordinaire, clé locale restée posée (sauvegarde, puzzle) : aucun panneau', async () => {
    window.localStorage.setItem(CLE_CAMPAGNE, JSON.stringify({ id: 'trors-1', scenario: 'crossbones' }))
    const monde = mondeDeTest({ mode_campaign: false })
    const { container } = render(<PanneauRecompenses monde={monde} gagne siege={0} onTermine={() => {}} />)
    await laisserLePanneauDecider()
    expect(screen.queryByText('Pions retard')).toBeNull()
    expect(container.firstChild).toBeNull()
  })

  it('une partie ordinaire ne touche pas à la campagne : aucune route de campagne appelée', async () => {
    const monde = mondeDeTest({ mode_campaign: false })
    render(<PanneauRecompenses monde={monde} gagne siege={0} onTermine={() => {}} />)
    await laisserLePanneauDecider()
    expect(appels).toEqual([])
  })

  it('descripteur sans la règle (ancien moteur) : aucun panneau', async () => {
    const monde = mondeDeTest()
    delete monde.mode_campaign
    const { container } = render(<PanneauRecompenses monde={monde} gagne siege={0} onTermine={() => {}} />)
    await laisserLePanneauDecider()
    expect(container.firstChild).toBeNull()
  })

  it('défaite ordinaire : aucun panneau non plus', async () => {
    const monde = mondeDeTest({ mode_campaign: false })
    const { container } = render(<PanneauRecompenses monde={monde} gagne={false} siege={0} onTermine={() => {}} />)
    await laisserLePanneauDecider()
    expect(container.firstChild).toBeNull()
    expect(appels).toEqual([])
  })
})

describe('le témoin : une vraie partie de campagne ouvre toujours le panneau', () => {
  it('siège distant, aucune clé locale, règle mode_campaign vraie : le panneau s’ouvre par le serveur', async () => {
    const monde = mondeDeTest({ mode_campaign: true })
    render(<PanneauRecompenses monde={monde} gagne siege={1} onTermine={() => {}} />)
    await auBilan()
    await waitFor(() => expect(screen.getByText('Pions retard')).toBeInTheDocument())
  })

  it('hôte, clé locale posée, règle vraie : le panneau s’ouvre', async () => {
    window.localStorage.setItem(CLE_CAMPAGNE, JSON.stringify({ id: 'trors-1', scenario: 'crossbones' }))
    const monde = mondeDeTest({ mode_campaign: true })
    render(<PanneauRecompenses monde={monde} gagne siege={0} onTermine={() => {}} />)
    await auBilan()
    await waitFor(() => expect(screen.getByText('Pions retard')).toBeInTheDocument())
  })
})
