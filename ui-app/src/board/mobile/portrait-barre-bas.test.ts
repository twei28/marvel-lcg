// Defaut bloquant recette (11/09/2026), mesure a 500x844 dans Chrome.
//
// La barre du bas du portrait reutilise telle quelle `actionsPartie`, la barre
// du plateau PC (`.board-actions`, voir board.tsx). Deux consequences :
//
// 1. DEBORDEMENT. `.board-actions` porte `flex-shrink: 0` (board.css, couche
//    `base`) : elle refuse de retrecir. Mesuree a 1055 px de large dans une
//    barre de 500 ; Sauver, Historique, Options et Fin du tour tombaient hors
//    ecran. `flex-wrap: wrap` seul ne suffit PAS (verifie en direct dans
//    Chrome : 1063 -> 693, toujours dehors) : le passage a la ligne ne se
//    declenche que si le conteneur accepte d'abord de retrecir. Il faut donc
//    `flex: 1 1 auto` EN PLUS du wrap.
// 2. DOUBLON. Son `.bh-etat` ecrit « Round 1 / Tour de Steve Rogers / A toi de
//    jouer », mot pour mot ce que `.portrait-bandeau` affiche deja en haut de
//    l'ecran. Sur telephone la place ne permet pas de le dire deux fois.
//
// Mesure apres correction : `.board-actions` 8 -> 492, barre 0 -> 500, bandeau
// 0 -> 500, plus rien hors du cadre horizontal.
//
// POURQUOI `!important`, qui n'est normalement pas de mise ici : la
// declaration d'ordre `@layer socle, legacy, base, composants, utilitaires;`
// de styles/tokens.css DISPARAIT du bundle de production (verifie : elle ne
// figure dans aucun public/app/assets/*.css). L'ordre reel redevient celui de
// la premiere apparition de chaque nom, soit « composants, utilitaires,
// socle, base, legacy ». `base` bat donc `composants` ET `utilitaires`, et la
// surcharge perdait contre la declaration `flex: 0 0 auto` que board.css
// pose sur `.board-actions`
// (flex-shrink calcule mesure a 0 dans Chrome, malgre la regle presente et
// matchee dans le CSSOM). `!important` inverse l'ordre des couches et repasse
// devant. A retirer le jour ou l'ordre sera retabli au build.
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

describe('la barre du bas du portrait, qui reutilise .board-actions du plateau PC', () => {
  it('laisse la barre PC retrecir au lieu de la laisser sortir de l\'ecran', () => {
    expect(bloc('.portrait-bas .board-actions')).toContain('flex: 1 1 auto !important')
  })

  it('la fait passer a la ligne une fois qu\'elle accepte de retrecir', () => {
    expect(bloc('.portrait-bas .board-actions')).toContain('flex-wrap: wrap')
  })

  it('masque le .bh-etat de la barre PC, deja affiche par le bandeau du haut', () => {
    expect(bloc('.portrait-bas .bh-etat')).toContain('display: none !important')
  })
})
