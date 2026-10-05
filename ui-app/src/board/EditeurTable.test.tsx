// La table personnalisable, etape 2 : L'EDITEUR (decisions du 04/10/2026).
// Zones encadrees, deux poignees chacune (la place, la taille des cartes),
// grille aimantee sans chevauchement, « Terminer » enregistre, « Disposition
// d'origine » remet tout.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render } from '@testing-library/react'
import { EditeurTable, caseSousLePointeur } from './EditeurTable'
import { DISPOSITION_DE_DEPART } from './table-briques'
import { ecran as screen } from '../test-textes'

afterEach(() => window.localStorage.clear())

const boite = { left: 100, top: 50, width: 1200, height: 800 }

describe('la case sous le pointeur (grille aimantee)', () => {
  it('rend la colonne et la ligne, a partir de 1, bornees a la grille', () => {
    expect(caseSousLePointeur(boite, 100, 50, 12, 8)).toEqual({ col: 1, ligne: 1 })
    expect(caseSousLePointeur(boite, 100 + 1199, 50 + 799, 12, 8)).toEqual({ col: 12, ligne: 8 })
    expect(caseSousLePointeur(boite, 100 + 250, 50 + 250, 12, 8)).toEqual({ col: 3, ligne: 3 })
    expect(caseSousLePointeur(boite, -500, 9999, 12, 8)).toEqual({ col: 1, ligne: 8 })
  })
})

describe('l editeur de table', () => {
  const rendre = () => {
    const appels = { changer: vi.fn(), terminer: vi.fn(), origine: vi.fn(), annuler: vi.fn() }
    render(<EditeurTable disposition={DISPOSITION_DE_DEPART} {...appels} />)
    return appels
  }

  it('encadre les neuf zones, main comprise, chacune avec ses deux poignees', () => {
    rendre()
    expect(document.querySelectorAll('.editeur-zone')).toHaveLength(DISPOSITION_DE_DEPART.zones.length)
    expect(screen.getByText('Ta main')).toBeInTheDocument()
    expect(document.querySelectorAll('.editeur-poignee-place')).toHaveLength(DISPOSITION_DE_DEPART.zones.length)
    expect(document.querySelectorAll('.editeur-poignee-taille')).toHaveLength(DISPOSITION_DE_DEPART.zones.length)
  })

  it('pose chaque zone sur sa place de la grille', () => {
    rendre()
    const main = document.querySelector<HTMLElement>('.editeur-zone[data-zone="main"]')!
    expect(main.style.gridColumn).toBe('3 / span 10')
    expect(main.style.gridRow).toBe('7 / span 2')
  })

  it('Terminer, Disposition d origine, Annuler et Echap', () => {
    const appels = rendre()
    fireEvent.click(screen.getByRole('button', { name: 'Terminer' }))
    expect(appels.terminer).toHaveBeenCalledTimes(1)
    fireEvent.click(screen.getByRole('button', { name: 'Disposition d’origine' }))
    expect(appels.origine).toHaveBeenCalledTimes(1)
    fireEvent.click(screen.getByRole('button', { name: 'Annuler' }))
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(appels.annuler).toHaveBeenCalledTimes(2)
  })

  it('la poignee de taille se regle aussi au clavier, bornee', () => {
    const appels = rendre()
    const poignee = document.querySelector<HTMLElement>('.editeur-zone[data-zone="main"] .editeur-poignee-taille')!
    fireEvent.keyDown(poignee, { key: 'ArrowUp' })
    expect(appels.changer.mock.calls[0][0].zones.find((z: { briques: string[] }) => z.briques.includes('main')).taille).toBe(1.05)
  })

  it('une pastille par brique non epinglee, dans la zone qui la porte', () => {
    rendre()
    const pastilles = [...document.querySelectorAll<HTMLElement>('.editeur-brique')].map((b) => b.dataset.brique)
    expect(pastilles.sort()).toEqual(
      ['allies', 'environnements', 'heros', 'manigance-principale', 'manigances-annexes', 'mechant', 'sbires', 'soutiens'].sort()
    )
    expect(document.querySelector('.editeur-zone[data-zone="allies"] [data-brique="sbires"]')).not.toBeNull()
    expect(document.querySelector('.editeur-zone[data-zone="main"] .editeur-brique')).toBeNull()
  })
})
