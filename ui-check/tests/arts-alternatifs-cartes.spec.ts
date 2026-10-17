// ARTS ALTERNATIFS DES CARTES DE DECK (regle de l'utilisateur, 17/10/2026).
//
// A la selection d'un deck, une petite fenetre propose « Choisir des arts
// alternatifs pour les cartes de ce deck ? » (Oui / Non, case « Ne plus
// proposer »), puis liste les cartes du deck qui ont un art alternatif, avec
// leur choix. Un heros TMNT a l'art TMNT par defaut, les autres l'officielle.
//
// Ne lance rien : lit un moteur deja demarre, ne sauvegarde aucun deck.
//
//   UI_CHECK_BASE=http://127.0.0.1:<port> npx playwright test tests/arts-alternatifs-cartes.spec.ts --project=pc
import { expect, test, type Page } from '@playwright/test'
import fs from 'node:fs'

test.use({ viewport: { width: 1500, height: 950 } })

const CAPTURES = process.env.ARTS_CAPTURES ?? ''

async function capture(page: Page, nom: string) {
  if (!CAPTURES) return
  fs.mkdirSync(CAPTURES, { recursive: true })
  await page.screenshot({ path: `${CAPTURES}/${nom}.png` })
}

async function versLesDecks(page: Page, heros: RegExp) {
  await page.goto('/prepare.html')
  await page.waitForSelector('.acc-mode', { timeout: 20000 })
  await page.getByRole('button', { name: /^Solo/ }).first().click()
  await page.waitForSelector('#hero-grid .tb-port', { timeout: 20000 })
  // Les heros TMNT sont fan-made : le filtre est a cocher avant de les voir.
  const fan = page.getByRole('button', { name: 'Fan-made', exact: true })
  if (await fan.count()) await fan.click()
  await page.waitForTimeout(500)
  await page.locator('#hero-grid .tb-port').filter({ hasText: heros }).first().click()
  await page.waitForTimeout(800)
  const choisir = page.getByRole('button', { name: /Choisir ce h/i })
  if (await choisir.count()) await choisir.first().click()
  await page.waitForTimeout(800)
  const options = page.locator('.deck-modal')
  if (await options.count()) {
    const valider = options.getByRole('button', { name: /valider/i })
    if (await valider.count()) await valider.click()
  }
  await page.getByRole('button', { name: /continuer/i }).click()
  await page.waitForSelector('#deck-liste .tb-deck', { timeout: 20000 })
}

/** Clique les decks de la liste jusqu'a ce que la fenetre s'ouvre ; rend l'indice du deck. */
async function choisirUnDeckAvecArts(page: Page): Promise<number> {
  const n = await page.locator('#deck-liste .tb-deck').count()
  for (let i = 0; i < n; i++) {
    await page.locator('#deck-liste .tb-deck').nth(i).click()
    await page.waitForTimeout(500)
    if (await page.locator('.ac-modal').count()) return i
  }
  return -1
}

test('un heros TMNT : la fenetre, ses arts TMNT par defaut, « ne plus proposer »', async ({ page }) => {
  test.setTimeout(120_000)
  await versLesDecks(page, /Leonardo/)
  const i = await choisirUnDeckAvecArts(page)
  expect(i, 'aucun deck de Leonardo n a declenche la fenetre').toBeGreaterThanOrEqual(0)

  await expect(page.locator('.ac-question')).toContainText(/arts alternatifs/i)
  await capture(page, '1-question')

  await page.locator('[data-ac="oui"]').click()
  const cartes = page.locator('.ac-carte')
  expect(await cartes.count()).toBeGreaterThan(0)
  // Par defaut, l'art TMNT est choisi pour chaque carte d'un heros TMNT.
  const surLaPremiere = cartes.first().locator('.ac-vignette.on')
  await expect(surLaPremiere).toHaveAttribute('data-code', 'tmnt')
  await capture(page, '2-liste-defaut-tmnt')

  // Choisir l'officielle pour la premiere carte l'enregistre (cle lue par le plateau).
  const id = await cartes.first().getAttribute('data-carte')
  await cartes.first().locator('.ac-vignette[data-code="standard"]').click()
  await expect(cartes.first().locator('.ac-vignette.on')).toHaveAttribute('data-code', 'standard')
  const table = await page.evaluate(() => JSON.parse(localStorage.getItem('mc_card_art_v1') ?? '{}'))
  expect(table[id!]).toBe('standard')
  await capture(page, '3-liste-officielle-choisie')
  await page.locator('[data-ac="fin"]').click()
  await expect(page.locator('.ac-modal')).toHaveCount(0)

  // Selectionner de nouveau le meme deck repropose la fenetre ; « Ne plus proposer » la coupe.
  await page.locator('#deck-liste .tb-deck').nth(i).click()
  await expect(page.locator('.ac-modal')).toHaveCount(1)
  await page.locator('#ac-ne-plus').check()
  await capture(page, '5-ne-plus-proposer')
  await page.locator('[data-ac="non"]').click()
  await expect(page.locator('.ac-modal')).toHaveCount(0)
  await page.locator('#deck-liste .tb-deck').nth(i).click()
  await page.waitForTimeout(800)
  await expect(page.locator('.ac-modal')).toHaveCount(0)
})

test('editeur de deck : selecteur d art, art TMNT par defaut pour Leonardo, tuile unique', async ({ page }) => {
  const erreurs: string[] = []
  page.on('pageerror', (e) => erreurs.push(String(e)))
  await page.goto('/deck-builder.html?hero=leonardo')
  await page.evaluate(() => {
    localStorage.removeItem('mc_card_art_v1')
    localStorage.setItem('marvel-langue', 'en')
  })
  await page.reload()
  await page.waitForSelector('#db-grille .db-carte', { state: 'attached', timeout: 30000 })
  await page.locator('.db-recherche').fill('Combat Training')
  await page.waitForTimeout(600)
  const tuiles = page.locator('#db-grille .db-carte[title="Combat Training"]')
  await expect(tuiles).toHaveCount(1) // une seule tuile par nom, pas une par art
  await expect(tuiles.locator('img')).toHaveAttribute('src', /01057_tmnt/)
  await tuiles.hover()
  await expect(page.locator('#db-arts img')).toHaveCount(2)
  await expect(page.locator('#db-arts img.est-active')).toHaveAttribute('data-art', 'tmnt')
  await capture(page, '6-editeur-leonardo-tmnt')

  // Choisir l'officielle change l'image, pas le deck (meme carte, meme nombre d'exemplaires).
  await tuiles.locator('button[data-action="plus"]').click()
  await page.locator('#db-arts img[data-art="standard"]').click()
  await expect(page.locator('#db-grille .db-carte[title="Combat Training"] img')).not.toHaveAttribute('src', /_tmnt/)
  await expect(page.locator('#db-grille .db-carte[title="Combat Training"] .db-badge')).toHaveText('1/3')
  const table = await page.evaluate(() => JSON.parse(localStorage.getItem('mc_card_art_v1') ?? '{}'))
  expect(table['01057']).toBe('standard')
  await capture(page, '7-editeur-leonardo-officielle')
  expect(erreurs.join(' | '), 'erreur JS dans l editeur').toBe('')
})

test('editeur de deck : une exclusive TMNT n est proposee qu a un heros TMNT', async ({ page }) => {
  await page.goto('/deck-builder.html?hero=leonardo')
  await page.waitForSelector('#db-grille .db-carte', { state: 'attached', timeout: 30000 })
  await page.locator('.db-recherche').fill('Bo-Wing')
  await page.waitForTimeout(600)
  await expect(page.locator('#db-grille .db-carte[data-carte="ua006"]')).toHaveCount(1)
  await page.goto('/deck-builder.html?hero=spider_man')
  await page.waitForSelector('#db-grille .db-carte', { state: 'attached', timeout: 30000 })
  await page.locator('.db-recherche').fill('Bo-Wing')
  await page.waitForTimeout(600)
  await expect(page.locator('#db-grille .db-carte[data-carte="ua006"]')).toHaveCount(0)
  await capture(page, '8-editeur-spiderman-sans-exclusive')
})

test('un autre heros : l officielle par defaut', async ({ page }) => {
  test.setTimeout(120_000)
  await versLesDecks(page, /^Spider-Man/)
  const i = await choisirUnDeckAvecArts(page)
  if (i < 0) test.skip(true, 'aucun deck de Spider-Man ne contient de carte a art alternatif')
  await page.locator('[data-ac="oui"]').click()
  await expect(page.locator('.ac-carte').first().locator('.ac-vignette.on')).toHaveAttribute('data-code', 'standard')
  await capture(page, '4-autre-heros-officielle')
})

// CONVERSION DU 17/10/2026 : « Clobber » TMNT (ex-ua009, image seule) n'est plus une carte mais l'art
// alternatif `18012_tmnt` de l'officielle 18012. Leonardo l'a par defaut, Spider-Man garde l'officielle.
test('Clobber (ex-ua009) : art TMNT par defaut pour Leonardo, officielle pour Spider-Man', async ({ page }) => {
  const erreurs: string[] = []
  page.on('pageerror', (e) => erreurs.push(String(e)))
  for (const [hero, attendu] of [
    ['leonardo', /18012_tmnt/],
    ['spider_man', /18012(?!_tmnt)/],
  ] as const) {
    await page.goto(`/deck-builder.html?hero=${hero}`)
    await page.evaluate(() => {
      localStorage.removeItem('mc_card_art_v1')
      localStorage.setItem('marvel-langue', 'en')
    })
    await page.reload()
    await page.waitForSelector('#db-grille .db-carte', { state: 'attached', timeout: 30000 })
    await page.locator('.db-recherche').fill('Clobber')
    await page.waitForTimeout(600)
    const tuiles = page.locator('#db-grille .db-carte[title="Clobber"]')
    await expect(tuiles).toHaveCount(1)
    await expect(page.locator('#db-grille .db-carte[data-carte="ua009"]')).toHaveCount(0) // la carte n'existe plus
    await expect(tuiles.locator('img')).toHaveAttribute('src', attendu)
    await tuiles.hover()
    await capture(page, `9-clobber-${hero}`)
  }
  expect(erreurs.join(' | '), 'erreur JS dans l editeur').toBe('')
})
