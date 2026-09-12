import { describe, expect, it } from 'vitest'
import { repartirEnBandes } from './bandes-portrait'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { ScanCardProps } from '../../components/ScanCard'

const unite = (cle: string, carte: Partial<ScanCardProps>, extra: Partial<UniteAffichee> = {}): UniteAffichee =>
  ({ cle, carte: { id: cle, name: cle, kind: 'unknown', imageUrl: '', ...carte }, attachees: [], ...extra }) as UniteAffichee

const emplacement = (cle: CleEmplacement, ...unites: UniteAffichee[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }) as EmplacementAffiche

const plateau = (...emplacements: EmplacementAffiche[]): Plateau =>
  ({ emplacements, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

describe('repartirEnBandes', () => {
  it('epingle le mechant et met l environnement a sa droite, pas chez les engages', () => {
    const bandes = repartirEnBandes(
      plateau(
        emplacement('rencontre', unite('rhino', { kind: 'villain' })),
        emplacement(
          'terrain-combat',
          unite('sbire', { kind: 'minion' }),
          unite('allie', { kind: 'ally' }),
          unite('env', { kind: 'environment' })
        )
      )
    )
    expect(bandes.vilain.epinglee?.cle).toBe('rhino')
    expect(bandes.vilain.unites.map((u) => u.cle)).toEqual(['env'])
    expect(bandes.engages.unites.map((u) => u.cle)).toEqual(['sbire'])
    expect(bandes.heros.unites.map((u) => u.cle)).toEqual(['allie'])
  })

  it('epingle la manigance principale, les annexes defilent a sa droite', () => {
    const bandes = repartirEnBandes(
      plateau(
        emplacement('complot-principal', unite('principale', { kind: 'main-scheme' })),
        emplacement('complots-secondaires', unite('annexe-1', { kind: 'side-scheme' }), unite('annexe-2', { kind: 'side-scheme' }))
      )
    )
    expect(bandes.manigances.epinglee?.cle).toBe('principale')
    expect(bandes.manigances.unites.map((u) => u.cle)).toEqual(['annexe-1', 'annexe-2'])
  })

  it('epingle l identite du heros (heros ou alter ego), le reste du soutien defile', () => {
    const bandes = repartirEnBandes(
      plateau(
        emplacement('terrain-soutien', unite('soutien', { kind: 'support' }), unite('peter', { kind: 'alter-ego' }), unite('oblig', { kind: 'obligation' }))
      )
    )
    expect(bandes.heros.epinglee?.cle).toBe('peter')
    expect(bandes.heros.unites.map((u) => u.cle)).toEqual(['soutien', 'oblig'])
  })

  it('range toutes les piles a part, reperees par leur cle, deck special compris', () => {
    const bandes = repartirEnBandes(
      plateau(
        emplacement('piles-joueur', unite('joueur-deck', { name: 'Deck', pileCount: 30 }), unite('joueur-defausse', { name: 'Haymaker' }, { pileContenu: [] })),
        emplacement('piles-rencontre', unite('rencontre-encounter-deck', { pileCount: 20 })),
        emplacement('nemesis', unite('nemesis-set', { name: 'Vulture' }, { pileContenu: [{ id: 'x' } as ScanCardProps], pileTitre: 'Némésis' })),
        emplacement('annexes', unite('annexes-visibles', { name: 'Victoire' }, { pileContenu: [] })),
        emplacement('deck-special', unite('soutien-deck', { pileCount: 5 }), unite('invocation', { kind: 'support' }))
      )
    )
    expect(bandes.piles.map((p) => p.cle)).toEqual([
      'joueur-deck', 'joueur-defausse', 'rencontre-encounter-deck', 'nemesis-set', 'annexes-visibles', 'soutien-deck',
    ])
    expect(bandes.piles[0].compte).toBe(30)
    expect(bandes.piles[3].titre).toBe('Némésis')
    // Le deck special qui n'est pas une pile (l'invocation posee) reste chez le heros.
    expect(bandes.heros.unites.map((u) => u.cle)).toEqual(['invocation'])
    expect(bandes.heros.unites.some((u) => u.cle === 'soutien-deck')).toBe(false)
  })

  it('rend les quatre bandes et la main meme quand tout est vide', () => {
    const bandes = repartirEnBandes(plateau())
    expect(bandes.vilain.unites).toEqual([])
    expect(bandes.vilain.epinglee).toBeUndefined()
    expect(bandes.manigances.unites).toEqual([])
    expect(bandes.engages.unites).toEqual([])
    expect(bandes.heros.unites).toEqual([])
    expect(bandes.main).toEqual([])
    expect(bandes.piles).toEqual([])
  })
})
