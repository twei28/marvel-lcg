// Le scenario qui a casse : « Choisis les cibles 0/3 », et apres la premiere
// designation le plateau bascule sur « Paie 0/1 » — les cibles 2 et 3 ne sont
// plus cliquables du tout, alors que la carte en annonce trois.
//
// La cause etait un couplage : l'etape courante pilotait A LA FOIS le texte
// affiche et le droit de cliquer. Des qu'un cout restait du, l'etape passait a
// « payment » et les cibles perdaient leur `agir`. Ces tests verrouillent la
// separation des deux.

import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { Demande, Option } from './ask'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import type { World } from './world'

const HEROS = 100
const CIBLES = [201, 202, 203]
const RESSOURCE = 300
const EFFET_RESSOURCE = 7

function carte(id: number, extra: Record<string, unknown> = {}) {
  return {
    id,
    card_type: 'ally',
    name: `Carte ${id}`,
    card_id: `0100${id}`,
    resources: [],
    info: {},
    traits: {},
    buffs: {},
    ...extra,
  }
}

/** Un monde minimal : `indexerCartes` ne retient que `id` + `card_type`. */
const MONDE = {
  render_id: 1,
  players: [
    {
      area_hero: [carte(HEROS, { card_type: 'hero' })],
      area_ally: CIBLES.map((id) => carte(id)),
      // La carte qui paie porte l'effet de ressource attendu.
      hand: [carte(RESSOURCE, { card_type: 'event', resources: [EFFET_RESSOURCE] })],
    },
  ],
} as unknown as World

/** Une action « jusqu'a 3 cibles », qui coute 1 ressource. */
function optionTroisCibles(): Option {
  return {
    id: 1,
    name: 'Play',
    bind_id: HEROS,
    bind_player_id: 0,
    all_legal_targets: [...CIBLES],
    target_num_range: [1, 3],
    target_payment: {
      0: {
        cost: '1',
        payment: [{ effect_id: EFFET_RESSOURCE, res_text: '1' }],
        rule: [],
      },
    },
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

const CATALOGUE: Catalogue = {
  pvMax: () => undefined,
  statImprimee: () => undefined,
  motsCles: () => [],
  surpayable: () => false,
  type: () => undefined,
} as unknown as Catalogue

function monter(option: Option) {
  const demande: Demande = {
    options: [option],
    refus: [],
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
  const affiches = new Set([HEROS, RESSOURCE, ...CIBLES])
  return renderHook(() =>
    useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple')
  )
}

describe('useInteraction, action a plusieurs cibles', () => {
  it('laisse designer les cibles 2 et 3 alors que le cout reste du', () => {
    const { result } = monter(optionTroisCibles())

    act(() => result.current.choisirOption(optionTroisCibles()))
    expect(result.current.assistant.etape).toBe('target')
    expect(result.current.assistant.cibleMaximum).toBe(3)

    // Premiere cible : le minimum est atteint, mais le cout de 1 devient du.
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())
    expect(result.current.assistant.cibleNombre).toBe(1)

    // C'est ICI que tout se jouait : l'etape basculait sur « payment » et les
    // deux cibles restantes n'avaient plus d'action.
    expect(result.current.assistant.etape).toBe('target')
    expect(result.current.cartes.get(CIBLES[1])?.agir).toBeTypeOf('function')
    expect(result.current.cartes.get(CIBLES[2])?.agir).toBeTypeOf('function')

    act(() => result.current.cartes.get(CIBLES[1])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[2])?.agir?.())
    expect(result.current.assistant.cibleNombre).toBe(3)
  })

  it('laisse payer sans imposer d ordre, des le choix de la premiere cible', () => {
    const { result } = monter(optionTroisCibles())

    act(() => result.current.choisirOption(optionTroisCibles()))
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())

    // Le texte parle encore des cibles, mais la ressource reste depensable :
    // annoncer les cibles d'abord ne doit pas bloquer le paiement.
    expect(result.current.cartes.get(RESSOURCE)?.agir).toBeTypeOf('function')
    act(() => result.current.cartes.get(RESSOURCE)?.agir?.())
    expect(result.current.prete).toBe(true)
  })

  it('n a plus rien a demander quand le maximum de cibles est atteint', () => {
    const { result } = monter(optionTroisCibles())

    act(() => result.current.choisirOption(optionTroisCibles()))
    for (const cible of CIBLES) {
      act(() => result.current.cartes.get(cible)?.agir?.())
    }
    // Trois sur trois : plus de cible a prendre, le cout passe devant.
    expect(result.current.assistant.etape).toBe('payment')
  })

  it('ne reste pas bloque a l etape des cibles quand une seule carte est visable', () => {
    const option = optionTroisCibles()
    option.all_legal_targets = [CIBLES[0]]
    const { result } = monter(option)

    act(() => result.current.choisirOption(option))
    // Le maximum annonce est 3, mais la table n'offre qu'une carte : sans le
    // plafond reel, l'assistant reclamait indefiniment des cibles absentes.
    expect(result.current.assistant.etape).toBe('payment')
  })
})

describe('useInteraction, design essai : les types qui manquent', () => {
  it('expose les types manquants pour la phrase d’état', () => {
    const option = optionTroisCibles()
    option.target_payment = {
      0: { cost: 'Y', payment: [{ effect_id: EFFET_RESSOURCE, res_text: 'Y' }], rule: [] },
    }
    const demande: Demande = {
      options: [option],
      refus: [],
      prompt_text: '',
      event_name: 'test',
      show_cancel: true,
      ability_type: '',
    }
    const affiches = new Set([HEROS, RESSOURCE, ...CIBLES])
    const { result } = renderHook(() =>
      useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple')
    )
    act(() => result.current.choisirOption(option))
    expect(result.current.assistant.typesManquants).toEqual({ Y: 1 })
  })
})
