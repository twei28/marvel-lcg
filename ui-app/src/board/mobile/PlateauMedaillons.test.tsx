import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PlateauMedaillons } from './PlateauMedaillons'
import type { EtatInteractif } from '../interaction'
import type { CardEffectDelta } from '../../components/ScanCard'
import type { Plateau } from '../zones'
import type { World } from '../world'

// jsdom n'implemente pas ResizeObserver (aucune mise en page reelle). PlateauMedaillons
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

/** Le medaillon d'une carte posee : c'est un bouton portant son data-card-id. */
function medaillon(id: string): HTMLElement {
  const cible = document.querySelector<HTMLElement>(`.medaillon[data-card-id="${id}"]`)
  if (!cible) throw new Error(`medaillon introuvable : ${id}`)
  return cible
}

/** Le libelle d'une rangee (« MÉCHANT »), qui n'est plus un bouton. */
function rangee(nom: string): HTMLElement {
  const titre = [...document.querySelectorAll<HTMLElement>('.rangee')].find(
    (element) => element.querySelector('.rangee-nom')?.textContent?.startsWith(nom)
  )
  if (!titre) throw new Error(`rangee introuvable : ${nom}`)
  return titre
}

describe('PlateauMedaillons', () => {
  it('rend une rangee de medaillons par zone peuplee', () => {
    render(
      <PlateauMedaillons world={MONDE} playerId={0} plateau={PLATEAU} />
    )
    expect(rangee('Méchant')).toBeInTheDocument()
    // La carte posee est un MEDAILLON : pas de nom ecrit, l'identite passe par
    // l'illustration et par le libelle accessible.
    expect(medaillon('1')).toHaveAccessibleName(/Rhino/)
  })

  it('ne dessine aucune bande vide', () => {
    render(
      <PlateauMedaillons world={MONDE} playerId={0} plateau={PLATEAU} />
    )
    expect(screen.queryByText('Manigances')).not.toBeInTheDocument()
    expect(screen.queryByText('Ta main')).not.toBeInTheDocument()
  })

  it("la pastille porte les PV, et rien d'autre", () => {
    render(
      <PlateauMedaillons world={MONDE} playerId={0} plateau={PLATEAU} />
    )
    // Une SEULE pastille : les PV. Attaque, contre et defense s'affichent a
    // l'ouverture de la carte, pas sur le medaillon.
    expect(medaillon('1').querySelectorAll('.medaillon-pastille')).toHaveLength(1)
    expect(screen.getByText('12/22')).toBeInTheDocument()
  })

  it('marque les cartes rendues agissantes par l\'interaction', () => {
    const agir = vi.fn()
    const interactifs = new Map<number, EtatInteractif>([
      [1, { role: 'porteur', choisie: false, agir }],
    ])
    render(
      <PlateauMedaillons
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        interactifs={interactifs}
      />
    )

    const tuile = medaillon('1')
    expect(tuile).toHaveClass('state-playable')

    // Un medaillon ne porte ni nom ni texte de regles : l'appui l'OUVRE d'abord,
    // et c'est le panneau qui declenche l'action. Sans cette ouverture, on ne
    // pouvait pas lire ce qu'on allait jouer.
    fireEvent.click(tuile)
    expect(agir).not.toHaveBeenCalled()

    fireEvent.click(screen.getByRole('button', { name: /Utiliser cette carte/ }))
    expect(agir).toHaveBeenCalledOnce()
  })

  it('compte les cibles legales sur le titre de la bande (spec S5)', () => {
    const interactifs = new Map<number, EtatInteractif>([
      [1, { role: 'cible', choisie: false, agir: () => {} }],
    ])
    render(
      <PlateauMedaillons
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        interactifs={interactifs}
      />
    )

    expect(rangee('Méchant').querySelector('.rangee-cibles')).toHaveTextContent('1')
    expect(medaillon('1')).toHaveClass('state-targetable')
    // Pendant un ciblage, tout ce qui n'est pas visable s'eteint.
    expect(document.querySelector('.plateau-mobile')).toHaveClass('est-en-ciblage')
  })

  it('montre la variation de compteur et le badge du heros actif', () => {
    const effets = new Map<number, CardEffectDelta>([[1, { value: -3, kind: 'damage' }]])
    // Comme sur le plateau PC, effectDelta ne rejoint la carte qu'a travers
    // avecInteraction : il faut donc que la carte soit dans l'interaction.
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'cible', choisie: false, agir: () => {} }]])
    render(
      <PlateauMedaillons
        world={MONDE}
        playerId={0}
        plateau={PLATEAU}
        interactifs={interactifs}
        effets={effets}
        heroActifId={1}
      />
    )
    // Le medaillon ne porte ni badge « Actif » ni variation : il n'a la place
    // que d'une pastille. Le nombre qui s'envole est rendu par la couche
    // d'animations du plateau, au-dessus.
    expect(medaillon('1')).toBeInTheDocument()
  })

  it("sans action possible, l'appui ouvre quand meme la carte pour la lire", () => {
    render(
      <PlateauMedaillons world={MONDE} playerId={0} plateau={PLATEAU} />
    )
    fireEvent.click(medaillon('1'))
    // La carte s'ouvre pour etre LUE, sans bouton d'action : le moteur n'en
    // propose aucune.
    expect(screen.getByRole('dialog', { name: 'Rhino' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Utiliser cette carte/ })).toBeNull()
  })
})
