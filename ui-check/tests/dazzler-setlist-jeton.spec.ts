// Bug 134 (16/11/2026) : le jeton « son » de Rehearsal sur une chanson de la Setlist (Dazzler) doit s'afficher.
//   UI_CHECK_BASE=http://127.0.0.1:2345 DAZZLER_JETON=1 npx playwright test tests/dazzler-setlist-jeton.spec.ts --project=pc
// Affichage « Normal » = valeur rangee `epure` (CLAUDE.md). Captures dans captures/dazzler_jeton/.
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.DAZZLER_JETON, 'cree une partie')
const LANGUE = process.env.DAZZLER_LANGUE ?? 'fr'
const SORTIE = path.resolve('..', 'captures', LANGUE === 'fr' ? 'dazzler_jeton' : 'dazzler_jeton-en')

test('jeton son sur la Setlist de Dazzler', async ({ page }) => {
  test.setTimeout(240_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?dazzler')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard, seed: 4321, timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript((l: string) => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', l)
      localStorage.setItem('mc_affichage_v1', 'epure')
    } catch { /* */ }
  }, LANGUE)
  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)
  for (let i = 0; i < 60; i++) {
    const t = await (await request.get('/get_ask?p=0')).text()
    if (t.trim() && JSON.parse(t).event_name === 'WhenPlayerInTurn') break
    await repondre(request, 0)
    await page.waitForTimeout(500)
  }
  await page.waitForTimeout(3000)
  const continuer = async () => {
    for (let i = 0; i < 12; i++) {
      const suite = page.getByRole('button', { name: /continuer/i }).first()
      if (!(await suite.isVisible().catch(() => false))) { await page.waitForTimeout(800); if (!(await suite.isVisible().catch(() => false))) break }
      await suite.click()
      await page.waitForTimeout(1200)
    }
  }
  const cmd = async (c: string) => { const r = await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); await page.waitForTimeout(1500); console.log('CMD', c, await r.text(), (await (await request.get('/get_ask?p=0')).text()).slice(0, 120)) }
  await cmd("Puzzle.ChangeForm('dz001b')")
  for (const c of ['dz012', 'dz005']) await cmd(`Puzzle.PlaceUnder('${c}', 'dz017a', face_up=True)`)
  await continuer()
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '1-avant-rehearsal.png') })
  await cmd("Puzzle.Action('dz001a', 'HeroAction')")
  // Rehearsal demande LAQUELLE des chansons repeter : on prend « Too Good to be True » (celle du signalement).
  const ask = JSON.parse(await (await request.get('/get_ask?p=0')).text()) as { options_json?: string }
  const options = JSON.parse(ask.options_json ?? '[]') as Array<Record<string, unknown>>
  console.log('OPTIONS', JSON.stringify(options.map((o) => [o.id, o.name])))
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '1b-choix-chanson.png') })
  const voulue = options.find((o) => /Too_Good|Too Good/i.test(String(o.name))) ?? options[0]
  await request.post('/post?p=0', { data: encodeURIComponent(JSON.stringify({ id: String(voulue.id), targets: [], resources: [] })) })
  await page.waitForTimeout(1500)
  await continuer()
  await page.waitForTimeout(2000)
  await page.screenshot({ path: path.join(SORTIE, '2-apres-rehearsal.png') })
  const txt = await page.locator('body').innerText()
  console.log('CARTES', JSON.stringify(await page.locator('article[aria-label]').evaluateAll((e) => e.map((x) => x.getAttribute('aria-label')))))
  const carte = page.locator('article[aria-label*="Too Good"], article[aria-label*="Trop Beau"]').first()
  const jeton = carte.locator('.jeton-compteur').first()
  console.log('BOX carte', JSON.stringify(await carte.boundingBox()), 'jeton', JSON.stringify(await jeton.boundingBox()),
    'visible', await jeton.isVisible(), 'css', await jeton.evaluate((e) => { const c = getComputedStyle(e); return [c.display, c.opacity, c.visibility, getComputedStyle(e.parentElement!).zIndex].join('|') }))
  const box = (await carte.boundingBox())!
  await page.mouse.move(box.x + 20, box.y + box.height / 2 - 20, { steps: 6 })
  await page.mouse.move(box.x + 22, box.y + box.height / 2 - 18, { steps: 4 })
  await page.waitForTimeout(1800)
  await page.screenshot({ path: path.join(SORTIE, '3-survol-too-good.png') })
  console.log('JETON', /\bson\b|sound/i.test(txt))
})
