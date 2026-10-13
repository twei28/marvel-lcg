// L'etape 3 dite par joueur (essai, 13/10/2026) : « Carte rencontre 2/2 · Captain America ».
import { describe, expect, it } from 'vitest'
import type { EtapeDeroule } from './deroule-phase'
import { rencontreDuJoueur } from './vue-cartouche'

const rev = (cle: string, joueur: number, auteurNom: string, extra: Partial<EtapeDeroule> = {}): EtapeDeroule =>
  ({ cle, temps: 'revelation', titre: 'revelation', regle: '', joueur, auteurNom, boosts: [], ...extra }) as EtapeDeroule
const dist = (joueur: number, montant: number): EtapeDeroule =>
  ({ cle: `d${joueur}`, temps: 'distribution', titre: 'distribution', regle: '', joueur, montant, boosts: [] }) as EtapeDeroule

describe('la carte rencontre de chaque joueur', () => {
  const etapes = [dist(0, 2), dist(1, 1), rev('a', 0, '* Ironheart'), rev('b', 0, '* Ironheart'), rev('c', 1, 'Captain America')]

  it('numerotee par joueur, avec son heros (prefixe decoratif retire)', () => {
    expect(rencontreDuJoueur(etapes, 'a')).toEqual({ rang: 1, total: 2, nom: 'Ironheart' })
    expect(rencontreDuJoueur(etapes, 'b')).toEqual({ rang: 2, total: 2, nom: 'Ironheart' })
    expect(rencontreDuJoueur(etapes, 'c')).toEqual({ rang: 1, total: 1, nom: 'Captain America' })
  })

  it('le total est connu des la premiere carte, Renfort compris', () => {
    const debut = [dist(0, 2), rev('a', 0, 'Ironheart'), rev('r', 0, 'Ironheart', { parSurge: true })]
    expect(rencontreDuJoueur(debut, 'a')).toEqual({ rang: 1, total: 3, nom: 'Ironheart' })
  })

  it('le tableau de distribution de l essai compte aussi', () => {
    const tableau = { cle: 't', temps: 'distribution', titre: 'distribution-tableau', regle: '', boosts: [], lignesDistribution: [{ joueur: 0, cartes: 2, raisons: [] }] } as unknown as EtapeDeroule
    expect(rencontreDuJoueur([tableau, rev('a', 0, 'Ironheart')], 'a')?.total).toBe(2)
  })

  it('une etape qui n est pas une revelation : rien', () => {
    expect(rencontreDuJoueur(etapes, 'd0')).toBeUndefined()
  })
})
