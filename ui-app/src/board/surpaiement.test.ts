// Ce que ces cas protègent : une carte à COÛT X ne fait rien si le joueur ne
// dépense rien pour elle. Le plateau ne le lui rappelait que si le texte
// contenait « overpay », formule absente des neuf cartes à coût X du
// catalogue. Signalé en jeu sur Tendril Explosion (vr006) : la carte semblait
// cassée alors qu'elle est correcte, et son cas de comportement passait.
import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { construire } from './catalogue'

const catalogue = (cartes: unknown[]) => construire({ paquet: cartes })

describe('surpayable', () => {
  it('reconnait le texte « overpay », comme avant', () => {
    const c = catalogue([
      { card_id: '01001', text: 'for each resource you overpaid for this cost' },
    ])
    expect(c.surpayable('01001')).toBe(true)
  })

  it('reconnait un COÛT X, dont le texte ne dit jamais « overpay »', () => {
    const c = catalogue([
      { card_id: 'vr006', desc: { Cost: 'X' }, text: 'Hero Action: Deal X damage to each enemy.' },
    ])
    expect(c.surpayable('vr006')).toBe(true)
  })

  it('ne signale pas une carte à coût fixe', () => {
    const c = catalogue([
      { card_id: 'vr007', desc: { Cost: '2' }, text: 'Deal 5 damage to an enemy.' },
    ])
    expect(c.surpayable('vr007')).toBe(false)
  })
})

// Le catalogue réel, pas un échantillon : c'est la seule façon de savoir que
// la règle attrape bien TOUTES les cartes concernées du jeu.
describe('le catalogue réel', () => {
  const cartes = (() => {
    const ici = dirname(fileURLToPath(import.meta.url))
    const base = join(ici, '../../../Fusion/marvel-lcg-src/data')
    const sortie: Array<Record<string, unknown>> = []
    for (const nom of ['cards.json', 'cards_custom.json']) {
      const brut = JSON.parse(readFileSync(join(base, nom), 'utf-8')) as Record<string, unknown[]>
      for (const liste of Object.values(brut)) {
        for (const c of liste) if (c && typeof c === 'object') sortie.push(c as Record<string, unknown>)
      }
    }
    return sortie
  })()

  it('a bien été chargé', () => {
    expect(cartes.length).toBeGreaterThan(4000)
  })

  it('les neuf cartes à coût X sont toutes surpayables', () => {
    const c = construire({ paquet: cartes })
    const coutX = cartes.filter(
      (x) => (x.desc as Record<string, string> | undefined)?.Cost === 'X'
    )
    expect(coutX.length).toBeGreaterThanOrEqual(9)
    const oubliees = coutX
      .map((x) => String(x.card_id))
      .filter((id) => !c.surpayable(id))
    expect(oubliees).toEqual([])
  })
})
