import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { SelecteurCibles } from './SelecteurCibles'
import type { CibleHorsTable } from './interaction'

function cibleDeTest(agir = vi.fn()): CibleHorsTable {
  return {
    props: { id: '7', name: 'Iron Man', kind: 'ally', imageUrl: '/scan.jpg' },
    choisie: false,
    agir,
  }
}

describe('SelecteurCibles', () => {
  it('previent le survol quand la carte recoit le focus (tap ou tabulation)', () => {
    const survoler = vi.fn()
    render(
      <SelecteurCibles cibles={[cibleDeTest()]} titre="Choisis une cible" survoler={survoler} />
    )
    const carte = screen.getByRole('button', { name: /Iron Man/ })

    fireEvent.focus(carte)
    expect(survoler).toHaveBeenCalledWith({ id: '7', name: 'Iron Man', kind: 'ally', imageUrl: '/scan.jpg' })

    fireEvent.blur(carte)
    expect(survoler).toHaveBeenLastCalledWith(undefined)
  })

  it('le focus ne declenche pas le choix de la cible : agir() reste reserve au clic', () => {
    const agir = vi.fn()
    render(
      <SelecteurCibles cibles={[cibleDeTest(agir)]} titre="Choisis une cible" survoler={() => {}} />
    )
    const carte = screen.getByRole('button', { name: /Iron Man/ })

    fireEvent.focus(carte)
    expect(agir).not.toHaveBeenCalled()

    fireEvent.click(carte)
    expect(agir).toHaveBeenCalledOnce()
  })
})

// RAPPORT n76 (Yarro, tablette, 10/10/2026) : le Contrôle climatique de Storm
// ouvrait le sélecteur SOUS le panneau central « Choisir la cible », qui
// cachait deux des cartes. Quand toutes les cibles sont hors table, le
// sélecteur devient UNE fenêtre : les cartes, puis Annuler / Valider.
describe('SelecteurCibles en fenêtre (toutes les cibles hors table)', () => {
  const choix = (props: Partial<Parameters<typeof SelecteurCibles>[0]> = {}) => {
    const valider = vi.fn()
    const annuler = vi.fn()
    const agir = vi.fn()
    render(
      <SelecteurCibles
        cibles={[cibleDeTest(agir)]}
        titre="Contrôle climatique"
        fenetre={{ choisies: 0, minimum: 1, maximum: 1, valider, annuler }}
        {...props}
      />
    )
    return { valider, annuler, agir }
  }

  it('est une fenêtre modale qui porte le titre de l action', () => {
    choix()
    expect(screen.getByRole('dialog', { name: /Contrôle climatique/ })).toBeTruthy()
  })

  it('Valider reste grisé tant qu aucune carte n est choisie', () => {
    const { valider } = choix()
    const bouton = screen.getByRole('button', { name: 'Valider' }) as HTMLButtonElement
    expect(bouton.disabled).toBe(true)
    fireEvent.click(bouton)
    expect(valider).not.toHaveBeenCalled()
  })

  it('une carte choisie : Valider envoie', () => {
    const valider = vi.fn()
    render(
      <SelecteurCibles
        cibles={[{ ...cibleDeTest(), choisie: true }]}
        titre="Contrôle climatique"
        fenetre={{ choisies: 1, minimum: 1, maximum: 1, valider, annuler: vi.fn() }}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: 'Valider' }))
    expect(valider).toHaveBeenCalledOnce()
  })

  it('toucher une carte la choisit, Annuler annule', () => {
    const { agir, annuler } = choix()
    fireEvent.click(screen.getByRole('button', { name: /Iron Man/ }))
    expect(agir).toHaveBeenCalledOnce()
    fireEvent.click(screen.getByRole('button', { name: 'Annuler' }))
    expect(annuler).toHaveBeenCalledOnce()
  })

  it('sans `fenetre`, pas de boutons : le panneau central garde la main', () => {
    render(<SelecteurCibles cibles={[cibleDeTest()]} titre="Choisis une cible" />)
    expect(screen.queryByRole('button', { name: 'Valider' })).toBeNull()
    expect(screen.queryByRole('dialog')).toBeNull()
  })
})
