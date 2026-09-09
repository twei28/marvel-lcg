// Les jetons de l'apercu agrandi : SOUS la carte, a cote des statuts.
//
// Demande de l'utilisateur (09/09/2026) : en grand, un jeton pose sur
// l'illustration cache le texte de la carte, qu'on vient justement y lire.
// Sur la table, en revanche, ils restent sur la carte : c'est la que le joueur
// lit l'etat d'un coup d'oeil.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { JetonsCarte } from './ScanCard'

describe('les jetons d une carte', () => {
  it('ne rend rien quand la carte n en porte aucun', () => {
    const { container } = render(<JetonsCarte compteurs={[]} />)
    expect(container.firstChild).toBeNull()
  })

  it('sur la carte : les jetons a leur coin, sans conteneur', () => {
    const { container } = render(<JetonsCarte menace={3} compteurs={[]} />)
    expect(container.querySelector('.jetons-dessous')).toBeNull()
    expect(container.querySelector('.jeton-menace')?.textContent).toBe('3')
  })

  it('sous la carte : les memes jetons, dans une rangee', () => {
    const { container } = render(
      <JetonsCarte menace={3} compteurs={[{ label: 'réacteur', value: 2, cle: 'reactor' }]} dessous />
    )
    const rangee = container.querySelector('.jetons-dessous')
    expect(rangee).not.toBeNull()
    expect(rangee?.querySelector('.jeton-menace')?.textContent).toBe('3')
    expect(rangee?.querySelector('.jeton-compteur')?.textContent).toContain('2')
  })

  it('un compteur d acceleration a 1 ne montre pas son chiffre', () => {
    const { container } = render(
      <JetonsCarte compteurs={[{ label: 'accélération', value: 1, cle: 'acceleration' }]} dessous />
    )
    expect(container.querySelector('.jeton-acceleration')?.querySelector('b')).toBeNull()
  })
})
