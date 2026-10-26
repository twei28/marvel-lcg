// La fenetre de choix de cible au telephone se GLISSE au doigt et se cale sur trois positions (maquette approuvee le 26/10/2026) :
// reduite (poignee, titre, compteur), basse (tout, boutons compris), haute (plein cadre). Fonctions pures.
import { describe, expect, it } from 'vitest'
import { borner, caler, positionsFeuille } from './calage-feuille'

describe('les positions de la feuille', () => {
  it('haute colle la feuille en haut, basse montre tout, reduite ne montre que la poignee, le titre et le compteur', () => {
    expect(positionsFeuille({ hauteur: 560, basse: 410, reduite: 120 })).toEqual({ haute: 0, basse: 150, reduite: 440 })
  })

  it('une feuille plus courte que la position basse reste entiere : basse = haute', () => {
    const positions = positionsFeuille({ hauteur: 300, basse: 410, reduite: 120 })
    expect(positions.haute).toBe(0)
    expect(positions.basse).toBe(0)
    expect(positions.reduite).toBe(180)
  })

  it('la position reduite ne depasse jamais la hauteur de la feuille', () => {
    expect(positionsFeuille({ hauteur: 90, basse: 410, reduite: 120 }).reduite).toBe(0)
  })
})

describe('borner', () => {
  const positions = positionsFeuille({ hauteur: 560, basse: 410, reduite: 120 })
  it('ne laisse pas la feuille monter au-dessus de la haute ni descendre sous la reduite', () => {
    expect(borner(-40, positions)).toBe(0)
    expect(borner(999, positions)).toBe(440)
    expect(borner(200, positions)).toBe(200)
  })
})

describe('caler : la position la plus proche, avec l elan du doigt', () => {
  const positions = positionsFeuille({ hauteur: 560, basse: 410, reduite: 120 })
  it('sans vitesse, se cale sur la position la plus proche', () => {
    expect(caler(140, 0, positions)).toBe('basse')
    expect(caler(10, 0, positions)).toBe('haute')
    expect(caler(430, 0, positions)).toBe('reduite')
  })

  it('un coup de doigt vers le haut la fait monter meme depuis le milieu', () => {
    // 300 est plus pres de basse (150) que de reduite (440), mais l'elan (-30 px par image) la lance vers le haut
    expect(caler(300, -30, positions)).toBe('haute')
  })

  it('un coup de doigt vers le bas la fait descendre', () => {
    expect(caler(300, 25, positions)).toBe('reduite')
  })

  it('un petit elan ne change pas la position la plus proche', () => {
    expect(caler(160, -2, positions)).toBe('basse')
  })
})
