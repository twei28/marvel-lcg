import { describe, expect, it } from 'vitest'
import { EMPLACEMENT_MAIN, RANGEES, estUnePile, mainDe, repartirEnRangees, separerEpingles, unitesDe } from './rangees'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'

function unite(id: string): UniteAffichee {
  return { cle: `u${id}`, carte: { id, name: `Carte ${id}`, kind: 'ally', imageUrl: '' }, attachees: [] }
}

function emplacement(cle: CleEmplacement, unites: UniteAffichee[] = []): EmplacementAffiche {
  return { cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }
}

function plateau(emplacements: EmplacementAffiche[]): Plateau {
  return {
    emplacements,
    nombreDeCartes: 0,
    idsAffiches: new Set<number>(),
    representantsDePile: new Map<number, number>(),
    nombreIgnore: 0,
  }
}

describe('RANGEES', () => {
  it('range les 12 emplacements sans oubli ni doublon, main comprise', () => {
    const toutes: CleEmplacement[] = [
      'piles-rencontre', 'rencontre', 'complot-principal', 'complots-secondaires',
      'terrain-combat', 'terrain-soutien', 'deck-special', 'piles-joueur',
      'nemesis', 'annexes', 'reserve', 'main',
    ]
    const rangees = RANGEES.flatMap((rangee) => [...rangee.defilants, ...rangee.epingles])
    expect([...rangees, EMPLACEMENT_MAIN].sort()).toEqual([...toutes].sort())
  })

  it('lit la rangee ennemie du mechant vers le terrain, piles de rencontre epinglees', () => {
    const ennemie = RANGEES.find((rangee) => rangee.cle === 'ennemie')
    expect(ennemie?.defilants).toEqual(['rencontre', 'complot-principal', 'complots-secondaires', 'terrain-combat'])
    expect(ennemie?.epingles).toEqual(['piles-rencontre'])
  })

  // Demande de l'utilisateur (7/8/2026), toujours valable : la Reserve de Brawn
  // vit avec le heros, a cote du deck special d'un Doctor Strange : c'est sa zone personnelle.
  it('range la Reserve et le deck special avec le heros', () => {
    const heros = RANGEES.find((rangee) => rangee.cle === 'heros')
    expect(heros?.defilants).toEqual(['terrain-soutien', 'deck-special', 'reserve', 'nemesis'])
    expect(heros?.epingles).toEqual(['piles-joueur', 'annexes'])
  })
})

describe('repartirEnRangees', () => {
  it('rend TOUJOURS les deux rangees, meme sans aucun emplacement', () => {
    const rangees = repartirEnRangees(plateau([]))
    expect(rangees.map((rangee) => rangee.cle)).toEqual(['ennemie', 'heros'])
    expect(rangees[0].defilants).toEqual([])
    expect(rangees[0].epingles).toEqual([])
  })

  it('range chaque emplacement present dans sa rangee, defilant ou epingle', () => {
    const rangees = repartirEnRangees(
      plateau([emplacement('piles-joueur'), emplacement('rencontre'), emplacement('terrain-soutien')])
    )
    expect(rangees[0].defilants.map((e) => e.cle)).toEqual(['rencontre'])
    expect(rangees[1].defilants.map((e) => e.cle)).toEqual(['terrain-soutien'])
    expect(rangees[1].epingles.map((e) => e.cle)).toEqual(['piles-joueur'])
  })

  it('garde l\'ordre de lecture, pas celui du plateau', () => {
    const rangees = repartirEnRangees(
      plateau([emplacement('terrain-combat'), emplacement('complot-principal'), emplacement('rencontre')])
    )
    expect(rangees[0].defilants.map((e) => e.cle)).toEqual(['rencontre', 'complot-principal', 'terrain-combat'])
  })
})

describe('unitesDe et mainDe', () => {
  it('aplatit tous les groupes de tous les emplacements', () => {
    const a = emplacement('rencontre', [unite('1')])
    const b: EmplacementAffiche = { cle: 'terrain-combat', titre: 'x', groupes: [[unite('2')], [unite('3')]], nombreSurLaLigne: 2 }
    expect(unitesDe([a, b]).map((u) => u.carte.id)).toEqual(['1', '2', '3'])
  })

  it('mainDe rend les cartes de la main, ou rien si elle est absente', () => {
    expect(mainDe(plateau([]))).toEqual([])
    const main = mainDe(plateau([emplacement('main', [unite('7')])]))
    expect(main.map((u) => u.carte.id)).toEqual(['7'])
  })
})

// `annexes` (zones.ts) melange des piles fondues et des cartes posees isolees
// (preuves, regle, ressources) : seules les premieres doivent etre epinglees.
describe('estUnePile et separerEpingles', () => {
  it('une unite avec pileCount, pileContenu ou pileGroupes est une pile ; une carte simple ne l\'est pas', () => {
    const parPileCount: UniteAffichee = { ...unite('1'), carte: { ...unite('1').carte, pileCount: 3 } }
    const parPileContenu: UniteAffichee = { ...unite('2'), pileContenu: [] }
    const parPileGroupes: UniteAffichee = { ...unite('3'), pileGroupes: [] }
    expect(estUnePile(parPileCount)).toBe(true)
    expect(estUnePile(parPileContenu)).toBe(true)
    expect(estUnePile(parPileGroupes)).toBe(true)
    expect(estUnePile(unite('4'))).toBe(false)
  })

  it('separerEpingles garde l\'ordre de lecture dans chaque groupe', () => {
    const a = unite('1')
    const pileB: UniteAffichee = { ...unite('2'), pileContenu: [] }
    const c = unite('3')
    const pileD: UniteAffichee = { ...unite('4'), pileGroupes: [] }
    const { piles, posees } = separerEpingles([a, pileB, c, pileD])
    expect(piles.map((u) => u.carte.id)).toEqual(['2', '4'])
    expect(posees.map((u) => u.carte.id)).toEqual(['1', '3'])
  })
})
