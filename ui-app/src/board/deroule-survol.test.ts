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
    // Sur la CARTE, pas sur le conteneur : un padding sur `.apercu-face`
    // tombe apres le texte et ne le pousse pas (verifie au rendu).
    expect(CSS).toContain('.carte-apercu .scan-card:has(.jauge-carte)')
    expect(bloc('.carte-apercu .scan-card:has(.jauge-carte)')).toContain(
      'margin-bottom: var(--jauge-debord)'
    )
  })
})

describe('les decorations des cartes de la scene', () => {
  // ⚠ `.deroule-jeton` A DISPARU DE LA LISTE (15/09/2026). Le jeton se posait
  // sur la carte visee ; le cartouche ne dessine plus l'auteur ni sa cible
  // (« arrete de montrer les cartes »), et un jeton n'a pas de sens pose sur
  // rien. Le nombre est dans la phrase et dans le compteur.
  it.each(['.deroule-carte-legende'])(
    '%s ne prend pas le pointeur',
    (selecteur) => {
      expect(bloc(selecteur)).toContain('pointer-events: none')
    }
  )

  // L'inverse, et c'est le defaut du 12/09/2026 : la CARTE, elle, doit garder
  // le pointeur. `.deroule-carte .scan-card { pointer-events: none }` (« ni
  // curseur, ni survol ») faisait tomber la souris sur la figure, jamais sur
  // `.scan-card`, et la loupe ne s'ouvrait plus sur aucune carte de la scene.
  // Mesure dans Chrome : `elementFromPoint` au centre de la carte rendait
  // `figure.deroule-carte`, et un `mouseover` envoye directement a la carte
  // ouvrait bien la loupe.
  it('la carte elle-meme garde le pointeur, sinon la loupe est morte', () => {
    expect(bloc('.deroule-carte .scan-card')).not.toContain('pointer-events')
  })
})
