// Alopex (TMNT, `ta`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_alopex.py` prouve ce que le moteur FAIT ; ce fichier prouve ce
// que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main
// l'état d'arrivée que le moteur publie et on affirme sur `dessinee(...)`.
//
// Cartes concernées (elles attachent, posent un compteur ou un statut, mettent
// de côté) : ta001a/ta011 (Prey attachée à un ennemi ou une manigance), ta001b
// (Prey mise de côté, Kama mises en jeu inclinées), ta002/ta003/ta014 (Cloaked),
// ta002/ta003 (Dazed), ta008 (compteurs de chasseur, dépensables), ta009/ta010
// (Kama inclinées). Sans cas : ta004-ta007, ta012, ta013, ta015 (ne font que
// chiffrer, défausser ou piocher).
//
// Pas de panorama des paires jumelles 14/15 (ta009/ta010) : à trancher par
// l'utilisateur (voir .planning/tmnt/alopex-questions.md).
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, type Demande } from './ask'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const IDENTITE = 1
const ENNEMI = 50
const COMPLOT = 60
const PREY = 2

const heros = (extra: Record<string, unknown> = {}) => carte(IDENTITE, 'ta001a', 'Hero', 'Alopex', extra)

describe('ta011 Prey : attachée à l ennemi attaqué ou à la manigance contrée (Matagi)', () => {
  it('Prey pend à l ennemi', () => {
    const monde = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(ENNEMI, '01094', 'EncounterVillain', 'Rhino'),
        carte(PREY, 'ta011', 'Upgrade', 'Prey', { bind_object_id: ENNEMI }),
      ],
    })
    expect(dessinee(monde, PREY)).toBeDefined()
    expect(dessinee(monde, PREY)?.portePar).toBe(ENNEMI)
  })

  it('Prey pend à la manigance, pas à l ennemi', () => {
    const monde = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [carte(ENNEMI, '01094', 'EncounterVillain', 'Rhino')],
      area_schemes_main: [
        carte(COMPLOT, '01097b', 'MainScheme', 'The Break-In!'),
        carte(PREY, 'ta011', 'Upgrade', 'Prey', { bind_object_id: COMPLOT }),
      ],
    })
    expect(dessinee(monde, PREY)?.portePar).toBe(COMPLOT)
  })

  it('Prey mise de côté (ennemi vaincu) : plus rien n est dessiné sur la table', () => {
    const monde = tableAvec(
      siege({
        area_hero: [heros()],
        additional_discard_pile: [carte(PREY, 'ta011', 'Upgrade', 'Prey')],
        set_aside_deck: [carte(PREY, 'ta011', 'Upgrade', 'Prey')],
      }),
      { area_villain: [carte(ENNEMI, '01094', 'EncounterVillain', 'Rhino')] }
    )
    const vue = dessinee(monde, PREY)
    expect(vue?.portePar ?? 0).not.toBe(ENNEMI)
  })
})

describe('ta002 / ta003 / ta014 : états Cloaked et Dazed dessinés', () => {
  it('Dazed est dessinée sur l ennemi hébété (ta002 Nobody, ta003 Bold Strategy)', () => {
    const monde = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(ENNEMI, '01094', 'EncounterVillain', 'Rhino'),
        carte(70, 'dazed', 'StatusCard', 'dazed', { bind_object_id: ENNEMI }),
      ],
    })
    const vue = dessinee(monde, 70)
    expect(vue?.kind).toBe('status')
    expect(vue?.codeCarte).toBe('dazed')
    expect(vue?.portePar).toBe(ENNEMI)
  })

  it('Cloaked est dessinée sur Alopex (ta003) et sur Kitsune (ta014)', () => {
    const monde = tableAvec(
      siege({
        area_hero: [heros(), carte(71, 'cloaked', 'StatusCard', 'cloaked', { bind_object_id: IDENTITE })],
        engaged_enemies: [
          carte(72, 'ta014', 'Minion', 'Kitsune'),
          carte(73, 'cloaked', 'StatusCard', 'cloaked', { bind_object_id: 72 }),
        ],
      })
    )
    expect(dessinee(monde, 71)?.portePar).toBe(IDENTITE)
    expect(dessinee(monde, 73)?.portePar).toBe(72)
    expect(dessinee(monde, 73)?.codeCarte).toBe('cloaked')
  })

  it('ta014 Kitsune inclut l identité inclinée', () => {
    const monde = tableAvec(siege({ area_hero: [heros({ is_ready: false })] }))
    expect(dessinee(monde, IDENTITE)?.exhausted).toBe(true)
  })
})

describe('ta001b / ta009 / ta010 : Kama mises en jeu inclinées', () => {
  it('les deux Kama sont dessinées attachées à l identité, couchées', () => {
    const monde = tableAvec(
      siege({
        area_hero: [
          carte(IDENTITE, 'ta001b', 'AlterEgo', 'Alopex'),
          carte(11, 'ta009', 'Upgrade', "Alopex's Kama", { bind_object_id: IDENTITE, is_ready: false }),
          carte(12, 'ta010', 'Upgrade', "Alopex's Other Kama", { bind_object_id: IDENTITE, is_ready: false }),
        ],
      })
    )
    for (const id of [11, 12]) {
      expect(dessinee(monde, id)).toBeDefined()
      expect(dessinee(monde, id)?.exhausted).toBe(true)
    }
  })
})

describe('ta008 Kitsune Kabuki : compteurs de chasseur', () => {
  const kabuki = (n: number, extra: Record<string, unknown> = {}) =>
    carte(20, 'ta008', 'Upgrade', 'Kitsune Kabuki', {
      bind_object_id: IDENTITE,
      info: n > 0 ? { c_hunter: n } : {},
      ...extra,
    })

  it('1 compteur de chasseur est dessiné sur la carte, pas sur l identité', () => {
    const monde = tableAvec(siege({ area_hero: [heros(), kabuki(1)] }))
    expect(dessinee(monde, 20)?.compteurs.hunter).toBe(1)
    expect(dessinee(monde, IDENTITE)?.compteurs.hunter).toBeUndefined()
  })

  it('compteurs dépensés : plus aucun compteur dessiné', () => {
    const monde = tableAvec(siege({ area_hero: [heros(), kabuki(0)] }))
    expect(dessinee(monde, 20)?.compteurs.hunter).toBeUndefined()
  })
})

// ta008 : « chaque compteur de chasseur peut être dépensé comme une ressource
// [mental] » : la carte devient une source de paiement cliquable.
const EFFET_CHASSEUR = 301
const CARTE_JOUEE = 61

function monde(n: number): World {
  return tableAvec(
    siege({
      area_hero: [
        heros(),
        carte(20, 'ta008', 'Upgrade', 'Kitsune Kabuki', {
          bind_object_id: IDENTITE,
          info: { c_hunter: n },
          resources: [EFFET_CHASSEUR],
        }),
      ],
      hand_cards: [carte(CARTE_JOUEE, 'ta005', 'Event', 'Prowl')],
    })
  )
}

function demande(cout: string): Demande {
  const option = {
    id: 45,
    name: 'Play',
    bind_id: CARTE_JOUEE,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: { '0': { cost: cout, payment: [{ [EFFET_CHASSEUR]: 'B' }, { [EFFET_CHASSEUR]: 'B' }], rule: [] } },
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
  return lireDemande({
    options_json: JSON.stringify([option]),
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  })!
}

const CATALOGUE = {
  pvMax: () => undefined,
  statImprimee: () => undefined,
  motsCles: () => [],
  surpayable: () => false,
  type: () => undefined,
} as unknown as Catalogue

function monter(m: World, d: Demande) {
  const affiches = new Set(cartesDessinees(m).map((c) => c.id))
  return renderHook(() => useInteraction(m, d, vi.fn(), affiches, 0, CATALOGUE, 'simple'))
}

describe('ta008 : les compteurs de chasseur se dépensent depuis la carte dessinée', () => {
  it('la carte Kabuki devient une source de paiement cliquable', () => {
    const d = demande('1')
    const { result } = monter(monde(2), d)
    act(() => result.current.choisirOption(d.options[0]!))
    expect(result.current.cartes.get(20)?.role).toBe('ressource')
    expect(result.current.cartes.get(20)?.agir).toBeTypeOf('function')
  })

  it('cliquer la carte dépense un chasseur et remplit un cran du coût', () => {
    const d = demande('2')
    const { result } = monter(monde(2), d)
    act(() => result.current.choisirOption(d.options[0]!))
    act(() => result.current.cartes.get(20)?.agir?.())
    expect(result.current.cartes.get(20)?.choisie).toBe(true)
    expect(result.current.assistant.coutSlots.filter((s) => s.rempli).length).toBeGreaterThan(0)
  })
})
