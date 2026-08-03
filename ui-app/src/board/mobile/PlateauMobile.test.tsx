import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PlateauMobile } from './PlateauMobile'
import type { EtatInteractif } from '../interaction'
import type { CardEffectDelta } from '../../components/ScanCard'
import type { Plateau } from '../zones'
import type { World } from '../world'

// jsdom n'implemente pas ResizeObserver (aucune mise en page reelle). PlateauMobile
// en observe le cadre pour recalculer sa largeur de condensation : sans ce bouchon,
// tout rendu leverait une ReferenceError des le premier effet.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon

const MONDE = {
  phase: 'Player 1 Turn',
  round_id: 3,
  prompt: '',
  players: [],
} as unknown as World

const PLATEAU: Plateau = {
  emplacements: [
    {
      cle: 'rencontre',
      titre: 'Méchant',
      nombreSurLaLigne: 1,
      groupes: [
        [
          {
            cle: 'v',
            carte: { id: '1', name: 'Rhino', kind: 'villain', imageUrl: '', allyHp: '12/22' },
            attachees: [],
          },
        ],
      ],
    },
  ],
  nombreDeCartes: 1,
  idsAffiches: new Set<number>([1]),
  representantsDePile: new Map<number, number>(),
  nombreIgnore: 0,
}

describe('PlateauMobile', () => {
  it('montre le HUD et les bandes peuplees', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    expect(screen.getByText('Méchant')).toBeInTheDocument()
    expect(screen.getByText('Rhino')).toBeInTheDocument()
  })

  it('ne dessine aucune bande vide', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    expect(screen.queryByText('Manigances')).not.toBeInTheDocument()
    expect(screen.queryByText('Ta main')).not.toBeInTheDocument()
  })

  it('ouvre la bande en focus au tap sur son titre', () => {
    render(
      <PlateauMobile world={MONDE} playerId={0} plateau={PLATEAU} source="test" />
    )
    fireEvent.click(screen.getByRole('button', { name: /Méchant/ }))
    expect(screen.getByRole('dialog', { name: 'Méchant' })).toBeInTheDocument()
  })

  it('marque les cartes rendues agissantes par l\'interaction', () => {
    const agir = vi.fn()
    const interactifs = new Map<number, EtatInteractif>([
      [1, { role: 'porteur', choisie: false, agir }],
    ])
    render(
      <PlateauMobile
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        source="test"
        interactifs={interactifs}
      />
    )

    const tuile = screen.getByRole('button', { name: /Rhino/ })
    expect(tuile).toHaveAttribute('data-etat', 'playable')

    // Le clic passe par l'action du moteur, pas par onCardClick : c'est la
    // branche `if (carte.onSelect)` de ouvrirCarte, qui etait du code mort.
    fireEvent.click(tuile)
    expect(agir).toHaveBeenCalledOnce()
  })

  it('compte les cibles legales sur le titre de la bande (spec S5)', () => {
    const interactifs = new Map<number, EtatInteractif>([
      [1, { role: 'cible', choisie: false, agir: () => {} }],
    ])
    render(
      <PlateauMobile
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        source="test"
        interactifs={interactifs}
      />
    )

    const titre = screen.getByRole('button', { name: /Méchant/ })
    expect(titre).toHaveTextContent('1')
    expect(screen.getByRole('button', { name: /Rhino/ })).toHaveAttribute(
      'data-etat',
      'targetable'
    )
  })

  it('montre la variation de compteur et le badge du heros actif', () => {
    const effets = new Map<number, CardEffectDelta>([[1, { value: -3, kind: 'damage' }]])
    // Comme sur le plateau PC, effectDelta ne rejoint la carte qu'a travers
    // avecInteraction : il faut donc que la carte soit dans l'interaction.
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'cible', choisie: false, agir: () => {} }]])
    render(
      <PlateauMobile
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        source="test"
        interactifs={interactifs}
        effets={effets}
        heroActifId={1}
      />
    )
    expect(screen.getByText('-3')).toBeInTheDocument()
    expect(screen.getByText('Actif')).toBeInTheDocument()
  })

  it('sans interaction, un clic retombe sur onCardClick', () => {
    const onCardClick = vi.fn()
    render(
      <PlateauMobile
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        source="test"
        onCardClick={onCardClick}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: /Rhino/ }))
    expect(onCardClick).toHaveBeenCalledOnce()
  })
})
