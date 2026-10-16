// @vitest-environment node
// L'import d'un deck par lien : MarvelCDB et MC4DB (public/js/marvelcdb/sources.js, 16/10/2026).
import { describe, it, expect } from 'vitest'
// @ts-expect-error module JS servi tel quel, sans types
import { lireLien, chargerDeck } from '../../Fusion/marvel-lcg-src/public/js/marvelcdb/sources.js'

type Rep = { ok: boolean; status: number; json: () => Promise<unknown> }
const rep = (status: number, corps: unknown = {}): Rep => ({ ok: status < 400, status, json: async () => corps })
/** Un faux reseau : `table` associe une adresse a sa reponse (ou `'panne'`) ; chaque appel est note. */
function reseau(table: Record<string, Rep | 'panne'>) {
  const appels: string[] = []
  const chercher = async (u: string) => {
    appels.push(u)
    const r = table[u]
    if (!r || r === 'panne') throw new Error('hors ligne')
    return r
  }
  return { appels, chercher }
}

describe('lireLien', () => {
  it('reconnait le site, le numero et la forme', () => {
    expect(lireLien('https://marvelcdb.com/decklist/view/123/nom')).toMatchObject({ id: '123', decklist: true, site: { cle: 'marvelcdb' } })
    expect(lireLien('https://mc4db.merlindumesnil.net/decklist/view/45')).toMatchObject({ id: '45', decklist: true, site: { cle: 'mc4db' } })
    expect(lireLien('https://marvelcdb.com/deck/view/777')).toMatchObject({ id: '777', decklist: false, site: { cle: 'marvelcdb' } })
    expect(lireLien('4321')).toMatchObject({ id: '4321', site: null })
    expect(lireLien('rien').id).toBe('')
  })
})

describe('chargerDeck', () => {
  const M = 'https://marvelcdb.com/api/public'
  const C = 'https://mc4db.merlindumesnil.net/api/public'

  it('un lien MC4DB ne questionne que MC4DB', async () => {
    const { appels, chercher } = reseau({ [`${C}/decklist/9.json`]: rep(200, { name: 'x' }) })
    const r = await chargerDeck('https://mc4db.merlindumesnil.net/decklist/view/9', chercher)
    expect(r.site.cle).toBe('mc4db')
    expect(appels.every((u) => u.startsWith(C))).toBe(true)
  })

  it('un lien MarvelCDB ne questionne jamais MC4DB, meme en panne', async () => {
    const { appels, chercher } = reseau({})
    expect(await chargerDeck('https://marvelcdb.com/decklist/view/9', chercher)).toBeNull()
    expect(appels.every((u) => u.startsWith(M))).toBe(true)
  })

  it('un numero nu : MarvelCDB d\'abord, MC4DB seulement si MarvelCDB est en panne', async () => {
    const panne = reseau({ [`${C}/decklist/555.json`]: rep(200, { name: 'chez merlin' }) })
    const r = await chargerDeck('555', panne.chercher)
    expect(r.site.cle).toBe('mc4db')
    expect(panne.appels[0].startsWith(M)).toBe(true)
  })

  it('un numero nu introuvable chez MarvelCDB (404) ne va PAS chez MC4DB : autre numerotation', async () => {
    const { appels, chercher } = reseau({
      [`${M}/decklist/555.json`]: rep(404), [`${M}/deck/555.json`]: rep(404),
      [`${C}/decklist/555.json`]: rep(200, { name: 'un autre deck' }),
    })
    expect(await chargerDeck('555', chercher)).toBeNull()
    expect(appels.some((u) => u.startsWith(C))).toBe(false)
  })

  it('un lien /deck/ essaie la forme deck avant decklist', async () => {
    const { appels, chercher } = reseau({ [`${M}/deck/8.json`]: rep(200, { name: 'perso' }) })
    const r = await chargerDeck('https://marvelcdb.com/deck/view/8', chercher)
    expect(r.data.name).toBe('perso')
    expect(appels[0]).toBe(`${M}/deck/8.json`)
  })

  it('MC4DB refuse les decks prives (403) : introuvable, sans plantage', async () => {
    const { chercher } = reseau({ [`${C}/decklist/3.json`]: rep(404), [`${C}/deck/3.json`]: rep(403) })
    expect(await chargerDeck('https://mc4db.merlindumesnil.net/deck/view/3', chercher)).toBeNull()
  })
})
