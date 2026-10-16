// Michelangelo (TMNT, `tm`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_michelangelo.py` prouve ce que le moteur FAIT (92 cas verts) ;
// ce fichier prouve ce que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis).
// On pose à la main l'état d'arrivée que le moteur publie, et on affirme sur
// `dessinee(...)` et sur `useInteraction` (cliquable ou non).
//
// Cartes SANS cas ici, parce qu'elles ne font que chiffrer ou jouer depuis la
// main sans rien dessiner de nouveau : tm003 (une carte en main), tm004,
// tm006 (dégâts), tm007 (soin + pioche), tm008 (défausse -> deck : couvert par
// `pileCount`, cf. tl002), tm010 (bascule de forme + inclinaison), tm016
// (dégâts indirects). Aucune carte Michelangelo ne pose de compteur : Booyakasha
// déplace de la MENACE (jeton de menace des manigances), pas un compteur.
//
// Pas de panorama des paires jumelles 14/15 (travail ultérieur).
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, type Demande } from './ask'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const IDENTITE = 1
const NUNCHUCK_1 = 11
const NUNCHUCK_2 = 12
const MANIGANCE = 20

const alterEgo = () => carte(IDENTITE, 'tm001b', 'AlterEgo', 'Mikey')
const heros = () => carte(IDENTITE, 'tm001a', 'Hero', 'Michelangelo')
const nunchuck1 = (extra: Partial<WorldCard> = {}) =>
  carte(NUNCHUCK_1, 'tm011', 'Upgrade', "Michelangelo's Nunchuck", { bind_object_id: IDENTITE, ...extra })
const nunchuck2 = (extra: Partial<WorldCard> = {}) =>
  carte(NUNCHUCK_2, 'tm012', 'Upgrade', "Michelangelo's Other Nunchuck", { bind_object_id: IDENTITE, ...extra })
const manigance = (menace: number, id = MANIGANCE) =>
  carte(id, 'tm009', 'PlayerSideScheme', "I'm Here to Help", { info: { k_threat: menace } })

describe('tm001b Mikey : Setup, tm009 posée sur la table', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [alterEgo()],
        player_deck: [carte(30, 'ls010', 'Upgrade', 'Autre', { is_face_up: false, visible_for_players: [] })],
      }),
      { area_schemes_side: [manigance(3)] }
    )

  it('la manigance est dessinée avec ses 3 jetons de menace', () => {
    expect(dessinee(monde(), MANIGANCE)).toBeDefined()
    expect(dessinee(monde(), MANIGANCE)?.menace).toBe(3)
  })

  it('elle est dans la zone des manigances annexes, pas dans le deck', () => {
    expect(dessinee(monde(), MANIGANCE)?.zone).toBe('complots-secondaires')
    expect(dessinee(monde(), 30)?.zone).toBe('piles-joueur')
  })

  it('posée depuis la main (mulligan, défausse) : plus dans la main', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo()], hand_cards: [] }), { area_schemes_side: [manigance(3)] })
    expect(cartesDessinees(m).filter((c) => c.zone === 'main')).toHaveLength(0)
    expect(dessinee(m, MANIGANCE)).toBeDefined()
  })
})

describe('tm001b Mikey : deux Nunchuck mis en jeu inclinés par la recherche', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [alterEgo(), nunchuck1({ is_ready: false }), nunchuck2({ is_ready: false })],
        player_deck: [carte(30, 'ls010', 'Upgrade', 'Autre', { is_face_up: false, visible_for_players: [] })],
        player_discard_pile: [carte(31, 'ls001a', 'Event', 'Coût payé')],
      })
    )

  it('les deux Nunchuck sont dessinés sur l identité, couchés', () => {
    for (const id of [NUNCHUCK_1, NUNCHUCK_2]) {
      const vue = dessinee(monde(), id)
      expect(vue).toBeDefined()
      expect(vue?.portePar).toBe(IDENTITE)
      expect(vue?.kind).toBe('upgrade')
      expect(vue?.exhausted).toBe(true)
    }
  })

  it('ils ne sont plus dans la pile du deck, la carte défaussée en coût est sur la défausse', () => {
    expect(dessinee(monde(), NUNCHUCK_1)?.zone).toBe('terrain-soutien')
    expect(dessinee(monde(), 30)?.zone).toBe('piles-joueur')
    expect(dessinee(monde(), 31)?.zone).toBe('piles-joueur')
  })

  it('un seul trouvé : un seul Nunchuck est dessiné', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo(), nunchuck1({ is_ready: false })] }))
    expect(dessinee(m, NUNCHUCK_1)).toBeDefined()
    expect(dessinee(m, NUNCHUCK_2)).toBeUndefined()
  })
})

describe('tm001a Booyakasha : la menace déplacée d une manigance à l autre', () => {
  const principale = (menace: number) =>
    carte(40, 'ms001a', 'MainScheme', 'Complot', { info: { k_threat: menace } })

  it('les deux jetons de menace reflètent le nouvel état', () => {
    const m = tableAvec(siege({ area_hero: [heros()] }), {
      area_schemes_main: [principale(5)],
      area_schemes_side: [manigance(1)],
    })
    expect(dessinee(m, MANIGANCE)?.menace).toBe(1)
    expect(dessinee(m, 40)?.menace).toBe(5)
  })

  it('annexe vidée = vaincue : plus de carte sur la table (jeton absent, pas de zéro dessiné)', () => {
    const m = tableAvec(siege({ area_hero: [heros()], player_discard_pile: [manigance(0)] }), {
      area_schemes_main: [principale(8)],
      area_schemes_side: [],
    })
    expect(dessinee(m, MANIGANCE)?.zone).toBe('piles-joueur')
    expect(dessinee(m, 40)?.menace).toBe(8)
  })

  it('une menace à zéro n a pas de jeton', () => {
    const m = tableAvec(siege({ area_hero: [heros()] }), {
      area_schemes_main: [principale(0)],
    })
    expect(dessinee(m, 40)?.menace).toBeUndefined()
  })
})

describe('tm009 I m Here to Help : menace retirée, vaincue, pioche de 3 cartes', () => {
  it('la menace retirée en fin de phase des joueurs se voit sur le jeton', () => {
    const m = tableAvec(siege({ area_hero: [heros()] }), { area_schemes_side: [manigance(2)] })
    expect(dessinee(m, MANIGANCE)?.menace).toBe(2)
  })

  it('vaincue : elle quitte la table, 3 cartes arrivent dans la main', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros()],
        hand_cards: [
          carte(50, 'ls001a', 'Event', 'A'),
          carte(51, 'ls001a', 'Event', 'B'),
          carte(52, 'ls001a', 'Event', 'C'),
        ],
        player_discard_pile: [manigance(0)],
      }),
      { area_schemes_side: [] }
    )
    expect(dessinee(m, MANIGANCE)?.zone).toBe('piles-joueur')
    expect(cartesDessinees(m).filter((c) => c.zone === 'main')).toHaveLength(3)
  })
})

describe('tm002 Slash, tm015 Wyrm : le statut Tough', () => {
  it('la carte Tough est dessinée sous Slash', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros()],
        allies: [
          carte(60, 'tm002', 'Ally', 'Slash'),
          carte(61, 'tough', 'StatusCard', 'Tough', { bind_object_id: 60 }),
        ],
      })
    )
    expect(dessinee(m, 61)?.kind).toBe('status')
    expect(dessinee(m, 61)?.codeCarte).toBe('tough')
    expect(dessinee(m, 61)?.portePar).toBe(60)
  })

  it('Wyrm engagé porte son Tough ; défaussé il perd sa carte', () => {
    const avec = tableAvec(
      siege({
        area_hero: [heros()],
        engaged_enemies: [
          carte(62, 'tm015', 'Minion', 'Wyrm'),
          carte(63, 'tough', 'StatusCard', 'Tough', { bind_object_id: 62 }),
        ],
      })
    )
    expect(dessinee(avec, 63)?.portePar).toBe(62)
    const sans = tableAvec(siege({ area_hero: [heros()], engaged_enemies: [carte(62, 'tm015', 'Minion', 'Wyrm')] }))
    expect(dessinee(sans, 63)).toBeUndefined()
  })
})

describe('tm005 Kaiten : Sonné ou Désorienté + Nunchuck incliné', () => {
  it('le statut est dessiné sur l ennemi et le Nunchuck est couché', () => {
    for (const statut of ['stunned', 'confused']) {
      const m = tableAvec(siege({ area_hero: [heros(), nunchuck1({ is_ready: false })] }), {
        area_villain: [
          carte(70, '01094', 'EncounterVillain', 'Rhino'),
          carte(71, statut, 'StatusCard', statut, { bind_object_id: 70 }),
        ],
      })
      expect(dessinee(m, 71)?.portePar).toBe(70)
      expect(dessinee(m, 71)?.codeCarte).toBe(statut)
      expect(dessinee(m, NUNCHUCK_1)?.exhausted).toBe(true)
    }
  })
})

describe('tm013 All Alone : forme alter-ego forcée, alliés et soutien inclinés', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [alterEgo(), carte(80, 'tm008', 'Support', "Mikey's Couch", { is_ready: false })],
        allies: [carte(81, 'tm002', 'Ally', 'Slash', { is_ready: false })],
        obligations_area: [carte(82, 'tm013', 'Obligation', 'All Alone')],
      })
    )

  it('l obligation est dessinée, l identité apparaît en civil', () => {
    expect(dessinee(monde(), 82)).toBeDefined()
    expect(dessinee(monde(), IDENTITE)?.codeCarte).toBe('tm001b')
  })

  it('l allié et le soutien sont dessinés couchés', () => {
    expect(dessinee(monde(), 80)?.exhausted).toBe(true)
    expect(dessinee(monde(), 81)?.exhausted).toBe(true)
  })

  it('retirée du jeu, elle rejoint les cartes retirées', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo()], obligations_area: [] }), {
      area_removed: [carte(82, 'tm013', 'Obligation', 'All Alone')],
    })
    expect(dessinee(m, 82)?.zone).toBe('annexes')
  })
})

// ---------------------------------------------------------------------------
// tm011 / tm012 : « chaque NUNCHUCK que vous contrôlez gagne : Réponse de héros,
// inclinez cette carte -> +1 à un pouvoir de base ». L'effet octroyé est publié
// comme une option dont `bind_id` est le Nunchuck porteur : chaque Nunchuck
// dessiné et prêt doit être cliquable, un Nunchuck incliné ne l'est pas.
// ---------------------------------------------------------------------------
const CARTE_JOUEE = 90

function optionReponse(bind: number, extra: Record<string, unknown> = {}) {
  return {
    id: 50 + bind,
    name: 'HeroResponse',
    bind_id: bind,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
    ...extra,
  }
}

function demandeDe(...options: Array<Record<string, unknown>>): Demande {
  return lireDemande({
    options_json: JSON.stringify(options),
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

describe('tm011 / tm012 : la Réponse octroyée aux deux Nunchuck est cliquable', () => {
  const monde = (n1: Partial<WorldCard> = {}, n2: Partial<WorldCard> = {}) =>
    tableAvec(
      siege({
        area_hero: [heros(), nunchuck1(n1), nunchuck2(n2)],
        hand_cards: [carte(CARTE_JOUEE, 'ls001a', 'Event', 'Joué')],
      })
    )

  it('les deux Nunchuck sont dessinés (condition pour être cliquables)', () => {
    expect(dessinee(monde(), NUNCHUCK_1)).toBeDefined()
    expect(dessinee(monde(), NUNCHUCK_2)).toBeDefined()
  })

  it('chacun est un porteur cliquable de sa Réponse', () => {
    const d = demandeDe(optionReponse(NUNCHUCK_1), optionReponse(NUNCHUCK_2))
    const { result } = monter(monde(), d)
    for (const id of [NUNCHUCK_1, NUNCHUCK_2]) {
      expect(result.current.cartes.get(id)?.role).toBe('porteur')
      expect(result.current.cartes.get(id)?.agir).toBeTypeOf('function')
    }
  })

  it('cliquer un Nunchuck le focalise, l autre reste disponible', () => {
    const d = demandeDe(optionReponse(NUNCHUCK_1), optionReponse(NUNCHUCK_2))
    const { result } = monter(monde(), d)
    act(() => result.current.cartes.get(NUNCHUCK_1)?.agir?.())
    expect(result.current.cartes.get(NUNCHUCK_1)?.role).toBe('source')
    expect(result.current.cartes.get(NUNCHUCK_1)?.choisie).toBe(true)
    expect(result.current.cartes.get(NUNCHUCK_2)?.choisie).toBeFalsy()
  })

  it('un Nunchuck incliné est dessiné couché et n offre rien (Réponse indisponible)', () => {
    const d = demandeDe(
      optionReponse(NUNCHUCK_1, { failure_reason: 'exhausted' }),
      optionReponse(NUNCHUCK_2)
    )
    const m = monde({ is_ready: false })
    expect(dessinee(m, NUNCHUCK_1)?.exhausted).toBe(true)
    const { result } = monter(m, d)
    expect(result.current.cartes.get(NUNCHUCK_1)?.role).toBe('indisponible')
    expect(result.current.cartes.get(NUNCHUCK_2)?.role).toBe('porteur')
  })

  it('témoin : sans option sur eux (pas d événement joué), aucun Nunchuck n est cliquable', () => {
    const d = demandeDe(optionReponse(CARTE_JOUEE, { name: 'Play' }))
    const { result } = monter(monde(), d)
    expect(result.current.cartes.get(NUNCHUCK_1)).toBeUndefined()
    expect(result.current.cartes.get(NUNCHUCK_2)).toBeUndefined()
  })

  it('le Nunchuck donneur parti, l autre est seul dessiné et seul cliquable', () => {
    const m = tableAvec(siege({ area_hero: [heros(), nunchuck2()] }))
    const d = demandeDe(optionReponse(NUNCHUCK_2))
    expect(dessinee(m, NUNCHUCK_1)).toBeUndefined()
    const { result } = monter(m, d)
    expect(result.current.cartes.get(NUNCHUCK_2)?.agir).toBeTypeOf('function')
  })
})
