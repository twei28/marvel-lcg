// Apercu au survol des cartes jumelles (decision du 20/10/2026) : quand les DEUX moities d'une paire sont en jeu
// sur la table, l'apercu montre les deux, bord a bord, gauche puis droite. Une seule en jeu, la main : une carte.
import { act, fireEvent, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { Board } from './Board'
import { catalogueVide } from './catalogue'
import { APERCU_JUMELLES_DOUBLE, jumellesPourApercu } from './panorama-jumelles'
import { carteSurTable as carte, siege, tableAvec } from './plateau-de-test'
import { construirePlateau } from './zones'
import type { WorldCard } from './world'

const IDENTITE = 1
const identite = () => carte(IDENTITE, 'tl001b', 'AlterEgo', 'Leo')
const g = () => carte(11, 'tl011', 'Upgrade', "Leonardo's Katana", { bind_object_id: IDENTITE })
const d = () => carte(12, 'tl012', 'Upgrade', "Leonardo's Other Katana", { bind_object_id: IDENTITE })

function plateauDe(cartes: WorldCard[], main: WorldCard[] = []) {
  const monde = tableAvec(siege({ area_hero: cartes, hand_cards: main }))
  return { monde, plateau: construirePlateau(monde, { playerId: 0, catalogue: catalogueVide }) }
}

beforeEach(() => {
  vi.useFakeTimers()
  vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
})
afterEach(() => vi.useRealTimers())

function survoler(cartes: WorldCard[], idSurvole: number, main: WorldCard[] = []) {
  const { monde, plateau } = plateauDe(cartes, main)
  const rendu = render(<Board world={monde} playerId={0} plateau={plateau} bandeManigances />)
  fireEvent.mouseOver(rendu.container.querySelector(`[data-card-id="${idSurvole}"]`)!)
  act(() => {
    vi.advanceTimersByTime(300)
  })
  return document.querySelector('.carte-apercu')
}

describe('choix de l apercu : double ou simple', () => {
  it('le drapeau est actif', () => expect(APERCU_JUMELLES_DOUBLE).toBe(true))

  it('les deux en jeu : la paire, gauche (tl011) puis droite (tl012), quelle que soit la moitie survolee', () => {
    const { plateau } = plateauDe([identite(), d(), g()])
    for (const id of ['11', '12']) {
      const paire = jumellesPourApercu(plateau.emplacements, id)
      expect(paire?.map((j) => [j.carte.id, j.panorama])).toEqual([['11', 'gauche'], ['12', 'droite']])
    }
  })
  it('une seule en jeu : pas de paire', () => {
    for (const seule of [g(), d()]) {
      const { plateau } = plateauDe([identite(), seule])
      expect(jumellesPourApercu(plateau.emplacements, String(seule.id))).toBeUndefined()
    }
  })
  it('depuis la main : pas de paire, meme avec les deux cartes en main', () => {
    const { plateau } = plateauDe([identite()], [g(), d()])
    expect(jumellesPourApercu(plateau.emplacements, '11')).toBeUndefined()
    expect(jumellesPourApercu(plateau.emplacements, '12')).toBeUndefined()
  })
  it('carte non jumelle : pas de paire', () => {
    const { plateau } = plateauDe([identite(), g(), d()])
    expect(jumellesPourApercu(plateau.emplacements, String(IDENTITE))).toBeUndefined()
  })
})

describe('rendu de l apercu au survol', () => {
  it.each([11, 12])('les deux en jeu, survol de %i : deux faces, gauche puis droite, collees', (survole) => {
    const apercu = survoler([identite(), d(), g()], survole)!
    expect(apercu.classList.contains('a-jumelles')).toBe(true)
    const faces = [...apercu.querySelectorAll('.apercu-face .scan-card')]
    expect(faces.map((c) => c.getAttribute('data-card-id'))).toEqual(['11', '12'])
    expect(faces[0].classList.contains('panorama-gauche')).toBe(true)
    expect(faces[1].classList.contains('panorama-droite')).toBe(true)
  })
  it('une seule en jeu : apercu d une carte, inchange', () => {
    const apercu = survoler([identite(), g()], 11)!
    expect(apercu.classList.contains('a-jumelles')).toBe(false)
    expect(apercu.querySelectorAll('.apercu-face')).toHaveLength(1)
    expect(apercu.querySelector('.scan-card.est-panorama')).toBeNull()
  })
  it('survol depuis la main : apercu d une carte', () => {
    const apercu = survoler([identite()], 11, [g(), d()])!
    expect(apercu.classList.contains('a-jumelles')).toBe(false)
    expect(apercu.querySelectorAll('.apercu-face')).toHaveLength(1)
  })
  it('carte non jumelle a cote d une paire : apercu d une carte', () => {
    const apercu = survoler([identite(), d(), g()], IDENTITE)!
    expect(apercu.classList.contains('a-jumelles')).toBe(false)
    expect(apercu.querySelectorAll('.apercu-face')).toHaveLength(1)
  })
})
