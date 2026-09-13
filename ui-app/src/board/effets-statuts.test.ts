// Les statuts poses ou retires entre deux rendus, tels que le plateau les
// annonce d'un badge. Voir effets-statuts.ts pour le pourquoi.
import { describe, expect, it } from 'vitest'
import { deltasStatuts, libelleStatut, statutsPortes } from './effets-statuts'
import type { WorldCard } from './world'

const carte = (id: number, card_type: string, card_id: string, bind = 0): WorldCard =>
  ({ id, card_type, card_id, bind_object_id: bind, name: card_id, info: {} }) as unknown as WorldCard

const monde = (...cartes: WorldCard[]) => new Map(cartes.map((c) => [c.id, c]))

const klaw = carte(97, 'EncounterVillain', '01113')
const heros = carte(1, 'Hero', '01001a')

describe('statuts portes', () => {
  it('rattache chaque statut a son porteur, et ignore la pile sans porteur', () => {
    const portes = statutsPortes(monde(klaw, carte(200, 'StatusCard', 'stunned', 97), carte(201, 'StatusCard', 'tough', 0)))
    expect(portes.get(97)).toEqual(['stunned'])
    expect(portes.has(0)).toBe(false)
  })
})

describe('deltas de statuts', () => {
  it('signale un statut qui vient d etre pose', () => {
    const avant = monde(klaw)
    const apres = monde(klaw, carte(200, 'StatusCard', 'confused', 97))
    expect(deltasStatuts(avant, apres)).toEqual([[97, { kind: 'status', statut: 'confused', value: 1 }]])
  })

  it('signale un statut qui vient d etre retire', () => {
    const avant = monde(klaw, carte(200, 'StatusCard', 'stunned', 97))
    const apres = monde(klaw)
    expect(deltasStatuts(avant, apres)).toEqual([[97, { kind: 'status', statut: 'stunned', value: -1 }]])
  })

  // Quatrieme carte d'etat, pack `sentinel`. Sans son entree dans STATUTS,
  // `estStatut` la rejetterait et le badge ne partirait jamais.
  it('signale Exposé, la quatrieme carte d etat', () => {
    const avant = monde(klaw)
    const apres = monde(klaw, carte(202, 'StatusCard', 'exposed', 97))
    expect(deltasStatuts(avant, apres)).toEqual([[97, { kind: 'status', statut: 'exposed', value: 1 }]])
    expect(libelleStatut('exposed', 1, 'fr')).toBe('Exposé')
  })

  it('ne dit rien quand rien ne change, meme avec un statut en place', () => {
    const m = monde(klaw, carte(200, 'StatusCard', 'tough', 97))
    expect(deltasStatuts(m, m)).toEqual([])
  })

  it('la pose l emporte sur le retrait dans le meme rendu', () => {
    // Un Robuste consomme et remplace d'un coup : on lit « Robuste », pas « retire ».
    const avant = monde(heros, carte(200, 'StatusCard', 'tough', 1))
    const apres = monde(heros, carte(201, 'StatusCard', 'tough', 1), carte(202, 'StatusCard', 'stunned', 1))
    expect(deltasStatuts(avant, apres)).toEqual([[1, { kind: 'status', statut: 'stunned', value: 1 }]])
  })

  it('un porteur vaincu ne fait pas annoncer la perte de ses statuts', () => {
    const avant = monde(klaw, carte(200, 'StatusCard', 'stunned', 97))
    const apres = monde()
    expect(deltasStatuts(avant, apres)).toEqual([])
  })
})

describe('libelle du badge', () => {
  it('parle la langue du plateau', () => {
    expect(libelleStatut('stunned', 1, 'fr')).toBe('Sonné')
    expect(libelleStatut('stunned', 1, 'en')).toBe('Stunned')
    expect(libelleStatut('tough', -1, 'fr')).toBe('Robuste retiré')
    expect(libelleStatut('confused', -1, 'en')).toBe('Confused removed')
  })
})
