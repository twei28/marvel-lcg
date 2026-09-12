// Un cout MIXTE : des types EXIGES plus des ressources libres.
//
// Le moteur ecrit « Y1 » pour Thunder Strike (cout 2, Requirement [energy]) :
// une lettre par type exige, puis le nombre de ressources libres
// (`GetPrintedCostWithRequirement`, game/card/face/attribute/has_cost.py, et
// `color_text`, game/element/rbyg.py). Le plateau lisait `Number('Y1')` =
// NaN : plus de total, aucune pastille, « Payer le cout » au lieu de « Payer
// 2 », et le coup se disait pret des la premiere energie. Signale en partie
// le 12/09/2026.
import { describe, expect, it } from 'vitest'
import { nombreDeRessources, reponsePrete, totalDuCout, typesManquants, type Option, type Paiement } from './ask'

const paiement = (cost: string): Paiement => ({ cost, payment: [], rule: [] }) as unknown as Paiement

describe('totalDuCout', () => {
  it('lit un cout en chiffres', () => {
    expect(totalDuCout('0')).toBe(0)
    expect(totalDuCout('2')).toBe(2)
  })

  it('lit un cout MIXTE : les types exiges plus les ressources libres', () => {
    expect(totalDuCout('Y1')).toBe(2) // Thunder Strike : 1 energie + 1 libre
    expect(totalDuCout('YYY2')).toBe(5) // Wrath of Olympus
    expect(totalDuCout('BB1')).toBe(3) // Honed Technique
  })

  it('lit un cout ecrit en types seuls', () => {
    expect(totalDuCout('BY')).toBe(2) // Energy Shield
    expect(totalDuCout('Y')).toBe(1)
  })

  it('ne devine rien sur un cout que le moteur ne chiffre pas', () => {
    expect(totalDuCout('*')).toBeUndefined() // cout ignore (ignore_resource_cost)
    expect(totalDuCout('X')).toBeUndefined()
  })

  it('un cout vide vaut zero, comme avant : le moteur ne demande rien', () => {
    // `get_cost_str_rule` (game/effect/effect.py) rend "" quand la cible n'a
    // pas de cout propre. Comportement d'origine, conserve.
    expect(totalDuCout('')).toBe(0)
  })
})

describe('nombreDeRessources', () => {
  it('rend le total du cout mixte, celui qu attendent les pastilles', () => {
    expect(nombreDeRessources(paiement('Y1'))).toBe(2)
    expect(nombreDeRessources(paiement('2'))).toBe(2)
    expect(nombreDeRessources(undefined)).toBeUndefined()
  })
})

describe('typesManquants avec un cout mixte', () => {
  it('ne reclame que le TYPE exige, le reste du cout etant libre', () => {
    expect(typesManquants(paiement('Y1'), [])).toEqual({ Y: 1 })
    expect(typesManquants(paiement('YYY2'), [])).toEqual({ Y: 3 })
  })
})

describe('reponsePrete face a un cout mixte', () => {
  // Thunder Strike : cout 2, dont une energie. Le moteur ecrit « Y1 » et
  // propose deux ressources : une energie (7) et une mentale (8).
  const THUNDER_STRIKE = {
    id: 1,
    name: 'Play',
    bind_id: 9,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {
      0: {
        cost: 'Y1',
        payment: [
          { effect_id: 7, res_text: 'Y' },
          { effect_id: 8, res_text: 'B' },
        ],
        rule: [],
      },
    },
    select_rule: '',
    select_rule_param: [0, 0],
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  } as unknown as Option

  it('refuse tant que l energie manque, et le dit par son type', () => {
    expect(reponsePrete(THUNDER_STRIKE, [], []).raison).toMatch(/energy/i)
  })

  it('refuse encore avec la SEULE energie : il reste une ressource a poser', () => {
    // C'est le defaut vu en partie : le plateau se disait pret ici.
    const verdict = reponsePrete(THUNDER_STRIKE, [], [7])
    expect(verdict.prete).toBe(false)
    expect(verdict.raison).toMatch(/1 more resource/i)
  })

  it('accepte avec l energie ET une seconde ressource', () => {
    expect(reponsePrete(THUNDER_STRIKE, [], [7, 8]).prete).toBe(true)
  })
})
