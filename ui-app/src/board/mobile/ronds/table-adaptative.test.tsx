// La table en ronds ADAPTATIVE (26/10/2026) : TableRonds mesure son conteneur (`.portrait-table`), demande la disposition a
// `calculerDisposition` et la pose en style (diametre, largeur et colonnes de chaque zone). jsdom n'a pas de mise en page : on
// simule la taille du conteneur et on observe ce que le composant en fait. Le rendu reel est prouve dans Chromium (garde ui-check).
import { render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../../../components/ScanCard'
import type { UniteAffichee } from '../../zones'
import type { BandesPortrait } from '../bandes-portrait'
import { CLES_TELEPHONE } from '../reglages-telephone'
import type { DecorRonds } from './Rond'
import { TableRonds } from './TableRonds'

const carte = (id: string, kind: ScanCardProps['kind'], reste: Partial<ScanCardProps> = {}): ScanCardProps => ({
  id,
  name: `Carte ${id}`,
  kind,
  imageUrl: `/scan/${id}.jpg`,
  ...reste,
})
const unite = (id: string, kind: ScanCardProps['kind'], attachees: ScanCardProps[] = []): UniteAffichee => ({ cle: `u-${id}`, carte: carte(id, kind), attachees })
const plusieurs = (prefixe: string, kind: ScanCardProps['kind'], n: number): UniteAffichee[] =>
  Array.from({ length: n }, (_, i) => unite(`${prefixe}${i}`, kind))
const bandes = (reste: Partial<BandesPortrait> = {}): BandesPortrait => ({
  vilain: { epinglee: unite('rhino', 'villain'), unites: [] },
  manigances: { epinglee: unite('effraction', 'main-scheme'), unites: [unite('annexe', 'side-scheme')] },
  engages: { unites: [] },
  heros: { epinglee: unite('spidey', 'hero'), unites: [] },
  soutiens: { unites: [] },
  ameliorations: { unites: [] },
  main: [],
  piles: [],
  ...reste,
})
const decor = (): DecorRonds => ({ interactifs: new Map(), effets: new Map(), ouvrirPile: vi.fn(), ouvrirCarte: vi.fn(), agir: vi.fn() })

/** La capture de l'utilisateur : 1 allie, 2 sbires, 5 cartes en jeu. */
const plateauCapture = () =>
  bandes({
    heros: { epinglee: unite('spidey', 'hero'), unites: plusieurs('allie', 'ally', 1) },
    engages: { unites: plusieurs('sbire', 'minion', 2) },
    soutiens: { unites: plusieurs('soutien', 'support', 2) },
    ameliorations: { unites: plusieurs('amelio', 'upgrade', 3) },
  })

let largeur = 412
let hauteur = 560
let contenu = 400 // scrollHeight du conteneur

class ObservateurFactice {
  constructor(private cb: () => void) {}
  observe() {
    this.cb()
  }
  disconnect() {}
  unobserve() {}
}

beforeEach(() => {
  largeur = 412
  hauteur = 560
  contenu = 400
  window.localStorage.clear()
  vi.stubGlobal('ResizeObserver', ObservateurFactice)
  vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockImplementation(() => largeur)
  vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockImplementation(() => hauteur)
  vi.spyOn(HTMLElement.prototype, 'scrollHeight', 'get').mockImplementation(() => contenu)
})
afterEach(() => {
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

function table(b: BandesPortrait) {
  const { container } = render(
    <div className="portrait-table">
      <TableRonds bandes={b} decor={decor()} />
    </div>,
  )
  const racine = container.querySelector<HTMLElement>('.table-ronds')!
  const zone = (cle: string) => container.querySelector<HTMLElement>(`[data-zone="${cle}"]`)!
  return { racine, zone, container }
}

describe('la table en ronds mesure son conteneur', () => {
  it('capture de l\'utilisateur (1 allie, 2 sbires, 5 cartes en jeu) a 412 px : ronds de 62 px, colonnes 1 / 2 / 4', () => {
    hauteur = 900 // la largeur seule decide
    const { racine, zone } = table(plateauCapture())
    expect(racine.classList.contains('est-adaptative')).toBe(true)
    expect(racine.style.getPropertyValue('--d')).toBe('62px')
    expect(zone('allies').dataset.colonnes).toBe('1')
    expect(zone('sbires').dataset.colonnes).toBe('2')
    expect(zone('enJeu').dataset.colonnes).toBe('4')
    expect(zone('manigances').dataset.colonnes).toBe('2')
    expect(zone('vilain').dataset.colonnes).toBe('1')
  })

  it('la largeur de chaque zone est posee en px et les deux zones d\'une rangee remplissent la rangee', () => {
    const { container } = table(plateauCapture())
    for (const rangee of Array.from(container.querySelectorAll<HTMLElement>('.ronds-rangee'))) {
      const zones = Array.from(rangee.querySelectorAll<HTMLElement>(':scope > .ronds-zone'))
      expect(zones).toHaveLength(2)
      const somme = zones.reduce((s, z) => s + parseFloat(z.style.width), 0)
      expect(somme + 17).toBeCloseTo(412 - 20, 0)
    }
  })

  it('a 360 px les ronds rapetissent (52 px) et rien ne deborde', () => {
    largeur = 360
    hauteur = 900
    const { racine } = table(plateauCapture())
    expect(racine.style.getPropertyValue('--d')).toBe('52px')
  })

  it('une zone vide se reduit a un bandeau et la voisine prend sa place', () => {
    const { zone } = table(bandes({ engages: { unites: plusieurs('sbire', 'minion', 3) } }))
    expect(zone('allies').classList.contains('est-vide')).toBe(true)
    expect(zone('allies').dataset.colonnes).toBe('0')
    expect(parseFloat(zone('allies').style.width)).toBeLessThanOrEqual(80)
    expect(parseFloat(zone('sbires').style.width)).toBeGreaterThan(250)
  })

  it('le reglage des colonnes (Sbires 1) est respecte', () => {
    window.localStorage.setItem(CLES_TELEPHONE.colonnesZones, '3,3,1,4')
    const { zone } = table(bandes({ engages: { unites: plusieurs('sbire', 'minion', 3) } }))
    expect(zone('sbires').dataset.colonnes).toBe('1')
  })

  it('les ronds rapetissent encore tant que le contenu depasse la hauteur du conteneur, jusqu\'a 44 px', () => {
    contenu = 2000 // le conteneur ne peut jamais contenir : l'ecran defile
    const { racine } = table(plateauCapture())
    expect(racine.style.getPropertyValue('--d')).toBe('44px')
  })

  it('sans mesure (conteneur de largeur nulle) : on retombe sur le CSS d\'origine, sans style en ligne', () => {
    largeur = 0
    const { racine, zone } = table(plateauCapture())
    expect(racine.classList.contains('est-adaptative')).toBe(false)
    expect(racine.style.getPropertyValue('--d')).toBe('')
    expect(zone('sbires').style.width).toBe('')
  })

  it('en dessous de 54 px, les stats des ronds sont masquees (classe ronds-petits)', () => {
    largeur = 340
    contenu = 2000
    const { racine } = table(plateauCapture())
    expect(racine.classList.contains('ronds-petits')).toBe(true)
  })
})
