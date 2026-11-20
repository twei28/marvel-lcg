// Les ERRATA officiels (RRG 1.8) a l'ecran (03/11/2026) : le nouveau texte pose sur la carte agrandie, la pastille « Errata » et sa bulle.
//   UI_CHECK_BASE=http://127.0.0.1:2391 ERRATA_ECRANS=1 [ERRATA_LANGUE=en] npx playwright test tests/errata-ecrans.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.ERRATA_ECRANS, 'cree une partie')
const LANGUE = process.env.ERRATA_LANGUE ?? 'fr'
const SORTIE = path.resolve('..', 'captures', LANGUE === 'fr' ? 'errata' : 'errata-en')

async function partie(page: Page, heros: string) {
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get(`/get_hero_json?${heros}`)).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard, seed: 4321, timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript((l: string) => {
    try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', l); localStorage.setItem('mc_affichage_v1', 'normal') } catch { /* */ }
  }, LANGUE)
  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)
  for (let i = 0; i < 60; i++) {
    const t = await (await request.get('/get_ask?p=0')).text()
    if (t.trim() && JSON.parse(t).event_name === 'WhenPlayerInTurn') break
    await repondre(request, 0)
    await page.waitForTimeout(500)
  }
  await page.waitForTimeout(2500)
  return async (c: string) => { await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); await page.waitForTimeout(1000) }
}

async function survoler(page: Page, code: string, nom: string, bulle = true) {
  const carte = page.locator(`article:has(img[src*="${code}"])`).first()
  if (!(await carte.isVisible().catch(() => false))) { console.log('ABSENTE', code); return }
  await carte.hover({ force: true })
  await page.waitForTimeout(2200)
  await page.screenshot({ path: path.join(SORTIE, `${nom}.png`) })
  const pastille = page.locator('.pastille-errata').first()
  const presente = await pastille.isVisible().catch(() => false)
  console.log('PASTILLE', code, presente, (await page.locator('.note-errata').first().innerText().catch(() => '')).slice(0, 120))
  if (bulle && presente) {
    await pastille.focus()
    await page.waitForTimeout(500)
    await page.screenshot({ path: path.join(SORTIE, `${nom}-bulle.png`) })
  }
  await page.mouse.move(800, 200)
  await page.waitForTimeout(400)
}

test('errata sur la table : Suit Up, Honorary Avenger, S.H.I.E.L.D. Deputy, Ionic Physiology, Moon Knight, Search for Spiral', async ({ page }) => {
  test.setTimeout(300_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  const cmd = await partie(page, 'spider_man')
  await cmd('Puzzle.EmptyHand()')
  await cmd("Puzzle.CreateHandCards('45017', '03025', '54033', '58002', '08009')")
  await cmd("Puzzle.PutIntoPlay('57065')")
  await cmd("Puzzle.PutIntoPlay('39016')")
  await cmd("Puzzle.PutIntoPlay('21116')")
  await page.waitForTimeout(2000)
  for (let i = 0; i < 8; i++) {
    const suite = page.getByRole('button', { name: /continuer|continue/i }).first()
    if (!(await suite.isVisible().catch(() => false))) break
    await suite.click()
    await page.waitForTimeout(1200)
  }
  await page.screenshot({ path: path.join(SORTIE, 'table.png') })
  await survoler(page, '45017', 'suit-up')
  await survoler(page, '03025', 'honorary-avenger')
  await survoler(page, '54033', 'shield-deputy')
  await survoler(page, '58002', 'ionic-physiology-deja-corrigee')
  await survoler(page, '08009', 'synth-suit-deja-corrigee')
  await survoler(page, '57065', 'moon-knight')
  await survoler(page, '39016', 'search-for-spiral')
  await survoler(page, '21116', 'sanctuary')
})

test('errata de titre sans voile : Iron Man heros', async ({ page }) => {
  test.setTimeout(240_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  await partie(page, 'iron_man')
  await survoler(page, '01029a', 'iron-man-heros')
  await survoler(page, '01029b', 'iron-man-alter-ego', false)
})
