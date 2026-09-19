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
})
