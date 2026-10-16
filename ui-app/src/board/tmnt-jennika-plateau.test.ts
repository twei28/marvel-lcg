// Jennika (TMNT, `tj`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `Fusion/marvel-lcg-src/tools/cas/tmnt_jennika.py` prouve ce que le moteur FAIT ; ce fichier prouve
// ce que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée que
// le moteur publie, et on affirme sur `dessinee(...)` et sur `useInteraction` (cliquable ou non).
//
// Cartes SANS cas ici, parce qu'elles ne font que chiffrer ou jouer depuis la main sans rien dessiner
// de nouveau : tj001a (bonus +1/+1/+1 : la jauge le montre déjà), tj002 (une carte revient en main),
// tj010 (+2 ATQ le temps d'une attaque : aucune trace sur la table), tj013 hors jeton de menace.
//
// Paire jumelle 14/15 (tj009 + tj010, illustration continue) : panorama CONFIRMÉ le 16/10/2026
// (panorama-jumelles.ts) ; le test ci-dessous vérifie leur placement 14|15 à côté de l'identité.
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, type Demande } from './ask'
import { kindLabel } from '../components/ScanCard'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const IDENTITE = 1
const VOIE = 10
const TEKKO_1 = 11
const TEKKO_2 = 12
const ARC = 13
const CRIB = 14
const RESOLVE = 15
const MANIGANCE = 20

const alterEgo = () => carte(IDENTITE, 'tj001b', 'AlterEgo', 'Jenny')
const heros = () => carte(IDENTITE, 'tj001a', 'Hero', 'Jennika')
const voie = (extra: Partial<WorldCard> = {}) => carte(VOIE, 'tj011', 'Path', 'Sōsaiken', extra)
const tekko1 = (extra: Partial<WorldCard> = {}) =>
  carte(TEKKO_1, 'tj009', 'Upgrade', "Jennika's Tekko-Kagi", { bind_object_id: IDENTITE, ...extra })
const tekko2 = (extra: Partial<WorldCard> = {}) =>
  carte(TEKKO_2, 'tj010', 'Upgrade', "Jennika's Other Tekko-Kagi", { bind_object_id: IDENTITE, ...extra })

describe('tj001b Jenny Setup : la Voie tj011 est posée sur la table', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [alterEgo()],
        supports: [voie()],
        hand_cards: [carte(30, 'tj002', 'Event', 'Composure')],
      })
    )

  it('la Voie est dessinée, en genre voie (Path, pas soutien), dans la zone des soutiens', () => {
    const v = dessinee(monde(), VOIE)
    expect(v).toBeDefined()
    expect(v?.kind).toBe('path')
    expect(v?.zone).toBe('terrain-soutien')
  })

  it('la Voie porte l étiquette « Voie »', () => {
    const v = dessinee(monde(), VOIE)
    expect(kindLabel.path).toBe('Voie')
    expect(v?.kind).toBe('path')
    expect(v?.kind).not.toBe('support')
  })

  it('prête à l entrée, elle n est pas couchée', () => {
    expect(dessinee(monde(), VOIE)?.exhausted).toBe(false)
  })

  it('mise de côté avant le Setup : la copie en zone de mise de côté n est PAS sur la table', () => {
    const avant = tableAvec(
      siege({ area_hero: [alterEgo()], additional_discard_pile: [voie({ is_face_up: false, visible_for_players: [] })] })
    )
    expect(cartesDessinees(avant).filter((c) => c.zone === 'terrain-soutien' && c.id === VOIE)).toHaveLength(0)
  })

  it('elle n est pas dans la main de départ', () => {
    expect(cartesDessinees(monde()).filter((c) => c.zone === 'main' && c.id === VOIE)).toHaveLength(0)
  })
})

describe('tj001b Jenny Action : deux Tekko-Kagi mises en jeu inclinées', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [alterEgo(), tekko1({ is_ready: false }), tekko2({ is_ready: false })],
        player_deck: [carte(30, 'ls010', 'Upgrade', 'Autre', { is_face_up: false, visible_for_players: [] })],
        player_discard_pile: [carte(31, 'ls001a', 'Event', 'Coût payé')],
      })
    )

  it('les deux Tekko-Kagi sont dessinées, en genre amélioration, couchées', () => {
    for (const id of [TEKKO_1, TEKKO_2]) {
      const vue = dessinee(monde(), id)
      expect(vue).toBeDefined()
      expect(vue?.kind).toBe('upgrade')
      expect(vue?.exhausted).toBe(true)
    }
  })

  it('elles ne sont plus dans la pile du deck ; la carte défaussée en coût est sur la défausse', () => {
    expect(dessinee(monde(), TEKKO_1)?.zone).toBe('terrain-soutien')
    expect(dessinee(monde(), 30)?.zone).toBe('piles-joueur')
    expect(dessinee(monde(), 31)?.zone).toBe('piles-joueur')
  })

  it('une seule trouvée : une seule Tekko-Kagi est dessinée', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo(), tekko1({ is_ready: false })] }))
    expect(dessinee(m, TEKKO_1)).toBeDefined()
    expect(dessinee(m, TEKKO_2)).toBeUndefined()
  })
})

describe('tj005 Moonlighting, tj014 Phantasm, tj015 Street Phantoms : la carte d état Cloaked', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros(), carte(70, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: IDENTITE })],
        engaged_enemies: [
          carte(60, 'tj015', 'Minion', 'Street Phantoms'),
          carte(61, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 60 }),
          carte(62, 'tj014', 'Minion', 'Phantasm'),
        ],
      })
    )

  it('Jennika porte sa carte Cloaked (Moonlighting)', () => {
    const c = dessinee(monde(), 70)
    expect(c?.kind).toBe('status')
    expect(c?.codeCarte).toBe('cloaked')
    expect(c?.portePar).toBe(IDENTITE)
  })

  it('Street Phantoms porte la sienne (Cloak Street Phantoms)', () => {
    expect(dessinee(monde(), 61)?.portePar).toBe(60)
    expect(dessinee(monde(), 61)?.kind).toBe('status')
  })

  it('Phantasm, non camouflé, ne porte aucune carte d état', () => {
    expect(cartesDessinees(monde()).filter((c) => c.portePar === 62)).toHaveLength(0)
  })

  it('Phantasm vaincu : chaque sbire PHANTOMS en jeu reçoit sa carte (deux sbires, deux cartes)', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros()],
        engaged_enemies: [
          carte(60, 'tj015', 'Minion', 'Street Phantoms'),
          carte(61, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 60 }),
          carte(63, 'tj015', 'Minion', 'Street Phantoms'),
          carte(64, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 63 }),
        ],
      }),
      { encounter_discard_pile: [carte(62, 'tj014', 'Minion', 'Phantasm')] }
    )
    expect(dessinee(m, 61)?.portePar).toBe(60)
    expect(dessinee(m, 64)?.portePar).toBe(63)
    expect(dessinee(m, 62)?.zone).toBe('piles-rencontre')
  })
})

describe('tj003 Apparition, tj004 Decisive Strike : Désorienté et Sonné posés sur l ennemi', () => {
  it('la carte de statut est dessinée sur l ennemi', () => {
    for (const statut of ['confused', 'stunned']) {
      const m = tableAvec(siege({ area_hero: [heros()] }), {
        area_villain: [
          carte(80, '01094', 'EncounterVillain', 'Rhino'),
          carte(81, statut, 'StatusCard', statut, { bind_object_id: 80 }),
        ],
      })
      expect(dessinee(m, 81)?.portePar).toBe(80)
      expect(dessinee(m, 81)?.codeCarte).toBe(statut)
    }
  })
})

describe('tj006 Fearless Resolve : les compteurs de samouraï sont dessinés', () => {
  const resolve = (samurai: number) =>
    carte(RESOLVE, 'tj006', 'Upgrade', 'Fearless Resolve', { bind_object_id: IDENTITE, info: { c_samurai: samurai } })
  const mondeAvec = (...cartes: WorldCard[]) => tableAvec(siege({ area_hero: [heros(), ...cartes] }))

  it('elle entre avec 2 compteurs', () => {
    expect(dessinee(mondeAvec(resolve(2)), RESOLVE)?.compteurs.samurai).toBe(2)
  })

  it('en genre amélioration, attachée à Jennika', () => {
    expect(dessinee(mondeAvec(resolve(2)), RESOLVE)?.kind).toBe('upgrade')
  })

  it('après l action : plus sur la table, dans la défausse du joueur ; Jennika est redressée', () => {
    const m = tableAvec(siege({ area_hero: [heros()], player_discard_pile: [resolve(0)] }))
    expect(dessinee(m, RESOLVE)?.zone).toBe('piles-joueur')
    expect(dessinee(m, IDENTITE)?.exhausted).toBe(false)
  })

  it('l action coûte l inclinaison : la carte restante, inclinée, est couchée', () => {
    expect(dessinee(mondeAvec({ ...resolve(2), is_ready: false } as WorldCard), RESOLVE)?.exhausted).toBe(true)
  })
})

describe('tj007 Jenny s Crib : la Crib s incline, l identité se redresse', () => {
  it('la Crib est dessinée couchée, l identité est prête', () => {
    const m = tableAvec(
      siege({
        area_hero: [alterEgo()],
        supports: [carte(CRIB, 'tj007', 'Support', "Jenny's Crib", { is_ready: false })],
      })
    )
    expect(dessinee(m, CRIB)?.exhausted).toBe(true)
    expect(dessinee(m, CRIB)?.kind).toBe('support')
    expect(dessinee(m, IDENTITE)?.exhausted).toBe(false)
  })

  it('avant l action : identité inclinée, Crib prête', () => {
    const m = tableAvec(
      siege({
        area_hero: [{ ...alterEgo(), is_ready: false } as WorldCard],
        supports: [carte(CRIB, 'tj007', 'Support', "Jenny's Crib")],
      })
    )
    expect(dessinee(m, IDENTITE)?.exhausted).toBe(true)
    expect(dessinee(m, CRIB)?.exhausted).toBe(false)
  })
})

describe('tj008 Jennika s Bow : l arc s incline, puis se redresse', () => {
  const arc = (extra: Partial<WorldCard> = {}) =>
    carte(ARC, 'tj008', 'Upgrade', "Jennika's Bow", { bind_object_id: IDENTITE, ...extra })

  it('après la Hero Action : l arc est couché', () => {
    const m = tableAvec(siege({ area_hero: [heros(), arc({ is_ready: false })] }))
    expect(dessinee(m, ARC)?.exhausted).toBe(true)
    expect(dessinee(m, ARC)?.kind).toBe('upgrade')
  })

  it('après la Hero Response : l arc est redressé', () => {
    const m = tableAvec(siege({ area_hero: [heros(), arc()] }))
    expect(dessinee(m, ARC)?.exhausted).toBe(false)
  })
})

describe('tj011 Sōsaiken : la Voie s incline après sa Réponse', () => {
  it('couchée après avoir pioché ; la carte piochée est dans la main', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros()],
        supports: [voie({ is_ready: false })],
        hand_cards: [carte(31, 'ls001a', 'Event', 'Piochée')],
      })
    )
    expect(dessinee(m, VOIE)?.exhausted).toBe(true)
    expect(dessinee(m, 31)?.zone).toBe('main')
  })
})

describe('tj012 Personality Adjustment : obligation en jeu, retirée de la partie ou défaussée', () => {
  it('en jeu : elle est dessinée dans la zone des obligations', () => {
    const m = tableAvec(siege({ area_hero: [heros()], obligations_area: [carte(40, 'tj012', 'Obligation', 'Personality Adjustment')] }))
    expect(dessinee(m, 40)).toBeDefined()
    expect(dessinee(m, 40)?.kind).toBe('obligation')
  })

  it('retirée de la partie (Exhaust Jenny) : elle quitte les obligations et rejoint les cartes retirées', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo()], obligations_area: [] }), {
      area_removed: [carte(40, 'tj012', 'Obligation', 'Personality Adjustment')],
    })
    expect(dessinee(m, 40)?.zone).toBe('annexes')
  })

  it('défaussée (3 menaces posées) : dans la défausse de rencontre, la menace du principal monte', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo()], obligations_area: [] }), {
      encounter_discard_pile: [carte(40, 'tj012', 'Obligation', 'Personality Adjustment')],
      area_schemes_main: [carte(41, '01097b', 'MainScheme', 'The Break-In!', { info: { k_threat: 7 } })],
    })
    expect(dessinee(m, 40)?.zone).toBe('piles-rencontre')
    expect(dessinee(m, 41)?.menace).toBe(7)
  })
})

describe('tj013 Dun Import Exports : Entrave 1, le jeton de menace est dessiné', () => {
  it('une manigance annexe avec 1 jeton de menace', () => {
    const m = tableAvec(siege({ area_hero: [heros()] }), {
      area_schemes_side: [carte(MANIGANCE, 'tj013', 'SideScheme', 'Dun Import Exports', { info: { k_threat: 1 } })],
    })
    expect(dessinee(m, MANIGANCE)?.zone).toBe('complots-secondaires')
    expect(dessinee(m, MANIGANCE)?.menace).toBe(1)
  })

  it('à deux joueurs : 2 jetons ; sans menace aucun jeton dessiné', () => {
    const deux = tableAvec(siege({ area_hero: [heros()] }), {
      area_schemes_side: [carte(MANIGANCE, 'tj013', 'SideScheme', 'Dun Import Exports', { info: { k_threat: 2 } })],
    })
    expect(dessinee(deux, MANIGANCE)?.menace).toBe(2)
    const vide = tableAvec(siege({ area_hero: [heros()] }), {
      area_schemes_side: [carte(MANIGANCE, 'tj013', 'SideScheme', 'Dun Import Exports', { info: { k_threat: 0 } })],
    })
    expect(dessinee(vide, MANIGANCE)?.menace).toBeUndefined()
  })
})

// ---------------------------------------------------------------------------
// tj009 : la ressource OCTROYÉE aux Tekko-Kagi dans la modale de paiement.
// Le moteur publie la ressource octroyée dans `resources` de CHAQUE Tekko-Kagi (`Card.get_resources`
// lit tous les effets payants, donnés compris) et propose `{effet: 'G'}` dans le paiement : le
// plateau doit rendre chaque Tekko-Kagi cliquable comme source de paiement.
// ---------------------------------------------------------------------------
const EFFET_TEKKO_1 = 101
const EFFET_TEKKO_2 = 102
const CARTE_JOUEE = 22

function mondePaiement(t1: Partial<WorldCard> = {}, t2: Partial<WorldCard> = {}): World {
  return tableAvec(
    siege({
      area_hero: [
        heros(),
        tekko1({ resources: [EFFET_TEKKO_1], ...t1 }),
        tekko2({ resources: [EFFET_TEKKO_2], ...t2 }),
      ],
      hand_cards: [carte(CARTE_JOUEE, 'tj004', 'Event', 'Decisive Strike')],
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
        payment: [{ [EFFET_TEKKO_1]: 'G' }, { [EFFET_TEKKO_2]: 'G' }],
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
  // Ce que la table dessine, plus la main : les Tekko-Kagi doivent y figurer.
  const affiches = new Set(cartesDessinees(monde).map((c) => c.id))
  return renderHook(() => useInteraction(monde, d, vi.fn(), affiches, 0, CATALOGUE, 'simple'))
}

describe('tj009 / tj010 : la ressource octroyée aux Tekko-Kagi dans le paiement', () => {
  it('les deux Tekko-Kagi sont dessinées sur la table (condition pour être cliquables)', () => {
    expect(dessinee(mondePaiement(), TEKKO_1)).toBeDefined()
    expect(dessinee(mondePaiement(), TEKKO_2)).toBeDefined()
  })

  it('chaque Tekko-Kagi devient une source de paiement cliquable', () => {
    const d = demande('2')
    const { result } = monter(mondePaiement(), d)
    act(() => result.current.choisirOption(d.options[0]!))
    for (const id of [TEKKO_1, TEKKO_2]) {
      expect(result.current.cartes.get(id)?.role).toBe('ressource')
      expect(result.current.cartes.get(id)?.agir).toBeTypeOf('function')
    }
  })

  it('cliquer une Tekko-Kagi dépense sa ressource octroyée et remplit un cran du coût', () => {
    const d = demande('2')
    const { result } = monter(mondePaiement(), d)
    act(() => result.current.choisirOption(d.options[0]!))
    act(() => result.current.cartes.get(TEKKO_1)?.agir?.())
    expect(result.current.cartes.get(TEKKO_1)?.choisie).toBe(true)
    expect(result.current.cartes.get(TEKKO_2)?.choisie).toBeFalsy()
    expect(result.current.assistant.coutSlots.filter((s) => s.rempli)).toHaveLength(1)
    expect(result.current.assistant.coutSlots).toHaveLength(2)
  })

  it('les deux Tekko-Kagi ensemble paient un coût de 2', () => {
    const d = demande('2')
    const { result } = monter(mondePaiement(), d)
    act(() => result.current.choisirOption(d.options[0]!))
    act(() => result.current.cartes.get(TEKKO_1)?.agir?.())
    act(() => result.current.cartes.get(TEKKO_2)?.agir?.())
    expect(result.current.assistant.coutSlots.every((s) => s.rempli)).toBe(true)
  })

  // Témoin : une Tekko-Kagi qui n'a pas reçu l'octroi n'offre rien.
  it('une Tekko-Kagi sans ressource octroyée n est pas proposée', () => {
    const d = demande('1')
    const { result } = monter(mondePaiement({ resources: [] }), d)
    act(() => result.current.choisirOption(d.options[0]!))
    expect(result.current.cartes.get(TEKKO_1)?.agir).toBeUndefined()
    expect(result.current.cartes.get(TEKKO_2)?.agir).toBeTypeOf('function')
  })
})

describe('tj009 / tj010 : panorama des Tekko-Kagi', () => {
  it('les deux Tekko-Kagi sont en panorama 14|15 à côté de l identité', () => {
    const monde = tableAvec(
      siege({
        area_hero: [
          carte(IDENTITE, 'tj001b', 'AlterEgo', 'Jenny'),
          carte(TEKKO_1, 'tj009', 'Upgrade', "Jennika's Tekko-Kagi", { bind_object_id: IDENTITE }),
          carte(TEKKO_2, 'tj010', 'Upgrade', "Jennika's Other Tekko-Kagi", { bind_object_id: IDENTITE }),
        ],
      })
    )
    expect(dessinee(monde, TEKKO_1)?.panorama).toBe('gauche')
    expect(dessinee(monde, TEKKO_2)?.panorama).toBe('droite')
  })
})
