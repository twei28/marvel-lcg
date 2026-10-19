// LE CARTOUCHE DU BAS HORS DE LA PHASE DU MECHANT, cable dans le plateau
// (lot 5 de la refonte du 04/10/2026, scene PC, mode « Étape par étape ») :
//  - un coup du mechant pendant le tour ouvre « Pendant ton tour » (D26), et
//    plus le cartouche d'un seul coup de la table (`CoupHorsPhase`) ;
//  - « Revoir la phase du méchant » rouvre le cartouche du bas en relecture
//    (D38), plus `RevuePhase` dans le volet ;
//  - la carte revelee en grand (`CoucheRevelation`) se tait : le cartouche
//    s'en charge (D42), sauf la manigance principale de la mise en place.
//
// Monte la vraie page avec un moteur remplace, comme `manuel/plateau-muet`.
import { act, fireEvent, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { MoteurFaux, etatInitial } from './moteur-faux'
import { CLE_MODE_PHASE, type EtatMoteur } from './moteur'
import { catalogueVide } from './catalogue'
import { mondeDeTest } from './manuel/fixture-monde'
import { carteSurTable } from './plateau-de-test'
import type { FaitMechant } from './world'
import type { Demande } from './ask'
import { ecran as screen } from '../test-textes'

vi.mock('./moteur', async (original) => ({
  ...(await original<typeof import('./moteur')>()),
  Moteur: MoteurFaux,
}))

const { PagePartie } = await import('../board')

function monter() {
  return render(<PagePartie playerId={0} catalogue={catalogueVide} modeActions="simple" changerModeActions={() => {}} />)
}

async function emettre(trame: Partial<EtatMoteur>) {
  await act(async () => {
    MoteurFaux.derniere?.emettre({ ...etatInitial(), connecte: true, ...trame })
  })
}

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}

beforeEach(() => {
  MoteurFaux.derniere = undefined
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
  document.body.className = ''
})

/** La phase du mechant du round 2, finie : le joueur est au tour du round 3. */
const PHASE_PRECEDENTE: FaitMechant[] = [
  {
    genre: 'menace',
    round_id: 2,
    phase: 'Main Scheme Place Threat',
    cible: "The Breakin' and Takin'",
    cible_id: 9,
    montant: 1,
    restant: 3,
    plafond: 10,
  },
]

/** Rhino frappe pendant le tour du joueur (une traitrise, un effet). */
const COUP_PENDANT_LE_TOUR: FaitMechant = {
  genre: 'attaque',
  round_id: 3,
  phase: 'Player 1 Turn',
  auteur: 'Rhino',
  auteur_id: 50,
  cible: 'Spider-Man',
  cible_id: 1,
  base: 2,
  boost: 0,
  defense: 0,
  inflige: 2,
  subi: 2,
  restant: 8,
  boosts: [],
}

const auTour = (renderId: number, faits: FaitMechant[], fragment: Parameters<typeof mondeDeTest>[0] = {}) =>
  mondeDeTest({ phase: 'Player Turn', round_id: 3, render_id: renderId, faits_mechant: faits, ...fragment })

describe('le cartouche du bas hors de la phase du mechant, dans le plateau', () => {
  it('un coup du mechant pendant le tour ouvre « Pendant ton tour », jamais le cartouche de la table', async () => {
    const { container } = monter()
    await emettre({ monde: auTour(10, PHASE_PRECEDENTE) })
    expect(container.querySelector('.deroule-phase.est-hors-phase')).toBeNull()
    await emettre({ monde: auTour(11, [...PHASE_PRECEDENTE, COUP_PENDANT_LE_TOUR]) })
    const cartouche = container.querySelector('.deroule-phase.est-scene.est-hors-phase')
    expect(cartouche).not.toBeNull()
    expect(cartouche?.querySelector('.deroule-bandeau')?.textContent).toBe('Pendant ton tour')
    expect(screen.queryByText('Hors de la phase du méchant')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    expect(container.querySelector('.deroule-phase.est-hors-phase')).toBeNull()
  })

  it('« Revoir la phase du méchant » rouvre le cartouche du bas en relecture, plus la revue du volet', async () => {
    const { container } = monter()
    await emettre({ monde: auTour(20, PHASE_PRECEDENTE) })
    fireEvent.click(container.querySelector('.volet-journal-languette') as HTMLElement)
    fireEvent.click(screen.getByRole('button', { name: 'Revoir la phase du méchant' }))
    expect(document.querySelector('.deroule-phase.est-revue')).toBeNull()
    const relecture = document.querySelector('.deroule-phase.est-scene.est-relecture')
    expect(relecture).not.toBeNull()
    expect(relecture?.querySelectorAll('li.deroule-pastille button')).toHaveLength(5)
    fireEvent.click(screen.getByRole('button', { name: 'Fermer' }))
    expect(document.querySelector('.deroule-phase.est-relecture')).toBeNull()
  })

  it('la carte revelee en grand se tait pendant le tour : le cartouche s en charge (D42)', async () => {
    const { container } = monter()
    await emettre({ monde: auTour(30, PHASE_PRECEDENTE) })
    await emettre({
      monde: auTour(31, PHASE_PRECEDENTE, {
        area_revealing: [carteSurTable(77, '01106', 'Treachery', 'Stampede', { is_face_up: true })],
      }),
    })
    expect(container.querySelector('.couche-revelation')).toBeNull()
  })

  it('a la mise en place, la manigance principale garde sa presentation en grand', async () => {
    const { container } = monter()
    await emettre({ monde: auTour(40, [], { round_id: 0, phase: 'Setup' }) })
    await emettre({
      monde: auTour(41, [], {
        round_id: 0,
        phase: 'Setup',
        area_revealing: [carteSurTable(78, '01097a', 'MainScheme', "The Break-In!", { is_face_up: true })],
      }),
    })
    expect(container.querySelector('.couche-revelation')).not.toBeNull()
  })
})

// TEMOINS DU MODE « SUR LA TABLE » (verification du lot 5) : il ne change pas.
// Le coup pendant le tour garde le cartouche d'un seul coup (`CoupHorsPhase`),
// le journal garde sa revue dans le volet (`RevuePhase`), et la carte revelee
// se montre toujours en grand (`CoucheRevelation`). Sans ces cas, rien dans la
// suite ne verrait la table perdre l'un des trois.
describe('en mode « Sur la table », le hors phase ne change pas', () => {
  beforeEach(() => {
    window.localStorage.setItem(CLE_MODE_PHASE, 'sur-table')
  })
  afterEach(() => {
    window.localStorage.removeItem(CLE_MODE_PHASE)
  })

  // T16 (19/10/2026) : « Sur la table », le coup d'un sbire Rapide passe par le bandeau lateral de la
  // table (meme bandeau, meme calcul, meme Continuer que la phase), plus par le cartouche d'un seul coup.
  it('un coup du mechant pendant le tour passe par le bandeau de la table', async () => {
    const { container } = monter()
    await emettre({ monde: auTour(50, PHASE_PRECEDENTE) })
    await emettre({ monde: auTour(51, [...PHASE_PRECEDENTE, COUP_PENDANT_LE_TOUR]) })
    expect(container.querySelector('.tsm-bandeau')).not.toBeNull()
    expect(screen.queryByText('Hors de la phase du méchant')).toBeNull()
    expect(container.querySelector('.deroule-phase.est-hors-phase')).toBeNull()
    expect(container.querySelector('.deroule-phase.est-scene')).toBeNull()
  })

  it('« Revoir la phase du méchant » garde la revue du volet, sans cartouche du bas', async () => {
    const { container } = monter()
    await emettre({ monde: auTour(60, PHASE_PRECEDENTE) })
    fireEvent.click(container.querySelector('.volet-journal-languette') as HTMLElement)
    fireEvent.click(screen.getByRole('button', { name: 'Revoir la phase du méchant' }))
    expect(document.querySelector('.deroule-phase.est-revue')).not.toBeNull()
    expect(document.querySelector('.deroule-phase.est-scene')).toBeNull()
  })

  it('la carte revelee pendant le tour se montre toujours en grand', async () => {
    const { container } = monter()
    await emettre({ monde: auTour(70, PHASE_PRECEDENTE) })
    await emettre({
      monde: auTour(71, PHASE_PRECEDENTE, {
        area_revealing: [carteSurTable(79, '01106', 'Treachery', 'Stampede', { is_face_up: true })],
      }),
    })
    expect(container.querySelector('.couche-revelation')).not.toBeNull()
  })
})

// LES RACCOURCIS DE FIN DE TOUR (verification du lot 5). « Pendant ton tour »
// pose `body.cartouche-scene`, qui cache le bouton « Fin du tour » : Espace
// (et E) ne doivent pas finir le tour qu'on ne voit plus. Pendant toute la
// phase, Espace tournait les pages de ce meme cartouche : le reflexe finissait
// le tour du joueur venu fermer le coup du mechant.
describe('pendant ton tour, les raccourcis de fin de tour se taisent sous le cartouche', () => {
  /** La question libre du tour du joueur : la fin du tour est possible. */
  const tourLibre: Demande = {
    options: [],
    refus: [],
    prompt_text: '',
    event_name: 'WhenPlayerInTurn',
    show_cancel: true,
    ability_type: 'Normal',
  }

  it('temoin : sans cartouche, Espace finit le tour', async () => {
    monter()
    await emettre({ monde: auTour(80, PHASE_PRECEDENTE), aNous: true, demande: tourLibre })
    const avant = MoteurFaux.derniere?.reponses.length ?? 0
    fireEvent.keyDown(document, { key: ' ' })
    expect(MoteurFaux.derniere?.reponses.length).toBe(avant + 1)
  })

  it('« Pendant ton tour » a l ecran : ni Espace ni E ne finissent le tour ; apres « Continuer », Espace le refait', async () => {
    const { container } = monter()
    await emettre({ monde: auTour(90, PHASE_PRECEDENTE), aNous: true, demande: tourLibre })
    await emettre({ monde: auTour(91, [...PHASE_PRECEDENTE, COUP_PENDANT_LE_TOUR]), aNous: true, demande: tourLibre })
    expect(container.querySelector('.deroule-phase.est-scene.est-hors-phase')).not.toBeNull()
    const avant = MoteurFaux.derniere?.reponses.length ?? 0
    fireEvent.keyDown(document, { key: ' ' })
    fireEvent.keyDown(document, { key: 'e' })
    expect(MoteurFaux.derniere?.reponses.length).toBe(avant)
    fireEvent.click(screen.getByRole('button', { name: 'Continuer' }))
    fireEvent.keyDown(document, { key: ' ' })
    expect(MoteurFaux.derniere?.reponses.length).toBe(avant + 1)
  })
})
