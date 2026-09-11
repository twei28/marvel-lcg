import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { BarreMenace } from './BarreMenace'

describe('BarreMenace', () => {
  it('dessine une case par point de menace, et remplit celles qui sont posees', () => {
    const { container } = render(<BarreMenace pose={1} total={6} />)
    expect(container.querySelectorAll('.barre-menace-case')).toHaveLength(6)
    expect(container.querySelectorAll('.barre-menace-case.est-pose')).toHaveLength(1)
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('/6')).toBeInTheDocument()
  })

  it('dit son etat aux lecteurs d ecran', () => {
    render(<BarreMenace pose={3} total={6} />)
    const jauge = screen.getByRole('meter')
    expect(jauge).toHaveAttribute('aria-valuenow', '3')
    expect(jauge).toHaveAttribute('aria-valuemax', '6')
  })

  it('ne dessine RIEN quand le total est inconnu', () => {
    // Un complot sans seuil (certaines manigances annexes) : une barre de zero
    // case serait un trait vide, pire que pas de barre.
    const { container } = render(<BarreMenace pose={2} total={0} />)
    expect(container.querySelector('.barre-menace')).toBeNull()
  })

  it('ne deborde pas quand la menace depasse le seuil', () => {
    const { container } = render(<BarreMenace pose={9} total={6} />)
    expect(container.querySelectorAll('.barre-menace-case.est-pose')).toHaveLength(6)
  })
})
