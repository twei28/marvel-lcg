// « Quitter la partie » ferme la table, et le plateau doit le dire avant.
//
// ⚠ POURQUOI CE MODULE EXISTE. Le bouton ne faisait que naviguer vers
// `/prepare.html` : le moteur gardait son monde chargé, l'emplacement restait
// pris, et le salon des invités — qui bascule dès que la table porte UNE
// partie — expédiait les arrivants sur l'ANCIENNE avant même qu'ils aient
// choisi leur héros. Deux soirées perdues les 19 et 20/09/2026.
//
// ⚠ ET LE DANGER EST LA PAGE MORTE. Une seconde après la fermeture, le moteur
// n'existe plus : toute adresse qu'il servirait (`/prepare.html`, `/`) serait
// morte avec lui. Le seul atterrissage valable est celui que le SITE donne.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { fermerLaTable, laTableVaSeFermer, urlDuSite } from './quitter-la-table'

const SITE = 'https://exemple.test'

afterEach(() => {
  vi.unstubAllGlobals()
})

/** Une réponse HTTP minimale, comme `fetch` la rend. */
function reponse(corps: unknown, ok = true): Response {
  return { ok, json: async () => corps } as Response
}

describe('qui ferme la table, et qui ne fait que partir', () => {
  it('l’hôte d’une table du site la ferme', () => {
    expect(laTableVaSeFermer({ siege: 0, spectateur: false, urlSite: SITE })).toBe(true)
  })

  it('⚠ un INVITÉ ne ferme pas la table de l’hôte', () => {
    // Le moteur le refuserait de toute façon (403), mais c'est ici que se
    // décide ce qu'on lui ANNONCE : lui promettre la fermeture serait un
    // mensonge, et lui promettre les autres déconnectés, une frayeur.
    expect(laTableVaSeFermer({ siege: 1, spectateur: false, urlSite: SITE })).toBe(false)
  })

  it('un spectateur ne ferme rien non plus', () => {
    expect(laTableVaSeFermer({ siege: 0, spectateur: true, urlSite: SITE })).toBe(false)
  })

  it('sans site derrière, il n’y a aucune table à rendre', () => {
    // Partie locale (JOUER-SOLO.bat) : personne ne tient d'emplacement, et
    // `/prepare.html` reste vivant puisque le moteur ne s'éteint pas.
    expect(laTableVaSeFermer({ siege: 0, spectateur: false, urlSite: '' })).toBe(false)
  })
})

describe('l’adresse du site', () => {
  it('se lit auprès du moteur, qui seul la connaît', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ url: SITE })))
    expect(await urlDuSite()).toBe(SITE)
    expect(fetch).toHaveBeenCalledWith('/get_site_url')
  })

  it('est vide quand le moteur tourne sans site', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ url: '' })))
    expect(await urlDuSite()).toBe('')
  })

  it('est vide, et non une exception, quand la lecture échoue', async () => {
    // Un réseau qui hoquette ne doit pas laisser le joueur sans réponse : il
    // verra la confirmation prudente, et rien ne sera détruit.
    vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('coupé') }))
    expect(await urlDuSite()).toBe('')
  })
})

describe('fermer la table', () => {
  it('le demande au moteur, en POST', async () => {
    vi.stubGlobal('fetch', vi.fn(async () =>
      reponse({ eteinte: true, url: SITE + '/arret' })))
    const depart = await fermerLaTable()
    expect(fetch).toHaveBeenCalledWith('/quitter_la_table', expect.objectContaining({
      method: 'POST',
    }))
    expect(depart).toEqual({ eteinte: true, url: SITE + '/arret' })
  })

  it('⚠ ne déclare RIEN fermé sans adresse où atterrir', async () => {
    // La gate, et elle n'est pas théorique : annoncer la fermeture sans lieu
    // où renvoyer le joueur le laisserait sur une page du moteur qu'on vient
    // de tuer. Pas d'adresse, pas de fermeture.
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ eteinte: true, url: '' })))
    expect(await fermerLaTable()).toEqual({ eteinte: false, url: '' })
  })

  it('un refus du moteur ne ferme rien', async () => {
    // 403 : ce siège n'est pas celui de l'hôte.
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ error: 'not the host' }, false)))
    expect(await fermerLaTable()).toEqual({ eteinte: false, url: '' })
  })

  it('un moteur injoignable ne ferme rien, et ne jette pas', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('coupé') }))
    expect(await fermerLaTable()).toEqual({ eteinte: false, url: '' })
  })
})
