// Le test qui manquait, et dont l'absence a laisse passer TROIS bugs de suite
// sur ce chantier : le vilain invisible, le nemesis range sous « Engagés », et
// la vue « Auto » qui montre la table des autres joueurs.
//
// Tous les autres tests du portrait fabriquent leur `Plateau` a la main, avec
// un cast. Le typage verifie alors que les cles existent dans
// `CleEmplacement` ; il ne peut RIEN dire de ce que chaque emplacement
// contient vraiment. Or c'est exactement la ou les trois bugs vivaient.
//
// Ici on monte un vrai monde et on appelle `construirePlateau`, via
// `plateau-de-test.ts` ecrit pour ce motif precis.

import { describe, expect, it } from 'vitest'
import { catalogueVide } from '../catalogue'
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import { construirePlateau } from '../zones'
import { repartirEnBlocs } from './blocs-portrait'

/** Une table de solo : un vilain, une manigance, un allie, un sbire engage. */
function tableSolo() {
  const vilain = carteSurTable(1, '01096', 'EncounterVillain', 'Rhino')
  const manigance = carteSurTable(2, '01097a', 'MainScheme', 'The Break-In!')
  const heros = carteSurTable(3, '01001a', 'Hero', '* Spider-Man')
  const allie = carteSurTable(4, '01006', 'Ally', 'Aunt May')
  const sbire = carteSurTable(5, '01099', 'Minion', 'Rhino Thug')
  // Le set nemesis est une liste PLATE de cartes (zones.ts le passe a `piles`,
  // qui en tire un representant) : un tableau de tableaux ne produit rien.
  const nemesis = carteSurTable(6, 'zz901', 'Minion', 'Le nemesis mis de cote')
  return tableAvec(
    siege({ area_hero: [heros], allies: [allie], engaged_enemies: [sbire], set_aside_nemesis_sets: [nemesis] }),
    { area_villain: [vilain], area_schemes_main: [manigance] }
  )
}

function blocsDe(world: ReturnType<typeof tableSolo>, playerId = 0) {
  const plateau = construirePlateau(world, { playerId, catalogue: catalogueVide })
  const blocs = repartirEnBlocs(plateau)
  const noms = (cle: string) =>
    blocs.find((bloc) => bloc.cle === cle)?.unites.map((unite) => unite.carte.name) ?? []
  return { blocs, noms }
}

describe('la repartition en blocs, sur un plateau reellement construit', () => {
  it('met le mechant dans « Méchant »', () => {
    expect(blocsDe(tableSolo()).noms('vilain')).toContain('Rhino')
  })

  it('met la manigance principale dans « Manigances »', () => {
    expect(blocsDe(tableSolo()).noms('complot')).toContain("L'Effraction !")
  })

  it('met l\'allie avec le heros, pas avec les ennemis', () => {
    const { noms } = blocsDe(tableSolo())
    // « Tante May » et non « Aunt May » : le nom passe par la VF officielle
    // depuis le 11/09/2026 (noms-cartes-fr.ts).
    expect(noms('heros')).toContain('Tante May')
    expect(noms('engages')).not.toContain('Tante May')
  })

  it('met le sbire engage dans « Engagés »', () => {
    expect(blocsDe(tableSolo()).noms('engages')).toContain('Rhino Thug')
  })

  it('ne range PAS le set nemesis mis de cote sous « Engagés »', () => {
    // Il est hors jeu : l'y montrer laisse croire qu'il est sur la table.
    // C'est le « Baron Zemo » releve a la recette du 11/09/2026.
    expect(blocsDe(tableSolo()).noms('engages')).not.toContain('Le nemesis mis de cote')
  })

  it('rend toujours les six blocs, meme vides', () => {
    const { blocs } = blocsDe(tableSolo())
    expect(blocs.map((bloc) => bloc.cle)).toEqual([
      'vilain',
      'complot',
      'rencontre',
      'engages',
      'heros',
      'main',
    ])
  })
})
