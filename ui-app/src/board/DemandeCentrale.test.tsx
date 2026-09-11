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
