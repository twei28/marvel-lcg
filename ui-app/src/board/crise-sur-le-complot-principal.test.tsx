// Une manigance annexe à CRISE verrouille la menace du complot principal, et
// le joueur doit le VOIR.
//
// Rapport joueur du 11/09/2026 (« des contres ne retirent pas la menace »),
// journal moteur à l'appui : Pour la Justice visait Hostile Takeover pendant
// que Collapsing Bridge (Crise) était en jeu. Le moteur appliquait la règle,
// la carte partait sans effet, et rien sur la table ne disait pourquoi. Le
// joueur a annulé et rejoué le même coup trois fois.
//
// Le moteur expose `info.crisis` sur la manigance annexe (has_crisis.py) : le
// plateau en tire un bandeau « Crise » sur le complot principal et une phrase
// dans l'aperçu au survol.
import { describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { ScanCard } from '../components/ScanCard'
import { CarteApercu } from './Board'

// jsdom n'implemente pas ResizeObserver, que l'apercu observe pour se placer.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const PRINCIPAL = 48
const PONT = 59
const AUTRE = 60

const monde = (crisis: number | undefined) =>
  tableAvec(siege({ area_hero: [carteSurTable(1, '01001a', 'Hero', 'Spider-Man')] }), {
    area_schemes_main: [carteSurTable(PRINCIPAL, '02004b', 'MainScheme', 'Hostile Takeover')],
    area_schemes_side: [
      carteSurTable(PONT, '02009', 'SideScheme', 'Collapsing Bridge', {
        info: crisis === undefined ? {} : { crisis },
      }),
      carteSurTable(AUTRE, '01166', 'SideScheme', 'Highway Robbery'),
    ],
  })

describe('la Crise sur le complot principal', () => {
  it('nomme la manigance à Crise sur le complot principal', () => {
    expect(dessinee(monde(1), PRINCIPAL)?.crise).toBe('Collapsing Bridge')
  })

  it('ne dit rien quand aucune manigance annexe ne porte de Crise', () => {
    expect(dessinee(monde(undefined), PRINCIPAL)?.crise).toBeUndefined()
    expect(dessinee(monde(0), PRINCIPAL)?.crise).toBeUndefined()
  })

  // Témoin : la Crise ne se pose que sur le complot PRINCIPAL, pas sur les
  // autres manigances annexes.
  it('ne marque pas les autres manigances annexes', () => {
    expect(dessinee(monde(1), AUTRE)?.crise).toBeUndefined()
    expect(dessinee(monde(1), PONT)?.crise).toBeUndefined()
  })

  it('dessine le bandeau « Crise » sur la carte', () => {
    const { container } = render(
      <ScanCard id="48" name="Hostile Takeover" kind="hero" imageUrl="/hostile.jpg" crise="Collapsing Bridge" />
    )
    expect(container.querySelector('.pastille-crise')?.textContent).toBe('Crise')
  })
})

describe('l’aperçu d’une carte en Crise', () => {
  it('pose le picto en filigrane et une ligne sobre, plus de pavé rouge', () => {
    // Retour de l'utilisateur (11/09/2026) : « ce bandeau crise un peu nul ».
    // Le picto du jeu (glyphe C de ChampionsIcons) en filigrane sur
    // l'illustration, et dessous « Crise · <la manigance qui verrouille> ».
    const { container } = render(
      <CarteApercu
        carte={{ id: '48', name: 'Hostile Takeover', kind: 'main-scheme', imageUrl: '/h.jpg', crise: 'Collapsing Bridge' }}
      />
    )
    expect(container.querySelector('.apercu-crise')).toBeNull()
    const filigrane = document.querySelector('.filigrane-crise')
    expect(filigrane).not.toBeNull()
    expect(filigrane).toHaveAttribute('aria-hidden', 'true')
    const ligne = document.querySelector('.apercu-crise-ligne')
    expect(ligne?.textContent).toBe('Crise · Collapsing Bridge')
  })

  it('ne montre rien sur une carte face cachée ni sans crise', () => {
    const { container: sansCrise } = render(
      <CarteApercu carte={{ id: '48', name: 'X', kind: 'main-scheme', imageUrl: '/h.jpg' }} />
    )
    expect(sansCrise.ownerDocument.querySelector('.filigrane-crise')).toBeNull()
    render(
      <CarteApercu
        carte={{ id: '49', name: 'Y', kind: 'main-scheme', imageUrl: '/h.jpg', crise: 'Pont', facedown: true }}
      />
    )
    expect(document.querySelectorAll('.filigrane-crise')).toHaveLength(0)
  })
})
