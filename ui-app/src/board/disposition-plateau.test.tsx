// Table personnalisable, etape 1 : le plateau PC dessine la grille DEPUIS les
// donnees (disposition.ts), a l'identique de la CSS d'origine.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { render } from '@testing-library/react'
import { Board } from './Board'
import { siege, tableAvec } from './plateau-de-test'
import { construirePlateau } from './zones'
import { EMPLACEMENT_DE_BRIQUE } from './table-rendu'
import { catalogueVide } from './catalogue'
import { DISPOSITION_ORIGINE, aireDeGrille, ancre, changerTaille, type CleBrique } from './table-briques'

const monde = tableAvec(siege({}))
const plateau = construirePlateau(monde, { playerId: 0, catalogue: catalogueVide })

// jsdom n'a pas ResizeObserver (useEchelle) : meme bouchon que Board.test.tsx.
beforeEach(() => {
  vi.stubGlobal('ResizeObserver', class {
    observe() {}
    unobserve() {}
    disconnect() {}
  })
})

describe('la grille du plateau vient de la disposition', () => {
  it('sans disposition choisie : la grille d origine, ecrite depuis les donnees', () => {
    const { container } = render(<Board world={monde} playerId={0} plateau={plateau} bandeManigances />)
    const scene = container.querySelector<HTMLElement>('.plateau-scene')!
    expect(scene.style.gridTemplateAreas.replace(/"/g, "'").replace(/\s+/g, ' ')).toBe(
      aireDeGrille(DISPOSITION_ORIGINE).replace(/\s+/g, ' ')
    )
  })

  it('chaque zone porte la taille de ses cartes', () => {
    // La premiere brique d'une zone que ce plateau dessine vraiment.
    const cle = plateau.emplacements.map((e) => e.cle).find((c) => DISPOSITION_ORIGINE.zones.some((z) => z.briques.some((b) => EMPLACEMENT_DE_BRIQUE[b] === c)))
    expect(cle).toBeDefined()
    const brique = (Object.keys(EMPLACEMENT_DE_BRIQUE) as CleBrique[]).find((b) => EMPLACEMENT_DE_BRIQUE[b] === cle)!
    const d = changerTaille(DISPOSITION_ORIGINE, ancre(DISPOSITION_ORIGINE.zones.find((z) => z.briques.includes(brique))!), 1.3)
    const { container } = render(<Board world={monde} playerId={0} plateau={plateau} bandeManigances disposition={d} />)
    const zone = container.querySelector<HTMLElement>(`.zone-${cle}`)
    expect(zone?.style.getPropertyValue('--taille-zone')).toBe('1.3')
  })
})
