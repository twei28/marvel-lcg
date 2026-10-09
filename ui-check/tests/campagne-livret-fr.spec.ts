// L'ecran de campagne montre les pages du livret refaites en francais
// (public/stories/<code>/fr/, tools/livret_fr.py) quand le jeu est en
// francais, et les pages anglaises en anglais ou quand la page FR manque.
//
//   UI_CHECK_BASE=http://127.0.0.1:2330 WSLENV=UI_CHECK_BASE \
//     npx playwright test tests/campagne-livret-fr.spec.ts --project=pc
import { test, expect, type APIRequestContext, type Page } from '@playwright/test'

const NOM = 'Essai livret FR'
let identifiant = ''

async function poser(request: APIRequestContext) {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        code: 'hunting_season',
        nom: NOM,
        difficulte: 'standard',
        equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'] }],
        termines: [],
        carnet: {},
        tentatives: {},
        partieEnCours: null,
      },
    },
  })
  expect(reponse.status()).toBe(200)
  identifiant = (await reponse.json()).id as string
}

async function ouvrir(page: Page, langue: 'fr' | 'en') {
  await page.goto('/campagne.html')
  await page.evaluate((l) => localStorage.setItem('marvel-langue', l), langue)
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
}

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{ id: string; nom?: string }>
  for (const c of liste) if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
  await poser(request)
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test('en francais, la page du scenario est la page traduite', async ({ page }) => {
  await ouvrir(page, 'fr')
  const pageVermin = page.locator('img.cmp-page[src*="01-hs_vermin-regles-1.jpg"]').first()
  await expect(pageVermin).toBeVisible()
  await expect(pageVermin).toHaveAttribute('src', /\/stories\/hunting_season\/fr\/01-hs_vermin-regles-1\.jpg$/)
  await expect.poll(() => pageVermin.evaluate((img: HTMLImageElement) => img.naturalWidth)).toBeGreaterThan(0)
  await page.screenshot({ path: 'test-results/campagne-livret-fr.png', fullPage: false })
})

test('en anglais, la page anglaise', async ({ page }) => {
  await ouvrir(page, 'en')
  const pageVermin = page.locator('img.cmp-page[src*="01-hs_vermin-regles-1.jpg"]').first()
  await expect(pageVermin).toHaveAttribute('src', /\/stories\/hunting_season\/01-hs_vermin-regles-1\.jpg$/)
})

test('une campagne sans pages francaises retombe sur l anglais', async ({ page, request }) => {
  const reponse = await request.get('/public/stories/aos/fr/00-campagne-regles-1.jpg')
  expect(reponse.status(), 'cet essai suppose aos sans traduction').not.toBe(200)
  await page.goto('/campagne.html')
  await page.evaluate(() => localStorage.setItem('marvel-langue', 'fr'))
  // Le repli est dans pageLivret : une image FR absente bascule sur l'URL anglaise.
  const src = await page.evaluate(async () => {
    const { pageLivretUrl } = await import('/public/js/campagne/api-campagne.js')
    return [pageLivretUrl('aos', 'x.jpg', 'fr'), pageLivretUrl('aos', 'x.jpg')]
  })
  expect(src).toEqual(['/public/stories/aos/fr/x.jpg', '/public/stories/aos/x.jpg'])
})
