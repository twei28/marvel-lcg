import { describe, expect, it } from 'vitest'
import { mesurerHorsChamp, nombreHorsChamp } from './hors-champ'

const cartes = (n: number, largeur = 100, ecart = 8) =>
  Array.from({ length: n }, (_, i) => ({ gauche: i * (largeur + ecart), largeur }))

describe('nombreHorsChamp', () => {
  it('vaut 0 quand tout tient', () => {
    expect(nombreHorsChamp(cartes(3), 0, 400)).toBe(0)
  })

  it('compte les cartes dont plus de la moitie depasse a droite', () => {
    // 5 cartes de 100 px, ecart 8 : bords droits a 100, 208, 316, 424, 532.
    // Fenetre de 370 px : la 4e depasse de 54 px (plus de la moitie), la 5e entierement.
    expect(nombreHorsChamp(cartes(5), 0, 370)).toBe(2)
  })

  it('ne compte pas une carte qui ne depasse que d\'un peu', () => {
    // La 4e carte (316 a 416) depasse de 16 px sur 100 : elle se lit encore.
    expect(nombreHorsChamp(cartes(4), 0, 400)).toBe(0)
  })

  it('compte aussi ce qui est cache a gauche par le defilement', () => {
    // Defilement de 60 px : la 1re carte (0 a 100) a 60 px caches, plus de la moitie.
    expect(nombreHorsChamp(cartes(3), 60, 1000)).toBe(1)
  })

  it('vaut 0 sans carte', () => {
    expect(nombreHorsChamp([], 0, 400)).toBe(0)
  })
})

describe('mesurerHorsChamp', () => {
  it('lit les positions des enfants dans le DOM', () => {
    const conteneur = document.createElement('div')
    for (const boite of cartes(5)) {
      const enfant = document.createElement('div')
      enfant.className = 'carte-posee'
      Object.defineProperty(enfant, 'offsetLeft', { value: boite.gauche })
      Object.defineProperty(enfant, 'offsetWidth', { value: boite.largeur })
      conteneur.append(enfant)
    }
    Object.defineProperty(conteneur, 'clientWidth', { value: 370 })
    conteneur.scrollLeft = 0
    expect(mesurerHorsChamp(conteneur)).toBe(2)
  })
})
