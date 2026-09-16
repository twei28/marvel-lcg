// Le bandeau de mise à jour : il ne s'affiche que quand il faut, et son bouton
// recharge vraiment.
import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { BandeauMiseAJour } from './BandeauMiseAJour'

describe('BandeauMiseAJour', () => {
  it('ne montre rien tant qu’il n’y a rien à dire', () => {
    const { container } = render(<BandeauMiseAJour visible={false} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('annonce la mise à jour et propose de recharger', () => {
    render(<BandeauMiseAJour visible={true} />)
    expect(screen.getByRole('status').textContent).toMatch(/mise à jour/i)
    expect(screen.getByRole('button', { name: /recharger/i })).toBeTruthy()
  })

  it('le bouton appelle bien le rechargement', () => {
    const recharger = vi.fn()
    render(<BandeauMiseAJour visible={true} recharger={recharger} />)
    screen.getByRole('button', { name: /recharger/i }).click()
    expect(recharger).toHaveBeenCalledOnce()
  })
})
