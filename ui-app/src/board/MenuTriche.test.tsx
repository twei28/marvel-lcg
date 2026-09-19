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

/**
 * Un `emettreGeste` de test qui appelle vraiment le déposeur (comme le fait
 * `useTriche`) : sans ça, `triche.deplacerVers` ne serait jamais invoqué et
 * `fetch` ne verrait jamais passer la commande.
 */
function emettreGesteDeTest() {
  return vi.fn(async (_libelle: string, deposer: () => Promise<boolean>) => {
    await deposer()
  })
}

describe('le sous-menu « Déplacer vers »', () => {
  it('deplace la carte vers la pile choisie, dessus', async () => {
    const emettreGeste = emettreGesteDeTest()
    const { getByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGeste} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getByText('Deck Rencontre'))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Top')"] }),
    }))
    // Le menu DÉPOSE le geste (`emettreGeste`), il n'écrit plus lui-même la
    // ligne de journal : c'est `useTriche` qui la résout au rendu suivant
    // (correction du 19/09/2026, tâche 4 ter).
    expect(emettreGeste).toHaveBeenCalledWith(
      expect.stringContaining('Carte test'),
      expect.any(Function)
    )
  })

  it('depose sous la pile quand on le demande explicitement', async () => {
    // « Deck du héros » (PlayerDeck) est un deck ORDONNÉ : le dessous a un
    // sens, contrairement aux zones en jeu (voir `ZONES_ORDONNEES`).
    const { getByText, getAllByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getAllByText('Sous la pile')[0])
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'PlayerDeck', 'Bottom')"] }),
    }))
  })

  it('n’offre « Sous la pile » que sur les six decks ordonnés', () => {
    // Treize des dix-neuf piles ne sont pas des decks ORDONNÉS (alliés,
    // sbires engagés, set némésis, réserve, manigance principale, mises de
    // côté...) : leur "dessous" n'existe pas côté moteur (`MoveTo`,
    // `pile.flags.is_deck`/`is_dealt_encounter`), le bouton y ferait deux
    // fois le même geste. Un seul « Sous la pile » par pile ordonnée donne
    // 6, pas 19 (ronde de correction 1 de la tâche 5, 19/09/2026 :
    // `AdditionalDeck` et `AdditionalDiscardPile` ont rejoint les quatre
    // decks déjà ordonnés ; I2, revue finale du 20/09/2026 : `AsideScenario`
    // et `AsideModular` ont rejoint le menu, ni l'un ni l'autre ordonné).
    const { getByText, getAllByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    expect(getAllByText('Sous la pile')).toHaveLength(6)
    // « Alliés » (AlliesArea, une zone en jeu) n'a pas de second bouton :
    // seul le libellé de la pile est cliquable sur sa ligne.
    const ligneAllies = getByText('Alliés').closest('li')
    expect(ligneAllies?.querySelectorAll('button')).toHaveLength(1)
  })

  // ⚠ I2 (revue finale, 20/09/2026). `AsideScenario` et `AsideModular`
  // (`RunPuzzle.ZONES_MONDE`, `puzzle.py`) n'étaient atteignables par AUCUN
  // geste : leurs cartes sont fondues à l'affichage (`zones.ts`,
  // `pileFondue`, zone `annexes`), donc le glisser ne peut pas les viser
  // (`glisser-manuel.ts` les laisse volontairement hors de `PILE_PAR_ZONE`).
  // Le menu, qui vise par NOM et non par carte dessinée, n'a pas ce
  // problème : ce test prouve que les deux zones y sont bien arrivées.
  it('atteint les mises de côté du scénario et les mises de côté modulaires (I2)', async () => {
    const emettreGeste = emettreGesteDeTest()
    const { getByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGeste} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getByText('Mises de côté du scénario'))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'AsideScenario', 'Top')"] }),
    }))
  })

  it('atteint les mises de côté modulaires (I2)', async () => {
    const emettreGeste = emettreGesteDeTest()
    const { getByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGeste} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getByText('Mises de côté modulaires'))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'AsideModular', 'Top')"] }),
    }))
  })

  it('précise que la pile écartée du menu est celle du héros, pas une pile du monde', () => {
    const { getByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    // Plusieurs piles moteur portent le type `AsideDeck` ; celle du menu est
    // `set_aside_nemesis_sets`, déjà nommée « Set némésis » dans zones.ts.
    // MÊME libellé que là-bas : pas un second nom pour le même objet.
    expect(getByText('Set némésis')).not.toBeNull()
  })
})
