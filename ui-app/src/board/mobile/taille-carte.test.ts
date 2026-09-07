import { describe, expect, it } from 'vitest'
import { HAUTEUR_FIXE, LARGEUR_MAX, LARGEUR_MIN, hauteurRangee, largeurCarte } from './taille-carte'

describe('taille-carte', () => {
  it('reserve 166 px aux bandes fixes : barre 48, main 90, deux etiquettes de 14', () => {
    expect(HAUTEUR_FIXE).toBe(48 + 90 + 2 * 14)
  })

  it('partage le reste en deux rangees egales', () => {
    expect(hauteurRangee(480)).toBe(157)
  })

  // S24 Ultra en paysage, plein ecran : la carte fait environ 112 px.
  it('donne environ 112 px en plein ecran (480 px de haut)', () => {
    expect(Math.round(largeurCarte(480))).toBe(112)
  })

  // Le meme, avec la barre du navigateur : environ 95 px.
  it('donne environ 95 px avec la barre du navigateur (430 px de haut)', () => {
    expect(Math.round(largeurCarte(430))).toBe(95)
  })

  it('ne descend jamais sous le plancher de 84 px', () => {
    expect(largeurCarte(300)).toBe(LARGEUR_MIN)
    expect(largeurCarte(0)).toBe(LARGEUR_MIN)
  })

  it('ne depasse jamais 150 px, la largeur du plateau PC (tablette)', () => {
    expect(largeurCarte(820)).toBe(LARGEUR_MAX)
  })
})
