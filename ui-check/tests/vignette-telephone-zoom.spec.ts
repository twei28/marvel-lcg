// Bug 136 (16/11/2026) : au telephone, en pleine defense, la vignette de la carte doit s'agrandir au toucher (sans choisir).
//   UI_CHECK_BASE=http://127.0.0.1:2345 VIGNETTE_ZOOM=1 npx playwright test tests/vignette-telephone-zoom.spec.ts --project=s24
// Affichage « Normal » = `epure`. Captures dans captures/vignette_zoom/.
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.VIGNETTE_ZOOM, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'vignette_zoom')

test('defense au telephone : la vignette s’agrandit, le choix part du bouton', async ({ page }) => {
  test.setTimeout(240_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?spider_man')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard, seed: 4321, timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript(() => {
    try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'epure') } catch { /* */ }
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
  const cmd = async (c: string) => { await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); await page.waitForTimeout(1500) }
  await cmd("Puzzle.ChangeForm('01001b')")
  await cmd("Puzzle.PutIntoPlay('01011', under_control=True)")
  await cmd("Puzzle.EnemyAttacks('01094', '01001a')")
  await page.waitForTimeout(2500)
  const choixPlateau = page.getByRole('button', { name: /^Ronds/ })
  if (await choixPlateau.isVisible().catch(() => false)) { await choixPlateau.click(); await page.waitForTimeout(1500) }
  await page.screenshot({ path: path.join(SORTIE, '1-defense.png') })
  const vignette = page.locator('.dc-vignette').first()
  console.log('VIGNETTES', await page.locator('.dc-vignette').count(), 'repere', await vignette.evaluate((e) => getComputedStyle(e, '::after').content).catch(() => 'n/a'))
  await vignette.locator('article, button').first().tap()
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '2-zoom.png') })
  console.log('ZOOM', await page.locator('.carte-ouverte').count(), 'ASK', (await (await request.get('/get_ask?p=0')).text()).slice(0, 80))
})
