// Le volet du journal tire depuis le bord droit (VoletJournal.tsx).
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { useState } from 'react'
import { SEUIL_GESTE_PX, VoletJournal } from './VoletJournal'

function Banc() {
  const [ouvert, setOuvert] = useState(false)
  return (
    <VoletJournal ouvert={ouvert} ouvrir={() => setOuvert(true)} fermer={() => setOuvert(false)}>
      <p>Historique de la partie</p>
    </VoletJournal>
  )
}

const languette = () => screen.getByRole('button', { name: /journal/i, expanded: undefined })
const volet = () => screen.queryByRole('dialog')

describe('VoletJournal', () => {
  it('ferme au depart : seule la languette est la', () => {
    render(<Banc />)
    expect(languette()).toHaveAttribute('aria-expanded', 'false')
    expect(volet()).toBeNull()
  })

  it('un clic sur la languette ouvre, un second referme', () => {
    render(<Banc />)
    fireEvent.click(languette())
    expect(volet()).not.toBeNull()
    expect(screen.getByText('Historique de la partie')).toBeInTheDocument()
    fireEvent.click(languette())
    expect(volet()).toBeNull()
  })

  it('tirer vers la gauche ouvre, tirer vers la droite referme', () => {
    render(<Banc />)
    fireEvent.pointerDown(languette(), { clientX: 500 })
    fireEvent.pointerUp(languette(), { clientX: 500 - SEUIL_GESTE_PX - 10 })
    fireEvent.click(languette())
    expect(volet()).not.toBeNull()
    fireEvent.pointerDown(languette(), { clientX: 300 })
    fireEvent.pointerUp(languette(), { clientX: 300 + SEUIL_GESTE_PX + 10 })
    fireEvent.click(languette())
    expect(volet()).toBeNull()
  })

  it('un geste trop court compte pour un clic', () => {
    render(<Banc />)
    fireEvent.pointerDown(languette(), { clientX: 500 })
    fireEvent.pointerUp(languette(), { clientX: 495 })
    fireEvent.click(languette())
    expect(volet()).not.toBeNull()
  })

  it('Echap et la croix referment', () => {
    render(<Banc />)
    fireEvent.click(languette())
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(volet()).toBeNull()
    fireEvent.click(languette())
    fireEvent.click(screen.getByTitle('Fermer'))
    expect(volet()).toBeNull()
  })

  it('n appelle ouvrir qu une fois pour un geste', () => {
    const ouvrir = vi.fn()
    render(
      <VoletJournal ouvert={false} ouvrir={ouvrir} fermer={() => {}}>
        <p>x</p>
      </VoletJournal>
    )
    fireEvent.pointerDown(languette(), { clientX: 500 })
    fireEvent.pointerUp(languette(), { clientX: 400 })
    fireEvent.click(languette())
    expect(ouvrir).toHaveBeenCalledTimes(1)
  })
})
