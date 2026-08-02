import { describe, expect, it } from 'vitest'
import { groupesParJoueur, ordreDAffichage } from './joueurs'
import type { EmplacementAffiche } from '../zones'

const EMPLACEMENT: EmplacementAffiche = {
  cle: 'terrain-soutien',
  titre: 'Héros et soutiens',
  groupes: [[], [], [], [], [], []],
  nombreSurLaLigne: 0,
  proprietaires: [0, 0, 0, 1, 1, 1],
}

describe('groupesParJoueur', () => {
  it('range chaque groupe sous son joueur', () => {
    const par = groupesParJoueur(EMPLACEMENT)
    expect([...par.keys()]).toEqual([0, 1])
    expect(par.get(0)).toHaveLength(3)
    expect(par.get(1)).toHaveLength(3)
  })

  it('met tout sous le joueur 0 quand le champ est absent', () => {
    const par = groupesParJoueur({ ...EMPLACEMENT, proprietaires: undefined })
    expect([...par.keys()]).toEqual([0])
    expect(par.get(0)).toHaveLength(6)
  })
})

describe('ordreDAffichage', () => {
  it('met le joueur actif en premier', () => {
    expect(ordreDAffichage([0, 1, 2], 2)).toEqual([2, 0, 1])
  })

  it("ne bouge rien si l'actif est inconnu", () => {
    expect(ordreDAffichage([0, 1, 2], 7)).toEqual([0, 1, 2])
  })
})
