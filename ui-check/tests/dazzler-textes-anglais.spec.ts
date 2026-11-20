// Audit (16/11/2026, rapport 134 : « encore quelques infos en anglais ») : tout le TEXTE visible d'une partie Dazzler en
// francais (journal, survols des cartes, fenetres de choix, table), ecrit dans captures/dazzler_textes/*.txt.
//   UI_CHECK_BASE=http://127.0.0.1:2345 DAZZLER_TEXTES=1 npx playwright test tests/dazzler-textes-anglais.spec.ts --project=pc
// Affichage « Normal » = `epure`.
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.DAZZLER_TEXTES, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'dazzler_textes')

test('textes visibles en francais, partie Dazzler', async ({ page }) => {
  test.setTimeout(280_000)
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
  const continuer = async () => {
    for (let i = 0; i < 12; i++) {
      const suite = page.getByRole('button', { name: /continuer/i }).first()
      if (!(await suite.isVisible().catch(() => false))) { await page.waitForTimeout(800); if (!(await suite.isVisible().catch(() => false))) break }
      await suite.click()
      await page.waitForTimeout(1000)
    }
  }
  const cmd = async (c: string) => { await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); await page.waitForTimeout(1300) }
  const releve: string[] = []
  const noter = async (titre: string) => {
    const corps = await page.locator('body').innerText()
    releve.push(`\n===== ${titre} =====\n${corps}`)
  }
  await cmd("Puzzle.ChangeForm('dz001b')")
  for (const c of ['dz012', 'dz005', 'dz004']) await cmd(`Puzzle.PlaceUnder('${c}', 'dz017a', face_up=True)`)
  await cmd("Puzzle.PutIntoPlay('dz014', under_control=True)")
  await cmd("Puzzle.PutIntoPlay('dz015', under_control=True)")
  await continuer()
  await noter('table apres mise en place')

  // Fenetre de choix de Rehearsal : texte de la demande, avant de repondre.
  await cmd("Puzzle.Action('dz001a', 'HeroAction')")
  await page.waitForTimeout(1500)
  await noter('choix de Rehearsal (demande en cours)')
  const ask = JSON.parse(await (await request.get('/get_ask?p=0')).text()) as { options_json?: string; prompt_text?: string }
  releve.push(`\n===== ask brut =====\n${JSON.stringify(ask).slice(0, 3000)}`)
  const options = JSON.parse(ask.options_json ?? '[]') as Array<Record<string, unknown>>
  if (options[0]) await request.post('/post?p=0', { data: encodeURIComponent(JSON.stringify({ id: String(options[0].id), targets: [], resources: [] })) })
  await page.waitForTimeout(2000)
  await continuer()
  await noter('apres Rehearsal')

  // Une defense : le vilain attaque.
  await cmd("Puzzle.EnemyAttacks('01094', 'dz001a')")
  await page.waitForTimeout(2000)
  await noter('defense (Rhino attaque)')

  // Survol de chaque carte de la table : le panneau d'apercu.
  const noms = await page.locator('article[aria-label]').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label')))
  let n = 0
  for (const nom of noms) {
    if (!nom) continue
    const carte = page.locator(`article[aria-label="${nom.replace(/"/g, '\\"')}"]`).first()
    const box = await carte.boundingBox().catch(() => null)
    if (!box) continue
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2 - 10, { steps: 5 })
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 3 })
    await page.waitForTimeout(900)
    const apercu = await page.locator('.carte-apercu').first().innerText().catch(() => '')
    releve.push(`\n===== survol « ${nom} » =====\n${apercu}`)
    n++
    if (n >= 30) break
  }
  await page.mouse.move(800, 100)
  // Le journal.
  const journal = page.getByText(/^journal$/i).first()
  if (await journal.isVisible().catch(() => false)) { await journal.click(); await page.waitForTimeout(1500) }
  await noter('journal ouvert')
  await page.screenshot({ path: path.join(SORTIE, 'journal.png') })
  fs.writeFileSync(path.join(SORTIE, 'textes.txt'), releve.join('\n'))
  console.log('ECRIT', releve.join('\n').length)
})
