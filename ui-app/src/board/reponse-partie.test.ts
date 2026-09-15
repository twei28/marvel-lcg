// « LA REPONSE EST-ELLE PARTIE ? » — CE QUE `repondre` DIT MAINTENANT.
//
// Defaut trouve en relecture le 15/09/2026 : `Moteur.repondre` attrapait
// l'erreur reseau, gardait la demande et ne publiait qu'une erreur, sans rien
// rendre (`Promise<void>`). Le panneau de la manigance laissait donc son
// bouton `disabled` pour toujours : plus aucun moyen de renvoyer, partie
// figee sur la face A.
//
// La porte est desormais un FAIT rendu par le moteur : `true` quand le POST
// est parti, `false` quand il a echoue. Aucune minuterie, aucune devinette.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Moteur } from './moteur'

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('Moteur.repondre', () => {
  it('⚠ REND FALSE quand l’envoi echoue : le bouton doit pouvoir rouvrir', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => {
        throw new Error('Failed to fetch')
      })
    )

    const moteur = new Moteur(0)
    await expect(moteur.repondre({ id: 7, targets: [], resources: [] })).resolves.toBe(false)
  })

  it('rend true quand le POST est parti', async () => {
    // La relecture qui suit echoue ici (elle interroge le serveur de partie,
    // absent d'un test) : elle est attrapee par `lire`, et ne change rien au
    // fait qui nous interesse — la REPONSE, elle, est bien partie.
    const fetchSimule = vi.fn(async (url: unknown) => {
      if (typeof url === 'string' && url.startsWith('/post')) {
        return { ok: true, text: async () => '' } as unknown as Response
      }
      throw new Error('pas de serveur de partie dans un test')
    })
    vi.stubGlobal('fetch', fetchSimule)

    const moteur = new Moteur(0)
    await expect(moteur.repondre({ id: 7, targets: [], resources: [] })).resolves.toBe(true)
    expect(fetchSimule).toHaveBeenCalled()
  })
})
