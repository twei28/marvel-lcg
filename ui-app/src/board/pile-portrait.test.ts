// Une pile se pose en PORTRAIT, quelle que soit sa carte du dessus.
//
// Une manigance se pose en paysage sur la table. Quand une manigance défaussée
// arrivait sur le dessus de la défausse, la pile passait de 127 à 176 px de
// large : deck et défausse ne tenaient plus côte à côte dans les 270 px de la
// colonne de gauche, se repliaient l'une sous l'autre, et le groupe montait de
// 203 à 358 px — il débordait sur la rangée du dessous et décalait la table
// entière. Mesuré le 08/08/2026, signalé en jeu.
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { construirePlateau } from './zones'
import type { World } from './world'

const carte = (id: number, type: string, nom: string) => ({
  id,
  card_type: type,
  name: nom,
  card_id: `8800${id}`,
  pic_id: `8800${id}`,
  visible_for_players: [0],
  down_card_ids: [],
  resources: [],
  info: {},
  traits: {},
  buffs: {},
})

const MANIGANCE_DEFAUSSEE = 40
const MANIGANCE_EN_JEU = 41

function monde(): World {
  return {
    render_id: 1,
    // La manigance annexe défaussée est la DERNIÈRE de la pile, donc dessus.
    encounter_discard_pile: [
      carte(38, 'Minion', 'Weapons Runner'),
      carte(MANIGANCE_DEFAUSSEE, 'EncounterSideScheme', 'Defense Network'),
    ],
    area_schemes_side: [carte(MANIGANCE_EN_JEU, 'EncounterSideScheme', 'The Immortal Klaw')],
    players: [
      {
        area_hero: [],
        supports: [],
        allies: [],
        obligations_area: [],
        engaged_enemies: [],
        environment_area: [],
        hand_cards: [],
        reserve: [],
        player_deck: [],
        player_discard_pile: [],
        additional_deck: [],
        additional_discard_pile: [],
        set_aside_deck: [],
        set_aside_nemesis_sets: [],
        resources: '',
        is_eliminated: false,
      },
    ],
  } as unknown as World
}

/** Retrouve une carte dessinée, où qu'elle soit sur la table. */
function dessinee(world: World, id: number) {
  const plateau = construirePlateau(world, { playerId: 0, catalogue: catalogueVide })
  for (const emplacement of plateau.emplacements) {
    for (const groupe of emplacement.groupes) {
      for (const unite of groupe) {
        if (Number(unite.carte.id) === id) return { unite, zone: emplacement.cle }
      }
    }
  }
  return undefined
}

describe('orientation des piles', () => {
  it('pose en PORTRAIT une manigance qui coiffe la défausse', () => {
    const trouvee = dessinee(monde(), MANIGANCE_DEFAUSSEE)
    expect(trouvee?.zone).toBe('piles-rencontre')
    expect(trouvee?.unite.carte.isLandscape).toBe(false)
  })

  it('laisse en PAYSAGE une manigance encore en jeu', () => {
    // C'est la moitié qui compte vraiment : le correctif ne doit pas redresser
    // les manigances de la table, seulement celles qui coiffent une pile.
    const trouvee = dessinee(monde(), MANIGANCE_EN_JEU)
    expect(trouvee?.zone).toBe('complots-secondaires')
    expect(trouvee?.unite.carte.isLandscape).toBe(true)
  })
})
