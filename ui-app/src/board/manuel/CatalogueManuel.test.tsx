// CatalogueManuel.test.tsx — la recherche du catalogue, en mode manuel.
//
// Le moteur ne conduit plus rien : faire apparaître une carte qui n'était pas
// dans la partie passe entièrement par ici. La recherche est par NOM (le
// joueur ne connaît aucun card_id), et ne part qu'à partir de deux caractères
// saisis — le catalogue réel dépasse les 6000 cartes, tout renvoyer à la
// première lettre serait illisible ET couteux.
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { CatalogueManuel } from './CatalogueManuel'
import { catalogueVide } from '../catalogue'

const CARTES = [
  { card_id: '01001a', name: 'Spider-Man' },
  { card_id: '01094', name: 'Rhino' },
]

const catalogue = {
  ...catalogueVide,
  chercherParNom: (fragment: string) =>
    fragment.length < 2
      ? []
      : CARTES.filter((c) => c.name.toLowerCase().includes(fragment.toLowerCase())),
}

describe('la recherche dans le catalogue', () => {
  it('ne montre rien tant qu on n a pas cherche', () => {
    render(<CatalogueManuel catalogue={catalogue} onFermer={() => {}} onPoser={() => {}} />)
    expect(screen.queryByText('Rhino')).toBeNull()
  })

  it('ne cherche pas sur une seule lettre', () => {
    render(<CatalogueManuel catalogue={catalogue} onFermer={() => {}} onPoser={() => {}} />)
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'r' } })
    expect(screen.queryByText('Rhino')).toBeNull()
  })

  it('montre les cartes qui correspondent', () => {
    render(<CatalogueManuel catalogue={catalogue} onFermer={() => {}} onPoser={() => {}} />)
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'rhi' } })
    expect(screen.getByText('Rhino')).toBeTruthy()
  })

  it('pose la carte choisie, identifiant ET nom (le journal doit dire le nom)', () => {
    const poser = vi.fn()
    render(<CatalogueManuel catalogue={catalogue} onFermer={() => {}} onPoser={poser} />)
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'rhi' } })
    fireEvent.click(screen.getByText('Rhino'))
    expect(poser).toHaveBeenCalledWith('01094', 'Rhino')
  })

  it('ferme au clic sur Fermer', () => {
    const fermer = vi.fn()
    render(<CatalogueManuel catalogue={catalogue} onFermer={fermer} onPoser={() => {}} />)
    fireEvent.click(screen.getByText('Fermer'))
    expect(fermer).toHaveBeenCalled()
  })
})
