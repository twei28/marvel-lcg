import { describe, expect, it } from 'vitest'
import { repartirEnBlocs } from './blocs-portrait'
import type { EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { CleEmplacement } from '../zones'

const unite = (nom: string): UniteAffichee =>
  ({ cle: nom, carte: { id: nom, name: nom, kind: 'minion' }, attachees: [] }) as unknown as UniteAffichee

const emplacement = (cle: CleEmplacement, noms: string[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [noms.map(unite)], nombreSurLaLigne: noms.length }) as EmplacementAffiche

const plateau = (...emplacements: EmplacementAffiche[]): Plateau =>
  ({ emplacements, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

describe('repartirEnBlocs', () => {
  it('range chaque emplacement dans son bloc', () => {
    const blocs = repartirEnBlocs(
      plateau(
        emplacement('terrain-combat', ['Rhino']),
        emplacement('complot-principal', ['L’Effraction']),
        emplacement('piles-rencontre', ['Deck']),
        emplacement('terrain-soutien', ['Steve Rogers']),
        emplacement('main', ['Quinjet']),
      )
    )
    const par = (cle: string) => blocs.find((b) => b.cle === cle)?.unites.map((u) => u.cle)
    expect(par('vilain')).toEqual(['Rhino'])
    expect(par('complot')).toEqual(['L’Effraction'])
    expect(par('rencontre')).toEqual(['Deck'])
    expect(par('heros')).toEqual(['Steve Rogers'])
    expect(par('main')).toEqual(['Quinjet'])
  })

  it('rend TOUJOURS les six blocs, meme vides', () => {
    const blocs = repartirEnBlocs(plateau())
    expect(blocs.map((b) => b.cle)).toEqual(['vilain', 'complot', 'rencontre', 'engages', 'heros', 'main'])
    expect(blocs.every((b) => b.unites.length === 0)).toBe(true)
  })

  it('garde l ordre des emplacements a l interieur d un bloc', () => {
    const blocs = repartirEnBlocs(
      plateau(emplacement('complot-principal', ['Principal']), emplacement('complots-secondaires', ['Annexe']))
    )
    expect(blocs.find((b) => b.cle === 'complot')?.unites.map((u) => u.cle)).toEqual(['Principal', 'Annexe'])
  })
})
