// Telephone (26/10/2026, maquette approuvee) : la question « choisis la cible » devient une FEUILLE qu'on glisse au doigt, avec les ronds
// des cibles DEDANS. board.tsx ne la fournit que sur telephone ; sans elle, l'assistant garde sa forme d'avant.
import { fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import { AssistantAction } from './AssistantAction'
import type { Demande, Option } from './ask'
import { nomLisible } from './BarreAction'
import type { AssistantInteraction, EtatInteractif, Interaction } from './interaction'
import type { DecorRonds } from './mobile/ronds/Rond'
import type { UniteAffichee } from './zones'

const option = (name = 'Response Marrow'): Option =>
  ({
    id: 44,
    name,
    bind_id: 0,
    bind_player_id: 0,
    all_legal_targets: [1, 2],
    target_num_range: [1, 1],
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
    coutAffiche: '',
    prete: false,
    surpaiementRecompense: false,
    assistant: {
      etape: 'target',
      titre: 'Choisis la cible',
      detail: '0/1 requise(s) · 2 possible(s)',
      cibleMinimum: 1,
      cibleMaximum: 1,
      cibleNombre: 0,
      ciblePossibles: 2,
      cibleRepetable: false,
      coutPaye: 0,
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
    ...reste,
  } as unknown as Interaction
}

const carte = (id: string): ScanCardProps => ({ id, name: `Sbire ${id}`, kind: 'minion', imageUrl: `/scan/${id}.jpg`, camp: 'encounter', jauge: { texte: '3/3', remplissage: 1, genre: 'pv', alarme: false } })
const unites: UniteAffichee[] = [
  { cle: 'u1', carte: carte('1'), attachees: [] },
  { cle: 'u2', carte: carte('2'), attachees: [] },
]
const decor = (): DecorRonds => ({
  interactifs: new Map<number, EtatInteractif>([
    [1, { role: 'cible', choisie: false }],
    [2, { role: 'cible', choisie: false }],
  ]),
  effets: new Map(),
  ouvrirPile: vi.fn(),
  ouvrirCarte: vi.fn(),
  agir: vi.fn(),
})

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

function rendre(inter: Interaction, feuilleCibles?: { unites: UniteAffichee[]; decor: DecorRonds }) {
  return render(
    <AssistantAction demande={demande()} interaction={inter} aNous={true} connecte={true} cartesParId={new Map()} designEssai={true} feuilleCibles={feuilleCibles} />
  )
}

describe('AssistantAction : la feuille du telephone', () => {
  it('avec des cibles sur la table, la question devient une feuille qui montre les ronds', () => {
    rendre(interaction(), { unites, decor: decor() })
    const feuille = document.querySelector('.est-feuille-cible')
    expect(feuille).toBeTruthy()
    expect(feuille!.querySelectorAll('.feuille-cibles .rond')).toHaveLength(2)
    expect(screen.getByText('0/1 requise(s) · 2 possible(s)')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: nomLisible(option()) })).toBeInTheDocument()
  })

  it('Annuler et valider branchent l interaction', () => {
    const inter = interaction({}, { prete: true })
    rendre(inter, { unites, decor: decor() })
    fireEvent.click(screen.getByRole('button', { name: 'Annuler' }))
    fireEvent.click(screen.getByRole('button', { name: nomLisible(option()) }))
    expect(inter.annuler).toHaveBeenCalledTimes(1)
    expect(inter.valider).toHaveBeenCalledTimes(1)
  })

  it('elle reste a l etape « confirmer » tant que des cibles sont choisies : le choix reste sous les yeux', () => {
    const inter = interaction({ etape: 'confirm', cibleNombre: 1, detail: undefined }, { prete: true, cibles: [2] })
    rendre(inter, { unites, decor: decor() })
    expect(document.querySelector('.est-feuille-cible')).toBeTruthy()
    expect(screen.getByText('1/1 requise(s) · 2 possible(s)')).toBeInTheDocument()
    expect((screen.getByRole('button', { name: nomLisible(option()) }) as HTMLButtonElement).disabled).toBe(false)
  })

  it('a l etape « confirmer » SANS cible choisie (action sans cible), l assistant garde sa forme d avant', () => {
    rendre(interaction({ etape: 'confirm' }, { prete: true, cibles: [] }), { unites, decor: decor() })
    expect(document.querySelector('.est-feuille-cible')).toBeNull()
  })

  it('sans feuille fournie (PC, tablette), l assistant garde sa forme d avant', () => {
    rendre(interaction())
    expect(document.querySelector('.est-feuille-cible')).toBeNull()
    expect(document.querySelector('.assistant-action.design-essai')).toBeTruthy()
  })

  it('sans cible sur la table (elles sont dans une pile), l assistant garde sa forme d avant', () => {
    rendre(interaction(), { unites: [], decor: decor() })
    expect(document.querySelector('.est-feuille-cible')).toBeNull()
  })

  it('a l etape du paiement, la feuille ne remplace pas l assistant (il faut montrer le cout)', () => {
    rendre(interaction({ etape: 'payment', titre: 'Payer le coût', coutRequis: 2 }), { unites, decor: decor() })
    expect(document.querySelector('.est-feuille-cible')).toBeNull()
  })
})
