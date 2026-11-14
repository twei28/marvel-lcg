// La pastille de PV d'un personnage annonce « courant / maximum ».
//
// Le maximum venait du CATALOGUE, c'est-a-dire du PV imprime sur la carte. Or il
// bouge en jeu : une amelioration qui donne « +2 points de vie » releve le
// plafond. Un allie a 5 PV sur une carte qui en imprime 3 s'affichait donc
// « 5/3 », un rapport absurde, et un allie soigne a fond paraissait blesse.
//
// Le moteur connait ce maximum courant (max_health, qui suit UpdateMaxHealth).
// Il l'envoie desormais dans `info`. Le catalogue ne sert plus que de secours,
// pour une partie servie par un moteur qui ne l'expose pas encore.
import { describe, expect, it } from 'vitest'
import { toScanCard, type ContexteCarte } from './card-model'
import { catalogueVide, type Catalogue } from './catalogue'
import type { WorldCard } from './world'

const CODE = '01002'

function allie(info: Record<string, number>): WorldCard {
  return {
    id: 7,
    bind_object_id: 0,
    name: 'Black Cat',
    info,
    traits: {},
    buffs: {},
    card_id: CODE,
    pic_id: CODE,
    down_card_ids: [],
    card_type: 'Ally',
    is_face_up: true,
    is_ready: true,
    visible_for_players: [0],
  } as unknown as WorldCard
}

/** Catalogue qui connait le PV IMPRIME de la carte : 3. */
const catalogue: Catalogue = { ...catalogueVide, pvMax: () => 3 }

const contexte = (cat: Catalogue): ContexteCarte => ({
  playerId: 0,
  actives: new Set<number>(),
  catalogue: cat,
})

describe('pastille de PV', () => {
  it('suit le maximum du moteur, ameliorations comprises', () => {
    // 5 PV sur 5, sur une carte qui n'en imprime que 3 : une amelioration a
    // releve le plafond. Avant, cette carte affichait « 5/3 ».
    const carte = toScanCard(allie({ health: 5, max_health: 5 }), contexte(catalogue))
    expect(carte.allyHp).toBe('5/5')
  })

  it('montre bien les degats subis sur le maximum releve', () => {
    const carte = toScanCard(allie({ health: 2, max_health: 5 }), contexte(catalogue))
    expect(carte.allyHp).toBe('2/5')
  })

  it('retombe sur le PV imprime quand le moteur ne dit rien', () => {
    const carte = toScanCard(allie({ health: 2 }), contexte(catalogue))
    expect(carte.allyHp).toBe('2/3')
  })

  it('n affiche aucun rapport sans maximum connu d aucune source', () => {
    const carte = toScanCard(allie({ health: 2 }), contexte(catalogueVide))
    expect(carte.allyHp).toBe('2')
  })

  it('ignore un maximum a zero, que le moteur envoie pour les PV infinis', () => {
    const carte = toScanCard(allie({ health: 4, max_health: 0 }), contexte(catalogue))
    expect(carte.allyHp).toBe('4/3')
  })

  it('laisse les PV infinis tels quels', () => {
    const carte = toScanCard(
      allie({ health: 1, max_health: 0, is_infinite_health: 1 }),
      contexte(catalogue)
    )
    expect(carte.allyHp).toBe('∞')
  })
})
