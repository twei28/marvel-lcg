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

  // Lot 5 du 06/10/2026 : à plusieurs héros, une pile de joueur se vise par
  // le siège du propriétaire, jamais le premier joueur du moment.
  it('vise le siège du propriétaire quand la cible le porte', async () => {
    const { getByText } = render(
      <MenuTriche cible={{ ...CIBLE, siege: 1 }} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} />
    )
    fireEvent.click(getByText('Déplacer vers'))
    fireEvent.click(getByText('Pile de défausse'))
    await attendreLeReseau()
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'DiscardPile', 'Top', siege=1)"] }),
    }))
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

// ==========================================================================
// Le menu reste ENTIÈREMENT dans l'écran (22/09/2026)
// ==========================================================================
// ⚠ SIGNALÉ EN JEU : un clic droit sur un PERSONNAGE (bien plus d'entrées
// qu'une carte ordinaire — soigner, dégâts, épuiser, statuts, compteurs…)
// ouvrait un menu dont le bas dépassait l'écran, SANS AUCUN MOYEN de
// l'atteindre (ni défilement, ni repositionnement). L'ancien calcul devinait
// une hauteur fixe de 340px, qui ne suffisait qu'aux petits menus (une carte
// ordinaire n'a que « Défausser » / « Retirer de la partie »).
//
// jsdom ne fait AUCUNE mise en page réelle : `getBoundingClientRect` y rend
// toujours des zéros. On le remplace donc, comme `geste.test.tsx` le fait
// pour `elementFromPoint` — c'est la seule chose simulée, tout le reste (le
// calcul de position, l'effet) est le vrai code.
describe('le menu contextuel reste dans l’écran', () => {
  const tailleEcran = (largeur: number, hauteur: number) => {
    Object.defineProperty(window, 'innerWidth', { configurable: true, value: largeur })
    Object.defineProperty(window, 'innerHeight', { configurable: true, value: hauteur })
  }

  it('⚠ LE CAS SIGNALÉ : un menu de PERSONNAGE, plus haut que l’écran, reste défilable plutôt qu’invisible', () => {
    tailleEcran(1600, 400)
    // Un menu de personnage, mesuré nettement plus haut que l'écran (comme
    // celui du signalement, ouvert tout en bas d'un écran de 400px de haut).
    vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({
      width: 224, height: 520, top: 0, left: 0, right: 224, bottom: 520, x: 0, y: 0,
      toJSON: () => ({}),
    })
    const cible = { id: 7, nom: 'Nathan Summers', estPersonnage: true }
    const { container } = render(
      <MenuTriche cible={cible} x={800} y={388} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} />
    )
    const boite = container.querySelector('.menu-triche') as HTMLElement
    // ⚠ LE CHIFFRE QUI DISCRIMINE. Avec une hauteur mesurée (520) plus grande
    // que l'écran (400), le menu ne peut matériellement PAS tenir entier :
    // le mieux qu'une position puisse faire est de le coller tout en haut
    // (top = la marge, 8px), pour laisser le PLUS de hauteur possible au
    // filet CSS (`max-height` + `overflow-y: auto`) qui rend le reste
    // atteignable en défilant. L'ancien calcul (deviner 340px de haut fixe)
    // rendait `top = 60` ici — une valeur qui semble raisonnable mais qui,
    // combinée à une hauteur RÉELLE de 520, laisse le bas du menu à 580,
    // à 180px sous un écran de 400 : invisible, et rien à l'époque pour le
    // faire défiler.
    expect(parseFloat(boite.style.top)).toBe(8)
    vi.restoreAllMocks()
  })

  it('un menu ordinaire, qui tient déjà dans l’écran, ne bouge pas du curseur', () => {
    tailleEcran(1600, 1000)
    vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({
      width: 224, height: 90, top: 0, left: 0, right: 224, bottom: 90, x: 0, y: 0,
      toJSON: () => ({}),
    })
    const { container } = render(
      <MenuTriche cible={CIBLE} x={300} y={300} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} />
    )
    const boite = container.querySelector('.menu-triche') as HTMLElement
    expect(parseFloat(boite.style.left)).toBe(300)
    expect(parseFloat(boite.style.top)).toBe(300)
    vi.restoreAllMocks()
  })

  it('un clic tout en bas à droite ramène le menu par la gauche ET par le haut', () => {
    tailleEcran(1000, 800)
    vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({
      width: 240, height: 300, top: 0, left: 0, right: 240, bottom: 300, x: 0, y: 0,
      toJSON: () => ({}),
    })
    const { container } = render(
      <MenuTriche cible={CIBLE} x={990} y={790} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} />
    )
    const boite = container.querySelector('.menu-triche') as HTMLElement
    // 990 + 240 (largeur) déborderait de 230px : ramené à 1000 - 240 - 8.
    expect(parseFloat(boite.style.left)).toBe(1000 - 240 - 8)
    // 790 + 300 (hauteur) déborderait de 490px : ramené à 800 - 300 - 8.
    expect(parseFloat(boite.style.top)).toBe(800 - 300 - 8)
    vi.restoreAllMocks()
  })
})

describe('« Ajouter des compteurs » n’est pas offert sur une carte en main', () => {
  it('offert sur une carte en jeu', () => {
    const { queryByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} manuel />
    )
    expect(queryByText('Ajouter des compteurs')).not.toBeNull()
  })

  it('absent sur une carte en main', () => {
    const { queryByText } = render(
      <MenuTriche cible={CIBLE} x={0} y={0} onFermer={vi.fn()} emettreGeste={emettreGesteDeTest()} manuel enMain />
    )
    expect(queryByText('Ajouter des compteurs')).toBeNull()
  })
})
