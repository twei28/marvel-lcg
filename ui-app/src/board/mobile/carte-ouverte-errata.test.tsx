// Retour d'un joueur : « On ne voit pas les errata sur le téléphone. » L'aperçu agrandi du plateau mobile (CarteOuverte)
// affichait le scan nu : ni voile ni pastille « Errata ». Il porte désormais les mêmes que l'ordinateur.
import { render } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { CarteOuverte } from './CarteOuverte'
import { CODES_ERRATA } from '../errata-rrg'
import type { ScanCardProps } from '../../components/ScanCard'

const carte = (codeCarte: string | undefined, extra: Partial<ScanCardProps> = {}): ScanCardProps =>
  ({ id: 'c1', name: 'Carte', kind: 'event', imageUrl: 'x.jpg', codeCarte, ...extra }) as ScanCardProps

describe('CarteOuverte : errata officiel', () => {
  it('pose la pastille Errata sur une carte qui en a un', () => {
    render(<CarteOuverte carte={carte(CODES_ERRATA.find((c) => !c.endsWith('b')))} onFermer={() => {}} />)
    expect(document.querySelector('.carte-ouverte .pastille-errata')).toBeInTheDocument()
  })
  it('ne pose rien sur une carte sans errata', () => {
    render(<CarteOuverte carte={carte('99999')} onFermer={() => {}} />)
    expect(document.querySelector('.pastille-errata')).not.toBeInTheDocument()
  })
  it('l\'autre face porte l\'errata de SA carte, pas celui de la face en jeu', () => {
    const code = CODES_ERRATA[0]
    render(<CarteOuverte carte={carte('99999', { autresFaces: [{ url: 'y.jpg', code }] })} detail onFermer={() => {}} />)
    expect(document.querySelectorAll('.pastille-errata')).toHaveLength(1)
  })
})
