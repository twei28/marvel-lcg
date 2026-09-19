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
