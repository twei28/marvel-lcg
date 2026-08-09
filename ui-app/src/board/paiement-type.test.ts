// Le scenario qui a casse : Crossbones porte « Energy Shield » (04073), dont
// l'action de heros coute [energy][mental] — une ressource de CHAQUE type, pas
// deux ressources quelconques.
//
// Le moteur decrit ce cout par un texte de TYPES, « BY », la ou une carte
// ordinaire porte un nombre (« 2 »). Capture sur la vraie partie, option 153 :
//   cost    : "BY"
//   payment : effet 62 -> "Y" (For Justice!), 65 -> "B" (Great Responsibility),
//             70 -> "B" (Surveillance Team)
//
// Le plateau lisait ce cout avec Number("BY") = NaN, concluait « cout inconnu »,
// et se contentait alors d'UNE ressource : il annoncait l'action prete apres un
// seul paiement, le moteur la refusait, et l'action paraissait morte.
//
// Ces cas verrouillent la lecture d'un cout par types.
import { describe, expect, it } from 'vitest'
import { coutParType, reponsePrete, type Option } from './ask'

/** Option 153 telle que le moteur l'a envoyee, reduite a ce qui compte ici. */
const ENERGY_SHIELD: Option = {
  id: 153,
  name: 'Hero_Action',
  bind_id: 115,
  bind_player_id: 1,
  all_legal_targets: [],
  target_num_range: [0, 0],
  target_payment: {
    0: {
      cost: 'BY',
      payment: [
        { effect_id: 62, res_text: 'Y' },
        { effect_id: 65, res_text: 'B' },
        { effect_id: 70, res_text: 'B' },
      ],
      rule: [],
    },
  },
  select_rule: '',
  target_must_include_traits: [],
  failure_reason: '',
  is_search: false,
}

describe('coutParType', () => {
  it('lit un cout ecrit en types', () => {
    expect(coutParType('BY')).toEqual({ B: 1, Y: 1 })
  })

  it('compte les types repetes', () => {
    expect(coutParType('BBB')).toEqual({ B: 3 })
    expect(coutParType('YBR')).toEqual({ Y: 1, B: 1, R: 1 })
  })

  it('ne voit aucun type dans un cout numerique', () => {
    expect(coutParType('2')).toBeUndefined()
    expect(coutParType('0')).toBeUndefined()
    expect(coutParType('')).toBeUndefined()
  })
})

describe('reponsePrete face a un cout par types', () => {
  it('refuse une seule ressource quand deux types sont exiges', () => {
    const avecLeMental = reponsePrete(ENERGY_SHIELD, [], [62])
    expect(avecLeMental.prete).toBe(false)
    const avecUneEnergie = reponsePrete(ENERGY_SHIELD, [], [65])
    expect(avecUneEnergie.prete).toBe(false)
  })

  it('refuse deux ressources du MEME type', () => {
    // 65 et 70 fournissent tous deux « B », c'est-a-dire [mental] : il manque
    // le [energy]. Le commentaire disait l'inverse, comme la table de noms du
    // plateau, qui intervertissait B et Y (corrige le 9/8/2026).
    expect(reponsePrete(ENERGY_SHIELD, [], [65, 70]).prete).toBe(false)
  })

  it('accepte une ressource de chaque type exige', () => {
    expect(reponsePrete(ENERGY_SHIELD, [], [62, 65]).prete).toBe(true)
    expect(reponsePrete(ENERGY_SHIELD, [], [62, 70]).prete).toBe(true)
  })

  it('dit ce qui manque, en clair', () => {
    // Ces deux attentes etaient INVERSEES : elles encodaient le defaut de la
    // table de noms du plateau, qui appelait « energy » le mental et
    // reciproquement. 62 fournit « Y » (energy), il manque donc le mental ;
    // 65 fournit « B » (mental), il manque donc l'energy.
    expect(reponsePrete(ENERGY_SHIELD, [], [62]).raison).toMatch(/mental/i)
    expect(reponsePrete(ENERGY_SHIELD, [], [65]).raison).toMatch(/energy/i)
  })
})

/** 180 cartes du jeu portent un cout par types : les autres formes comptent
    autant que « BY ». Une carte a DOUBLE ressource en paie deux d'un coup, et
    un joker [wild] bouche n'importe quel trou. */
function optionAvecCout(cost: string, moyens: Array<[number, string]>): Option {
  return {
    ...ENERGY_SHIELD,
    target_payment: {
      0: {
        cost,
        payment: moyens.map(([effect_id, res_text]) => ({ effect_id, res_text })),
        rule: [],
      },
    },
  }
}

describe('les autres formes de cout par types', () => {
  it('exige deux ressources du meme type pour « BB »', () => {
    const option = optionAvecCout('BB', [
      [1, 'B'],
      [2, 'B'],
    ])
    expect(reponsePrete(option, [], [1]).prete).toBe(false)
    expect(reponsePrete(option, [], [1, 2]).prete).toBe(true)
  })

  it('accepte une carte a double ressource pour « BB »', () => {
    // Une seule carte, mais elle porte deux icones : elle paie le cout entier.
    const option = optionAvecCout('BB', [[1, 'BB']])
    expect(reponsePrete(option, [], [1]).prete).toBe(true)
  })

  it('laisse un joker completer un type manquant', () => {
    const option = optionAvecCout('BY', [
      [1, 'B'],
      [2, 'G'],
    ])
    expect(reponsePrete(option, [], [1, 2]).prete).toBe(true)
  })

  it('exige les trois types pour « YBR »', () => {
    const option = optionAvecCout('YBR', [
      [1, 'Y'],
      [2, 'B'],
      [3, 'R'],
    ])
    expect(reponsePrete(option, [], [1, 2]).prete).toBe(false)
    expect(reponsePrete(option, [], [1, 2, 3]).prete).toBe(true)
  })

  it('refuse un type qui ne correspond pas, meme en bon nombre', () => {
    // Le piege des couts a UN seul type : le compte etait bon, le type non.
    const option = optionAvecCout('B', [
      [1, 'R'],
      [2, 'B'],
    ])
    expect(reponsePrete(option, [], [1]).prete).toBe(false)
    expect(reponsePrete(option, [], [2]).prete).toBe(true)
  })
})
