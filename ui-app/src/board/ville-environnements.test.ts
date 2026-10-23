// La ville ne dort jamais : ce que le plateau DESSINE pour les environnements (23/10/2026).
// The City (pu005) + Never Sleeps (pu006) : panorama 5|6, collees, la 1re a gauche, quel que soit l'ordre d'arrivee.
// Les lieux : seul celui que le joueur occupe est sur la table (les autres se lisent dans l'onglet « Ville »).
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const lieu = (ligne: number, colonne: number, objet: number) => ({
  ligne, colonne, objet, card_id: `pu0${30 + ligne * 3 + colonne}`, joueurs: [], sbires_attaches: [], limite_utilisee: false, piste: null,
})

const monde = (ordre: 'normal' | 'inverse'): World => {
  const city = carte(105, 'pu005', 'Environment', 'The City')
  const jamais = carte(106, 'pu006', 'Environment', 'Never Sleeps')
  const environnement = ordre === 'normal' ? [city, jamais] : [jamais, city]
  return tableAvec(siege(), {
    area_environment: [...environnement, carte(130, 'pu030', 'Environment', "Hell's Kitchen"), carte(134, 'pu034', 'Environment', 'Midtown')],
    ville: {
      lignes: [{ ligne: 0, capo: null, capo_card_id: '' }, { ligne: 1, capo: null, capo_card_id: '' }],
      cases: [lieu(0, 0, 130), lieu(1, 1, 134)],
      joueurs: [{ player_id: 0, ligne: 1, colonne: 1 }],
    },
  } as Partial<World>)
}

describe('environnements de La ville', () => {
  it.each(['normal', 'inverse'] as const)('pose The City a gauche et Never Sleeps a droite, en panorama (%s)', (ordre) => {
    expect(dessinee(monde(ordre), 105)?.panorama).toBe('gauche')
    expect(dessinee(monde(ordre), 106)?.panorama).toBe('droite')
  })

  it('ne montre que le lieu occupe', () => {
    expect(dessinee(monde('normal'), 134)).toBeDefined()
    expect(dessinee(monde('normal'), 130)).toBeUndefined()
  })

  it("grise le CAPO d'une autre rangee, pas celui de la notre", () => {
    const m = monde('normal')
    m.area_villain = [carte(200, 'pu048a', 'EncounterVillain', 'Capo A'), carte(201, 'pu049a', 'EncounterVillain', 'Capo B')]
    m.ville = {
      lignes: [{ ligne: 0, capo: 200, capo_card_id: 'pu048a' }, { ligne: 1, capo: 201, capo_card_id: 'pu049a' }],
      cases: [lieu(0, 0, 130), lieu(1, 1, 134)],
      joueurs: [{ player_id: 0, ligne: 1, colonne: 1 }],
    }
    expect(dessinee(m, 200)?.inactif).toBe(true)
    expect(dessinee(m, 201)?.inactif).toBeFalsy()
  })
})
