// RÉGRESSION. Le plateau a DEUX rendus, et le placement doit marcher sur les
// deux : sur PC une carte est une `.scan-card`, en mode mobile c'est un
// `.medaillon`. Même attribut `data-card-id`, balise différente.
//
// La première version visait `.scan-card[data-card-id]`. Vérifiée en jouant, la
// disposition mobile ne renvoyait AUCUNE carte : les panneaux y retombaient sur
// leur position par défaut — celle qui recouvre les cartes — sans le moindre
// signe d'erreur. C'est le pire des échecs, celui qui a l'air de fonctionner.
import { afterEach, describe, expect, it } from 'vitest'
import { boitesDesCartes, boitesDesPanneaux } from './boites'

/** jsdom rend tout à 0x0 : on impose des dimensions mesurables. */
function poser(html: string, rect: { x: number; y: number; w: number; h: number }): HTMLElement {
  const hote = document.createElement('div')
  hote.innerHTML = html
  const el = hote.firstElementChild as HTMLElement
  el.getBoundingClientRect = () =>
    ({ left: rect.x, top: rect.y, width: rect.w, height: rect.h, right: 0, bottom: 0, x: 0, y: 0, toJSON: () => ({}) }) as DOMRect
  document.body.append(el)
  return el
}

afterEach(() => {
  document.body.innerHTML = ''
})

describe('boitesDesCartes', () => {
  it('trouve une carte du plateau PC (.scan-card)', () => {
    poser('<div class="scan-card" data-card-id="42"></div>', { x: 10, y: 20, w: 100, h: 140 })
    expect(boitesDesCartes([42])).toEqual([{ x: 10, y: 20, w: 100, h: 140 }])
  })

  it('trouve une carte du plateau mobile (.medaillon)', () => {
    poser('<button class="medaillon" data-card-id="49"></button>', { x: 5, y: 6, w: 40, h: 40 })
    expect(boitesDesCartes([49])).toEqual([{ x: 5, y: 6, w: 40, h: 40 }])
  })

  it('ignore un identifiant absent de la table sans se plaindre', () => {
    poser('<div class="scan-card" data-card-id="42"></div>', { x: 0, y: 0, w: 10, h: 10 })
    expect(boitesDesCartes([999])).toEqual([])
  })

  it("ignore l'identifiant 0, qui veut dire « aucune carte »", () => {
    poser('<div class="scan-card" data-card-id="0"></div>', { x: 0, y: 0, w: 10, h: 10 })
    expect(boitesDesCartes([0])).toEqual([])
  })

  it('ignore une carte sans surface (masquée)', () => {
    poser('<div class="scan-card" data-card-id="7"></div>', { x: 0, y: 0, w: 0, h: 0 })
    expect(boitesDesCartes([7])).toEqual([])
  })

  it('ne rend pas deux fois la même carte demandée deux fois', () => {
    poser('<div class="scan-card" data-card-id="42"></div>', { x: 1, y: 2, w: 3, h: 4 })
    expect(boitesDesCartes([42, 42])).toHaveLength(1)
  })
})

describe('boitesDesPanneaux', () => {
  it('rend les panneaux visés', () => {
    poser('<section class="demande-centrale"></section>', { x: 50, y: 60, w: 660, h: 133 })
    expect(boitesDesPanneaux(['.demande-centrale'])).toEqual([{ x: 50, y: 60, w: 660, h: 133 }])
  })

  it("n'inclut jamais le panneau qui interroge — il se fuirait lui-même", () => {
    const soi = poser('<section class="demande-centrale"></section>', { x: 0, y: 0, w: 10, h: 10 })
    expect(boitesDesPanneaux(['.demande-centrale'], soi)).toEqual([])
  })
})
