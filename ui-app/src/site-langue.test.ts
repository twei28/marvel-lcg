// LA GATE DES TRADUCTIONS DU SITE — celle qui manquait.
//
// ⚠ POURQUOI ELLE EXISTE. Le PLATEAU est gardé depuis le 14/09/2026
// (`board/dico-en.test.ts`, écrite après que soixante et une clés se sont
// affichées en français sur un écran anglais). Le SITE — le wizard de
// préparation, la galerie, la campagne, la reprise, le deck-builder — a son
// propre `t()` et son propre dictionnaire (`public/js/prepare/dico-en.js`), et
// n'avait AUCUN contrôle. Mesure du 15/09/2026 : 580 appels littéraux, dont
// **89 sans anglais**.
//
// ⚠ ET LE DÉFAUT EST INVISIBLE À QUI JOUE EN FRANÇAIS, c'est-à-dire à nous.
// `t()` rend la clé telle quelle quand le dictionnaire ne la connaît pas : rien
// ne plante, rien ne rougit, l'écran affiche simplement du français.
//
// ⚠ ON LIT LES SOURCES, PAS UNE LISTE TENUE À LA MAIN. Une liste se périme au
// premier `t()` ajouté ; le scan, non. Même principe que la gate du plateau.
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { describe, expect, it } from 'vitest'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const SITE = path.resolve(ICI, '../../Fusion/marvel-lcg-src/public/js')
const DICO = path.join(SITE, 'prepare/dico-en.js')

/** Le code d'un fichier, commentaires ôtés.
 *
 *  ⚠ LES COMMENTAIRES D'ABORD. Ce projet commente en français, apostrophes
 *  comprises : « l'étape » ouvre une chaîne qui se referme à l'apostrophe
 *  suivante, et un scan naïf y lit des dizaines de libellés inexistants.
 */
function codeSeul(fichier: string): string {
  return fs
    .readFileSync(fichier, 'utf8')
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/^\s*\/\/.*$/gm, '')
}

/**
 * Les clés déclarées dans un code : `'clé': 'valeur'` ou `"clé": "valeur"`.
 *
 * ⚠ ON RÉSOUT LES ÉCHAPPEMENTS, comme le fait la gate du plateau. Une clé qui
 * contient une apostrophe s'écrit `'l\'autre'` dans la source, mais c'est
 * `l'autre` que `t()` reçoit. Comparer les littéraux donnait quatre manquants
 * imaginaires — tous français, tous à apostrophe.
 */
function clesDeclarees(source: string): Set<string> {
  const cles = new Set<string>()
  const ajouter = (brut: string) => cles.add(brut.replace(/\\"/g, '"').replace(/\\'/g, "'"))
  for (const m of source.matchAll(/^\s*"((?:[^"\\]|\\.)*)"\s*:/gm)) ajouter(m[1])
  for (const m of source.matchAll(/^\s*'((?:[^'\\]|\\.)*)'\s*:/gm)) ajouter(m[1])
  return cles
}

/**
 * Le dictionnaire COMMUN du site.
 *
 * ⚠ IL N'EST PAS LE SEUL, et l'ignorer donne une gate qui crie au loup. Trois
 * mécanismes coexistent, découverts en mesurant :
 *   1. `DICO_EN_BASE` (prepare/dico-en.js), commun à tout le site ;
 *   2. `enregistrerTraductions({…})`, qui AJOUTE au commun depuis un écran
 *      (galerie, panneau des documents, panneau de bug) ;
 *   3. `DICO_EN_LOCAL = {…}`, un dictionnaire PRIVÉ à un fichier, avec son
 *      propre `t()` (reprise, lien-galerie, lien-admin).
 * Une première version ne lisait que le premier et annonçait 89 clés sans
 * anglais : la plupart étaient traduites, ailleurs.
 */
function clesConnues(): Set<string> {
  return clesDeclarees(codeSeul(DICO))
}

/** Les clés qu'un fichier traduit LUI-MÊME (mécanismes 2 et 3 ci-dessus). */
function clesDuFichier(source: string): Set<string> {
  const cles = new Set<string>()
  for (const bloc of source.matchAll(/(?:enregistrerTraductions\(|DICO_EN_LOCAL\s*=\s*)\{([\s\S]*?)\n\s*\}/g)) {
    for (const cle of clesDeclarees(bloc[1])) cles.add(cle)
  }
  return cles
}

/** Chaque `t('…')` écrit en toutes lettres dans les scripts du site. */
function clesUtilisees(): Map<string, string[]> {
  const cles = new Map<string, string[]>()
  const parcourir = (dossier: string) => {
    for (const entree of fs.readdirSync(dossier, { withFileTypes: true })) {
      const chemin = path.join(dossier, entree.name)
      if (entree.isDirectory()) {
        parcourir(chemin)
        continue
      }
      if (!entree.name.endsWith('.js') || entree.name.includes('dico-en')) continue
      const source = codeSeul(chemin)
      const locales = clesDuFichier(source)
      // ⚠ SEULEMENT LES LITTÉRAUX, comme la gate du plateau. `t(variable)` ne se
      // vérifie pas statiquement : le compter ici produirait de faux manquants,
      // et la gate serait désarmée par le bruit.
      for (const m of source.matchAll(/\bt\(\s*(["'])((?:(?!\1)[^\\]|\\.)*)\1\s*\)/g)) {
        const cle = m[2].replace(/\\"/g, '"').replace(/\\'/g, "'")
        // Traduite sur place par cet écran : rien à demander au commun.
        if (locales.has(cle)) continue
        const ou = cles.get(cle) ?? []
        ou.push(path.relative(SITE, chemin).replace(/\\/g, '/'))
        cles.set(cle, ou)
      }
    }
  }
  parcourir(SITE)
  return cles
}

describe('⚠ les fichiers du site se chargent VRAIMENT', () => {
  // ⚠ CE CAS EXISTE PARCE QUE J'AI CASSÉ LE SITE, le 15/09/2026, en ajoutant
  // les traductions ci-dessous : une DOUBLE VIRGULE laissée par le script qui
  // les a écrites. `dico-en.js` ne se parsait plus, donc plus rien ne se
  // chargeait — wizard, galerie, campagne et deck-builder muets d'un coup.
  //
  // ⚠ ET LE CONTRÔLE DE LANGUE DISAIT VERT. Il comptait les lignes françaises
  // à l'écran : une page morte n'en affiche aucune. Un écran vide passait donc
  // pour un écran parfaitement traduit. C'est le pire genre de vert.
  //
  // `node --check` ne l'avait pas vu non plus : il lit le fichier comme du
  // CommonJS. Il faut l'IMPORTER comme le navigateur le fait.
  it('le dictionnaire du site se parse comme un vrai module', () => {
    // ⚠ ON LE FAIT PARSER PAR NODE, DANS SON PROPRE PROCESSUS, et non par un
    // `import()` du test : le bundler de tests intercepte les imports
    // dynamiques et ne résout pas un chemin hors de son périmètre. Un
    // sous-processus fait exactement ce que fait le navigateur.
    const script = `import(${JSON.stringify(pathToFileURL(DICO).href)})` +
      `.then((m) => { if (!m.DICO_EN_BASE) { console.error('SANS DICO_EN_BASE'); process.exit(2) }` +
      ` console.log(Object.keys(m.DICO_EN_BASE).length) })` +
      `.catch((e) => { console.error(e.message); process.exit(1) })`
    const sortie = execFileSync(process.execPath, ['--input-type=module', '-e', script], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    })
    expect(Number(sortie.trim()), 'le dictionnaire du site rend trop peu de clés').toBeGreaterThan(100)
  })
})

describe('le dictionnaire anglais couvre tout ce que le SITE affiche', () => {
  it('⚠ aucune clé du site ne reste sans traduction', () => {
    const connues = clesConnues()
    const manquantes = [...clesUtilisees()]
      .filter(([cle]) => !connues.has(cle))
      .map(([cle, ou]) => `« ${cle} » (${[...new Set(ou)].join(', ')})`)
      .sort()
    expect(
      manquantes,
      `${manquantes.length} clé(s) du site s'afficheraient en FRANÇAIS sur un ` +
        `écran anglais :\n  ${manquantes.join('\n  ')}`
    ).toEqual([])
  })

  it('le dictionnaire du site est vraiment lu', () => {
    // Garde-fou du garde-fou : si le chemin change, le test ci-dessus
    // passerait au vert en ne trouvant plus aucun appel.
    expect(clesConnues().size).toBeGreaterThan(100)
    expect(clesUtilisees().size).toBeGreaterThan(100)
  })
})
