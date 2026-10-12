// La question du moteur : survoler un bouton montre la carte qui le porte,
// et la carte est nommee en francais quand le plateau connait son nom.
//
// Avant, l'agrandissement ne s'ouvrait que pour un choix PAR TEXTE (une carte
// hors table) ; une interruption comme « Spider-Sense » ne montrait rien, et
// « Backflip » restait en anglais sous « Jouer » (retours de l'utilisateur,
// 11/09/2026).
import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import type { Demande, Option } from './ask'
import { DemandeCentrale, libelleRefus } from './DemandeCentrale'
import type { WorldCard } from './world'

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

const option = (): Option =>
  ({
    id: 7,
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
  }) as unknown as Option

const demande = (): Demande =>
  ({ options: [option()], prompt_text: '', event_name: 'WhenDamage', show_cancel: true, ability_type: 'Interrupt' }) as unknown as Demande

const cartes = new Map<number, WorldCard>([
  [12, { id: 12, name: 'Backflip', card_type: 'event' } as unknown as WorldCard],
])
const scan: ScanCardProps = { id: '12', name: 'Backflip', kind: 'event', imageUrl: '/scan/12' }

function rendre(props: Partial<Parameters<typeof DemandeCentrale>[0]> = {}) {
  return render(
    <DemandeCentrale
      demande={demande()}
      options={[option()]}
      cartesParId={cartes}
      choisirOption={vi.fn()}
      annuler={vi.fn()}
      {...props}
    />
  )
}

describe('DemandeCentrale — une fenetre de reaction se comprend sans survoler', () => {
  // « I Object! » de Jennifer Walters avant la menace du point 1 : le panneau
  // ne montrait que le nom de la capacite et « Passer ». Signale en jeu le
  // 12/09/2026 : « pour un nouveau joueur c'est pas du tout user-friendly ».
  const objection = (): Option => ({ ...option(), id: 1, name: '"I_Object!"', bind_id: 12 })
  const fenetre = (): Demande =>
    ({
      options: [objection()],
      prompt_text: '[(48,01097b) The Break-In!] s’apprête à recevoir 1⚠ (Main Scheme Phase Place Threat)',
      event_name: 'WhenSchemeWouldPlaceThreat',
      show_cancel: true,
      ability_type: 'Interrupt',
    }) as unknown as Demande
  const jennifer = new Map<number, WorldCard>([
    [12, { id: 12, name: 'Jennifer Walters', card_type: 'AlterEgo', card_id: '01019b' } as unknown as WorldCard],
  ])

  it('dans le cartouche du mechant, ni « À toi de jouer » ni « peut réagir » (03/10/2026)', () => {
    const { container } = rendre({
      demande: fenetre(),
      options: [objection()],
      cartesParId: jennifer,
      carteAuSurvol: () => ({ ...scan, name: 'Jennifer Walters' }),
      enScene: true,
    })
    expect(container.querySelector('.plateau-eyebrow')).toBeNull()
    expect(container.querySelector('.dc-reagit')).toBeNull()
    expect(screen.queryByText('Jennifer Walters peut réagir')).toBeNull()
  })

  it('dit qui peut reagir et montre la carte porteuse, sans le texte de la capacite', () => {
    rendre({
      demande: fenetre(),
      options: [objection()],
      cartesParId: jennifer,
      carteAuSurvol: () => ({ ...scan, name: 'Jennifer Walters' }),
      texteCapacite: () =>
        '"I Object!" — Interrupt: When threat would be placed on a scheme, prevent 1 of that threat. (Limit once per round.)',
    })
    expect(screen.getByText('Jennifer Walters peut réagir')).toBeInTheDocument()
    // La parenthese technique du moteur a disparu du titre, et la carte citee
    // par son code est nommee en francais (noms-fr.ts), pas « The Break-In! ».
    expect(screen.queryByText(/Main Scheme Phase/)).toBeNull()
    expect(screen.queryByText(/The Break-In!/)).toBeNull()
    expect(screen.getByText(/Effraction/)).toBeInTheDocument()
    // Plus de texte de capacite sous les boutons (retire le 03/10/2026).
    expect(screen.queryByText(/prevent 1 of that threat/)).toBeNull()
    // La vignette de la carte porteuse, sans survol.
    expect(document.querySelector('.dc-vignette')).not.toBeNull()
    // « Passer » est devenu « Ne pas utiliser … » (04/10/2026) : Objection est
    // une capacite EN JEU (pas d'`estEnMain` ici).
    expect(screen.getByRole('button', { name: /^Ne pas utiliser/ })).toBeInTheDocument()
  })

  it('le bouton prend le nom francais de la capacite quand le texte le donne', () => {
    rendre({
      demande: fenetre(),
      options: [objection()],
      cartesParId: jennifer,
      texteCapacite: () =>
        '"Objection !" — Interruption : quand de la menace est censée être placée sur une manigance, prévenez 1 de ces menaces.',
    })
    expect(screen.getByRole('button', { name: /^Objection !/ })).toBeInTheDocument()
    // Le refus reprend le meme nom : « Ne pas utiliser Objection ! ».
    expect(screen.getByRole('button', { name: 'Ne pas utiliser Objection !' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /I Object/ })).toBeNull()
  })

  it('sur un choix ordinaire, ni phrase de reaction ni texte de capacite', () => {
    rendre({
      demande: { ...fenetre(), show_cancel: false, ability_type: 'Normal', event_name: 'Choose' } as unknown as Demande,
      options: [objection()],
      cartesParId: jennifer,
      carteAuSurvol: () => scan,
      texteCapacite: () => 'un texte qui ne doit pas apparaitre',
    })
    expect(screen.queryByText(/peut réagir|Tu peux réagir/)).toBeNull()
    expect(screen.queryByText('un texte qui ne doit pas apparaitre')).toBeNull()
    expect(document.querySelector('.dc-vignette')).toBeNull()
  })
})

describe('DemandeCentrale — la carte au survol', () => {
  it('ouvre l’agrandissement de la carte porteuse quand on survole son bouton', () => {
    rendre({ carteAuSurvol: () => scan })
    fireEvent.mouseOver(screen.getByRole('button', { name: /Play|Jouer/ }))
    expect(document.querySelector('.carte-apercu')).not.toBeNull()
  })

  it('n’ouvre rien quand aucune carte n’est connue pour ce bouton', () => {
    rendre()
    fireEvent.mouseOver(screen.getByRole('button', { name: /Play|Jouer/ }))
    expect(document.querySelector('.carte-apercu')).toBeNull()
  })
})

describe('DemandeCentrale — le nom de la carte porteuse', () => {
  it('prend le nom français fourni par le plateau', () => {
    rendre({ nomPorteur: () => 'Salto arrière' })
    expect(screen.getByText('Salto arrière')).toBeInTheDocument()
    expect(screen.queryByText('Backflip')).toBeNull()
  })

  it('retombe sur le nom du moteur sans le plateau', () => {
    rendre()
    expect(screen.getByText('Backflip')).toBeInTheDocument()
  })
})

// Defaut signale en jeu le 15/09/2026, capture a l'appui : « pourquoi il montre
// l'image de mon perso deux fois ? ». Ironheart portait DEUX options de la meme
// fenetre de reaction (DEFENSE et ASK), et chaque bouton posait SA vignette :
// deux fois la meme carte cote a cote, plus la vraie sur la table.
describe('DemandeCentrale — deux boutons portes par la meme carte', () => {
  const ironheart = new Map<number, WorldCard>([
    [12, { id: 12, name: 'Ironheart', card_type: 'Hero', card_id: 'ih001a' } as unknown as WorldCard],
    [13, { id: 13, name: 'Laura Kinney', card_type: 'Ally', card_id: 'x23' } as unknown as WorldCard],
  ])
  const fenetre = (options: Option[]): Demande =>
    ({
      options,
      prompt_text: 'Ironheart is being attacked by Crossbones',
      event_name: 'WhenUnitWouldAttack',
      show_cancel: true,
      ability_type: 'Interrupt',
    }) as unknown as Demande

  it('ne pose qu UNE vignette pour les deux', () => {
    const defense = { ...option(), id: 1, name: 'Defense', bind_id: 12 }
    const ask = { ...option(), id: 2, name: 'Ask', bind_id: 12 }
    rendre({
      demande: fenetre([defense, ask]),
      options: [defense, ask],
      cartesParId: ironheart,
      carteAuSurvol: () => ({ ...scan, name: 'Ironheart' }),
    })

    expect(document.querySelectorAll('.dc-vignette')).toHaveLength(1)
    // Les deux boutons restent la : on enleve la redite, pas un choix.
    // (Les libelles sont traduits : « Defense » -> « Défendre ».)
    expect(screen.getByRole('button', { name: /Défendre/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Demander/ })).toBeInTheDocument()
  })

  it('en pose bien DEUX quand ce sont deux cartes differentes', () => {
    // Le temoin : sans lui, supprimer toutes les vignettes passerait au vert.
    const defense = { ...option(), id: 1, name: 'Defense', bind_id: 12 }
    const allie = { ...option(), id: 2, name: 'Defense', bind_id: 13 }
    rendre({
      demande: fenetre([defense, allie]),
      options: [defense, allie],
      cartesParId: ironheart,
      carteAuSurvol: (o: Option) => ({ ...scan, id: String(o.bind_id), name: `Carte ${o.bind_id}` }),
    })

    expect(document.querySelectorAll('.dc-vignette')).toHaveLength(2)
  })
})

describe('DemandeCentrale — un seul choix ne se dit pas deux fois', () => {
  // Capture du 03/10/2026 : « Fin de phase pour Domino » en titre, puis
  // « FIN DE PHASE / Domino » sur l'unique bouton. « Pourquoi il y a deux
  // boutons qui disent la meme chose ? »
  const finDePhase = (): Demande =>
    ({
      options: [option()],
      prompt_text: 'Fin de phase pour Domino',
      event_name: 'WhenPlayerInTurn',
      show_cancel: false,
      ability_type: 'Normal',
    }) as unknown as Demande

  it('sans « Passer », le titre disparait et la poignee reste', () => {
    const { container } = rendre({ demande: finDePhase() })
    expect(screen.queryByText('Fin de phase pour Domino')).toBeNull()
    expect(container.querySelector('.dc-texte.poignee-glisser.est-poignee-seule')).not.toBeNull()
    expect(container.querySelectorAll('.af-action-wrap')).toHaveLength(1)
  })

  // 12/10/2026 : « le bouton Fin de phase n'est pas tres visible » -> le jaune de Continuer, plus grand.
  it('le choix unique porte est-choix-unique (jaune, plus grand) ; pas avec « Passer » ni a deux choix', () => {
    const { container, unmount } = rendre({ demande: finDePhase() })
    expect(container.querySelector('.dc-boutons.est-choix-unique .af-action')).not.toBeNull()
    unmount()
    const avecPasser = rendre({ demande: { ...finDePhase(), show_cancel: true } })
    expect(avecPasser.container.querySelector('.est-choix-unique')).toBeNull()
    avecPasser.unmount()
    const deux = [option(), { ...option(), id: 8 }]
    const aDeux = rendre({ demande: { ...finDePhase(), options: deux }, options: deux })
    expect(aDeux.container.querySelector('.est-choix-unique')).toBeNull()
  })

  it('avec « Passer », le titre reste : il dit ce qui declenche la fenetre', () => {
    const { container } = rendre({ demande: { ...finDePhase(), show_cancel: true } })
    expect(screen.getByText('Fin de phase pour Domino')).toBeTruthy()
    expect(container.querySelector('.est-poignee-seule')).toBeNull()
  })

  it('deux choix gardent le titre', () => {
    const deux = [option(), { ...option(), id: 8 }]
    rendre({ demande: { ...finDePhase(), options: deux }, options: deux })
    expect(screen.getByText('Fin de phase pour Domino')).toBeTruthy()
  })
})

describe('DemandeCentrale — le bouton de refus dit ce qu il fait', () => {
  // Demande du 04/10/2026 : « le mot "passer" n'indique pas vraiment ce que ça
  // fait ». Choix pris une question a la fois.
  const avec = (surcharge: Partial<Option>): Option => ({ ...option(), ...surcharge }) as Option

  // Decision du 04/10/2026 : ce qui est connu de l'attaque entre parentheses
  // DANS le bouton, sur la meme ligne, pour que « Défendre avec X » et « Ne pas
  // défendre » restent au meme niveau ; detail complet au survol.
  it('defense : « Ne pas défendre (ATQ …) » dans le bouton, plus de ligne en dessous', () => {
    const defendre = avec({ name: 'Defense' })
    const { container } = rendre({
      demande: { ...demande(), options: [defendre], event_name: 'WhenEnemyAttack' } as unknown as Demande,
      options: [defendre],
      ligneSansDefense: 'ATQ 2 + 1 Armure + 1 Charge + 3 autres + 1 carte boost',
      survolSansDefense: 'ATQ 2 + 1 Armure + 1 Charge + 1 Rage + 2 Furie + 1 carte boost',
    })
    const refus = screen.getByRole('button', { name: 'Ne pas défendre (ATQ 2 + 1 Armure + 1 Charge + 3 autres + 1 carte boost)' })
    expect(refus.getAttribute('title')).toBe('ATQ 2 + 1 Armure + 1 Charge + 1 Rage + 2 Furie + 1 carte boost')
    expect(container.querySelector('.dc-pass-consequence')).toBeNull()
  })

  it('defense : « Défendre avec X (DÉF …) », la defense du personnage et ses bonus', () => {
    const defendre = avec({ name: 'Defense' })
    const avecDef = new Map<number, WorldCard>([
      [12, { id: 12, name: 'Jessica Jones', card_type: 'hero', info: { defense: 3 }, bonus: { DEF: [['Bouclier', 40, 1]] } } as unknown as WorldCard],
    ])
    rendre({
      demande: { ...demande(), options: [defendre], event_name: 'WhenEnemyAttack' } as unknown as Demande,
      options: [defendre],
      cartesParId: avecDef,
    })
    expect(screen.getByRole('button', { name: 'Défendre avec Jessica Jones (DÉF 2 + 1 Bouclier)' })).toBeInTheDocument()
  })

  it('reaction a une carte EN MAIN : « Ne pas jouer » et son nom', () => {
    expect(libelleRefus([avec({ name: 'Play' })], true, cartes, undefined, undefined, () => true)).toBe(
      'Ne pas jouer Backflip'
    )
  })

  it('reaction a une capacite EN JEU : « Ne pas utiliser » et son nom', () => {
    const sens = avec({ name: '"Spider-Sense"' })
    expect(libelleRefus([sens], true, cartes, undefined, () => '« Sens d’Araignée » — Interruption : piochez 1 carte.', () => false)).toBe(
      'Ne pas utiliser Sens d’Araignée'
    )
  })

  it('capacite nommee SANS guillemets (Spider-Sense) : son nom, pas celui de la carte', () => {
    // Vu en capture le 04/10/2026 : « Ne pas utiliser Spider-Man ».
    expect(libelleRefus([avec({ name: 'Spider-Sense' })], true, cartes, undefined, undefined, () => false)).toBe(
      'Ne pas utiliser Spider-Sense'
    )
  })

  it('en francais, la capacite prend son nom francais : « Sens d’Araignée », pas « Spider-Sense »', () => {
    // Signale le 04/10/2026. Le texte francais officiel commence par le nom.
    const texte = () => 'Sens d’Araignée — Interruption : quand le méchant initie une attaque contre vous, piochez 1 carte.'
    expect(libelleRefus([avec({ name: 'Spider-Sense' })], true, cartes, undefined, texte, () => false)).toBe(
      'Ne pas utiliser Sens d’Araignée'
    )
  })

  it('un nom technique ou un type ne prend JAMAIS l’en-tete du texte', () => {
    const texte = () => 'Scientifique — Ressource : générez une ressource.'
    expect(libelleRefus([avec({ name: 'Generate_Mental' })], true, cartes, undefined, texte, () => false)).toBe(
      'Ne pas utiliser Backflip'
    )
    expect(libelleRefus([avec({ name: 'Resource' })], true, cartes, undefined, texte, () => false)).toBe(
      'Ne pas utiliser Backflip'
    )
  })

  it('capacite sans nom : le nom de la carte, jamais « Ne pas utiliser Interruption »', () => {
    expect(libelleRefus([avec({ name: 'Interrupt' })], true, cartes, undefined, undefined, () => false)).toBe(
      'Ne pas utiliser Backflip'
    )
  })

  it('plusieurs reactions : « Ne rien jouer »', () => {
    expect(libelleRefus([avec({}), avec({ id: 8 })], true, cartes)).toBe('Ne rien jouer')
  })

  it('hors reaction et hors defense : « Passer » reste', () => {
    expect(libelleRefus([avec({})], false, cartes)).toBe('Passer')
  })
})

// « Combien de fois ce choix ? » (signalement Yarro, 05/10/2026) : la fenetre
// « Echo — choose an option » proposait « Repeat this choice 1..4 more times »
// sans dire quelle carte, quel choix etait deja fait ni combien en restait.
describe('DemandeCentrale — la question « combien de fois » nomme la carte et le choix', () => {
  const choix = (id: number, name: string): Option => ({ ...option(), id, name, bind_id: 0 })
  const question = (prompt_text: string, noms: string[]): Demande =>
    ({
      options: noms.map((nom, i) => choix(i + 1, nom)),
      prompt_text,
      event_name: 'WhenPlayerChooseAbility',
      show_cancel: false,
      ability_type: 'ChooseAbility',
    }) as unknown as Demande

  beforeEach(() => window.localStorage.setItem('marvel-langue', 'fr'))
  afterEach(() => window.localStorage.clear())

  it('apres un premier choix : carte, choix fait, reste a faire, et « Aucun / +N »', () => {
    const noms = ['No repeat', '+1', '+2', '+3', '+4']
    const d = question('[(83,53019) Strength in Diversity]: Deal 1 damage to an enemy done (1 of 5). How many more times?', noms)
    rendre({ demande: d, options: d.options })
    expect(
      screen.getByText('La Force de la Diversité : Infliger 1 dégât à un ennemi fait (1 sur 5). Combien de fois en plus ?')
    ).toBeInTheDocument()
    expect(screen.getByText('Aucun')).toBeInTheDocument()
    expect(screen.getByText('+4')).toBeInTheDocument()
  })

  it('choix unique : la question vient avant, en nombre de fois au total', () => {
    const d = question(
      '[(83,53019) Strength in Diversity]: Deal 1 damage to an enemy. How many times? (1 to 5)',
      ['1 time', '2 times', '3 times', '4 times', '5 times']
    )
    rendre({ demande: d, options: d.options })
    expect(
      screen.getByText('La Force de la Diversité : Infliger 1 dégât à un ennemi. Combien de fois ? (1 à 5)')
    ).toBeInTheDocument()
    expect(screen.getByText('1 fois')).toBeInTheDocument()
    expect(screen.getByText('5 fois')).toBeInTheDocument()
  })

  it('en anglais, rien n est traduit', () => {
    window.localStorage.setItem('marvel-langue', 'en')
    // Le nom suit les SCANS (noms-cartes-fr.ts) : la bascule 🌐 coupe les deux.
    window.localStorage.setItem('marvel-board-scans-fr', 'off')
    const d = question('[(83,53019) Strength in Diversity]: Deal 1 damage to an enemy. How many times? (1 to 2)', ['1 time', '2 times'])
    rendre({ demande: d, options: d.options })
    expect(screen.getByText('Strength in Diversity: Deal 1 damage to an enemy. How many times? (1 to 2)')).toBeInTheDocument()
    expect(screen.getByText('2 times')).toBeInTheDocument()
  })
})

// Sonic Boom, heros incline et ressources incompletes (rapport Yarro, 11/10/2026) :
// aucune option n'est faisable en entier, le moteur impose celle qu'on peut faire
// au maximum. Le joueur doit lire POURQUOI, et voir laquelle est imposee.
describe('DemandeCentrale — aucune option faisable en entier : on le dit et on surligne celle a faire', () => {
  const titre = '[(81,01123) Sonic Boom]: no option can be done in full. Do as much as you can: Spend [[energy]][[mental]]'
  const imposee = (): Option => ({ ...option(), id: 3, name: 'Spend [[energy]][[mental]]', bind_id: 0, au_maximum: true })
  const d = (): Demande =>
    ({ options: [imposee()], prompt_text: titre, event_name: 'WhenPlayerChooseAbility', show_cancel: false, ability_type: 'ChooseAbility' }) as unknown as Demande

  beforeEach(() => window.localStorage.setItem('marvel-langue', 'fr'))
  afterEach(() => window.localStorage.clear())

  it('le titre explique en francais et nomme l option imposee', () => {
    const { container } = rendre({ demande: d(), options: d().options })
    expect(container.textContent).toContain("aucune option n'est faisable en entier, tu dois en faire une au maximum. Celle-ci : Dépenser")
  })

  it('le bouton de l option imposee est surligne, pas les autres', () => {
    const autre = { ...option(), id: 4, name: 'Exhaust each character you control', bind_id: 0 }
    const { container } = rendre({ demande: d(), options: [imposee(), autre] })
    expect(container.querySelectorAll('.af-action.est-au-maximum')).toHaveLength(1)
    expect(container.querySelector('[data-option-id="3"] .af-action')?.classList.contains('est-au-maximum')).toBe(true)
  })
})

describe('DemandeCentrale — la croix annule l’action en cours', () => {
  const dansUneAction = (): Demande => ({ ...demande(), annuler_action: true })

  it('montre la croix quand la question fait partie d’une action, et la croix appelle l’annulation', () => {
    const annulerAction = vi.fn()
    rendre({ demande: dansUneAction(), annulerAction })
    fireEvent.click(screen.getByRole('button', { name: 'Annuler l’action' }))
    expect(annulerAction).toHaveBeenCalledTimes(1)
  })

  it('ne montre pas de croix hors d’une action (fenêtre de réaction, question du tour)', () => {
    rendre({ annulerAction: vi.fn() })
    expect(screen.queryByRole('button', { name: 'Annuler l’action' })).toBeNull()
  })

  it('ne montre pas de croix sans annulation branchée (mode manuel)', () => {
    rendre({ demande: dansUneAction() })
    expect(screen.queryByRole('button', { name: 'Annuler l’action' })).toBeNull()
  })
})
