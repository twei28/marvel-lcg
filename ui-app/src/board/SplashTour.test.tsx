// Le splash « a qui le tour » annonce aussi la phase du mechant. En mode
// detaille, BandeauPhase.tsx prend le relais sur ce meme declencheur : ces
// tests protegent le garde-fou qui neutralise UNIQUEMENT cette branche-la,
// sans toucher au splash du tour d'un joueur.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { SplashTour } from './SplashTour'
import type { World } from './world'

/** Un monde minimal : seuls round_id et phase comptent pour ces cas. */
const monde = (zones: Record<string, unknown>): World =>
  ({ round_id: 1, players: [], ...zones }) as unknown as World

describe('SplashTour', () => {
  it('sans la prop, la phase du mechant affiche le splash', () => {
    const { container } = render(
      <SplashTour monde={monde({ phase: 'Main Scheme Place Threat' })} />,
    )
    expect(container.querySelector('.splash-tour.est-mechant')).not.toBeNull()
    expect(container.textContent).toContain('Phase du méchant')
  })

  it('avec la prop a vrai, la phase du mechant n affiche rien', () => {
    const { container } = render(
      <SplashTour
        monde={monde({ phase: 'Main Scheme Place Threat' })}
        annonceMechantAilleurs
      />,
    )
    expect(container.querySelector('.splash-tour')).toBeNull()
  })

  it('avec la prop a vrai, un tour de joueur affiche toujours son splash', () => {
    const { container } = render(
      <SplashTour
        monde={monde({
          phase: 'Player 1 Turn',
          players: [{ area_hero: [{ name: 'Spider-Man' }] }],
        })}
        annonceMechantAilleurs
      />,
    )
    expect(container.querySelector('.splash-tour.est-heros')).not.toBeNull()
    expect(container.textContent).toContain('Spider-Man')
  })
})
