// Le texte FR de repli ne doit apparaitre QUE la ou il manque un scan francais.
// Sur une carte deja en francais il ferait doublon avec l'image.
//
// Les cartes des packs FAN-MADE sont le cas qui compte le plus : elles n'auront
// jamais de scan francais ni de page marvelcdb, donc ce bloc est le seul
// francais que le joueur verra dessus.
import { act, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { ApercuMarvelcdb, Board } from './Board'
import { CLE_SCANS_FR } from './scans-fr'
import { CODES_SCAN_FR } from './scans-fr-liste'
import { TEXTES_FR } from './textes-fr'
import { TEXTES_FR_FANMADE } from './textes-fr-fanmade'
import type { Plateau } from './zones'
import type { World } from './world'

const AVEC_SCAN = '01001a'
const SANS_SCAN = '01043b'
const FANMADE = 'sg001a'
/** Code au bon format, absent des deux dictionnaires : rien ne doit s'afficher. */
const INCONNU = '99999'

beforeEach(() => {
  window.localStorage.clear()
  ;(CODES_SCAN_FR as Set<string>).clear()
  ;(CODES_SCAN_FR as Set<string>).add(AVEC_SCAN)
  ;(TEXTES_FR as Record<string, string | undefined>)[SANS_SCAN] = 'Action de héros de repli'
})

describe('ApercuMarvelcdb', () => {
  it('affiche le texte francais quand la carte n a pas de scan francais', () => {
    render(<ApercuMarvelcdb codeCarte={SANS_SCAN} />)
    expect(screen.getByText(/Action de héros de repli/)).toBeInTheDocument()
  })

  it('n affiche rien quand la carte a deja son scan francais', () => {
    render(<ApercuMarvelcdb codeCarte={AVEC_SCAN} />)
    expect(screen.queryByText(/Action de héros de repli/)).not.toBeInTheDocument()
  })

  it('n affiche rien quand l option scans FR est coupee', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    render(<ApercuMarvelcdb codeCarte={SANS_SCAN} />)
    expect(screen.queryByText(/Action de héros de repli/)).not.toBeInTheDocument()
  })

  it('n affiche rien pour une carte inconnue des deux dictionnaires', () => {
    const { container } = render(<ApercuMarvelcdb codeCarte={INCONNU} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('affiche le texte francais traduit a la main d une carte fan-made', () => {
    expect(TEXTES_FR_FANMADE[FANMADE]).toBeDefined()
    render(<ApercuMarvelcdb codeCarte={FANMADE} />)
    expect(screen.getByText(/Armée imbattable/)).toBeInTheDocument()
  })

  it('ne montre aucune carte fan-made quand l option est coupee', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    const { container } = render(<ApercuMarvelcdb codeCarte={FANMADE} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('rend les sauts de ligne visibles au lieu de coller les capacites', () => {
    ;(TEXTES_FR as Record<string, string | undefined>)[SANS_SCAN] =
      'Première capacité.\nSeconde capacité.'
    const { container } = render(<ApercuMarvelcdb codeCarte={SANS_SCAN} />)
    expect(container.querySelectorAll('br')).toHaveLength(1)
  })
})

// jsdom n'implemente pas ResizeObserver : useEchelle en observe le cadre pour
// recalculer --echelle. Ce bouchon capture le callback pour le declencher a la
// main, avec une taille de cadre choisie par le test.
class ResizeObserverBouchon {
  static derniere: ResizeObserverBouchon | undefined
  constructor(public readonly callback: ResizeObserverCallback) {
    ResizeObserverBouchon.derniere = this
  }
  observe() {}
  unobserve() {}
  disconnect() {}
}

const MONDE_VIDE = {
  phase: 'Player 1 Turn',
  round_id: 1,
  prompt: '',
  players: [],
} as unknown as World

const PLATEAU_VIDE: Plateau = {
  emplacements: [],
  nombreDeCartes: 0,
  idsAffiches: new Set(),
  representantsDePile: new Map(),
  nombreIgnore: 0,
}

/** Rend le plateau, simule un cadre de la taille donnee, et lit --echelle. */
function mesurerEchelle(largeur: number, hauteur: number): number {
  const { container } = render(<Board world={MONDE_VIDE} playerId={1} plateau={PLATEAU_VIDE} />)
  const cadre = container.querySelector('.plateau-cadre') as HTMLElement
  cadre.getBoundingClientRect = () => ({ width: largeur, height: hauteur }) as DOMRect
  act(() => {
    ResizeObserverBouchon.derniere?.callback([], ResizeObserverBouchon.derniere as unknown as ResizeObserver)
  })
  const scene = container.querySelector('.plateau-scene') as HTMLElement
  return Number(scene.style.getPropertyValue('--echelle'))
}

describe('useEchelle : plafond a 1', () => {
  beforeEach(() => {
    ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
  })

  it('plafonne l echelle a 1 sur un tres grand ecran (5120x2160, ratio brut ~2,3)', () => {
    expect(mesurerEchelle(5120, 2160)).toBe(1)
  })

  it('plafonne aussi a une echelle brute de 1,6 (ecran juste plus grand que la scene)', () => {
    // 1920*1.6=3072, 940*1.6=1504 : ratio brut = 1.6, doit retomber a 1.
    expect(mesurerEchelle(3072, 1504)).toBe(1)
  })

  it('laisse l echelle inchangee en dessous de 1 (table ordinaire)', () => {
    // 1920*0.67=1286.4, 940*0.67=629.8 : le plus petit ratio reste ~0.67.
    expect(mesurerEchelle(1286, 630)).toBeCloseTo(0.67, 2)
  })
})
