// Defaut 5 de la revue finale du 11/09/2026 : en vue « Auto » (le defaut,
// `vueForcee === null`), `board.tsx` passe `seulCeJoueur: false`. C'est voulu
// pour le plateau PC, qui pose les tables cote a cote « comme une vraie partie
// a plusieurs ». Sur telephone, c'est faux : « Ton héros » listait alors les
// heros et allies de TOUTE la table, et « Engagés » les ennemis de tout le
// monde. Le titre ment, et la hauteur des blocs devient imprevisible.
//
// Le portrait ne deplie qu'un joueur a la fois, les onglets changent de
// joueur : il lui faut donc toujours `seulCeJoueur: true`.

import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { catalogueVide } from '../catalogue'
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import { construirePlateau } from '../zones'
import { repartirEnBandes } from './bandes-portrait'
import type { World, WorldPlayer } from '../world'

/** Deux joueurs, chacun avec son heros et son allie. */
function tableADeuxJoueurs(): World {
  const joueur = (id: number, nomHeros: string, nomAllie: string): WorldPlayer =>
    siege({
      area_hero: [carteSurTable(id * 10, '01001a', 'Hero', nomHeros)],
      allies: [carteSurTable(id * 10 + 1, '01006', 'Ally', nomAllie)],
    })
  const monde = tableAvec(joueur(1, '* Spider-Man', 'Allie de Spidey'), {})
  return { ...monde, players: [joueur(1, '* Spider-Man', 'Allie de Spidey'), joueur(2, '* Hulk', 'Allie de Hulk')] }
}

function nomsDuBlocHeros(seulCeJoueur: boolean): string[] {
  const plateau = construirePlateau(tableADeuxJoueurs(), {
    playerId: 0,
    catalogue: catalogueVide,
    seulCeJoueur,
  })
  // Le bloc du joueur tient sur trois lignes depuis le 13/10/2026 (heros et
  // allies, soutiens, ameliorations : retour de Raven).
  const bandes = repartirEnBandes(plateau)
  return [bandes.heros.epinglee, ...bandes.heros.unites, ...bandes.soutiens.unites, ...bandes.ameliorations.unites].flatMap(
    (unite) => (unite ? [unite.carte.name] : [])
  )
}

describe('le bloc « Ton héros » en multijoueur', () => {
  it('montre la table des AUTRES joueurs quand seulCeJoueur est faux', () => {
    // Le garde-fou : c'est bien ce mode-la qui produisait le defaut. Si cette
    // assertion tombait, la suivante ne prouverait plus rien.
    expect(nomsDuBlocHeros(false)).toContain('* Hulk')
  })

  it('ne montre que le joueur regarde quand seulCeJoueur est vrai', () => {
    const noms = nomsDuBlocHeros(true)
    expect(noms).toContain('* Spider-Man')
    expect(noms).not.toContain('* Hulk')
    expect(noms).not.toContain('Allie de Hulk')
  })
})

describe('le cablage de board.tsx', () => {
  it('demande seulCeJoueur des que le plateau telephone est affiche', () => {
    const source = readFileSync('src/board.tsx', 'utf-8')
    // Le portrait ne deplie qu'un joueur : la vue « Auto » ne doit pas lui
    // faire poser toute la table.
    expect(source).toContain("seulCeJoueur: vueForcee !== null || modePlateau === 'mobile'")
  })
})
