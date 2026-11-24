// Voiles FR d'un échantillon des cartes du scénario 5 « Cassandra Nova » (Hellfire Hunt, `hf`, 01/11/2026) : survol de chacune, captures dans captures/cassandra-nova-voiles/.
//   UI_CHECK_BASE=http://127.0.0.1:10555 CASSANDRA_VOILES=1 npx playwright test tests/cassandra-nova-voiles.spec.ts --project=pc
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.CASSANDRA_VOILES, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'cassandra-nova-voiles')
// card_id mis en jeu par le bac à sable, puis nom imprimé de la carte (début de l'aria-label).
const CARTES: Array<[string, string, string]> = [
  ['hf608', 'Exploding Their Head', 'exploding'],
  ['hf610', 'Psychic Control', 'psychic-control'],
  ['hf620', 'Global Opinion Controls', 'global-opinion'],
  ['hf621', 'The Hate Machine', 'hate-machine'],
  ['hf382', 'Wild Sentinel', 'wild-sentinel'],
  ['hf381', 'Mutant Extinction Agenda', 'mutant-extinction'],
  ['hf372', 'False Reality', 'false-reality'],
  ['hf373', 'Mind Maze', 'mind-maze'],
]
const EN_PLACE = ['Cassandra Nova', 'Diplomatic Sabotage', 'Cassandra Domination', 'Psychic Aegis']

test('voiles FR de Cassandra Nova', async ({ page }) => {
  test.setTimeout(240_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?hellfire_cassandra_nova')).json()
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
  for (const [id] of CARTES) {
    const r = await request.post('/sandbox_command?p=0', { data: { commands: [`Puzzle.PutIntoPlay('${id}')`] } })
    console.log('CMD', id, r.status())
    await page.waitForTimeout(1500)
  }
  // Deux compteurs sur l'identité : visibles sur la carte.
  await request.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.PlaceCounters('01001b', 'cassandra_controls', 2)"] } })
  await page.waitForTimeout(1500)
  for (let i = 0; i < 12; i++) {
    const suite = page.getByRole('button', { name: /continuer/i }).first()
    if (!(await suite.isVisible().catch(() => false))) { await page.waitForTimeout(800); if (!(await suite.isVisible().catch(() => false))) break }
    await suite.click()
    await page.waitForTimeout(1200)
  }
  await page.screenshot({ path: path.join(SORTIE, '0-table.png') })
  const noms = await page.locator('article[aria-label]').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label')))
  console.log('CARTES SUR LA TABLE', JSON.stringify(noms))
  const aSurvoler: Array<[string, string]> = [...CARTES.map(([, nom, f]) => [nom, f] as [string, string]), ...EN_PLACE.map((n) => [n, n.toLowerCase().replace(/ /g, '-')] as [string, string])]
  for (const [nom, fichier] of aSurvoler) {
    const carte = page.locator(`article[aria-label^="${nom}"]`).first()
    if (!(await carte.count())) { console.log('ABSENTE', nom); continue }
    await carte.hover({ force: true })
    await page.waitForTimeout(1800)
    await page.screenshot({ path: path.join(SORTIE, `voile-${fichier}.png`) })
    await page.mouse.move(800, 300)
    await page.waitForTimeout(500)
  }
})
