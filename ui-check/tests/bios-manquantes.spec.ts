// Biographies ajoutees le 02/11/2026 (Hawkeye MCDC 2026, Iron Patriot, She-Hulk Why Not, Spider-Woman Kajislav) : le panneau du wizard les affiche.
//   UI_CHECK_BASE=http://127.0.0.1:2346 BIOS_ECRANS=1 npx playwright test tests/bios-manquantes.spec.ts --project=pc
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'

test.skip(!process.env.BIOS_ECRANS, 'ouvre le wizard')
const SORTIE = path.resolve('..', 'captures', 'bios')
const HEROS: [string, RegExp][] = [
  ['hawkeye_mcdc_2026', /Tales of Suspense #57/],
  ['iron_patriot', /Norman Osborn/],
  ['she_hulk_why_not', /Savage She-Hulk #1/],
  ['spider_woman_kajislav', /Julia Carpenter/],
]

for (const [id, motif] of HEROS) {
  test(`biographie de ${id}`, async ({ page }) => {
    test.setTimeout(90_000)
    page.setDefaultTimeout(15_000)
    fs.mkdirSync(SORTIE, { recursive: true })
    await page.setViewportSize({ width: 1600, height: 900 })
    await page.addInitScript(() => {
      try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr') } catch { /* */ }
    })
    await page.goto('/prepare.html')
    await page.getByRole('button', { name: /^Solo/ }).first().click()
    await page.getByRole('button', { name: /fan-made/i }).first().click()
    const tuile = page.locator(`.tb-port[data-hero="${id}"]`)
    await tuile.waitFor({ timeout: 30_000 })
    await tuile.hover()
    await page.waitForTimeout(1200)
    await page.getByText(/biographie/i).first().click()
    await page.waitForTimeout(1000)
    await page.screenshot({ path: path.join(SORTIE, `${id}.png`) })
    expect(await page.locator('body').innerText()).toMatch(motif)
  })
}
