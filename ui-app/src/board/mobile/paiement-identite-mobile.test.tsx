// Payer avec une capacite portee par l'IDENTITE, sur le plateau mobile.
//
// Le cas reel : Venom joue Sonic Rifle (cout 3). Le moteur propose la double
// ressource de la main ET « Symbiotic Bond », porte par la carte d'identite.
// Sur telephone, les cartes posees sont des MEDAILLONS : un appui les OUVRE
// pour les lire, l'action se declenchant depuis le panneau. Les cartes de la
// main, elles, agissent directement. Ces tests verrouillent le fait que le
// chemin du medaillon mene bien jusqu'au paiement.

import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PlateauMobile } from './PlateauMobile'
import type { EtatInteractif } from '../interaction'
import type { Plateau } from '../zones'
import type { World } from '../world'

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon

const IDENTITE = 12

const MONDE = {
  phase: 'Player 1 Turn',
  round_id: 3,
  prompt: '',
  players: [],
} as unknown as World

/** Un plateau reduit a la bande des heros : l'identite y est un medaillon. */
const PLATEAU: Plateau = {
  emplacements: [
    {
      cle: 'terrain-soutien',
      titre: 'Héros et soutiens',
      nombreSurLaLigne: 1,
      groupes: [
        [
          {
            cle: 'h',
            carte: { id: String(IDENTITE), name: 'Venom', kind: 'hero', imageUrl: '' },
            attachees: [],
          },
        ],
      ],
    },
  ],
  nombreDeCartes: 1,
  idsAffiches: new Set<number>([IDENTITE]),
  representantsDePile: new Map<number, number>(),
  nombreIgnore: 0,
}

function medaillon(id: string): HTMLElement {
  const cible = document.querySelector<HTMLElement>(`.medaillon[data-card-id="${id}"]`)
  if (!cible) throw new Error(`medaillon introuvable : ${id}`)
  return cible
}

describe('paiement par l identite sur le plateau mobile', () => {
  it('allume l identite quand elle peut payer', () => {
    const interactifs = new Map<number, EtatInteractif>([
      [IDENTITE, { role: 'ressource', choisie: false, agir: () => {} }],
    ])
    render(
      <PlateauMobile
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        interactifs={interactifs}
      />
    )

    // Un paiement est en cours : le plateau doit le signaler et laisser
    // l'identite en pleine lumiere, sinon elle passe pour eteinte.
    expect(medaillon(String(IDENTITE))).toHaveClass('state-playable')
  })

  it('declenche le paiement depuis le panneau de la carte', () => {
    const agir = vi.fn()
    const interactifs = new Map<number, EtatInteractif>([
      [IDENTITE, { role: 'ressource', choisie: false, agir }],
    ])
    render(
      <PlateauMobile
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        interactifs={interactifs}
      />
    )

    // Un medaillon s'OUVRE d'abord (il ne porte ni nom ni texte de regles).
    fireEvent.click(medaillon(String(IDENTITE)))
    const panneau = screen.getByRole('dialog', { name: 'Venom' })
    expect(panneau).toBeInTheDocument()

    // C'est ICI que le paiement doit pouvoir se declencher.
    const bouton = screen.getByRole('button', { name: /Utiliser cette carte/ })
    fireEvent.click(bouton)
    expect(agir).toHaveBeenCalled()
  })
})
