// Alt + glisser, monte dans un vrai plateau. jsdom n'a pas de mise en page :
// on ecrit les rectangles des cartes (seule chose simulee).
import { fireEvent, render } from '@testing-library/react'

import { beforeAll, describe, expect, it } from 'vitest'
import { Board } from '../Board'
import type { ScanCardProps } from '../../components/ScanCard'
import type { Plateau } from '../zones'
import type { World } from '../world'

const MONDE = { phase: 'Player 1 Turn', round_id: 1, prompt: '', players: [] } as unknown as World

const carte = (id: number, name: string, kind = 'ally'): ScanCardProps =>
  ({ id: String(id), name, kind }) as ScanCardProps

const PLATEAU: Plateau = {
  emplacements: [
    {
      cle: 'terrain-combat',
      titre: 'Combat',
      nombreSurLaLigne: 3,
      groupes: [
        [
          { cle: 'u1', carte: carte(1, 'Alpha'), attachees: [] },
          { cle: 'u2', carte: carte(2, 'Beta'), attachees: [] },
          {
            cle: 'u3',
            carte: carte(3, 'Gamma'),
            attachees: [carte(31, 'Up A', 'upgrade'), carte(32, 'Up B', 'upgrade')],
          },
        ],
      ],
    },
  ],
  idsAffiches: new Set<number>(),
  nombreIgnore: 0,
} as unknown as Plateau

beforeAll(() => {
  Element.prototype.setPointerCapture = function () {}
  Element.prototype.releasePointerCapture = function () {}
  globalThis.ResizeObserver ??= class {
    observe() {}
    unobserve() {}
    disconnect() {}
  } as unknown as typeof ResizeObserver
})

function monter(partieId?: string) {
  const rendu = render(<Board world={MONDE} playerId={0} plateau={PLATEAU} identitePartie={partieId} />)
  // Chaque carte occupe 100 px de large, cote a cote ; les ameliorations sont
  // empilees verticalement a droite de leur porteur.
  const posX = new Map<string, number>([['1', 0], ['2', 100], ['3', 200], ['31', 320], ['32', 320]])
  const posY = new Map<string, number>([['31', 0], ['32', 120]])
  for (const el of rendu.container.querySelectorAll<HTMLElement>('.scan-card')) {
    const id = el.dataset.cardId ?? ''
    const x = posX.get(id) ?? 0
    const y = posY.get(id) ?? 0
    el.getBoundingClientRect = () =>
      ({ left: x, right: x + 100, top: y, bottom: y + 100, width: 100, height: 100 }) as DOMRect
  }
  return rendu
}

const ordre = (conteneur: HTMLElement) =>
  [...conteneur.querySelectorAll<HTMLElement>('.plateau-groupe > .plateau-unite > .scan-card')].map(
    (c) => c.dataset.cardId
  )
const pile = (conteneur: HTMLElement) =>
  [...conteneur.querySelectorAll<HTMLElement>('.est-attachee > .scan-card')].map((c) => c.dataset.cardId)

// Voir geste.test.tsx : `fireEvent.pointerDown` perd les coordonnees sous jsdom.
function pointeur(cible: HTMLElement, type: string, x: number, y: number, alt = true) {
  fireEvent(cible, new MouseEvent(type, { bubbles: true, cancelable: true, clientX: x, clientY: y, altKey: alt }))
}

function glisser(_cadre: HTMLElement, depuis: HTMLElement, vers: { x: number; y: number }, alt = true) {
  pointeur(depuis, 'pointerdown', 50, 50, alt)
  pointeur(depuis, 'pointermove', vers.x, vers.y, alt)
  pointeur(depuis, 'pointerup', vers.x, vers.y, alt)
}

describe('ranger les cartes avec Alt + glisser', () => {
  it('une carte change de place dans sa rangee et le repere apparait pendant le geste', () => {
    const { container } = monter()
    const gamma = container.querySelector<HTMLElement>('[data-card-id="3"]')!
    expect(ordre(container)).toEqual(['1', '2', '3'])
    pointeur(gamma, 'pointerdown', 250, 50)
    pointeur(gamma, 'pointermove', 20, 50)
    expect(document.querySelector('.ordre-repere')).not.toBeNull()
    pointeur(gamma, 'pointerup', 20, 50)
    expect(document.querySelector('.ordre-repere')).toBeNull()
    expect(ordre(container)).toEqual(['3', '1', '2'])
  })

  it('sans Alt, rien ne bouge', () => {
    const { container } = monter()
    glisser(container, container.querySelector<HTMLElement>('[data-card-id="3"]')!, { x: 20, y: 50 }, false)
    expect(ordre(container)).toEqual(['1', '2', '3'])
  })

  it('un simple Alt + clic, sans deplacer, ne change rien', () => {
    const { container } = monter()
    const gamma = container.querySelector<HTMLElement>('[data-card-id="3"]')!
    glisser(container, gamma, { x: 51, y: 50 })
    expect(ordre(container)).toEqual(['1', '2', '3'])
  })

  it('les ameliorations d une carte se rangent entre elles', () => {
    const { container } = monter()
    expect(pile(container)).toEqual(['31', '32'])
    glisser(container, container.querySelector<HTMLElement>('[data-card-id="32"]')!, { x: 340, y: -20 })
    expect(pile(container)).toEqual(['32', '31'])
  })

  it('l ordre survit a un rechargement de la meme partie, pas a une autre', () => {
    window.sessionStorage.clear()
    const premier = monter('partie-1')
    glisser(premier.container, premier.container.querySelector<HTMLElement>('[data-card-id="3"]')!, { x: 20, y: 50 })
    expect(ordre(premier.container)).toEqual(['3', '1', '2'])
    premier.unmount()
    const recharge = monter('partie-1')
    expect(ordre(recharge.container)).toEqual(['3', '1', '2'])
    recharge.unmount()
    expect(ordre(monter('partie-2').container)).toEqual(['1', '2', '3'])
  })
})
