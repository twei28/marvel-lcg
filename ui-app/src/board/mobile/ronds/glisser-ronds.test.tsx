// Le glisser au doigt des ronds : un rond se leve des qu'il bouge, une carte de la main seulement vers le haut, le clic
// qui suit un glisser est avale, et les regles sont celles du plateau PC (`glisser.onDepot`).
import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { ReglagesGlisser } from '../../Board'
import { ContexteGlisse, CoucheGlisseRonds, SEUIL_MAIN, SEUIL_ROND, cibleSousLeRond, useGlisserAuDoigt } from './glisser-ronds'

function regles(reste: Partial<ReglagesGlisser> = {}): ReglagesGlisser {
  return {
    estSource: (id) => id === 1 || id === 9,
    ciblesLegales: () => new Set([2]),
    zonesLegales: () => new Set(),
    libelle: () => 'Attaquer · Rhino',
    onDepot: vi.fn(() => undefined),
    ...reste,
  }
}

function Banc({ glisser, surClic }: { glisser: ReglagesGlisser; surClic?: () => void }) {
  const g = useGlisserAuDoigt(glisser)
  return (
    <ContexteGlisse.Provider value={g.valeur}>
      <main data-testid="racine" {...g.gestes}>
        <div className="ronds-zone" data-zone="vilain">
          <div className="rond" data-card-id="2">
            <button type="button">Rhino</button>
          </div>
        </div>
        <div className="rond" data-card-id="1">
          <button
            type="button"
            onClick={() => {
              if (g.clicAvale()) return
              surClic?.()
            }}
          >
            Spider-Man
          </button>
          <span className="rond-art" style={{ backgroundImage: 'url(/x.jpg)' }} />
          <svg className="rond-anneau" data-testid="anneau">
            <circle />
          </svg>
        </div>
        <section className="main-dock">
          <span className="main-portrait-carte">
            <div className="scan-card" data-card-id="9">
              <img src="/main.jpg" alt="" />
            </div>
          </span>
        </section>
        <CoucheGlisseRonds glisse={g.glisse} refus={g.refus} />
      </main>
    </ContexteGlisse.Provider>
  )
}

/** Sous jsdom, `fireEvent.pointerX` perd clientX/clientY (voir glisser/geste.test.tsx) : on emet un MouseEvent du type d'un pointeur. */
const evt = (x: number, y: number) => ({ x, y })
function ptr(cible: Element, type: string, p: { x: number; y: number }) {
  fireEvent(cible, new MouseEvent(type, { bubbles: true, cancelable: true, clientX: p.x, clientY: p.y }))
}
Element.prototype.setPointerCapture = function () {}
Element.prototype.releasePointerCapture = function () {}
afterEach(() => vi.restoreAllMocks())

describe('le glisser au doigt', () => {
  it('un rond se leve au-dela du seuil, et le lacher sur une cible appelle onDepot avec cette cible', () => {
    const g = regles()
    document.elementFromPoint = vi.fn(() => document.querySelector('.ronds-zone .rond button'))
    render(<Banc glisser={g} />)
    const racine = screen.getByTestId('racine')
    const bouton = screen.getByText('Spider-Man')
    ptr(bouton, 'pointerdown', evt(100, 300))
    ptr(racine, 'pointermove', evt(100 + SEUIL_ROND - 2, 300))
    expect(document.querySelector('.glisse-rond-fantome')).toBeNull()
    ptr(racine, 'pointermove', evt(120, 200))
    expect(document.querySelector('.glisse-rond-fantome')).toBeTruthy()
    expect(document.querySelector('.glisse-rond-libelle')?.textContent).toBe('Attaquer · Rhino')
    ptr(racine, 'pointerup', evt(120, 200))
    expect(g.onDepot).toHaveBeenCalledWith(1, expect.objectContaining({ carteId: 2, zone: 'rencontre' }))
    expect(document.querySelector('.glisse-rond-fantome')).toBeNull()
  })

  it('un appui sur l\'anneau SVG du rond le leve aussi (c\'est lui qui est touche)', () => {
    const g = regles()
    document.elementFromPoint = vi.fn(() => null)
    render(<Banc glisser={g} />)
    const racine = screen.getByTestId('racine')
    ptr(screen.getByTestId('anneau').firstElementChild as Element, 'pointerdown', evt(100, 300))
    ptr(racine, 'pointermove', evt(150, 240))
    expect(document.querySelector('.glisse-rond-fantome')).toBeTruthy()
  })

  it('un simple toucher ne glisse rien et le clic passe ; apres un glisser, le clic est avale', () => {
    const g = regles()
    document.elementFromPoint = vi.fn(() => null)
    const clic = vi.fn()
    render(<Banc glisser={g} surClic={clic} />)
    const racine = screen.getByTestId('racine')
    const bouton = screen.getByText('Spider-Man')
    ptr(bouton, 'pointerdown', evt(100, 300))
    ptr(racine, 'pointerup', evt(100, 300))
    fireEvent.click(bouton)
    expect(g.onDepot).not.toHaveBeenCalled()
    expect(clic).toHaveBeenCalledTimes(1)
    ptr(bouton, 'pointerdown', evt(100, 300))
    ptr(racine, 'pointermove', evt(140, 220))
    ptr(racine, 'pointerup', evt(140, 220))
    fireEvent.click(bouton)
    expect(clic).toHaveBeenCalledTimes(1)
  })

  it('un lacher refuse (a vide, mauvaise cible) dit la raison en bulle', () => {
    const g = regles({ onDepot: vi.fn(() => 'Pas ici') })
    document.elementFromPoint = vi.fn(() => null)
    render(<Banc glisser={g} />)
    const racine = screen.getByTestId('racine')
    ptr(screen.getByText('Spider-Man'), 'pointerdown', evt(100, 300))
    ptr(racine, 'pointermove', evt(150, 250))
    ptr(racine, 'pointerup', evt(150, 250))
    expect(screen.getByText('Pas ici')).toBeTruthy()
  })

  it('une carte de la main ne se leve que vers le haut ; de cote, la main defile', () => {
    const g = regles()
    document.elementFromPoint = vi.fn(() => null)
    render(<Banc glisser={g} />)
    const racine = screen.getByTestId('racine')
    const carte = document.querySelector('.main-dock .scan-card') as HTMLElement
    ptr(carte, 'pointerdown', evt(200, 750))
    ptr(racine, 'pointermove', evt(280, 748))
    expect(document.querySelector('.glisse-rond-fantome')).toBeNull()
    ptr(racine, 'pointermove', evt(205, 750 - SEUIL_MAIN - 4))
    expect(document.querySelector('.glisse-rond-fantome')).toBeTruthy()
    ptr(racine, 'pointerup', evt(205, 700))
    expect(g.onDepot).toHaveBeenCalledWith(9, expect.anything())
  })

  it('une carte qui n\'est pas une source ne se leve pas', () => {
    const g = regles({ estSource: () => false })
    render(<Banc glisser={g} />)
    const racine = screen.getByTestId('racine')
    ptr(screen.getByText('Spider-Man'), 'pointerdown', evt(100, 300))
    ptr(racine, 'pointermove', evt(160, 200))
    expect(document.querySelector('.glisse-rond-fantome')).toBeNull()
  })

  it('sans regles du moteur (hors de notre tour, question en cours), rien ne glisse', () => {
    const { container } = render(<Banc glisser={undefined as never} />)
    expect(container.querySelector('.glisse-rond-fantome')).toBeNull()
  })

  it('cibleSousLeRond lit le rond et la zone sous le doigt', () => {
    document.body.innerHTML = '<div class="ronds-zone" data-zone="sbires"><div class="rond" data-card-id="7"><button id="b">x</button></div></div>'
    document.elementFromPoint = vi.fn(() => document.getElementById('b'))
    expect(cibleSousLeRond(10, 10)).toEqual({ carteId: 7, zone: 'terrain-combat' })
    document.elementFromPoint = vi.fn(() => null)
    expect(cibleSousLeRond(10, 10)).toEqual({})
    act(() => {})
  })
})
