import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { CartePosee } from './CartePosee'
import type { UniteAffichee } from '../zones'
import type { ScanCardProps } from '../../components/ScanCard'

const carte = (id: string, name: string, kind: ScanCardProps['kind'] = 'ally'): ScanCardProps => ({
  id, name, kind, imageUrl: '',
})

function unite(attachees: ScanCardProps[] = []): UniteAffichee {
  return { cle: 'u1', carte: { ...carte('1', 'Rhino', 'villain'), allyHp: '12/22', state: 'targetable', onSelect: () => {} }, attachees }
}

describe('CartePosee', () => {
  it('rend une VRAIE carte, avec son nom et ses PV, et se tape comme un bouton', () => {
    const ouvrir = vi.fn()
    render(<CartePosee unite={unite()} onOuvrir={ouvrir} />)
    const cible = screen.getByRole('button', { name: /Rhino/ })
    expect(cible).toHaveAttribute('data-tactile', 'carte')
    expect(cible.querySelector('.scan-card[data-card-id="1"]')).toBeInTheDocument()
    expect(screen.getByText('12/22')).toBeInTheDocument()
  })

  it('garde l\'etat d\'interaction sur la carte, mais le tap OUVRE au lieu d\'agir', () => {
    const agir = vi.fn()
    const ouvrir = vi.fn()
    const u = unite()
    u.carte.onSelect = agir
    render(<CartePosee unite={u} onOuvrir={ouvrir} />)
    expect(document.querySelector('.scan-card')).toHaveClass('state-targetable')
    fireEvent.click(screen.getByRole('button', { name: /Rhino/ }))
    expect(agir).not.toHaveBeenCalled()
    expect(ouvrir).toHaveBeenCalledWith(expect.objectContaining({ id: '1', onSelect: agir }))
  })

  it('pose les etats en pastilles lettrees, pas en cartes', () => {
    render(<CartePosee unite={unite([carte('s1', 'Stunned', 'status'), carte('s2', 'Tough', 'status')])} onOuvrir={() => {}} />)
    const pastilles = document.querySelectorAll('.carte-posee-etat')
    expect([...pastilles].map((p) => p.textContent)).toEqual(['S', 'T'])
    expect(pastilles[0]).toHaveClass('est-sonne')
    expect(pastilles[0]).toHaveAttribute('title', 'Sonné')
    // Aucune carte de statut n'est dessinee en carte.
    expect(document.querySelectorAll('.scan-card')).toHaveLength(1)
  })

  it('glisse les ameliorations derriere, tap possible sur chacune', () => {
    const ouvrir = vi.fn()
    render(
      <CartePosee
        unite={unite([carte('a1', 'Web-Shooter', 'upgrade'), carte('a2', 'Armor', 'upgrade')])}
        onOuvrir={ouvrir}
      />
    )
    const conteneur = document.querySelector<HTMLElement>('.carte-posee')
    expect(conteneur?.style.getPropertyValue('--nb')).toBe('2')
    const attachees = document.querySelectorAll<HTMLElement>('.carte-posee-attachee')
    expect(attachees).toHaveLength(2)
    expect(attachees[1].style.getPropertyValue('--i')).toBe('2')
    fireEvent.click(attachees[1])
    expect(ouvrir).toHaveBeenCalledWith(expect.objectContaining({ id: 'a2' }))
    expect(ouvrir).toHaveBeenCalledTimes(1)
  })

  it('s\'ouvre aussi au clavier, Entree ou Espace', () => {
    const ouvrir = vi.fn()
    render(<CartePosee unite={unite()} onOuvrir={ouvrir} />)
    fireEvent.keyDown(screen.getByRole('button', { name: /Rhino/ }), { key: 'Enter' })
    expect(ouvrir).toHaveBeenCalledTimes(1)
  })
})
