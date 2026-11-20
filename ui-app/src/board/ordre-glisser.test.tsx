// Permuter deux cartes d'une selection ordonnee au glisser-deposer
// (demande de Yarro, 28/09/2026 ; voir ordre-glisser.ts).
import { describe, expect, it, vi } from 'vitest'
import { createEvent, fireEvent, render } from '@testing-library/react'
import { CiblesScene, type CibleScene } from './CiblesScene'
import type { ScanCardProps } from '../components/ScanCard'

const scan = (id: number): ScanCardProps => ({
  id: String(id),
  name: `Sbire ${id}`,
  kind: 'minion',
  imageUrl: `/scan/${id}`,
})

function monter(cibles: CibleScene[]) {
  return render(
    <CiblesScene
      titre="Ordre d'activation"
      cibles={cibles}
      choisies={2}
      minimum={2}
      maximum={2}
      prete
      raison=""
      valider={() => {}}
      annuler={() => {}}
    />
  )
}

/** Un evenement de glisser avec un dataTransfer minimal (jsdom n'en fournit pas). */
function glisser(type: 'dragStart' | 'dragOver' | 'drop', el: Element) {
  const evenement = createEvent[type](el)
  Object.defineProperty(evenement, 'dataTransfer', {
    value: { setData: () => {}, effectAllowed: '', dropEffect: '' },
  })
  fireEvent(el, evenement)
  return evenement
}

describe('glisser une carte choisie sur une autre', () => {
  it('echange les deux cartes : la carte lachee appelle permuterAvec avec la source', () => {
    const permuter1 = vi.fn()
    const permuter2 = vi.fn()
    const { container } = monter([
      { props: scan(1), choisie: true, ordre: 1, permuterAvec: permuter1 },
      { props: scan(2), choisie: true, ordre: 2, permuterAvec: permuter2 },
    ])
    const [premiere, seconde] = [...container.querySelectorAll('.cibles-scene-carte')]
    expect(premiere!.getAttribute('draggable')).toBe('true')

    glisser('dragStart', premiere!)
    expect(premiere!.classList.contains('est-glisse')).toBe(true)
    const survol = glisser('dragOver', seconde!)
    // Le survol est ACCEPTE (sans preventDefault le navigateur refuse le depot).
    expect(survol.defaultPrevented).toBe(true)
    glisser('drop', seconde!)

    expect(permuter2).toHaveBeenCalledExactlyOnceWith(1)
    expect(permuter1).not.toHaveBeenCalled()
    expect(container.querySelector('.est-glisse')).toBeNull()
  })

  it('une carte pas encore choisie ne se glisse pas et ne recoit rien', () => {
    const permuter = vi.fn()
    const { container } = monter([
      { props: scan(1), choisie: true, ordre: 1, permuterAvec: permuter },
      { props: scan(2), choisie: false },
    ])
    const [premiere, seconde] = [...container.querySelectorAll('.cibles-scene-carte')]
    expect(seconde!.getAttribute('draggable')).toBeNull()
    glisser('dragStart', premiere!)
    const survol = glisser('dragOver', seconde!)
    expect(survol.defaultPrevented).toBe(false)
    glisser('drop', seconde!)
    expect(permuter).not.toHaveBeenCalled()
  })

  it('lacher une carte sur elle-meme ne fait rien', () => {
    const permuter = vi.fn()
    const { container } = monter([
      { props: scan(1), choisie: true, ordre: 1, permuterAvec: permuter },
      { props: scan(2), choisie: true, ordre: 2, permuterAvec: () => {} },
    ])
    const premiere = container.querySelector('.cibles-scene-carte')!
    glisser('dragStart', premiere)
    glisser('drop', premiere)
    expect(permuter).not.toHaveBeenCalled()
  })

  it('hors selection ordonnee (aucun permuterAvec), rien ne se glisse', () => {
    const { container } = monter([
      { props: scan(1), choisie: false },
      { props: scan(2), choisie: false },
    ])
    for (const carte of container.querySelectorAll('.cibles-scene-carte')) {
      expect(carte.getAttribute('draggable')).toBeNull()
    }
  })
})
