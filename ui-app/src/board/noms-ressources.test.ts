// Ce que ce cas protège : le plateau nomme les ressources qui manquent au
// joueur (« Pay 1 mental resource(s) »). Il tirait ces noms d'une table écrite
// à la main, où B et Y étaient INVERSÉS par rapport au moteur : il annonçait
// « energy » quand il manquait une mentale, et l'inverse. Un joueur qui s'y
// fie construit un modèle faux de ses propres ressources.
//
// On ne recopie pas la bonne table ici : on la relit dans le MOTEUR. Une table
// recopiée peut diverger en silence, c'est exactement ce qui s'est produit.
import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ici = dirname(fileURLToPath(import.meta.url))

/** { r: 'physical', g: 'wild', b: 'mental', y: 'energy' } lu dans le moteur. */
function tableDuMoteur(): Record<string, string> {
  const source = readFileSync(
    join(ici, '../../../Fusion/marvel-lcg-src/src/game/element/resources.py'),
    'utf-8'
  )
  const ligne = /RES_TEXT[^=]*=\s*\{([^}]*)\}/.exec(source)
  if (!ligne) throw new Error('RES_TEXT introuvable dans resources.py')
  const table: Record<string, string> = {}
  for (const [, lettre, nom] of ligne[1].matchAll(/'(\w)':\s*Symbol\.r_\w_(\w+)/g)) {
    table[lettre.toUpperCase()] = nom
  }
  return table
}

/** La table du plateau, relue dans ask.ts. */
function tableDuPlateau(): Record<string, string> {
  const source = readFileSync(join(ici, 'ask.ts'), 'utf-8')
  const bloc = /const NOM_TYPE: Record<string, string> = \{([\s\S]*?)\n\}/.exec(source)
  if (!bloc) throw new Error('NOM_TYPE introuvable dans ask.ts')
  const table: Record<string, string> = {}
  for (const [, lettre, nom] of bloc[1].matchAll(/^\s*(\w):\s*'(\w+)'/gm)) {
    table[lettre] = nom
  }
  return table
}

describe('les noms de ressources', () => {
  it('le moteur en déclare bien quatre', () => {
    expect(Object.keys(tableDuMoteur()).sort()).toEqual(['B', 'G', 'R', 'Y'])
  })

  it('le plateau en déclare bien quatre', () => {
    expect(Object.keys(tableDuPlateau()).sort()).toEqual(['B', 'G', 'R', 'Y'])
  })

  it('le plateau dit exactement la même chose que le moteur', () => {
    expect(tableDuPlateau()).toEqual(tableDuMoteur())
  })

  it('et B est bien mental, pas energy', () => {
    // Le cas précédent suffirait, mais celui-ci nomme l'erreur trouvée le
    // 9/8/2026 : elle reviendrait sans bruit si quelqu'un « corrigeait » la
    // table du plateau au jugé.
    expect(tableDuPlateau().B).toBe('mental')
    expect(tableDuPlateau().Y).toBe('energy')
  })
})
