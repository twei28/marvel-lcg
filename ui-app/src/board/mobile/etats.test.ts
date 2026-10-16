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

  // Quatrieme carte d'etat, ajoutee par le pack `sentinel` : elle a son nom
  // francais et sa classe propre, et ne retombe pas sur le repli generique.
  it('reconnait Exposé, la quatrieme carte d etat', () => {
    expect(etatDe(carte('Exposed'))).toEqual({ lettre: 'E', classe: 'est-expose', nom: 'Exposé' })
  })

  // Cinquieme carte d'etat (« Cloaked », pack TMNT) : nom francais et classe
  // propres, lettre K (le C est deja a Désorienté).
  it('reconnait Camouflé, la cinquieme carte d etat', () => {
    expect(etatDe(carte('Cloaked'))).toEqual({ lettre: 'K', classe: 'est-camoufle', nom: 'Camouflé' })
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
