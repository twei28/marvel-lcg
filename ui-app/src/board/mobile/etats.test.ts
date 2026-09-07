import { describe, expect, it } from 'vitest'
import { etatDe, separerAttachees } from './etats'
import type { ScanCardProps } from '../../components/ScanCard'

const carte = (name: string, kind: ScanCardProps['kind'] = 'status'): ScanCardProps => ({
  id: name, name, kind, imageUrl: '',
})

describe('etatDe', () => {
  it('reconnait les trois etats par leur nom, sans tenir compte de la casse', () => {
    expect(etatDe(carte('Tough'))?.lettre).toBe('T')
    expect(etatDe(carte('STUNNED'))?.classe).toBe('est-sonne')
    expect(etatDe(carte(' confused '))?.nom).toBe('Désorienté')
  })

  // Le moteur pose les statuts avec kind 'status' (Board.tsx:174). Un statut
  // dont le nom serait traduit ou inconnu reste un etat, avec son initiale.
  it('traite toute carte de kind status comme un etat, meme au nom inconnu', () => {
    expect(etatDe(carte('Coriace', 'status'))).toEqual({ lettre: 'C', classe: 'est-autre', nom: 'Coriace' })
  })

  it('ne prend pas une amelioration pour un etat', () => {
    expect(etatDe(carte('Web-Shooter', 'upgrade'))).toBeUndefined()
  })
})

describe('separerAttachees', () => {
  it('separe les etats des ameliorations en gardant leur ordre', () => {
    const { etats, ameliorations } = separerAttachees([
      carte('Web-Shooter', 'upgrade'), carte('Stunned'), carte('Tough'), carte('Armor', 'upgrade'),
    ])
    expect(etats.map((etat) => etat.lettre)).toEqual(['S', 'T'])
    expect(ameliorations.map((a) => a.name)).toEqual(['Web-Shooter', 'Armor'])
  })
})
