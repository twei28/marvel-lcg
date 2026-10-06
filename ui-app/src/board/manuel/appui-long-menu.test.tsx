// appui-long-menu.test.tsx — au doigt, tenir une carte ouvre son menu (lot 4,
// question 11 du 06/10/2026). iPad n'envoie aucun `contextmenu` : c'est la
// minuterie de `useTriche` qui le fait. Harnais de clavier-wiring.test.tsx.
import { act, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CoucheTriche, useTriche } from '../CoucheTriche'
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import { APPUI_LONG_MS } from '../mobile/useAppuiLong'
import type { World } from '../world'

const VILAIN = carteSurTable(7, '01001a', 'EncounterVillain', 'Rhino')

function mondeManuel(): World {
  return tableAvec(siege({}), { mode_manuel: true, manuel_actif: true, villains: [VILAIN] } as never)
}

function Harness({ world }: { world: World }) {
  const triche = useTriche(world, 0)
  return <CoucheTriche actif={triche.actif} manuel={triche.manuel} couche={triche.couche} />
}

function pointeur(cible: Element, type: string, pointerType: string, x = 50, y = 60): void {
  const evenement = new MouseEvent(type, { bubbles: true, clientX: x, clientY: y })
  Object.defineProperty(evenement, 'pointerType', { value: pointerType })
  cible.dispatchEvent(evenement)
}

function carte(id: number): HTMLElement {
  const noeud = document.createElement('div')
  noeud.setAttribute('data-card-id', String(id))
  document.body.appendChild(noeud)
  return noeud
}

beforeEach(() => {
  vi.useFakeTimers()
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
})
afterEach(() => {
  vi.useRealTimers()
  document.body.innerHTML = ''
})

describe('appui long au doigt = menu du clic droit', () => {
  it('un doigt tenu sur une carte ouvre son menu', () => {
    render(<Harness world={mondeManuel()} />)
    pointeur(carte(VILAIN.id), 'pointerdown', 'touch')
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS)
    })
    expect(screen.getByText('Incliner')).toBeTruthy()
  })

  it('un doigt tenu dans le vide ouvre le menu de la table', () => {
    render(<Harness world={mondeManuel()} />)
    const vide = document.createElement('div')
    document.body.appendChild(vide)
    pointeur(vide, 'pointerdown', 'touch')
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS)
    })
    expect(screen.getByText('Faire apparaître une carte')).toBeTruthy()
  })

  it('un doigt qui bouge devient un glisser : aucun menu', () => {
    render(<Harness world={mondeManuel()} />)
    const noeud = carte(VILAIN.id)
    pointeur(noeud, 'pointerdown', 'touch', 50, 60)
    pointeur(noeud, 'pointermove', 'touch', 80, 60)
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS * 2)
    })
    expect(screen.queryByText('Incliner')).toBeNull()
  })

  it('un doigt leve avant la duree : aucun menu', () => {
    render(<Harness world={mondeManuel()} />)
    const noeud = carte(VILAIN.id)
    pointeur(noeud, 'pointerdown', 'touch')
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS - 100)
    })
    pointeur(noeud, 'pointerup', 'touch')
    act(() => {
      vi.advanceTimersByTime(500)
    })
    expect(screen.queryByText('Incliner')).toBeNull()
  })

  // Constat du 06/10/2026 (lot 7, navigateur 1024x768 tactile) : au lever du
  // doigt, le navigateur envoie mousedown, mouseup puis click AU POINT DE
  // CONTACT. Le menu venant de s'ouvrir sous le doigt, ce clic tombait sur une
  // de ses entrées (« Défausser », vue `est-danger`) : tenir une carte la
  // défaussait.
  it('lever le doigt apres l appui long ne declenche pas l entree sous le doigt', async () => {
    render(<Harness world={mondeManuel()} />)
    pointeur(carte(VILAIN.id), 'pointerdown', 'touch')
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS)
    })
    const entree = screen.getByText('Incliner')
    vi.mocked(fetch).mockClear()
    pointeur(entree, 'pointerup', 'touch')
    const fin = new Event('touchend', { bubbles: true, cancelable: true })
    entree.dispatchEvent(fin)
    expect(fin.defaultPrevented, 'le lever du doigt doit annuler le clic de compatibilité').toBe(true)
    // Filet si un navigateur l'envoie quand même.
    act(() => {
      entree.click()
    })
    await act(async () => {
      await Promise.resolve()
    })
    expect(fetch).not.toHaveBeenCalled()
    expect(screen.getByText('Incliner')).toBeTruthy()
  })

  it('une vraie tape ensuite sur une entree du menu agit normalement', async () => {
    render(<Harness world={mondeManuel()} />)
    pointeur(carte(VILAIN.id), 'pointerdown', 'touch')
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS)
    })
    const entree = screen.getByText('Incliner')
    pointeur(entree, 'pointerup', 'touch')
    entree.dispatchEvent(new Event('touchend', { bubbles: true, cancelable: true }))
    vi.mocked(fetch).mockClear()
    // Nouvelle tape, courte : doigt posé, levé, clic.
    pointeur(entree, 'pointerdown', 'touch')
    pointeur(entree, 'pointerup', 'touch')
    const fin = new Event('touchend', { bubbles: true, cancelable: true })
    entree.dispatchEvent(fin)
    expect(fin.defaultPrevented).toBe(false)
    await act(async () => {
      entree.click()
      await Promise.resolve()
    })
    expect(fetch).toHaveBeenCalled()
  })

  it('la souris tenue n ouvre rien : elle a son clic droit', () => {
    render(<Harness world={mondeManuel()} />)
    pointeur(carte(VILAIN.id), 'pointerdown', 'mouse')
    act(() => {
      vi.advanceTimersByTime(APPUI_LONG_MS * 2)
    })
    expect(screen.queryByText('Incliner')).toBeNull()
  })
})
