// Panorama des cartes jumelles TMNT (decision du 16/10/2026) : deux cartes a
// illustration continue (Katana de Leonardo, tl011 14/15 + tl012 15/15) se
// posent bord a bord, 14 a gauche, 15 a droite, A COTE de l'identite et non
// glissees dessous. Chaque carte garde son etat et son clic.
import { render, fireEvent } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { Board } from './Board'
import { catalogueVide } from './catalogue'
import { PAIRES_JUMELLES } from './panorama-jumelles'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { EtatInteractif } from './interaction'
import { construirePlateau } from './zones'
import type { WorldCard } from './world'

const IDENTITE = 1
const identite = () => carte(IDENTITE, 'tl001b', 'AlterEgo', 'Leo')
const g = (s: Partial<WorldCard> = {}) =>
  carte(11, 'tl011', 'Upgrade', "Leonardo's Katana", { bind_object_id: IDENTITE, ...s })
const d = (s: Partial<WorldCard> = {}) =>
  carte(12, 'tl012', 'Upgrade', "Leonardo's Other Katana", { bind_object_id: IDENTITE, ...s })
const ordre = (cartes: WorldCard[]) => tableAvec(siege({ area_hero: cartes }))

beforeEach(() => {
  vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
})

function rendre(cartes: WorldCard[], interactifs?: Map<number, EtatInteractif>) {
  const monde = ordre(cartes)
  const plateau = construirePlateau(monde, { playerId: 0, catalogue: catalogueVide })
  return render(<Board world={monde} playerId={0} plateau={plateau} interactifs={interactifs} bandeManigances />)
}

describe('registre des paires', () => {
  it('declare les paires confirmees une a une : Katana de Leonardo, Nunchuck de Michelangelo, Sai de Raphael', () => {
    expect(PAIRES_JUMELLES).toEqual([
      { gauche: 'tl011', droite: 'tl012' },
      { gauche: 'tm011', droite: 'tm012' },
      { gauche: 'tr011', droite: 'tr012' },
    ])
  })
})

describe('plateau : la paire est un bloc 14|15 a cote de l identite', () => {
  it('les deux en jeu : ni sous l identite, ni dans ses attachees', () => {
    const m = ordre([identite(), g(), d()])
    expect(dessinee(m, 11)?.portePar).toBe(0)
    expect(dessinee(m, 12)?.portePar).toBe(0)
    expect(dessinee(m, 11)?.panorama).toBe('gauche')
    expect(dessinee(m, 12)?.panorama).toBe('droite')
  })
  it('meme zone que l identite, rangs consecutifs 14 puis 15', () => {
    const v = cartesDessinees(ordre([identite(), g(), d()]))
    const ids = v.map((c) => c.id)
    expect(dessinee(ordre([identite(), g(), d()]), 11)?.zone).toBe(v.find((c) => c.id === IDENTITE)?.zone)
    expect(ids.indexOf(12)).toBe(ids.indexOf(11) + 1)
  })
  it('ordre inverse a l arrivee : toujours 14 puis 15', () => {
    const v = cartesDessinees(ordre([identite(), d(), g()])).map((c) => c.id)
    expect(v.indexOf(11)).toBeLessThan(v.indexOf(12))
    expect(v.indexOf(12)).toBe(v.indexOf(11) + 1)
  })
  it('une seule en jeu : rendu normal, sous l identite', () => {
    for (const seule of [g(), d()]) {
      const vue = dessinee(ordre([identite(), seule]), seule.id)
      expect(vue?.panorama).toBeUndefined()
      expect(vue?.portePar).toBe(IDENTITE)
    }
  })
  it('carte non declaree : comportement inchange', () => {
    const autre = carte(13, 'tl009', 'Upgrade', 'Autre', { bind_object_id: IDENTITE })
    const vue = dessinee(ordre([identite(), autre]), 13)
    expect(vue?.portePar).toBe(IDENTITE)
    expect(vue?.panorama).toBeUndefined()
  })
})

describe('rendu : bloc, epuisement, clics', () => {
  it('un seul bloc panorama, 14 avant 15, hors de l unite de l identite', () => {
    const { container } = rendre([identite(), d(), g()])
    const blocs = container.querySelectorAll('.panorama-jumelles')
    expect(blocs).toHaveLength(1)
    const ids = [...blocs[0].querySelectorAll('.scan-card')].map((c) => c.getAttribute('data-card-id'))
    expect(ids).toEqual(['11', '12'])
    expect(container.querySelector('.panorama-jumelles .est-attachee')).toBeNull()
    expect(container.querySelector('[data-card-id="1"]')?.closest('.plateau-unite')?.querySelector('[data-card-id="11"]')).toBeNull()
  })
  it('l une epuisee : marqueur sur celle-la seulement, sans rotation', () => {
    const { container } = rendre([identite(), g({ is_ready: false }), d()])
    const c11 = container.querySelector('[data-card-id="11"]')!
    const c12 = container.querySelector('[data-card-id="12"]')!
    expect(c11.querySelector('.panorama-epuise')).not.toBeNull()
    expect(c11.querySelector('.panorama-epuise')?.textContent).toMatch(/épuisée/i)
    expect(c11.classList.contains('est-panorama-epuise')).toBe(true)
    expect(c12.querySelector('.panorama-epuise')).toBeNull()
  })
  it('deux epuisees : deux marqueurs', () => {
    const { container } = rendre([identite(), g({ is_ready: false }), d({ is_ready: false })])
    expect(container.querySelectorAll('.panorama-epuise')).toHaveLength(2)
  })
  it('hors panorama une carte epuisee n a pas de marqueur', () => {
    const { container } = rendre([identite(), g({ is_ready: false })])
    expect(container.querySelectorAll('.panorama-epuise')).toHaveLength(0)
  })
  it('chaque carte reste cliquable separement', () => {
    const clics: number[] = []
    const etat = (id: number): EtatInteractif => ({ role: 'source', choisie: false, agir: () => clics.push(id) }) as EtatInteractif
    const { container } = rendre([identite(), g(), d()], new Map([[11, etat(11)], [12, etat(12)]]))
    fireEvent.click(container.querySelector('[data-card-id="12"]')!)
    fireEvent.click(container.querySelector('[data-card-id="11"]')!)
    expect(clics).toEqual([12, 11])
  })
})
