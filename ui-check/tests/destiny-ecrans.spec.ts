// Destiny a l'ecran (02/11/2026) : biographie du wizard, cartes du pack sur la table, Glimpse avec la carte glissee, X du heros,
// survols FR (scans fr_dy*.jpg). Captures dans captures/destiny/.
//   UI_CHECK_BASE=http://127.0.0.1:2346 DESTINY_ECRANS=1 npx playwright test tests/destiny-ecrans.spec.ts --project=pc
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.DESTINY_ECRANS, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'destiny')

test('biographie de Destiny dans le wizard', async ({ page }) => {
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
  const tuile = page.locator('.tb-port[data-hero="destiny"]')
  await tuile.waitFor({ timeout: 30_000 })
  await tuile.hover()
  await page.waitForTimeout(1200)
  await page.getByText(/biographie/i).first().click()
  await page.waitForTimeout(1200)
  await page.screenshot({ path: path.join(SORTIE, 'bio.png') })
  const corps = await page.locator('body').innerText()
  console.log('BIO', /Aveugle de naissance/.test(corps), /Krakoa/.test(corps))
})

test('Destiny sur la table', async ({ page }) => {
  test.setTimeout(240_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?destiny')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard, seed: 4321, timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript(() => {
    try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'normal') } catch { /* */ }
  })
  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)
  for (let i = 0; i < 60; i++) {
    const t = await (await request.get('/get_ask?p=0')).text()
    if (t.trim() && JSON.parse(t).event_name === 'WhenPlayerInTurn') break
    await repondre(request, 0)
    await page.waitForTimeout(500)
  }
  await page.waitForTimeout(3000)
  const cmd = async (c: string) => { await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); await page.waitForTimeout(1200) }
  await page.screenshot({ path: path.join(SORTIE, 'alter-ego.png') })
  await cmd("Puzzle.ChangeToFace('dy001b', 'dy001a')")
  for (const c of ['dy003', 'dy004', 'dy005', 'dy006', 'dy007', 'dy008', 'dy011', 'dy012']) await cmd(`Puzzle.PutIntoPlay('${c}', under_control=True)`)
  for (const c of ['dy014', 'dy015']) await cmd(`Puzzle.PutIntoPlay('${c}')`)
  await cmd("Puzzle.PlaceUnder('01103', 'dy002')")
  await page.waitForTimeout(2000)
  for (let i = 0; i < 12; i++) {
    const suite = page.getByRole('button', { name: /continuer/i }).first()
    if (!(await suite.isVisible().catch(() => false))) { await page.waitForTimeout(800); if (!(await suite.isVisible().catch(() => false))) break }
    await suite.click()
    await page.waitForTimeout(1200)
  }
  await page.screenshot({ path: path.join(SORTIE, 'table.png') })
  const noms = await page.locator('article[aria-label]').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label')))
  console.log('CARTES', JSON.stringify(noms))
  const imgs = await page.locator('article[aria-label] img').evaluateAll((els) => els.map((e) => (e as HTMLImageElement).src.split('/').pop()))
  console.log('IMGS', JSON.stringify(imgs))
  let n = 0
  for (const nom of noms) {
    if (!nom) continue
    const carte = page.locator(`article[aria-label="${nom}"]`).first()
    const box = await carte.boundingBox()
    if (!box) continue
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2 - 12, { steps: 6 })
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 4 })
    await page.waitForTimeout(1600)
    await page.screenshot({ path: path.join(SORTIE, `survol-${String(n++).padStart(2, '0')}.png`) })
    await page.mouse.move(800, 300)
    await page.waitForTimeout(300)
  }
})
