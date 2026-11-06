// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest'
import { heureLocale, transportMoteur, type MessageTchat } from './tchat'

afterEach(() => {
  vi.unstubAllGlobals()
})

function reponseJson(corps: unknown, ok = true): Response {
  return { ok, json: async () => corps } as unknown as Response
}

describe('heureLocale', () => {
  it('rend la chaine brute sans quandTs', () => {
    const m: MessageTchat = { id: 1, pseudo: 'A', texte: 'x', quand: '21:30' }
    expect(heureLocale(m)).toBe('21:30')
  })

  it('convertit quandTs dans le fuseau du lecteur', () => {
    const m: MessageTchat = { id: 1, pseudo: 'A', texte: 'x', quand: '21:30', quandTs: 1700000000 }
    expect(heureLocale(m)).toMatch(/\d{1,2}:\d{2}/)
  })
})

describe('transportMoteur — lire', () => {
  it('fil general : demande sans salon=table, traduit quand_ts et prives', async () => {
    const fetchSimule = vi.fn(async (url: string) => {
      expect(url).toContain('/get_salon_joueurs?')
      expect(url).not.toContain('salon=table')
      return reponseJson({
        actif: true,
        pseudo: 'moi',
        messages: [{ id: 5, pseudo: 'moi', texte: 'salut', quand: '21:30', quand_ts: 1700000000 }],
        dernier: 5,
        prives: { bob: 3 },
      })
    })
    vi.stubGlobal('fetch', fetchSimule)
    const vue = await transportMoteur().lire('general', 0)
    expect(vue.actif).toBe(true)
    expect(vue.pseudo).toBe('moi')
    expect(vue.messages[0].quandTs).toBe(1700000000)
    expect(vue.prives).toEqual({ bob: 3 })
  })

  it('fil table : demande salon=table', async () => {
    const fetchSimule = vi.fn(async (url: string) => {
      expect(url).toContain('salon=table')
      return reponseJson({ actif: true, messages: [], dernier: 0 })
    })
    vi.stubGlobal('fetch', fetchSimule)
    await transportMoteur().lire('table', 0)
    expect(fetchSimule).toHaveBeenCalled()
  })

  it('reponse non ok ou actif:false : muet, jamais d’exception', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponseJson({}, false)))
    const vue = await transportMoteur().lire('general', 7)
    expect(vue).toEqual({ actif: false, messages: [], dernier: 7 })
  })

  it('fetch qui leve : muet, jamais d’exception', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('reseau coupe') }))
    const vue = await transportMoteur().lire('general', 3)
    expect(vue.actif).toBe(false)
  })
})

describe('transportMoteur — dire', () => {
  it('texte vide : rien envoye', async () => {
    const fetchSimule = vi.fn()
    vi.stubGlobal('fetch', fetchSimule)
    const ok = await transportMoteur().dire('general', '   ')
    expect(ok).toBe(false)
    expect(fetchSimule).not.toHaveBeenCalled()
  })

  it('fil table : pose salon=table et un siege dans le corps', async () => {
    const fetchSimule = vi.fn(async (_url: string, init: RequestInit) => {
      const corps = JSON.parse(init.body as string)
      expect(corps.salon).toBe('table')
      expect(typeof corps.siege).toBe('number')
      return reponseJson({ ok: true })
    })
    vi.stubGlobal('fetch', fetchSimule)
    const ok = await transportMoteur().dire('table', 'salut la table')
    expect(ok).toBe(true)
  })

  it('fil prive : pose le destinataire', async () => {
    const fetchSimule = vi.fn(async (_url: string, init: RequestInit) => {
      const corps = JSON.parse(init.body as string)
      expect(corps.a).toBe('bob')
      return reponseJson({ ok: true })
    })
    vi.stubGlobal('fetch', fetchSimule)
    await transportMoteur().dire('prive', 'coucou', 'bob')
  })
})
