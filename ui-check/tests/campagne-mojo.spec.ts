// MojoMania, la campagne en trois scenarios : de la fin de Magog au panneau de recompenses.
//
// Ce que ce test prouve, dans une VRAIE fin de partie et le VRAI panneau (jamais sur des formes) :
//
// * le moteur releve, a la fin de Magog, les soutiens et ameliorations ELIGIBLES de chaque joueur
//   (`Player N Eligible Support / Upgrade`, cout imprime 3 ou moins tant que The Champion est du cote BOOING
//   CROWD, jamais une carte plus chere) ;
// * le panneau les PROPOSE comme des cartes cliquables, et rien d'autre ;
// * la carte cochee est ecrite au carnet de la campagne (`Player 1 Support / Upgrade #1`), et la cle de travail
//   « Eligible … » n'y est PAS recopiee ;
// * Longshot, absent du jeu a la fin, n'est pas note ; les sets modulaires de la partie sont cumules.
//
//   npm run campagne-mojo      (ou : UI_CHECK_BASE=http://127.0.0.1:2399 npx playwright test tests/campagne-mojo.spec.ts --project=pc)
//
// ATTENTION : ce test lance de VRAIES parties. Toute partie en cours sur le serveur vise est perdue.
import { test, expect } from '@playwright/test'
import {
  acheverLaPartie,
  lancer,
  nettoyer,
  ouvrirEtMettreEnPlace,
  poserCampagne,
  relireCampagne,
  repondre,
} from '../pilote-campagne'

const NOM = 'Essai automatique - mojomania'

/** Helicarrier et Tac Team : soutiens a cout 3 d'Iron Man. Avengers Mansion : cout 4, JAMAIS propose. */
const COUT_3 = ['01092', '01056']
const COUT_4 = '01091'

test.describe.serial('Campagne MojoMania', () => {
  test.setTimeout(240000)

  let identifiant = ''

  test.beforeAll(async ({ request }) => {
    await nettoyer(request, NOM)
  })

  test.afterAll(async ({ request }) => {
    if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
  })

  test('la boite figure parmi les campagnes definies', async ({ request }) => {
    const liste = (await (await request.get('/list_campagnes_definies?')).json()) as Array<{ code?: string }>
    expect(liste.map((c) => c.code), 'MojoMania doit etre proposee a la creation.').toContain('mojo')
  })

  test('Magog : le panneau propose les soutiens eligibles, et la carte cochee va au carnet', async ({ page, request }) => {
    identifiant = await poserCampagne(request, {
      code: 'mojo',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'iron_man', nomHeros: 'Iron Man' }],
      termines: [],
      carnet: {},
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem('mc-campagne-partie', JSON.stringify({ id, scenario: 'magog' }))
    }, identifiant)

    // « Modular Sets This Scenario » : ce que l'ecran de campagne pose au lancement.
    await lancer(request, { scenario: 'magog', heros: ['iron_man'], carnet: { 'Modular Sets This Scenario': 'crime' } })
    await ouvrirEtMettreEnPlace(page, request)

    for (const id of [...COUT_3, COUT_4]) {
      await request.get('/debug?' + encodeURIComponent(`PutIntoPlay("${id}")`))
      for (let i = 0; i < 3; i++) {
        await repondre(request)
        await page.waitForTimeout(300)
      }
    }

    const m = await acheverLaPartie(page, request, 'Win()', 40)
    expect(m.players_won, 'La partie devait etre gagnee (Win()).').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    const champ = page.locator('.camp-champ', { hasText: /Soutien ou amélioration/i })
    await expect(champ, 'Le choix de la carte a garder doit etre affiche.').toBeVisible()

    // Les cartes a cout 3 sont proposees (The Champion est Booing Crowd), la carte a cout 4 ne l'est pas.
    for (const id of COUT_3) await expect(champ.locator(`[data-card-id="${id}"]`)).toHaveCount(1)
    await expect(champ.locator(`[data-card-id="${COUT_4}"]`), 'Une carte a cout 4 ne doit jamais etre proposee.').toHaveCount(0)

    await champ.locator(`[data-card-id="${COUT_3[0]}"] button`).click()
    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    expect(apres.carnet?.['Player 1 Support / Upgrade #1'], 'La carte cochee n est pas au carnet.').toBe(COUT_3[0])
    expect(apres.carnet?.['Modular Sets Used'], 'Le set modulaire utilise n est pas coche au carnet.').toBe('crime')
    expect(apres.carnet?.['Longshot In Play: Scenario 1'], 'Longshot n etait pas en jeu : il ne doit pas etre note.').toBeUndefined()
    expect(
      Object.keys(apres.carnet ?? {}).filter((k) => k.includes('Eligible')),
      'La liste de propositions est une cle de travail : elle ne doit pas etre recopiee au carnet.'
    ).toEqual([])
    expect(apres.termines, 'Magog doit etre marque comme termine.').toContain('magog')
  })
})
