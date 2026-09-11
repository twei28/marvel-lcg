import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { CarteAvecChiffres } from './CarteAvecChiffres'
import type { ScanCardProps } from '../../components/ScanCard'

const carte: ScanCardProps = { id: '1', name: 'Rhino', kind: 'villain', imageUrl: '/scan/01097' }

describe('CarteAvecChiffres', () => {
  it('met les chiffres A COTE de la carte, jamais dessus', () => {
    const { container } = render(
      <CarteAvecChiffres carte={carte} nom="RHINO" surtitre="Stade 1" chiffres={[{ valeur: '14/14', libelle: 'PV' }]} />
    )
    // La carte et les chiffres sont FRERES : aucun chiffre a l'interieur du scan.
    expect(container.querySelector('.scan-card .portrait-chiffre')).toBeNull()
    expect(container.querySelector('.portrait-carte-chiffres .portrait-chiffre')).not.toBeNull()
    expect(screen.getByText('14/14')).toBeInTheDocument()
    expect(screen.getByText('PV')).toBeInTheDocument()
    expect(screen.getByText('RHINO')).toBeInTheDocument()
    expect(screen.getByText('Stade 1')).toBeInTheDocument()
  })

  it('sans chiffre, n affiche pas de colonne vide', () => {
    const { container } = render(<CarteAvecChiffres carte={carte} nom="RHINO" chiffres={[]} />)
    expect(container.querySelector('.portrait-carte-chiffres')).toBeNull()
  })

  it('ne transmet pas les stats a ScanCard : aucun badge cale sur l illustration', () => {
    // toScanCard() (card-model.ts) peuple TOUJOURS `stats` pour une carte
    // reelle ; si on la laisse fuiter vers ScanCard, elle pose ses propres
    // badges *par-dessus* le scan (.scan-stats-calee, position absolute) en
    // plus des chiffres qu'on affiche deja a cote : exactement l'interdit du
    // chantier.
    const carteAvecStats: ScanCardProps = { ...carte, stats: [{ label: 'ATQ', value: 2 }] }
    const { container } = render(
      <CarteAvecChiffres carte={carteAvecStats} nom="RHINO" chiffres={[{ valeur: '2', libelle: 'ATQ' }]} />
    )
    expect(container.querySelector('.scan-card .scan-stats-calee')).toBeNull()
  })
})
