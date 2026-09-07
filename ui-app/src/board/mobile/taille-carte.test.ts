import { describe, expect, it } from 'vitest'
import { HAUTEUR_FIXE, LARGEUR_MAX, LARGEUR_MIN, hauteurRangee, largeurCarte } from './taille-carte'

describe('taille-carte', () => {
  it('reserve 166 px aux bandes fixes : barre 48, main 90, deux etiquettes de 14', () => {
    expect(HAUTEUR_FIXE).toBe(48 + 90 + 2 * 14)
  })

  it('partage le reste en deux rangees egales', () => {
    expect(hauteurRangee(480)).toBe(157)
  })

  // S24 Ultra en paysage, plein ecran : (157 - 18 de jauge) * 63 / 88 ≈ 99.5,
  // arrondi a 100 px. Cette fonction reste une estimation pour la main
  // (barre a sa hauteur nominale de 48px) : les cartes posees, en CSS,
  // mesurent la vraie hauteur de leur rangee (100cqh, paysage.css) et ne
  // devinent pas la hauteur de la barre.
  it('donne environ 100 px en plein ecran (480 px de haut)', () => {
    expect(Math.round(largeurCarte(480))).toBe(100)
  })

  // Le meme, avec la barre du navigateur : la marge de jauge fait tomber le
  // calcul sous le plancher de lisibilite, qui prend le relais.
  it('tombe au plancher de 84 px avec la barre du navigateur visible (430 px de haut)', () => {
    expect(largeurCarte(430)).toBe(LARGEUR_MIN)
  })

  it('ne descend jamais sous le plancher de 84 px', () => {
    expect(largeurCarte(300)).toBe(LARGEUR_MIN)
    expect(largeurCarte(0)).toBe(LARGEUR_MIN)
  })

  it('ne depasse jamais 150 px, la largeur du plateau PC (tablette)', () => {
    expect(largeurCarte(820)).toBe(LARGEUR_MAX)
  })
})
