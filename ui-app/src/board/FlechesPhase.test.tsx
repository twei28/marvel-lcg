// La couche des fleches (lot 3) : dessinee seulement avec l'essai, et ses
// bouts poses sur les bords des cartes mesurees.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { render } from '@testing-library/react'
import { DeroulePhase } from './DeroulePhase'
import type { CadreJoueur } from './couleur-joueur'
import type { EtapeDeroule } from './deroule-phase'

const etapes: EtapeDeroule[] = [
  {
    cle: 'b',
    temps: 'mechant',
    titre: 'attaque',
    regle: 'regle:activations',
    carteId: 50,
    cibleId: 12,
    auteurNom: 'Klaw',
    cibleNom: 'Spider-Man',
    etat: 'resolu',
    montant: 2,
    boosts: [],
  },
]
const cadres: CadreJoueur[] = [{ couleurs: ['#e6be3c'], raye: false, siege: 1 }]
const joueurDeCarte = (id: number | undefined) => (id === 12 ? 0 : undefined)

const RECTS: Record<string, DOMRect> = {
  '50': { left: 700, top: 80, width: 100, height: 140, right: 800, bottom: 220, x: 700, y: 80, toJSON() {} } as DOMRect,
  '12': { left: 900, top: 500, width: 100, height: 140, right: 1000, bottom: 640, x: 900, y: 500, toJSON() {} } as DOMRect,
}

let table: HTMLElement
beforeEach(() => {
  table = document.createElement('div')
  table.className = 'plateau-cadre'
  table.innerHTML = '<div class="scan-card" data-card-id="50"></div><div class="scan-card" data-card-id="12"></div>'
  document.body.appendChild(table)
  vi.spyOn(Element.prototype, 'getBoundingClientRect').mockImplementation(function (this: Element) {
    const id = (this as HTMLElement).dataset?.cardId
    const r = id ? RECTS[id] : undefined
    return r ?? ({ left: 0, top: 0, width: 0, height: 0, right: 0, bottom: 0, x: 0, y: 0, toJSON() {} } as DOMRect)
  })
})
afterEach(() => {
  vi.restoreAllMocks()
  table.remove()
})

describe('FlechesPhase dans la phase du mechant (lot 3)', () => {
  it('avec l essai : une fleche de Klaw a Spider-Man, du bord de l un au bord de l autre, couleur du joueur', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} essai cadresJoueurs={cadres} joueurDeCarte={joueurDeCarte} />)
    const fleches = document.querySelectorAll('.fleches-phase .fleche-phase')
    expect(fleches).toHaveLength(1)
    const g = fleches[0] as SVGGElement
    expect(g.style.getPropertyValue('--fleche-couleur')).toBe('#e6be3c')
    const [x1, y1] = (g.dataset.depart ?? '').split(',').map(Number)
    const [x2, y2] = (g.dataset.arrivee ?? '').split(',').map(Number)
    // Depart sur le bord de Klaw, arrivee sur le bord de Spider-Man.
    expect(x1 >= 700 && x1 <= 800 && y1 >= 80 && y1 <= 220).toBe(true)
    expect(x2 >= 900 && x2 <= 1000 && y2 >= 500 && y2 <= 640).toBe(true)
  })

  it('sans l essai : aucune fleche, le rendu actuel est inchange', () => {
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} cadresJoueurs={cadres} joueurDeCarte={joueurDeCarte} />)
    expect(document.querySelector('.fleches-phase')).toBeNull()
  })

  it('une cible face cachee (carte distribuee) n est pas sa place : pas de fleche', () => {
    table.querySelector('[data-card-id="12"]')?.classList.add('is-facedown')
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} essai cadresJoueurs={cadres} joueurDeCarte={joueurDeCarte} />)
    expect(document.querySelector('.fleches-phase')).toBeNull()
  })

  it('une cible absente de la table : pas de fleche vers un point invente', () => {
    table.querySelector('[data-card-id="12"]')?.remove()
    render(<DeroulePhase etapes={etapes} onTerminer={() => {}} essai cadresJoueurs={cadres} joueurDeCarte={joueurDeCarte} />)
    expect(document.querySelector('.fleches-phase')).toBeNull()
  })
})
