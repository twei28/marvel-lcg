// LA BOUCLE COMPLÈTE d'une campagne en ordre libre : gagner une affaire, voir
// le carnet s'écrire, puis lancer la suivante et constater que l'environnement
// laissé par la première est en jeu.
//
// ⚠⚠ CE TEST CRÉE DES PARTIES SUR LE MOTEUR VISÉ, et toute partie en cours y
// est perdue. Script séparé (`npm run campagne-boucle`), à viser sur un moteur
// d'essai :
//   UI_CHECK_BASE=http://127.0.0.1:40000 WSLENV=UI_CHECK_BASE npm run campagne-boucle
//
// La victoire est forcée par la commande de console `Gagner()` (ajoutée le
// 19/09/2026 avec `Puzzle.Win`) : sans elle, rien ne permettait de finir une
// partie à la demande, et tout ce qui se passe APRÈS la dernière carte jouée
// — carnet de campagne, panneau de récompenses, mise en place suivante —
// restait hors de portée des tests.
import { test, expect, type Page } from '@playwright/test'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const NOM = 'Essai boucle ordre libre'
const DECK = JSON.parse(
  readFileSync(join(process.cwd(), '..', 'Fusion', 'marvel-lcg-src', 'deck', 'starter', 'spider_man.json'), 'utf-8')
)
let identifiant = ''

const campagne = async (request: any) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<any>
  return liste.find((c) => c.id === identifiant)
}

async function lancer(page: Page, affaire: RegExp) {
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
  await page.getByRole('button', { name: /tirer la progression/i }).click()
  await page.getByRole('button', { name: affaire }).click()
  await page.locator('.cmp-mission button', { hasText: /Lancer le scénario/ }).click()
  await page.waitForURL(/board\.html/, { timeout: 120000 })
  await expect(page.locator('body')).toContainText(/Hammerhead|Bullseye|Electro/i, { timeout: 120000 })
}

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{ id: string; nom?: string }>
  for (const c of liste) if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
})
test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test('gagner une affaire l inscrit au carnet, et la suivante démarre avec son environnement', async ({ page, request }) => {
  test.setTimeout(300000)
  const r = await request.post('/save_campagne', { data: { campagne: {
    code: 'fne', nom: NOM, difficulte: 'standard',
    equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'], deck: DECK }],
    termines: [], carnet: {}, tentatives: {}, partieEnCours: null, tirage: null } } })
  identifiant = (await r.json()).id as string

  // 1. Première affaire : Le casse du musée.
  await lancer(page, /^Le casse du musée|^Art Museum Heist/)

  // 2. Victoire forcée : le moteur termine la partie comme une vraie victoire.
  await page.evaluate(() => fetch('/debug?Gagner()'))

  // 3. Le panneau de récompenses s'ouvre et se valide.
  const panneau = page.locator('section.camp-recomp')
  await expect(panneau, 'le panneau de récompenses ne s est pas ouvert').toBeVisible({ timeout: 60000 })
  await page.getByRole('button', { name: /Valider et continuer la campagne|Voir la conclusion/ }).click()

  // 4. Le carnet porte l'affaire gagnée.
  await expect.poll(async () => (await campagne(request))?.carnet?.['Completed Scenarios'],
    { timeout: 30000, message: 'l affaire gagnée n est pas inscrite au carnet' }).toContain('art_museum_heist')
  const apres = await campagne(request)
  expect(apres.termines, 'la liste des scénarios terminés').toContain('art_museum_heist')
  expect(apres.partieEnCours, 'la partie en cours aurait dû être fermée').toBeFalsy()

  // 5. Affaire suivante : son environnement Complété doit être en jeu.
  await lancer(page, /^La fuite|^The Getaway/)
  await expect(page.locator('body'), "l environnement de l affaire gagnée n est pas en jeu")
    .toContainText(/Art Museum Heist|Casse du musée/i, { timeout: 120000 })
})
