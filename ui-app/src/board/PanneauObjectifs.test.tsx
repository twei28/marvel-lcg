// Le panneau des objectifs d'un puzzle (E3) : replie par defaut, coche ce que le moteur dit atteint, et laisse cocher les objectifs LIBRES.
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { BilanObjectifs, PanneauObjectifs, libelleObjectif } from './PanneauObjectifs'

const OBJECTIFS = [
  { kind: 'defeat_villain', text: '', target: '', done: true },
  { kind: 'survive', text: '', target: '', done: false },
  { kind: 'free_text', text: 'Garde Black Cat en vie', target: '', done: false },
]

describe('panneau des objectifs', () => {
  it('ne montre rien hors puzzle a objectifs', () => {
    const { container } = render(<PanneauObjectifs objectifs={[]} />)
    expect(container.querySelector('.panneau-objectifs')).toBeNull()
  })

  it('est replie par defaut et dit combien sont atteints', () => {
    const { container } = render(<PanneauObjectifs objectifs={OBJECTIFS} />)
    expect(container.querySelector('.panneau-objectifs-liste')).toBeNull()
    expect(container.querySelector('.panneau-objectifs-compte')?.textContent).toBe('1/3')
  })

  it('s ouvre au clic et liste les objectifs', () => {
    const { container } = render(<PanneauObjectifs objectifs={OBJECTIFS} />)
    fireEvent.click(screen.getByRole('button'))
    const lignes = container.querySelectorAll('.panneau-objectifs-liste li')
    expect(lignes).toHaveLength(3)
    expect(lignes[0].className).toContain('est-atteint')
    expect(lignes[1].className).not.toContain('est-atteint')
  })

  it('un objectif libre se coche, un objectif automatique n a pas de case', () => {
    const cocher = vi.fn()
    const { container } = render(<PanneauObjectifs objectifs={OBJECTIFS} cocher={cocher} />)
    fireEvent.click(screen.getByRole('button'))
    expect(container.querySelectorAll('input[type=checkbox]')).toHaveLength(1)
    fireEvent.click(screen.getByLabelText(/Garde Black Cat en vie/))
    expect(cocher).toHaveBeenCalledWith(2)
  })

  it('un objectif libre deja atteint ne se decoche pas', () => {
    const { container } = render(
      <PanneauObjectifs objectifs={[{ kind: 'free_text', text: 'x', target: '', done: true }]} />,
    )
    fireEvent.click(screen.getByRole('button'))
    expect((container.querySelector('input') as HTMLInputElement).disabled).toBe(true)
  })

  it('le bilan de fin marque chaque objectif atteint ou manque', () => {
    const { container } = render(<BilanObjectifs objectifs={OBJECTIFS} />)
    expect(container.querySelectorAll('.est-atteint')).toHaveLength(1)
    expect(container.querySelectorAll('.est-manque')).toHaveLength(2)
  })

  it('libelle les objectifs automatiques sans texte', () => {
    expect(libelleObjectif({ kind: 'defeat_villain', text: '', target: '', done: false })).toMatch(/méchant/)
    expect(libelleObjectif({ kind: 'complete_scheme', text: '', target: '01109', done: false })).toContain('01109')
  })
})
