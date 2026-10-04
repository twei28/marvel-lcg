// La garde des ESSAIS : c'est le serveur qui decide, jamais le client.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `un serveur muet ne donne pas les essais` :
// hors ligne, moteur lance a la main, route absente, le repli doit etre
// « ferme ». Un repli « ouvert » donnerait un ecran en chantier a tout le
// monde, ce qui est exactement ce que cette garde existe pour empecher.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { essaisOuverts as essaisDe, estHoteLocal, oublierEssais } from './essais'

// ⚠ jsdom sert les tests depuis `localhost` : sans hote explicite, tous les
// cas ci-dessous tomberaient dans l'exception locale.
const essaisOuverts = () => essaisDe('p1.exemple.test')

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

describe('en local, les essais sont ouverts comme en ligne pour l administrateur', () => {
  beforeEach(() => oublierEssais())
  afterEach(() => {
    vi.unstubAllGlobals()
    oublierEssais()
  })

  it('un moteur lance sur la machine ouvre les essais sans demander au serveur', async () => {
    const appels = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ url: '' }) })
    vi.stubGlobal('fetch', appels)
    expect(await essaisDe('127.0.0.1')).toBe(true)
    expect(appels).not.toHaveBeenCalled()
  })

  it('seules les adresses de la machine comptent', () => {
    expect(estHoteLocal('localhost')).toBe(true)
    expect(estHoteLocal('[::1]')).toBe(true)
    // Un sous-domaine qui commence pareil n'est PAS la machine.
    expect(estHoteLocal('localhost.exemple.test')).toBe(false)
    expect(estHoteLocal('123.discordsays.com')).toBe(false)
    expect(estHoteLocal('')).toBe(false)
  })
})
