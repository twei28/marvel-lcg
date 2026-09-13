// Les trois emplacements de sauvegarde appartiennent A UNE TABLE, pas au serveur.
//
// ⚠ LE DEFAUT CORRIGE LE 13/09/2026, ET IL ETAIT GRAVE. Le plateau ecrivait
// « ../replays/save_1.json » en dur : le dossier COMMUN, le meme pour tout le
// monde. Sur un serveur a vingt places, les trois emplacements etaient donc
// PARTAGES entre tous les comptes — chacun ecrasait la sauvegarde du voisin, et
// chargeait des parties qu'il n'avait jamais jouees.
//
// Signale par un joueur (« j'ai charge un truc que je n'ai jamais fait »), puis
// confirme en production : `replays/save_1..3.json` existaient a la racine
// pendant que les dossiers `replays/serveur-N/` de chacun restaient vides.
//
// La configuration disait pourtant la verite depuis toujours (`replay_folders`,
// separe par place dans tools/config_serveur.py) : c'est le client qui
// inventait un chemin au lieu de la lire.
import { describe, expect, it, vi, afterEach } from 'vitest'
import { dossierSauvegardes, cheminEmplacement } from './sauvegardes'

function repond(corps: unknown, ok = true) {
  return vi.fn().mockResolvedValue({ ok, json: async () => corps } as unknown as Response)
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('dossier de sauvegardes', () => {
  it('vient du moteur, pas du client', async () => {
    const appel = repond({ dossier: '../replays/serveur-9/' })
    vi.stubGlobal('fetch', appel)
    expect(await dossierSauvegardes()).toBe('../replays/serveur-9/')
    expect(appel).toHaveBeenCalledWith('/get_dossier_sauvegardes', { cache: 'no-store' })
  })

  // ⚠ LE CAS QUI COMPTE : deux tables differentes ne doivent JAMAIS tomber sur
  // le meme fichier. C'est tout le defaut, en une ligne.
  it('deux tables ne partagent pas un emplacement', async () => {
    vi.stubGlobal('fetch', repond({ dossier: '../replays/serveur-9/' }))
    const chezYarro = await cheminEmplacement(1)
    vi.stubGlobal('fetch', repond({ dossier: '../replays/serveur-3/' }))
    const chezUnAutre = await cheminEmplacement(1)
    expect(chezYarro).not.toBe(chezUnAutre)
    expect(chezYarro).toBe('../replays/serveur-9/save_1.json')
  })

  it('les trois emplacements d une meme table sont distincts', async () => {
    vi.stubGlobal('fetch', repond({ dossier: '../replays/serveur-2/' }))
    const chemins = [await cheminEmplacement(1), await cheminEmplacement(2),
                     await cheminEmplacement(3)]
    expect(new Set(chemins).size).toBe(3)
  })

  // Partie locale : il n'y a qu'un joueur, donc personne a ecraser.
  it('sans moteur pour repondre, on retombe sur le dossier local', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('hors ligne')))
    expect(await cheminEmplacement(2)).toBe('../replays/save_2.json')
  })

  it('un moteur qui refuse ne fait pas inventer un chemin vide', async () => {
    vi.stubGlobal('fetch', repond({}, false))
    expect(await cheminEmplacement(1)).toBe('../replays/save_1.json')
  })

  it('un dossier sans barre finale en recoit une', async () => {
    vi.stubGlobal('fetch', repond({ dossier: '../replays/serveur-4' }))
    // Le moteur la pose deja, mais le client ne doit pas produire un chemin
    // colle si jamais elle manquait.
    expect(await cheminEmplacement(1)).toContain('serveur-4')
  })
})
