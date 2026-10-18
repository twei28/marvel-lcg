// Où se posent les cartes qui sortent du deck rencontre.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `elles ne sortent jamais du plateau`. Une
// carte boost posée hors du cadre est une carte qu'on ne verra pas, et tout le
// geste ne sert qu'à la faire voir : « les cartes boost sortent vraiment du
// paquet pour se mettre à côté, pour ensuite voir à combien ».
import { describe, expect, it } from 'vitest'
import {
  ECART,
  placeDeLaRevelee,
  placesDeLecture,
  placesDesBoosts,
  type Boite,
} from './places-rencontre'

const CADRE: Boite = { x: 0, y: 0, w: 1900, h: 940 }
// Le deck rencontre : en haut à gauche de la table, collé au bord.
const DECK: Boite = { x: 10, y: 12, w: 127, h: 200 }

// L'attaquant : le méchant, au milieu de la rangée haute.
const ATTAQUANT: Boite = { x: 760, y: 11, w: 127, h: 200 }

describe('les cartes boost se posent contre l’ATTAQUANT', () => {
  // ⚠ PAS CONTRE LE PAQUET (14/09/2026). Elles se posaient à côté du deck
  // rencontre, en haut à gauche, loin du méchant. Choix de l'utilisateur parmi
  // trois : « à côté du méchant qui frappe ». On voit à qui appartient l'élan.
  it('à la suite, à droite de la carte qui frappe', () => {
    const places = placesDesBoosts(ATTAQUANT, CADRE, 2)
    expect(places[0].x).toBe(ATTAQUANT.x + ATTAQUANT.w + ECART)
    expect(places[0].y).toBe(ATTAQUANT.y)
  })

  it('à sa gauche quand la droite déborderait', () => {
    const colleADroite: Boite = { x: 1700, y: 11, w: 127, h: 200 }
    const places = placesDesBoosts(colleADroite, CADRE, 3)
    for (const p of places) expect(p.x).toBeGreaterThanOrEqual(CADRE.x)
    expect(places[0].x).toBeLessThan(colleADroite.x)
  })

  it('se posent à la suite, à droite de l’ancre reçue', () => {
    const places = placesDesBoosts(DECK, CADRE, 3)
    expect(places).toHaveLength(3)
    expect(places[0].x).toBe(DECK.x + DECK.w + ECART)
    expect(places[1].x).toBe(places[0].x + DECK.w + ECART)
    expect(places[2].x).toBe(places[1].x + DECK.w + ECART)
  })

  it('gardent la taille et la hauteur du paquet', () => {
    const [p] = placesDesBoosts(DECK, CADRE, 1)
    expect(p.w).toBe(DECK.w)
    expect(p.h).toBe(DECK.h)
    expect(p.y).toBe(DECK.y)
  })

  it('aucune ne sort du plateau, même à quatre sur un cadre étroit', () => {
    const etroit: Boite = { x: 0, y: 0, w: 600, h: 940 }
    for (const p of placesDesBoosts(DECK, etroit, 4)) {
      expect(p.x).toBeGreaterThanOrEqual(etroit.x)
    }
  })

  it('zéro boost ne donne aucune place', () => {
    // Une manigance du méchant n'a pas de boost : le geste ne doit rien poser,
    // pas poser une carte vide.
    expect(placesDesBoosts(DECK, CADRE, 0)).toEqual([])
  })
})

describe('la lecture centrale des rencontres et des boosts', () => {
  it('centre une carte nettement agrandie', () => {
    const p = placeDeLaRevelee(DECK, CADRE)
    expect(p.x + p.w / 2).toBeCloseTo(CADRE.w / 2)
    expect(p.y + p.h / 2).toBeCloseTo(CADRE.h / 2)
    expect(p.w).toBeGreaterThan(300)
  })

  it('conserve une carte horizontale lisible et son ratio', () => {
    const [p] = placesDeLecture(CADRE, [176 / 127])
    expect(p.w / p.h).toBeCloseTo(176 / 127)
    expect(p.w).toBeGreaterThan(500)
  })

  it('garde les boosts côte à côte dans le cadre sur un petit écran', () => {
    const cadre = { x: 20, y: 15, w: 600, h: 400 }
    const places = placesDeLecture(cadre, Array(4).fill(127 / 176))
    for (const p of places) {
      expect(p.x).toBeGreaterThanOrEqual(cadre.x)
      expect(p.x + p.w).toBeLessThanOrEqual(cadre.x + cadre.w)
      expect(p.y).toBeGreaterThanOrEqual(cadre.y)
      expect(p.y + p.h).toBeLessThanOrEqual(cadre.y + cadre.h)
    }
    expect(places[1].x).toBeGreaterThan(places[0].x + places[0].w)
  })

  it('réserve la barre du haut et garde la carte dans un cadre bas', () => {
    const cadre = { x: 0, y: 0, w: 1000, h: 300 }
    const [p] = placesDeLecture(cadre, [127 / 176])
    expect(p.y).toBeGreaterThanOrEqual(70)
    expect(p.y + p.h).toBeLessThanOrEqual(cadre.h)
  })

  it('ne crée aucune place sans carte', () => {
    expect(placesDeLecture(CADRE, [])).toEqual([])
  })
})
