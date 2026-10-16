// Intensified (7e carte d'état, TMNT) et te201 Intense Combatants : ce que le plateau DESSINE.
//
// `tools/cas/intensified.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur
// REGARDE (PROCESSUS-CARTE.md, étape 8 bis). te201 pose une carte Intensified à côté d'un état
// déjà présent : les DEUX cartes d'état doivent être dessinées sur le porteur, et deux
// Intensified empilées aussi (aucun plafond).
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'
import { etatDe } from './mobile/etats'

const IDENTITE = 1
const RHINO = 80
const identite = () => carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')
const rhino = () => carte(RHINO, '01094', 'EncounterVillain', 'Rhino')

describe('intensified : la carte d état est dessinée sur son porteur, à côté de l état qu elle garde', () => {
  it('Sonné + Intensified sur le vilain (te201 au second Sonné) : les deux sont dessinées', () => {
    const m = tableAvec(siege({ area_hero: [identite()] }), {
      area_villain: [
        rhino(),
        carte(90, 'stunned', 'StatusCard', 'Stunned', { bind_object_id: RHINO }),
        carte(91, 'intensified', 'StatusCard', 'Intensified', { bind_object_id: RHINO }),
      ],
    })
    expect(dessinee(m, 90)).toBeDefined()
    expect(dessinee(m, 91)).toBeDefined()
    expect(dessinee(m, 91)?.kind).toBe('status')
    expect(dessinee(m, 91)?.codeCarte).toBe('intensified')
    expect(dessinee(m, 91)?.portePar).toBe(RHINO)
  })

  it('deux Intensified empilées sur l identité (aucun plafond) : chacune est dessinée', () => {
    const m = tableAvec(siege({
      area_hero: [
        identite(),
        carte(70, 'tough', 'StatusCard', 'Tough', { bind_object_id: IDENTITE }),
        carte(71, 'intensified', 'StatusCard', 'Intensified', { bind_object_id: IDENTITE }),
        carte(72, 'intensified', 'StatusCard', 'Intensified', { bind_object_id: IDENTITE }),
      ],
    }))
    expect(dessinee(m, 71)?.portePar).toBe(IDENTITE)
    expect(dessinee(m, 72)?.portePar).toBe(IDENTITE)
  })

  it('la pastille mobile la nomme en français (lettre I, Intensifié)', () => {
    expect(etatDe({ id: 'i', name: 'Intensified', kind: 'status', imageUrl: '' })?.nom).toBe('Intensifié')
  })
})
