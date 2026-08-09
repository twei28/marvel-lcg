// La RESERVE du pack Brawn, et sa regle de cloisonnement.
//
// L'insert du pack :
//   « When generating resources to pay a cost, a player cannot generate
//     resources by discarding cards from both their reserve and their hand;
//     they must choose one or the other. »
//
// Le moteur applique deja la moitie DETERMINISTE de la regle : une carte jouee
// depuis la main ne se finance que par la main, une carte jouee depuis la
// reserve que par la reserve (# CORRECTIF de game/ability/factory/resources.py).
//
// Reste le cas ou le cout n'appartient a aucune des deux zones — capacite d'une
// carte EN JEU, ou cout d'une carte de rencontre. Le moteur dresse alors la
// liste des payeurs AVANT tout choix du joueur, et propose donc legitimement
// les deux zones. C'est le plateau qui doit fermer le melange, au moment ou le
// joueur clique. C'est ce que ces tests verrouillent.

import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, type Demande } from './ask'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import type { World } from './world'

const CHO_S_LAB = 20 // le soutien EN JEU qui porte l'action a payer
const MAIN_A = 45
const MAIN_B = 46
const RESERVE_A = 60
const RESERVE_B = 61

function carte(id: number, extra: Record<string, unknown> = {}) {
  return {
    id,
    card_type: 'event',
    name: `Carte ${id}`,
    card_id: `7700${id}`,
    resources: [],
    info: {},
    traits: {},
    buffs: {},
    ...extra,
  }
}

const MONDE = {
  render_id: 1,
  players: [
    {
      area_hero: [carte(1, { card_type: 'hero' })],
      supports: [carte(CHO_S_LAB, { card_type: 'support' })],
      hand_cards: [
        carte(MAIN_A, { resources: [MAIN_A] }),
        carte(MAIN_B, { resources: [MAIN_B] }),
      ],
      reserve: [
        carte(RESERVE_A, { resources: [RESERVE_A] }),
        carte(RESERVE_B, { resources: [RESERVE_B] }),
      ],
    },
  ],
} as unknown as World

/**
 * Une action portee par une carte EN JEU, a payer 2. Le moteur propose les
 * quatre payeurs : deux en main, deux en reserve. C'est exactement le cas que
 * lui seul ne peut pas trancher.
 */
function demandeBrute(): Record<string, unknown> {
  return {
    options_json: JSON.stringify([
      {
        id: 44,
        name: 'Action',
        bind_id: CHO_S_LAB,
        bind_player_id: 0,
        all_legal_targets: [],
        target_num_range: [0, 0],
        target_payment: {
          '0': {
            cost: '2',
            payment: [
              { [MAIN_A]: 'B' },
              { [MAIN_B]: 'B' },
              { [RESERVE_A]: 'B' },
              { [RESERVE_B]: 'B' },
            ],
            rule: [],
          },
        },
        select_rule: '',
        target_must_include_traits: [],
        failure_reason: '',
        is_search: false,
      },
    ]),
    prompt_text: '',
    event_name: 'test-reserve',
    show_cancel: true,
    ability_type: '',
  }
}

const CATALOGUE: Catalogue = {
  pvMax: () => undefined,
  statImprimee: () => undefined,
  motsCles: () => [],
  surpayable: () => false,
} as unknown as Catalogue

function monter(demande: Demande) {
  const affiches = new Set([CHO_S_LAB, MAIN_A, MAIN_B, RESERVE_A, RESERVE_B])
  return renderHook(() =>
    useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple')
  )
}

describe('cloisonnement main / reserve', () => {
  it('propose les quatre payeurs tant que rien n est engage', () => {
    const demande = lireDemande(demandeBrute())!
    const { result } = monter(demande)

    act(() => result.current.choisirOption(demande.options[0]!))

    for (const id of [MAIN_A, MAIN_B, RESERVE_A, RESERVE_B]) {
      expect(result.current.cartes.get(id)?.agir).toBeTypeOf('function')
    }
  })

  it('ferme la reserve des qu une carte de la main a paye', () => {
    const demande = lireDemande(demandeBrute())!
    const { result } = monter(demande)

    act(() => result.current.choisirOption(demande.options[0]!))
    act(() => result.current.cartes.get(MAIN_A)!.agir!())

    // L'autre carte de la MAIN reste disponible : c'est la meme zone.
    expect(result.current.cartes.get(MAIN_B)?.agir).toBeTypeOf('function')

    // La reserve, elle, n'est plus cliquable du tout.
    expect(result.current.cartes.get(RESERVE_A)?.agir).toBeUndefined()
    expect(result.current.cartes.get(RESERVE_B)?.agir).toBeUndefined()
  })

  it('ferme la main des qu une carte de la reserve a paye', () => {
    const demande = lireDemande(demandeBrute())!
    const { result } = monter(demande)

    act(() => result.current.choisirOption(demande.options[0]!))
    act(() => result.current.cartes.get(RESERVE_A)!.agir!())

    expect(result.current.cartes.get(RESERVE_B)?.agir).toBeTypeOf('function')
    expect(result.current.cartes.get(MAIN_A)?.agir).toBeUndefined()
    expect(result.current.cartes.get(MAIN_B)?.agir).toBeUndefined()
  })

  it('rouvre l autre zone quand on reprend la ressource posee', () => {
    const demande = lireDemande(demandeBrute())!
    const { result } = monter(demande)

    act(() => result.current.choisirOption(demande.options[0]!))
    act(() => result.current.cartes.get(MAIN_A)!.agir!())
    expect(result.current.cartes.get(RESERVE_A)?.agir).toBeUndefined()

    // La carte deja posee reste TOUJOURS cliquable, sinon le joueur ne pourrait
    // plus revenir en arriere et resterait coince dans la mauvaise zone.
    expect(result.current.cartes.get(MAIN_A)?.agir).toBeTypeOf('function')
    act(() => result.current.cartes.get(MAIN_A)!.agir!())

    expect(result.current.cartes.get(RESERVE_A)?.agir).toBeTypeOf('function')
  })
})
