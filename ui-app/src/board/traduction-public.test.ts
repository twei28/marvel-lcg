// Les copies JS de la traduction posée (deckbuilder, galerie) doivent rester
// identiques à une transpilation fraîche du TypeScript du plateau. Rouge ?
// Lancer `node outils/generer-traduction-public.mjs`.
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import { MODULES, transpiler } from '../../outils/generer-traduction-public.mjs'

const SORTIE = resolve(__dirname, '../../../Fusion/marvel-lcg-src/public/js/traduction')

describe('copies JS de la traduction posée', () => {
  for (const nom of MODULES as string[]) {
    it(`${nom}.js est à jour`, () => {
      expect(readFileSync(resolve(SORTIE, `${nom}.js`), 'utf8')).toBe(transpiler(nom))
    })
  }
  it('la feuille de style est à jour', () => {
    expect(readFileSync(resolve(SORTIE, 'traduction-posee.css'), 'utf8')).toBe(
      readFileSync(resolve(__dirname, 'traduction-posee.css'), 'utf8')
    )
  })
})
