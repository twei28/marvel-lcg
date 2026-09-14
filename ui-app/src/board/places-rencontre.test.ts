// Où se posent les cartes qui sortent du deck rencontre.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `elles ne sortent jamais du plateau`. Une
// carte boost posée hors du cadre est une carte qu'on ne verra pas, et tout le
// geste ne sert qu'à la faire voir : « les cartes boost sortent vraiment du
// paquet pour se mettre à côté, pour ensuite voir à combien ».
import { describe, expect, it } from 'vitest'
import {
  AGRANDISSEMENT,
  ECART,
  placeDeLaRevelee,
  placesDesBoosts,
  type Boite,
} from './places-rencontre'

const CADRE: Boite = { x: 0, y: 0, w: 1900, h: 940 }
// Le deck rencontre : en haut à gauche de la table, collé au bord.
const DECK: Boite = { x: 10, y: 12, w: 127, h: 200 }

describe('les cartes boost sortent du paquet', () => {
  it('se posent à la suite, à droite du paquet', () => {
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

describe('la carte rencontre s’agrandit à côté du paquet', () => {
  it('elle est nettement plus grande que sur la table', () => {
    // À 127 px son texte est illisible, et c'est tout l'objet du geste.
    const p = placeDeLaRevelee(DECK, CADRE)
    expect(p.w).toBeCloseTo(DECK.w * AGRANDISSEMENT)
    expect(p.w).toBeGreaterThan(200)
  })

  it('elle se pose à droite du paquet, pas dessus', () => {
    const p = placeDeLaRevelee(DECK, CADRE)
    expect(p.x).toBeGreaterThanOrEqual(DECK.x + DECK.w)
  })

  it('⚠ elle ne dépasse JAMAIS par le haut', () => {
    // Le deck rencontre touche le bord supérieur : une carte agrandie centrée
    // sur lui sortirait de la table par le haut.
    const p = placeDeLaRevelee(DECK, CADRE)
    expect(p.y).toBeGreaterThanOrEqual(CADRE.y)
    expect(p.y + p.h).toBeLessThanOrEqual(CADRE.y + CADRE.h)
  })

  it('sur un cadre bas, elle reste dedans', () => {
    const bas: Boite = { x: 0, y: 0, w: 1900, h: 300 }
    const p = placeDeLaRevelee(DECK, bas)
    expect(p.y).toBeGreaterThanOrEqual(bas.y)
  })

  it('sans place à droite, elle passe à gauche plutôt que de sortir', () => {
    const etroit: Boite = { x: 0, y: 0, w: 400, h: 940 }
    const deckADroite: Boite = { x: 250, y: 12, w: 127, h: 200 }
    const p = placeDeLaRevelee(deckADroite, etroit)
    expect(p.x).toBeGreaterThanOrEqual(etroit.x)
    expect(p.x).toBeLessThan(deckADroite.x)
  })
})
