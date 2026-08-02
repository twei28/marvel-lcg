import { describe, expect, it, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { TuileCondensee } from './TuileCondensee'
import type { ScanCardProps } from '../../components/ScanCard'

const RHINO: ScanCardProps = {
  id: '42',
  name: 'Rhino',
  kind: 'villain',
  imageUrl: '/scan.jpg',
  allyHp: '12/22',
  counters: [{ label: 'Tough', value: 1 }],
}

describe('TuileCondensee', () => {
  it('montre le nom et les compteurs sans ouvrir la carte', () => {
    render(<TuileCondensee carte={RHINO} taille="confort" onOuvrir={() => {}} />)
    expect(screen.getByText('Rhino')).toBeInTheDocument()
    expect(screen.getByText('12/22')).toBeInTheDocument()
    expect(screen.getByText('Tough 1')).toBeInTheDocument()
  })

  it('est un bouton, donc atteignable au doigt et au clavier', () => {
    const ouvrir = vi.fn()
    render(<TuileCondensee carte={RHINO} taille="confort" onOuvrir={ouvrir} />)
    screen.getByRole('button', { name: /Rhino/ }).click()
    expect(ouvrir).toHaveBeenCalledOnce()
  })

  it('porte la classe de sa taille', () => {
    const { container } = render(
      <TuileCondensee carte={RHINO} taille="plancher" onOuvrir={() => {}} />
    )
    expect(container.querySelector('.tuile')).toHaveClass('tuile-plancher')
  })

  it('ne divulgue rien d\'une carte face cachee', () => {
    render(
      <TuileCondensee
        carte={{ ...RHINO, facedown: true }}
        taille="confort"
        onOuvrir={() => {}}
      />
    )
    expect(screen.queryByText('Rhino')).not.toBeInTheDocument()
    expect(screen.queryByText('12/22')).not.toBeInTheDocument()
  })
})
