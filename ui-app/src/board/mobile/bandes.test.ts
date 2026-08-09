import { describe, expect, it } from 'vitest'
import { BANDES, repartir } from './bandes'
import type { CleEmplacement, EmplacementAffiche, Plateau } from '../zones'

function emplacement(cle: CleEmplacement): EmplacementAffiche {
  return { cle, titre: cle, groupes: [[]], nombreSurLaLigne: 0 }
}

function plateau(cles: CleEmplacement[]): Plateau {
  return {
    emplacements: cles.map(emplacement),
    nombreDeCartes: 0,
    idsAffiches: new Set<number>(),
    representantsDePile: new Map<number, number>(),
    nombreIgnore: 0,
  }
}

describe('BANDES', () => {
  it('range les 12 emplacements sans oubli ni doublon', () => {
    const toutes: CleEmplacement[] = [
      'piles-rencontre', 'rencontre', 'complot-principal', 'complots-secondaires',
      'terrain-combat', 'terrain-soutien', 'deck-special', 'piles-joueur',
      'nemesis', 'annexes', 'reserve', 'main',
    ]
    const rangees = BANDES.flatMap((bande) => bande.emplacements)
    expect([...rangees].sort()).toEqual([...toutes].sort())
  })

  // Demande de l'utilisateur (7/8/2026) : la Réserve de Brawn doit vivre au
  // MÊME endroit que le deck spécial d'un Doctor Strange, c'est-à-dire dans la
  // bande du héros — et surtout pas avec la main, où elle était au départ.
  it('range la Réserve avec le héros, à côté du deck spécial', () => {
    const bandeHeros = BANDES.find((bande) => bande.cle === 'heros')
    expect(bandeHeros?.emplacements).toContain('reserve')
    expect(bandeHeros?.emplacements).toContain('deck-special')

    const bandeMain = BANDES.find((bande) => bande.cle === 'main')
    expect(bandeMain?.emplacements).not.toContain('reserve')
  })
})

describe('repartir', () => {
  it('ne rend pas une bande dont aucun emplacement n\'est present', () => {
    const bandes = repartir(plateau(['rencontre']))
    expect(bandes.map((bande) => bande.cle)).toEqual(['vilain'])
  })

  it('regroupe les emplacements d\'une meme bande', () => {
    const bandes = repartir(plateau(['complot-principal', 'complots-secondaires']))
    expect(bandes).toHaveLength(1)
    expect(bandes[0].cle).toBe('complots')
    expect(bandes[0].emplacements).toHaveLength(2)
  })

  it('rend les bandes dans l\'ordre de lecture, pas dans celui du plateau', () => {
    const bandes = repartir(plateau(['main', 'rencontre', 'complot-principal']))
    expect(bandes.map((bande) => bande.cle)).toEqual(['vilain', 'complots', 'main'])
  })
})
