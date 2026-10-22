import { describe, expect, it } from 'vitest'
import type { Option } from './ask'
import { casesAtteignables, casesDeLaLigne, lignesOrdonnees, optionSeDeplacer, positionDuJoueur, resumeCompteurs, villeDuMonde } from './ville-etat'
import type { VilleCase, World } from './world'

const lieu = (ligne: number, colonne: number, objet: number): VilleCase => ({
  ligne, colonne, objet, card_id: `pu0${30 + ligne * 3 + colonne}`, joueurs: [], sbires_attaches: [], limite_utilisee: false, piste: null,
})
const monde = {
  ville: {
    lignes: [{ ligne: 1, capo: 7, capo_card_id: 'pu050a' }, { ligne: -1, capo: 5, capo_card_id: 'pu048a' }, { ligne: 0, capo: 6, capo_card_id: 'pu049a' }],
    cases: [lieu(0, 1, 11), lieu(0, 0, 10), lieu(1, 1, 14), lieu(-1, 0, 20)],
    joueurs: [{ player_id: 0, ligne: 1, colonne: 1 }],
  },
} as unknown as World
const option = (name: string, cibles: number[], echec = ''): Option => ({
  id: 70, name, bind_id: 3, bind_player_id: 0, all_legal_targets: cibles, target_num_range: [1, 1], target_payment: {},
  select_rule: '', target_must_include_traits: [], failure_reason: echec, is_search: false,
})

describe('etat de la ville', () => {
  it('rend undefined hors de la ville (champ vide ou absent)', () => {
    expect(villeDuMonde(undefined)).toBeUndefined()
    expect(villeDuMonde({ ville: {} } as unknown as World)).toBeUndefined()
  })
  it('ordonne les rangees, Uptown (-1) au-dessus, et les cases par colonne', () => {
    const v = villeDuMonde(monde)!
    expect(lignesOrdonnees(v).map((l) => l.ligne)).toEqual([-1, 0, 1])
    expect(casesDeLaLigne(v, 0).map((c) => c.colonne)).toEqual([0, 1])
  })
  it('trouve la position du joueur', () => {
    const v = villeDuMonde(monde)!
    expect(positionDuJoueur(v, 0)).toEqual({ player_id: 0, ligne: 1, colonne: 1 })
    expect(positionDuJoueur(v, 3)).toBeUndefined()
  })
  it("les cases atteignables sont les cibles legales de « Move », rien sans l'option", () => {
    const v = villeDuMonde(monde)!
    expect(casesAtteignables(v, option('Move', [11, 20])).map((c) => c.objet)).toEqual([11, 20])
    expect(casesAtteignables(v, undefined)).toEqual([])
  })
  it("trouve l'option « Move » offerte, pas une option refusee ni un autre nom", () => {
    expect(optionSeDeplacer([option('Hero_Action', [1]), option('Move', [11])])?.name).toBe('Move')
    expect(optionSeDeplacer([option('Move', [11], 'pas payable')])).toBeUndefined()
    expect(optionSeDeplacer(undefined)).toBeUndefined()
  })
  it('resume les compteurs de piste', () => {
    expect(resumeCompteurs({ bouncer: 2 })).toBe('2')
    expect(resumeCompteurs({ culture: 1, hustle: 2 })).toBe('1 + 2')
    expect(resumeCompteurs({})).toBe('')
  })
})
