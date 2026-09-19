// MenuTriche.test.tsx — le sous-menu « Déplacer vers », qui rend le menu
// utilisable en mode manuel : c'est lui qui parle à `triche.deplacerVers`.
import { fireEvent, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { MenuTriche } from './MenuTriche'

const CIBLE = { id: 42, nom: 'Carte test' }

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
})

/** Laisse les promesses de `triche.ts` (fetch, puis `envoyer`) se résoudre. */
const attendreLeReseau = () => new Promise((resolve) => setTimeout(resolve, 0))

describe('le sous-menu « Déplacer vers »', () => {
  it('deplace la carte vers la pile choisie, dessus', async () => {
    const onIntervention = vi.fn()
    const { getByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} onIntervention={onIntervention} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getByText('Deck Rencontre'))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Top')"] }),
    }))
    expect(onIntervention).toHaveBeenCalled()
  })

  it('depose sous la pile quand on le demande explicitement', async () => {
    const { getByText, getAllByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} onIntervention={vi.fn()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getAllByText('Sous la pile')[0])
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'HandsArea', 'Bottom')"] }),
    }))
  })

  it('précise que la pile écartée du menu est celle du héros, pas une pile du monde', () => {
    const { getByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} onIntervention={vi.fn()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    // Plusieurs piles moteur portent le type `AsideDeck` ; celle du menu est
    // `set_aside_nemesis_sets`, le set némésis du héros (voir triche.ts et
    // zones.ts, qui nomme déjà cette pile ainsi).
    expect(getByText('Set némésis du héros')).not.toBeNull()
  })
})
