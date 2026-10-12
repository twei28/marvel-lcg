// La couleur du joueur dans la boîte de la phase du méchant (refonte du
// 12/10/2026, décisions 14 à 20 et 57).
import { describe, expect, it } from 'vitest'
import type { Aspect, Catalogue } from './catalogue'
import { catalogueVide } from './catalogue'
import {
  aspectsDuJoueur,
  cadreDeLEtape,
  cadresDesJoueurs,
  COULEUR_ASPECT,
  COULEUR_COMMUNE,
  COULEUR_SANS_ASPECT,
  joueurDeLaCarte,
  styleDuCadre,
} from './couleur-joueur'
import type { EtapeDeroule } from './deroule-phase'
import type { World, WorldCard, WorldPlayer } from './world'

const ASPECTS: Record<string, Aspect> = {
  r1: 'aggression',
  r2: 'aggression',
  j1: 'justice',
  j2: 'justice',
  p1: 'protection',
  b1: 'basic',
}
const catalogue: Catalogue = { ...catalogueVide, aspect: (id) => ASPECTS[id] }

let prochainId = 1
const carte = (card_id: string): WorldCard => ({ id: prochainId++, card_id }) as WorldCard
const joueur = (ids: string[], extra: Partial<WorldPlayer> = {}): WorldPlayer =>
  ({
    area_hero: [],
    allies: [],
    supports: [],
    hand_cards: ids.map(carte),
    player_deck: [],
    player_discard_pile: [],
    engaged_enemies: [],
    ...extra,
  }) as unknown as WorldPlayer
const monde = (...joueurs: WorldPlayer[]): World => ({ players: joueurs }) as unknown as World

const etape = (sur: Partial<EtapeDeroule>): EtapeDeroule => ({
  cle: 'e',
  temps: 'mechant',
  titre: 'attaque',
  regle: '',
  boosts: [],
  ...sur,
})

describe('aspects et couleurs des joueurs', () => {
  it("prend l'aspect du deck, le plus représenté d'abord, sans Basique", () => {
    expect(aspectsDuJoueur(joueur(['j1', 'r1', 'r2', 'b1']), catalogue)).toEqual(['aggression', 'justice'])
  })

  it('un deck Basique seul est gris', () => {
    expect(cadresDesJoueurs(monde(joueur(['b1'])), catalogue)[0]?.couleurs).toEqual([COULEUR_SANS_ASPECT])
  })

  it('deux joueurs du même aspect : le second est rayé et garde son numéro de siège (Q15)', () => {
    const cadres = cadresDesJoueurs(monde(joueur(['j1']), joueur(['r1']), joueur(['j2'])), catalogue)
    expect(cadres.map((c) => c.raye)).toEqual([false, false, true])
    expect(cadres[2]).toMatchObject({ couleurs: [COULEUR_ASPECT.justice], siege: 3 })
  })

  it('un deck à deux aspects donne une pastille partagée (Q16)', () => {
    const [cadre] = cadresDesJoueurs(monde(joueur(['r1', 'p1'])), catalogue)
    const style = styleDuCadre({ genre: 'joueur', joueur: 0, ...cadre! })
    expect(style['--cadre-joueur']).toBe(COULEUR_ASPECT.aggression)
    expect(style['--cadre-pastille']).toContain('conic-gradient')
    expect(style['--cadre-pastille']).toContain(COULEUR_ASPECT.protection)
  })
})

describe("le cadre de l'étape affichée", () => {
  const sbire = carte('m1')
  const alliee = carte('a1')
  const m = monde(joueur(['j1']), joueur(['r1'], { allies: [alliee], engaged_enemies: [sbire] }))
  const cadres = cadresDesJoueurs(m, catalogue)
  const proprietaire = (id: number | undefined) => joueurDeLaCarte(m, id)

  it('menace, bilan et changement de stade : gris acier, commun à la table (Q20, Q57)', () => {
    for (const e of [etape({ temps: 'menace' }), etape({ temps: 'bilan' }), etape({ stade: 'manigance' })]) {
      expect(cadreDeLEtape(e, cadres, proprietaire)).toEqual({ genre: 'commun' })
    }
    expect(styleDuCadre({ genre: 'commun' })['--cadre-joueur']).toBe(COULEUR_COMMUNE)
  })

  it("une attaque prend la couleur du joueur dont la carte est visée (ici un allié de J2)", () => {
    expect(cadreDeLEtape(etape({ cibleId: alliee.id }), cadres, proprietaire)).toMatchObject({
      genre: 'joueur',
      joueur: 1,
      couleurs: [COULEUR_ASPECT.aggression],
    })
  })

  it('une carte révélée prend la couleur du joueur qui la révèle', () => {
    expect(cadreDeLEtape(etape({ temps: 'revelation', joueur: 0 }), cadres, proprietaire)).toMatchObject({
      genre: 'joueur',
      joueur: 0,
    })
  })

  it('un joueur inconnu ne fait pas deviner une couleur : commun', () => {
    expect(cadreDeLEtape(etape({ cibleId: 9999 }), cadres, proprietaire)).toEqual({ genre: 'commun' })
  })
})
