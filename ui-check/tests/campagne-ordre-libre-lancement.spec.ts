// Lancer VRAIMENT une partie depuis l'écran de campagne en ordre libre.
//
// ⚠⚠ CE TEST CRÉE UNE NOUVELLE PARTIE SUR LE MOTEUR VISÉ, et toute partie en
// cours y est perdue. Il a donc son propre script (`npm run campagne-lancement`)
// et ne fait pas partie de la suite ordinaire. Le viser sur un moteur d'essai :
//   UI_CHECK_BASE=http://127.0.0.1:40000 WSLENV=UI_CHECK_BASE npm run campagne-lancement
//
// Ce qu'il tient, et que rien d'autre ne tenait : le chemin complet entre
// l'écran de campagne et le plateau. Le défaut qu'il a trouvé du premier coup
// (19/09/2026) était dans le test lui-même — l'équipe d'une campagne porte le
// DECK ENTIER, pas son nom — mais c'est exactement le genre d'erreur qui rend
// une campagne injouable sans que rien d'autre ne le dise : le moteur répond
// HTTP 500 et l'écran affiche « Failed to create the game ».
import { test, expect } from '@playwright/test'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

// L'equipe d'une campagne porte le DECK ENTIER (l'ecran de preparation l'y
// met), pas son nom : `lancerScenario` le passe tel quel au moteur, qui en
// fait un HeroDescriptor (version, hero_deck, obligations, nemesis_set).
const DECK = JSON.parse(
  readFileSync(join(process.cwd(), '..', 'Fusion', 'marvel-lcg-src', 'deck', 'starter', 'spider_man.json'), 'utf-8')
)

const NOM = 'Essai lancement ordre libre'
let identifiant = ''

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{ id: string; nom?: string }>
  for (const c of liste) if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
})
test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test('choisir une affaire et un vilain lance la bonne partie', async ({ page, request }) => {
  test.setTimeout(180000)
  const r = await request.post('/save_campagne', { data: { campagne: {
    code: 'fne', nom: NOM, difficulte: 'standard',
    equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'], deck: DECK }],
    termines: [], carnet: {}, tentatives: {}, partieEnCours: null, tirage: null } } })
  expect(r.status()).toBe(200)
  identifiant = (await r.json()).id as string

  page.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLE', m.text().slice(0, 300)) })
  page.on('response', (r) => { if (r.status() >= 400) console.log('HTTP', r.status(), r.url().slice(0, 160)) })
  page.on('pageerror', (e) => console.log('PAGEERROR', String(e).slice(0, 300)))
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
  await page.getByRole('button', { name: /tirer la progression/i }).click()
  await page.getByRole('button', { name: /^Le casse du musée|^Art Museum Heist/ }).click()
  // Bullseye plutôt que le recommandé : on vérifie que le vilain CHOISI arrive.
  await page.locator('.cmp-mission button', { hasText: /^Bullseye/ }).click()
  await page.locator('.cmp-mission button', { hasText: /Lancer le scénario/ }).click()

  // Si l'écran reste, il a une raison à afficher : la lire avant d'échouer.
  await page.waitForTimeout(4000)
  const erreur = await page.locator('.cmp-erreur').allTextContents()
  expect(erreur, `l écran de campagne a refusé de lancer : ${erreur.join(' / ')}`).toEqual([])
  await page.waitForURL(/board\.html/, { timeout: 120000 })
  // Le plateau est monté : le vilain choisi et la manigance sont en jeu.
  await expect(page.locator('body')).toContainText(/Bullseye/i, { timeout: 120000 })
  // Le plateau ecrit le nom francais OFFICIEL de la carte depuis ae946a5d (08/10/2026,
  // noms mc4db) : « Cambriolage du Musée d'Art », pas le titre de l'ecran de campagne.
  await expect(page.locator('body')).toContainText(/Cambriolage du Musée d.Art|Casse du musée|Art Museum Heist/i)

  // La campagne a enregistré la partie en cours et le vilain retenu.
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<any>
  const c = liste.find((x) => x.id === identifiant)
  expect(c.partieEnCours?.scenario, 'la partie en cours n est pas rattachée').toBe('art_museum_heist')
  expect(c.carnet?.['Villain: art_museum_heist'], 'le vilain n est pas inscrit au carnet').toBe('bullseye')
  expect(c.tirage, 'le tirage aurait dû être consommé').toBeFalsy()

  // Le plateau doit savoir qu'il joue une campagne, sans quoi le panneau de
  // récompenses ne s'ouvrira jamais et la partie ne sera pas reportée au carnet.
  const contexte = await page.evaluate(() => window.localStorage.getItem('mc-campagne-partie'))
  expect(contexte, 'le plateau ne sait pas qu il joue une campagne').toContain('art_museum_heist')
  expect(JSON.parse(contexte || '{}').id).toBe(identifiant)
})
