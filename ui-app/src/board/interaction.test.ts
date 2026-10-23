// Le scenario qui a casse : « Choisis les cibles 0/3 », et apres la premiere
// designation le plateau bascule sur « Paie 0/1 » — les cibles 2 et 3 ne sont
// plus cliquables du tout, alors que la carte en annonce trois.
//
// La cause etait un couplage : l'etape courante pilotait A LA FOIS le texte
// affiche et le droit de cliquer. Des qu'un cout restait du, l'etape passait a
// « payment » et les cibles perdaient leur `agir`. Ces tests verrouillent la
// separation des deux.

import { act, renderHook, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { Demande, Option } from './ask'
import type { Catalogue } from './catalogue'
import { CLE_PAIEMENT_AUTO, CLE_VALIDATION_COURTE, useInteraction } from './interaction'
import { NOM_OPTION_MANIGANCE } from './manigance-face-a'
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

// Signalement Yarro n28 (27/09/2026) : les cartes « a remettre dans l'ordre
// voulu » (Madame Web et consorts, `PlaceOnTopInAnyOrder` cote moteur) ne
// montraient aucun ordre a l'ecran -- le joueur cliquait a l'aveugle. La
// carte porte maintenant un numero (`.ordre`) qui suit l'ordre du clic,
// UNIQUEMENT pour ce genre de selection (voir `optionEstOrdonnee`).
describe('useInteraction, une selection ou l ordre de clic compte', () => {
  function optionOrdonnee(): Option {
    const option = optionTroisCibles()
    option.name = 'Place_on_top'
    option.target_num_range = [3, 3]
    return option
  }

  it('numerote chaque cible dans l ordre ou elle a ete cliquee', () => {
    const { result } = monter(optionOrdonnee())

    act(() => result.current.choisirOption(optionOrdonnee()))
    // Ordre de clic volontairement different de l'ordre des ids.
    act(() => result.current.cartes.get(CIBLES[1])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[2])?.agir?.())

    expect(result.current.cartes.get(CIBLES[1])?.ordre).toBe(1)
    expect(result.current.cartes.get(CIBLES[0])?.ordre).toBe(2)
    expect(result.current.cartes.get(CIBLES[2])?.ordre).toBe(3)
  })

  it('ne numerote rien pour une selection ordinaire (l ordre du clic n y veut rien dire)', () => {
    const { result } = monter(optionTroisCibles())

    act(() => result.current.choisirOption(optionTroisCibles()))
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[1])?.agir?.())

    expect(result.current.cartes.get(CIBLES[0])?.ordre).toBeUndefined()
    expect(result.current.cartes.get(CIBLES[1])?.ordre).toBeUndefined()
  })

  // Demande de l'utilisateur, 28/09/2026 : sur le modele des boutons
  // « ←/→ » de Felt Table (Flesh and Blood), PAS de glisser-depose --
  // chaque carte deja choisie porte deux boutons qui echangent sa position
  // avec sa voisine immediate.
  it('permute deux cartes avec ordreAvancer/ordreReculer et met les numeros a jour', () => {
    const { result } = monter(optionOrdonnee())

    act(() => result.current.choisirOption(optionOrdonnee()))
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[1])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[2])?.agir?.())
    // Avant permutation : CIBLES[0]=1, CIBLES[1]=2, CIBLES[2]=3.

    act(() => result.current.cartes.get(CIBLES[0])?.ordreAvancer?.())

    expect(result.current.cartes.get(CIBLES[1])?.ordre).toBe(1)
    expect(result.current.cartes.get(CIBLES[0])?.ordre).toBe(2)
    expect(result.current.cartes.get(CIBLES[2])?.ordre).toBe(3)
  })

  it('n offre pas de bouton pour sortir des deux bouts de la rangee', () => {
    const { result } = monter(optionOrdonnee())

    act(() => result.current.choisirOption(optionOrdonnee()))
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[1])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[2])?.agir?.())

    // Premiere carte cliquee (CIBLES[0], rang 1) : rien devant elle.
    expect(result.current.cartes.get(CIBLES[0])?.ordreReculer).toBeUndefined()
    expect(result.current.cartes.get(CIBLES[0])?.ordreAvancer).toBeTypeOf('function')
    // Carte du milieu (CIBLES[1], rang 2) : les deux boutons.
    expect(result.current.cartes.get(CIBLES[1])?.ordreReculer).toBeTypeOf('function')
    expect(result.current.cartes.get(CIBLES[1])?.ordreAvancer).toBeTypeOf('function')
    // Derniere carte cliquee (CIBLES[2], rang 3) : rien apres elle.
    expect(result.current.cartes.get(CIBLES[2])?.ordreAvancer).toBeUndefined()
    expect(result.current.cartes.get(CIBLES[2])?.ordreReculer).toBeTypeOf('function')
  })

  it('n offre aucun bouton de reordonnancement pour une selection ordinaire', () => {
    const { result } = monter(optionTroisCibles())

    act(() => result.current.choisirOption(optionTroisCibles()))
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())
    act(() => result.current.cartes.get(CIBLES[1])?.agir?.())

    expect(result.current.cartes.get(CIBLES[0])?.ordreReculer).toBeUndefined()
    expect(result.current.cartes.get(CIBLES[0])?.ordreAvancer).toBeUndefined()
    expect(result.current.cartes.get(CIBLES[1])?.ordreReculer).toBeUndefined()
    expect(result.current.cartes.get(CIBLES[1])?.ordreAvancer).toBeUndefined()
  })
})

// Nice-to-have relaye par Yarro (28/09/2026) : repartir des degats (ou un
// soin) sur plusieurs sbires/allies se faisait un clic par point de degat,
// jusqu'a epuisement du total. `assignerReste` ajoute d'un coup tout ce
// qu'une carte peut encore recevoir, plafonne par SON propre maximum
// (`all_legal_targets` compte ses occurrences, cf. `AssignDamage` cote
// moteur qui plafonne par PV/`Sustained` restants) ET par ce qu'il reste a
// distribuer au total (`target_num_range[1]`).
describe('useInteraction, assignation en masse sur une selection repetable', () => {
  /** `capacites[i]` = combien de fois CIBLES[i] apparait dans `all_legal_targets`
   *  (son plafond propre, cote moteur : PV restants, Sustained...). */
  function optionRepartition(total: number, capacites: number[]): Option {
    const cibles: number[] = []
    CIBLES.forEach((id, i) => {
      for (let n = 0; n < (capacites[i] ?? 0); n++) cibles.push(id)
    })
    const option = optionTroisCibles()
    option.name = `Assign ${total} damage`
    option.all_legal_targets = cibles
    option.target_num_range = [0, total]
    return option
  }

  it('ajoute d’un coup tout ce que la carte peut recevoir, plafonne par son propre maximum', () => {
    const option = optionRepartition(10, [3, 5])
    const { result } = monter(option)
    act(() => result.current.choisirOption(optionRepartition(10, [3, 5])))

    expect(result.current.cartes.get(CIBLES[0])?.assignerResteQuantite).toBe(3)
    act(() => result.current.cartes.get(CIBLES[0])?.assignerReste?.())

    expect(result.current.cartes.get(CIBLES[0])?.fois).toBe(3)
    // La carte est a son maximum propre : plus rien a assigner d'un coup ici.
    expect(result.current.cartes.get(CIBLES[0])?.assignerReste).toBeUndefined()
  })

  it('plafonne par le total encore a distribuer, meme si la carte pourrait recevoir plus', () => {
    const option = optionRepartition(3, [5, 5])
    const { result } = monter(option)
    act(() => result.current.choisirOption(optionRepartition(3, [5, 5])))

    expect(result.current.cartes.get(CIBLES[0])?.assignerResteQuantite).toBe(3)
    act(() => result.current.cartes.get(CIBLES[0])?.assignerReste?.())

    expect(result.current.cartes.get(CIBLES[0])?.fois).toBe(3)
    // Le total (3) est atteint : plus aucune carte ne peut plus rien recevoir.
    expect(result.current.cartes.get(CIBLES[1])?.assignerReste).toBeUndefined()
  })

  it('ne propose rien pour une cible non repetable (elle n’apparait qu’une fois)', () => {
    const option = optionRepartition(10, [1, 5])
    const { result } = monter(option)
    act(() => result.current.choisirOption(optionRepartition(10, [1, 5])))

    expect(result.current.cartes.get(CIBLES[0])?.assignerReste).toBeUndefined()
    expect(result.current.cartes.get(CIBLES[0])?.assignerResteQuantite).toBeUndefined()
    // Sa voisine, elle, apparait 5 fois : le raccourci lui reste propose.
    expect(result.current.cartes.get(CIBLES[1])?.assignerResteQuantite).toBe(5)
  })
})

// Demande de l'utilisateur (30/09/2026, apres le signalement Wiccan n35) :
// quand on repartit des degats « jusqu'a N », il faut voir combien il en reste
// a placer, et etre prevenu si l'on valide sans les avoir tous places. Le signe
// d'une selection repartie est le meme que pour `assignerReste` : le moteur
// repete la meme carte dans `all_legal_targets`.
describe('useInteraction, points repartis non tous places', () => {
  function optionRepartie(total: number, capacites: number[], minimum = 0): Option {
    const cibles: number[] = []
    CIBLES.forEach((id, i) => {
      for (let n = 0; n < (capacites[i] ?? 0); n++) cibles.push(id)
    })
    const option = optionTroisCibles()
    option.all_legal_targets = cibles
    option.target_num_range = [minimum, total]
    return option
  }

  function monterAvecReponse(option: Option) {
    const repondre = vi.fn()
    const demande: Demande = {
      options: [option],
      refus: [],
      prompt_text: '',
      event_name: 'test',
      show_cancel: true,
      ability_type: '',
    }
    const affiches = new Set([HEROS, RESSOURCE, ...CIBLES])
    const rendu = renderHook(() =>
      useInteraction(MONDE, demande, repondre, affiches, 0, CATALOGUE, 'simple')
    )
    return { ...rendu, repondre }
  }

  afterEach(() => vi.unstubAllGlobals())

  it('annonce combien de points il reste a placer', () => {
    const { result } = monterAvecReponse(optionRepartie(3, [5, 5]))
    act(() => result.current.choisirOption(optionRepartie(3, [5, 5])))
    expect(result.current.ciblesRestantes).toBe(3)

    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())
    expect(result.current.ciblesRestantes).toBe(2)
  })

  it('plafonne ce qui reste par ce que la table peut recevoir', () => {
    const { result } = monterAvecReponse(optionRepartie(4, [1, 2]))
    act(() => result.current.choisirOption(optionRepartie(4, [1, 2])))
    // 3 designations possibles au total, pas 4 : rien ne sert de reclamer la quatrieme.
    expect(result.current.ciblesRestantes).toBe(3)
  })

  it('previent avant de valider quand des points ne sont pas places, et n envoie rien si on refuse', async () => {
    const confirmMock = vi.fn((_texte?: string) => false)
    vi.stubGlobal('confirm', confirmMock)
    const { result, repondre } = monterAvecReponse(optionRepartie(3, [5, 5]))
    act(() => result.current.choisirOption(optionRepartie(3, [5, 5])))
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())

    act(() => result.current.valider())
    await waitFor(() => expect(confirmMock).toHaveBeenCalledTimes(1))
    expect(confirmMock.mock.calls[0]?.[0]).toContain('2')
    expect(repondre).not.toHaveBeenCalled()
  })

  it('envoie quand meme si le joueur confirme', async () => {
    vi.stubGlobal('confirm', vi.fn(() => true))
    const { result, repondre } = monterAvecReponse(optionRepartie(3, [5, 5]))
    act(() => result.current.choisirOption(optionRepartie(3, [5, 5])))
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())

    act(() => result.current.valider())
    await waitFor(() => expect(repondre).toHaveBeenCalledTimes(1))
  })

  it('ne dit rien quand tout est place', () => {
    const confirmMock = vi.fn(() => false)
    vi.stubGlobal('confirm', confirmMock)
    const { result, repondre } = monterAvecReponse(optionRepartie(3, [5, 5]))
    act(() => result.current.choisirOption(optionRepartie(3, [5, 5])))
    act(() => result.current.cartes.get(CIBLES[0])?.assignerReste?.())
    expect(result.current.ciblesRestantes).toBe(0)

    act(() => result.current.valider())
    expect(confirmMock).not.toHaveBeenCalled()
    expect(repondre).toHaveBeenCalledTimes(1)
  })

  it('ne s applique pas a un simple « jusqu a N cartes » (chaque carte une seule fois)', () => {
    const confirmMock = vi.fn(() => false)
    vi.stubGlobal('confirm', confirmMock)
    const { result, repondre } = monterAvecReponse(optionTroisCibles())
    act(() => result.current.choisirOption(optionTroisCibles()))
    act(() => result.current.cartes.get(CIBLES[0])?.agir?.())
    expect(result.current.ciblesRestantes).toBe(0)

    act(() => result.current.valider())
    expect(confirmMock).not.toHaveBeenCalled()
    expect(repondre).toHaveBeenCalledTimes(1)
  })
})

// Paiement automatique (24/09/2026) : quand une seule carte peut encore
// payer, elle est payee toute seule -- MONDE n'a qu'une seule carte en main
// (RESSOURCE), donc n'importe quel cout ici est deja un cas a un seul payeur.
describe('useInteraction, paiement automatique', () => {
  beforeEach(() => window.localStorage.removeItem(CLE_PAIEMENT_AUTO))
  afterEach(() => window.localStorage.removeItem(CLE_PAIEMENT_AUTO))

  it('paie tout seul quand un seul payeur reste et que le reglage est actif', async () => {
    window.localStorage.setItem(CLE_PAIEMENT_AUTO, 'on')
    const option = optionTroisCibles()
    option.all_legal_targets = [CIBLES[0]]
    const { result } = monter(option)

    // Avec le reglage deja sur 'on', l'effet paie des la composition de
    // l'option : `act()` flush deja l'effet avant de rendre la main, donc on
    // ne voit jamais l'etat "payment" intermediaire ici (contrairement au
    // test suivant, ou le reglage est coupe). On verifie directement l'etat
    // final.
    act(() => result.current.choisirOption(option))
    await waitFor(() => expect(result.current.ressources).toEqual([EFFET_RESSOURCE]))
    expect(result.current.prete).toBe(true)
  })

  it('ne paie rien tout seul quand le reglage est desactive', async () => {
    window.localStorage.setItem(CLE_PAIEMENT_AUTO, 'off')
    const option = optionTroisCibles()
    option.all_legal_targets = [CIBLES[0]]
    const { result } = monter(option)

    act(() => result.current.choisirOption(option))
    expect(result.current.assistant.etape).toBe('payment')

    // Rien ne doit bouger tout seul : on laisse passer un tick pour verifier
    // une absence, pas juste l'instant d'avant l'effet.
    await new Promise((resoudre) => setTimeout(resoudre, 0))
    expect(result.current.ressources).toEqual([])
  })

  it('propose une modale la toute premiere fois, avant tout choix persiste', async () => {
    // Ni 'on' ni 'off' : CLE_PAIEMENT_AUTO absent = 'pas-demande'. Hors
    // FournisseurConfirmation, useConfirmation retombe sur window.confirm.
    const confirmMock = vi.fn(() => true)
    vi.stubGlobal('confirm', confirmMock)
    const option = optionTroisCibles()
    option.all_legal_targets = [CIBLES[0]]
    const { result } = monter(option)

    act(() => result.current.choisirOption(option))
    await waitFor(() => expect(confirmMock).toHaveBeenCalledTimes(1))
    await waitFor(() => expect(result.current.ressources).toEqual([EFFET_RESSOURCE]))
    // La reponse est memorisee : plus jamais redemandee.
    expect(window.localStorage.getItem(CLE_PAIEMENT_AUTO)).toBe('on')
    expect(result.current.paiementAutoChoix).toBe('on')
    vi.unstubAllGlobals()
  })
})

// Signalement Yarro n23 (26/09/2026) : paiement MIXTE (une carte de main +
// une interface SP//dr), deux payeurs distincts qui couvrent chacun 1 sur un
// cout de 2. Le signalement dit que payer l'interface EN PREMIER empeche
// d'ajouter ensuite la carte de main, alors que l'ordre inverse fonctionne.
describe('useInteraction, paiement mixte a deux payeurs', () => {
  const INTERFACE = 400
  const EFFET_INTERFACE = 8

  function optionCoutMixte(): Option {
    return {
      id: 1,
      name: 'Play',
      bind_id: HEROS,
      bind_player_id: 0,
      all_legal_targets: [],
      target_num_range: [0, 0],
      target_payment: {
        0: {
          cost: '2',
          payment: [
            { effect_id: EFFET_RESSOURCE, res_text: '1' },
            { effect_id: EFFET_INTERFACE, res_text: '1' },
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

  function monterAvecInterface(option: Option) {
    const monde = {
      ...MONDE,
      players: [
        {
          ...MONDE.players[0],
          area_upgrade: [carte(INTERFACE, { resources: [EFFET_INTERFACE] })],
        },
      ],
    } as unknown as World
    const demande: Demande = {
      options: [option],
      refus: [],
      prompt_text: '',
      event_name: 'test',
      show_cancel: true,
      ability_type: '',
    }
    const affiches = new Set([HEROS, RESSOURCE, INTERFACE])
    const repondre = vi.fn()
    const rendu = renderHook(() =>
      useInteraction(monde, demande, repondre, affiches, 0, CATALOGUE, 'simple')
    )
    return { ...rendu, repondre }
  }

  /**
   * Sync Ratio avec 2 interfaces pretes ANNONCE 2 (somme des deux) meme si le
   * joueur ne veut en incliner qu'une pour completer avec la main : un seul
   * clic sur ce moyen suffit donc, a l'annonce, a couvrir tout le cout de 2.
   */
  function optionCoutMixteSurvalorise(): Option {
    const option = optionCoutMixte()
    const paiement = option.target_payment[0]
    if (!paiement) throw new Error('optionCoutMixte() doit poser target_payment[0]')
    // 'RR' = 2 ressources physiques (lettre de couleur, pas un chiffre) : deux
    // interfaces pretes annoncees ensemble par Sync Ratio pour un seul clic.
    paiement.payment[1] = { effect_id: EFFET_INTERFACE, res_text: 'RR' }
    return option
  }

  beforeEach(() => window.localStorage.setItem(CLE_PAIEMENT_AUTO, 'off'))
  afterEach(() => window.localStorage.removeItem(CLE_PAIEMENT_AUTO))

  it('accepte main puis interface', () => {
    const { result } = monterAvecInterface(optionCoutMixte())
    act(() => result.current.choisirOption(optionCoutMixte()))

    act(() => result.current.cartes.get(RESSOURCE)?.agir?.())
    act(() => result.current.cartes.get(INTERFACE)?.agir?.())

    expect(result.current.ressources.sort()).toEqual([EFFET_RESSOURCE, EFFET_INTERFACE].sort())
    expect(result.current.prete).toBe(true)
  })

  it('accepte interface puis main (ordre inverse, signalement Yarro n23)', () => {
    const { result } = monterAvecInterface(optionCoutMixte())
    act(() => result.current.choisirOption(optionCoutMixte()))

    act(() => result.current.cartes.get(INTERFACE)?.agir?.())
    // Le signalement dit que la carte de main n'est plus proposable ensuite.
    expect(result.current.cartes.get(RESSOURCE)?.agir).toBeTypeOf('function')
    act(() => result.current.cartes.get(RESSOURCE)?.agir?.())

    expect(result.current.ressources.sort()).toEqual([EFFET_RESSOURCE, EFFET_INTERFACE].sort())
    expect(result.current.prete).toBe(true)
  })

  /**
   * Signalement Yarro n24 (27/09/2026) : la carte qui porte Sync Ratio est
   * AUSSI la cible unique et obligatoire de l'amelioration jouee (elle
   * s'attache au heros). Quand les DEUX interfaces sont deja inclinees,
   * Sync Ratio n'est plus un moyen de paiement valable (absent de
   * `payment`), mais la carte reste la cible auto-selectionnee, sans
   * alternative. Le clic dessus (le joueur, habitue a cliquer cette carte
   * pour payer, la reclique par reflexe) tombe alors sur `basculerCible`,
   * qui videait TOUTE la selection de paiement en cours -- la carte de main
   * deja posee disparaissait sans message, le joueur devait tout recompter.
   */
  function optionCibleUniqueSansInterfacePrete(): Option {
    return {
      id: 1,
      name: 'Play',
      bind_id: HEROS,
      bind_player_id: 0,
      all_legal_targets: [INTERFACE],
      target_num_range: [1, 1],
      target_payment: {
        0: {
          cost: '2',
          // Sync Ratio absent : aucune interface prete, elle n'annonce plus rien.
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

  it('un clic sur la cible unique, epuisee comme payeur, n efface pas la main deja posee', () => {
    const option = optionCibleUniqueSansInterfacePrete()
    const { result } = monterAvecInterface(option)
    act(() => result.current.choisirOption(option))

    act(() => result.current.cartes.get(RESSOURCE)?.agir?.())
    expect(result.current.ressources).toEqual([EFFET_RESSOURCE])

    // La cible unique reste affichee comme "choisie", sans alternative a lui
    // substituer : son clic ne doit plus etre un detarget destructeur.
    act(() => result.current.cartes.get(INTERFACE)?.agir?.())
    expect(result.current.ressources).toEqual([EFFET_RESSOURCE])
  })

  it('la validation courte ne part pas des le clic sur l interface survalorisee, laisse ajouter la main', () => {
    window.localStorage.setItem(CLE_VALIDATION_COURTE, 'on')
    const { result, repondre } = monterAvecInterface(optionCoutMixteSurvalorise())
    act(() => result.current.choisirOption(optionCoutMixteSurvalorise()))

    // L'interface ANNONCE 2 a elle seule (deux interfaces pretes) : avant le
    // correctif, ce seul clic suffisait a declencher la validation courte et
    // `repondre` partait aussitot avec l'interface SEULE.
    act(() => result.current.cartes.get(INTERFACE)?.agir?.())
    expect(repondre).not.toHaveBeenCalled()
    expect(result.current.cartes.get(RESSOURCE)?.agir).toBeTypeOf('function')

    // La main s'ajoute normalement, mais tant que l'interface survalorisee
    // reste parmi les moyens choisis, un dernier "Valider" explicite reste
    // demande : le risque de surestimation ne disparait pas en cours de
    // route, il vaut mieux le dernier regard a chaque fois.
    act(() => result.current.cartes.get(RESSOURCE)?.agir?.())
    expect(repondre).not.toHaveBeenCalled()
    expect(result.current.prete).toBe(true)

    act(() => result.current.valider())
    expect(repondre).toHaveBeenCalledTimes(1)
    expect(repondre.mock.calls[0]?.[0]?.resources.sort()).toEqual(
      [EFFET_RESSOURCE, EFFET_INTERFACE].sort()
    )
  })

  it('la validation courte reste immediate pour un moyen unique sans risque de surestimation', () => {
    window.localStorage.setItem(CLE_VALIDATION_COURTE, 'on')
    const option = optionCoutMixte()
    option.target_payment[0] = {
      cost: '1',
      payment: [{ effect_id: EFFET_RESSOURCE, res_text: '1' }],
      rule: [],
    }
    const { result, repondre } = monterAvecInterface(option)
    act(() => result.current.choisirOption(option))

    act(() => result.current.cartes.get(RESSOURCE)?.agir?.())
    expect(repondre).toHaveBeenCalledTimes(1)
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

// Le defaut signale en jeu le 15/09/2026 : « quand je drag n drop mon perso sur
// le mechant, il me propose deux attack, l'une d'elle c'est l'attaque avec un
// allie ». Le depot calculait bien les actions de la SOURCE, puis les jetait des
// qu'il y en avait plusieurs pour ouvrir le menu de la CIBLE, qui liste tout ce
// qui peut viser cette carte, allie compris. Le geste perdait sa source.
const VILAIN = 900
const ALLIE_ATTAQUANT = 201

function attaqueDe(id: number, porteur: number): Option {
  return {
    id,
    name: 'Attack',
    bind_id: porteur,
    bind_player_id: 0,
    all_legal_targets: [VILAIN],
    target_num_range: [1, 1],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

function monterAvec(options: Option[]) {
  const demande: Demande = {
    options,
    refus: [],
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
  const affiches = new Set([HEROS, RESSOURCE, VILAIN, ...CIBLES])
  return renderHook(() =>
    useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple')
  )
}

describe('useInteraction, une cible focalisee depuis un depot', () => {
  it('ne montre que les actions de la carte lachee', () => {
    const { result } = monterAvec([attaqueDe(1, HEROS), attaqueDe(2, ALLIE_ATTAQUANT)])

    act(() => result.current.focaliserCible(VILAIN, HEROS))

    expect(result.current.options.map((o) => o.id)).toEqual([1])
  })

  it('suit les actions generales quand la source est l identite', () => {
    // `bind_id === 0` = action generale, rattachee a l'identite du joueur.
    const generale = attaqueDe(3, 0)
    const { result } = monterAvec([generale, attaqueDe(2, ALLIE_ATTAQUANT)])

    act(() => result.current.focaliserCible(VILAIN, HEROS))

    expect(result.current.options.map((o) => o.id)).toEqual([3])
  })

  it('garde toutes les actions quand la cible est cliquee, sans source', () => {
    // Le clic direct sur une cible ne change pas : il liste bien tout ce qui
    // peut la viser, c'est son role.
    const { result } = monterAvec([attaqueDe(1, HEROS), attaqueDe(2, ALLIE_ATTAQUANT)])

    act(() => result.current.focaliserCible(VILAIN))

    expect(result.current.options.map((o) => o.id)).toEqual([1, 2])
  })
})

// LA QUESTION DE LA MANIGANCE N'APPARTIENT QU'A SON PANNEAU.
//
// Defaut trouve en relecture le 15/09/2026 : la vague precedente avait ferme
// `DemandeCentrale`, la scene et `BarreAction` (voir `ou-va-la-question.ts`),
// mais PAS le menu d'une carte. `Reveal_Main_Scheme` porte `bind_id` = la
// manigance principale : la table lui posait donc son halo, et son menu
// offrait l'option sous son libelle technique brut. En mode Detaille, une
// carte qui n'a qu'une action disponible la DECLENCHE au clic (`actionUnique`)
// — le clic sur la manigance repondait donc directement a la question.
//
// Pourquoi c'est grave et pas seulement laid : pendant les 400 ms du
// retournement, `board.css` met l'overlay du panneau en `pointer-events: none`
// et la table redevient cliquable. Ce chemin-la contournait la garde « un seul
// envoi » du panneau et pouvait repondre a la question SUIVANTE.
describe('useInteraction, la question de la manigance est prise par son panneau', () => {
  const MANIGANCE = 400

  const MONDE_MANIGANCE = {
    render_id: 1,
    area_schemes_main: [carte(MANIGANCE, { card_type: 'main_scheme' })],
    players: [{ area_hero: [carte(HEROS, { card_type: 'hero' })] }],
  } as unknown as World

  function demandeManigance(): Demande {
    return {
      options: [
        {
          id: 9,
          name: NOM_OPTION_MANIGANCE,
          bind_id: MANIGANCE,
          bind_player_id: 0,
          all_legal_targets: [],
          target_num_range: [0, 0],
          target_payment: {},
          select_rule: '',
          target_must_include_traits: [],
          failure_reason: '',
          is_search: false,
        },
      ],
      refus: [],
      prompt_text: '',
      event_name: 'ConfirmMainSchemeReveal',
      show_cancel: false,
      ability_type: '',
    }
  }

  function monterManigance(mode: 'simple' | 'detailed') {
    return renderHook(() =>
      useInteraction(
        MONDE_MANIGANCE,
        demandeManigance(),
        vi.fn(),
        new Set([MANIGANCE, HEROS]),
        0,
        CATALOGUE,
        mode
      )
    )
  }

  it('ne pose aucun halo sur la manigance principale', () => {
    // Si la gate sautait : `role: 'porteur'` reviendrait sur la carte, et le
    // joueur verrait la table l'appeler alors que le panneau tient deja la
    // reponse.
    const { result } = monterManigance('simple')
    expect(result.current.cartes.get(MANIGANCE)).toBeUndefined()
  })

  it('⚠ NE DONNE AUCUN MOYEN DE REPONDRE EN CLIQUANT LA MANIGANCE', () => {
    // LE CAS QUI COMPTE. En mode Detaille, une carte qui n'a qu'une action
    // disponible la declenche AU CLIC. Sans la gate, ce clic postait la
    // reponse a la place du panneau — et, pendant le retournement, a la
    // question SUIVANTE.
    const { result } = monterManigance('detailed')
    expect(result.current.cartes.get(MANIGANCE)?.agir).toBeUndefined()
  })

  it('n offre la question dans AUCUN menu de carte', () => {
    const { result } = monterManigance('simple')
    expect(result.current.options).toEqual([])
    act(() => result.current.focaliserCarte(MANIGANCE))
    expect(result.current.options).toEqual([])
  })

  it('ne touche a rien quand la question n est pas celle de la manigance', () => {
    // La contre-epreuve : une action ordinaire garde son halo et son menu.
    const { result } = monter(optionTroisCibles())
    expect(result.current.cartes.get(HEROS)?.agir).toBeTypeOf('function')
    expect(result.current.options).toHaveLength(1)
  })
})

// Rapport n°57 (04/10/2026) : Study the Tape propose 4 cartes dans la fenêtre, la 5e
// (le DESSUS de la défausse) n'est offerte que sur la table. La règle vaut pour TOUTE
// liste de cibles : une carte qui est le dessus d'une pile y figure aussi.
describe('useInteraction, liste hors table et dessus de pile', () => {
  function optionUneCible(): Option {
    return { ...optionTroisCibles(), target_num_range: [1, 1], target_payment: {} }
  }

  // Des cartes complètes : la liste hors table les DESSINE (`toScanCard` lit leurs dos).
  const MONDE_COMPLET = {
    render_id: 1,
    players: [
      {
        area_hero: [carte(HEROS, { card_type: 'hero' })],
        area_ally: CIBLES.map((id) =>
          carte(id, { down_card_ids: [], visible_for_players: [0], is_face_up: true, pic_id: `0100${id}` })
        ),
        hand: [],
      },
    ],
  } as unknown as World

  const CATALOGUE_COMPLET = { ...CATALOGUE, aspect: () => undefined } as unknown as Catalogue

  function monterAvec(representants?: ReadonlyMap<number, number>) {
    const option = optionUneCible()
    const demande: Demande = {
      options: [option],
      refus: [],
      prompt_text: '',
      event_name: 'test',
      show_cancel: true,
      ability_type: '',
    }
    // 201 est dessinée sur la table (dessus d'une pile), 202 et 203 ne le sont pas.
    const affiches = new Set([HEROS, CIBLES[0]])
    const rendu = renderHook(() =>
      useInteraction(MONDE_COMPLET, demande, vi.fn(), affiches, 0, CATALOGUE_COMPLET, 'simple', representants)
    )
    act(() => rendu.result.current.choisirOption(option))
    return rendu
  }

  it('garde le dessus d une pile dans la liste, avec les cartes hors table', () => {
    const { result } = monterAvec(new Map([[CIBLES[0], CIBLES[0]]]))
    expect(result.current.ciblesHorsTable.map((c) => c.props.id).sort()).toEqual(
      CIBLES.map(String)
    )
  })

  it('une carte simplement posée sur la table reste absente de la liste', () => {
    const { result } = monterAvec(new Map())
    expect(result.current.ciblesHorsTable.map((c) => c.props.id).sort()).toEqual(
      [CIBLES[1], CIBLES[2]].map(String)
    )
  })
})

describe('useInteraction chez celui qui regarde (relecture fidele, 08/10/2026)', () => {
  const demande: Demande = {
    options: [optionTroisCibles()],
    refus: [],
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
  const affiches = new Set([HEROS, RESSOURCE, ...CIBLES])

  it('le joueur publie sa selection, le spectateur la montre telle quelle', () => {
    const joueur = renderHook(() => useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple'))
    act(() => joueur.result.current.choisirOption(optionTroisCibles()))
    act(() => joueur.result.current.focaliserCible(CIBLES[1]))
    const publiee = joueur.result.current.selectionPartagee!
    expect(publiee.o).toBe(optionTroisCibles().id)

    const spectateur = renderHook(() =>
      useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple', undefined, publiee)
    )
    expect(spectateur.result.current.option?.id).toBe(optionTroisCibles().id)
    expect(spectateur.result.current.cibles).toEqual(joueur.result.current.cibles)
    expect(spectateur.result.current.ressources).toEqual(joueur.result.current.ressources)
  })

  it('une selection d une autre question, ou aucune, ne montre rien', () => {
    const autre = renderHook(() =>
      useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple', undefined, {
        e: 'une autre question',
        o: optionTroisCibles().id,
        c: [],
        r: [],
      })
    )
    expect(autre.result.current.option).toBeUndefined()
    const rien = renderHook(() => useInteraction(MONDE, demande, vi.fn(), affiches, 0, CATALOGUE, 'simple', undefined, null))
    expect(rien.result.current.option).toBeUndefined()
    // Ses propres clics n'y changent rien : il regarde.
    act(() => rien.result.current.choisirOption(optionTroisCibles()))
    expect(rien.result.current.option).toBeUndefined()
  })
})

// Rapport Yarro n93 (17/10/2026) : Nebula's Ship (16093), « Exhaust the Milano
// and spend UP TO 2 resources → remove 1 evasion counter for each resource
// spent ». Le cout « jusqu'a N » n'exigeant rien, le plateau sautait droit a
// « Prêt à valider » : aucune carte ne clignotait, Yarro a valide sans rien
// depenser et le Milano s'est incline pour rien.
describe('useInteraction, cout « jusqu a N » (UpTo)', () => {
  const UN = 300
  const DEUX = 301
  const mondeUpTo = {
    render_id: 1,
    players: [
      {
        area_hero: [carte(HEROS, { card_type: 'hero' })],
        hand: [
          carte(UN, { card_type: 'event', resources: [7] }),
          carte(DEUX, { card_type: 'event', resources: [8] }),
        ],
      },
    ],
  } as unknown as World
  const vaisseau: Option = {
    id: 70,
    name: 'Shoot_the_Thrusters!',
    bind_id: HEROS,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {
      0: {
        cost: '2',
        payment: [
          { effect_id: 7, res_text: 'Y' },
          { effect_id: 8, res_text: 'BB' },
        ],
        rule: ['UpTo'],
      },
    },
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
  const monterUpTo = () => {
    const demande: Demande = {
      options: [vaisseau],
      refus: [],
      prompt_text: '',
      event_name: 'WhenPlayerInTurn',
      show_cancel: true,
      ability_type: 'FirstPlayerAction',
    }
    return renderHook(() =>
      useInteraction(mondeUpTo, demande, vi.fn(), new Set([HEROS, UN, DEUX]), 0, CATALOGUE, 'simple')
    )
  }

  it('reste a l etape du paiement, cartes surlignees, tant qu il reste de quoi depenser ; valider reste permis', () => {
    const { result } = monterUpTo()
    act(() => result.current.choisirOption(vaisseau))
    expect(result.current.assistant.etape).toBe('payment')
    expect(result.current.cartes.get(UN)?.pulse).toBe(true)
    expect(result.current.prete).toBe(true)

    act(() => result.current.cartes.get(UN)?.agir?.())
    expect(result.current.assistant.etape).toBe('payment')
    expect(result.current.assistant.coutPaye).toBe(1)
    expect(result.current.prete).toBe(true)
  })

  it('refuse de depasser N : le moteur abandonnerait le paiement et la capacite partirait pour rien', () => {
    const { result } = monterUpTo()
    act(() => result.current.choisirOption(vaisseau))
    act(() => result.current.cartes.get(UN)?.agir?.())
    act(() => result.current.cartes.get(DEUX)?.agir?.())
    expect(result.current.assistant.coutPaye).toBe(3)
    expect(result.current.prete).toBe(false)
    expect(result.current.raison).toBe('Remove 1 resource(s)')
  })

  it('a N tout juste, passe a la confirmation', () => {
    const { result } = monterUpTo()
    act(() => result.current.choisirOption(vaisseau))
    act(() => result.current.cartes.get(DEUX)?.agir?.())
    expect(result.current.assistant.etape).toBe('confirm')
    expect(result.current.prete).toBe(true)
  })
})

describe('useInteraction, toutes les cibles imposees (le vilain et ses sbires)', () => {
  const imposee = (plus: Partial<Option> = {}): Option => ({
    ...optionTroisCibles(),
    name: 'Special',
    all_legal_targets: [201, 202],
    target_num_range: [2, 2],
    target_payment: {},
    select_rule: 'VillainAndMinionsEngagedSamePlayer',
    ...plus,
  })

  it('coche toutes les cibles toute seule : rien a choisir (Morsure d araignees, rapport BL-Stark)', async () => {
    const { result } = monter(imposee())
    act(() => result.current.choisirOption(imposee()))
    await waitFor(() => expect(result.current.assistant.cibleNombre).toBe(2))
  })

  it('TEMOIN : une selection libre (meme nombre de cibles, autre regle) reste a faire a la main', async () => {
    const libre = imposee({ select_rule: '' })
    const { result } = monter(libre)
    act(() => result.current.choisirOption(libre))
    expect(result.current.assistant.cibleNombre).toBe(0)
  })

  it('TEMOIN : des cibles en trop pour le nombre demande se choisissent encore', async () => {
    const trop = imposee({ all_legal_targets: [201, 202, 203] })
    const { result } = monter(trop)
    act(() => result.current.choisirOption(trop))
    expect(result.current.assistant.cibleNombre).toBe(0)
  })
})
