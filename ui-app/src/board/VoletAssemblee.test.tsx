// L'onglet « Assemblée » : le code a donner, Longue vie vers son seuil, Le Roi, les groupes, et le verdict qui s'ouvre tout seul une fois.
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { VoletAssemblee } from './VoletAssemblee'
import type { AssembleeExport } from './world'

const assemblee = (plus: Partial<AssembleeExport> = {}): AssembleeExport => ({
  code: 'KING-7F3A', table: 'p1', organisateur: 'p1', total_jetons: 5, seuil: 12, retournee: false, degats: 2, menace: 1, joueurs: 4,
  groupes: [
    { tab: 'p1', joueurs: 2, noms: 'Spider-Man, Hawkeye', etat: 0, recus: 0 },
    { tab: 'p2', joueurs: 2, noms: 'Thor, Storm', etat: 1, recus: 2 },
  ],
  terminee: false, gagnee: false, ...plus,
})

function rendu(a: AssembleeExport, ouvert = true) {
  const ouvrir = vi.fn()
  const fermer = vi.fn()
  const r = render(<VoletAssemblee assemblee={a} ouvert={ouvert} ouvrir={ouvrir} fermer={fermer} />)
  return { ...r, ouvrir, fermer }
}

describe('VoletAssemblee', () => {
  it('ferme : une languette seulement, qui ouvre au clic', () => {
    const { ouvrir } = rendu(assemblee(), false)
    expect(screen.queryByRole('dialog')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: /Ouvrir l’assemblée/ }))
    expect(ouvrir).toHaveBeenCalled()
  })
  it('ouvert : le code, la barre de Longue vie, Le Roi et les deux groupes', () => {
    const { container } = rendu(assemblee())
    expect(screen.getByText('KING-7F3A')).toBeTruthy()
    expect(screen.getByRole('progressbar').getAttribute('aria-valuenow')).toBe('5')
    expect(screen.getByRole('progressbar').getAttribute('aria-valuemax')).toBe('12')
    expect(container.querySelector('.assemblee-roi .est-degats b')?.textContent).toBe('2')
    expect(container.querySelector('.assemblee-roi .est-menace b')?.textContent).toBe('1')
    expect(container.querySelectorAll('.assemblee-groupes li')).toHaveLength(2)
    expect(container.querySelector('.assemblee-groupes li.est-ici')?.textContent).toContain('Spider-Man, Hawkeye')
    expect(container.querySelector('.assemblee-groupe-recus')?.textContent).toBe('+2')
    expect(screen.getByText(/1 groupe|Un groupe joue encore/)).toBeTruthy()
  })
  it('Longue vie retournee : le texte « A bas » remplace le compteur', () => {
    rendu(assemblee({ retournee: true, total_jetons: 12 }))
    expect(screen.getByText(/Retournée/)).toBeTruthy()
  })
  it("pas de verdict tant qu'une table joue ; apres, il s'affiche et l'onglet s'ouvre tout seul UNE fois", () => {
    const { ouvrir, rerender } = rendu(assemblee(), false)
    expect(ouvrir).not.toHaveBeenCalled()
    const fin = assemblee({ terminee: true, gagnee: true, groupes: assemblee().groupes.map((g) => ({ ...g, etat: 1 as const })) })
    rerender(<VoletAssemblee assemblee={fin} ouvert={false} ouvrir={ouvrir} fermer={() => {}} />)
    expect(ouvrir).toHaveBeenCalledTimes(1)
    rerender(<VoletAssemblee assemblee={{ ...fin }} ouvert={false} ouvrir={ouvrir} fermer={() => {}} />)
    expect(ouvrir).toHaveBeenCalledTimes(1)
  })
  it('verdict : « gagne » ou « perd » selon les degats et la menace', () => {
    const { unmount } = rendu(assemblee({ terminee: true, gagnee: true }))
    expect(screen.getByRole('status').textContent).toContain('gagne')
    unmount()
    rendu(assemblee({ terminee: true, gagnee: false }))
    expect(screen.getByRole('status').textContent).toContain('perd')
  })
})
