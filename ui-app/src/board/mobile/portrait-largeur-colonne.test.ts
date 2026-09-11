// Defaut bloquant recette (11/09/2026) : mesure a 500x844 dans Chrome, tout le
// plateau faisait 855 px de large. `.plateau-portrait` est fixe a la taille de
// l'ecran (`position: fixed; inset: 0`, mesure 500 px), mais son enfant
// `.portrait-table` mesurait 855 px : le nom des cartes debordait a droite,
// et la colonne des chiffres ("14 / 14 PV") se retrouvait a x = 763 -> 843,
// invisible.
//
// Cause : `.plateau-portrait` ne declare que `grid-template-rows`. La grille
// n'a donc AUCUNE colonne explicite et cree une colonne implicite, dimensionnee
// par `grid-auto-columns: auto`. Une piste `auto` se resout sur le max-content
// de son contenu AVANT la repartition de la place libre : elle grandit
// au-dela du conteneur au lieu d'y etre bornee. `min-width: 0` sur l'enfant
// n'y change rien (verifie en direct dans Chrome : toujours 855 px) parce que
// ce n'est pas l'enfant qui refuse de retrecir, c'est la PISTE qui est trop
// large. Il faut donc borner la piste elle-meme.
//
// `minmax(0, 1fr)` la borne a la largeur du conteneur (le 0 en minimum annule
// a son tour le plancher min-content de la piste). Mesure Chrome apres
// correction : plateau 500, table 500, scrollWidth 500, plus aucun
// debordement horizontal hors de la main, qui defile de son cote par
// conception.
//
// jsdom ne fait pas de mise en page : on verrouille la REGLE dans la feuille,
// comme portrait-table-defilement.test.ts.

import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

// Chemin depuis la racine d'ui-app, comme les tests voisins de ce dossier.
const CSS = readFileSync('src/board/mobile/portrait.css', 'utf-8')

/** Les declarations d'un selecteur, sans les regles voisines. */
function bloc(selecteur: string): string {
  const debut = CSS.indexOf(`\n  ${selecteur} {`)
  expect(debut, `selecteur absent de portrait.css : ${selecteur}`).toBeGreaterThan(-1)
  return CSS.slice(debut, CSS.indexOf('}', debut))
}

describe('.plateau-portrait (grille du plateau telephone)', () => {
  it('borne sa colonne a la largeur de l\'ecran au lieu de la laisser grandir au max-content', () => {
    expect(bloc('.plateau-portrait')).toContain('grid-template-columns: minmax(0, 1fr)')
  })
})
