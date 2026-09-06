// Un joueur éliminé quitte la table — sa carte de héros comprise.
//
// Ce que fait le moteur (`src/game/player/player.py`, `Player.Eliminate`) :
// il défausse alliés, soutiens, main, deck et obligations, MAIS exclut
// explicitement le type Identity. La carte de héros reste donc dans
// `area_hero`. Et le joueur reste dans `world.players`, parce que le
// descripteur est bâti sur `const_seat_order_players` — ce qui garde les
// numéros de siège stables, donc le sens de `playerId`.
//
// Résultat avant ce correctif, signalé en jeu à deux héros : le héros mort
// restait posé au milieu du terrain, seul rescapé de son aire.
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { construirePlateau } from './zones'
import type { World, WorldPlayer } from './world'

// Les cinq champs verifies par `estUneCarte` (world.ts) sont obligatoires :
// sans eux la carte est ecartee en silence et la table sort vide.
const carte = (id: number, extra: Record<string, unknown> = {}) => ({
  id,
  card_type: 'ally',
  name: `Carte ${id}`,
  card_id: `9900${id}`,
  pic_id: `9900${id}`,
  visible_for_players: [0, 1],
  down_card_ids: [],
  resources: [],
  info: {},
  traits: {},
  buffs: {},
  ...extra,
})

const LAURA = 1
const ALBERT = 2
const ALLIE_ALBERT = 30
const SOUTIEN_ALBERT = 31

function joueur(heroId: number, nom: string, elimine: boolean): unknown {
  return {
    area_hero: [carte(heroId, { card_type: 'hero', name: nom })],
    supports: heroId === ALBERT ? [carte(SOUTIEN_ALBERT, { card_type: 'support' })] : [],
    allies: heroId === ALBERT ? [carte(ALLIE_ALBERT)] : [],
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
    is_eliminated: elimine,
  }
}

function monde(albertElimine: boolean): World {
  return {
    render_id: 1,
    players: [
      joueur(LAURA, 'Laura Kinney', false) as WorldPlayer,
      joueur(ALBERT, 'Albert', albertElimine) as WorldPlayer,
    ],
  } as unknown as World
}

/**
 * Les cartes RÉELLEMENT dessinées. `idsAffiches` est la liste que le plateau
 * tient déjà pour savoir ce qui est sur la table (une pile n'y compte que pour
 * sa carte visible) : c'est exactement la question posée ici.
 */
function idsSurLaTable(world: World, playerId = 0): Set<number> {
  return construirePlateau(world, { playerId, catalogue: catalogueVide }).idsAffiches
}

describe('joueur éliminé', () => {
  it('laisse tout en place tant que personne n’est éliminé', () => {
    const ids = idsSurLaTable(monde(false))
    expect(ids).toContain(LAURA)
    expect(ids).toContain(ALBERT)
    expect(ids).toContain(ALLIE_ALBERT)
    expect(ids).toContain(SOUTIEN_ALBERT)
  })

  it('retire la CARTE DE HÉROS du joueur éliminé', () => {
    const ids = idsSurLaTable(monde(true))
    expect(ids).not.toContain(ALBERT)
  })

  it('retire aussi le reste de son aire', () => {
    const ids = idsSurLaTable(monde(true))
    expect(ids).not.toContain(ALLIE_ALBERT)
    expect(ids).not.toContain(SOUTIEN_ALBERT)
  })

  it('ne touche pas au joueur qui survit', () => {
    expect(idsSurLaTable(monde(true))).toContain(LAURA)
  })

  it('vaut aussi quand c’est LE joueur regardé qui est éliminé', () => {
    // La vue peut rester braquée sur lui : son aire doit être vide quand même,
    // pas montrer un héros mort en pleine forme.
    const ids = idsSurLaTable(monde(true), 1)
    expect(ids).not.toContain(ALBERT)
    expect(ids).toContain(LAURA)
  })
})
