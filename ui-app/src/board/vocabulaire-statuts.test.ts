// LE VOCABULAIRE OFFICIEL DES ÉTATS ET DE LEURS MOTS-CLÉS, TENU PAR UNE GATE.
//
// Audit du 30/09/2026 (Guide de référence v1.8 en français) :
//   Stunned = Sonné · Confused = Désorienté · Tough (carte d'état) = Tenace
//   Toughness = Ténacité · Stalwart = Robuste · Steady = Solide
// 77 textes fan-made s'en écartaient (« étourdi », « carte de statut
// Robuste », « Inébranlable », « Résistance », « Stable »…), et le badge du
// plateau appelait la carte Tough « Robuste », le nom de Stalwart. Un joueur
// lisait donc « Robuste » pour deux règles différentes.
import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { TEXTES_FR_FANMADE } from './textes-fr-fanmade'
import { libelleStatut } from './effets-statuts'

const ici = dirname(fileURLToPath(import.meta.url))

function textesAnglais(): Map<string, string> {
  const textes = new Map<string, string>()
  const parcourir = (o: unknown): void => {
    if (Array.isArray(o)) {
      o.forEach(parcourir)
      return
    }
    if (o && typeof o === 'object') {
      const carte = o as { card_id?: unknown; text?: unknown }
      if (typeof carte.card_id === 'string' && 'text' in carte) {
        textes.set(carte.card_id, typeof carte.text === 'string' ? carte.text : '')
        return
      }
      Object.values(o).forEach(parcourir)
    }
  }
  for (const fichier of ['cards.json', 'cards_custom.json']) {
    try {
      parcourir(JSON.parse(readFileSync(join(ici, '../../../Fusion/marvel-lcg-src/data', fichier), 'utf-8')))
    } catch {
      // cards_custom.json peut manquer sur une copie de travail.
    }
  }
  return textes
}

const ATTENDUS: Array<[RegExp, RegExp, string]> = [
  [/\bstalwart\b/i, /Robuste/, 'Stalwart → Robuste'],
  [/\bsteady\b/i, /Solide/, 'Steady → Solide'],
  [/\btoughness\b/i, /T[ée]nacit[ée]/, 'Toughness → Ténacité'],
  [/\btough\b/i, /Tenace/, 'tough → Tenace'],
]
const INTERDITS = [/Robustesse/, /Inébranlable/, /(statut|état) Robuste/, /Résistance\./, /[ée]tourdi/i]

describe('vocabulaire officiel des états', () => {
  it('chaque texte fan-made emploie les termes officiels', () => {
    const anglais = textesAnglais()
    const ecarts: string[] = []
    for (const [id, fr] of Object.entries(TEXTES_FR_FANMADE)) {
      if (!fr) continue
      for (const interdit of INTERDITS) if (interdit.test(fr)) ecarts.push(`${id} : ${interdit}`)
      const en = anglais.get(id)
      if (!en) continue
      for (const [motEn, motFr, libelle] of ATTENDUS) {
        if (motEn.test(en) && !motFr.test(fr)) ecarts.push(`${id} : manque ${libelle}`)
      }
    }
    expect(ecarts).toEqual([])
  })

  it('le badge de la carte Tough dit Tenace, pas Robuste', () => {
    expect(libelleStatut('tough', 1, 'fr')).toBe('Tenace')
  })
})
