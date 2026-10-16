// Raphael (TMNT, `tr`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_raphael.py` prouve ce que le moteur FAIT (97 cas verts) ; ce
// fichier prouve ce que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis).
// On pose à la main l'état d'arrivée que le moteur publie (le compteur de rage
// est `info.c_rage` de l'IDENTITE, quelle que soit sa face : `Friend -> Unit2
// -> CanPlaceCounter`), et on affirme sur `dessinee(...)`.
//
// Cartes SANS cas ici, parce qu'elles ne font que chiffrer (dégâts, menace,
// ATQ) ou défausser/piocher sans rien dessiner de nouveau : tr005 Savage
// Assault, tr006 Unbridled Fury (+2 ATQ), tr008 Shell Cycle (soutien incliné,
// couvert par tr009), tr011/tr012 Sai (inclinaison + dégât, couvertes par
// tr001b), tr015 Old Hob (natif), tr016/tr017 (défausses de main ou d'allié).
//
// Pas de panorama des paires jumelles 14/15 (travail ultérieur).
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, type Demande } from './ask'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const IDENTITE = 1

const heros = (rage = 0, extra: Record<string, unknown> = {}) =>
  carte(IDENTITE, 'tr001a', 'Hero', 'Raphael', { info: rage > 0 ? { c_rage: rage } : {}, ...extra })
const civil = (rage = 0, extra: Record<string, unknown> = {}) =>
  carte(IDENTITE, 'tr001b', 'AlterEgo', 'Raph', { info: rage > 0 ? { c_rage: rage } : {}, ...extra })

describe('la rage est dessinée sur l identité', () => {
  // tr001a Yaban Hito, tr010 Gekido, tr011 Sai (rage posée à la main).
  it('forme héros : 2 compteurs de rage visibles sur Raphael', () => {
    const monde = tableAvec(siege({ area_hero: [heros(2)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.rage).toBe(2)
  })

  it('forme héros : le plafond de 3 (Yaban Hito) est dessiné tel quel', () => {
    const monde = tableAvec(siege({ area_hero: [heros(3)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.rage).toBe(3)
  })

  // tr002 Casey Jones et tr007 Seething Rage visent l'identité même en civil.
  it('forme alter-ego (civil) : la rage posée par Casey / Seething Rage est visible sur Raph', () => {
    const monde = tableAvec(siege({ area_hero: [civil(1)] }))
    const raph = dessinee(monde, IDENTITE)
    expect(raph?.codeCarte).toBe('tr001b')
    expect(raph?.compteurs.rage).toBe(1)
  })

  // Casey Jones et Gekido ne plafonnent pas : 3 -> 4 doit se voir.
  it('sans plafond : 4 compteurs de rage sont dessinés', () => {
    const monde = tableAvec(siege({ area_hero: [civil(4)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.rage).toBe(4)
  })

  // tr009 Raph's Punching Bag retire TOUTE la rage : plus de compteur dessiné.
  it('rage retirée : plus aucun compteur sur l identité', () => {
    const monde = tableAvec(siege({ area_hero: [civil(0)] }))
    expect(dessinee(monde, IDENTITE)?.compteurs.rage).toBeUndefined()
  })

  // Contre-cas : la rage reste sur l'identité, pas sur un attachement voisin.
  it('la rage n apparaît que sur l identité, pas sur Gekido attaché', () => {
    const monde = tableAvec(
      siege({
        area_hero: [
          heros(1),
          carte(10, 'tr010', 'Upgrade', 'Gekido', { bind_object_id: IDENTITE, is_ready: false }),
        ],
      })
    )
    expect(dessinee(monde, 10)?.compteurs.rage).toBeUndefined()
    expect(dessinee(monde, 10)?.exhausted).toBe(true)
    expect(dessinee(monde, IDENTITE)?.compteurs.rage).toBe(1)
  })
})

describe('tr001b Raph : deux Sai mises en jeu inclinées', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          civil(),
          carte(11, 'tr011', 'Upgrade', "Raphael's Sai", { bind_object_id: IDENTITE, is_ready: false }),
          carte(12, 'tr012', 'Upgrade', "Raphael's Other Sai", { bind_object_id: IDENTITE, is_ready: false }),
        ],
        player_discard_pile: [carte(13, '01089', 'Event', 'Genius')],
      })
    )

  it('les deux Sai sont dessinées sur l identité, couchées', () => {
    for (const id of [11, 12]) {
      const vue = dessinee(monde(), id)
      expect(vue).toBeDefined()
      expect(vue?.portePar).toBe(IDENTITE)
      expect(vue?.kind).toBe('upgrade')
      expect(vue?.exhausted).toBe(true)
    }
  })

  it('la carte défaussée en coût est sur la pile de défausse', () => {
    expect(dessinee(monde(), 13)?.zone).toBe('piles-joueur')
  })
})

describe('tr009 Raph s Punching Bag : soutien incliné, rage retirée, cartes piochées', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          civil(0),
          carte(20, 'tr009', 'Support', "Raph's Punching Bag", { is_ready: false }),
        ],
        hand_cards: [carte(21, '01090', 'Event', 'Strength'), carte(22, '01090', 'Event', 'Strength')],
      })
    )

  it('le soutien est dessiné incliné', () => {
    expect(dessinee(monde(), 20)?.exhausted).toBe(true)
  })

  it('les cartes piochées arrivent dans la main', () => {
    expect(cartesDessinees(monde()).filter((c) => c.zone === 'main')).toHaveLength(2)
  })
})

describe('tr013 Out of Control : forme héros forcée, identité inclinée, puis libération', () => {
  it('l obligation est dessinée et l identité apparaît en forme héros, inclinée', () => {
    const monde = tableAvec(
      siege({
        area_hero: [heros(0, { is_ready: false })],
        obligations_area: [carte(30, 'tr013', 'Obligation', 'Out of Control')],
      })
    )
    expect(dessinee(monde, 30)).toBeDefined()
    expect(dessinee(monde, IDENTITE)?.codeCarte).toBe('tr001a')
    expect(dessinee(monde, IDENTITE)?.exhausted).toBe(true)
  })

  it('après l Action : retour en civil, 2 rage retirées, l obligation a quitté la table', () => {
    const monde = tableAvec(
      siege({ area_hero: [civil(1)], obligations_area: [] }),
      { encounter_discard_pile: [carte(30, 'tr013', 'Obligation', 'Out of Control')] }
    )
    expect(dessinee(monde, IDENTITE)?.codeCarte).toBe('tr001b')
    expect(dessinee(monde, IDENTITE)?.compteurs.rage).toBe(1)
    expect(dessinee(monde, 30)?.zone).toBe('piles-rencontre')
  })
})

describe('tr014 Mutagen Bomb : le compteur de temps', () => {
  it('1 compteur timer est dessiné sur la manigance annexe', () => {
    const monde = tableAvec(siege({ area_hero: [civil()] }), {
      area_schemes_side: [
        carte(40, 'tr014', 'EncounterSideScheme', 'Mutagen Bomb', { info: { c_timer: 1, k_threat: 2 } }),
      ],
    })
    expect(dessinee(monde, 40)?.compteurs.timer).toBe(1)
  })

  it('au second compteur elle est défaussée : la table ne la montre plus, la carte donnée est face cachée', () => {
    const monde = tableAvec(
      siege({
        area_hero: [civil()],
        dealt_encounter_cards: [
          carte(41, 'tr016', 'Treachery', 'Insurrection', { is_face_up: false, visible_for_players: [] }),
        ],
      }),
      { area_schemes_side: [] }
    )
    expect(dessinee(monde, 40)).toBeUndefined()
    expect(dessinee(monde, 41)?.facedown).toBe(true)
  })
})

describe('tr003 Disarm : l attachement de rencontre part de l ennemi ; tr004 Headbutt : statut', () => {
  const ENNEMI = 50
  const mondeAvec = (cartes: ReturnType<typeof carte>[], defausse: ReturnType<typeof carte>[] = []) =>
    tableAvec(siege({ area_hero: [heros()], player_discard_pile: defausse }), {
      area_villain: [carte(ENNEMI, '01094', 'EncounterVillain', 'Rhino'), ...cartes],
    })

  it('avant : l attachement pend à l ennemi', () => {
    const monde = mondeAvec([carte(51, 'xx001', 'Attachment', 'Gekido', { bind_object_id: ENNEMI })])
    expect(dessinee(monde, 51)?.portePar).toBe(ENNEMI)
  })

  it('après : il a quitté l ennemi, et la Sai défaussée est sur la défausse', () => {
    const monde = mondeAvec([], [carte(52, 'tr011', 'Upgrade', "Raphael's Sai")])
    expect(dessinee(monde, 51)).toBeUndefined()
    expect(dessinee(monde, 52)?.zone).toBe('piles-joueur')
  })

  it('Headbutt pose Sonné ou Désorienté : la carte de statut est dessinée sur l ennemi', () => {
    for (const statut of ['stunned', 'confused']) {
      const monde = mondeAvec([carte(53, statut, 'StatusCard', statut, { bind_object_id: ENNEMI })])
      const vue = dessinee(monde, 53)
      expect(vue?.kind).toBe('status')
      expect(vue?.codeCarte).toBe(statut)
      expect(vue?.portePar).toBe(ENNEMI)
    }
  })
})

// ---------------------------------------------------------------------------
// tr001a : « chaque compteur de rage peut être dépensé comme une ressource
// [physical] ». Le moteur publie l'effet de dépense dans `resources` de
// l'identité (comme Symbiotic Bond, paiement-identite.test.ts) : l'identité
// doit rester cliquable pour payer, même quand elle n'est plus qu un jeton.
// ---------------------------------------------------------------------------
const EFFET_RAGE = 201
const CARTE_JOUEE = 60

function monde(rage: number): World {
  return tableAvec(
    siege({
      area_hero: [heros(rage, { resources: [EFFET_RAGE] })],
      hand_cards: [carte(CARTE_JOUEE, 'tr008', 'Support', 'Shell Cycle')],
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
    target_payment: { '0': { cost: cout, payment: [{ [EFFET_RAGE]: 'R' }, { [EFFET_RAGE]: 'R' }], rule: [] } },
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

describe('tr001a : la rage se dépense depuis l identité dessinée', () => {
  it('le compteur de rage dépensable est bien dessiné sur l identité cliquée', () => {
    expect(dessinee(monde(2), IDENTITE)?.compteurs.rage).toBe(2)
  })

  it('l identité devient une source de paiement cliquable', () => {
    const d = demande('1')
    const { result } = monter(monde(2), d)
    act(() => result.current.choisirOption(d.options[0]!))
    expect(result.current.cartes.get(IDENTITE)?.role).toBe('ressource')
    expect(result.current.cartes.get(IDENTITE)?.agir).toBeTypeOf('function')
  })

  it('cliquer l identité dépense une rage et remplit un cran du coût', () => {
    const d = demande('2')
    const { result } = monter(monde(2), d)
    act(() => result.current.choisirOption(d.options[0]!))
    act(() => result.current.cartes.get(IDENTITE)?.agir?.())
    expect(result.current.cartes.get(IDENTITE)?.choisie).toBe(true)
    expect(result.current.assistant.coutSlots.filter((s) => s.rempli).length).toBeGreaterThan(0)
  })
})
