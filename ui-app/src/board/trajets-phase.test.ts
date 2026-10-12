// Les trajets des cartes (refonte, lot 4, essai, 12/10/2026).
import { describe, expect, it } from 'vitest'
import { changementDeTable, pileDeDepart, TROP_DE_CHANGEMENTS, type Releve } from './trajets-phase'

const releve = (...ids: number[]) => new Map<number, Releve>(ids.map((id) => [id, { id, camp: id > 100 ? 'encounter' : 'player' }]))

describe('ce qui arrive sur la table et ce qui en part', () => {
  it('une carte en plus arrive, une carte en moins part', () => {
    const { arrivees, departs } = changementDeTable(releve(1, 2, 150), releve(1, 150, 160))
    expect(arrivees).toEqual([160])
    expect(departs.map((d) => d.id)).toEqual([2])
  })

  it('la table qui se redessine entierement ne fait voler personne', () => {
    const avant = releve(1)
    const apres = releve(...Array.from({ length: TROP_DE_CHANGEMENTS + 1 }, (_, i) => 200 + i))
    expect(changementDeTable(avant, apres)).toEqual({ arrivees: [], departs: [] })
  })

  it('un sbire part vers la defausse rencontre, un allie vers la defausse du joueur', () => {
    expect(pileDeDepart('encounter')).toContain('encounter-discard')
    expect(pileDeDepart('player')).toContain('-defausse')
    expect(pileDeDepart(undefined)).toContain('-defausse')
  })
})
