// Boosts et traîtrises vers la défausse rencontre au clic (essai, 13/10/2026).
import { cleanup, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { cartesQuiPartent, DepartsDeLaBoite } from './DepartsDeLaBoite'

const attaque = {
  cle: 'a1', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu', carteId: 50, cibleId: 12,
  boosts: [
    { cle: 'b1', nom: 'Assaut', cibleId: 90, apport: 2 },
    { cle: 'b2', nom: 'Raté', cibleId: 91, apport: 0 },
  ],
} as EtapeDeroule
const traitrise = { cle: 'r1', temps: 'revelation', titre: 'revelation', regle: '', carteId: 70, typeCarte: 'Treachery', boosts: [] } as EtapeDeroule
const suite = { cle: 'b', temps: 'bilan', titre: 'bilan', regle: '', boosts: [] } as unknown as EtapeDeroule

describe('les cartes de la boîte qui partent à la défausse', () => {
  it('les boosts retournés d’une attaque ou d’une manigance', () => {
    expect(cartesQuiPartent(attaque, 2)).toEqual([90, 91])
    expect(cartesQuiPartent(attaque, 1)).toEqual([90])
    expect(cartesQuiPartent({ ...attaque, etat: 'annonce' }, 2)).toEqual([])
  })
  it('une traîtrise révélée, pas un sbire', () => {
    expect(cartesQuiPartent(traitrise, 0)).toEqual([70])
    expect(cartesQuiPartent({ ...traitrise, typeCarte: 'Minion' }, 0)).toEqual([])
  })
})

describe('le vol au clic', () => {
  let animations: Array<{ onfinish: (() => void) | null; finish: () => void }>
  beforeEach(() => {
    animations = []
    document.body.innerHTML =
      '<div class="plateau-cadre"><div data-pile="rencontre-encounter-discard"></div></div>' +
      '<section class="deroule-phase est-essai"><div class="deroule-corps"><span data-card-id="90"><img src="/90"></span><span data-card-id="91"></span></div></section>'
    vi.spyOn(Element.prototype, 'getBoundingClientRect').mockReturnValue({ x: 0, y: 0, left: 0, top: 0, right: 50, bottom: 70, width: 50, height: 70 } as DOMRect)
    Element.prototype.animate = vi.fn(() => {
      const a = { onfinish: null as (() => void) | null, finish: () => a.onfinish?.() }
      animations.push(a)
      return a as unknown as Animation
    })
  })
  afterEach(() => {
    cleanup()
    vi.restoreAllMocks()
    document.body.className = ''
  })

  it('au changement d’écran, chaque boost part vers la défausse rencontre', () => {
    const { rerender } = render(<DepartsDeLaBoite etape={attaque} boostsMontres={2} actif />)
    expect(animations).toHaveLength(0)
    rerender(<DepartsDeLaBoite etape={suite} boostsMontres={0} actif />)
    expect(animations).toHaveLength(2)
    expect(document.querySelectorAll('.trajet-copie')).toHaveLength(2)
    animations.forEach((a) => a.onfinish?.())
    expect(document.querySelectorAll('.trajet-copie')).toHaveLength(0)
  })

  it('animations coupées : rien ne vole', () => {
    document.body.classList.add('plateau-sans-animations')
    const { rerender } = render(<DepartsDeLaBoite etape={attaque} boostsMontres={2} actif />)
    rerender(<DepartsDeLaBoite etape={suite} boostsMontres={0} actif />)
    expect(animations).toHaveLength(0)
  })
})
