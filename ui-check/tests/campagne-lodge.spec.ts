// Le Lodge de « Hunting Season » : le Marché générique, réglé par la boîte.
//
// Livret p.3 : « Between each scenario, players get the option to add cards to
// their deck from The Lodge... "Experience Cost" followed by a number ». Gibbon
// est « set aside and cannot be added to any player's deck until the campaign
// instructs the card to be added to The Lodge » (victoire contre Vulture).
//
// Ce que la boîte déclare (data/campagnes/hunting_season.json, bloc `marche`) et
// que l'écran doit tenir : ids non numériques (`cartes`), prix lu par
// `motif_cout`, verrou de Gibbon, ouverture APRÈS le premier scénario, et les
// réglages de début de campagne (`options_campagne`).
//
//   npx playwright test tests/campagne-lodge.spec.ts --project=pc
import { test, expect, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - lodge'
/** Taunt (hs172) coûte 1 XP, Rocket Raccoon (hs164) en coûte 4, Gibbon (hs168) 1. */
const TAUNT = 'hs172'
const ROCKET = 'hs164'
const GIBBON = 'hs168'

let identifiant = ''

async function poser(
  request: APIRequestContext,
  carnet: Record<string, string>,
  termines: string[],
  difficulte = 'standard'
): Promise<void> {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        ...(identifiant ? { id: identifiant } : {}),
        code: 'hunting_season',
        nom: NOM,
        difficulte,
        equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'] }],
        termines,
        carnet,
        tentatives: {},
        partieEnCours: null,
      },
    },
  })
  expect(reponse.status()).toBe(200)
  identifiant = (await reponse.json()).id as string
}

const carnet = async (request: APIRequestContext) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{
    id: string
    carnet?: Record<string, string>
  }>
  return liste.find((c) => c.id === identifiant)?.carnet ?? {}
}

async function ouvrir(page: import('@playwright/test').Page) {
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
}

const vignette = (page: import('@playwright/test').Page, id: string) =>
  page.locator('.cmp-marche-carte').filter({ has: page.locator(`img[src*="${id}"]`) })

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{ id: string; nom?: string }>
  for (const c of liste) {
    if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
  }
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test.describe.serial('Le Lodge', () => {
  test('Avant le premier scénario, pas de Lodge, et les réglages se choisissent', async ({ page, request }) => {
    await poser(request, {}, [], 'expert')
    await ouvrir(page)
    await expect(page.getByRole('button', { name: /lodge/i }), 'Le Lodge est ouvert avant le scénario 1.').toHaveCount(0)

    const reglages = page.locator('.cmp-bloc', { hasText: /réglages|settings/i })
    await expect(reglages).toBeVisible()
    await reglages.locator('.cmp-champ', { hasText: /hunter mode|mode hunter/i }).getByRole('button', { name: /oui|yes/i }).click()
    await expect.poll(async () => (await carnet(request))['Hunter Mode']).toBe('1')
    await reglages.locator('.cmp-champ', { hasText: /master hunter/i }).getByRole('button', { name: 'Spider-Man' }).click()
    await expect.poll(async () => (await carnet(request))['Master Hunter']).toBe('1')
  })

  test('Après un scénario : prix lu sur la carte, Gibbon verrouillé, achat inscrit au carnet', async ({ page, request }) => {
    await poser(request, { 'Player 1 Experience': '3' }, ['hs_vermin'])
    await ouvrir(page)
    // Reglages figes apres le premier scenario (le mode Hunter, expert seulement, n'apparait pas ici).
    await expect(page.locator('.cmp-bloc', { hasText: /réglages|settings/i }).getByRole('button', { name: 'Spider-Man' }))
      .toBeDisabled()
    await page.getByRole('button', { name: /lodge/i }).click()

    await expect(page.locator('.cmp-marche-solde strong')).toHaveText('3')
    await expect(vignette(page, TAUNT).locator('.cmp-marche-cout')).toHaveText('1')
    await expect(vignette(page, ROCKET).locator('.cmp-marche-cout')).toHaveText('4')
    await expect(vignette(page, ROCKET), 'Rocket à 4 XP est achetable avec 3.').toBeDisabled()
    await expect(vignette(page, GIBBON), 'Gibbon est au Lodge avant la victoire contre Vulture.').toHaveCount(0)

    await vignette(page, TAUNT).click()
    await expect(page.locator('.cmp-marche-solde strong')).toHaveText('2')
    const apres = await carnet(request)
    expect(apres['Player 1 Experience']).toBe('2')
    expect((apres['Player 1 Cards added to deck'] ?? '').split(';')).toContain(TAUNT)
  })

  test('« Gibbon unlocked » au carnet : Gibbon entre au Lodge', async ({ page, request }) => {
    await poser(request, { 'Player 1 Experience': '3', 'Gibbon unlocked': '1' }, ['hs_vermin'])
    await ouvrir(page)
    // L'ecran se redessine une fois les cartes chargees : attendre les reglages avant de cliquer.
    await expect(page.locator('.cmp-bloc', { hasText: /réglages|settings/i }).getByRole('button', { name: 'Spider-Man' })).toBeVisible()
    await page.getByRole('button', { name: /lodge/i }).click()
    await expect(vignette(page, GIBBON)).toHaveCount(1)
    await expect(vignette(page, GIBBON).locator('.cmp-marche-cout')).toHaveText('1')
  })
})
