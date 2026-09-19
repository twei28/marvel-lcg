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
    // « Deck du héros » (PlayerDeck) est un deck ORDONNÉ : le dessous a un
    // sens, contrairement aux zones en jeu (voir `ZONES_ORDONNEES`).
    const { getByText, getAllByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} onIntervention={vi.fn()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getAllByText('Sous la pile')[0])
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'PlayerDeck', 'Bottom')"] }),
    }))
  })

  it('n’offre « Sous la pile » que sur les quatre decks ordonnés', () => {
    // Neuf des treize piles sont des zones EN JEU (alliés, sbires engagés,
    // set némésis...) : leur "dessous" n'existe pas côté moteur (`MoveTo`,
    // `pile.flags.is_deck`/`is_dealt_encounter`), le bouton y ferait deux
    // fois le même geste. Un seul « Sous la pile » par pile ordonnée donne
    // 4, pas 13.
    const { getByText, getAllByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} onIntervention={vi.fn()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    expect(getAllByText('Sous la pile')).toHaveLength(4)
    // « Alliés » (AlliesArea, une zone en jeu) n'a pas de second bouton :
    // seul le libellé de la pile est cliquable sur sa ligne.
    const ligneAllies = getByText('Alliés').closest('li')
    expect(ligneAllies?.querySelectorAll('button')).toHaveLength(1)
  })

  it('précise que la pile écartée du menu est celle du héros, pas une pile du monde', () => {
    const { getByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} onIntervention={vi.fn()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    // Plusieurs piles moteur portent le type `AsideDeck` ; celle du menu est
    // `set_aside_nemesis_sets`, déjà nommée « Set némésis » dans zones.ts.
    // MÊME libellé que là-bas : pas un second nom pour le même objet.
    expect(getByText('Set némésis')).not.toBeNull()
  })
})
