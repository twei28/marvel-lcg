// L'onglet « Ville » : mini-carte dans l'onglet ferme, cases vertes cliquables pour se deplacer, rangee d'un coequipier en lecture seule,
// carte agrandie a gauche du volet. Decisions du 22/10/2026 (.planning/mcdc-punisher/decisions-interface-ville.md).
import { fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { Option } from './ask'
import { catalogueVide } from './catalogue'
import { VoletVille } from './VoletVille'
import type { VilleCase, VilleExport } from './world'

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

const lieu = (ligne: number, colonne: number, joueurs: number[] = [], plus: Partial<VilleCase> = {}): VilleCase => ({
  ligne, colonne, objet: 100 + ligne * 3 + colonne, card_id: `pu0${30 + ligne * 3 + colonne}`, joueurs,
  sbires_attaches: [], limite_utilisee: false, piste: null, ...plus,
})
const ville = (): VilleExport => ({
  lignes: [0, 1, 2].map((l) => ({ ligne: l, capo: 50 + l, capo_card_id: `pu04${8 + l}a` })),
  cases: [0, 1, 2].flatMap((l) =>
    [0, 1, 2].map((c) => lieu(l, c, l === 1 && c === 1 ? [0] : l === 2 && c === 0 ? [1] : [], c === 2 && l === 0 ? { sbires_attaches: [9], limite_utilisee: true } : {}))
  ),
  joueurs: [{ player_id: 0, ligne: 1, colonne: 1 }, { player_id: 1, ligne: 2, colonne: 0 }],
})
const move = (): Option =>
  ({ id: 70, name: 'Move', bind_id: 3, bind_player_id: 0, all_legal_targets: [101, 103, 105, 107], target_num_range: [1, 1], target_payment: {},
     select_rule: '', target_must_include_traits: [], failure_reason: '', is_search: false }) as unknown as Option

function rendu(options: Partial<{ option: Option | undefined; ouvert: boolean }> = {}) {
  const seDeplacer = vi.fn()
  const ouvrir = vi.fn()
  const fermer = vi.fn()
  const r = render(
    <VoletVille
      ville={ville()} moi={0} nomsJoueurs={{ 0: 'Spider-Man', 1: 'Black Panther' }}
      optionDeplacement={'option' in options ? options.option : move()}
      seDeplacer={seDeplacer} catalogue={catalogueVide} ouvert={options.ouvert ?? true} ouvrir={ouvrir} fermer={fermer}
    />
  )
  return { ...r, seDeplacer, ouvrir, fermer }
}

describe('VoletVille', () => {
  it("ferme, l'onglet montre la mini-carte (9 cases) et s'ouvre au clic", () => {
    const { container, ouvrir } = rendu({ ouvert: false })
    expect(container.querySelectorAll('.ville-mini-case')).toHaveLength(9)
    expect(container.querySelectorAll('.ville-mini-case.est-ici')).toHaveLength(1)
    expect(container.querySelectorAll('.ville-mini-case.est-atteignable')).toHaveLength(4)
    fireEvent.click(screen.getByRole('button', { name: /Ouvrir la ville/ }))
    expect(ouvrir).toHaveBeenCalled()
    expect(screen.queryByRole('dialog')).toBeNull()
  })
  it("ouvert, seules les 4 cases cibles legales de « Move » sont vertes et cliquables ; le clic envoie l'objet du lieu", () => {
    const { container, seDeplacer } = rendu()
    expect(container.querySelectorAll('.ville-case')).toHaveLength(9)
    const vertes = container.querySelectorAll('.ville-case.est-atteignable')
    expect(vertes).toHaveLength(4)
    fireEvent.click(vertes[0]!)
    expect(seDeplacer).toHaveBeenCalledTimes(1)
    expect(seDeplacer.mock.calls[0]![1]).toBe(101)
    fireEvent.click(container.querySelector('.ville-case.est-ici')!)
    expect(seDeplacer).toHaveBeenCalledTimes(1)
  })
  it("sans l'option « Move » (hors de son tour), aucune case n'est cliquable et l'aide le dit", () => {
    const { container, seDeplacer } = rendu({ option: undefined })
    expect(container.querySelectorAll('.ville-case.est-atteignable')).toHaveLength(0)
    fireEvent.click(container.querySelectorAll('.ville-case')[0]!)
    expect(seDeplacer).not.toHaveBeenCalled()
    expect(screen.getByText(/Vous pourrez vous déplacer/)).toBeTruthy()
  })
  it("le pion d'un coequipier montre SA rangee en lecture seule ; son propre pion ramene a la sienne", () => {
    const { container, seDeplacer } = rendu()
    expect(container.querySelector('.ville-rangee.est-regardee .ville-pion.est-moi')).not.toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Black Panther' }))
    expect(container.querySelector('.ville-rangee.est-regardee .ville-pion.est-moi')).toBeNull()
    expect(container.querySelectorAll('.ville-case.est-atteignable')).toHaveLength(0)
    fireEvent.click(container.querySelectorAll('.ville-case')[0]!)
    expect(seDeplacer).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'Spider-Man' }))
    expect(container.querySelectorAll('.ville-case.est-atteignable')).toHaveLength(4)
  })
  it('affiche la pastille de sbire attache et la marque « Utilise » sur le lieu concerne', () => {
    const { container } = rendu()
    expect(container.querySelectorAll('.ville-badge.est-sbire')).toHaveLength(1)
    expect(container.querySelectorAll('.ville-badge.est-utilise')).toHaveLength(1)
  })
  it("le survol d'une case montre la carte agrandie dans l'apercu, a gauche du volet", () => {
    const { container } = rendu()
    expect(document.querySelector('.ville-apercu')).toBeNull()
    fireEvent.mouseEnter(container.querySelectorAll('.ville-case')[4]!)
    expect(document.querySelector('.ville-apercu')).not.toBeNull()
    fireEvent.mouseLeave(container.querySelector('.ville-grille')!)
    expect(document.querySelector('.ville-apercu')).toBeNull()
  })
})
