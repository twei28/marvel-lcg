// Casey Jones (TMNT, `tc`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_casey.py` prouve ce que le moteur FAIT ; ce fichier prouve ce
// que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main
// l'état d'arrivée que le moteur publie, et on affirme sur `dessinee(...)` et
// sur `useInteraction` (cliquable ou non).
//
// Ce que le pack fait VOIR (cartes concernées par l'étape 8 bis) :
//  - tc001b Setup : le Sac (tc013) entre en jeu, attaché à l'identité ;
//  - tc013 Casey's Bag : des cartes sont GLISSÉES dessous (comme td012), et on
//    peut les JOUER comme en main (option `Play` portée par la carte glissée) ;
//  - tc006 Anything Goes : échange une arme en jeu et une arme glissée ;
//  - tc001a Overswing : une arme est DÉFAUSSÉE (changement de zone) ;
//  - tc003 Cross Block, tc017 Goons : une carte d'état Tenace sur une carte ;
//  - tc002 Clap Back : une carte d'état Désorienté sur un ennemi ;
//  - tc009 Cricket Willow : défaussé, une carte d'état Sonné sur un ennemi ;
//  - tc014 Daddy Issues : bascule en civil, obligation puis retirée du jeu.
//
// Cartes SANS cas ici, parce qu'elles ne font que chiffrer ou jouer depuis la
// main sans rien dessiner de nouveau : tc004 / tc005 (dégâts), tc007 / tc011 /
// tc012 (valeurs de pouvoir, inclinaison : couverte par `exhausted`), tc008
// (redressement), tc010 (dégâts / menace), tc015 (menace, Incitation, Crise : la
// pastille de crise est déjà couverte par la gate des manigances à Crise),
// tc016 (Sonné : voir plus bas).
//
// Pas de correctif plateau pour ce pack : le moteur de rendu savait déjà
// dessiner une carte glissée sous une amélioration (Carapace td012) et les
// cartes d'état ; ces cas sont verts d'emblée (aucun « rouge avant correctif »
// à montrer, rien n'a été corrigé).
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, type Demande } from './ask'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const IDENTITE = 1
const SAC = 11
const ARME = 12
const GLISSEE = 13
const ARME_EN_JEU = 14
const ANYTHING = 15

const alterEgo = (extra: Partial<WorldCard> = {}) => carte(IDENTITE, 'tc001b', 'AlterEgo', 'Casey Jones', extra)
const heros = (extra: Record<string, unknown> = {}) =>
  carte(IDENTITE, 'tc001a', 'Hero', 'Casey Jones', extra)
const sac = (extra: Partial<WorldCard> = {}) =>
  carte(SAC, 'tc013', 'Upgrade', "Casey's Bag", { bind_object_id: IDENTITE, ...extra })
/** Carte glissée sous le Sac : face cachée, mais visible de son propriétaire. */
const glissee = (cardId = 'tc007', type = 'Upgrade', nom = 'Baseball Bat', extra: Partial<WorldCard> = {}) =>
  carte(GLISSEE, cardId, type, nom, { bind_object_id: SAC, is_face_up: false, ...extra })

describe('tc001b Setup : le Sac entre en jeu, attaché à l identité en alter-ego', () => {
  const monde = () => tableAvec(siege({ area_hero: [alterEgo(), sac()] }))

  it('le Sac est dessiné, en amélioration, porté par l identité', () => {
    const vue = dessinee(monde(), SAC)
    expect(vue).toBeDefined()
    expect(vue?.kind).toBe('upgrade')
    expect(vue?.portePar).toBe(IDENTITE)
  })

  it('l identité est dessinée en civil (face tc001b)', () => {
    expect(dessinee(monde(), IDENTITE)?.codeCarte).toBe('tc001b')
  })

  it('le Sac n est plus dans le deck : il a quitté la pile', () => {
    const m = tableAvec(
      siege({
        area_hero: [alterEgo(), sac()],
        player_deck: [carte(30, 'tc002', 'Event', 'Clap Back', { is_face_up: false, visible_for_players: [] })],
      })
    )
    expect(dessinee(m, SAC)?.zone).not.toBe('piles-joueur')
    expect(dessinee(m, 30)?.zone).toBe('piles-joueur')
  })
})

describe('tc013 Sac : la carte glissée dessous est dessinée', () => {
  const monde = () =>
    tableAvec(siege({ area_hero: [heros(), sac(), glissee()], hand_cards: [carte(40, 'tc002', 'Event', 'Main')] }))

  it('la carte glissée est à l écran (assertion qui aurait attrapé Contingency Plan)', () => {
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
  })

  it('elle suit immédiatement le Sac dans l unité de l identité', () => {
    const vues = cartesDessinees(monde())
    expect(dessinee(monde(), GLISSEE)?.portePar).toBe(IDENTITE)
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(GLISSEE)).toBe(rang(SAC) + 1)
  })

  it('elle est marquée posée face cachée, pas réduite à un dos de carte', () => {
    expect(dessinee(monde(), GLISSEE)?.peeking).toBe(true)
    expect(dessinee(monde(), GLISSEE)?.facedown).toBe(false)
  })

  it('le Sac garde sa place d amélioration face visible, l autre carte reste en main', () => {
    expect(dessinee(monde(), SAC)?.peeking).toBe(false)
    expect(dessinee(monde(), SAC)?.portePar).toBe(IDENTITE)
    expect(dessinee(monde(), 40)?.zone).toBe('main')
  })

  it('plusieurs cartes glissées : toutes sont dessinées (pas de plafond imprimé)', () => {
    const m = tableAvec(
      siege({
        area_hero: [
          heros(),
          sac(),
          glissee('tc007', 'Upgrade', 'Baseball Bat'),
          carte(16, 'tc009', 'Upgrade', 'Cricket Willow', { bind_object_id: SAC, is_face_up: false }),
          carte(17, 'tc011', 'Upgrade', 'Hockey Stick', { bind_object_id: SAC, is_face_up: false }),
        ],
      })
    )
    for (const id of [GLISSEE, 16, 17]) expect(dessinee(m, id)).toBeDefined()
    expect(cartesDessinees(m).filter((c) => c.portePar === IDENTITE && c.peeking)).toHaveLength(3)
  })

  it('Sac incliné par l Action : la carte glissée reste dessinée', () => {
    const m = tableAvec(siege({ area_hero: [heros(), sac({ is_ready: false }), glissee()] }))
    expect(dessinee(m, SAC)?.exhausted).toBe(true)
    expect(dessinee(m, GLISSEE)).toBeDefined()
  })

  it('vue d un autre siège : la carte glissée n est qu un dos', () => {
    const m = tableAvec(
      siege({ area_hero: [heros(), sac(), glissee('tc007', 'Upgrade', 'Baseball Bat', { visible_for_players: [] })] })
    )
    expect(dessinee(m, GLISSEE)?.facedown).toBe(true)
    expect(dessinee(m, GLISSEE)?.codeCarte).toBeUndefined()
  })

  it('sans carte glissée (après l avoir jouée), il ne reste plus rien sous le Sac', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros(), sac(), carte(ARME_EN_JEU, 'tc007', 'Upgrade', 'Baseball Bat', { bind_object_id: IDENTITE })],
      })
    )
    expect(dessinee(m, ARME_EN_JEU)?.portePar).toBe(IDENTITE)
    expect(cartesDessinees(m).filter((c) => c.peeking)).toHaveLength(0)
  })
})

describe('tc013 Action : la plus basse arme de la défausse est glissée sous le Sac', () => {
  it('avant : l arme est sur la défausse ; après : sous le Sac et plus sur la défausse', () => {
    const avant = tableAvec(
      siege({ area_hero: [heros(), sac()], player_discard_pile: [carte(ARME, 'tc007', 'Upgrade', 'Baseball Bat')] })
    )
    expect(dessinee(avant, ARME)?.zone).toBe('piles-joueur')
    const apres = tableAvec(
      siege({
        area_hero: [heros(), sac({ is_ready: false }), carte(ARME, 'tc007', 'Upgrade', 'Baseball Bat', { bind_object_id: SAC, is_face_up: false })],
        player_discard_pile: [],
      })
    )
    expect(dessinee(apres, ARME)).toBeDefined()
    expect(dessinee(apres, ARME)?.zone).not.toBe('piles-joueur')
    expect(dessinee(apres, ARME)?.portePar).toBe(IDENTITE)
    expect(dessinee(apres, ARME)?.peeking).toBe(true)
  })
})

describe('tc006 Anything Goes : l échange des deux armes se voit', () => {
  // État d'arrivée : le Willow (ex-glissé) est en jeu sur l'identité, la batte (ex-en-jeu) est sous le Sac.
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          heros(),
          sac(),
          carte(ANYTHING, 'tc006', 'Upgrade', 'Anything Goes', { bind_object_id: IDENTITE, is_ready: false }),
          carte(ARME_EN_JEU, 'tc009', 'Upgrade', 'Cricket Willow', { bind_object_id: IDENTITE }),
          glissee('tc007', 'Upgrade', 'Baseball Bat'),
        ],
      })
    )

  it('l arme entrante est une amélioration attachée à l identité, face visible', () => {
    const vue = dessinee(monde(), ARME_EN_JEU)
    expect(vue).toBeDefined()
    expect(vue?.portePar).toBe(IDENTITE)
    expect(vue?.peeking).toBe(false)
  })

  it('l arme sortante est dessinée sous le Sac (pas disparue, pas défaussée)', () => {
    const vue = dessinee(monde(), GLISSEE)
    expect(vue).toBeDefined()
    expect(vue?.portePar).toBe(IDENTITE)
    expect(vue?.peeking).toBe(true)
    expect(vue?.zone).not.toBe('piles-joueur')
  })

  it('Anything Goes est dessinée inclinée', () => {
    expect(dessinee(monde(), ANYTHING)?.exhausted).toBe(true)
  })
})

describe('tc001a Overswing : l arme défaussée en coût est sur la défausse', () => {
  it('avant : l arme est attachée à l identité ; après : sur la pile de défausse du joueur', () => {
    const avant = tableAvec(
      siege({ area_hero: [heros(), carte(ARME, 'tc007', 'Upgrade', 'Baseball Bat', { bind_object_id: IDENTITE })] })
    )
    expect(dessinee(avant, ARME)?.portePar).toBe(IDENTITE)
    const apres = tableAvec(
      siege({ area_hero: [heros()], player_discard_pile: [carte(ARME, 'tc007', 'Upgrade', 'Baseball Bat')] })
    )
    expect(dessinee(apres, ARME)?.zone).toBe('piles-joueur')
    expect(dessinee(apres, ARME)?.portePar).toBe(0)
  })
})

describe('tc003 Cross Block, tc017 Goons : la carte d état Tenace est dessinée', () => {
  it('Cross Block : Tenace sur l identité de Casey', () => {
    const m = tableAvec(
      siege({ area_hero: [heros(), carte(70, 'tough', 'StatusCard', 'Tough', { bind_object_id: IDENTITE })] })
    )
    const c = dessinee(m, 70)
    expect(c?.kind).toBe('status')
    expect(c?.codeCarte).toBe('tough')
    expect(c?.portePar).toBe(IDENTITE)
  })

  it('Goons (Une fois révélée) : Tenace sur le VILAIN', () => {
    const m = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(80, '01094', 'EncounterVillain', 'Rhino'),
        carte(81, 'tough', 'StatusCard', 'Tough', { bind_object_id: 80 }),
      ],
    })
    expect(dessinee(m, 81)?.portePar).toBe(80)
    expect(dessinee(m, 81)?.kind).toBe('status')
  })
})

describe('tc002 Clap Back, tc009 Cricket Willow, tc016 Hun : les cartes d état Désorienté / Sonné', () => {
  const surEnnemi = (statut: string) =>
    tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(80, '01094', 'EncounterVillain', 'Rhino'),
        carte(81, statut, 'StatusCard', statut, { bind_object_id: 80 }),
      ],
    })

  it('Clap Back : Désorienté sur l ennemi', () => {
    expect(dessinee(surEnnemi('confused'), 81)?.portePar).toBe(80)
    expect(dessinee(surEnnemi('confused'), 81)?.codeCarte).toBe('confused')
  })

  it('Cricket Willow : Sonné sur l ennemi attaqué', () => {
    expect(dessinee(surEnnemi('stunned'), 81)?.portePar).toBe(80)
    expect(dessinee(surEnnemi('stunned'), 81)?.codeCarte).toBe('stunned')
  })

  it('Hun : Sonné sur le héros blessé, et sur un allié blessé', () => {
    const m = tableAvec(
      siege({
        area_hero: [heros(), carte(82, 'stunned', 'StatusCard', 'Sonné', { bind_object_id: IDENTITE })],
        allies: [
          carte(50, 'tl002', 'Ally', 'Splinter'),
          carte(83, 'stunned', 'StatusCard', 'Sonné', { bind_object_id: 50 }),
        ],
      })
    )
    expect(dessinee(m, 82)?.portePar).toBe(IDENTITE)
    expect(dessinee(m, 83)?.portePar).toBe(50)
  })

  it('Cricket Willow défaussé : sur la défausse, plus sur l identité', () => {
    const m = tableAvec(
      siege({ area_hero: [heros()], player_discard_pile: [carte(ARME, 'tc009', 'Upgrade', 'Cricket Willow')] })
    )
    expect(dessinee(m, ARME)?.zone).toBe('piles-joueur')
  })
})

describe('tc014 Daddy Issues : bascule en civil, obligation puis retrait du jeu', () => {
  it('l obligation est dessinée et l identité apparaît en civil (la bascule se voit)', () => {
    const m = tableAvec(
      siege({ area_hero: [alterEgo()], obligations_area: [carte(90, 'tc014', 'Obligation', 'Daddy Issues')] })
    )
    expect(dessinee(m, 90)).toBeDefined()
    expect(dessinee(m, IDENTITE)?.codeCarte).toBe('tc001b')
  })

  it('retirée du jeu, l obligation rejoint les cartes retirées', () => {
    const m = tableAvec(siege({ area_hero: [alterEgo({ is_ready: false })], obligations_area: [] }), {
      area_removed: [carte(90, 'tc014', 'Obligation', 'Daddy Issues')],
    })
    expect(dessinee(m, 90)?.zone).toBe('annexes')
    expect(dessinee(m, IDENTITE)?.exhausted).toBe(true)
  })
})

// ---------------------------------------------------------------------------
// tc013 : « jouer les cartes glissées comme si elles étaient dans la main ». Le
// moteur publie une option dont `bind_id` est la carte glissée ; elle doit être
// cliquable (même mécanisme que td012).
// ---------------------------------------------------------------------------
function optionBase(extra: Record<string, unknown>) {
  return {
    id: 44,
    name: 'Play',
    bind_id: 60,
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

describe('tc013 : jouer la carte glissée comme si elle était en main', () => {
  const monde = () => tableAvec(siege({ area_hero: [heros(), sac(), glissee('tc004', 'Event', 'Face-Off')] }))

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
      siege({ area_hero: [heros(), sac(), glissee()], hand_cards: [carte(40, 'tc002', 'Event', 'Main')] })
    )
    const { result } = monter(m, d)
    expect(result.current.cartes.get(GLISSEE)).toBeUndefined()
  })
})

describe('tc006 : le choix de l arme entrante parmi les armes rangées', () => {
  it('les armes glissées sous le Sac sont des cibles cliquables du choix d échange', () => {
    const m = tableAvec(
      siege({
        area_hero: [
          heros(),
          sac(),
          carte(ANYTHING, 'tc006', 'Upgrade', 'Anything Goes', { bind_object_id: IDENTITE }),
          glissee('tc009', 'Upgrade', 'Cricket Willow'),
          carte(16, 'tc011', 'Upgrade', 'Hockey Stick', { bind_object_id: SAC, is_face_up: false }),
        ],
      })
    )
    const d = demandeDe(
      optionBase({
        bind_id: ANYTHING,
        name: 'Swap with a WEAPON upgrade tucked under Casey\'s Bag',
        all_legal_targets: [GLISSEE, 16],
        target_num_range: [1, 1],
      })
    )
    const { result } = monter(m, d)
    act(() => result.current.choisirOption(d.options[0]!))
    expect(result.current.cartes.get(GLISSEE)?.role).toBe('cible')
    expect(result.current.cartes.get(16)?.role).toBe('cible')
    expect(result.current.cartes.get(GLISSEE)?.agir).toBeTypeOf('function')
  })
})
