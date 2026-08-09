// Le scenario qui a casse : Venom joue Sonic Rifle (cout 3). Le moteur propose
// TROIS moyens de paiement — les deux cartes doubles de la main, et l'effet
// « Symbiotic Bond » porte par la carte d'IDENTITE (prendre 1 degat pour
// generer un [wild]). Sur la table, seules les deux cartes de la main etaient
// cliquables : impossible d'activer Symbiotic Bond, donc impossible de payer 3.
//
// Le moteur, lui, est innocent. Verifie sur une vraie partie (tools/
// test_capacites.py, cas « 20001a Symbiotic Bond ») : la carte se paie, Venom
// prend bien 1 degat, et le descripteur envoye au plateau contient
//   identite : resources = [1]
//   option Play : target_payment = {"0": {"cost": "3",
//                   "payment": [{"1": "G"}, {"45": "YY"}, {"46": "BB"}]}}
//
// Ces tests verrouillent les deux maillons cote plateau : le parsing du format
// « objet a une seule cle » et le droit de cliquer l'identite pour payer.

import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, paiementCourant, foisDisponible, type Demande, type Option } from './ask'
import type { Catalogue } from './catalogue'
import { useInteraction } from './interaction'
import type { World } from './world'

/** Identifiants repris de la partie reelle capturee. */
const IDENTITE = 12
const SONIC_RIFLE = 34
const MAIN_ENERGIE = 45
const MAIN_MENTAL = 46
const EFFET_SYMBIOTIC_BOND = 1

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

const MONDE = {
  render_id: 1,
  players: [
    {
      // L'identite PORTE l'effet de ressource : c'est tout l'enjeu.
      area_hero: [carte(IDENTITE, { card_type: 'hero', resources: [EFFET_SYMBIOTIC_BOND] })],
      hand: [
        carte(SONIC_RIFLE, { card_type: 'upgrade' }),
        carte(MAIN_ENERGIE, { card_type: 'event', resources: [MAIN_ENERGIE] }),
        carte(MAIN_MENTAL, { card_type: 'event', resources: [MAIN_MENTAL] }),
      ],
    },
  ],
} as unknown as World

/** L'option « Play » telle que le moteur l'envoie vraiment (format brut). */
function optionBrute(): Record<string, unknown> {
  return {
    id: 44,
    name: 'Play',
    bind_id: SONIC_RIFLE,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {
      '0': {
        cost: '3',
        // Format « objet a une seule cle », celui du moteur.
        payment: [
          { [EFFET_SYMBIOTIC_BOND]: 'G' },
          { [MAIN_ENERGIE]: 'YY' },
          { [MAIN_MENTAL]: 'BB' },
        ],
        rule: [],
      },
    },
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

function demandeBrute(): Record<string, unknown> {
  return {
    // Le moteur envoie les options SERIALISEES, comme le fait le vrai socket.
    options_json: JSON.stringify([optionBrute()]),
    prompt_text: '',
    event_name: 'test',
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
  // La table dessine l'identite (emplacement « Héros et soutiens ») et la main.
  const affiches = new Set([IDENTITE, SONIC_RIFLE, MAIN_ENERGIE, MAIN_MENTAL])
  return renderHook(() =>
    useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple')
  )
}

describe('paiement par une capacite de l identite (Symbiotic Bond)', () => {
  it('lit les trois moyens de paiement, dont celui porte par l identite', () => {
    const demande = lireDemande(demandeBrute())
    expect(demande).toBeDefined()
    const option = demande!.options[0]!
    const paiement = paiementCourant(option, [])

    expect(paiement?.cost).toBe('3')
    expect(paiement?.payment).toHaveLength(3)
    expect(foisDisponible(paiement, EFFET_SYMBIOTIC_BOND)).toBe(1)
    expect(foisDisponible(paiement, MAIN_ENERGIE)).toBe(1)
  })

  it('rend l identite cliquable pour payer, comme les cartes de la main', () => {
    const demande = lireDemande(demandeBrute())!
    const { result } = monter(demande)

    act(() => result.current.choisirOption(demande.options[0]!))

    // Les cartes de la main sont cliquables — ça, ça marchait déjà.
    expect(result.current.cartes.get(MAIN_ENERGIE)?.agir).toBeTypeOf('function')
    expect(result.current.cartes.get(MAIN_MENTAL)?.agir).toBeTypeOf('function')

    // C'est ICI que tout se jouait : l'identité n'était pas cliquable, donc
    // Symbiotic Bond restait inactivable et le coût de 3 impayable.
    expect(result.current.cartes.get(IDENTITE)?.role).toBe('ressource')
    expect(result.current.cartes.get(IDENTITE)?.agir).toBeTypeOf('function')
  })

  it('depense bien la ressource de l identite quand on la clique', () => {
    const demande = lireDemande(demandeBrute())!
    const { result } = monter(demande)

    act(() => result.current.choisirOption(demande.options[0]!))
    act(() => result.current.cartes.get(IDENTITE)?.agir?.())

    expect(result.current.cartes.get(IDENTITE)?.choisie).toBe(true)
  })
})

// La main REELLE du joueur : une seule carte double (2 mentales). Il manque
// donc exactement 1 ressource, que seul Symbiotic Bond peut fournir. C'est la
// configuration ou le blocage a ete signale.
function optionBruteMainCourte(): Record<string, unknown> {
  const o = optionBrute()
  ;(o.target_payment as Record<string, { payment: unknown[] }>)['0']!.payment = [
    { [EFFET_SYMBIOTIC_BOND]: 'G' },
    { [MAIN_MENTAL]: 'BB' },
  ]
  return o
}

function demandeMainCourte(): Record<string, unknown> {
  return {
    options_json: JSON.stringify([optionBruteMainCourte()]),
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
}

describe('paiement quand la double ne suffit pas (2 sur 3)', () => {
  it('laisse cliquer l identite APRES avoir pose la carte double', () => {
    const demande = lireDemande(demandeMainCourte())!
    const { result } = monter(demande)

    act(() => result.current.choisirOption(demande.options[0]!))

    // On paie d'abord avec la double : 2 sur 3.
    act(() => result.current.cartes.get(MAIN_MENTAL)?.agir?.())
    expect(result.current.cartes.get(MAIN_MENTAL)?.choisie).toBe(true)

    // Il manque 1 : l'identite doit rester cliquable pour completer.
    expect(result.current.cartes.get(IDENTITE)?.agir).toBeTypeOf('function')

    act(() => result.current.cartes.get(IDENTITE)?.agir?.())
    expect(result.current.cartes.get(IDENTITE)?.choisie).toBe(true)
  })

  it('compte 3 payes une fois la double et l identite posees', () => {
    const demande = lireDemande(demandeMainCourte())!
    const { result } = monter(demande)

    act(() => result.current.choisirOption(demande.options[0]!))
    act(() => result.current.cartes.get(MAIN_MENTAL)?.agir?.())
    act(() => result.current.cartes.get(IDENTITE)?.agir?.())

    // 2 (BB) + 1 (G) = 3, et non « 2 cartes » : une double vaut deux
    // ressources. L'assistant doit donc annoncer le cout comme couvert.
    expect(result.current.assistant.etape).toBe('confirm')
  })
})

// LE cas signale : Sonic Rifle est une AMELIORATION. Venom est donc a la fois
// la cible qui la recoit ET le payeur (Symbiotic Bond). Le plateau donnait la
// priorite au role de cible et sautait la carte pour le paiement — Venom
// restait donc inutilisable comme ressource.
function optionBruteAmelioration(): Record<string, unknown> {
  return {
    id: 44,
    name: 'Play',
    bind_id: SONIC_RIFLE,
    bind_player_id: 0,
    // L'amelioration s'attache a l'identite : une cible, obligatoire.
    all_legal_targets: [IDENTITE],
    target_num_range: [1, 1],
    target_payment: {
      // Le cout est indexe par la CIBLE des que l'option en a une.
      [IDENTITE]: {
        cost: '3',
        payment: [{ [EFFET_SYMBIOTIC_BOND]: 'G' }, { [MAIN_MENTAL]: 'BB' }],
        rule: [],
      },
    },
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

function demandeAmelioration(): Record<string, unknown> {
  return {
    options_json: JSON.stringify([optionBruteAmelioration()]),
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
}

describe('la cible de l amelioration est aussi le payeur', () => {
  it('laisse Venom payer alors qu il est deja la cible du Sonic Rifle', () => {
    const demande = lireDemande(demandeAmelioration())!
    const { result } = monter(demande)

    // Une seule cible legale : le plateau designe Venom tout seul.
    act(() => result.current.choisirOption(demande.options[0]!))
    expect(result.current.assistant.cibleNombre).toBe(1)
    expect(result.current.cartes.get(IDENTITE)?.role).toBe('cible')

    // On paie d'abord avec la double de la main : 2 sur 3.
    act(() => result.current.cartes.get(MAIN_MENTAL)?.agir?.())
    expect(result.current.assistant.detail).toContain('2/3')

    // Il manque 1, que seul Symbiotic Bond peut donner. C'est ICI que tout se
    // jouait : Venom etant deja la cible, son clic ne faisait que le
    // DE-cibler, et sa ressource restait hors d'atteinte.
    expect(result.current.cartes.get(IDENTITE)?.agir).toBeTypeOf('function')
    act(() => result.current.cartes.get(IDENTITE)?.agir?.())

    // Le Sonic Rifle part toujours sur Venom, et le cout est couvert.
    expect(result.current.assistant.cibleNombre).toBe(1)
    expect(result.current.assistant.etape).toBe('confirm')
  })
})

// Le meme conflit ne touche pas que l'identite : tout ALLIE ou SOUTIEN qui
// genere des ressources peut recevoir une amelioration (Brawn, Quincarrier,
// Pepper Potts...). Et la carte qui PORTE l'action (role « source ») pourrait
// elle aussi vouloir payer. On verrouille les deux.
const ALLIE = 77
const EFFET_ALLIE = 5

const MONDE_ALLIE = {
  render_id: 1,
  players: [
    {
      area_hero: [carte(IDENTITE, { card_type: 'hero' })],
      allies: [carte(ALLIE, { card_type: 'ally', resources: [EFFET_ALLIE] })],
      hand: [
        carte(SONIC_RIFLE, { card_type: 'upgrade' }),
        carte(MAIN_MENTAL, { card_type: 'event', resources: [MAIN_MENTAL] }),
      ],
    },
  ],
} as unknown as World

function demandeSurAllie(): Record<string, unknown> {
  return {
    options_json: JSON.stringify([
      {
        id: 44,
        name: 'Play',
        bind_id: SONIC_RIFLE,
        bind_player_id: 0,
        all_legal_targets: [ALLIE],
        target_num_range: [1, 1],
        target_payment: {
          [ALLIE]: {
            cost: '3',
            payment: [{ [EFFET_ALLIE]: 'G' }, { [MAIN_MENTAL]: 'BB' }],
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
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
}

describe('le meme conflit sur un allie generateur de ressources', () => {
  it('laisse l allie payer l amelioration qu il recoit', () => {
    const demande = lireDemande(demandeSurAllie())!
    const affiches = new Set([IDENTITE, ALLIE, SONIC_RIFLE, MAIN_MENTAL])
    const { result } = renderHook(() =>
      useInteraction(MONDE_ALLIE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple')
    )

    act(() => result.current.choisirOption(demande.options[0]!))
    expect(result.current.assistant.cibleNombre).toBe(1)

    act(() => result.current.cartes.get(MAIN_MENTAL)?.agir?.())
    expect(result.current.assistant.detail).toContain('2/3')

    // L'allie est la cible ET le seul moyen de completer le cout.
    act(() => result.current.cartes.get(ALLIE)?.agir?.())
    expect(result.current.assistant.cibleNombre).toBe(1)
    expect(result.current.assistant.etape).toBe('confirm')
  })
})

// Dernier role qui pourrait confisquer le clic : « source », pose sur la carte
// qui PORTE l'action (option.bind_id). Une amelioration en jeu qui genere des
// ressources et porte une action payante tomberait dessus.
const OUTIL = 88
const EFFET_OUTIL = 9

const MONDE_OUTIL = {
  render_id: 1,
  players: [
    {
      area_hero: [carte(IDENTITE, { card_type: 'hero' })],
      supports: [carte(OUTIL, { card_type: 'upgrade', resources: [EFFET_OUTIL] })],
      hand: [],
    },
  ],
} as unknown as World

function demandeActionPortee(): Record<string, unknown> {
  return {
    options_json: JSON.stringify([
      {
        id: 50,
        name: 'Action',
        // La carte qui porte l'action est AUSSI le seul moyen de la payer.
        bind_id: OUTIL,
        bind_player_id: 0,
        all_legal_targets: [],
        target_num_range: [0, 0],
        target_payment: {
          '0': { cost: '1', payment: [{ [EFFET_OUTIL]: 'G' }], rule: [] },
        },
        select_rule: '',
        target_must_include_traits: [],
        failure_reason: '',
        is_search: false,
      },
    ]),
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
}

describe('la carte qui porte l action peut aussi la payer', () => {
  it('laisse payer avec la carte source elle-meme', () => {
    const demande = lireDemande(demandeActionPortee())!
    const affiches = new Set([IDENTITE, OUTIL])
    const { result } = renderHook(() =>
      useInteraction(MONDE_OUTIL, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple')
    )

    act(() => result.current.choisirOption(demande.options[0]!))
    expect(result.current.assistant.etape).toBe('payment')

    // Le moteur propose la carte comme moyen de paiement : le plateau doit
    // permettre de cliquer dessus, malgre son role de « source ».
    expect(result.current.cartes.get(OUTIL)?.agir).toBeTypeOf('function')
    act(() => result.current.cartes.get(OUTIL)?.agir?.())
    expect(result.current.assistant.etape).toBe('confirm')
  })
})
