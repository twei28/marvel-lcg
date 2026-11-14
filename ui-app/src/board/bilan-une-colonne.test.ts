// Le Bilan de fin de phase du méchant tient en UNE colonne : trois colonnes de 122 px coupaient les noms au milieu des
// mots (« Hel / ibo / und… ») à cause de `overflow-wrap: anywhere`. Verrou sur la feuille de style réelle (vu à l'écran
// avant/après le 09/11/2026).
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

const css = readFileSync(`${process.cwd()}/src/board/cartouche-tris.css`, 'utf8')
const base = readFileSync(`${process.cwd()}/src/board/cartouche-phase.css`, 'utf8')

describe('bilan de la phase du méchant', () => {
  it('une seule colonne pleine largeur', () => {
    expect(css).toMatch(/\.est-tris \.deroule-bilan \{[^}]*grid-template-columns:\s*minmax\(0, 1fr\)/s)
  })

  it('le chiffre passe sous le nom plutôt que de couper le mot', () => {
    expect(css).toMatch(/\.est-tris \.deroule-bilan \.deroule-lignes li \{[^}]*flex-wrap:\s*wrap/s)
    expect(css).toMatch(/\.est-tris \.deroule-bilan \.deroule-colonne-nom \{[^}]*overflow-wrap:\s*break-word/s)
  })

  it('témoin : la règle de base garde ses trois colonnes (autres cartouches inchangés)', () => {
    expect(base).toMatch(/\.deroule-bilan \{[^}]*repeat\(3, minmax\(0, 1fr\)\)/s)
  })
})
