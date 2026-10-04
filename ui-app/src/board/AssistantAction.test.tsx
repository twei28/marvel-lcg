// Le bouton de l'assistant nomme ce qu'il valide.
//
// « Confirmer » obligeait à relire le titre pour savoir ce qu'on confirmait.
// Sous le design essai, le bouton porte l'action elle-même : « Jouer Hawkeye »,
// « Attaquer Rhino ». Sans le drapeau, rien ne change : c'est ce que verrouille
// le premier test.

import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { AssistantAction } from './AssistantAction'
import type { Demande, Option } from './ask'
import { nomLisible } from './BarreAction'
import type { AssistantInteraction, Interaction } from './interaction'
import type { WorldCard } from './world'

function option(): Option {
  return {
    id: 44,
    name: 'Play Hawkeye',
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

function interaction(assistant: Partial<AssistantInteraction>, prete = true): Interaction {
  return {
    option: option(),
    options: [option()],
    cartes: new Map(),
    cibles: [],
    ressources: [],
    coutAffiche: '1/2',
    prete,
    surpaiementRecompense: false,
    assistant: {
      etape: 'payment',
      titre: 'Payer le coût',
      cibleMinimum: 0,
      cibleMaximum: 0,
      cibleNombre: 0,
      ciblePossibles: 0,
      cibleRepetable: false,
      coutPaye: 1,
      coutRequis: 2,
      coutSlots: [],
      coutRegles: [],
      ...assistant,
    },
    choisirOption: vi.fn(),
    abandonnerOption: vi.fn(),
    valider: vi.fn(),
    annuler: vi.fn(),
    defocaliser: vi.fn(),
    focaliserCarte: vi.fn(),
    focaliserCible: vi.fn(),
    ciblesHorsTable: [],
  } as unknown as Interaction
}

// jsdom n'implemente pas ResizeObserver : usePlacement observe le panneau pour
// le poser. Meme bouchon inerte que Board.test.tsx.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

function rendre(props: { designEssai?: boolean; affichage?: 'simple' | 'detailed' }, assistant = {}) {
  return render(
    <AssistantAction
      demande={demande()}
      interaction={interaction(assistant)}
      aNous={true}
      connecte={true}
      cartesParId={new Map()}
      {...props}
    />
  )
}

describe('AssistantAction — libellé du bouton', () => {
  it('dit « Confirmer » sans le drapeau (non-régression)', () => {
    rendre({ affichage: 'detailed' })
    expect(screen.getByRole('button', { name: 'Confirmer' })).toBeInTheDocument()
  })

  it('nomme l’action sous le design essai, en mode détaillé', () => {
    const { container } = rendre({ designEssai: true, affichage: 'detailed' })
    expect(screen.getByRole('button', { name: nomLisible(option()) })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Confirmer' })).toBeNull()
    // Le panneau porte la classe qui déclenche sa typo (board.css).
    expect(container.querySelector('.assistant-action')).toHaveClass('design-essai')
  })

  it('nomme l’action sous le design essai, en mode simple', () => {
    rendre({ designEssai: true, affichage: 'simple' })
    expect(screen.getByRole('button', { name: nomLisible(option()) })).toBeInTheDocument()
  })
})

describe('AssistantAction — le bouton nomme aussi la carte', () => {
  const cartes = (type: string) =>
    new Map([[12, { id: 12, name: 'Quinjet', card_type: type } as unknown as WorldCard]])
  const jouer = () => ({ ...option(), name: 'Play' }) as Option

  it('ajoute la carte porteuse : « Jouer Quinjet »', () => {
    render(
      <AssistantAction
        demande={demande()}
        interaction={{ ...interaction({}), option: jouer() }}
        aNous={true}
        connecte={true}
        cartesParId={cartes('Support')}
        designEssai={true}
        affichage="detailed"
      />
    )
    expect(screen.getByRole('button', { name: `${nomLisible(jouer())} Quinjet` })).toBeInTheDocument()
  })

  it('préfère le nom français fourni par le plateau', () => {
    render(
      <AssistantAction
        demande={demande()}
        interaction={{ ...interaction({}), option: jouer() }}
        aNous={true}
        connecte={true}
        cartesParId={cartes('Support')}
        nomPorteur={() => 'Quinjet (VF)'}
        designEssai={true}
        affichage="detailed"
      />
    )
    expect(screen.getByRole('button', { name: `${nomLisible(jouer())} Quinjet (VF)` })).toBeInTheDocument()
  })

  it('ne colle pas le nom du héros derrière une capacité d’identité', () => {
    render(
      <AssistantAction
        demande={demande()}
        interaction={{ ...interaction({}), option: { ...jouer(), name: 'Attack' } }}
        aNous={true}
        connecte={true}
        cartesParId={cartes('Hero')}
        designEssai={true}
        affichage="detailed"
      />
    )
    expect(screen.getByRole('button', { name: nomLisible({ ...jouer(), name: 'Attack' }) })).toBeInTheDocument()
  })
})

describe('AssistantAction — mulligan', () => {
  const mulligan = () => ({ ...option(), name: 'Resolve Mulligans' }) as Option

  it('propose de garder la main tant qu’aucune carte n’est choisie', () => {
    render(
      <AssistantAction
        demande={demande()}
        interaction={{ ...interaction({ etape: 'target', cibleNombre: 0 }), option: mulligan() }}
        aNous={true}
        connecte={true}
        cartesParId={new Map()}
        designEssai={true}
        affichage="detailed"
      />
    )
    expect(screen.getByRole('button', { name: 'Garder ma main' })).toBeInTheDocument()
  })

  it('compte les cartes à défausser dès qu’il y en a', () => {
    render(
      <AssistantAction
        demande={demande()}
        interaction={{ ...interaction({ etape: 'target', cibleNombre: 2 }), option: mulligan() }}
        aNous={true}
        connecte={true}
        cartesParId={new Map()}
        designEssai={true}
        affichage="detailed"
      />
    )
    expect(screen.getByRole('button', { name: 'Défausser 2 cartes' })).toBeInTheDocument()
  })
})

describe('AssistantAction — les pastilles du coût', () => {
  it('dessine le picto de la ressource payée, pas sa lettre anglaise', () => {
    const { container } = rendre(
      { designEssai: true, affichage: 'detailed' },
      { coutSlots: [{ index: 0, rempli: true, label: 'B', type: 'B' }, { index: 1, rempli: false }] }
    )
    const pastilles = container.querySelectorAll('.assistant-slot')
    expect(pastilles).toHaveLength(2)
    expect(pastilles[0].querySelector('.icone-res.res-mental')).not.toBeNull()
    expect(pastilles[0].textContent).not.toContain('B')
    expect(pastilles[1].querySelector('.icone-res')).toBeNull()
  })
})

describe('AssistantAction — phrase d’état', () => {
  it('dit ce qui manque, sans nommer de carte, sous le design essai', () => {
    rendre({ designEssai: true, affichage: 'detailed' })
    expect(screen.getByText('Il manque 1 ressource')).toBeInTheDocument()
  })

  it('met la carte en petit et la consigne en gros, et retire la ligne « -> »', () => {
    const { container } = render(
      <AssistantAction
        demande={demande()}
        interaction={{ ...interaction({}, false), option: { ...option(), name: 'Play' } }}
        aNous={true}
        connecte={true}
        cartesParId={new Map([[12, { id: 12, name: 'Quinjet', card_type: 'Support' } as unknown as WorldCard]])}
        designEssai={true}
        affichage="simple"
      />
    )
    expect(container.querySelector('.assistant-eyebrow')?.textContent).toBe('Quinjet')
    expect(container.querySelector('strong')?.textContent).toBe('Payer 2 pour jouer')
    expect(screen.queryByText(/->/)).toBeNull()
    // Le bouton est la, grise, au lieu d'apparaitre d'un coup une fois paye.
    const bouton = screen.getByRole('button', { name: 'Jouer Quinjet' })
    expect(bouton).toBeDisabled()
  })

  it('garde le détail d’origine sans le drapeau', () => {
    rendre({ affichage: 'detailed' }, { detail: '1/2 payé' })
    expect(screen.getByText('1/2 payé')).toBeInTheDocument()
  })
})

describe('AssistantAction — le mulligan se lit comme facultatif, dans tous les modes', () => {
  // Capture du 03/10/2026 : « ce n'est pas clair que le mulligan n'est pas
  // obligatoire ». Le panneau simple disait « Choisis les cibles 0/6 »,
  // « Annuler » et « Confirmer ».
  const mulligan = () => ({ ...option(), name: 'Resolve Mulligans' }) as Option
  const rendreMulligan = (affichage: 'simple' | 'detailed', cibleNombre: number) =>
    render(
      <AssistantAction
        demande={demande()}
        interaction={{ ...interaction({ etape: 'target', cibleNombre, cibleMaximum: 6 }), option: mulligan() }}
        aNous={true}
        connecte={true}
        cartesParId={new Map()}
        affichage={affichage}
      />
    )

  it.each(['simple', 'detailed'] as const)('mode %s : titre, consigne facultative, un seul bouton', (affichage) => {
    rendreMulligan(affichage, 0)
    expect(screen.getByText('Mulligan')).toBeInTheDocument()
    expect(screen.getByText('Sélectionne les cartes que tu veux changer (facultatif)')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Garder ma main' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Annuler' })).toBeNull()
    expect(screen.queryByText(/Choisis les cibles/)).toBeNull()
  })

  it('une carte touchee : le compte remplace la consigne et le bouton dit le geste', () => {
    rendreMulligan('simple', 1)
    expect(screen.getByText('1 carte sélectionnée')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Défausser 1 carte' })).toBeInTheDocument()
  })
})

describe('AssistantAction — la fin de tour dit qu on peut defausser', () => {
  // Capture du 04/10/2026 : « Fin de phase », « Choisis les cibles 0/6 » et un
  // seul « Annuler ». « Ce n'est pas clair qu'on peut défausser en fin de tour. »
  const finDePhase = (minimum: number) =>
    ({ ...option(), name: 'End Phase', target_num_range: [minimum, 6] }) as Option
  const rendreFin = (minimum: number, cibleNombre: number, tailleMain?: number) =>
    render(
      <AssistantAction
        demande={demande()}
        interaction={{
          ...interaction({ etape: 'target', cibleNombre, cibleMaximum: 6 }, cibleNombre >= minimum),
          option: finDePhase(minimum),
        }}
        aNous={true}
        connecte={true}
        cartesParId={new Map()}
        affichage="simple"
        tailleMain={tailleMain}
      />
    )

  it('facultatif : la consigne donne la taille de main DU heros', () => {
    rendreFin(0, 0, 6)
    expect(screen.getByText('Fin de tour')).toBeInTheDocument()
    expect(
      screen.getByText('Sélectionne les cartes que tu veux défausser (facultatif). Tu repioches jusqu’à 6.')
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Garder ma main' })).toBeEnabled()
    expect(screen.queryByRole('button', { name: 'Annuler' })).toBeNull()
  })

  it('main trop grande : le minimum est dit, le bouton attend', () => {
    rendreFin(1, 0, 5)
    expect(screen.getByText('Défausse au moins 1 carte : ta main est limitée à 5.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Défausser 1 carte' })).toBeDisabled()
  })

  it('moteur sans taille de main : aucun chiffre invente', () => {
    rendreFin(0, 0, undefined)
    expect(screen.getByText('Sélectionne les cartes que tu veux défausser (facultatif).')).toBeInTheDocument()
  })
})

// Capture du 04/10/2026 (Hulk, « Deal 1 damage to an enemy » pendant l'attaque
// de Klaw) : la cible se choisissait DANS la scene du deroule, et l'assistant
// reposait la meme question hors de la scene, a moitie sous elle.
describe('AssistantAction — cede la place a la scene du deroule', () => {
  function rendreEnScene(etape: 'target' | 'confirm' | 'payment') {
    return render(
      <AssistantAction
        demande={demande()}
        interaction={interaction({ etape })}
        aNous={true}
        connecte={true}
        cartesParId={new Map()}
        affichage="detailed"
        choixDansLaScene={true}
      />
    )
  }

  it('se tait au choix de la cible et a la confirmation', () => {
    expect(rendreEnScene('target').container.querySelector('.assistant-action')).toBeNull()
    expect(rendreEnScene('confirm').container.querySelector('.assistant-action')).toBeNull()
  })

  it('reste la pour payer un cout, que la scene ne sait pas faire', () => {
    expect(rendreEnScene('payment').container.querySelector('.assistant-action')).not.toBeNull()
  })
})
