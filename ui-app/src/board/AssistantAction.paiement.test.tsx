// Telephone (26/10/2026) : « PAY 2 TO PLAY » ne cache plus la main. La question du paiement devient la MEME feuille qu'on glisse au
// doigt, avec DEDANS les cartes qui peuvent payer (main, puis table) : un toucher paie, un second retire.
import { fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import { AssistantAction } from './AssistantAction'
import type { Demande, Option } from './ask'
import type { AssistantInteraction, Interaction } from './interaction'
import type { UniteAffichee } from './zones'

const option = (): Option =>
  ({
    id: 7,
    name: 'Play Stop Hitting Yourself',
    bind_id: 0,
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
  ({ options: [option()], prompt_text: '', event_name: 'test', show_cancel: false, ability_type: '' }) as unknown as Demande

function interaction(assistant: Partial<AssistantInteraction> = {}, reste: Partial<Interaction> = {}): Interaction {
  return {
    option: option(),
    options: [option()],
    cartes: new Map(),
    cibles: [],
    ressources: [],
    coutAffiche: '2',
    prete: false,
    surpaiementRecompense: false,
    assistant: {
      etape: 'payment',
      titre: 'Payer 2 pour jouer',
      cibleMinimum: 0,
      cibleMaximum: 0,
      cibleNombre: 0,
      ciblePossibles: 0,
      cibleRepetable: false,
      coutRequis: 2,
      coutPaye: 0,
      coutSlots: [
        { index: 0, rempli: false },
        { index: 1, rempli: false },
      ],
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
    ...reste,
  } as unknown as Interaction
}

const carte = (id: string, extra: Partial<ScanCardProps> = {}): ScanCardProps => ({ id, name: `Carte ${id}`, kind: 'event', imageUrl: `/scan/${id}.jpg`, state: 'playable', onSelect: vi.fn(), ...extra })
const cartes: UniteAffichee[] = [
  { cle: 'm1', carte: carte('1'), attachees: [] },
  { cle: 'm2', carte: carte('2'), attachees: [] },
  { cle: 'm3', carte: carte('3', { state: 'selected' }), attachees: [] },
]

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

function rendre(inter: Interaction, feuillePaiement?: { cartes: UniteAffichee[] }) {
  return render(
    <AssistantAction demande={demande()} interaction={inter} aNous={true} connecte={true} cartesParId={new Map()} designEssai={true} feuillePaiement={feuillePaiement} />
  )
}

describe('AssistantAction : la feuille de paiement du telephone', () => {
  it('montre les cartes qui peuvent payer DANS la feuille, avec ce qui manque', () => {
    rendre(interaction(), { cartes })
    const feuille = document.querySelector('.est-feuille-cible.est-feuille-paiement')
    expect(feuille).toBeTruthy()
    expect(feuille!.querySelectorAll('.feuille-paiement-main [data-tactile="carte-main"]')).toHaveLength(3)
    expect(screen.getByText('Il manque 2 ressources')).toBeInTheDocument()
  })

  it('montre les emplacements du cout, remplis au fur et a mesure', () => {
    rendre(
      interaction({ coutPaye: 1, coutSlots: [{ index: 0, rempli: true, type: 'Y', label: 'Y' }, { index: 1, rempli: false }] }),
      { cartes }
    )
    const slots = document.querySelectorAll('.feuille-paiement-slots .assistant-slot')
    expect(slots).toHaveLength(2)
    expect(slots[0]!.className).toContain('est-rempli')
    expect(slots[1]!.className).not.toContain('est-rempli')
    expect(screen.getByText('Il manque 1 ressource')).toBeInTheDocument()
  })

  it('un toucher sur une carte de la main la paie (action du moteur)', () => {
    rendre(interaction(), { cartes })
    const premiere = document.querySelectorAll('.feuille-paiement-main [data-tactile="carte-main"] button, .feuille-paiement-main [data-tactile="carte-main"] [role="button"]')[0] as HTMLElement
    fireEvent.click(premiere)
    expect(cartes[0]!.carte.onSelect).toHaveBeenCalledTimes(1)
  })

  it('le bouton « jouer » reste grise tant que le cout n est pas couvert, puis s active', () => {
    const { unmount } = rendre(interaction(), { cartes })
    const bouton = () => document.querySelector('.est-feuille-cible .assistant-confirmer') as HTMLButtonElement
    expect(bouton().disabled).toBe(true)
    unmount()
    const inter = interaction({ coutPaye: 2 }, { prete: true })
    rendre(inter, { cartes })
    expect(bouton().disabled).toBe(false)
    fireEvent.click(bouton())
    expect(inter.valider).toHaveBeenCalledTimes(1)
    fireEvent.click(screen.getByRole('button', { name: 'Annuler' }))
    expect(inter.annuler).toHaveBeenCalledTimes(1)
  })

  it('le cout couvert se dit', () => {
    rendre(interaction({ coutPaye: 2 }, { prete: true }), { cartes })
    expect(screen.getByText('Coût couvert')).toBeInTheDocument()
  })

  it('sans carte a montrer, ou hors paiement, ou sans feuille fournie (PC, tablette), l assistant garde sa forme d avant', () => {
    rendre(interaction(), { cartes: [] })
    expect(document.querySelector('.est-feuille-paiement')).toBeNull()
    expect(document.querySelector('.assistant-action.design-essai')).toBeTruthy()
  })

  it('sans feuille fournie, rien ne change', () => {
    rendre(interaction())
    expect(document.querySelector('.est-feuille-paiement')).toBeNull()
  })

  it('a l etape « cible » ou « confirmer », la feuille de paiement ne s ouvre pas', () => {
    rendre(interaction({ etape: 'confirm' }, { prete: true }), { cartes })
    expect(document.querySelector('.est-feuille-paiement')).toBeNull()
  })
})
