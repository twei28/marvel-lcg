// Le geste lui-meme, monte dans un vrai plateau.
//
// Ce que ces cas protegent, et qui ne se voit nulle part ailleurs :
//
//  1. LE CLIC SURVIT. C'est la condition posee au chantier : le glisser
//     s'ajoute, il ne remplace rien. Un appui suivi d'un relachement au meme
//     endroit doit rester un clic, et un lacher apres un vrai deplacement ne
//     doit PAS declencher le clic par-dessus (deux actions pour un geste).
//  2. Le seuil : quelques pixels de tremblement ne sont pas un glisser.
//  3. Le lacher passe bien la source ET la cible aux regles.
//
// ⚠ jsdom N'A PAS DE MISE EN PAGE : `elementFromPoint` y rend toujours `null`.
// On le remplace donc par une table « point -> carte » ecrite par le test.
// C'est la seule chose simulee ; tout le reste (les handlers, le seuil, la
// suppression du clic) est le vrai code.
import { readFileSync } from 'node:fs'
import { fireEvent, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { Board, type ReglagesGlisser } from '../Board'
import type { EtatInteractif } from '../interaction'
import type { ScanCardProps } from '../../components/ScanCard'
import type { Plateau } from '../zones'
import type { World } from '../world'

const HEROS = 1
const RHINO = 2

const MONDE = {
  phase: 'Player 1 Turn',
  round_id: 1,
  prompt: '',
  players: [],
} as unknown as World

function carte(id: number, name: string): ScanCardProps {
  return { id: String(id), name, kind: 'hero' } as ScanCardProps
}

const PLATEAU: Plateau = {
  emplacements: [
    {
      cle: 'terrain-combat',
      titre: 'Combat',
      nombreSurLaLigne: 2,
      groupes: [
        [
          { cle: 'u1', carte: carte(HEROS, 'Blade'), attachees: [] },
          { cle: 'u2', carte: carte(RHINO, 'Rhino'), attachees: [] },
        ],
      ],
    },
  ],
  nombreDeCartes: 2,
  idsAffiches: new Set([HEROS, RHINO]),
  representantsDePile: new Map(),
  nombreIgnore: 0,
}

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}

/** Fait repondre `elementFromPoint` : au-dela de x=100, on est sur Rhino. */
function poserLaTable(conteneur: HTMLElement) {
  const parId = (id: number) =>
    conteneur.querySelector<HTMLElement>(`.scan-card[data-card-id="${id}"]`)
  document.elementFromPoint = (x: number) => (x > 100 ? parId(RHINO) : parId(HEROS))
}

function reglages(surDepot: ReglagesGlisser['onDepot']): ReglagesGlisser {
  return {
    estSource: (id) => id === HEROS,
    ciblesLegales: () => new Set([RHINO]),
    zonesLegales: () => new Set<string>(),
    libelle: () => 'Attaque · Rhino',
    onDepot: surDepot,
  }
}

function monter(
  surDepot: ReglagesGlisser['onDepot'],
  surClic = vi.fn(),
  interactifs?: Map<number, EtatInteractif>
) {
  const rendu = render(
    <Board
      world={MONDE}
      playerId={0}
      plateau={PLATEAU}
      glisser={reglages(surDepot)}
      onCardClick={surClic}
      interactifs={interactifs}
    />
  )
  poserLaTable(rendu.container)
  const cadre = rendu.container.querySelector('.plateau-cadre') as HTMLElement
  const source = rendu.container.querySelector<HTMLElement>(`.scan-card[data-card-id="${HEROS}"]`)!
  return { ...rendu, cadre, source, surClic }
}

/**
 * Un evenement de pointeur qui porte VRAIMENT ses coordonnees.
 *
 * ⚠ DEUX PIEGES PAYES ICI, ET C'EST POURQUOI ON N'UTILISE PAS `fireEvent.pointerDown` :
 *
 *  1. ON EMET SUR LA CARTE, PAS SUR LE CADRE. Les handlers vivent sur le cadre
 *     et lisent `evenement.target` pour savoir quelle carte est prise ; un
 *     evenement emis sur le cadre a le CADRE pour cible, et le geste ne demarre
 *     jamais. La propagation fait le reste, comme un vrai clic.
 *  2. Sous jsdom, les raccourcis `pointerDown`/`pointerUp` de `fireEvent`
 *     PERDENT `clientX`/`clientY` (mesure du 08/09/2026 : seul `pointerMove`
 *     les conservait). Le seuil se calculait alors sur des zeros, et un simple
 *     tremblement passait pour un glisser. On construit donc un `MouseEvent`,
 *     que jsdom remplit correctement, et on lui donne le type d'un pointeur.
 */
function pointeur(cible: HTMLElement, type: string, x: number, y: number) {
  fireEvent(cible, new MouseEvent(type, { bubbles: true, cancelable: true, clientX: x, clientY: y }))
}

/** Un geste complet : appuyer sur la source, aller en (x, y), relacher. */
function glisser(source: HTMLElement, x: number, y = 0) {
  pointeur(source, 'pointerdown', 0, 0)
  pointeur(source, 'pointermove', x, y)
  pointeur(source, 'pointerup', x, y)
}

beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
  // Element.setPointerCapture n'existe pas dans jsdom : le code l'appelle sous
  // try/catch, mais autant que le test ne compte pas sur une exception.
  Element.prototype.setPointerCapture = function () {}
  Element.prototype.releasePointerCapture = function () {}
})

describe('le geste', () => {
  // Le lacher rapporte la carte ET la zone qui la contient : une carte est
  // toujours DANS une zone. C'est aux regles de trancher, et elles preferent la
  // carte (voir `onDepot` dans board.tsx) ; la zone ne sert qu'aux cartes
  // lachees a cote, celles qui ne visent personne.
  it('lacher sur une carte passe la source, la cible et sa zone aux regles', () => {
    const surDepot = vi.fn(() => undefined)
    const { source } = monter(surDepot)
    glisser(source, 300)
    expect(surDepot).toHaveBeenCalledWith(HEROS, { carteId: RHINO, zone: 'terrain-combat', surLaTable: true })
  })

  // ⚠ LE CAS QUI COMPTE. Sans la garde posee sur `onPointerUp`, le lacher
  // declencherait AUSSI le clic sous le pointeur : deux actions pour un geste.
  it('un lacher ne declenche pas le clic par-dessus', () => {
    const surClic = vi.fn()
    const { source } = monter(vi.fn(() => undefined), surClic)
    glisser(source, 300)
    expect(surClic).not.toHaveBeenCalled()
  })

  it('un appui sans deplacement reste un clic', () => {
    const surDepot = vi.fn(() => undefined)
    const surClic = vi.fn()
    const { source } = monter(surDepot, surClic)
    pointeur(source, 'pointerdown', 40, 40)
    pointeur(source, 'pointerup', 40, 40)
    expect(surDepot).not.toHaveBeenCalled()
    expect(surClic).toHaveBeenCalledTimes(1)
  })

  it('un tremblement sous le seuil reste un clic', () => {
    const surDepot = vi.fn(() => undefined)
    const surClic = vi.fn()
    const { source } = monter(surDepot, surClic)
    pointeur(source, 'pointerdown', 40, 40)
    pointeur(source, 'pointermove', 43, 41)
    pointeur(source, 'pointerup', 43, 41)
    expect(surDepot).not.toHaveBeenCalled()
    expect(surClic).toHaveBeenCalledTimes(1)
  })

  it('une carte qui n est pas une source ne se souleve pas', () => {
    const surDepot = vi.fn(() => undefined)
    const rendu = monter(surDepot)
    const rhino = rendu.container.querySelector<HTMLElement>(`.scan-card[data-card-id="${RHINO}"]`)!
    pointeur(rhino, 'pointerdown', 0, 0)
    pointeur(rhino, 'pointermove', 300, 0)
    pointeur(rhino, 'pointerup', 300, 0)
    expect(surDepot).not.toHaveBeenCalled()
  })
})

describe('ce que le geste montre', () => {
  it('le cadre se marque pendant le geste, et se demarque apres', () => {
    const { source, container } = monter(vi.fn(() => undefined))
    pointeur(source, 'pointerdown', 0, 0)
    pointeur(source, 'pointermove', 300, 0)
    expect(container.querySelector('.plateau-cadre.est-en-glisser')).not.toBeNull()
    expect(container.querySelector('.couche-glisser')).not.toBeNull()
    pointeur(source, 'pointerup', 300, 0)
    expect(container.querySelector('.plateau-cadre.est-en-glisser')).toBeNull()
    expect(container.querySelector('.couche-glisser')).toBeNull()
  })

  it('la cible legale s allume pendant le geste', () => {
    const { source, container } = monter(vi.fn(() => undefined))
    pointeur(source, 'pointerdown', 0, 0)
    pointeur(source, 'pointermove', 300, 0)
    const rhino = container.querySelector(`.scan-card[data-card-id="${RHINO}"]`)
    expect(rhino?.className).toMatch(/is-target-pulse|state-targetable/)
  })

  // ⚠ TEMOIN DU REFUS. La bulle ne doit apparaitre QUE quand les regles rendent
  // une raison : un lacher reussi ne dit rien.
  it('le refus rendu par les regles s affiche en bulle', () => {
    const { source, container } = monter(() => 'Un Gardien vous en empeche')
    glisser(source, 300)
    expect(container.querySelector('.glisser-refus')?.textContent).toBe('Un Gardien vous en empeche')
  })

  // Lot 2 du 06/10/2026 : lâchée près du bord gauche de l'écran, la bulle
  // (centrée sur le point du lâcher) sortait à moitié de l'écran et le refus
  // devenait illisible (capture lot2-1280-06). Elle reste dans l'écran.
  it('la bulle de refus reste dans l’écran, même lâchée au bord', () => {
    const { source, container } = monter(() => 'Une ressource se défausse pour payer')
    glisser(source, 300, 0)
    const bulle = container.querySelector<HTMLElement>('.glisser-refus')!
    expect(bulle.style.getPropertyValue('--refus-x')).toBe('300px')
    expect(bulle.style.getPropertyValue('--refus-y')).toBe('0px')
    const css = readFileSync('src/board/glisser/glisser.css', 'utf-8')
    expect(css).toContain('left: clamp(160px, var(--refus-x), calc(100vw - 160px));')
    expect(css).toContain('top: max(64px, var(--refus-y));')
  })

  // Lot 6 du 06/10/2026 : un lecteur d'écran annonce le refus.
  it('la bulle de refus est annoncée (role status, hors aria-hidden)', () => {
    const { source, container } = monter(() => 'Un Gardien vous en empeche')
    glisser(source, 300)
    const bulle = container.querySelector<HTMLElement>('.glisser-refus')!
    expect(bulle.getAttribute('role')).toBe('status')
    expect(bulle.closest('[aria-hidden="true"]')).toBeNull()
  })

  it('un lacher accepte n affiche aucune bulle', () => {
    const { source, container } = monter(vi.fn(() => undefined))
    glisser(source, 300)
    expect(container.querySelector('.glisser-refus')).toBeNull()
  })

  // ⚠ LE CAS QUI COMPTE POUR LE « BLEU », ET C'EST LE VRAI. Bouton enfonce, le
  // navigateur selectionne ce que le pointeur balaie et le peint en bleu. Le
  // cadre est desormais `user-select: none` (glisser.css), mais la selection a
  // pu commencer pendant les six pixels du seuil : le geste l'efface une fois,
  // au moment ou il se reconnait. Sans cet effacement, le bleu reste affiche
  // pendant tout le glisser.
  it('le depart du geste efface la selection du navigateur', () => {
    const vider = vi.fn()
    const vraiGetSelection = window.getSelection
    window.getSelection = () => ({ removeAllRanges: vider }) as unknown as Selection
    try {
      const { source } = monter(vi.fn(() => undefined))
      pointeur(source, 'pointerdown', 0, 0)
      expect(vider).not.toHaveBeenCalled()   // pas encore : c'est peut-etre un clic
      pointeur(source, 'pointermove', 300, 0)
      expect(vider).toHaveBeenCalledTimes(1)
    } finally {
      window.getSelection = vraiGetSelection
    }
  })

  // ⚠ LE CAS QUI COMPTE POUR LA COULEUR, ET IL VIENT DE DEUX SIGNALEMENTS
  // (08/09/2026, « ce halo bleu degueulasse »). Une carte deja marquee
  // `choisie` par une action en cours garde l'etat `selected`, dont le halo
  // est BLEU. Le geste doit lui rendre la couleur des cibles, la doree :
  // sinon une meme rangee melange deux couleurs et rien ne se comprend.
  it('une cible deja choisie ailleurs ne reste pas bleue', () => {
    const dejaChoisie = new Map<number, EtatInteractif>([
      [RHINO, { role: 'cible', choisie: true, pulse: false } as EtatInteractif],
    ])
    const { source, container } = monter(vi.fn(() => undefined), vi.fn(), dejaChoisie)
    pointeur(source, 'pointerdown', 0, 0)
    pointeur(source, 'pointermove', 300, 0)
    const rhino = container.querySelector(`.scan-card[data-card-id="${RHINO}"]`)!
    expect(rhino.className).not.toMatch(/state-selected/)
    expect(rhino.className).toMatch(/state-targetable|is-target-pulse/)
  })

  it('sans reglages, le plateau se comporte comme avant', () => {
    const surClic = vi.fn()
    const { container } = render(
      <Board world={MONDE} playerId={0} plateau={PLATEAU} onCardClick={surClic} />
    )
    const cadre = container.querySelector('.plateau-cadre') as HTMLElement
    const source = container.querySelector<HTMLElement>(`.scan-card[data-card-id="${HEROS}"]`)!
    pointeur(source, 'pointerdown', 0, 0)
    pointeur(source, 'pointermove', 300, 0)
    pointeur(source, 'pointerup', 300, 0)
    expect(container.querySelector('.est-en-glisser')).toBeNull()
    expect(surClic).toHaveBeenCalledTimes(1)
  })

  // Lot 2 du 06/10/2026 (mode manuel, question 12) : tout ce qui accepte la
  // carte s'entoure, la table d'un seul cadre et les piles fines ; et le rouge
  // ne s'affiche que si le lâcher sera VRAIMENT refusé (`accepte`).
  it('en manuel, la table et la pile qui accueillent la carte s’entourent, sans rouge', () => {
    const avecPile: Plateau = {
      ...PLATEAU,
      emplacements: [
        ...PLATEAU.emplacements,
        {
          cle: 'piles-joueur',
          titre: 'Piles',
          nombreSurLaLigne: 1,
          groupes: [[{ cle: 'u3', carte: carte(3, 'Deck'), attachees: [], pile: 'joueur-deck' }]],
        },
      ],
    }
    const manuel: ReglagesGlisser = {
      estSource: () => true,
      ciblesLegales: () => new Set<number>(),
      zonesLegales: () => new Set(['joueur-deck']),
      libelle: () => 'Poser en jeu : Blade (Alliés)',
      accepte: () => true,
      accueilleLaTable: () => true,
      onDepot: () => undefined,
    }
    const { container } = render(
      <Board world={MONDE} playerId={0} plateau={avecPile} glisser={manuel} onCardClick={vi.fn()} />
    )
    poserLaTable(container)
    const source = container.querySelector<HTMLElement>(`.scan-card[data-card-id="${HEROS}"]`)!
    pointeur(source, 'pointerdown', 0, 0)
    pointeur(source, 'pointermove', 300, 0)
    const cadre = container.querySelector('.plateau-cadre') as HTMLElement
    expect(cadre.hasAttribute('data-table-accueille')).toBe(true)
    expect(container.querySelector('.plateau-unite[data-pile="joueur-deck"]')?.hasAttribute('data-pile-accueille')).toBe(true)
    expect(container.querySelector('.glisser-etiquette.est-refuse')).toBeNull()
  })

  it('en manuel, un lâcher que les règles refusent vire au rouge', () => {
    const manuel: ReglagesGlisser = {
      estSource: () => true,
      ciblesLegales: () => new Set<number>(),
      zonesLegales: () => new Set<string>(),
      libelle: () => undefined,
      accepte: () => false,
      accueilleLaTable: () => false,
      onDepot: () => 'non',
    }
    const { container } = render(
      <Board world={MONDE} playerId={0} plateau={PLATEAU} glisser={manuel} onCardClick={vi.fn()} />
    )
    poserLaTable(container)
    const source = container.querySelector<HTMLElement>(`.scan-card[data-card-id="${HEROS}"]`)!
    pointeur(source, 'pointerdown', 0, 0)
    pointeur(source, 'pointermove', 300, 0)
    expect((container.querySelector('.plateau-cadre') as HTMLElement).hasAttribute('data-table-accueille')).toBe(false)
    expect(container.querySelector('.est-refuse')).not.toBeNull()
  })
})

// Lot 4 du 06/10/2026 (question 11) : au doigt, une carte doit pouvoir se
// glisser sans que la page défile. Le cadre l'annonce, le CSS coupe le
// défilement tactile sur les seules cartes.
describe('au doigt, en manuel', () => {
  it('le cadre annonce un glisser au doigt quand les réglages le demandent', () => {
    const manuel: ReglagesGlisser = {
      estSource: () => true,
      ciblesLegales: () => new Set<number>(),
      zonesLegales: () => new Set<string>(),
      libelle: () => undefined,
      auDoigt: true,
      onDepot: () => undefined,
    }
    const { container } = render(
      <Board world={MONDE} playerId={0} plateau={PLATEAU} glisser={manuel} onCardClick={vi.fn()} />
    )
    expect((container.querySelector('.plateau-cadre') as HTMLElement).hasAttribute('data-glisser-doigt')).toBe(true)
  })

  it('hors manuel, le doigt garde le défilement de la page', () => {
    const { container } = render(<Board world={MONDE} playerId={0} plateau={PLATEAU} onCardClick={vi.fn()} />)
    expect((container.querySelector('.plateau-cadre') as HTMLElement).hasAttribute('data-glisser-doigt')).toBe(false)
  })

  it('le CSS coupe le défilement tactile sur les cartes seulement', () => {
    const css = readFileSync('src/board/glisser/glisser.css', 'utf-8')
    expect(css).toMatch(/\.plateau-cadre\[data-glisser-doigt\] \.scan-card \{\s*touch-action: none;/)
  })
})

// Lot 5 du 06/10/2026 (question 6) : chaque groupe dit à quel siège il
// appartient, pour qu'une carte lâchée dedans arrive chez ce joueur.
describe('le siège de chaque groupe', () => {
  it('un groupe avec propriétaire porte data-joueur, un groupe sans n’en porte pas', () => {
    const avecProprietaires: Plateau = {
      ...PLATEAU,
      emplacements: [
        {
          cle: 'terrain-combat',
          titre: 'Combat',
          nombreSurLaLigne: 2,
          groupes: [
            [{ cle: 'u1', carte: carte(HEROS, 'Blade'), attachees: [] }],
            [{ cle: 'u2', carte: carte(RHINO, 'Rhino'), attachees: [] }],
          ],
          proprietaires: [1, undefined],
        },
      ],
    }
    const { container } = render(
      <Board world={MONDE} playerId={0} plateau={avecProprietaires} onCardClick={vi.fn()} />
    )
    const groupes = container.querySelectorAll<HTMLElement>('.plateau-groupe')
    expect(groupes[0].dataset.joueur).toBe('1')
    expect(groupes[1].hasAttribute('data-joueur')).toBe(false)
  })
})

// Écart 32 de la spec du 06/10/2026 : comme sur OCTGN, saisir une pile prend
// sa carte du DESSUS (celle que la pile montre, `card-model.ts`, `toPileCard`).
describe('glisser depuis une pile', () => {
  const DESSUS = 7
  const PLATEAU_AVEC_PILE: Plateau = {
    ...PLATEAU,
    emplacements: [
      ...PLATEAU.emplacements,
      {
        cle: 'piles-joueur',
        titre: 'Deck',
        nombreSurLaLigne: 1,
        groupes: [
          [
            {
              cle: 'joueur-deck',
              carte: carte(DESSUS, 'Dessus du deck'),
              attachees: [],
              pile: 'joueur-deck',
              pileTitre: 'Deck',
              pileContenu: [carte(DESSUS, 'Dessus du deck')],
            },
          ],
        ],
      },
    ],
    idsAffiches: new Set([HEROS, RHINO, DESSUS]),
  }

  it('la carte du dessus se soulève et se lâche ailleurs', () => {
    const surDepot = vi.fn(() => undefined)
    const rendu = render(
      <Board
        world={MONDE}
        playerId={0}
        plateau={PLATEAU_AVEC_PILE}
        glisser={{ ...reglages(surDepot), estSource: () => true }}
        onCardClick={vi.fn()}
      />
    )
    poserLaTable(rendu.container)
    const dessus = rendu.container.querySelector<HTMLElement>(`.scan-card[data-card-id="${DESSUS}"]`)!
    glisser(dessus, 300)
    expect(surDepot).toHaveBeenCalledWith(DESSUS, expect.objectContaining({ carteId: RHINO }))
  })
})
