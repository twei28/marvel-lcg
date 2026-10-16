// Leonardo (TMNT, `tl`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_leonardo.py` prouve ce que le moteur FAIT (76 cas verts) ; ce
// fichier prouve ce que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis).
// On pose à la main l'état d'arrivée que le moteur publie, et on affirme sur
// `dessinee(...)`. Les cartes qui ne font que chiffrer ou redresser sans rien
// déplacer (tl001a, tl003, tl004, tl005, tl008, tl009, tl010, tl012 hors
// ressource octroyée) n'ont pas de cas ici : leur effet est une inclinaison ou
// un chiffre, déjà couverts par la jauge et `exhausted`.
//
// Paire jumelle 14/15 (tl011 + tl012) : panorama, voir panorama-jumelles.test.tsx.
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, type Demande } from './ask'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const IDENTITE = 1

const identite = (cardId = 'tl001b', type = 'AlterEgo', nom = 'Leo') =>
  carte(IDENTITE, cardId, type, nom)

describe('tl001b Leo : deux katanas mises en jeu inclinées', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          identite(),
          carte(11, 'tl011', 'Upgrade', "Leonardo's Katana", { bind_object_id: IDENTITE, is_ready: false }),
          carte(12, 'tl012', 'Upgrade', "Leonardo's Other Katana", { bind_object_id: IDENTITE, is_ready: false }),
        ],
        player_deck: [carte(30, 'ls010', 'Upgrade', 'Autre', { is_face_up: false, visible_for_players: [] })],
      })
    )

  it('dessine les deux katanas en panorama 14|15 A COTE de l identité, couchées', () => {
    // Décision du 16/10/2026 (panorama-jumelles.ts) : la paire ne se glisse plus
    // sous l'identité, elle se pose à côté, entièrement visible.
    for (const [id, cote] of [[11, 'gauche'], [12, 'droite']] as const) {
      const vue = dessinee(monde(), id)
      expect(vue).toBeDefined()
      expect(vue?.portePar).toBe(0)
      expect(vue?.panorama).toBe(cote)
      expect(vue?.kind).toBe('upgrade')
      expect(vue?.exhausted).toBe(true)
    }
  })

  it('ne les laisse pas dans la pile du deck', () => {
    expect(dessinee(monde(), 11)?.zone).toBe('terrain-soutien')
    expect(dessinee(monde(), 30)?.zone).toBe('piles-joueur')
  })
})

describe('tl002 Splinter : la carte repose sur le dessus du deck', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [identite()],
        player_deck: [
          carte(31, 'ls001a', 'Event', 'Fond', { is_face_up: false, visible_for_players: [] }),
          carte(32, 'tl003', 'Event', 'Uke Nagashi', { is_face_up: false, visible_for_players: [] }),
        ],
        player_discard_pile: [carte(33, 'tl004', 'Event', 'Vigilant')],
      })
    )

  it('la pile du deck est représentée par la carte du dessus, dos visible', () => {
    const deck = dessinee(monde(), 32)
    expect(deck).toBeDefined()
    expect(deck?.zone).toBe('piles-joueur')
    expect(deck?.facedown).toBe(true)
    expect(deck?.pileCount).toBe(2)
  })

  it('la défausse ne montre plus la carte remontée', () => {
    expect(dessinee(monde(), 33)?.pileCount).toBe(1)
    expect(cartesDessinees(monde()).filter((c) => c.codeCarte === 'tl003')).toHaveLength(0)
  })
})

describe('tl006 Yo Ko Giri : retour en main ; tl007 Leo s Greenhouse : pioche', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          identite(),
          carte(21, 'tl007', 'Support', "Leo's Greenhouse", { is_ready: false }),
        ],
        hand_cards: [
          carte(22, 'tl006', 'Event', 'Yo Ko Giri'),
          carte(23, 'ls001a', 'Event', 'Pioche 1'),
          carte(24, 'ls001a', 'Event', 'Pioche 2'),
        ],
      })
    )

  it('l événement revenu en main est dessiné dans la main', () => {
    expect(dessinee(monde(), 22)?.zone).toBe('main')
  })

  it('les cartes piochées arrivent dans la main', () => {
    expect(cartesDessinees(monde()).filter((c) => c.zone === 'main')).toHaveLength(3)
  })

  it('la serre est dessinée inclinée', () => {
    expect(dessinee(monde(), 21)?.exhausted).toBe(true)
  })
})

describe('tl013 Brainwashed Betrayal : bascule forcée, allié défaussé, retrait du jeu', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [identite('tl001a', 'Hero', 'Leonardo')],
        obligations_area: [carte(40, 'tl013', 'Obligation', 'Brainwashed Betrayal')],
        player_discard_pile: [carte(41, 'tl002', 'Ally', 'Splinter')],
      })
    )

  it('l identité est dessinée en face héros (la bascule se voit)', () => {
    expect(dessinee(monde(), IDENTITE)?.codeCarte).toBe('tl001a')
  })

  it('l obligation est dessinée sur la table tant qu elle est en jeu', () => {
    expect(dessinee(monde(), 40)).toBeDefined()
  })

  it('l allié défaussé est sur la pile de défausse', () => {
    expect(dessinee(monde(), 41)?.zone).toBe('piles-joueur')
  })

  it('retirée du jeu, elle quitte la table et rejoint les cartes retirées', () => {
    const retiree = tableAvec(
      siege({ area_hero: [identite()], obligations_area: [] }),
      { area_removed: [carte(40, 'tl013', 'Obligation', 'Brainwashed Betrayal')] }
    )
    expect(dessinee(retiree, 40)?.zone).toBe('annexes')
  })
})

describe('tl014 Foot Patrol : le sbire du Foot Clan entre en jeu engagé', () => {
  it('le sbire mis en jeu est dessiné dans la zone de combat', () => {
    const monde = tableAvec(
      siege({
        area_hero: [identite()],
        engaged_enemies: [carte(50, 'tl016', 'Minion', 'Foot Soldiers')],
      })
    )
    expect(dessinee(monde, 50)?.zone).toBe('terrain-combat')
  })
})

describe('tl015 Karai, tl016 Foot Soldiers : le statut Cloaked', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [identite()],
        engaged_enemies: [
          carte(60, 'tl015', 'Minion', 'Karai'),
          carte(61, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 60 }),
          carte(62, 'tl016', 'Minion', 'Foot Soldiers'),
          carte(63, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 62 }),
        ],
        dealt_encounter_cards: [
          carte(64, 'tl015', 'Minion', 'Karai', { is_face_up: false, visible_for_players: [] }),
        ],
      }),
      {
        area_villain: [
          carte(70, '01094', 'EncounterVillain', 'Rhino'),
          carte(71, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 70 }),
        ],
      }
    )

  it('Karai porte une carte Cloaked dessinée sous elle', () => {
    const cloaked = dessinee(monde(), 61)
    expect(cloaked).toBeDefined()
    expect(cloaked?.kind).toBe('status')
    expect(cloaked?.codeCarte).toBe('cloaked')
    expect(cloaked?.portePar).toBe(60)
  })

  it('le sbire Foot Soldiers porte la sienne', () => {
    expect(dessinee(monde(), 63)?.portePar).toBe(62)
  })

  it('le vilain devient Cloaked quand Karai est vaincue, la carte est sur lui', () => {
    expect(dessinee(monde(), 71)?.portePar).toBe(70)
    expect(dessinee(monde(), 71)?.kind).toBe('status')
  })

  it('le boost de Karai la donne face cachée au premier joueur : on ne voit que le dos', () => {
    const donnee = dessinee(monde(), 64)
    expect(donnee).toBeDefined()
    expect(donnee?.facedown).toBe(true)
    expect(donnee?.codeCarte).toBeUndefined()
  })
})

// ---------------------------------------------------------------------------
// tl011 / tl012 : la ressource OCTROYÉE aux katanas dans la modale de paiement.
// Le moteur publie la ressource octroyée dans `resources` de CHAQUE katana
// (`Card.get_resources` lit tous les effets payants, donnés compris) et
// propose `{effet: 'G'}` dans le paiement. Le plateau doit rendre chaque katana
// cliquable comme source de paiement.
// ---------------------------------------------------------------------------
const EFFET_KATANA_1 = 101
const EFFET_KATANA_2 = 102
const KATANA_1 = 11
const KATANA_2 = 12
const CARTE_JOUEE = 22

function mondePaiement(katana1: Partial<WorldCard> = {}, katana2: Partial<WorldCard> = {}): World {
  return tableAvec(
    siege({
      area_hero: [
        identite('tl001a', 'Hero', 'Leonardo'),
        carte(KATANA_1, 'tl011', 'Upgrade', "Leonardo's Katana", {
          bind_object_id: IDENTITE,
          resources: [EFFET_KATANA_1],
          ...katana1,
        }),
        carte(KATANA_2, 'tl012', 'Upgrade', "Leonardo's Other Katana", {
          bind_object_id: IDENTITE,
          resources: [EFFET_KATANA_2],
          ...katana2,
        }),
      ],
      hand_cards: [carte(CARTE_JOUEE, 'tl004', 'Event', 'Vigilant')],
    })
  )
}

function demande(cout: string): Demande {
  const option = {
    id: 44,
    name: 'Play',
    bind_id: CARTE_JOUEE,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {
      '0': {
        cost: cout,
        payment: [{ [EFFET_KATANA_1]: 'G' }, { [EFFET_KATANA_2]: 'G' }],
        rule: [],
      },
    },
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

function monter(monde: World, d: Demande) {
  // Ce que la table dessine, plus la main : les katanas doivent y figurer.
  const affiches = new Set(cartesDessinees(monde).map((c) => c.id))
  return renderHook(() => useInteraction(monde, d, vi.fn(), affiches, 0, CATALOGUE, 'simple'))
}

describe('tl011 / tl012 : la ressource octroyée aux katanas dans le paiement', () => {
  it('les deux katanas sont dessinées sur la table (condition pour être cliquables)', () => {
    expect(dessinee(mondePaiement(), KATANA_1)).toBeDefined()
    expect(dessinee(mondePaiement(), KATANA_2)).toBeDefined()
  })

  it('chaque katana devient une source de paiement cliquable', () => {
    const d = demande('2')
    const { result } = monter(mondePaiement(), d)
    act(() => result.current.choisirOption(d.options[0]!))
    for (const id of [KATANA_1, KATANA_2]) {
      expect(result.current.cartes.get(id)?.role).toBe('ressource')
      expect(result.current.cartes.get(id)?.agir).toBeTypeOf('function')
    }
  })

  it('cliquer une katana dépense sa ressource octroyée et remplit un cran du coût', () => {
    const d = demande('2')
    const { result } = monter(mondePaiement(), d)
    act(() => result.current.choisirOption(d.options[0]!))
    act(() => result.current.cartes.get(KATANA_1)?.agir?.())
    expect(result.current.cartes.get(KATANA_1)?.choisie).toBe(true)
    expect(result.current.cartes.get(KATANA_2)?.choisie).toBeFalsy()
    expect(result.current.assistant.coutSlots.filter((s) => s.rempli)).toHaveLength(1)
    expect(result.current.assistant.coutSlots).toHaveLength(2)
  })

  it('les deux katanas ensemble paient un coût de 2', () => {
    const d = demande('2')
    const { result } = monter(mondePaiement(), d)
    act(() => result.current.choisirOption(d.options[0]!))
    act(() => result.current.cartes.get(KATANA_1)?.agir?.())
    act(() => result.current.cartes.get(KATANA_2)?.agir?.())
    expect(result.current.assistant.coutSlots.every((s) => s.rempli)).toBe(true)
  })

  // Témoin : une katana qui n'a pas reçu l'octroi (tl011 partie) n'offre rien.
  it('une katana sans ressource octroyée n est pas proposée', () => {
    const d = demande('1')
    const { result } = monter(mondePaiement({ resources: [] }), d)
    act(() => result.current.choisirOption(d.options[0]!))
    expect(result.current.cartes.get(KATANA_1)?.agir).toBeUndefined()
    expect(result.current.cartes.get(KATANA_2)?.agir).toBeTypeOf('function')
  })
})
