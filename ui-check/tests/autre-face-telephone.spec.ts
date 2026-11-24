// Bug 135 (16/11/2026) : au telephone, la carte du heros ouverte en carrousel ne doit PAS recopier la pastille de la face
// en jeu (« Alter ego ») sur l'autre face.
//   UI_CHECK_BASE=http://127.0.0.1:2345 AUTRE_FACE=1 npx playwright test tests/autre-face-telephone.spec.ts --project=s24
// Affichage « Normal » = `epure`. Captures dans captures/autre_face/.
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.AUTRE_FACE, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'autre_face')

test('autre face du heros au telephone : pas de pastille recopiee', async ({ page }) => {
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
  const choixPlateau = page.getByRole('button', { name: /^Ronds/ })
  if (await choixPlateau.isVisible().catch(() => false)) { await choixPlateau.click(); await page.waitForTimeout(1500) }
  // Le didacticiel « Les ronds » (1/6) pose sa carte SUR la table : on le passe.
  const passer = page.getByRole('button', { name: /^Passer$/ })
  if (await passer.isVisible().catch(() => false)) { await passer.click(); await page.waitForTimeout(1000) }
  await page.screenshot({ path: path.join(SORTIE, '0-table.png') })
  const ronds = page.locator('.rond-bouton')
  console.log('RONDS', await ronds.count(), JSON.stringify(await ronds.evaluateAll((e) => e.map((x) => x.getAttribute('aria-label')))))
  // Le rond du HEROS (alter ego au depart : « Peter Parker »).
  await page.locator('.rond-bouton[aria-label^="Peter Parker"]').first().tap()
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '1-face-en-jeu.png') })
  const pill1 = await page.locator('.carte-ouverte-scan .kind-pill').allTextContents()
  console.log('OUVERTE', await page.locator('.carte-ouverte').count(), 'carrousel', await page.locator('.en-carrousel').count(), 'PILLS face 1', JSON.stringify(pill1))
  await page.locator('.carte-ouverte-fleche.est-droite').first().tap()
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '2-autre-face.png') })
  const info = await page.locator('.carte-ouverte-scan.est-autre-face .top-strip, .carte-ouverte-scan.est-autre-face .kind-pill').evaluateAll(
    (els) => els.map((e) => ({ cls: e.className, visible: !!(e as HTMLElement).offsetParent && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden', texte: e.textContent }))
  )
  console.log('AUTRE FACE', await page.locator('.est-autre-face').count(), JSON.stringify(info))
})
