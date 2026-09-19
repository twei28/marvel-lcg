// Le plateau manuel ne montre RIEN de ce que le moteur disait.
//
// On vise les classes CSS plutot que les composants : c'est ce que le joueur
// voit, et ca ne bouge pas quand un composant est renomme.
//
// ⚠ CORRECTION AU BRIEF (voir task-2-report.md). Le brief visait un attribut
// `data-pile` qui n'existe pas encore : il n'arrive qu'a la tache 5. On vise
// ici ce qui marque REELLEMENT la main aujourd'hui : `data-zone="main"`
// (Board.tsx, `Emplacement`) et la classe `main-visible-forcee` qui decide si
// elle se montre sans avoir besoin d'un survol (board.css).
//
// Le montage est calque sur `PagePartie.test.tsx`, qui monte deja cette page
// avec un moteur remplace (`MoteurFaux`) : on ne reecrit pas un second
// montage a cote.
import { act, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { MoteurFaux, etatInitial } from '../moteur-faux'
import type { EtatMoteur } from '../moteur'
import { catalogueVide } from '../catalogue'
import { mondeDeTest } from './fixture-monde'

vi.mock('../moteur', async (original) => ({
  ...(await original<typeof import('../moteur')>()),
  Moteur: MoteurFaux,
}))

const { PagePartie } = await import('../../board')

function monter() {
  return render(
    <PagePartie
      playerId={0}
      catalogue={catalogueVide}
      modeActions="simple"
      changerModeActions={() => {}}
    />
  )
}

/** Emet une trame vers l'ecran monte, sur l'etat d'ouverture par defaut. */
async function emettre(trame: Partial<EtatMoteur>) {
  await act(async () => {
    MoteurFaux.derniere?.emettre({ ...etatInitial(), connecte: true, ...trame })
  })
}

// jsdom n'implemente pas ResizeObserver : le plateau observe son cadre pour
// calculer l'echelle. Meme bouchon que PagePartie.test.tsx.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}

beforeEach(() => {
  MoteurFaux.derniere = undefined
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

describe('le plateau manuel se tait', () => {
  it('ne montre pas le bandeau de phase', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: true }) })
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('ne montre pas le deroule de phase', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: true }) })
    expect(container.querySelector('.deroule-phase')).toBeNull()
  })

  it('montre encore ces reperes en partie ordinaire', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({}) })
    expect(container.querySelector('.bandeau-phase')).not.toBeNull()
    expect(container.querySelector('.deroule-phase')).not.toBeNull()
  })
})

// LA MAIN DE CHAQUE HEROS (etape 5 du brief). Le plateau ne dessine
// aujourd'hui QUE la main du joueur regarde (zones.ts, `notre?.hand_cards`) :
// il n'y a pas plusieurs zones « main » a compter, une seule, cachee derriere
// un survol (board.css, `.zone-main:hover`). En manuel, un seul operateur
// manipule tous les heros : cette main doit rester visible SANS survol.
describe('le plateau manuel montre la main sans avoir besoin d\'un survol', () => {
  it('force la main visible', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: true }) })
    expect(container.querySelectorAll('[data-zone="main"]').length).toBeGreaterThan(0)
    expect(container.querySelector('.plateau.main-visible-forcee')).not.toBeNull()
  })

  it('ne la force pas en partie ordinaire, hors interaction', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({}) })
    expect(container.querySelectorAll('[data-zone="main"]').length).toBeGreaterThan(0)
    expect(container.querySelector('.plateau.main-visible-forcee')).toBeNull()
  })
})
