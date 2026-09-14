// Où se pose le cartouche de la phase jouée sur la table.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `il ne sort jamais du plateau` : le
// cartouche porte le bouton OK, seul moyen d'avancer dans ce mode. Un
// cartouche à moitié dehors est une partie bloquée jusqu'au filet anti-blocage
// de 90 secondes.
import { describe, expect, it } from 'vitest'
import { MARGE, placeDuCartouche, type Boite } from './phase-sur-table'

const CADRE: Boite = { x: 0, y: 0, w: 1000, h: 600 }
const TAILLE = { w: 240, h: 120 }
const carte = (x: number, y: number): Boite => ({ x, y, w: 100, h: 145 })

describe('le cartouche se pose à côté de la carte qui agit', () => {
  it('à sa droite quand la place y est', () => {
    const place = placeDuCartouche(carte(200, 200), CADRE, TAILLE)
    expect(place.cote).toBe('droite')
    expect(place.x).toBe(200 + 100 + MARGE)
  })

  it('centré sur la hauteur de la carte', () => {
    const place = placeDuCartouche(carte(200, 200), CADRE, TAILLE)
    // La carte va de 200 à 345, son milieu est à 272,5 ; le cartouche fait 120.
    expect(place.y).toBeCloseTo(272.5 - 60)
  })

  it('à sa gauche quand la droite déborderait', () => {
    // Une carte collée au bord droit : à droite il ne reste rien.
    const place = placeDuCartouche(carte(880, 200), CADRE, TAILLE)
    expect(place.cote).toBe('gauche')
    expect(place.x).toBe(880 - 240 - MARGE)
  })

  it('ne recouvre JAMAIS la carte qui agit', () => {
    // C'est elle qu'on regarde : l'annonce ne doit pas la cacher.
    for (const x of [0, 200, 500, 880, 940]) {
      const c = carte(x, 200)
      const place = placeDuCartouche(c, CADRE, TAILLE)
      const seChevauchent =
        place.x < c.x + c.w && place.x + TAILLE.w > c.x &&
        place.y < c.y + c.h && place.y + TAILLE.h > c.y
      expect(seChevauchent, `chevauchement pour x=${x}`).toBe(false)
    }
  })
})

describe('le cartouche ne sort jamais du plateau', () => {
  it('une carte tout en haut ne le fait pas sortir par le haut', () => {
    const place = placeDuCartouche(carte(200, 0), CADRE, TAILLE)
    expect(place.y).toBeGreaterThanOrEqual(MARGE)
  })

  it('une carte tout en bas ne le fait pas sortir par le bas', () => {
    const place = placeDuCartouche(carte(200, 560), CADRE, TAILLE)
    expect(place.y + TAILLE.h).toBeLessThanOrEqual(CADRE.h - MARGE)
  })

  it('sur un plateau étroit, il reste dedans des deux côtés', () => {
    // Ni à droite ni à gauche : il passe dessous, recalé dans le cadre.
    const etroit: Boite = { x: 0, y: 0, w: 300, h: 600 }
    const place = placeDuCartouche(carte(60, 100), etroit, TAILLE)
    expect(place.x).toBeGreaterThanOrEqual(MARGE)
    expect(place.x + TAILLE.w).toBeLessThanOrEqual(etroit.w - MARGE)
  })

  it('même si le plateau est plus petit que le cartouche, il commence dedans', () => {
    // ⚠ Cas limite de la fonction de bornage : la borne basse doit gagner,
    // sinon le cartouche sort par le HAUT au lieu de sortir par le bas.
    const minuscule: Boite = { x: 0, y: 0, w: 200, h: 100 }
    const place = placeDuCartouche(carte(20, 20), minuscule, TAILLE)
    expect(place.x).toBeGreaterThanOrEqual(0)
    expect(place.y).toBeGreaterThanOrEqual(0)
  })

  it('le cadre peut être décalé dans la page', () => {
    // Le plateau n'est pas toujours en 0,0 : il est centré, avec une barre au-dessus.
    const decale: Boite = { x: 160, y: 48, w: 1000, h: 600 }
    const place = placeDuCartouche(carte(1000, 60), decale, TAILLE)
    expect(place.x).toBeGreaterThanOrEqual(decale.x)
    expect(place.y).toBeGreaterThanOrEqual(decale.y)
  })
})

describe('une étape sans auteur', () => {
  it('pose le cartouche en bas au centre', () => {
    // L'étape de menace n'a pas d'auteur : c'est une règle du jeu qui pose la
    // menace. Il n'y a donc aucune carte à côté de laquelle se mettre.
    const place = placeDuCartouche(undefined, CADRE, TAILLE)
    expect(place.cote).toBe('centre')
    expect(place.x).toBe((1000 - 240) / 2)
    expect(place.y).toBe(600 - 120 - MARGE)
  })
})
