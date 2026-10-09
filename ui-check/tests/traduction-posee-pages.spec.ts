// La traduction posée sur les scans anglais, hors plateau : aperçu du
// deckbuilder et fiche de la galerie, en français.
import { test, expect } from '@playwright/test'

test.use({ deviceScaleFactor: 2 })

test('deckbuilder : la traduction se pose sur un scan fan-made anglais', async ({ page }) => {
  const erreurs: string[] = []
  page.on('pageerror', (e) => erreurs.push(String(e)))
  await page.goto('/deck-builder.html?hero=spider_man')
  await page.evaluate(() => localStorage.setItem('marvel-langue', 'fr'))
  await page.reload()
  await page.waitForSelector('.db-chip', { timeout: 30000 })
  await page.locator('.db-recherche').fill('Advice')
  await page.locator('#db-grille [data-carte="mw028"] img').hover()
  const pose = page.locator('#db-apercu .traduction-posee')
  await expect(pose).toHaveCount(1, { timeout: 15000 })
  await expect(pose).toContainText('TACTIQUE')
  await page.waitForTimeout(800)
  await page.locator('#db-apercu').screenshot({ path: 'test-results/traduction-deckbuilder.png' })
  // Une carte officielle a son scan français : rien n'est posé.
  await page.locator('.db-recherche').fill('Manoir des Avengers')
  await page.locator('#db-grille .db-carte img').first().hover()
  await page.waitForTimeout(1500)
  await expect(page.locator('#db-apercu .traduction-posee')).toHaveCount(0)
  expect(erreurs.join(' | ')).toBe('')
})

test('galerie : la traduction se pose dans la fiche', async ({ page }) => {
  const erreurs: string[] = []
  page.on('pageerror', (e) => erreurs.push(String(e)))
  await page.goto('/galerie.html')
  await page.evaluate(() => localStorage.setItem('marvel-langue', 'fr'))
  await page.reload()
  await page.getByRole('checkbox', { name: 'Fan-made' }).check()
  await page.getByRole('searchbox').fill('Female Power')
  await page.locator('.g-carte').first().click()
  const pose = page.locator('.g-apercu .traduction-posee')
  await expect(pose).toHaveCount(1, { timeout: 15000 })
  await page.waitForTimeout(800)
  await page.locator('.g-apercu-cadre').screenshot({ path: 'test-results/traduction-galerie.png' })
  expect(erreurs.join(' | ')).toBe('')
})
