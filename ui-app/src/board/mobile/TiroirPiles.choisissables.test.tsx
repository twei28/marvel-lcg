import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { TiroirPiles } from './TiroirPiles'
import { Encoche } from './Encoche'
import type { PileAffichee } from './bandes-portrait'

const pile = (cle: string, ids: number[]): PileAffichee =>
  ({
    cle,
    titre: cle,
    compte: ids.length,
    unite: {
      carte: { id: String(ids[0] ?? 0), name: cle, kind: 'ally', imageUrl: '/x.jpg' },
      pileContenu: ids.map((id) => ({ id: String(id), name: `c${id}`, kind: 'ally', imageUrl: '/x.jpg' })),
      pileTitre: cle,
    },
  }) as unknown as PileAffichee

// Demande de l'utilisateur (26/10/2026) : le choix attend (fenetre fermee sans annuler) -> l'onglet « Piles » clignote, et le
// tiroir met en evidence les piles ou l'on peut choisir une carte ; un tap dessus rouvre le choix au lieu de simplement les regarder.
describe('Encoche : clignote tant qu’un choix attend', () => {
  it('porte la classe « attend-un-choix » quand `attend` est vrai, et pas sinon', () => {
    const { rerender } = render(<Encoche cote="gauche" libelle="Piles" onOuvrir={() => {}} attend />)
    expect(screen.getByRole('button', { name: 'Piles' }).className).toContain('attend-un-choix')
    rerender(<Encoche cote="gauche" libelle="Piles" onOuvrir={() => {}} />)
    expect(screen.getByRole('button', { name: 'Piles' }).className).not.toContain('attend-un-choix')
  })
})

describe('TiroirPiles : piles où l’on peut choisir', () => {
  const piles = [pile('joueur-deck', [1, 2, 3]), pile('joueur-defausse', [4, 5]), pile('nemesis-set', [9])]

  it('met en evidence les piles choisissables, avec leur nombre de cartes', () => {
    render(
      <TiroirPiles
        piles={piles}
        ouvert
        onFermer={() => {}}
        onOuvrirPile={() => {}}
        choisissables={new Map([['joueur-deck', 2], ['joueur-defausse', 1]])}
        onChoisir={() => {}}
      />
    )
    const lignes = document.querySelectorAll('.tiroir-pile')
    expect(lignes[0].className).toContain('est-choisissable')
    expect(lignes[0].textContent).toContain('2')
    expect(lignes[1].className).toContain('est-choisissable')
    expect(lignes[2].className).not.toContain('est-choisissable')
  })

  it('un tap sur une pile choisissable rouvre le choix, ferme le tiroir, et n’etale pas la pile', () => {
    const onChoisir = vi.fn()
    const onOuvrirPile = vi.fn()
    const onFermer = vi.fn()
    render(
      <TiroirPiles
        piles={piles}
        ouvert
        onFermer={onFermer}
        onOuvrirPile={onOuvrirPile}
        choisissables={new Map([['joueur-deck', 2]])}
        onChoisir={onChoisir}
      />
    )
    fireEvent.click(document.querySelectorAll('.tiroir-pile')[0])
    expect(onChoisir).toHaveBeenCalledOnce()
    expect(onFermer).toHaveBeenCalled()
    expect(onOuvrirPile).not.toHaveBeenCalled()
  })
})
