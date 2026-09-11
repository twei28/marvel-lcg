// Les DECORATIONS posees sur une carte de la scene ne doivent pas prendre le
// pointeur.
//
// Mesure dans Chrome (11/09/2026) : le jeton « +1 » fait 64x64 en haut a
// droite de la carte, la legende « Boost +1 » court sous elle, et
// `document.elementFromPoint` y rend le jeton ou la legende, jamais la carte.
// Or le survol de la scene cherche `closest('.scan-card')` (apercu-survol.ts) :
// survoler cette zone fermait la loupe au lieu de l'ouvrir. Capture de
// l'utilisateur : la carte revelee, son triangle jaune, et rien en grand.
//
// jsdom ne fait ni mise en page ni test de recouvrement : ce cas ne peut pas
// se jouer en rendu. On verrouille donc la REGLE dans la feuille, comme
// noms-ressources.test.ts verrouille une table dans sa source.

import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

// Chemin depuis la racine d'ui-app, comme noms-ressources.test.ts : sous le
// transform de vitest, `import.meta.url` n'est pas une URL de fichier.
const CSS = readFileSync('src/board/board.css', 'utf-8')

/** Les declarations d'un selecteur, sans les regles voisines. */
function bloc(selecteur: string): string {
  const debut = CSS.indexOf(`\n  ${selecteur} {`)
  expect(debut, `selecteur absent de board.css : ${selecteur}`).toBeGreaterThan(-1)
  return CSS.slice(debut, CSS.indexOf('}', debut))
}

describe('l’aperçu d’une carte', () => {
  it('reserve la place que la jauge deborde sous le cadre', () => {
    // La jauge sort du cadre par une marge negative (ScanCard.css) : le flux ne
    // reserve pas ce debord, et le bandeau Crise passait dessous. Mesure dans
    // Chrome : 12 px de chevauchement avant, 0 apres. jsdom ne fait pas de mise
    // en page, on verrouille donc la regle dans la feuille.
    expect(CSS).toContain('.carte-apercu .apercu-face:has(.jauge-carte)')
    expect(bloc('.carte-apercu .apercu-face:has(.jauge-carte)')).toContain(
      'padding-bottom: var(--jauge-debord)'
    )
  })
})

describe('les decorations des cartes de la scene', () => {
  it.each(['.deroule-jeton', '.deroule-carte-legende'])(
    '%s ne prend pas le pointeur',
    (selecteur) => {
      expect(bloc(selecteur)).toContain('pointer-events: none')
    }
  )
})
