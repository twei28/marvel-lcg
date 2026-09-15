// La question du moteur : survoler un bouton montre la carte qui le porte,
// et la carte est nommee en francais quand le plateau connait son nom.
//
// Avant, l'agrandissement ne s'ouvrait que pour un choix PAR TEXTE (une carte
// hors table) ; une interruption comme « Spider-Sense » ne montrait rien, et
// « Backflip » restait en anglais sous « Jouer » (retours de l'utilisateur,
// 11/09/2026).
import { fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import type { Demande, Option } from './ask'
import { DemandeCentrale } from './DemandeCentrale'
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

  it('dit qui peut reagir, montre la carte porteuse et le texte de la capacite', () => {
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
    expect(screen.getByText(/prevent 1 of that threat/)).toBeInTheDocument()
    // La vignette de la carte porteuse, sans survol.
    expect(document.querySelector('.dc-vignette')).not.toBeNull()
    expect(screen.getByRole('button', { name: /Passer/ })).toBeInTheDocument()
  })

  it('le bouton prend le nom francais de la capacite quand le texte le donne', () => {
    rendre({
      demande: fenetre(),
      options: [objection()],
      cartesParId: jennifer,
      texteCapacite: () =>
        '"Objection !" — Interruption : quand de la menace est censée être placée sur une manigance, prévenez 1 de ces menaces.',
    })
    expect(screen.getByRole('button', { name: /Objection !/ })).toBeInTheDocument()
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
