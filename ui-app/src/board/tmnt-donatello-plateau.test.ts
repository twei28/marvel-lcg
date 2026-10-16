// Donatello (TMNT, `td`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_donatello.py` prouve ce que le moteur FAIT (101 cas verts) ; ce
// fichier prouve ce que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis).
// On pose à la main l'état d'arrivée que le moteur publie, et on affirme sur
// `dessinee(...)` et sur `useInteraction` (cliquable ou non).
//
// Cartes SANS cas ici, parce qu'elles ne font que chiffrer ou jouer depuis la
// main sans rien dessiner de nouveau : td001a (pioche), td003 / td004
// (prévention et dégâts), td006 (dégâts), td007 (icônes), td008 (rapatrie une
// carte en main), td009 / td010 / td011 (ATQ, inclinaison, redressement : couverts
// par `exhausted`), td015 (statistiques natives).
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
const BO = 11
const CARAPACE = 12
const GLISSEE = 13

const alterEgo = () => carte(IDENTITE, 'td001b', 'AlterEgo', 'Donnie')
const heros = (extra: Record<string, unknown> = {}) =>
  carte(IDENTITE, 'td001a', 'Hero', 'Donatello', extra)
const carapace = (extra: Partial<WorldCard> = {}) =>
  carte(CARAPACE, 'td012', 'Upgrade', "Donatello's Shell", { bind_object_id: IDENTITE, ...extra })
/** Carte glissée sous la Carapace : face cachée, mais visible de son propriétaire. */
const glissee = (cardId = 'td001b', type = 'Event', nom = 'Glissée', extra: Partial<WorldCard> = {}) =>
  carte(GLISSEE, cardId, type, nom, { bind_object_id: CARAPACE, is_face_up: false, ...extra })

describe('td001b Donnie : Bō et Carapace mis en jeu inclinés par la recherche', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          alterEgo(),
          carte(BO, 'td011', 'Upgrade', "Donatello's Bō", { bind_object_id: IDENTITE, is_ready: false }),
          carapace({ is_ready: false }),
        ],
        player_deck: [carte(30, 'ls010', 'Upgrade', 'Autre', { is_face_up: false, visible_for_players: [] })],
        player_discard_pile: [carte(31, 'td009', 'Upgrade', 'Gantelet')],
      })
    )

  it('les deux améliorations sont dessinées en panorama 14|15 A COTE de l identité, couchées', () => {
    // Décision du 16/10/2026 (panorama-jumelles.ts) : Bō (14/15) + Carapace (15/15), paire confirmée.
    for (const [id, cote] of [[BO, 'gauche'], [CARAPACE, 'droite']] as const) {
      const vue = dessinee(monde(), id)
      expect(vue).toBeDefined()
      expect(vue?.panorama).toBe(cote)
      expect(vue?.kind).toBe('upgrade')
      expect(vue?.exhausted).toBe(true)
    }
  })

  it('elles ne traînent plus dans le deck, la carte défaussée en coût est sur la défausse', () => {
    expect(dessinee(monde(), CARAPACE)?.zone).toBe('terrain-soutien')
    expect(dessinee(monde(), 30)?.zone).toBe('piles-joueur')
    expect(dessinee(monde(), 31)?.zone).toBe('piles-joueur')
  })
})

describe('td012 Carapace : la carte glissée dessous est dessinée', () => {
  const monde = () =>
    tableAvec(siege({ area_hero: [heros(), carapace(), glissee()], hand_cards: [carte(40, 'ls001a', 'Event', 'Main')] }))

  it('la carte glissée est à l écran (assertion qui aurait attrapé Contingency Plan)', () => {
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
  })

  it('elle suit immédiatement la Carapace dans l unité de l identité', () => {
    const vues = cartesDessinees(monde())
    expect(dessinee(monde(), GLISSEE)?.portePar).toBe(IDENTITE)
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(GLISSEE)).toBe(rang(CARAPACE) + 1)
  })

  it('elle est marquée posée face cachée, pas réduite à un dos de carte', () => {
    expect(dessinee(monde(), GLISSEE)?.peeking).toBe(true)
    expect(dessinee(monde(), GLISSEE)?.facedown).toBe(false)
  })

  it('la Carapace garde sa place d amélioration face visible, l autre carte reste en main', () => {
    expect(dessinee(monde(), CARAPACE)?.peeking).toBe(false)
    expect(dessinee(monde(), CARAPACE)?.portePar).toBe(IDENTITE)
    expect(dessinee(monde(), 40)?.zone).toBe('main')
  })

  it('Carapace inclinée par l Action : la carte glissée reste dessinée', () => {
    const m = tableAvec(siege({ area_hero: [heros(), carapace({ is_ready: false }), glissee()] }))
    expect(dessinee(m, CARAPACE)?.exhausted).toBe(true)
    expect(dessinee(m, GLISSEE)).toBeDefined()
  })

  it('vue d un autre siège : la carte glissée n est qu un dos', () => {
    const m = tableAvec(
      siege({ area_hero: [heros(), carapace(), glissee('td001b', 'Event', 'Glissée', { visible_for_players: [] })] })
    )
    expect(dessinee(m, GLISSEE)?.facedown).toBe(true)
    expect(dessinee(m, GLISSEE)?.codeCarte).toBeUndefined()
  })

  it('sans carte glissée (après l avoir jouée), il ne reste plus rien sous la Carapace', () => {
    const m = tableAvec(
      siege({ area_hero: [heros(), carapace()], player_discard_pile: [carte(GLISSEE, 'td001b', 'Event', 'Jouée')] })
    )
    expect(dessinee(m, GLISSEE)?.zone).toBe('piles-joueur')
    expect(cartesDessinees(m).filter((c) => c.peeking)).toHaveLength(0)
  })
})

// ---------------------------------------------------------------------------
// td012 : « jouer, dépenser ou défausser comme si en main ». Le moteur publie
// une option dont `bind_id` est la carte glissée ; elle doit être cliquable.
// ---------------------------------------------------------------------------
const EFFET_GLISSEE = 301
const CARTE_JOUEE = 60

function optionBase(extra: Record<string, unknown>) {
  return {
    id: 44,
    name: 'Play',
    bind_id: CARTE_JOUEE,
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

describe('td012 : jouer la carte glissée comme si elle était en main', () => {
  const monde = () => tableAvec(siege({ area_hero: [heros(), carapace(), glissee('td002', 'Ally', 'Metalhead')] }))

  it('la carte glissée est une source cliquable (porteur d une action Play)', () => {
    const d = demandeDe(optionBase({ bind_id: GLISSEE, name: 'Play' }))
    const { result } = monter(monde(), d)
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
    expect(result.current.cartes.get(GLISSEE)?.role).toBe('porteur')
    expect(result.current.cartes.get(GLISSEE)?.agir).toBeTypeOf('function')
  })

  it('cliquer la carte glissée la focalise : elle devient la source', () => {
    const d = demandeDe(optionBase({ bind_id: GLISSEE, name: 'Play' }))
    const { result } = monter(monde(), d)
    act(() => result.current.cartes.get(GLISSEE)?.agir?.())
    expect(result.current.cartes.get(GLISSEE)?.role).toBe('source')
    expect(result.current.cartes.get(GLISSEE)?.choisie).toBe(true)
  })

  it('témoin : sans option sur elle, la carte glissée n est pas cliquable', () => {
    const d = demandeDe(optionBase({ bind_id: 40, name: 'Play' }))
    const m = tableAvec(
      siege({ area_hero: [heros(), carapace(), glissee()], hand_cards: [carte(40, 'ls001a', 'Event', 'Main')] })
    )
    const { result } = monter(m, d)
    expect(result.current.cartes.get(GLISSEE)).toBeUndefined()
  })
})

describe('td012 : dépenser la carte glissée comme une ressource', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros(), carapace(), glissee('td009', 'Upgrade', 'Gantelet', { resources: [EFFET_GLISSEE] })],
        hand_cards: [carte(CARTE_JOUEE, 'td008', 'Support', 'Donnie s Lab')],
      })
    )
  const demande = (cout: string) =>
    demandeDe(
      optionBase({ target_payment: { '0': { cost: cout, payment: [{ [EFFET_GLISSEE]: 'Y' }], rule: [] } } })
    )

  it('elle devient une source de paiement cliquable', () => {
    const d = demande('1')
    const { result } = monter(monde(), d)
    act(() => result.current.choisirOption(d.options[0]!))
    expect(result.current.cartes.get(GLISSEE)?.role).toBe('ressource')
    expect(result.current.cartes.get(GLISSEE)?.agir).toBeTypeOf('function')
  })

  it('la cliquer paie un cran du coût', () => {
    const d = demande('1')
    const { result } = monter(monde(), d)
    act(() => result.current.choisirOption(d.options[0]!))
    act(() => result.current.cartes.get(GLISSEE)?.agir?.())
    expect(result.current.cartes.get(GLISSEE)?.choisie).toBe(true)
    expect(result.current.assistant.coutSlots.filter((s) => s.rempli)).toHaveLength(1)
  })
})

describe('td012 : défausser la carte glissée en coût (td001b, td009)', () => {
  it('elle est une cible cliquable du coût de défausse, au même titre que la main', () => {
    const m = tableAvec(
      siege({
        area_hero: [alterEgo(), carapace(), glissee()],
        hand_cards: [carte(40, 'ls001a', 'Event', 'Main')],
      })
    )
    const d = demandeDe(
      optionBase({
        bind_id: IDENTITE,
        name: 'Action',
        all_legal_targets: [40, GLISSEE],
        target_num_range: [1, 1],
      })
    )
    const { result } = monter(m, d)
    act(() => result.current.choisirOption(d.options[0]!))
    expect(result.current.cartes.get(GLISSEE)?.role).toBe('cible')
    expect(result.current.cartes.get(GLISSEE)?.agir).toBeTypeOf('function')
    expect(result.current.cartes.get(40)?.role).toBe('cible')
  })
})

describe('td002 Metalhead : jouée gratuitement depuis la Carapace ou la main', () => {
  it('l allié mis en jeu est dessiné parmi les alliés, la Carapace est vide', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros(), carapace()],
        allies: [carte(50, 'td002', 'Ally', 'Metalhead')],
      })
    )
    expect(dessinee(m, 50)).toBeDefined()
    expect(dessinee(m, 50)?.kind).toBe('ally')
    expect(cartesDessinees(m).filter((c) => c.portePar === CARAPACE)).toHaveLength(0)
  })
})

describe('td005 Improvised Tactics : le statut Cloaked sur deux personnages alliés', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros(), carte(70, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: IDENTITE })],
        allies: [
          carte(50, 'td002', 'Ally', 'Metalhead'),
          carte(71, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: 50 }),
        ],
      })
    )

  it('l identité porte sa carte Cloaked', () => {
    const c = dessinee(monde(), 70)
    expect(c?.kind).toBe('status')
    expect(c?.codeCarte).toBe('cloaked')
    expect(c?.portePar).toBe(IDENTITE)
  })

  it('l allié porte la sienne', () => {
    expect(dessinee(monde(), 71)?.portePar).toBe(50)
    expect(dessinee(monde(), 71)?.kind).toBe('status')
  })
})

describe('td005 Improvised Tactics : Sonné ou Désorienté sur un ennemi', () => {
  it('la carte de statut est dessinée sur l ennemi', () => {
    for (const statut of ['stunned', 'confused']) {
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

describe('td013 Broken Shell : bascule forcée, Carapace défaussée, retrait du jeu', () => {
  it('l obligation est dessinée et l identité apparaît en civil (la bascule se voit)', () => {
    const m = tableAvec(
      siege({ area_hero: [alterEgo()], obligations_area: [carte(90, 'td013', 'Obligation', 'Broken Shell')] })
    )
    expect(dessinee(m, 90)).toBeDefined()
    expect(dessinee(m, IDENTITE)?.codeCarte).toBe('td001b')
  })

  it('Action : la Carapace en jeu est défaussée, elle quitte l identité', () => {
    const m = tableAvec(
      siege({
        area_hero: [alterEgo()],
        obligations_area: [carte(90, 'td013', 'Obligation', 'Broken Shell')],
        player_discard_pile: [carte(CARAPACE, 'td012', 'Upgrade', "Donatello's Shell")],
      })
    )
    expect(dessinee(m, CARAPACE)?.zone).toBe('piles-joueur')
    expect(dessinee(m, CARAPACE)?.portePar).toBe(0)
  })

  it('retirée du jeu, l obligation rejoint les cartes retirées et l identité redevient héros', () => {
    const m = tableAvec(siege({ area_hero: [heros()], obligations_area: [] }), {
      area_removed: [carte(90, 'td013', 'Obligation', 'Broken Shell')],
    })
    expect(dessinee(m, 90)?.zone).toBe('annexes')
    expect(dessinee(m, IDENTITE)?.codeCarte).toBe('td001a')
  })
})

describe('td014 Extermination! : le sbire cherché arrive engagé', () => {
  it('le sbire mis en jeu est dessiné dans la zone de combat', () => {
    const m = tableAvec(
      siege({ area_hero: [heros()], engaged_enemies: [carte(95, 'td016', 'Minion', 'Plague of M.O.U.S.E.R.s')] })
    )
    expect(dessinee(m, 95)?.zone).toBe('terrain-combat')
  })
})

describe('td016 / td017 essaims : les compteurs swarm sont dessinés', () => {
  const essaim = (id: number, cardId: string, nom: string, swarm: number) =>
    carte(id, cardId, 'Minion', nom, { info: { c_swarm: swarm } })
  const mondeAvec = (...minions: WorldCard[]) =>
    tableAvec(siege({ area_hero: [heros()], engaged_enemies: minions }))

  it('td016 entre avec 2 compteurs, td017 avec 4', () => {
    const m = mondeAvec(essaim(100, 'td016', 'Plague', 2), essaim(101, 'td017', 'Flight', 4))
    expect(dessinee(m, 100)?.compteurs.swarm).toBe(2)
    expect(dessinee(m, 101)?.compteurs.swarm).toBe(4)
  })

  it('après des dégâts remplacés, le compteur diminue à l écran', () => {
    expect(dessinee(mondeAvec(essaim(100, 'td016', 'Plague', 1)), 100)?.compteurs.swarm).toBe(1)
  })

  it('le sbire est dessiné engagé, en genre sbire', () => {
    const vue = dessinee(mondeAvec(essaim(100, 'td016', 'Plague', 2)), 100)
    expect(vue?.zone).toBe('terrain-combat')
    expect(vue?.kind).toBe('minion')
  })

  it('au dernier compteur retiré le sbire est vaincu : plus sur la table, dans la défausse de rencontre', () => {
    const m = tableAvec(siege({ area_hero: [heros()], engaged_enemies: [] }), {
      encounter_discard_pile: [carte(100, 'td016', 'Minion', 'Plague')],
    })
    expect(dessinee(m, 100)?.zone).toBe('piles-rencontre')
  })

  it('deux essaims côte à côte gardent chacun leur compteur', () => {
    const m = mondeAvec(essaim(100, 'td016', 'Plague', 2), essaim(102, 'td016', 'Plague', 1))
    expect(dessinee(m, 100)?.compteurs.swarm).toBe(2)
    expect(dessinee(m, 102)?.compteurs.swarm).toBe(1)
  })
})
