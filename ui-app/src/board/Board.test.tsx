// Le texte FR de repli ne doit apparaitre QUE la ou il manque un scan francais.
// Sur une carte deja en francais il ferait doublon avec l'image.
//
// Les cartes des packs FAN-MADE sont le cas qui compte le plus : elles n'auront
// jamais de scan francais ni de page marvelcdb, donc ce bloc est le seul
// francais que le joueur verra dessus.
import { act, fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { ApercuMarvelcdb, Board } from './Board'
import { catalogueVide } from './catalogue'
import { carteSurTable, siege, tableAvec } from './plateau-de-test'
import { CLE_SCANS_FR } from './scans-fr'
import { CODES_SCAN_FR } from './scans-fr-liste'
import { TEXTES_FR } from './textes-fr'
import { TEXTES_FR_FANMADE } from './textes-fr-fanmade'
import { construirePlateau, type Plateau } from './zones'
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

  it('un art alternatif (scan anglais) donne le texte francais meme si la carte a son scan FR', async () => {
    // Demande du 03/10/2026 : « les cartes alternatives sont en anglais ».
    render(<ApercuMarvelcdb codeCarte={AVEC_SCAN} artAlternatif />)
    expect(await screen.findByText(/Sens d'Araignée/)).toBeInTheDocument()
  })

  it('pas d art alternatif en scans anglais : rien de plus', () => {
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    const { container } = render(<ApercuMarvelcdb codeCarte={AVEC_SCAN} artAlternatif />)
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

// LE PLAFOND D'ECHELLE, ET CE QUI LE FIXE (revu le 14/09/2026).
//
// Il valait 1, en dur. Consequence mesuree : sur un ecran 2560x1440 le plateau
// disposait de 2560x1316 et dessinait quand meme des cartes de 127 px, toute la
// place en plus perdue, et le texte illisible. Le plafond vient desormais de la
// SOURCE D'IMAGE : 246 px de vignette pour une carte de 127 px a l'echelle 1,
// donc 246 / (127 * devicePixelRatio).
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `il ne descend jamais sous 1`. Sur un ecran a
// forte densite (dpr 2) la formule donne 0,97 : appliquee telle quelle, elle
// RETRECIRAIT la table par rapport a aujourd'hui. On ne degrade pas l'existant
// pour appliquer une regle.
describe('useEchelle : le plafond vient de la source d image', () => {
  beforeEach(() => {
    ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
  })

  const avecDpr = (dpr: number, faire: () => void) => {
    const avant = window.devicePixelRatio
    Object.defineProperty(window, 'devicePixelRatio', { value: dpr, configurable: true })
    try {
      faire()
    } finally {
      Object.defineProperty(window, 'devicePixelRatio', { value: avant, configurable: true })
    }
  }

  it('laisse la table GRANDIR sur un grand ecran ordinaire (dpr 1)', () => {
    // 246 / 127 = 1,94 : un ecran deux fois trop grand ne monte que jusque-la.
    avecDpr(1, () => {
      expect(mesurerEchelle(5120, 2160)).toBeCloseTo(1.94, 2)
    })
  })

  it('grandit jusqu au ratio de l ecran quand il est sous le plafond', () => {
    // 1920*1.6=3072, 940*1.6=1504 : ratio 1,6, en dessous de 1,94, donc garde.
    avecDpr(1, () => {
      expect(mesurerEchelle(3072, 1504)).toBeCloseTo(1.6, 2)
    })
  })

  it('⚠ ne RETRECIT jamais la table sur un ecran a forte densite', () => {
    // 246 / (127*2) = 0,97 : la formule seule ferait reculer l'existant.
    avecDpr(2, () => {
      expect(mesurerEchelle(5120, 2160)).toBe(1)
    })
  })

  it('laisse l echelle inchangee en dessous de 1 (table ordinaire)', () => {
    // 1920*0.67=1286.4, 940*0.67=629.8 : le plus petit ratio reste ~0.67.
    expect(mesurerEchelle(1286, 630)).toBeCloseTo(0.67, 2)
  })

  it('un petit ecran n est pas concerne par le plafond, quel que soit le dpr', () => {
    avecDpr(2, () => {
      expect(mesurerEchelle(1286, 630)).toBeCloseTo(0.67, 2)
    })
  })
})

// ALT OUVRE L'APERCU TOUT DE SUITE (tache 4 du plan mode manuel), sans
// attendre les ~200ms du survol normal. Convention Tabletop Simulator, et le
// seul raccourci qui ne change pas l'etat de la partie : il vaut donc en
// partie ordinaire aussi, pas seulement en mode manuel.
describe('Alt agrandit sans attendre le delai du survol', () => {
  beforeEach(() => {
    ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
  })

  function monterAvecUneCarte() {
    const monde = tableAvec(
      siege({ area_hero: [carteSurTable(1, '01001a', 'Hero', 'Spider-Man')] }),
      { phase: 'Player 1 Turn', round_id: 1, prompt: '' }
    )
    const plateau = construirePlateau(monde, { playerId: 0, catalogue: catalogueVide })
    const { container } = render(<Board world={monde} playerId={0} plateau={plateau} />)
    const carte = container.querySelector('[data-card-id="1"]') as HTMLElement
    return { container, carte }
  }

  it('ouvre l’apercu au keydown Alt, sans attendre le survol', () => {
    const { carte } = monterAvecUneCarte()
    act(() => {
      fireEvent.mouseOver(carte)
      fireEvent.keyDown(document, { key: 'Alt' })
    })
    expect(document.querySelector('.carte-apercu')).not.toBeNull()
  })

  it('referme l’apercu au keyup Alt', () => {
    const { carte } = monterAvecUneCarte()
    act(() => {
      fireEvent.mouseOver(carte)
      fireEvent.keyDown(document, { key: 'Alt' })
    })
    expect(document.querySelector('.carte-apercu')).not.toBeNull()
    act(() => {
      fireEvent.keyUp(document, { key: 'Alt' })
    })
    expect(document.querySelector('.carte-apercu')).toBeNull()
  })

  it('ne s’ouvre pas sans rien survoler', () => {
    monterAvecUneCarte()
    act(() => {
      fireEvent.keyDown(document, { key: 'Alt' })
    })
    expect(document.querySelector('.carte-apercu')).toBeNull()
  })

  it('ignore les autres touches', () => {
    const { carte } = monterAvecUneCarte()
    act(() => {
      fireEvent.mouseOver(carte)
      fireEvent.keyDown(document, { key: 'Shift' })
    })
    expect(document.querySelector('.carte-apercu')).toBeNull()
  })
})
