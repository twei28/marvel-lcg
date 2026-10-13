// Lot A de l'implémentation des décisions du 13/10/2026 (essai) : l'affichage seul.
import { cleanup, render } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { PictoBoost, texteAlerteSeuil } from './CartouchePhase'
import type { EtapeDeroule } from './deroule-phase'
import { numerosDesSbires } from './NumerosSbires'
import { avecEcranStadeRevele } from './etapes-essai'
import { coupsDeLEtape } from './coups-sur-table'

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

describe('② le nouveau stade qui fait quelque chose en se révélant (13/10/2026)', () => {
  const stade = {
    cle: 'stade:1', temps: 'mechant', titre: 'stade', regle: '', carteId: 49, cibleNom: 'Distribution d’Armes', boosts: [],
    effets: [{ genre: 'entree', carte: 'Contrebande', carte_id: 80, type: 'manigance' }],
  } as unknown as EtapeDeroule

  it('un écran « Une fois révélé » juste après celui du stade, qui garde l’avant → après', () => {
    const suite = avecEcranStadeRevele([stade])
    expect(suite.map((e) => e.titre)).toEqual(['stade', 'stade-revele'])
    expect(suite[0].effets).toBeUndefined()
    expect(suite[1]).toMatchObject({ cle: 'stade:1:revele', carteId: 49, effets: stade.effets })
  })

  it('un stade sans effet n’a pas d’écran de plus', () => {
    const sansEffet = { ...stade, effets: undefined }
    expect(avecEcranStadeRevele([sansEffet])).toEqual([sansEffet])
  })

  it('ses effets chiffrés font voler leurs jetons depuis la boîte', () => {
    const revele = { ...stade, cle: 's:revele', titre: 'stade-revele', effets: [{ genre: 'degats', cible: 'Ironheart', cible_id: 1, montant: 2, restant: 9 }] } as unknown as EtapeDeroule
    expect(coupsDeLEtape(revele)).toEqual([{ genre: 'degats', cibleId: 1, avant: 11, montant: 2, depuis: { lieu: 'boite-corps' } }])
  })
})
