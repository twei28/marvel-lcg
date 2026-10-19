import { describe, expect, it } from 'vitest'
import { construire } from './catalogue'
import { iconesImprimees } from './traduction-posee'

describe('icônes de manigance imprimées', () => {
  it('suit l’ordre du scan : Accélération, Crise, Aléas, Amplification', () => {
    expect(iconesImprimees({ Crisis: '1', Acceleration: '1', Amplify: '1', Hazard: '1' })).toEqual([
      'acceleration',
      'crisis',
      'hazard',
      'amplify',
    ])
  })

  it('ignore Boost (hors de la boîte de texte), les champs vides et les zéros', () => {
    expect(iconesImprimees({ Boost: '2', Crisis: '', Hazard: '0', Acceleration: '1' })).toEqual(['acceleration'])
    expect(iconesImprimees(undefined)).toEqual([])
  })

  it('le catalogue les rend par carte', () => {
    const catalogue = construire({
      pack: [
        { card_id: 'tx010', desc: { Boost: '1', Acceleration: '1', Crisis: '1' } },
        { card_id: '01001a', desc: { HP: '10' } },
      ],
    })
    expect(catalogue.iconesManigance?.('tx010')).toEqual(['acceleration', 'crisis'])
    expect(catalogue.iconesManigance?.('01001a')).toEqual([])
  })
})
