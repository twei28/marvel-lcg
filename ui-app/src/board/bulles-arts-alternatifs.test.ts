// Les bulles de stats (THW, ATK, DEF, REC) se posent sur les stats imprimees
// de l'image AFFICHEE. Un art alternatif (cb, m3t, rog, rog2) les place
// ailleurs que la carte officielle : les positions doivent etre cherchees
// avec l'id de cet art, et chaque art livre doit avoir les siennes.
import fs from 'node:fs'
import path from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { STAT_BUBBLE_POSITIONS } from '../components/stat-bubbles/positions'
import { catalogueVide } from './catalogue'
import { carteSurTable } from './plateau-de-test'

const MOTEUR = path.join(__dirname, '..', '..', '..', 'Fusion', 'marvel-lcg-src')
const LABELS: Record<string, string[]> = { Hero: ['THW', 'ATK', 'DEF'], AlterEgo: ['REC'] }

function typesOfficiels(): Map<string, { type: string; labels: string[] }> {
  const donnees = JSON.parse(fs.readFileSync(path.join(MOTEUR, 'data', 'cards.json'), 'utf8')) as Record<string, unknown>
  const cartes = new Map<string, { type: string; labels: string[] }>()
  for (const paquet of Object.values(donnees)) {
    if (!Array.isArray(paquet)) continue
    for (const c of paquet as Array<{ card_id?: string; type?: string; desc?: Record<string, string> }>) {
      if (!c.card_id || !c.type || !LABELS[c.type] || !c.desc) continue
      const labels = LABELS[c.type].filter((l) => c.desc?.[l] && /\d/.test(c.desc[l]))
      if (labels.length) cartes.set(c.card_id, { type: c.type, labels })
    }
  }
  return cartes
}

describe('bulles de stats des arts alternatifs de heros et d\'alter-egos', () => {
  const officielles = typesOfficiels()
  const arts = fs
    .readdirSync(path.join(MOTEUR, 'assets', 'pics'))
    .map((f) => /^(\d{5}[ab])_(cb|m3t|rog2?)\.jpg$/.exec(f))
    .filter((m): m is RegExpExecArray => m !== null && officielles.has(m[1]))

  it('il y a des arts alternatifs a verifier', () => {
    expect(arts.length).toBeGreaterThan(100)
  })

  it('chaque art alternatif a une position pour chacune de ses stats', () => {
    const manques: string[] = []
    for (const [, officiel, style] of arts) {
      const id = `${officiel}_${style}`
      const pos = STAT_BUBBLE_POSITIONS[id] ?? {}
      for (const label of officielles.get(officiel)!.labels) {
        if (!pos[label as keyof typeof pos]) manques.push(`${id}:${label}`)
      }
    }
    expect(manques).toEqual([])
  })

  it('les positions d\'un art alternatif different de celles de la carte officielle', () => {
    const differents = arts.filter(([, officiel, style]) => {
      const alt = STAT_BUBBLE_POSITIONS[`${officiel}_${style}`]
      const off = STAT_BUBBLE_POSITIONS[officiel]
      return alt && off && JSON.stringify(alt) !== JSON.stringify(off)
    })
    expect(differents.length).toBeGreaterThan(50)
  })
})

describe('toScanCard, l\'id des positions', () => {
  const CLE_ART = 'mc_hero_art_v1'
  const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })

  async function toScanCardAvecArt(choix: Record<string, string>) {
    window.localStorage.setItem(CLE_ART, JSON.stringify(choix))
    vi.resetModules()
    return (await import('./card-model')).toScanCard
  }

  beforeEach(() => window.localStorage.removeItem(CLE_ART))
  afterEach(() => window.localStorage.removeItem(CLE_ART))

  it('garde l\'id officiel quand aucun art alternatif n\'est choisi', async () => {
    const scan = await toScanCardAvecArt({})
    expect(scan(carteSurTable(1, '01001a', 'Hero', 'Spider-Man'), contexte()).picId).toBe('01001a')
  })

  it('donne l\'id de l\'art affiche, pas celui de la carte officielle', async () => {
    const scan = await toScanCardAvecArt({ '01001': 'cb' })
    const rendu = scan(carteSurTable(1, '01001a', 'Hero', 'Spider-Man'), contexte())
    expect(rendu.picId).toBe('01001a_cb')
    expect(rendu.imageUrl).toContain('01001a_cb')
  })
})
