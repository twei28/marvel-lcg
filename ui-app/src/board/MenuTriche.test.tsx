// MenuTriche.test.tsx — le sous-menu « Déplacer vers », qui rend le menu
// utilisable en mode manuel : c'est lui qui parle à `triche.deplacerVers`.
import { fireEvent, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { MenuTriche, ZONES_MANUELLES } from './MenuTriche'

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

  // Suite de la revue finale (20/09/2026) : même famille de trou que
  // AsideScenario/AsideModular ci-dessus, cinq zones de plus repérées en
  // vérifiant `RunPuzzle.ZONES_JOUEUR`/`ZONES_MONDE` (`puzzle.py`) une par
  // une. Une propriété plus générale suit plus bas (« toute zone que le
  // moteur expose figure au menu ») ; ces cas nommés restent utiles pour
  // vérifier la commande exacte envoyée à chacune.
  it.each([
    ['Héros', 'HeroArea'],
    ['Ressources', 'ResourcesArea'],
    ['Obligations', 'ObligationsArea'],
    ['Environnement', 'EnvironmentArea'],
    ['En cours de résolution', 'ProcessingArea'],
  ])('atteint « %s » (%s)', async (libelle, zoneMoteur) => {
    const emettreGeste = emettreGesteDeTest()
    const { getByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGeste} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getByText(libelle))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: [`Puzzle.MoveTo(42, '${zoneMoteur}', 'Top')`] }),
    }))
  })

  // I4 (revue finale, 20/09/2026) : ce même menu s'ouvre en bac à sable ET en
  // mode manuel. « Triche » n'a de sens que dans le premier.
  it('marque « Triche » par défaut (bac à sable)', () => {
    const { getByText, queryByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} />
    )
    expect(getByText('Triche')).not.toBeNull()
    expect(queryByText('Geste manuel')).toBeNull()
  })

  it('marque « Geste manuel », jamais « Triche », en mode manuel', () => {
    const { getByText, queryByText } = render(
      <MenuTriche
        cible={CIBLE}
        x={0}
        y={0}
        onFermer={vi.fn()}
        emettreGeste={emettreGesteDeTest()}
        manuel
      />
    )
    expect(getByText('Geste manuel')).not.toBeNull()
    expect(queryByText('Triche')).toBeNull()
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

// --- Toute zone que le moteur expose figure au menu (suite de la revue
// finale, 20/09/2026) --------------------------------------------------
//
// I2 avait trouvé deux zones du moteur qu'aucun geste n'atteignait
// (AsideScenario, AsideModular) précisément parce que le test de propriété
// de la tâche 5 (`glisser-manuel.test.ts`) ne vérifie que « glisser ⊆
// menu », jamais « moteur ⊆ menu ». La revue en a trouvé cinq autres à la
// main juste après (HeroArea, ResourcesArea, ObligationsArea,
// EnvironmentArea, ProcessingArea). Cette propriété-ci ferme la vraie
// faille : elle attrapera le PROCHAIN oubli sans attendre une nouvelle
// relecture manuelle de `puzzle.py`.
//
// ⚠ MIROIR TENU À LA MAIN, PAS GÉNÉRÉ. Aucun pont Python → TypeScript
// n'existe dans ce projet : cette liste recopie `RunPuzzle.ZONES_JOUEUR` et
// `RunPuzzle.ZONES_MONDE` (`Fusion/marvel-lcg-src/src/game/puzzle/
// puzzle.py`) zone par zone, et DOIT être mise à jour avec ce fichier. La
// garantie qu'elle offre n'est donc pas absolue (une zone ajoutée là-bas
// sans être répercutée ici reste invisible), mais elle vaut mieux que rien
// — c'est exactement ce qui manquait pour attraper les sept zones ci-dessus
// avant qu'une revue humaine ne les remarque une par une.
const ZONES_MOTEUR = [
  // RunPuzzle.ZONES_JOUEUR
  'PlayerDeck', 'DiscardPile', 'HandsArea', 'AlliesArea', 'SupportsArea',
  'HeroArea', 'EngagedEnemiesArea', 'ResourcesArea', 'ReserveArea',
  'AsideDeck', 'ObligationsArea', 'AdditionalDeck', 'AdditionalDiscardPile',
  // RunPuzzle.ZONES_MONDE
  'EncounterDeck', 'EncounterDiscardPile', 'VillainArea', 'MainSchemesArea',
  'SideSchemesArea', 'EnvironmentArea', 'ProcessingArea', 'RemovedArea',
  'VictoryDisplay', 'AsideScenario', 'AsideModular',
]

describe('toute zone que le moteur expose figure au menu', () => {
  it('chaque zone de ZONES_MOTEUR figure dans ZONES_MANUELLES', () => {
    const manquantes = ZONES_MOTEUR.filter((zone) => !ZONES_MANUELLES.includes(zone))
    expect(
      manquantes,
      `zone(s) exposée(s) par le moteur mais absente(s) du menu de clic droit : ${manquantes.join(', ')}`
    ).toEqual([])
  })

  it('le témoin n’est pas vide : la propriété teste vraiment quelque chose', () => {
    expect(ZONES_MOTEUR.length).toBeGreaterThan(0)
    expect(ZONES_MANUELLES.length).toBeGreaterThan(0)
  })
})
