import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { PlateauPortrait } from './PlateauPortrait'
import type { BoardProps } from '../Board'
import type { EmplacementAffiche, Plateau, UniteAffichee } from '../zones'
import type { CleEmplacement } from '../zones'
import type { ScanCardProps } from '../../components/ScanCard'

const unite = (cle: string, carte: Partial<ScanCardProps>): UniteAffichee =>
  ({ cle, carte: { id: cle, name: cle, kind: 'unknown', imageUrl: '', ...carte }, attachees: [] }) as UniteAffichee

const emplacement = (cle: CleEmplacement, ...unites: UniteAffichee[]): EmplacementAffiche =>
  ({ cle, titre: cle, groupes: [unites], nombreSurLaLigne: unites.length }) as EmplacementAffiche

const plateau = (...emplacements: EmplacementAffiche[]): Plateau =>
  ({ emplacements, nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 }) as Plateau

const monde = { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] } as unknown as BoardProps['world']

describe('PlateauPortrait — bloc complot', () => {
  it('pose la manigance principale en petit, avec sa menace en cases a cote', () => {
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'complot-principal',
            unite('L’Effraction', { name: 'L’Effraction', kind: 'main-scheme', schemeThreat: '3/6' })
          )
        )}
      />
    )
    expect(container.querySelector('.portrait-nom')).toHaveTextContent('L’Effraction')
    expect(document.querySelectorAll('.barre-menace-case')).toHaveLength(6)
    expect(document.querySelectorAll('.barre-menace-case.est-pose')).toHaveLength(3)
  })

  it('ne pose jamais de chiffre sur l illustration de la manigance', () => {
    // Regle centrale du chantier (deja violee une fois a la tache 4) : un
    // chiffre ne va jamais sur le scan. Meme si `stats` trainait dessus.
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'complot-principal',
            unite('Complot', {
              name: 'Complot',
              kind: 'main-scheme',
              schemeThreat: '2/5',
              stats: [{ label: 'ATQ', value: 2 }],
            })
          )
        )}
      />
    )
    expect(document.querySelector('.scan-card .scan-stats-calee')).toBeNull()
  })

  it('sans manigance principale, ne dessine ni carte ni barre', () => {
    const { container } = render(<PlateauPortrait world={monde} playerId={0} plateau={plateau()} />)
    expect(container.querySelector('.barre-menace-bloc')).toBeNull()
  })
})

describe('PlateauPortrait — compteurs de rencontre', () => {
  it('compte le deck et la defausse de rencontre', () => {
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau(
          emplacement(
            'piles-rencontre',
            unite('rencontre-encounter-deck', { pileCount: 33 }),
            unite('rencontre-encounter-discard', { pileCount: 0 })
          )
        )}
      />
    )
    expect(screen.getByText('33')).toBeInTheDocument()
    expect(screen.getAllByText('0').length).toBeGreaterThan(0)
  })

  it('sans pile de rencontre, montre des compteurs a zero plutot que rien', () => {
    // Un bloc qui apparait/disparait ferait sauter la hauteur des autres
    // (spec du 11/09/2026) : la rencontre montre toujours ses compteurs.
    const { container } = render(<PlateauPortrait world={monde} playerId={0} plateau={plateau()} />)
    expect(container.querySelector('.portrait-compteurs')).not.toBeNull()
  })
})
