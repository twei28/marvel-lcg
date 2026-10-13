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
    // Une ligne par famille (retour de Raven, 12/10/2026) : le soutien et
    // l'obligation ont leur ligne, plus celle du heros.
    expect(bandes.heros.unites).toEqual([])
    expect(bandes.soutiens.unites.map((u) => u.cle)).toEqual(['soutien', 'oblig'])
  })

  it('une ligne par famille : heros + allies, soutiens, ameliorations (retour de Raven)', () => {
    const casque = { id: 'casque', name: 'Casque', kind: 'upgrade', imageUrl: '' } as ScanCardProps
    const tenace = { id: 'tenace', name: 'Tenace', kind: 'status', imageUrl: '' } as ScanCardProps
    const bandes = repartirEnBandes(
      plateau(
        emplacement(
          'terrain-soutien',
          unite('carol', { kind: 'hero' }, { attachees: [casque, tenace] }),
          unite('quinjet', { kind: 'support' }),
          unite('lance-toile', { kind: 'upgrade' })
        ),
        emplacement('terrain-combat', unite('wasp', { kind: 'ally' }, { attachees: [{ ...casque, id: 'sur-wasp' }] }), unite('sbire', { kind: 'minion' }))
      )
    )
    expect(bandes.heros.epinglee?.cle).toBe('carol')
    expect(bandes.heros.unites.map((u) => u.cle)).toEqual(['wasp'])
    expect(bandes.soutiens.unites.map((u) => u.cle)).toEqual(['quinjet'])
    // L'amelioration de l'identite quitte sa carte pour la ligne ; son statut reste.
    expect(bandes.ameliorations.unites.map((u) => u.carte.id)).toEqual(['casque', 'lance-toile'])
    expect(bandes.heros.epinglee?.attachees.map((a) => a.id)).toEqual(['tenace'])
    // Celle d'un allie reste sur son porteur.
    expect(bandes.heros.unites[0].attachees.map((a) => a.id)).toEqual(['sur-wasp'])
    expect(bandes.engages.unites.map((u) => u.cle)).toEqual(['sbire'])
  })

  it('range toutes les piles a part, reperees par leur cle, deck special compris', () => {
    const bandes = repartirEnBandes(
      plateau(
        emplacement('piles-joueur', unite('joueur-deck', { name: 'Deck', pileCount: 30 }), unite('joueur-defausse', { name: 'Haymaker' }, { pileContenu: [] })),
        emplacement('piles-rencontre', unite('rencontre-encounter-deck', { pileCount: 20 })),
        // ⚠ Le set nemesis vit dans « annexes » depuis le 14/09/2026 : il n'a
        // plus de zone a lui. Sur telephone, il arrive donc par cet
        // emplacement-la, et doit toujours etre range comme une pile.
        emplacement(
          'annexes',
          unite('annexes-nemesis', { name: 'Vulture' }, { pileContenu: [{ id: 'x' } as ScanCardProps], pileTitre: 'Némésis' }),
          unite('annexes-visibles', { name: 'Victoire' }, { pileContenu: [] })
        ),
        emplacement('deck-special', unite('soutien-deck', { pileCount: 5 }), unite('invocation', { kind: 'support' }))
      )
    )
    expect(bandes.piles.map((p) => p.cle)).toEqual([
      'joueur-deck', 'joueur-defausse', 'rencontre-encounter-deck', 'annexes-nemesis', 'annexes-visibles', 'soutien-deck',
    ])
    expect(bandes.piles[0].compte).toBe(30)
    expect(bandes.piles[3].titre).toBe('Némésis')
    // Le deck special qui n'est pas une pile (l'invocation posee) reste cote
    // joueur, dans la ligne de sa famille (un soutien).
    expect(bandes.soutiens.unites.map((u) => u.cle)).toEqual(['invocation'])
    expect(bandes.soutiens.unites.some((u) => u.cle === 'soutien-deck')).toBe(false)
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
