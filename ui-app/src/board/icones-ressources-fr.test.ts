// Ce que ce cas protège : la traduction française des cartes fan-made est
// écrite à la main, à côté du texte anglais du catalogue. Le 9/8/2026, quatre
// cartes du pack Lockjaw annonçaient une ressource [wild] là où le scan montre
// une [mental]. Le correctif devait toucher DEUX fichiers ; ne corriger que le
// catalogue aurait laissé le joueur francophone lire l'ancienne consigne, donc
// payer la carte de travers sans jamais comprendre pourquoi le bonus n'arrive
// pas.
//
// On ne juge pas ici quelle icône est la bonne : aucun test ne peut lire un
// scan. On exige seulement que les deux textes disent LA MÊME CHOSE.
import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ici = dirname(fileURLToPath(import.meta.url))
const RESSOURCES = ['physical', 'mental', 'energy', 'wild']

/** Les icônes de ressource d'un texte, triées, doublons compris. */
function icones(texte: string): string[] {
  return [...texte.matchAll(/\[([a-z]+)\]/g)]
    .map((m) => m[1])
    .filter((nom) => RESSOURCES.includes(nom))
    .sort()
}

/** Les textes anglais du catalogue, par card_id. */
function textesAnglais(): Record<string, string> {
  const brut = readFileSync(
    join(ici, '../../../Fusion/marvel-lcg-src/data/cards.json'),
    'utf-8'
  )
  const catalogue = JSON.parse(brut) as Record<string, unknown>
  const textes: Record<string, string> = {}
  for (const cartes of Object.values(catalogue)) {
    if (!Array.isArray(cartes)) continue
    for (const carte of cartes as Array<Record<string, unknown>>) {
      const id = carte.card_id
      const texte = carte.text
      if (typeof id === 'string' && typeof texte === 'string') textes[id] = texte
    }
  }
  return textes
}

/** Les textes français faits main, par card_id. */
function textesFrancais(): Record<string, string> {
  const source = readFileSync(join(ici, 'textes-fr-fanmade.ts'), 'utf-8')
  const textes: Record<string, string> = {}
  for (const [, id, texte] of source.matchAll(/^\s*'([^']+)': "((?:[^"\\]|\\.)*)",?$/gm)) {
    textes[id] = texte
  }
  return textes
}

describe('les icônes de ressource des traductions fan-made', () => {
  const fr = textesFrancais()
  const en = textesAnglais()

  it('le fichier français est bien relu', () => {
    // Sans ce garde-fou, une expression régulière cassée rendrait zéro carte
    // et le cas suivant passerait au vert en ne comparant rien.
    expect(Object.keys(fr).length).toBeGreaterThan(300)
  })

  it('chaque carte annonce les mêmes ressources en français et en anglais', () => {
    const ecarts: string[] = []
    for (const [id, texte] of Object.entries(fr)) {
      if (!(id in en)) continue
      const a = icones(texte)
      const b = icones(en[id])
      if (a.join(',') !== b.join(',')) ecarts.push(`${id} : FR [${a}] vs EN [${b}]`)
    }
    expect(ecarts).toEqual([])
  })

  it('et les quatre cartes Lockjaw demandent bien une mentale', () => {
    // Elles nomment l'erreur trouvée le 9/8/2026 : le cas précédent la
    // laisserait revenir si les deux fichiers repassaient à [wild] ensemble.
    for (const id of ['lj001a', 'lj009', 'lj010', 'lj011']) {
      expect(icones(fr[id])).toContain('mental')
      expect(icones(en[id])).toContain('mental')
    }
  })
})
