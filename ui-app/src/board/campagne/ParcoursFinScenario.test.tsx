// Le parcours de fin de scénario : Victoire → Bilan → Carnet → Suite.
//
// Verrouille ce que l'utilisateur a demandé (29/10/2026) : un « Continuer » par page,
// un « Retour » partout sauf sur la Victoire, le choix obligatoire qui bloque le bilan,
// et un « Commencer » qui lance d'office le scénario suivant (sauf assemblée).
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { PanneauRecompenses } from './PanneauRecompenses'
import { CLE_CAMPAGNE } from './contexte'
import { mondeDeTest } from './world-de-test'
import { alaSuite, auBilan, auCarnet } from './parcours-test'

const CAMPAGNE = {
  id: 'trors-1',
  code: 'trors',
  nom: 'Ma campagne',
  difficulte: 'standard',
  termines: [] as string[],
  carnet: {},
}

type Scenario = Record<string, unknown>

function definition(scenarios: Scenario[]) {
  return { code: 'trors', nom: 'The Rise of Red Skull', cle_extension: 'trors', scenarios }
}

const CROSSBONES: Scenario = {
  id: 'crossbones',
  numero: 1,
  nom: 'Crossbones',
  victoire: [
    { cle: 'Tech Upgrade', type: 'choix', parJoueur: true, obligatoire: true, libelle: 'Amélioration technologique', options: ['04155', '04156'] },
    { cle: 'Weapons', type: 'auto', format: 'liste', libelle: 'Armes expérimentales', options: ['04072'] },
  ],
}
const ABSORBING: Scenario = { id: 'absorbing_man', numero: 2, nom: 'Absorbing Man', resume: 'La chasse continue.', enjeu: 'Des pions retard.' }

function serveur(def: unknown, campagne: Record<string, unknown> = CAMPAGNE) {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      const repondre = (charge: unknown) => ({ ok: true, json: async () => charge })
      if (url.startsWith('/get_campagne_definition')) return repondre(def)
      if (url.startsWith('/get_campagne')) return repondre(campagne)
      if (url.startsWith('/get_carnet_suggere')) return repondre({ scenario: null, suggestions: {} })
      if (url.startsWith('/get_scenario_json')) return repondre({ villain: ['04076'], encounter_sets: ['standard'], modular_sets: ['hydra_patrol'] })
      if (url.startsWith('/save_')) return repondre({ campagne, carnet: {} })
      return repondre({})
    })
  )
}

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}

beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
  window.localStorage.clear()
  window.localStorage.setItem(CLE_CAMPAGNE, JSON.stringify({ id: 'trors-1', scenario: 'crossbones' }))
})
afterEach(() => vi.unstubAllGlobals())

const pageCourante = () => document.querySelector('.parcours-fin')?.getAttribute('data-page')

describe('le parcours de fin de scénario', () => {
  it("ouvre sur la page Victoire, sans bouton Retour", async () => {
    serveur(definition([CROSSBONES, ABSORBING]))
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={() => {}} />)
    await screen.findByRole('button', { name: 'Continuer' })
    expect(pageCourante()).toBe('victoire')
    expect(screen.queryByRole('button', { name: 'Retour' })).toBeNull()
  })

  it('un choix obligatoire manquant bloque « Continuer » sur le bilan', async () => {
    serveur(definition([CROSSBONES, ABSORBING]))
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={() => {}} />)
    await auBilan()
    const continuer = screen.getByRole('button', { name: 'Continuer' }) as HTMLButtonElement
    expect(continuer.disabled).toBe(true)
    expect(screen.getByText(/À choisir avant de continuer/)).toBeInTheDocument()
  })

  it('« Retour » ramène à la page précédente', async () => {
    serveur(definition([CROSSBONES, ABSORBING]))
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={() => {}} />)
    await auBilan()
    fireEvent.click(screen.getByRole('button', { name: 'Retour' }))
    await waitFor(() => expect(pageCourante()).toBe('victoire'))
  })

  it('le carnet propose les quatre onglets', async () => {
    serveur(definition([{ ...CROSSBONES, victoire: [{ cle: 'Poids', type: 'auto', format: 'int', libelle: 'Poids' }] }, ABSORBING]))
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={() => {}} />)
    await auCarnet()
    for (const nom of ['Valeurs du carnet', 'Journal des scénarios', 'Les héros', 'Histoire du livret']) {
      expect(screen.getByRole('tab', { name: nom })).toBeInTheDocument()
    }
    fireEvent.click(screen.getByRole('tab', { name: 'Journal des scénarios' }))
    expect(screen.getByText(/Absorbing Man/)).toBeInTheDocument()
  })

  it('« Commencer » demande le lancement direct du scénario suivant', async () => {
    serveur(definition([{ ...CROSSBONES, victoire: [] }, ABSORBING]))
    const fin = vi.fn()
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={fin} />)
    await alaSuite()
    expect(screen.getByText('Absorbing Man')).toBeInTheDocument()
    fireEvent.click(await screen.findByRole('button', { name: 'Commencer' }))
    await waitFor(() => expect(fin).toHaveBeenCalled())
    expect(fin).toHaveBeenCalledWith(true, { campagne: 'trors-1', lancer: 'absorbing_man' })
  })

  it('« Options du scénario » ouvre la campagne sans lancer le scénario', async () => {
    serveur(definition([{ ...CROSSBONES, victoire: [] }, ABSORBING]))
    const fin = vi.fn()
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={fin} />)
    await alaSuite()
    fireEvent.click(await screen.findByRole('button', { name: 'Options du scénario' }))
    await waitFor(() => expect(fin).toHaveBeenCalled())
    expect(fin).toHaveBeenCalledWith(true, { campagne: 'trors-1', lancer: undefined })
  })

  it("un scénario en assemblée ne se lance pas d'office", async () => {
    serveur(definition([{ ...CROSSBONES, victoire: [] }, { ...ABSORBING, assemblee: { mode: 'x' } }]))
    const fin = vi.fn()
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={fin} />)
    await alaSuite()
    fireEvent.click(await screen.findByRole('button', { name: 'Choisir la suite' }))
    await waitFor(() => expect(fin).toHaveBeenCalled())
    expect(fin).toHaveBeenCalledWith(true, { campagne: 'trors-1', lancer: undefined })
  })

  it('le dernier scénario gagné finit sur la page de fin de campagne', async () => {
    serveur(definition([{ ...CROSSBONES, victoire: [], final: true }]))
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={() => {}} />)
    await alaSuite()
    expect(screen.getByText('Campagne terminée !')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Voir la conclusion' })).toBeInTheDocument()
  })

  it("un distant n'a pas de bouton pour lancer : il attend l'hôte", async () => {
    serveur(definition([{ ...CROSSBONES, victoire: [] }, ABSORBING]))
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={1} onTermine={() => {}} />)
    await alaSuite()
    expect(screen.queryByRole('button', { name: 'Commencer' })).toBeNull()
    expect(screen.getByText(/En attente de l'hôte pour commencer/)).toBeInTheDocument()
  })
})
