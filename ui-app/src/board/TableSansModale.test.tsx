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
import { QuestionSurTable, type ChoixSurTable } from './TableSansModale'

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
