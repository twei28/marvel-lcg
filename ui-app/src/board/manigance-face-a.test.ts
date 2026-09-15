import { describe, expect, it } from 'vitest'
import {
  NOM_OPTION_MANIGANCE,
  maniganceAMontrer,
  questionDeLaManigance,
} from './manigance-face-a'
import type { Demande, Option } from './ask'
import type { World } from './world'

function option(nom: string): Option {
  return {
    id: 7,
    name: nom,
    bind_id: 0,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  }
}

function demande(options: Option[]): Demande {
  return {
    options,
    refus: [],
    prompt_text: '',
    event_name: '',
    show_cancel: false,
    ability_type: '',
  }
}

describe('questionDeLaManigance', () => {
  it('reconnaît la question du moteur à son nom technique', () => {
    const trouvee = questionDeLaManigance(demande([option(NOM_OPTION_MANIGANCE)]))
    expect(trouvee?.id).toBe(7)
  })

  it('ne se déclenche pas sur une autre question', () => {
    expect(questionDeLaManigance(demande([option('Attack')]))).toBeUndefined()
  })

  it('ne se déclenche pas quand le moteur ne demande rien', () => {
    expect(questionDeLaManigance(undefined)).toBeUndefined()
  })

  it("refuse une question qui porte AUSSI d'autres options", () => {
    // Une option de plus veut dire que ce n'est pas notre moment : on ne
    // détourne pas une question à laquelle le joueur doit vraiment répondre.
    const melange = demande([option(NOM_OPTION_MANIGANCE), option('Attack')])
    expect(questionDeLaManigance(melange)).toBeUndefined()
  })
})

describe('maniganceAMontrer', () => {
  it('rend la manigance principale en jeu', () => {
    const monde = {
      area_schemes_main: [{ id: 48, card_id: '01097a', name: 'The Break-In!' }],
    } as unknown as World
    expect(maniganceAMontrer(monde)?.card_id).toBe('01097a')
  })

  it('rend undefined quand la zone est vide', () => {
    const monde = { area_schemes_main: [] } as unknown as World
    expect(maniganceAMontrer(monde)).toBeUndefined()
  })

  it('rend undefined sans monde', () => {
    expect(maniganceAMontrer(undefined)).toBeUndefined()
  })
})
