// Une option ENGAGEE doit toujours offrir une issue.
//
// Le scenario qui a casse (partie reelle, 7/8/2026) : Calculated Defense dans
// la reserve de Brawn. Le joueur la choisit, decouvre qu'il ne peut pas la
// payer — le cloisonnement main/reserve retire les cartes de la main des
// payeurs possibles — et se retrouve SANS bouton pour sortir. Le moteur repose
// alors la meme question a l'infini : de l'exterieur, la partie a l'air de
// boucler sur l'attaque du vilain.
//
// La fonction `annuler` savait deja abandonner une option en cours ; c'est le
// BOUTON qui manquait, masque par un `option !== undefined ? null`.

import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { BarreAction } from './BarreAction'
import type { Demande, Option } from './ask'
import type { Interaction } from './interaction'

function option(): Option {
  return {
    id: 44,
    name: 'Play',
    bind_id: 12,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
  } as unknown as Option
}

function demande(): Demande {
  return {
    options: [option()],
    prompt_text: '',
    event_name: 'test',
    show_cancel: false,
    ability_type: '',
  } as unknown as Demande
}

/** Interaction minimale, avec une option ENGAGEE et un paiement en cours. */
function interaction(annuler: () => void): Interaction {
  return {
    option: option(),
    options: [option()],
    cartes: new Map(),
    cibles: [],
    ressources: [],
    coutAffiche: '1',
    carteFocus: undefined,
    cibleFocus: undefined,
    assistant: { etape: 'payment', titre: '', detail: '', indice: '' },
    choisirOption: vi.fn(),
    abandonnerOption: vi.fn(),
    valider: vi.fn(),
    annuler,
    defocaliser: vi.fn(),
    focaliserCarte: vi.fn(),
    focaliserCible: vi.fn(),
    ciblesHorsTable: [],
  } as unknown as Interaction
}

describe('BarreAction — issue de secours', () => {
  it('offre un bouton pour abandonner une option engagée', () => {
    const annuler = vi.fn()
    render(
      <BarreAction
        demande={demande()}
        interaction={interaction(annuler)}
        aNous={true}
        connecte={true}
        nomPorteur={() => undefined}
      />
    )

    const bouton = screen.getByRole('button', { name: 'Abandonner' })
    bouton.click()
    expect(annuler).toHaveBeenCalled()
  })

  it("ne promet plus de payer « avec des cartes de ta main »", () => {
    render(
      <BarreAction
        demande={demande()}
        interaction={interaction(vi.fn())}
        aNous={true}
        connecte={true}
        nomPorteur={() => undefined}
      />
    )

    // La main est justement INTERDITE pour une carte jouée depuis la réserve :
    // le libellé ne doit pas l'annoncer.
    expect(screen.queryByText(/cartes de ta main/)).toBeNull()
    expect(screen.getByText(/cartes surlignées/)).toBeTruthy()
  })
})
