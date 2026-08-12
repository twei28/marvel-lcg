// Un joueur qui REJOINT n'a jamais posé la clé `mc-campagne-partie` : c'est
// l'écran des campagnes qui l'écrit, et il ne l'ouvre pas. Son plateau doit
// donc demander au serveur, qui le déduit de la partie en cours.
//
// Le localStorage reste prioritaire : l'hôte l'a, il est juste, et il évite un
// aller-retour réseau à chaque fin de partie.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CLE_CAMPAGNE, lireContexte, resoudreContexte } from './contexte'

beforeEach(() => window.localStorage.clear())
afterEach(() => vi.unstubAllGlobals())

function serveurRend(charge: unknown, ok = true) {
  const fetchFeint = vi.fn().mockResolvedValue({ ok, json: async () => charge })
  vi.stubGlobal('fetch', fetchFeint)
  return fetchFeint
}

describe('le contexte de campagne', () => {
  it('préfère le localStorage et ne touche pas au réseau', async () => {
    const fetchFeint = serveurRend({ id: 'autre', scenario: 'autre' })
    window.localStorage.setItem(
      CLE_CAMPAGNE,
      JSON.stringify({ id: 'trors-1', scenario: 'crossbones' })
    )

    expect(await resoudreContexte()).toEqual({ id: 'trors-1', scenario: 'crossbones' })
    expect(fetchFeint).not.toHaveBeenCalled()
  })

  it('interroge le serveur quand la clé est absente', async () => {
    serveurRend({ id: 'trors-1', scenario: 'crossbones' })
    expect(await resoudreContexte()).toEqual({ id: 'trors-1', scenario: 'crossbones' })
  })

  it("rend null quand le serveur dit qu'aucune campagne n'est en cours", async () => {
    serveurRend({})
    expect(await resoudreContexte()).toBeNull()
  })

  it('rend null quand le serveur est injoignable', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('coupé')))
    expect(await resoudreContexte()).toBeNull()
  })

  it('rend null sur une réponse HTTP en erreur', async () => {
    serveurRend({ id: 'trors-1', scenario: 'crossbones' }, false)
    expect(await resoudreContexte()).toBeNull()
  })

  it('rend null sur une réponse incomplète', async () => {
    serveurRend({ id: 'trors-1' })
    expect(await resoudreContexte()).toBeNull()
  })

  it('laisse lireContexte purement locale', () => {
    // Le rapport de bug s'en sert : il se prend au clic et ne doit pas
    // attendre le réseau.
    serveurRend({ id: 'trors-1', scenario: 'crossbones' })
    expect(lireContexte()).toBeNull()
  })
})
