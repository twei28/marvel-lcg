import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { BarreManuelle } from './BarreManuelle'
import * as triche from '../../triche'

vi.mock('../../triche', () => ({
  blesser: vi.fn(async () => true),
  soigner: vi.fn(async () => true),
  poserMenace: vi.fn(async () => true),
  poserCompteur: vi.fn(async () => true),
  incliner: vi.fn(async () => true),
  redresser: vi.fn(async () => true),
  defausser: vi.fn(async () => true),
}))

const carte = (reste = {}) => ({ id: '12', name: 'Rhino', kind: 'villain' as const, imageUrl: '', ...reste })

describe('BarreManuelle (Q52)', () => {
  it('ne montre rien sans rond choisi', () => {
    const { container } = render(<BarreManuelle carte={undefined} onLire={() => {}} onFermer={() => {}} />)
    expect(container.firstChild).toBeNull()
  })
  it('agit sur le rond choisi : PV, epuiser, defausser', () => {
    render(<BarreManuelle carte={carte()} onLire={() => {}} onFermer={() => {}} />)
    fireEvent.click(screen.getByRole('button', { name: 'PV −1' }))
    expect(triche.blesser).toHaveBeenCalledWith(12, 1)
    fireEvent.click(screen.getByRole('button', { name: 'Incliner' }))
    expect(triche.incliner).toHaveBeenCalledWith(12)
    fireEvent.click(screen.getByRole('button', { name: 'Défausser' }))
    expect(triche.defausser).toHaveBeenCalledWith(12)
  })
  it('une manigance a la menace, pas les PV', () => {
    render(<BarreManuelle carte={carte({ kind: 'main-scheme' })} onLire={() => {}} onFermer={() => {}} />)
    fireEvent.click(screen.getByRole('button', { name: 'Menace +1' }))
    expect(triche.poserMenace).toHaveBeenCalledWith(12, 1)
    expect(screen.queryByRole('button', { name: 'PV −1' })).toBeNull()
  })
})
