import { describe, expect, it } from 'vitest'
import type { Demande, Option } from './ask'
import { choixRefuses } from './choix-refuses'

function refus(name: string, extra: Partial<Option> = {}): Option {
  return {
    id: 7, name, bind_id: 12, failure_reason: 'update legal targets', is_text_choice: true,
    all_legal_targets: [], target_num_range: [0, 0], ...extra,
  } as unknown as Option
}

function demande(event_name: string, liste: Option[]): Demande {
  return { event_name, options: [], refus: liste } as unknown as Demande
}

describe('choixRefuses (bug 129, Nick Fury)', () => {
  it('rend le choix sans menace, grise, avec la raison en clair', () => {
    const [choix, autre] = choixRefuses(
      demande('WhenPlayerChooseAbility', [refus('Remove_2_threat_from_a_scheme'), refus('Deal_4_damage_to_an_enemy')]),
    )
    expect(choix?.failure_reason).toBe('Aucune menace à retirer pour le moment')
    expect(autre?.failure_reason).toBe('Aucune cible possible en ce moment')
    expect(choix?.id).toBeLessThan(0)
    expect(autre?.id).not.toBe(choix?.id)
  })

  it("ignore les refus qui ne sont pas des choix, et les autres fenetres", () => {
    expect(choixRefuses(demande('WhenPlayerChooseAbility', [refus('Swinging_Web_Kick', { is_text_choice: false })]))).toEqual([])
    expect(choixRefuses(demande('WhenPlayerInTurn', [refus('Remove_2_threat_from_a_scheme')]))).toEqual([])
    expect(choixRefuses(undefined)).toEqual([])
  })
})
