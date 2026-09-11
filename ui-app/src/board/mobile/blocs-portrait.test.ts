import { describe, expect, it } from 'vitest'
import { repartirEnBlocs } from './blocs-portrait'
import type { CardKind } from '../../components/ScanCard'
import type { EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { CleEmplacement } from '../zones'

const unite = (nom: string, kind: CardKind = 'minion'): UniteAffichee =>
  ({ cle: nom, carte: { id: nom, name: nom, kind }, attachees: [] }) as unknown as UniteAffichee

const emplacement = (cle: CleEmplacement, unites: UniteAffichee[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }) as EmplacementAffiche

const noms = (cle: CleEmplacement, ...noms: string[]) => emplacement(cle, noms.map((nom) => unite(nom)))

const plateau = (...emplacements: EmplacementAffiche[]): Plateau =>
  ({ emplacements, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

describe('repartirEnBlocs', () => {
  // Regression du defaut majeur du 11/09/2026 : le mechant, pose par zones.ts
  // dans l'emplacement `rencontre` (voir `airesVilains`), doit atterrir dans
  // le bloc `vilain` — pas dans le bloc `rencontre` (ou il etait ignore, seuls
  // les deux compteurs de pile en etant lus) ni nulle part ailleurs.
  it('un mechant pose dans `rencontre` (la vraie zone du vilain) atterrit dans le bloc `vilain`', () => {
    const blocs = repartirEnBlocs(
      plateau(noms('rencontre', 'Rhino'), noms('piles-rencontre', 'Deck Rencontre'))
    )
    const par = (cle: string) => blocs.find((b) => b.cle === cle)?.unites.map((u) => u.cle)
    expect(par('vilain')).toEqual(['Rhino'])
    // Et le bloc `rencontre` (compteurs de deck/defausse) ne recoit QUE
    // piles-rencontre, jamais le mechant.
    expect(par('rencontre')).toEqual(['Deck Rencontre'])
  })

  it('range chaque emplacement reel dans son bloc', () => {
    const blocs = repartirEnBlocs(
      plateau(
        noms('rencontre', 'Rhino'),
        noms('complot-principal', 'L’Effraction'),
        noms('piles-rencontre', 'Deck'),
        noms('terrain-soutien', 'Steve Rogers'),
        noms('main', 'Quinjet'),
      )
    )
    const par = (cle: string) => blocs.find((b) => b.cle === cle)?.unites.map((u) => u.cle)
    expect(par('vilain')).toEqual(['Rhino'])
    expect(par('complot')).toEqual(['L’Effraction'])
    expect(par('rencontre')).toEqual(['Deck'])
    // L'identite du heros vit dans `terrain-soutien` (zones.ts : area_hero y
    // est pose), donc dans le bloc `heros`.
    expect(par('heros')).toEqual(['Steve Rogers'])
    expect(par('main')).toEqual(['Quinjet'])
  })

  // `terrain-combat` est le seul emplacement melangeant deux camps : les
  // allies du joueur ET les sbires ennemis engages (plus l'environnement),
  // voir son commentaire dans zones.ts. L'allie doit rejoindre le heros, le
  // sbire doit rester avec les engages — jamais l'inverse.
  it('separe terrain-combat entre heros (allies) et engages (sbires, environnement)', () => {
    const blocs = repartirEnBlocs(
      plateau(
        emplacement('terrain-combat', [
          unite('Faucon', 'ally'),
          unite('Soldat Hydra', 'minion'),
          unite('Pont en ruine', 'environment'),
        ]),
        noms('terrain-soutien', 'Steve Rogers'),
      )
    )
    const par = (cle: string) => blocs.find((b) => b.cle === cle)?.unites.map((u) => u.cle)
    expect(par('heros')).toEqual(['Steve Rogers', 'Faucon'])
    expect(par('engages')).toEqual(['Soldat Hydra', 'Pont en ruine'])
    // L'allie n'est PAS aussi range dans les engages, ni le sbire dans le heros.
    expect(par('heros')).not.toContain('Soldat Hydra')
    expect(par('engages')).not.toContain('Faucon')
  })

  it('rend TOUJOURS les six blocs, meme vides', () => {
    const blocs = repartirEnBlocs(plateau())
    expect(blocs.map((b) => b.cle)).toEqual(['vilain', 'complot', 'rencontre', 'engages', 'heros', 'main'])
    expect(blocs.every((b) => b.unites.length === 0)).toBe(true)
  })

  it('garde l ordre des emplacements a l interieur d un bloc', () => {
    const blocs = repartirEnBlocs(
      plateau(noms('complot-principal', 'Principal'), noms('complots-secondaires', 'Annexe'))
    )
    expect(blocs.find((b) => b.cle === 'complot')?.unites.map((u) => u.cle)).toEqual(['Principal', 'Annexe'])
  })
})
