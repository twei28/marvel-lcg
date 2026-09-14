// La gate des traductions : aucune clé affichée ne peut rester sans anglais.
//
// ⚠ POURQUOI ELLE EXISTE. `t()` rend la CLÉ telle quelle quand le dictionnaire
// ne la connaît pas : une clé oubliée ne plante pas, ne rougit pas, elle
// affiche simplement du français au milieu d'un plateau anglais. Soixante et
// une clés étaient dans ce cas le 14/09/2026, dont le bouton « Partie » de la
// barre. Signalé par l'utilisateur : « en anglais, dans le header, il y a
// marqué Partie. C'est n'importe quoi. »
//
// ⚠ ET LE DÉFAUT EST INVISIBLE À QUI JOUE EN FRANÇAIS, c'est-à-dire à nous.
// C'est exactement le genre de chose qu'un test doit garder, parce que
// personne ne la verra en travaillant.
//
// ⚠ ON LIT LES SOURCES, PAS UNE LISTE TENUE À LA MAIN. Une liste se périme au
// premier `t()` ajouté ; le scan, non.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { DICO_EN_BASE } from './dico-en'

const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

/** La valeur d'un littéral TypeScript en guillemets simples, échappements résolus. */
function litteralResolu(brut: string): string {
  try {
    return JSON.parse(`"${brut.replace(/\\'/g, "'").replace(/"/g, '\\"')}"`) as string
  } catch {
    // Un échappement que JSON ne connaît pas : on garde le littéral, quitte à
    // signaler un manquant de trop. Mieux vaut un faux positif qu'un trou.
    return brut
  }
}

/** Chaque `t('...')` écrit dans le code du plateau, hors tests. */
function clesUtilisees(): Map<string, string[]> {
  const cles = new Map<string, string[]>()
  const parcourir = (dossier: string) => {
    for (const entree of fs.readdirSync(dossier, { withFileTypes: true })) {
      const chemin = path.join(dossier, entree.name)
      if (entree.isDirectory()) {
        parcourir(chemin)
        continue
      }
      if (!/\.tsx?$/.test(entree.name) || /\.test\.tsx?$/.test(entree.name)) continue
      const source = fs.readFileSync(chemin, 'utf8')
      // ⚠ SEULEMENT LES LITTÉRAUX. `t(variable)` et `t(\`gabarit\`)` ne se
      // vérifient pas statiquement : les compter ici produirait de faux
      // manquants, et la gate serait désarmée par le bruit.
      for (const m of source.matchAll(/\bt\(\s*'((?:[^'\\]|\\.)*)'\s*\)/g)) {
        // ⚠ ON COMPARE LA CHAÎNE À L'EXÉCUTION, pas le littéral écrit. Le code
        // contient des échappements (`l\u2019emporte`, `\n`) : c'est le
        // caractère résolu que `t()` reçoit, et donc la clé du dictionnaire.
        // Comparer les littéraux donnait six faux manquants.
        const cle = litteralResolu(m[1])
        const ou = cles.get(cle) ?? []
        ou.push(path.relative(RACINE, chemin))
        cles.set(cle, ou)
      }
    }
  }
  parcourir(RACINE)
  return cles
}

describe('le dictionnaire anglais couvre tout ce qui s’affiche', () => {
  it('⚠ aucune clé du plateau ne reste sans traduction', () => {
    const utilisees = clesUtilisees()
    const manquantes = [...utilisees.entries()]
      .filter(([cle]) => !(cle in DICO_EN_BASE))
      .map(([cle, ou]) => `${JSON.stringify(cle)} (${ou[0]})`)
    expect(manquantes, `${manquantes.length} clé(s) sans anglais`).toEqual([])
  })

  it('le scan trouve bien des clés : la gate n’est pas vide', () => {
    // Témoin. Une expression régulière cassée rendrait zéro clé, et le cas
    // ci-dessus passerait au vert sans rien vérifier.
    expect(clesUtilisees().size).toBeGreaterThan(400)
  })

  it('la clé signalée par l’utilisateur est bien traduite', () => {
    expect(DICO_EN_BASE['Partie']).toBe('Game')
  })
})
