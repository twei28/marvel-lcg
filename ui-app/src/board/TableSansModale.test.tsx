// La main ANCREE pendant qu'une de ses cartes est une option cliquable sur la table (05/11/2026).
//
// Rapport de partie réelle : « quand je survole une carte que je peux jouer, la main monte et
// descend en boucle, même sans bouger la souris ; les cartes que je ne peux pas jouer restent
// bien en haut ». Cause : `PuceSurCarte` re-mesure la carte toutes les 120ms pour coller son
// bouton dessus ; or la main ne reste haute que par `:hover`/`:focus-within` (transition CSS de
// 180ms) — si la carte visée est dans la main, la mesurer pendant qu'elle monte/descend la fait
// chasser une cible mouvante, qui ressort de l'aire de survol dès qu'elle bouge, ce qui referme le
// survol, ce qui la fait redescendre, ce qui la ramène sous la souris : boucle sans fin.
//
// Le correctif pose une classe stable sur `.zone-main` tant que la puce existe, pour que la carte
// ARRÊTE de bouger sous elle (même modèle que `.main-visible-forcee`, voir `main-visible.ts`).
import { cleanup, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CiblageSurTable, QuestionSurTable, type ChoixSurTable, type CibleSurTable } from './TableSansModale'

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})
afterEach(() => {
  cleanup()
  document.body.innerHTML = ''
})

const CARTE_ID = 42

/** Une carte de la main, telle que le plateau la dessine, dans un `.zone-main` réel. */
function poserLaMainAvecLaCarte() {
  const zoneMain = document.createElement('div')
  zoneMain.className = 'plateau-emplacement zone-main'
  const carte = document.createElement('div')
  carte.className = 'scan-card'
  carte.dataset.cardId = String(CARTE_ID)
  zoneMain.appendChild(carte)
  document.body.appendChild(zoneMain)
  return zoneMain
}

function choixJouable(): ChoixSurTable {
  return { id: 1, nom: 'Jouer Tactical Navigation', carteId: CARTE_ID, choisir: vi.fn(), survoler: vi.fn() }
}

describe('la main reste ancrée tant qu’une de ses cartes est une option sur la table', () => {
  it('pose la classe d’ancrage sur .zone-main quand la carte visée y est', () => {
    const zoneMain = poserLaMainAvecLaCarte()
    render(<QuestionSurTable phrase="Klaw va attaquer Silver Surfer" choix={[choixJouable()]} />)
    expect(zoneMain.classList.contains('main-ancree-par-choix')).toBe(true)
  })

  it('retire la classe une fois la question refermée (carte démontée)', () => {
    const zoneMain = poserLaMainAvecLaCarte()
    const { unmount } = render(<QuestionSurTable phrase="Klaw va attaquer Silver Surfer" choix={[choixJouable()]} />)
    expect(zoneMain.classList.contains('main-ancree-par-choix')).toBe(true)
    unmount()
    expect(zoneMain.classList.contains('main-ancree-par-choix')).toBe(false)
  })

  // Témoin : une carte qui n'est PAS dans la main (sur la table, en jeu) ne doit ancrer AUCUNE
  // main — sinon le correctif réintroduirait un effet de bord sur une zone sans rapport.
  it('ne touche à rien quand la carte visée n’est pas dans la main', () => {
    const zoneMain = poserLaMainAvecLaCarte()
    const carteEnJeu = document.createElement('div')
    carteEnJeu.className = 'scan-card'
    carteEnJeu.dataset.cardId = '99'
    document.body.appendChild(carteEnJeu)
    render(<QuestionSurTable phrase="…" choix={[{ ...choixJouable(), carteId: 99 }]} />)
    expect(zoneMain.classList.contains('main-ancree-par-choix')).toBe(false)
  })
})

// Le trait pointillé du bandeau vers chaque carte cliquable (05/11/2026, demande de l'utilisateur).
// Les deux boîtes (bandeau, carte) doivent avoir des rectangles DIFFÉRENTS : `traitEntre` rend
// `undefined` (donc aucun trait) quand les deux se confondent — piège déjà documenté sur
// `trait-phase.ts`.
describe('le trait vers les cartes cliquables depuis le bandeau', () => {
  const rect = (b: { left: number; top: number; width: number; height: number }) =>
    ({ ...b, right: b.left + b.width, bottom: b.top + b.height, x: b.left, y: b.top, toJSON() {} }) as DOMRect

  let cadre: HTMLElement
  /** Où monter le composant : `render(ui, { container: cadre })` reconstruit TOUT `cadre` et
      effacerait la carte posée dessous — on lui donne donc un enfant à part, la carte restant sa
      sœur, toutes deux dans `.plateau-cadre` pour les sélecteurs scopés (`boiteDeLImage` et
      `useBoiteDuBandeau` cherchent dans `cadre.element`, jamais tout le document). */
  let monteIci: HTMLElement
  beforeEach(() => {
    cadre = document.createElement('div')
    cadre.className = 'plateau-cadre'
    document.body.appendChild(cadre)
    cadre.innerHTML = '<div class="scan-card" data-card-id="50"><div class="scan-frame"></div></div>'
    monteIci = document.createElement('div')
    cadre.appendChild(monteIci)
    vi.spyOn(Element.prototype, 'getBoundingClientRect').mockImplementation(function (this: Element) {
      if (this.classList.contains('plateau-cadre')) return rect({ left: 0, top: 0, width: 1000, height: 800 })
      if (this.classList.contains('tsm-bandeau')) return rect({ left: 0, top: 0, width: 300, height: 60 })
      if (this.classList.contains('scan-frame')) return rect({ left: 500, top: 400, width: 100, height: 140 })
      return rect({ left: 0, top: 0, width: 0, height: 0 })
    })
  })
  afterEach(() => {
    vi.restoreAllMocks()
    cadre.remove()
  })

  it('un trait VERT relie le bandeau à une carte jouable (QuestionSurTable)', () => {
    render(<QuestionSurTable phrase="…" choix={[{ ...choixJouable(), carteId: 50 }]} />, { container: monteIci })
    const trait = cadre.querySelector('.tsm-trait')
    expect(trait).toBeTruthy()
    expect(trait?.classList.contains('est-rouge')).toBe(false)
  })

  it('un trait ROUGE relie le bandeau à une cible attaquée (CiblageSurTable, hors défense)', () => {
    const cible: CibleSurTable = { id: 50, choisie: false, agir: vi.fn() }
    render(
      <CiblageSurTable titre="Attaquer" choisies={0} maximum={1} cibles={[cible]} prete={false} raison="" valider={vi.fn()} />,
      { container: monteIci }
    )
    const trait = cadre.querySelector('.tsm-trait')
    expect(trait).toBeTruthy()
    expect(trait?.classList.contains('est-rouge')).toBe(true)
  })

  it('un trait VERT relie le bandeau à un défenseur possible (CiblageSurTable, « Défendre »)', () => {
    const cible: CibleSurTable = { id: 50, choisie: false, agir: vi.fn() }
    render(
      <CiblageSurTable titre="Défendre" choisies={0} maximum={1} cibles={[cible]} prete={false} raison="" valider={vi.fn()} />,
      { container: monteIci }
    )
    const trait = cadre.querySelector('.tsm-trait')
    expect(trait).toBeTruthy()
    expect(trait?.classList.contains('est-rouge')).toBe(false)
  })
})
