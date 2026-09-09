// Un geste vaut le choix : ce qu'on a traine sur un ennemi part sans qu'on le
// confirme une seconde fois.
//
// LE DEFAUT, SIGNALE DES LE PREMIER ESSAI (08/09/2026) : « ca me demande la
// confirmation apres avoir drag vers un ennemi pour frapper ».
//
// La cause etait un garde-fou legitime de la validation courte : elle ne se
// declenche que si l'action n'avait QU'UNE cible legale, au motif qu'un joueur
// qui vient de choisir parmi plusieurs gagne a jeter un dernier regard avant de
// lancer. Ce motif ne tient plus quand la cible a ete DESIGNEE d'un geste :
// lui redemander confirmation, c'est lui faire faire deux fois le meme choix.
//
// Ce que ces cas verrouillent, dans les deux sens :
//  - au geste, avec plusieurs cibles legales, l'action part ;
//  - au clic, avec plusieurs cibles legales, elle attend toujours ;
//  - et le geste ne force RIEN quand il reste quelque chose a decider.
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import type { Demande, Option } from '../ask'
import type { Catalogue } from '../catalogue'
import { useInteraction } from '../interaction'
import type { World } from '../world'

const HEROS = 100
const ENNEMIS = [201, 202]
const RESSOURCE = 300
const EFFET_RESSOURCE = 7

function carte(id: number, extra: Record<string, unknown> = {}) {
  return {
    id,
    card_type: 'minion',
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
      area_hero: [carte(HEROS, { card_type: 'hero' })],
      engaged_enemies: ENNEMIS.map((id) => carte(id)),
      hand: [carte(RESSOURCE, { card_type: 'event', resources: [EFFET_RESSOURCE] })],
    },
  ],
} as unknown as World

const CATALOGUE: Catalogue = {
  pvMax: () => undefined,
  statImprimee: () => undefined,
  motsCles: () => [],
  surpayable: () => false,
  type: () => undefined,
} as unknown as Catalogue

/** Une attaque de base : deux ennemis possibles, aucun cout. */
function attaque(): Option {
  return {
    id: 1,
    name: 'Attack',
    bind_id: HEROS,
    bind_player_id: 0,
    all_legal_targets: [...ENNEMIS],
    target_num_range: [1, 1],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

/** La meme, mais elle coute une ressource : il reste a payer. */
function attaquePayante(): Option {
  return {
    ...attaque(),
    id: 2,
    target_payment: {
      0: { cost: '1', payment: [{ effect_id: EFFET_RESSOURCE, res_text: '1' }], rule: [] },
    },
  } as Option
}

function monter(option: Option) {
  const repondre = vi.fn()
  const demande: Demande = {
    options: [option],
    prompt_text: '',
    event_name: 'test',
    show_cancel: true,
    ability_type: '',
  }
  const affiches = new Set([HEROS, RESSOURCE, ...ENNEMIS])
  const rendu = renderHook(() =>
    useInteraction(MONDE, demande, repondre, affiches, 0, CATALOGUE, 'simple')
  )
  return { ...rendu, repondre }
}

describe('un geste vaut le choix', () => {
  it('lache sur un ennemi, l attaque part sans confirmation', () => {
    const { result, repondre } = monter(attaque())
    act(() => result.current.choisirOption(attaque(), [ENNEMIS[0]!], true))
    expect(repondre).toHaveBeenCalledTimes(1)
    expect(repondre.mock.calls[0]![0]).toMatchObject({ id: 1, targets: [ENNEMIS[0]] })
  })

  // ⚠ LE TEMOIN QUI COMPTE. Sans lui, on ne saurait pas si l'action part parce
  // que le geste l'a voulu, ou parce que la validation courte part toujours.
  it('choisie au CLIC, avec deux cibles possibles, elle attend toujours', () => {
    const { result, repondre } = monter(attaque())
    act(() => result.current.choisirOption(attaque(), [ENNEMIS[0]!]))
    expect(repondre).not.toHaveBeenCalled()
    expect(result.current.assistant.etape).toBe('confirm')
  })

  it('le geste ne saute pas le paiement qui reste du', () => {
    const { result, repondre } = monter(attaquePayante())
    act(() => result.current.choisirOption(attaquePayante(), [ENNEMIS[0]!], true))
    expect(repondre).not.toHaveBeenCalled()
    expect(result.current.assistant.etape).toBe('payment')
  })

  // Le geste marque UNE option : celle qu'on a lachee. Une action engagee au
  // clic juste apres ne doit pas heriter de sa dispense de confirmation.
  it('la dispense ne deborde pas sur l action suivante', () => {
    const { result, repondre } = monter(attaque())
    act(() => result.current.choisirOption(attaque(), [ENNEMIS[0]!], true))
    expect(repondre).toHaveBeenCalledTimes(1)
    act(() => result.current.annuler())
    act(() => result.current.choisirOption(attaque(), [ENNEMIS[1]!]))
    expect(repondre).toHaveBeenCalledTimes(1)
  })
})
