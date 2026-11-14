// Binary (Galactic Storm, Kajislav, gs001a-gs240) : ce que la table DESSINE. Étape 8 bis de
// PROCESSUS-CARTE.md (lot GS-1, 20/10/2026).
//
// Touched (gs237), l'attachement némésis, se pose sur N'IMPORTE QUEL personnage : l'identité du
// joueur, un allié, le vilain ou un sbire, et Rogue (gs032) la déplace à chaque début de phase des
// joueurs. C'est la seule carte du pack qui pose une carte de RENCONTRE sur une carte du JOUEUR :
// `test_capacites` prouve que le moteur l'attache (cas `[binary] gs237`, `gs032`) ; ce fichier prouve
// que la table la montre, sous son porteur.
//
// ⚠ LES FIXTURES NE SONT PAS ÉCRITES À LA MAIN. Elles sortent du moteur (`ToDescriptor.World`, ce que
// sert `/get_world`) par les trois cas « [binary] gs237 ... etape 8 bis » de
// `Fusion/marvel-lcg-src/tools/cas/binary.py` (vérificateur `bn_fixture_plateau`), lancés avec
// BINARY_FIXTURE_DIR=<ce dossier>/__fixtures__. Les relancer pour les régénérer.
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { cartesDessinees, dessinee } from './plateau-de-test'
import type { World } from './world'

const ici = dirname(fileURLToPath(import.meta.url))
type Fixture = { monde: World; touched: number; porteur: number }
const lire = (nom: string) =>
  JSON.parse(readFileSync(join(ici, '__fixtures__', nom), 'utf8')) as Fixture

type CarteBrute = { id: number; card_id: string }
function idDe(monde: World, cardId: string): number {
  const pile: unknown[] = [monde]
  while (pile.length) {
    const n = pile.pop()
    if (Array.isArray(n)) pile.push(...n)
    else if (n && typeof n === 'object') {
      const c = n as Partial<CarteBrute>
      if (c.card_id === cardId && typeof c.id === 'number') return c.id
      pile.push(...Object.values(n))
    }
  }
  throw new Error(`${cardId} absent de la fixture`)
}

describe('Touched (gs237) sur la table', () => {
  it('posée sur BINARY : dessinée, portée par l identité', () => {
    const f = lire('binary-touched-heros.json')
    expect(dessinee(f.monde, f.touched)).toBeDefined()
    expect(dessinee(f.monde, f.touched)?.portePar).toBe(f.porteur)
    expect(f.porteur).toBe(idDe(f.monde, 'gs001a'))
  })

  it('posée sur un ALLIÉ (Hope Summers) : dessinée, portée par l allié', () => {
    const f = lire('binary-touched-allie.json')
    expect(dessinee(f.monde, f.touched)).toBeDefined()
    expect(dessinee(f.monde, f.touched)?.portePar).toBe(idDe(f.monde, '40204'))
  })

  it('posée sur le VILAIN (Rhino) : présente dans le monde, rattachée à Rhino', () => {
    const f = lire('binary-touched-vilain.json')
    expect(f.porteur).toBe(idDe(f.monde, '01094'))
    expect(idDe(f.monde, 'gs237')).toBe(f.touched)
  })
})

describe('le reste du pack en jeu côté joueur', () => {
  const f = lire('binary-touched-heros.json')
  const vues = cartesDessinees(f.monde)
  for (const cardId of ['gs009', 'gs007']) {
    it(`${cardId} est dessinée`, () => {
      expect(vues.some((c) => c.id === idDe(f.monde, cardId))).toBe(true)
    })
  }
})
