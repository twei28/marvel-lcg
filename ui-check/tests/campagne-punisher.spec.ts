// « La ville ne dort jamais » : l'écran de campagne choisit le scénario des combats 2 et 3 d'après le CARNET.
//
// La décision est éprouvée à part, sans navigateur, dans Fusion/marvel-lcg-src/tools/test_catalogue_carnet.mjs (toutes les combinaisons
// désignent un scénario qui existe). Ce test-ci ne vérifie que l'écran : la bonne « Mise en place » s'affiche selon le carnet, et le bouton
// de lancement existe. Aucune partie n'est ouverte.
//
//   npx playwright test tests/campagne-punisher.spec.ts --project=pc
import { test, expect, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - Punisher'
let identifiant = ''

async function poser(request: APIRequestContext, termines: string[], carnet: Record<string, string>): Promise<void> {
  const campagne = {
    ...(identifiant ? { id: identifiant } : {}),
    code: 'punisher_mcdc_2026',
    nom: NOM,
    difficulte: 'standard',
    equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'], deck: {} }],
    termines,
    carnet,
    tentatives: {},
    partieEnCours: null,
  }
  const reponse = await request.post('/save_campagne', { data: { campagne } })
  expect(reponse.status(), "Le serveur a refusé la campagne d'essai.").toBe(200)
  identifiant = (await reponse.json()).id as string
}

async function ouvrir(page: import('@playwright/test').Page): Promise<string> {
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
  await expect(page.locator('.cmp-page-campagne')).toBeVisible()
  await expect(page.getByRole('button', { name: /lancer le scénario/i })).toBeVisible()
  return (await page.locator('.cmp-sets').innerText()).replace(/\s+/g, ' ')
}

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{ id: string; nom?: string }>
  for (const c of liste) if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test.describe.serial('La ville ne dort jamais : le carnet choisit le scénario', () => {
  test('Combat 2 : Jigsaw (le Trafiquant était The Rose)', async ({ page, request }) => {
    await poser(request, ['the_big_apple'], { 'Final LEAD Location': 'Chinatown', Gunrunner: 'The Rose' })
    const sets = await ouvrir(page)
    expect(sets, 'Le combat 2 contre Jigsaw doit montrer le set Jigsaw.').toMatch(/Jigsaw/i)
    expect(sets).not.toMatch(/Hobgoblin/i)
  })

  test('Combat 2 : Hobgoblin (le Trafiquant était Nightshade)', async ({ page, request }) => {
    await poser(request, ['the_big_apple'], { 'Final LEAD Location': 'Chinatown', Gunrunner: 'Nightshade' })
    const sets = await ouvrir(page)
    expect(sets, 'Le combat 2 contre Hobgoblin doit montrer le set Hobgoblin.').toMatch(/Hobgoblin/i)
    expect(sets).not.toMatch(/Jigsaw/i)
  })

  test("Combat 3 : l'AUTRE sous-fifre (Jigsaw au combat 2 -> Hobgoblin)", async ({ page, request }) => {
    await poser(request, ['the_big_apple', 'tracking_the_buyer'], { Underling: 'Jigsaw' })
    const sets = await ouvrir(page)
    expect(sets).toMatch(/Hobgoblin/i)
    expect(sets).not.toMatch(/Jigsaw/i)
  })

  test('Combat 4 : Kingsfall (SWAT Team et Tracksuit Mafia)', async ({ page, request }) => {
    await poser(request, ['the_big_apple', 'tracking_the_buyer', 'punishment'], { 'Punisher Ally': '1' })
    const sets = await ouvrir(page)
    expect(sets).toMatch(/SWAT/i)
    expect(sets).toMatch(/Tracksuit/i)
  })
})
