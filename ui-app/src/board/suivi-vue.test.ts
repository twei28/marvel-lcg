// La vue « Auto » suit celui qui doit agir — mais pas jusqu'a l'absurde.
//
// Ce qui a ete signale en jeu : « la partie se lance mais reste bloquee quand
// elle est censee afficher ma main ». En verite rien n'etait bloque. Pendant les
// mulligans, le moteur interroge chaque joueur a son tour ; la vue basculait
// donc sur le voisin, dont le moteur NE NOUS MONTRE PAS la main (elle n'est
// visible que du siege qui la tient). On voyait son plateau, aucune main, et
// plus rien a faire : tout indiquait un blocage.
//
// La regle : on ne suit un autre joueur que si on a quelque chose a y voir. En
// hot-seat (un seul navigateur pour tous les sieges) toute main s'affiche des
// qu'on regarde son joueur, le suivi est donc inconditionnel ; en partie
// repartie, chacun reste chez soi.
//
// ⚠ 09/09/2026 : la premiere ecriture du cas hot-seat supposait que le moteur
// inscrit tous les sieges locaux dans `visible_for_players`. Faux : la liste est
// calculee par proprietaire (card.py:845), la main du voisin porte [1] meme en
// hot-seat, et la vue ne le suivait jamais. Le cas est desormais ecrit avec la
// main CACHEE, comme le moteur la livre vraiment.
import { describe, expect, it } from 'vitest'
import { peutSuivre } from './suivi-vue'
import type { World, WorldPlayer } from './world'

const carte = (id: number, visiblePour: number[]) => ({
  id,
  card_type: 'event',
  name: `Carte ${id}`,
  card_id: `990${id}`,
  pic_id: `990${id}`,
  visible_for_players: visiblePour,
  down_card_ids: [],
  resources: [],
  info: {},
  traits: {},
  buffs: {},
})

const joueur = (main: ReturnType<typeof carte>[]): WorldPlayer =>
  ({ hand_cards: main, is_eliminated: false }) as unknown as WorldPlayer

const monde = (joueurs: WorldPlayer[]): World => ({ players: joueurs }) as unknown as World

describe('suivi automatique de la vue', () => {
  it('suit toujours notre propre siege', () => {
    const m = monde([joueur([carte(1, [0])]), joueur([carte(2, [1])])])
    expect(peutSuivre(m, 0, 0, true)).toBe(true)
  })

  it('en hot-seat, suit le voisin MEME si le moteur dit sa main cachee', () => {
    // Un seul navigateur tient les deux sieges ; la main du siege 1 porte [1],
    // c'est ainsi que le moteur la livre, et elle s'affiche quand meme.
    const m = monde([joueur([carte(1, [0])]), joueur([carte(2, [1])])])
    expect(peutSuivre(m, 1, 0, false)).toBe(true)
  })

  it('en partie repartie, suit un voisin dont la main nous est visible', () => {
    const m = monde([joueur([carte(1, [0])]), joueur([carte(2, [0, 1])])])
    expect(peutSuivre(m, 1, 0, true)).toBe(true)
  })

  it('en partie repartie, ne suit PAS un voisin dont la main nous est cachee', () => {
    const m = monde([joueur([carte(1, [0])]), joueur([carte(2, [1])])])
    expect(peutSuivre(m, 1, 0, true)).toBe(false)
  })

  it('suit un voisin qui n a pas de main : il n y a rien a cacher', () => {
    // Main videe, ou pas encore distribuee : le suivi reste utile, on verra son
    // plateau, et aucune main manquante ne fera croire a un blocage.
    const m = monde([joueur([carte(1, [0])]), joueur([])])
    expect(peutSuivre(m, 1, 0, true)).toBe(true)
  })

  it('ne suit pas un siege qui n existe pas', () => {
    const m = monde([joueur([carte(1, [0])])])
    expect(peutSuivre(m, 3, 0, true)).toBe(false)
  })

  it('se laisse faire quand le monde n est pas encore la', () => {
    // Au tout premier rendu, rien n'est charge : ne pas bloquer le suivi.
    expect(peutSuivre(undefined, 1, 0, true)).toBe(true)
  })
})
