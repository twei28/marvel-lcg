// Mode manuel, glisser SIMPLE (07/10/2026) : lachee dans sa rangee, la carte s'y
// range ; une amelioration lachee pres de son personnage change de rang ou de
// cote ; plus loin, ce n'est pas un rangement (le deplacement ordinaire suit).
import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { useReordonner } from './useReordonner'
import { cleDeCote, cleDePile } from './ordre-cartes'

const rect = (left: number, top: number, width: number, height: number) =>
  ({ left, top, width, height, right: left + width, bottom: top + height, x: left, y: top }) as DOMRect

function table() {
  document.body.innerHTML = `
    <div class="plateau-scene">
      <div class="plateau-groupe" data-rangee="allies">
        <div class="plateau-unite"><div class="scan-card" data-card-id="1"></div></div>
        <div class="plateau-unite"><div class="scan-card" data-card-id="2"></div></div>
        <div class="plateau-unite" id="u3"><div class="scan-card" data-card-id="3"></div>
          <span class="est-attachee"><div class="scan-card" data-card-id="31"></div></span>
          <span class="est-attachee"><div class="scan-card" data-card-id="32"></div></span>
        </div>
      </div>
    </div>`
  const poser = (sel: string, r: DOMRect) => {
    ;(document.querySelector(sel) as HTMLElement).getBoundingClientRect = () => r
  }
  poser('.plateau-groupe', rect(0, 0, 500, 100))
  poser('#u3', rect(200, 0, 300, 100))
  poser('[data-card-id="1"]', rect(0, 0, 100, 100))
  poser('[data-card-id="2"]', rect(100, 0, 100, 100))
  poser('[data-card-id="3"]', rect(200, 0, 100, 100))
  poser('[data-card-id="31"]', rect(300, 0, 100, 100))
  poser('[data-card-id="32"]', rect(400, 0, 100, 100))
}

afterEach(() => {
  document.body.innerHTML = ''
  window.sessionStorage.clear()
})

describe('ranger au glisser simple (mode manuel)', () => {
  it('lachee dans sa rangee, la carte change de place', () => {
    table()
    const { result } = renderHook(() => useReordonner())
    let range = false
    act(() => {
      range = result.current.rangerAuGlisser(1, 190, 50, true)
    })
    expect(range).toBe(true)
    expect(result.current.ordres.allies).toEqual([2, 1, 3])
  })

  it('lachee hors de sa rangee : pas un rangement', () => {
    table()
    const { result } = renderHook(() => useReordonner())
    let range = true
    act(() => {
      range = result.current.rangerAuGlisser(1, 190, 400, true)
    })
    expect(range).toBe(false)
    expect(result.current.ordres).toEqual({})
  })

  it('une amelioration lachee a gauche de son personnage passe a gauche', () => {
    table()
    const { result } = renderHook(() => useReordonner())
    act(() => {
      result.current.rangerAuGlisser(32, 220, 50, true)
    })
    expect(result.current.ordres[cleDeCote(3, 'gauche')]).toEqual([32])
    expect(result.current.ordres[cleDePile(3)]).toBeDefined()
  })

  it('au survol, seul le repere s affiche, rien ne change', () => {
    table()
    const { result } = renderHook(() => useReordonner())
    act(() => {
      result.current.rangerAuGlisser(1, 190, 50, false)
    })
    expect(result.current.geste?.repere).toBeDefined()
    expect(result.current.ordres).toEqual({})
  })
})
