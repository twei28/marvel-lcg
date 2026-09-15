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

// LA QUESTION DE LA MANIGANCE N'EST PAS OFFERTE ICI.
//
// Defaut trouve en relecture le 15/09/2026 : la barre affichait « Reveal Main
// Scheme » en meme temps que le panneau de la face A, avec ce libelle brut que
// `dico-en.ts` ne connait pas. Et pendant les 400 ms du retournement, le
// panneau passe en `pointer-events: none` : ce bouton-la restait cliquable et
// pouvait repondre a la question SUIVANTE a la place du joueur.
describe('BarreAction — la question de la manigance appartient a son panneau', () => {
  /** L'option telle que le moteur la publie pendant l'arret sur la face A. */
  function optionManigance(): Option {
    return { ...option(), id: 7, name: 'Reveal_Main_Scheme', bind_id: 3 }
  }

  /** Aucune option engagee : la barre en est au menu des propositions. */
  function interactionAuRepos(options: Option[]): Interaction {
    return {
      ...interaction(vi.fn()),
      option: undefined,
      options,
      coutAffiche: '',
    } as unknown as Interaction
  }

  it('⚠ N’OFFRE PAS le bouton de la question de la manigance', () => {
    render(
      <BarreAction
        demande={{ ...demande(), options: [optionManigance()] }}
        interaction={interactionAuRepos([optionManigance()])}
        aNous={true}
        connecte={true}
        nomPorteur={() => undefined}
        questionPriseParLePanneau={true}
      />
    )

    expect(screen.queryByRole('button', { name: /Reveal/i })).toBeNull()
    expect(screen.queryByRole('button', { name: /manigance/i })).toBeNull()
  })

  it('offre les autres questions comme avant', () => {
    render(
      <BarreAction
        demande={demande()}
        interaction={interactionAuRepos([option()])}
        aNous={true}
        connecte={true}
        nomPorteur={() => undefined}
      />
    )

    // « Play » passe par traduireMoteur et s'affiche « Jouer ».
    expect(screen.getByRole('button', { name: /Jouer/i })).toBeTruthy()
  })
})
