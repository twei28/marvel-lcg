// Defaut bloquant recette (11/09/2026) : mesure a 500x844 dans Chrome,
// `.main-portrait` (908 -> 1087) et la barre du bas (1093 -> 1144) tombaient
// hors ecran (844 px de haut), invisibles. Cause : `.portrait-table` occupe
// la rangee `1fr` de la grille `.plateau-portrait` (auto 1fr auto) sans
// aucune regle qui lui soit propre. Un enfant de grille garde
// `min-height: auto` par defaut : il refuse de retrecir sous la hauteur de
// son contenu, la rangee `1fr` grandit alors au-dela de l'ecran et pousse la
// main + la barre hors champ ; `overflow: hidden` sur `.plateau-portrait` les
// rogne alors en silence.
//
// PIEGE de diagnostic evite ici : `document.documentElement.scrollHeight`
// restait egal a `innerHeight` (844 = 844) sur la mesure fautive, ce qui
// donnait l'illusion que tout tenait. C'est faux : la page ne defilait pas
// parce que le contenu etait ROGNE, pas parce qu'il tenait. Seules les
// positions (`getBoundingClientRect`) l'ont montre — jsdom ne fait pas de
// mise en page et ne peut donc pas rejouer cette mesure : on verrouille la
// REGLE dans la feuille, comme deroule-survol.test.ts et
// portrait-deroule-phase.test.ts.

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

describe('.portrait-table (rangee du milieu de la grille .plateau-portrait)', () => {
  it('accepte de retrecir sous la hauteur de son contenu (annule min-height: auto)', () => {
    expect(bloc('.portrait-table')).toContain('min-height: 0')
  })

  it('defile en interne quand la table deborde, au lieu de pousser la main et la barre hors ecran', () => {
    expect(bloc('.portrait-table')).toContain('overflow-y: auto')
  })
})
