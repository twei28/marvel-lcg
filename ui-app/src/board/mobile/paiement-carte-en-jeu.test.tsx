// Payer avec une carte POSEE SUR LA TABLE, en portrait.
//
// Rapport joueur du 13/09/2026 : « la version mobile est top mais quand on
// doit payer des ressources avec des cartes sur la table, c'est impossible, on
// ne peut pas réduire la fenêtre de sélection des ressources ».
//
// Mesure avant correctif : la main s'ouvre seule sur une question de
// ressource, son voile couvre TOUT l'écran (`position: fixed; inset: 0`), et
// chaque ressource choisie fait repasser le plateau par un rendu SANS question
// le temps que le moteur réponde. `laQuestion` retombait à faux puis remontait,
// et la main se ROUVRAIT. Sur un coût à 3, il fallait la refermer trois fois.
import { render, fireEvent } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { PlateauPortrait } from './PlateauPortrait'
import type { BoardProps } from '../Board'
import type { EtatInteractif } from '../interaction'
import type { CleEmplacement, EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { ScanCardProps } from '../../components/ScanCard'

const unite = (cle: string, carte: Partial<ScanCardProps>): UniteAffichee =>
  ({ cle, carte: { id: cle, name: cle, kind: 'unknown', imageUrl: '', ...carte }, attachees: [] }) as UniteAffichee
const emplacement = (cle: CleEmplacement, ...unites: UniteAffichee[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }) as EmplacementAffiche
const plateau = (...e: EmplacementAffiche[]): Plateau =>
  ({ emplacements: e, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

const monde = { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] } as unknown as BoardProps['world']

const TABLE = plateau(
  emplacement('terrain-soutien', unite('7', { kind: 'support', name: 'Rifle sonique' })),
  emplacement('main', unite('9', { kind: 'event', name: 'Energie' }))
)

const question = (): Map<number, EtatInteractif> =>
  new Map<number, EtatInteractif>([
    [7, { role: 'ressource', choisie: false, agir: vi.fn() } as EtatInteractif],
    [9, { role: 'ressource', choisie: false, agir: vi.fn() } as EtatInteractif],
  ])

const rendre = (interactifs?: Map<number, EtatInteractif>) =>
  render(<PlateauPortrait world={monde} playerId={0} plateau={TABLE} interactifs={interactifs} />)

describe('payer avec une carte posee sur la table', () => {
  it('la main sort seule quand le moteur demande une ressource', () => {
    const { container } = rendre(question())
    expect(container.querySelector('.main-feuille-voile')).not.toBeNull()
  })

  it('une fois rangee a la main, elle NE SE ROUVRE PAS a la question suivante', () => {
    const vue = rendre(question())
    const voile = vue.container.querySelector('.main-feuille-voile')
    expect(voile).not.toBeNull()
    fireEvent.pointerDown(voile!)
    expect(vue.container.querySelector('.main-feuille-voile')).toBeNull()

    // Le va-et-vient reel : un rendu sans question, puis la question suivante.
    const redessiner = (inter?: Map<number, EtatInteractif>) =>
      vue.rerender(<PlateauPortrait world={monde} playerId={0} plateau={TABLE} interactifs={inter} />)
    redessiner(new Map())
    redessiner(question())
    expect(vue.container.querySelector('.main-feuille-voile')).toBeNull()

    // Et une troisieme ressource ne la rappelle pas davantage.
    redessiner(new Map())
    redessiner(question())
    expect(vue.container.querySelector('.main-feuille-voile')).toBeNull()
  })

  it('l encoche la rappelle, et l ouverture automatique reprend ensuite', () => {
    const vue = rendre(question())
    fireEvent.pointerDown(vue.container.querySelector('.main-feuille-voile')!)
    expect(vue.container.querySelector('.main-feuille-voile')).toBeNull()

    const encoche = vue.container.querySelector('.encoche-main')
    expect(encoche).not.toBeNull()
    fireEvent.click(encoche!)
    expect(vue.container.querySelector('.main-feuille-voile')).not.toBeNull()
  })

  it('un nouveau round efface le refus : la main peut ressortir seule', () => {
    const vue = rendre(question())
    fireEvent.pointerDown(vue.container.querySelector('.main-feuille-voile')!)
    const tourSuivant = { ...monde, round_id: 2 } as unknown as BoardProps['world']
    vue.rerender(<PlateauPortrait world={tourSuivant} playerId={0} plateau={TABLE} interactifs={new Map()} />)
    vue.rerender(<PlateauPortrait world={tourSuivant} playerId={0} plateau={TABLE} interactifs={question()} />)
    expect(vue.container.querySelector('.main-feuille-voile')).not.toBeNull()
  })
})
