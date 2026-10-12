// Lot 2 de la refonte (12/10/2026, decision 55) : les noms de cartes ecrits
// dans la boite ouvrent la carte, comme la carte elle-meme.
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, render } from '@testing-library/react'
import { NomsSurvolables, Texte, nomsMontrables } from './noms-survolables'
import type { ScanCardProps } from '../components/ScanCard'

afterEach(cleanup)

const scan = (id: number): ScanCardProps => ({ id: String(id), name: `carte ${id}`, kind: 'minion', imageUrl: '' })

describe('noms-survolables', () => {
  it('sans fournisseur (hors essai), la phrase est rendue telle quelle', () => {
    const { container } = render(<p><Texte>{'Attaque de Klaw'}</Texte></p>)
    expect(container.innerHTML).toBe('<p>Attaque de Klaw</p>')
  })

  it('dans la boite, le nom devient survolable avec l identifiant de sa carte', () => {
    const { container } = render(
      <NomsSurvolables value={[{ nom: 'Klaw', carteId: 7 }]}>
        <p><Texte>{'Attaque de Klaw'}</Texte></p>
      </NomsSurvolables>
    )
    const nom = container.querySelector('b.essai-nom')
    expect(nom?.textContent).toBe('Klaw')
    expect(nom?.getAttribute('data-card-id')).toBe('7')
    expect(container.textContent).toBe('Attaque de Klaw')
  })

  it('le nom le plus long gagne (Spider-Man 2099 avant Spider-Man)', () => {
    const { container } = render(
      <NomsSurvolables value={[{ nom: 'Spider-Man', carteId: 1 }, { nom: 'Spider-Man 2099', carteId: 2 }]}>
        <p><Texte>{'Spider-Man 2099 défend'}</Texte></p>
      </NomsSurvolables>
    )
    const noms = Array.from(container.querySelectorAll('b.essai-nom'))
    expect(noms.map((n) => n.getAttribute('data-card-id'))).toEqual(['2'])
  })

  it('ne garde que les noms dont la carte est montrable, un identifiant par nom', () => {
    const noms = nomsMontrables(
      [
        { nom: 'Klaw', carteId: 7 },
        { nom: 'Klaw', carteId: 8 },
        { nom: 'Rhino', carteId: 9 },
        { nom: 'X', carteId: 7 },
        { nom: 'Sans carte' },
      ],
      [scan(7), scan(8)]
    )
    expect(noms).toEqual([{ nom: 'Klaw', carteId: 7 }])
  })
})
