// Ce qu'un boost ★ met en jeu arrive sur la table au clic (essai, 13/10/2026).
import { render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { EtoilesEnAttente, etoilesDeLEcran } from './EtoilesEnAttente'

const attaque = {
  cle: 'activation:1', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu', carteId: 50, cibleId: 12, montant: 2, restant: 8,
  boosts: [
    { cle: 'b1', nom: 'Trafiquant d’Armes', cibleId: 90, apport: 0, etoile: true },
    { cle: 'b2', nom: 'Sans étoile', cibleId: 91, apport: 1 },
  ],
} as EtapeDeroule
const suivante = { cle: 'activation:2', temps: 'sbires', titre: 'attaque', regle: '', etat: 'annonce', boosts: [] } as unknown as EtapeDeroule

let animations: Array<{ onfinish: (() => void) | null; finish: () => void }>
const place = () => document.querySelector<HTMLElement>('.plateau-cadre .scan-card[data-card-id="90"]')!

beforeEach(() => {
  animations = []
  document.body.innerHTML =
    '<div class="plateau-cadre"><div class="scan-card" data-card-id="90"><img src="/scan/90"></div></div><div class="deroule-phase est-essai"><div class="deroule-corps"></div></div>'
  vi.spyOn(Element.prototype, 'getBoundingClientRect').mockReturnValue({ x: 0, y: 0, left: 0, top: 0, right: 100, bottom: 100, width: 100, height: 100 } as DOMRect)
  Element.prototype.animate = vi.fn(() => {
    const a = { onfinish: null as (() => void) | null, finish: () => a.onfinish?.() }
    animations.push(a)
    return a as unknown as Animation
  })
})
afterEach(() => {
  vi.restoreAllMocks()
  document.body.className = ''
})

describe('les cartes mises en jeu par un boost ★', () => {
  it('seulement les boosts ★ deja retournes d une attaque ou d une manigance resolue', () => {
    expect(etoilesDeLEcran(attaque, 2)).toEqual([90])
    expect(etoilesDeLEcran(attaque, 0)).toEqual([])
    expect(etoilesDeLEcran({ ...attaque, etat: 'annonce' }, 2)).toEqual([])
    expect(etoilesDeLEcran({ ...attaque, titre: 'revelation' }, 2)).toEqual([])
  })

  it('pendant l ecran : sa place reste vide, en pointilles', () => {
    render(<EtoilesEnAttente etape={attaque} boostsMontres={2} actif />)
    expect(place().classList.contains('trajet-arrivee')).toBe(true)
    expect(place().hasAttribute('data-etoile-attente')).toBe(true)
  })

  it('au clic : elle vole de la boite a sa place, puis s y pose', () => {
    const { rerender } = render(<EtoilesEnAttente etape={attaque} boostsMontres={2} actif />)
    rerender(<EtoilesEnAttente etape={suivante} boostsMontres={0} actif />)
    expect(animations).toHaveLength(1)
    expect(place().hasAttribute('data-etoile-attente')).toBe(false)
    expect(place().classList.contains('trajet-arrivee')).toBe(true)
    animations[0].onfinish?.()
    expect(place().classList.contains('trajet-arrivee')).toBe(false)
  })

  it('animations coupees : elle se pose tout de suite au clic', () => {
    document.body.classList.add('plateau-sans-animations')
    const { rerender } = render(<EtoilesEnAttente etape={attaque} boostsMontres={2} actif />)
    rerender(<EtoilesEnAttente etape={suivante} boostsMontres={0} actif />)
    expect(animations).toHaveLength(0)
    expect(place().classList.contains('trajet-arrivee')).toBe(false)
  })
})
