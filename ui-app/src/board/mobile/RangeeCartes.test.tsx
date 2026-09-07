import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { RangeeCartes, type GroupeRangee } from './RangeeCartes'
import type { UniteAffichee } from '../zones'

const unite = (id: string, name: string, state?: 'targetable' | 'disabled'): UniteAffichee => ({
  cle: `u${id}`,
  carte: { id, name, kind: 'ally', imageUrl: '', state },
  attachees: [],
})

function rendre(groupes: GroupeRangee[], extra: Partial<Parameters<typeof RangeeCartes>[0]> = {}) {
  return render(
    <RangeeCartes
      cle="heros"
      titre="Ton héros"
      groupes={groupes}
      piles={[]}
      onOuvrirCarte={() => {}}
      onOuvrirPile={() => {}}
      {...extra}
    />
  )
}

describe('RangeeCartes', () => {
  it('porte son etiquette et ses cartes dans l\'ordre', () => {
    rendre([{ cle: 'g', unites: [unite('1', 'Spider-Man'), unite('2', 'Black Cat')] }])
    expect(screen.getByRole('region', { name: 'Ton héros' })).toBeInTheDocument()
    const noms = [...document.querySelectorAll('.carte-posee')].map((c) => c.getAttribute('aria-label'))
    expect(noms).toEqual(['Spider-Man', 'Black Cat'])
  })

  it('dit « Vide » quand aucune carte, sans perdre son etiquette', () => {
    rendre([{ cle: 'g', unites: [] }])
    expect(screen.getByText('Vide')).toBeInTheDocument()
    expect(screen.getByText('Ton héros')).toBeInTheDocument()
  })

  it('separe deux groupes (deux heros) par un trait, et marque le groupe actif', () => {
    rendre([
      { cle: 'j0', unites: [unite('1', 'Spider-Man')], actif: true },
      { cle: 'j1', unites: [unite('2', 'Black Cat')] },
    ])
    expect(screen.getAllByRole('separator')).toHaveLength(1)
    const groupes = document.querySelectorAll('.rangee-cartes-groupe')
    expect(groupes[0]).toHaveClass('est-actif')
    expect(groupes[1]).not.toHaveClass('est-actif')
  })

  it('compte les cibles legales sur son etiquette', () => {
    rendre([{ cle: 'g', unites: [unite('1', 'A', 'targetable'), unite('2', 'B', 'disabled')] }], { cibles: 1 })
    expect(document.querySelector('.rangee-cartes-cibles')).toHaveTextContent('1')
  })

  it('ramene la premiere cible dans le champ quand un ciblage commence', () => {
    // Rien n'est ciblable au depart : le ciblage n'a pas encore commence.
    const { rerender } = rendre([{ cle: 'g', unites: [unite('1', 'A'), unite('2', 'B')] }])
    const recentrer = vi.fn()
    // jsdom n'implemente pas scrollIntoView ; on verifie l'APPEL, pas le defilement.
    Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', { value: recentrer, configurable: true })
    rerender(
      <RangeeCartes
        cle="heros"
        titre="Ton héros"
        groupes={[{ cle: 'g', unites: [unite('1', 'A'), unite('2', 'B', 'targetable')] }]}
        piles={[]}
        cibles={1}
        onOuvrirCarte={() => {}}
        onOuvrirPile={() => {}}
      />
    )
    const cible = document.querySelector('.state-targetable')?.closest('.carte-posee')
    expect(recentrer).toHaveBeenCalled()
    expect(cible).not.toBeNull()
  })

  it('affiche le voile +N et avance d\'un ecran au tap', () => {
    rendre([{ cle: 'g', unites: Array.from({ length: 6 }, (_, i) => unite(String(i), `C${i}`)) }])
    const defilement = document.querySelector<HTMLElement>('.rangee-cartes-defilement')!
    // jsdom ne mesure rien : on pose des mesures a la main, comme un vrai rendu.
    Object.defineProperty(defilement, 'clientWidth', { value: 400, configurable: true })
    ;[...defilement.querySelectorAll<HTMLElement>('.carte-posee')].forEach((carte, i) => {
      Object.defineProperty(carte, 'offsetLeft', { value: i * 108, configurable: true })
      Object.defineProperty(carte, 'offsetWidth', { value: 100, configurable: true })
    })
    fireEvent.scroll(defilement)
    const voile = screen.getByRole('button', { name: /cartes hors champ/ })
    expect(voile).toHaveClass('rangee-cartes-suite')
    // 6 cartes de 100 px au pas de 108 px, fenetre de 400 px : bords droits a
    // 100, 208, 316, 424, 532, 640. La 4e depasse de 24 px (moins de la
    // moitie, cf. hors-champ.test.ts) : elle reste visible. Seules les
    // cartes 5 et 6 depassent de plus de la moitie (132 et 240 px) : 2
    // cartes hors champ, pas 3 (verifie par le calcul et par le test).
    expect(voile).toHaveTextContent('+2')
    const scrollBy = vi.fn()
    defilement.scrollBy = scrollBy
    fireEvent.click(voile)
    expect(scrollBy).toHaveBeenCalledWith({ left: 400, behavior: 'smooth' })
  })

  it('se recale sur la nouvelle cible meme quand le compte de cibles ne change pas', () => {
    const recentrer = vi.fn()
    Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', { value: recentrer, configurable: true })
    const { rerender } = rendre(
      [{ cle: 'g', unites: [unite('1', 'A'), unite('2', 'B', 'targetable')] }],
      { cibles: 1 }
    )
    expect(recentrer).toHaveBeenCalledTimes(1)
    rerender(
      <RangeeCartes
        cle="heros"
        titre="Ton héros"
        groupes={[{ cle: 'g', unites: [unite('1', 'A', 'targetable'), unite('2', 'B')] }]}
        piles={[]}
        cibles={1}
        onOuvrirCarte={() => {}}
        onOuvrirPile={() => {}}
      />
    )
    expect(recentrer).toHaveBeenCalledTimes(2)
  })
})
