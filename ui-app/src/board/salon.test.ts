// Le tchat des comptes, vu depuis la table.
//
// Il existait deja, mais seulement sur l'ecran de PREPARATION
// (public/js/prepare/panneau-joueurs.js) : une fois la partie lancee, plus
// aucun moyen de se parler sans quitter le plateau.
//
// Le navigateur est servi depuis `p<N>.<domaine>` et le site depuis
// `<domaine>` : une requete directe serait croisee, et le cookie de session du
// site ne voyagerait pas. On parle donc au MOTEUR, qui relaie en 127.0.0.1 avec
// le jeton de la partie (/get_salon_joueurs, /post_salon_message).
//
// Ces routes repondent `{actif: false}` dans deux cas parfaitement normaux : le
// jeu tourne sans site derriere (partie locale), ou le siege n'est pas celui du
// titulaire du compte (un invite arrive par un lien de siege ne lit pas le tchat
// des comptes). Le plateau doit alors se taire, pas afficher une erreur.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { direSalon, lireSalon } from './salon'

const repondre = (donnees: unknown, ok = true) =>
  vi.fn().mockResolvedValue({
    ok,
    json: async () => donnees,
  } as Response)

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('lecture du salon', () => {
  it('rend les messages et le curseur du dernier lu', async () => {
    const fetch = repondre({
      actif: true,
      pseudo: 'arnaud',
      messages: [
        { id: 4, pseudo: 'chloe', texte: 'je joue Shuri', quand: '2026-09-05 21:30' },
        { id: 5, pseudo: 'arnaud', texte: 'ok', quand: '2026-09-05 21:31' },
      ],
      dernier: 5,
    })
    vi.stubGlobal('fetch', fetch)

    const vue = await lireSalon(3)

    expect(fetch).toHaveBeenCalledWith('/get_salon_joueurs?depuis=3', expect.anything())
    expect(vue.actif).toBe(true)
    expect(vue.pseudo).toBe('arnaud')
    expect(vue.messages.map((m) => m.texte)).toEqual(['je joue Shuri', 'ok'])
    expect(vue.dernier).toBe(5)
  })

  it('se tait quand il n y a pas de site derriere', async () => {
    vi.stubGlobal('fetch', repondre({ actif: false }))
    const vue = await lireSalon(0)
    expect(vue.actif).toBe(false)
    expect(vue.messages).toEqual([])
  })

  it('se tait aussi quand le moteur repond a cote', async () => {
    // Rien ici ne doit pouvoir casser le plateau : une partie continue meme si
    // le site tombe.
    vi.stubGlobal('fetch', repondre('pas du json attendu'))
    const vue = await lireSalon(0)
    expect(vue.actif).toBe(false)
  })

  it('se tait quand le reseau tombe', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('hors ligne')))
    const vue = await lireSalon(0)
    expect(vue.actif).toBe(false)
  })

  it('garde le curseur quand le moteur ne le renvoie pas', async () => {
    vi.stubGlobal('fetch', repondre({ actif: true, messages: [] }))
    const vue = await lireSalon(12)
    expect(vue.dernier).toBe(12)
  })

  it('ecarte une entree qui n a pas la forme d un message', async () => {
    vi.stubGlobal('fetch', repondre({
      actif: true,
      messages: [{ id: 1, pseudo: 'chloe', texte: 'vrai', quand: 'hier' }, { rien: true }, null],
      dernier: 1,
    }))
    const vue = await lireSalon(0)
    expect(vue.messages).toHaveLength(1)
  })
})

describe('envoi dans le salon', () => {
  it('poste le texte au moteur', async () => {
    const fetch = repondre({ ok: true })
    vi.stubGlobal('fetch', fetch)

    expect(await direSalon('bien joue')).toBe(true)

    const [url, options] = fetch.mock.calls[0] as [string, RequestInit]
    expect(url).toBe('/post_salon_message')
    expect(options.method).toBe('POST')
    expect(JSON.parse(String(options.body))).toEqual({ texte: 'bien joue' })
  })

  it('refuse d envoyer du vide', async () => {
    const fetch = repondre({ ok: true })
    vi.stubGlobal('fetch', fetch)
    expect(await direSalon('   ')).toBe(false)
    expect(fetch).not.toHaveBeenCalled()
  })

  it('rend faux quand le moteur refuse', async () => {
    vi.stubGlobal('fetch', repondre({ error: 'not the host' }, false))
    expect(await direSalon('coucou')).toBe(false)
  })
})
