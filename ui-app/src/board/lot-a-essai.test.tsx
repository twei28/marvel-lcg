// Lot A de l'implémentation des décisions du 13/10/2026 (essai) : l'affichage seul.
import { cleanup, render } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { PictoBoost, texteAlerteSeuil } from './CartouchePhase'
import type { EtapeDeroule } from './deroule-phase'
import { numerosDesSbires } from './NumerosSbires'

afterEach(() => cleanup())

describe('① seuil proche : « Encore N avant la défaite »', () => {
  it('à 2 ou moins du seuil', () => {
    expect(texteAlerteSeuil({ apres: 4, plafond: 6 })).toBe('Encore 2 avant la défaite')
    expect(texteAlerteSeuil({ apres: 5, plafond: 6 })).toBe('Encore 1 avant la défaite')
  })
  it('rien à 3 ou plus, au seuil (complétée), ou sans seuil (annexe)', () => {
    expect(texteAlerteSeuil({ apres: 3, plafond: 6 })).toBeUndefined()
    expect(texteAlerteSeuil({ apres: 6, plafond: 6 })).toBeUndefined()
    expect(texteAlerteSeuil({ apres: 5 })).toBeUndefined()
    expect(texteAlerteSeuil(undefined)).toBeUndefined()
  })
})

describe('④ boost à 0 : « +0 » gris', () => {
  it('sans ★ : marqué nul', () => {
    const { container } = render(<PictoBoost nombre={0} stat="atq" />)
    expect(container.querySelector('.est-boost')?.classList.contains('est-nul')).toBe(true)
  })
  it('avec ★ ou avec un apport : normal', () => {
    const { container } = render(
      <>
        <PictoBoost nombre={0} etoile stat="atq" />
        <PictoBoost nombre={2} stat="atq" />
      </>
    )
    expect(container.querySelectorAll('.est-nul')).toHaveLength(0)
  })
})


describe('⑩ numéros d’ordre des sbires sur la table', () => {
  const sbire = (cle: string, carteId: number, rangSbire: number, totalSbires = 3) =>
    ({ cle, temps: 'sbires', titre: 'attaque', regle: '', carteId, rangSbire, totalSbires, boosts: [] }) as EtapeDeroule
  const etapes = [sbire('a', 60, 1), sbire('b', 61, 2), sbire('c', 62, 3)]

  it('chaque sbire a son numéro ; ceux déjà passés sont barrés', () => {
    expect(numerosDesSbires(etapes, 'b')).toEqual([
      { carteId: 60, rang: 1, passe: true },
      { carteId: 61, rang: 2, passe: false },
      { carteId: 62, rang: 3, passe: false },
    ])
  })

  it('hors de l’étape 2B, ou avec un seul sbire : rien', () => {
    const menace = { cle: 'm', temps: 'menace', titre: 'menace', regle: '', boosts: [] } as EtapeDeroule
    expect(numerosDesSbires([menace, ...etapes], 'm')).toEqual([])
    expect(numerosDesSbires([sbire('x', 60, 1, 1)], 'x')).toEqual([])
  })
})
