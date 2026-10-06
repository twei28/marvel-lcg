import { describe, expect, it } from 'vitest'
import { cartesDeEtape } from './DetailCoup'
import type { EtapeDeroule } from './deroule-phase'

const etape = (champs: Partial<EtapeDeroule>): EtapeDeroule => ({ cle: 'x', temps: 'activation', titre: 'attaque', regle: '', ...champs }) as EtapeDeroule

describe('les cartes nommees par une etape de la phase du mechant', () => {
  it('une attaque : l auteur et la cible, chacun avec son identifiant', () => {
    expect(cartesDeEtape(etape({ carteId: 5, auteurNom: 'Rhino', cibleId: 9, cibleNom: 'Spider-Man' }))).toEqual([
      { id: 5, nom: 'Rhino' },
      { id: 9, nom: 'Spider-Man' },
    ])
  })

  it('une revelation : la carte revelee, jamais le heros qui revele', () => {
    expect(cartesDeEtape(etape({ titre: 'revelation', carteId: 40, auteurNom: 'Spider-Man', cibleNom: 'Assaut' }))).toEqual([
      { id: 40, nom: 'Assaut' },
    ])
  })

  it('sans identifiant, aucune carte', () => {
    expect(cartesDeEtape(etape({ auteurNom: 'Rhino', cibleNom: 'Spider-Man' }))).toEqual([])
  })
})
