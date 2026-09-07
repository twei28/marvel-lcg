import { describe, expect, it } from 'vitest'
import {
  HAUTEUR_FIXE,
  LARGEUR_MAX,
  LARGEUR_MIN,
  MARGE_SCANCARD,
  hauteurRangee,
  largeurCarte,
} from './taille-carte'

describe('taille-carte', () => {
  it('reserve 166 px aux bandes fixes (barre 48, main 90, deux etiquettes de 14), plus MARGE_SCANCARD', () => {
    expect(HAUTEUR_FIXE).toBe(48 + 90 + 2 * 14 + MARGE_SCANCARD)
  })

  it('partage le reste en deux rangees egales', () => {
    expect(hauteurRangee(480)).toBe(117)
  })

  // S24 Ultra en paysage, plein ecran : MARGE_SCANCARD (voir son commentaire
  // dans taille-carte.ts, qui couvre a la fois la bande de jauge PV/menace
  // ET le pire cas mesure de .pm-barre sur la page de fixtures) fait tomber
  // meme le plein ecran au plancher de lisibilite. Ce n'est PAS le
  // comportement souhaite a terme (voir le commentaire de la constante),
  // seulement ce que le pire cas mesure impose aujourd'hui.
  it('tombe au plancher de 84 px meme en plein ecran (480 px de haut)', () => {
    expect(largeurCarte(480)).toBe(LARGEUR_MIN)
  })

  // Le meme, avec la barre du navigateur (430 px) : encore plus serre, meme
  // plancher.
  it('tombe au plancher de 84 px avec la barre du navigateur (430 px de haut)', () => {
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
