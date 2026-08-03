import { describe, expect, it } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import { sections, ZoneFocus } from './ZoneFocus'
import type { BandeAffichee } from './bandes'
import type { ScanCardProps } from '../../components/ScanCard'

function carte(id: number, overrides: Partial<ScanCardProps> = {}): ScanCardProps {
  return { id: String(id), name: `Carte ${id}`, kind: 'ally', imageUrl: '', ...overrides }
}

/**
 * Deux joueurs se partagent terrain-soutien ; les piles et le deck special
 * n'existent que pour le siege regarde, comme les produit zones.ts.
 */
function bandeHeros(): BandeAffichee {
  return {
    cle: 'heros',
    titre: 'Héros',
    emplacements: [
      {
        cle: 'terrain-soutien',
        titre: 'Heros et soutiens',
        nombreSurLaLigne: 4,
        groupes: [
          [
            { cle: 'h0', carte: carte(0, { name: 'Captain Marvel', kind: 'hero' }), attachees: [] },
            { cle: 'a0', carte: carte(10, { name: 'Nick Fury' }), attachees: [] },
          ],
          [
            { cle: 'h1', carte: carte(1, { name: 'Iron Man', kind: 'hero' }), attachees: [] },
            { cle: 'a1', carte: carte(11, { name: 'War Machine' }), attachees: [] },
          ],
        ],
        proprietaires: [0, 1],
      },
      {
        cle: 'piles-joueur',
        titre: 'Piles',
        nombreSurLaLigne: 1,
        groupes: [[{ cle: 'p', carte: carte(20, { name: 'Défausse', pileCount: 3 }), attachees: [] }]],
      },
    ],
  }
}

function bandeVilain(): BandeAffichee {
  return {
    cle: 'vilain',
    titre: 'Méchant',
    emplacements: [
      {
        cle: 'rencontre',
        titre: 'Méchant',
        nombreSurLaLigne: 1,
        groupes: [[{ cle: 'v', carte: carte(30, { name: 'Rhino', kind: 'villain' }), attachees: [] }]],
      },
    ],
  }
}

describe('sections de la feuille de focus', () => {
  it('decoupe la bande Heros par joueur, le siege regarde en premier', () => {
    const resultat = sections(bandeHeros(), 1)
    expect(resultat.map((section) => section.titre)).toEqual(['Iron Man', 'Captain Marvel'])
  })

  it('range les emplacements propres au siege regarde sous SA section', () => {
    const resultat = sections(bandeHeros(), 0)
    const cles = resultat.map((section) => section.unites.map((unite) => unite.cle))
    expect(cles[0]).toEqual(['h0', 'a0', 'p'])
    expect(cles[1]).toEqual(['h1', 'a1'])
  })

  it('etiquette un joueur sans carte d\'identite par son numero', () => {
    const bande = bandeHeros()
    // Le joueur 1 n'a plus que son allie : aucune identite a nommer.
    bande.emplacements[0].groupes[1] = [
      { cle: 'a1', carte: carte(11, { name: 'War Machine' }), attachees: [] },
    ]
    expect(sections(bande, 0)[1].titre).toBe('Joueur 1')
  })

  it('laisse les autres bandes a plat, sans section titree', () => {
    const resultat = sections(bandeVilain(), 0)
    expect(resultat).toHaveLength(1)
    expect(resultat[0].titre).toBeUndefined()
    expect(resultat[0].unites.map((unite) => unite.cle)).toEqual(['v'])
  })
})

describe('ZoneFocus', () => {
  it('montre a qui appartient chaque carte de la bande Heros', () => {
    render(
      <ZoneFocus
        bande={bandeHeros()}
        playerId={0}
        onFermer={() => {}}
        onOuvrirCarte={() => {}}
      />
    )

    const feuille = screen.getByRole('dialog', { name: 'Héros' })
    const titres = within(feuille)
      .getAllByRole('heading', { level: 3 })
      .map((titre) => titre.textContent)
    expect(titres).toEqual(['Captain Marvel', 'Iron Man'])
  })

  it('ne titre rien pour une bande sans proprietaires', () => {
    render(
      <ZoneFocus
        bande={bandeVilain()}
        playerId={0}
        onFermer={() => {}}
        onOuvrirCarte={() => {}}
      />
    )
    expect(screen.queryByRole('heading', { level: 3 })).not.toBeInTheDocument()
  })
})
