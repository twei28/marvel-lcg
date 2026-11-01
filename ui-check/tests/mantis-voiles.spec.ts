// Voiles FR des cartes de Mantis non vues (01/11/2026) : cartes posees par /sandbox_command, apercu force par Alt au survol, captures dans captures/mantis-voiles/.
//   UI_CHECK_BASE=http://127.0.0.1:2351 MANTIS_VOILES=1 npx playwright test tests/mantis-voiles.spec.ts --project=pc
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.MANTIS_VOILES, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'mantis-voiles')
const EN_MAIN = ['mt003', 'mt004', 'mt005', 'mt006', 'mt008', 'mt009', 'mt015', 'mt016', 'mt011', 'mt013']

test('voiles FR de Mantis (cartes non vues)', async ({ page }) => {
  test.setTimeout(180_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?mantis')).json())],
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
  for (const cmd of ['Puzzle.EmptyHand()', `Puzzle.CreateHandCards(${EN_MAIN.map((c) => `'${c}'`).join(', ')})`]) {
    const r = await request.post('/sandbox_command?p=0', { data: { commands: [cmd] } })
    console.log('CMD', cmd, r.status())
    await page.waitForTimeout(2000)
  }
  await page.screenshot({ path: path.join(SORTIE, '0-table.png') })
  const noms = await page.locator('article[aria-label]').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label')))
  console.log('CARTES', JSON.stringify(noms))
  const vues: string[] = []
  for (const [i, nom] of noms.entries()) {
    if (!nom || !/Swordsman|Cotati|Fortified|Precognition|Pressure|Psychic|Biopathy|Mindlock|Mindlink/i.test(nom)) continue
    const carte = page.locator(`article[aria-label="${nom}"]`).first()
    await carte.scrollIntoViewIfNeeded().catch(() => undefined)
    const box = await carte.boundingBox()
    if (!box) { console.log('ABSENTE', nom); continue }
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2 - 10, { steps: 6 })
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 4 })
    await page.waitForTimeout(900)
    await page.keyboard.down('Alt')
    await page.waitForTimeout(900)
    const n = await page.locator('.carte-apercu').count()
    console.log('APERCU', nom, n)
    await page.screenshot({ path: path.join(SORTIE, `voile-${i}-${nom.split(',')[0].toLowerCase().replace(/[^a-z0-9]+/g, '-')}.png`) })
    await page.keyboard.up('Alt')
    await page.mouse.move(800, 300)
    await page.waitForTimeout(500)
    vues.push(nom)
  }
  console.log('VUES', JSON.stringify(vues))
})
