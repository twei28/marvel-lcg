// Le trait qui relie l'attaquant a sa cible : on lit la scene d'un coup d'oeil.
//
// Un SVG pose par-dessus le plateau, en position fixe, recalcule a chaque
// etape depuis la position reelle des deux cartes.
import { afterEach, describe, expect, it } from 'vitest'
import { render } from '@testing-library/react'
import { TraitCible } from './TraitCible'
import type { EtapeDeroule } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'activations',
  titre: 'attaque',
  regle: 'regle:activations',
  boosts: [],
  consequences: [],
  ...extra,
})

function poserCarte(id: number, x: number, y: number): void {
  let scene = document.querySelector('.plateau-scene')
  if (!scene) {
    scene = document.createElement('div')
    scene.className = 'plateau-scene'
    document.body.append(scene)
  }
  const carte = document.createElement('article')
  carte.className = 'scan-card'
  carte.setAttribute('data-card-id', String(id))
  carte.getBoundingClientRect = () =>
    ({ left: x, top: y, width: 100, height: 140, right: x + 100, bottom: y + 140, x, y }) as DOMRect
  scene.append(carte)
}

afterEach(() => {
  document.body.innerHTML = ''
})

describe('trait vers la cible', () => {
  it('trace une ligne entre les deux cartes', () => {
    poserCarte(50, 100, 100)
    poserCarte(12, 500, 400)
    const { container } = render(
      <TraitCible etape={etape({ carteId: 50, cibleId: 12 })} actif />
    )
    expect(container.querySelector('line')).not.toBeNull()
  })

  it('ne trace rien sans cible', () => {
    poserCarte(50, 100, 100)
    const { container } = render(<TraitCible etape={etape({ carteId: 50 })} actif />)
    expect(container.querySelector('line')).toBeNull()
  })

  it('ne trace rien quand une des deux cartes a quitte la table', () => {
    // La cible peut etre morte entre le fait et son affichage.
    poserCarte(50, 100, 100)
    const { container } = render(
      <TraitCible etape={etape({ carteId: 50, cibleId: 999 })} actif />
    )
    expect(container.querySelector('line')).toBeNull()
  })

  it('ne trace rien quand la mise en scene est coupee', () => {
    poserCarte(50, 100, 100)
    poserCarte(12, 500, 400)
    const { container } = render(
      <TraitCible etape={etape({ carteId: 50, cibleId: 12 })} actif={false} />
    )
    expect(container.querySelector('line')).toBeNull()
  })

  it('porte une pointe de fleche sur la cible', () => {
    poserCarte(50, 100, 100)
    poserCarte(12, 500, 400)
    const { container } = render(
      <TraitCible etape={etape({ carteId: 50, cibleId: 12 })} actif />
    )
    expect(container.querySelector('marker')).not.toBeNull()
  })
})
