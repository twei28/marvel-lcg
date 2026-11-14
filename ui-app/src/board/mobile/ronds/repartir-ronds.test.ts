// Le regroupement des environnements en ronds (24/10/2026, The Big Apple sur telephone) : la colonne des manigances ne doit plus
// empiler un rond par lieu et par environnement.
import { describe, expect, it } from 'vitest'
import type { ScanCardProps } from '../../../components/ScanCard'
import type { UniteAffichee } from '../../zones'
import { grouperLesEnvironnements } from './repartir-ronds'

const unite = (id: number, nom: string, codeCarte: string, traits: string[] = []): UniteAffichee => ({
  cle: `u${id}`,
  carte: { id: String(id), name: nom, kind: 'environment', imageUrl: `/scan/${codeCarte}.jpg`, codeCarte, traits } as ScanCardProps,
  attachees: [],
})

describe('grouperLesEnvironnements', () => {
  it('deux environnements permanents + un lieu : deux ronds (Environnements ×2, La ville)', () => {
    const sortie = grouperLesEnvironnements([
      unite(1, 'The City', 'pu005'),
      unite(2, 'Never Sleeps', 'pu006'),
      unite(3, 'Midtown', 'pu034', ['LOCATION']),
    ])
    expect(sortie.map((u) => u.groupe?.genre)).toEqual(['environnements', 'ville'])
    expect(sortie[0]!.groupe!.cartes).toHaveLength(2)
    expect(sortie[1]!.groupe!.cartes[0]!.name).toBe('Midtown')
  })
  it('un seul environnement hors ville : le rond reste une carte, sans groupe', () => {
    const sortie = grouperLesEnvironnements([unite(1, 'Weather', '01234')])
    expect(sortie).toHaveLength(1)
    expect(sortie[0]!.groupe).toBeUndefined()
  })
  it('aucun environnement : rien', () => {
    expect(grouperLesEnvironnements([])).toEqual([])
  })
  it('un lieu seul reste un rond « La ville » (le toucher ouvre l\'onglet Ville)', () => {
    const sortie = grouperLesEnvironnements([unite(3, 'Midtown', 'pu034', ['LOCATION'])])
    expect(sortie).toHaveLength(1)
    expect(sortie[0]!.groupe?.genre).toBe('ville')
  })
})
