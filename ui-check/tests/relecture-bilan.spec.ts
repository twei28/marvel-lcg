// Relecture : le bilan de la phase du mechant se referme quand le joueur
// l'avait referme, sans clic de celui qui regarde (signalement du 10/10/2026).
// N'a besoin que des pages : le lecteur ne parle pas au moteur.
import { mkdirSync, readFileSync } from 'node:fs'
import { gunzipSync } from 'node:zlib'
import { expect, test, type Frame, type Page } from '@playwright/test'

const FICHIER = '../ui-app/src/board/relecture/__fixtures__/partie-reelle.marvelreplay'
const DOSSIER = 'captures-tmp/relecture-bilan'

type Ligne = { k: string; t?: number; cle?: string }

const cadreDuPlateau = (page: Page): Frame => {
  const cadre = page.frames().find((f) => f !== page.mainFrame())
  if (!cadre) throw new Error('pas de cadre de relecture')
  return cadre
}

test('le bilan suit le joueur : affiche pendant sa lecture, referme ensuite', async ({ page }) => {
  test.setTimeout(120_000)
  mkdirSync(DOSSIER, { recursive: true })
  const lignes = gunzipSync(readFileSync(FICHIER))
    .toString('utf-8')
    .split('\n')
    .filter(Boolean)
    .map((l) => JSON.parse(l) as Ligne)
  const bilan = lignes.find((l) => l.k === 'e' && l.cle === 'bilan')?.t ?? 0
  const fermeture = lignes.find((l) => l.k === 'e' && l.cle === '' && (l.t ?? 0) > bilan)?.t ?? 0
  expect(bilan).toBeGreaterThan(0)
  expect(fermeture).toBeGreaterThan(bilan)

  await page.addInitScript(() => {
    localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille')
    localStorage.setItem('marvel-langue-choisie', '1')
  })
  await page.goto('/app/board.html?relecture=1')
  await page.locator('input[type=file]').setInputFiles(FICHIER)
  await page.waitForSelector('.relecture-fiche', { timeout: 15000 })
  await page.locator('.relecture-fiche .relecture-bouton-lecture').click()

  // Lecture depuis un peu avant le bilan : le plateau rejoue la fin de phase.
  await page.evaluate((t) => {
    const l = (window as unknown as { lecteurRelecture: { pause(): void; allerAuTemps(t: number): void; lecture(): void } })
      .lecteurRelecture
    l.pause()
    l.allerAuTemps(t)
    l.lecture()
  }, bilan - 3000)
  const temps = () => page.evaluate(() => (window as unknown as { lecteurRelecture: { tempsCourant(): number } }).lecteurRelecture.tempsCourant())
  const cartouches = () => cadreDuPlateau(page).locator('.deroule-phase').count()

  let vuPendantLeBilan = false
  let fermeApres = false
  for (let i = 0; i < 80 && !fermeApres; i++) {
    await page.waitForTimeout(150)
    const t = await temps()
    const n = await cartouches()
    if (t > bilan + 100 && t < fermeture - 100 && n > 0 && !vuPendantLeBilan) {
      vuPendantLeBilan = true
      await page.screenshot({ path: `${DOSSIER}/1-bilan-lu.png` })
    }
    if (t > fermeture + 400 && n === 0) {
      fermeApres = true
      await page.screenshot({ path: `${DOSSIER}/2-apres-fermeture.png` })
    }
  }
  expect(vuPendantLeBilan).toBe(true)
  expect(fermeApres).toBe(true)
})
