// @vitest-environment node
// Garde : aucun script du site (pages hors plateau) ne doit avoir une erreur de syntaxe.
//
// Une fusion avait laisse quatre accolades fermantes de moins dans `prepare/heros-info.js` : le
// navigateur refusait le module entier, l'ecran de preparation ne se chargeait plus, et aucun test
// unitaire ne le voyait puisque personne n'importait ce fichier. Seul un test Playwright de creation
// de campagne a rougi, loin de la cause.
import { describe, expect, it } from 'vitest'
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { transformSync } from 'esbuild'

const racine = join(dirname(fileURLToPath(import.meta.url)), '../../Fusion/marvel-lcg-src/public/js')

function scripts(dossier: string): string[] {
  return readdirSync(dossier).flatMap((nom) => {
    const chemin = join(dossier, nom)
    if (statSync(chemin).isDirectory()) return scripts(chemin)
    return nom.endsWith('.js') ? [chemin] : []
  })
}

describe('scripts du site', () => {
  it('chaque fichier de public/js se lit (syntaxe)', () => {
    const fautes: string[] = []
    for (const chemin of scripts(racine)) {
      try {
        transformSync(readFileSync(chemin, 'utf-8'), { loader: 'js', format: 'esm' })
      } catch (e) {
        fautes.push(`${chemin.slice(racine.length + 1)} : ${String((e as Error).message).split('\n')[0]}`)
      }
    }
    expect(fautes).toEqual([])
  })
})
