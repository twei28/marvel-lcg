// Le panneau à plusieurs : chacun ses cases, et l'hôte seul valide.
//
// Le piège que ce fichier verrouille : un distant qui verrait « Valider »
// terminerait le scénario pour toute la table, depuis un écran où il n'a
// rempli qu'une case. La règle est déjà testée dans `droits-carnet.test.ts` ;
// ici on vérifie qu'elle est bien BRANCHÉE, ce qu'un test de règle ne dit pas.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { PanneauRecompenses } from './PanneauRecompenses'
import { CLE_CAMPAGNE } from './contexte'
import { mondeDeTest } from './world-de-test'

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
        { cle: 'Upgrade', type: 'choix', parJoueur: true, libelle: 'Amélioration', options: ['01001'] },
        { cle: 'Bombs Defused', type: 'choix', format: 'int', libelle: 'Bombes désamorcées' },
      ],
    },
  ],
}

/** Le serveur, réduit à ce que le panneau lui demande au montage. */
function serveurDeCampagne() {
  const envois: Array<{ url: string; corps: unknown }> = []
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, options?: { body?: string }) => {
      if (options?.body) envois.push({ url, corps: JSON.parse(options.body) })
      const repondre = (charge: unknown) => ({ ok: true, json: async () => charge })
      if (url.startsWith('/get_campagne_definition')) return repondre(DEFINITION)
      if (url.startsWith('/get_campagne')) return repondre(CAMPAGNE)
      if (url.startsWith('/get_carnet_suggere')) return repondre({ scenario: null, suggestions: {} })
      if (url.startsWith('/save_carnet_partiel')) return repondre({ carnet: {} })
      return repondre({})
    })
  )
  return envois
}

// jsdom n'implemente pas ResizeObserver : l'aperçu agrandi l'observe pour se poser.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}

beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
  window.localStorage.clear()
  serveurDeCampagne()
  window.localStorage.setItem(
    CLE_CAMPAGNE,
    JSON.stringify({ id: 'trors-1', scenario: 'crossbones' })
  )
})
afterEach(() => vi.unstubAllGlobals())

describe('le panneau à plusieurs', () => {
  it("ne montre pas « Valider » à un siège qui n'est pas l'hôte", async () => {
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={1} onTermine={() => {}} />)
    await waitFor(() => expect(screen.getByText(/Envoyer mes champs/)).toBeInTheDocument())
    expect(screen.queryByText(/Valider et continuer/)).toBeNull()
  })

  it("montre « Valider » à l'hôte, et pas le bouton d'envoi", async () => {
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={0} onTermine={() => {}} />)
    await waitFor(() => expect(screen.getByText(/Valider et continuer/)).toBeInTheDocument())
    expect(screen.queryByText(/Envoyer mes champs/)).toBeNull()
  })

  it("dit au distant que c'est l'hôte qui valide", async () => {
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={1} onTermine={() => {}} />)
    await waitFor(() =>
      expect(screen.getByText(/L'hôte valide les récompenses pour la table/)).toBeInTheDocument()
    )
  })

  it('rend inertes les cases des autres sièges', async () => {
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={1} onTermine={() => {}} />)
    await waitFor(() => expect(screen.getByText(/Envoyer mes champs/)).toBeInTheDocument())

    // « Bombes désamorcées » est un champ COMMUN : il appartient à l'hôte, donc
    // le siège 1 ne peut pas y toucher.
    const commun = screen.getByRole('spinbutton') as HTMLInputElement
    expect(commun.disabled).toBe(true)

    // Le champ personnel existe en deux exemplaires (un par siège). Celui du
    // siège 0 est inerte, celui du siège 1 est ouvert.
    const cartes = screen.getAllByRole('button', { name: '01001' }) as HTMLButtonElement[]
    expect(cartes).toHaveLength(2)
    expect(cartes[0]?.disabled).toBe(true)
    expect(cartes[1]?.disabled).toBe(false)
  })

  it("agrandit la carte au survol, même quand sa case est inerte, et la ferme en sortant", async () => {
    render(<PanneauRecompenses monde={mondeDeTest()} gagne siege={1} onTermine={() => {}} />)
    await waitFor(() => expect(screen.getByText(/Envoyer mes champs/)).toBeInTheDocument())
    const cartes = screen.getAllByRole('button', { name: '01001' }) as HTMLButtonElement[]
    const inerte = cartes[0]!
    expect(inerte.disabled).toBe(true)
    expect(document.querySelector('.carte-apercu')).toBeNull()

    fireEvent.mouseOver(inerte.closest('[data-card-id]')!)
    expect(document.querySelector('.carte-apercu.au-dessus-de-la-fin')).not.toBeNull()

    fireEvent.mouseLeave(inerte.closest('.camp-cartes')!)
    expect(document.querySelector('.carte-apercu')).toBeNull()
  })
})
