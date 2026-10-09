// Copie JS, pour le deckbuilder et la galerie (pages hors plateau), des modules
// du plateau qui servent la traduction posée sur les scans. Une seule source,
// le TypeScript du plateau : ces fichiers sont TRANSPILÉS, jamais édités.
// Gardé par src/board/traduction-public.test.ts.
//
// Usage : node outils/generer-traduction-public.mjs
import { readFileSync, writeFileSync, copyFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import ts from 'typescript'

const ICI = dirname(fileURLToPath(import.meta.url))
const BOARD = resolve(ICI, '../src/board')
const SORTIE = resolve(ICI, '../../Fusion/marvel-lcg-src/public/js/traduction')
export const MODULES = [
  'traduction-posee', 'traits-fr', 'textes-fr', 'textes-fr-fanmade', 'scans-fr-liste',
  'zones-arts-alternatifs', 'textes-fr-complets',
]

export function transpiler(nom) {
  const source = readFileSync(resolve(BOARD, `${nom}.ts`), 'utf8')
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.ES2020, target: ts.ScriptTarget.ES2020, removeComments: false },
  })
  // Les imports relatifs du plateau (« ./traits-fr ») visent ici leur jumeau .js.
  const js = outputText.replace(/from '\.\/([\w-]+)'/g, "from './$1.js'")
  return `// GÉNÉRÉ par ui-app/outils/generer-traduction-public.mjs depuis ui-app/src/board/${nom}.ts — NE PAS ÉDITER.\n${js}`
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  for (const nom of MODULES) writeFileSync(resolve(SORTIE, `${nom}.js`), transpiler(nom), 'utf8')
  copyFileSync(resolve(BOARD, 'traduction-posee.css'), resolve(SORTIE, 'traduction-posee.css'))
  console.log(`${MODULES.length} modules et la feuille de style écrits dans ${SORTIE}`)
}
