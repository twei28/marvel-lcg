// Voiles FR des cartes du scenario 4 « Torn » (Hellfire Hunt) : survol de chacune, captures dans captures/torn-voiles/.
//   UI_CHECK_BASE=http://127.0.0.1:10399 TORN_VOILES=1 npx playwright test tests/torn-voiles.spec.ts --project=pc
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.TORN_VOILES, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'torn-voiles')
// card_id mis en jeu par /sandbox_command (hf501a et hf504a le sont deja a la mise en place).
const CARTES = (process.env.TORN_CARTES ?? 'hf505,hf507,hf508,hf509,hf510,hf341,hf354,hf355,hf357').split(',')

test('voiles FR de Torn', async ({ page }) => {
  test.setTimeout(240_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?hellfire_torn')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?spider_man')).json())],
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
  for (const c of CARTES) {
    const r = await request.post('/sandbox_command?p=0', { data: { commands: [`Puzzle.PutIntoPlay('${c}')`] } })
    console.log('CMD', c, r.status())
    await page.waitForTimeout(1500)
  }
  for (let i = 0; i < 12; i++) {
    const suite = page.getByRole('button', { name: /continuer/i }).first()
    if (!(await suite.isVisible().catch(() => false))) { await page.waitForTimeout(800); if (!(await suite.isVisible().catch(() => false))) break }
    await suite.click()
    await page.waitForTimeout(1200)
  }
  await page.screenshot({ path: path.join(SORTIE, '0-table.png') })
  const noms = await page.locator('article[aria-label]').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label')))
  console.log('ARTICLES', JSON.stringify(noms))
  fs.writeFileSync(path.join(SORTIE, 'articles.json'), JSON.stringify(noms, null, 1))
  let i = 0
  for (const nom of noms) {
    if (!nom) continue
    const carte = page.locator(`article[aria-label="${nom}"]`).first()
    await carte.hover().catch(() => undefined)
    await page.waitForTimeout(1800)
    await page.screenshot({ path: path.join(SORTIE, `voile-${String(i++).padStart(2, '0')}-${nom.replace(/[^a-zA-Z0-9]+/g, '-').slice(0, 40)}.png`) })
    await page.mouse.move(800, 300)
    await page.waitForTimeout(500)
  }
})
