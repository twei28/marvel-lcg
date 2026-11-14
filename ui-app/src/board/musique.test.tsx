// Musique : pas de coupure quand le monde change, repli sur le thème générique.
import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CLE_VOLUME_MUSIQUE, ecrireVolumeMusique, lireVolumeMusique, useMusique } from './musique'
import type { World } from './world'

type Faux = { src: string; volume: number; paused: boolean; erreur: () => void }
let crees: Faux[] = []

function monde(nom: string): World {
  return { area_villain: [{ name: nom }] } as unknown as World
}

beforeEach(() => {
  crees = []
  window.localStorage.clear()
  vi.stubGlobal(
    'Audio',
    class {
      volume = 1
      loop = false
      paused = true
      private sur: Array<() => void> = []
      constructor(public src: string) {
        crees.push(this as unknown as Faux)
      }
      addEventListener(type: string, fn: () => void) {
        if (type === 'error') this.sur.push(fn)
      }
      erreur() {
        this.sur.forEach((f) => f())
      }
      play() {
        this.paused = false
        return Promise.resolve()
      }
      pause() {
        this.paused = true
      }
    },
  )
})
afterEach(() => vi.unstubAllGlobals())

describe('useMusique', () => {
  it('un nouveau monde (incliner, redresser...) ne relance ni ne coupe la musique', () => {
    const { rerender } = renderHook(({ w }) => useMusique(w, true), { initialProps: { w: monde('Rhino') } })
    expect(crees).toHaveLength(1)
    rerender({ w: monde('Rhino') })
    rerender({ w: monde('Rhino') })
    expect(crees).toHaveLength(1)
    expect(crees[0].paused).toBe(false)
  })

  it('le thème du méchant manque : repli sur musique-plateau.mp3 même si un monde arrive entre-temps', () => {
    const { rerender } = renderHook(({ w }) => useMusique(w, true), { initialProps: { w: monde('Rhino') } })
    expect(crees[0].src).toBe('/musique-rhino.mp3')
    rerender({ w: monde('Rhino') }) // l'action « incliner » renvoie un monde avant l'erreur
    act(() => crees[0].erreur())
    expect(crees).toHaveLength(2)
    expect(crees[1].src).toBe('/musique-plateau.mp3')
    expect(crees[1].paused).toBe(false)
  })

  it('le volume vaut 25 % par défaut, se règle en direct et se retient', () => {
    expect(lireVolumeMusique()).toBe(25)
    renderHook(() => useMusique(monde('Rhino'), true))
    expect(crees[0].volume).toBeCloseTo(0.25)
    act(() => ecrireVolumeMusique(60))
    expect(window.localStorage.getItem(CLE_VOLUME_MUSIQUE)).toBe('60')
    expect(crees[0].volume).toBeCloseTo(0.6)
    expect(lireVolumeMusique()).toBe(60)
  })
})
