// La garde des ESSAIS : c'est le serveur qui decide, jamais le client.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `un serveur muet ne donne pas les essais` :
// hors ligne, moteur lance a la main, route absente, le repli doit etre
// « ferme ». Un repli « ouvert » donnerait un ecran en chantier a tout le
// monde, ce qui est exactement ce que cette garde existe pour empecher.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { essaisOuverts, oublierEssais } from './essais'

describe('les essais ne s ouvrent que si le serveur le dit', () => {
  beforeEach(() => oublierEssais())
  afterEach(() => {
    vi.unstubAllGlobals()
    oublierEssais()
  })

  const repond = (valeur: unknown, ok = true) =>
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok, json: async () => valeur }))

  it('une adresse d administration ouvre les essais', async () => {
    repond({ url: 'https://exemple.test/admin' })
    expect(await essaisOuverts()).toBe(true)
  })

  it('une adresse vide les laisse fermes', async () => {
    // C'est la reponse que le moteur fait a TOUT LE MONDE sauf l'administrateur.
    repond({ url: '' })
    expect(await essaisOuverts()).toBe(false)
  })

  it('un serveur muet ne donne pas les essais', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('hors ligne')))
    expect(await essaisOuverts()).toBe(false)
  })

  it('une reponse qui n est pas du JSON ne les donne pas non plus', async () => {
    // ⚠ Le moteur sert une IMAGE pour tout chemin inconnu : sur un serveur
    // d'avant cette route, la reponse est un JPEG en 200.
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: async () => { throw new SyntaxError('ce n est pas du json') },
    }))
    expect(await essaisOuverts()).toBe(false)
  })

  it('une reponse en erreur les laisse fermes', async () => {
    repond({ url: 'https://exemple.test/admin' }, false)
    expect(await essaisOuverts()).toBe(false)
  })

  it('la question n est posee QU UNE FOIS', async () => {
    // Le plateau se redessine plusieurs fois par seconde : demander a chaque
    // rendu noierait le serveur pour une reponse qui ne change jamais.
    const appels = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ url: 'x' }) })
    vi.stubGlobal('fetch', appels)
    await Promise.all([essaisOuverts(), essaisOuverts(), essaisOuverts()])
    await essaisOuverts()
    expect(appels).toHaveBeenCalledTimes(1)
  })
})
