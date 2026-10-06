// menu-manuel.test.tsx — les quatre gestes du mode manuel parlent au moteur.
//
// Ce test ne monte AUCUN composant : il vise directement le canal
// (`triche.ts`), comme `triche.test.ts` le fait déjà pour les gestes du bac à
// sable. Le `.tsx` du nom vient du gabarit du plan ; il n'y a pas de JSX ici.
import { describe, expect, it, vi, beforeEach } from 'vitest'
import * as triche from '../triche'

describe('les gestes manuels parlent au moteur', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  it('deplace une carte vers une pile nommee', async () => {
    await triche.deplacerVers(42, 'EncounterDeck')
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Top')"] }),
    }))
  })

  it('depose une carte sous une pile quand on le demande', async () => {
    await triche.deplacerVers(42, 'EncounterDeck', 'Bottom')
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Bottom')"] }),
    }))
  })

  it('melange une pile', async () => {
    await triche.melanger('PlayerDeck')
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.Shuffle('PlayerDeck')"] }),
    }))
  })

  it('attache une carte a une autre', async () => {
    await triche.attacher(3, 9)
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Attach(3, 9)'] }),
    }))
  })

  it('engage un sbire avec le joueur', async () => {
    await triche.engager(7)
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Engage(7)'] }),
    }))
  })

  // Fait apparaitre une carte du catalogue qui n'etait pas dans la partie.
  // MEME COMMANDE que `deplacerVers(id, 'ProcessingArea')` (le geste
  // « piocher » sur une pile du monde) : `Puzzle.MoveTo` fabrique la carte
  // via `FindOrCreateFace` quand le nom ne designe rien encore, donc un seul
  // appel cree ET pose, en zone de RESOLUTION - jamais « en jeu » : c'est au
  // joueur de la deplacer ensuite avec les gestes qu'il a deja.
  it('fait apparaitre une carte en zone de resolution, jamais en jeu directement', async () => {
    await triche.creerCarte('01094')
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo('01094', 'ProcessingArea', 'Top')"] }),
    }))
  })
})

describe('annulerDernierGeste (Ctrl+Z)', () => {
  it('poste sur /manuel_undo et rend vrai quand le moteur accepte', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    const reussi = await triche.annulerDernierGeste()
    expect(fetch).toHaveBeenCalledWith('/manuel_undo', { method: 'POST' })
    expect(reussi).toBe(true)
  })

  // 409 : hors partie manuelle, ou plus rien a annuler (route moteur, tache
  // 6 du plan). Ni l'un ni l'autre n'est une panne reseau : `reponse.ok` vaut
  // deja faux, donc pas de faux « annule ».
  it('rend faux quand le moteur refuse (409, rien a annuler)', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false }) as Response))
    const reussi = await triche.annulerDernierGeste()
    expect(reussi).toBe(false)
  })

  it('rend faux sur une panne reseau, sans lever', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('reseau coupe') }))
    const reussi = await triche.annulerDernierGeste()
    expect(reussi).toBe(false)
  })
})

// ---------------------------------------------------------------------------
// Lot 3 du 06/10/2026 : le clic droit sur une carte EN MAIN propose « Poser en
// jeu », le même geste que le glisser sur la table et le double-clic.
// ---------------------------------------------------------------------------
import { act, fireEvent, render, screen } from '@testing-library/react'
import { CoucheTriche, useTriche } from '../CoucheTriche'
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import type { World } from '../world'

const TANTE_MAY = carteSurTable(30, '01006', 'Support', 'Aunt May')
const ALLIE_EN_JEU = carteSurTable(5, '01002a', 'Ally', 'Black Cat')

function mondeAvecMain(): World {
  return tableAvec(siege({ hand_cards: [TANTE_MAY], allies: [ALLIE_EN_JEU] }), {
    mode_manuel: true,
    manuel_actif: true,
  } as never)
}

function Harness({ world }: { world: World }) {
  const triche = useTriche(world, 0)
  return <CoucheTriche actif={triche.actif} manuel={triche.manuel} couche={triche.couche} />
}

function clicDroitSur(id: number) {
  const noeud = document.createElement('div')
  noeud.setAttribute('data-card-id', String(id))
  document.body.appendChild(noeud)
  fireEvent.contextMenu(noeud)
}

describe('le menu d’une carte en mode manuel', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
    document.body.innerHTML = ''
  })

  it('sur une carte en main : « Poser en jeu » la pose selon son type', async () => {
    render(<Harness world={mondeAvecMain()} />)
    clicDroitSur(30)
    fireEvent.click(await screen.findByText('Poser en jeu'))
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(30, 'SupportsArea', 'Top', siege=0)"] }),
    }))
  })

  it('sur une carte déjà en jeu : pas de « Poser en jeu »', async () => {
    render(<Harness world={mondeAvecMain()} />)
    clicDroitSur(5)
    await screen.findByText('Déplacer vers')
    expect(screen.queryByText('Poser en jeu')).toBeNull()
  })

  it('le titre du menu est le nom français de la carte', async () => {
    render(<Harness world={mondeAvecMain()} />)
    clicDroitSur(30)
    const menu = await screen.findByRole('menu')
    expect(menu.querySelector('.menu-triche-titre')?.textContent).toContain('Tante May')
  })
})
