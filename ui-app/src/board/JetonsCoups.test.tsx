// Les jetons des coups de la phase du mechant (essai, 13/10/2026).
import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { useCoupsEnVol } from './JetonsCoups'

const menace = { cle: 'menace:1', temps: 'menace', titre: 'menace', regle: '', cibleId: 7, montant: 2, restant: 3, boosts: [] } as EtapeDeroule
const attaque = {
  cle: 'mechant:1', temps: 'mechant', titre: 'attaque', regle: '', etat: 'resolu', carteId: 50, cibleId: 12, montant: 3, restant: 7, boosts: [],
} as EtapeDeroule
const fin = { cle: 'bilan', temps: 'bilan', titre: 'bilan', regle: '', boosts: [] } as unknown as EtapeDeroule
const ETAPES = [menace, attaque, fin]

let animations: Array<{ onfinish: (() => void) | null }>

beforeEach(() => {
  animations = []
  document.body.innerHTML =
    '<div class="plateau-cadre"><div class="scan-card" data-card-id="7"></div><div class="scan-card" data-card-id="12"></div><div class="scan-card" data-card-id="50"></div></div><div class="deroule-phase est-essai"><div class="deroule-corps"></div></div>'
  vi.spyOn(Element.prototype, 'getBoundingClientRect').mockReturnValue({ x: 0, y: 0, left: 0, top: 0, right: 100, bottom: 100, width: 100, height: 100 } as DOMRect)
  Element.prototype.animate = vi.fn(() => {
    const a = { onfinish: null as (() => void) | null }
    animations.push(a)
    return a as unknown as Animation
  })
})
afterEach(() => {
  vi.restoreAllMocks()
  document.body.className = ''
})

const rendre = (cle: string, pret = true) =>
  renderHook(({ c, p }) => useCoupsEnVol(ETAPES, c, true, p), { initialProps: { c: cle, p: pret } })
const jetons = () => [...document.querySelectorAll<HTMLElement>('.jeton-coup')]

describe('les jetons des coups', () => {
  it('ecran Menace : la manigance figee a son niveau d avant, un jeton « 2 » attend', () => {
    const { result } = rendre('menace:1')
    expect(result.current).toEqual([{ genre: 'menace', cibleId: 7, valeur: 1 }])
    expect(jetons().map((j) => j.textContent)).toEqual(['2'])
    expect(animations).toHaveLength(0)
  })

  it('au clic sur Continuer : le jeton vole, la carte reste figee jusqu a son arrivee', () => {
    const { result, rerender } = rendre('menace:1')
    rerender({ c: 'mechant:1', p: true })
    // L'ecran de l'attaque fige deja ses PV ; la manigance attend son jeton.
    // 19/10/2026 : les PV ne sont plus figes (le jeton de degats ne vole plus), seule la menace vole.
    expect(result.current).toEqual([{ genre: 'menace', cibleId: 7, valeur: 1 }])
    expect(animations).toHaveLength(1)
    act(() => animations[0].onfinish?.())
    expect(result.current).toEqual([])
  })

  it('attaque : plus de jeton de degats, et les PV ne sont pas figes', () => {
    const { result, rerender } = rendre('mechant:1', false)
    expect(jetons()).toHaveLength(0)
    rerender({ c: 'mechant:1', p: true })
    expect(jetons()).toHaveLength(0)
    expect(result.current).toEqual([])
  })

  it('un nouvel ecran termine les vols d un coup', () => {
    const { result, rerender } = rendre('menace:1')
    rerender({ c: 'mechant:1', p: true })
    rerender({ c: 'bilan', p: true })
    // Le jeton de la menace a disparu ; celui de l'attaque part a son tour.
    expect(result.current).toEqual([])
    expect(jetons()).toHaveLength(0)
  })

  it('animations coupees : pas de jeton, la carte est a jour des le clic', () => {
    document.body.classList.add('plateau-sans-animations')
    const { result, rerender } = rendre('menace:1')
    expect(jetons()).toHaveLength(0)
    rerender({ c: 'bilan', p: true })
    expect(result.current).toEqual([])
  })

  it('le resultat reste le meme tableau d un rendu a l autre', () => {
    const { result, rerender } = rendre('menace:1')
    const premier = result.current
    rerender({ c: 'menace:1', p: true })
    expect(result.current).toBe(premier)
  })
})
