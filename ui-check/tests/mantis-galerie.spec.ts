// Galerie : voile FR des cartes de Mantis (captures dans captures/mantis/galerie-*.png).
//   UI_CHECK_BASE=http://127.0.0.1:2351 MANTIS_ECRANS=1 npx playwright test tests/mantis-galerie.spec.ts --project=pc
import { test } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
test.skip(!process.env.MANTIS_ECRANS, 'ouvre une page de galerie')
test('galerie Mantis', async ({ page }) => {
  test.setTimeout(90_000)
  page.setDefaultTimeout(15_000)
  const sortie = path.resolve('..', 'captures', 'mantis')
  fs.mkdirSync(sortie, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 1000 })
  await page.addInitScript(() => { try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr') } catch { /* */ } })
  await page.goto('/galerie.html')
  await page.waitForTimeout(3000)
  await page.screenshot({ path: path.join(sortie, 'galerie-0.png') })
  await page.getByLabel(/fan-made/i).check()
  const champ = page.locator('input[type="search"], input[type="text"]').first()
  for (const q of ['Slay Time', 'Auto-9', 'Precognition']) {
    await champ.fill(q)
    await page.waitForTimeout(1500)
    await page.screenshot({ path: path.join(sortie, `galerie-${q.split(' ')[0].toLowerCase()}.png`), clip: { x: 0, y: 0, width: 1600, height: 520 } })
  }
})
