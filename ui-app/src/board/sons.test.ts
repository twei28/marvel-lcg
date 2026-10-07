// Refonte des sons (décisions du 06 et du 07/10/2026,
// docs/superpowers/specs/2026-09-15-refonte-des-sons-design.md) : volume des
// effets réglable, au plus 2 sons à la fois, survol limité, son de vol, gestes
// du mode manuel sonorisés sans doublon avec le moteur.
import { renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  CLE_SONS,
  CLE_VOLUME_SONS,
  jouerGeste,
  jouerSon,
  jouerSurvol,
  jouerVol,
  lireVolumeSons,
  reinitialiserSons,
  useSons,
} from './sons'
import type { World } from './world'

type Joue = { src: string; volume: number; finir: () => void }

function ecouterLesSons(): Joue[] {
  const joues: Joue[] = []
  vi.stubGlobal(
    'Audio',
    class {
      volume = 1
      currentTime = 0
      paused = true
      ended = false
      error = null
      private ecouteurs: Array<() => void> = []
      constructor(public src: string) {}
      addEventListener(type: string, fn: () => void) {
        if (type === 'ended') this.ecouteurs.push(fn)
      }
      play() {
        this.paused = false
        joues.push({
          src: this.src,
          volume: this.volume,
          finir: () => {
            this.ended = true
            this.paused = true
            this.ecouteurs.forEach((fn) => fn())
          },
        })
        return Promise.resolve()
      }
    }
  )
  return joues
}

const monde = (renderId: number, son: string) => ({ render_id: renderId, sound_name: son }) as unknown as World

beforeEach(() => {
  reinitialiserSons()
  window.localStorage.clear()
  vi.useFakeTimers()
})

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

describe('le volume des effets', () => {
  it('vaut 20 % par défaut, comme avant', () => {
    expect(lireVolumeSons()).toBe(20)
    const joues = ecouterLesSons()
    jouerSon('activate')
    expect(joues[0].volume).toBeCloseTo(0.2)
  })

  it('suit le réglage enregistré', () => {
    window.localStorage.setItem(CLE_VOLUME_SONS, '60')
    const joues = ecouterLesSons()
    jouerSon('activate')
    expect(joues[0].volume).toBeCloseTo(0.6)
  })

  it('un réglage illisible retombe sur 20 %', () => {
    window.localStorage.setItem(CLE_VOLUME_SONS, 'beaucoup')
    expect(lireVolumeSons()).toBe(20)
  })

  it('« Bruitages » coupé : rien ne part', () => {
    window.localStorage.setItem(CLE_SONS, 'off')
    const joues = ecouterLesSons()
    jouerSon('activate')
    jouerSurvol()
    jouerVol()
    jouerGeste(['Puzzle.Flip(3)'])
    expect(joues).toEqual([])
  })
})

describe('au plus deux sons à la fois', () => {
  it('un troisième son pendant que deux jouent est sauté', () => {
    const joues = ecouterLesSons()
    jouerSon('activate')
    jouerSon('damage')
    jouerSon('flip')
    expect(joues.map((j) => j.src)).toEqual(['/activate.wav', '/damage.wav'])
  })

  it('dès qu’un son finit, la place se libère', () => {
    const joues = ecouterLesSons()
    jouerSon('activate')
    jouerSon('damage')
    joues[0].finir()
    jouerSon('flip')
    expect(joues.map((j) => j.src)).toEqual(['/activate.wav', '/damage.wav', '/flip.wav'])
  })
})

describe('le survol', () => {
  it('joue survol.wav très bas', () => {
    window.localStorage.setItem(CLE_VOLUME_SONS, '100')
    const joues = ecouterLesSons()
    jouerSurvol()
    expect(joues[0].src).toBe('/survol.wav')
    expect(joues[0].volume).toBeLessThan(0.5)
  })

  it('pas de rafale quand on balaie : un seul toutes les 80 ms', () => {
    const joues = ecouterLesSons()
    jouerSurvol()
    joues[0].finir()
    vi.advanceTimersByTime(40)
    jouerSurvol()
    expect(joues).toHaveLength(1)
    vi.advanceTimersByTime(50)
    jouerSurvol()
    expect(joues).toHaveLength(2)
  })
})

describe('la carte qui vole', () => {
  it('joue vol.wav', () => {
    const joues = ecouterLesSons()
    jouerVol()
    expect(joues.map((j) => j.src)).toEqual(['/vol.wav'])
  })

  it('se tait sous le voile d’ouverture', () => {
    const joues = ecouterLesSons()
    const { rerender } = renderHook(
      ({ voile }: { voile: boolean }) => useSons(monde(7001, ''), true, false, voile),
      { initialProps: { voile: true } }
    )
    jouerVol()
    expect(joues).toEqual([])
    rerender({ voile: false })
    jouerVol()
    expect(joues.map((j) => j.src)).toEqual(['/vol.wav'])
  })

  it('sonne même pendant une question du moteur (mode manuel, pioche)', () => {
    const joues = ecouterLesSons()
    renderHook(() => useSons(monde(7002, ''), true, true, false))
    jouerVol()
    expect(joues.map((j) => j.src)).toEqual(['/vol.wav'])
  })
})

describe('les gestes du mode manuel', () => {
  it('chaque geste joue le son de sa famille', () => {
    const joues = ecouterLesSons()
    jouerGeste(['Puzzle.Flip(3)'])
    joues[0].finir()
    jouerGeste(['Puzzle.Exhaust(3)'])
    joues[1].finir()
    jouerGeste(["Puzzle.MoveTo(4, 'AlliesArea', 'Top')"])
    joues[2].finir()
    jouerGeste(['Puzzle.Damage(5, 1)'])
    joues[3].finir()
    jouerGeste(["Puzzle.Shuffle('PlayerDeck')"])
    expect(joues.map((j) => j.src)).toEqual(['/flip.wav', '/draw.wav', '/draw.wav', '/damage.wav', '/shuffle.wav'])
  })

  it('les jetons, statuts et menaces jouent le jeton', () => {
    const joues = ecouterLesSons()
    jouerGeste(['Puzzle.Stun(5)'])
    expect(joues.map((j) => j.src)).toEqual(['/token.wav'])
  })

  it('une commande inconnue ne joue rien', () => {
    const joues = ecouterLesSons()
    jouerGeste(['Puzzle.Inconnue(1)'])
    expect(joues).toEqual([])
  })

  it('pas de double son : le moteur qui renvoie la même famille juste après est sauté', () => {
    const joues = ecouterLesSons()
    jouerGeste(['Puzzle.Exhaust(3)'])
    joues[0].finir()
    renderHook(() => useSons(monde(7101, 'carddrop'), true, false))
    expect(joues.map((j) => j.src)).toEqual(['/draw.wav'])
  })

  it('un son du moteur d’une AUTRE famille passe', () => {
    const joues = ecouterLesSons()
    jouerGeste(['Puzzle.Exhaust(3)'])
    joues[0].finir()
    renderHook(() => useSons(monde(7102, 'damage'), true, false))
    expect(joues.map((j) => j.src)).toEqual(['/draw.wav', '/damage.wav'])
  })

  it('la même famille plus tard passe à nouveau', () => {
    const joues = ecouterLesSons()
    jouerGeste(['Puzzle.Exhaust(3)'])
    joues[0].finir()
    vi.advanceTimersByTime(700)
    renderHook(() => useSons(monde(7103, 'carddrop'), true, false))
    expect(joues.map((j) => j.src)).toEqual(['/draw.wav', '/carddrop.wav'])
  })
})

describe('le survol des menus', () => {
  function survoler(el: Element, pointerType: string) {
    const evenement = new MouseEvent('pointerover', { bubbles: true })
    Object.defineProperty(evenement, 'pointerType', { value: pointerType })
    el.dispatchEvent(evenement)
  }

  function bouton(texte: string): HTMLButtonElement {
    const b = document.createElement('button')
    b.textContent = texte
    return b
  }

  it('entrer sur un bouton du menu sonne, entrer sur un enfant du même bouton non', async () => {
    const { installerSurvol } = await import('./sons')
    const joues = ecouterLesSons()
    const menu = document.createElement('div')
    menu.className = 'menu'
    const b = bouton('Reprendre')
    const icone = document.createElement('span')
    b.append(icone)
    menu.append(b)
    document.body.append(menu)
    const retirer = installerSurvol(document, '.menu button')
    survoler(b, 'mouse')
    joues[0]?.finir()
    vi.advanceTimersByTime(200)
    survoler(icone, 'mouse')
    expect(joues.map((j) => j.src)).toEqual(['/survol.wav'])
    retirer()
    menu.remove()
  })

  it('hors du menu, ou au doigt, rien', async () => {
    const { installerSurvol } = await import('./sons')
    const joues = ecouterLesSons()
    const ailleurs = bouton('Fin du tour')
    const menu = document.createElement('div')
    menu.className = 'menu'
    const b = bouton('Reprendre')
    menu.append(b)
    document.body.append(ailleurs, menu)
    const retirer = installerSurvol(document, '.menu button')
    survoler(ailleurs, 'mouse')
    survoler(b, 'touch')
    expect(joues).toEqual([])
    retirer()
    ailleurs.remove()
    menu.remove()
  })
})

describe('les menus du plateau', () => {
  it('le sélecteur vise les boutons de la fenêtre Menu et des Réglages, pas la table', async () => {
    const { SELECTEUR_SURVOL_PLATEAU } = await import('./sons')
    document.body.innerHTML =
      '<div class="reglages-fenetre modale-menu"><button id="reprendre">Reprendre</button></div>' +
      '<div class="board-actions"><button id="fin">Fin du tour</button></div>'
    expect(document.querySelector('#reprendre')?.matches(SELECTEUR_SURVOL_PLATEAU)).toBe(true)
    expect(document.querySelector('#fin')?.matches(SELECTEUR_SURVOL_PLATEAU)).toBe(false)
    document.body.innerHTML = ''
  })
})
