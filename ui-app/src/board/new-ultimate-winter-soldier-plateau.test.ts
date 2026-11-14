// New Ultimate Winter Soldier (Dipsome, `uw001a`-`uw018`) : ce que le plateau DESSINE une fois les cartes résolues.
//
// `Fusion/marvel-lcg-src/tools/cas/new_ultimate_winter_soldier.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). Les cartes du pack qui changent ce qu'on VOIT :
//   - uw002 Wolverine's Claws : amélioration Permanente posée sur l'identité par le Setup de Logan ;
//   - uw003 Phoenix : allié qui entre en jeu quand elle est défaussée au hasard ;
//   - uw011 Mission Objective / uw012 « This is Your Enemy » : améliorations posées sur un SBIRE, et la première se
//     DÉPLACE d'un sbire à un autre quand le héros paie 1 dégât ;
//   - uw016 Phoenix Specimen Brainwashing : attachement posé sur l'identité du joueur ;
//   - uw014 Directorate X : complot annexe ; uw015, uw017, uw018 : sbires du set némésis.
// Aucun correctif de plateau : le rendu générique suffisait, ces cas sont verts d'emblée.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const GRIFFES = 2
const MISSION = 3
const SBIRE_A = 81
const SBIRE_B = 82

const heros = () => carte(IDENTITE, 'uw001a', 'Hero', 'Winter Soldier')

describe('uw002 Wolverine\'s Claws : posées sur Winter Soldier au Setup', () => {
  it('est dessinée derrière le héros', () => {
    const monde = tableAvec(
      siege({ area_hero: [heros(), carte(GRIFFES, 'uw002', 'Upgrade', "Wolverine's Claws", { bind_object_id: IDENTITE })] })
    )
    expect(dessinee(monde, GRIFFES)).toBeDefined()
    expect(dessinee(monde, GRIFFES)?.portePar).toBe(IDENTITE)
  })
})

describe('uw003 Phoenix : allié en jeu', () => {
  it('est dessinée avec les alliés du joueur', () => {
    const monde = tableAvec(siege({ area_hero: [heros()], allies: [carte(10, 'uw003', 'Ally', 'Phoenix')] }))
    expect(dessinee(monde, 10)).toBeDefined()
  })
})

describe('uw011 Mission Objective et uw012 : posées sur un sbire', () => {
  const sbires = (...cartes: ReturnType<typeof carte>[]) =>
    tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [carte(80, '01094', 'EncounterVillain', 'Rhino'), ...cartes],
    })

  it('Mission Objective est dessinée sur son sbire', () => {
    const monde = sbires(
      carte(SBIRE_A, '01110', 'Minion', 'Hydra Bomber'),
      carte(MISSION, 'uw011', 'Upgrade', 'Mission Objective', { bind_object_id: SBIRE_A })
    )
    expect(dessinee(monde, MISSION)).toBeDefined()
    expect(dessinee(monde, MISSION)?.portePar).toBe(SBIRE_A)
  })

  it('Mission Objective, DÉPLACÉE sur un autre sbire, suit son nouveau porteur', () => {
    const monde = sbires(
      carte(SBIRE_B, '01103', 'Minion', 'Shocker'),
      carte(MISSION, 'uw011', 'Upgrade', 'Mission Objective', { bind_object_id: SBIRE_B })
    )
    expect(dessinee(monde, MISSION)?.portePar).toBe(SBIRE_B)
  })

  it('uw012 « This is Your Enemy » est dessinée sur son sbire', () => {
    const monde = sbires(
      carte(SBIRE_A, '01110', 'Minion', 'Hydra Bomber'),
      carte(4, 'uw012', 'Upgrade', 'This is Your Enemy', { bind_object_id: SBIRE_A })
    )
    expect(dessinee(monde, 4)?.portePar).toBe(SBIRE_A)
  })
})

describe('le set némésis : attachement, complot annexe, sbires', () => {
  it('uw016 Phoenix Specimen Brainwashing est dessinée sur l\'identité', () => {
    const monde = tableAvec(
      siege({ area_hero: [heros(), carte(5, 'uw016', 'Attachment', 'Phoenix Specimen Brainwashing', { bind_object_id: IDENTITE })] })
    )
    expect(dessinee(monde, 5)).toBeDefined()
    expect(dessinee(monde, 5)?.portePar).toBe(IDENTITE)
  })

  it('uw014 Directorate X, uw015 Alonya, uw017 et uw018 (Sentinelles) sont dessinés', () => {
    const monde = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(80, '01094', 'EncounterVillain', 'Rhino'),
        carte(20, 'uw014', 'SideScheme', 'Directorate X'),
        carte(21, 'uw015', 'Minion', 'Alonya Prostovich'),
        carte(22, 'uw017', 'Minion', 'X-S Sentinel I'),
        carte(23, 'uw018', 'Minion', 'X-S Sentinel II'),
      ],
    })
    for (const id of [20, 21, 22, 23]) expect(dessinee(monde, id)).toBeDefined()
  })
})
