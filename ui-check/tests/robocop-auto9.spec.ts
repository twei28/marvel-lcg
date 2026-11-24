// Parcours Auto-9 de RoboCop a la souris (01/11/2026) : alter ego -> heros -> menu de l'identite -> Auto-9 -> cible -> paiement.
//   UI_CHECK_BASE=http://127.0.0.1:2351 ROBOCOP_AUTO9=1 npx playwright test tests/robocop-auto9.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { choisir, lireDemande, monde, repondre } from '../pilote-campagne'

test.skip(!process.env.ROBOCOP_AUTO9, 'cree une partie : ROBOCOP_AUTO9=1 et un moteur d’essai')
const SORTIE = path.resolve('..', 'captures', 'robocop-auto9')

test('Auto-9 : menu, cible, paiement', async ({ page }) => {
  await parcours(page, false)
})

test('Auto-9 avec la main VIDE : proposee mais impayable', async ({ page }) => {
  await parcours(page, true)
})

async function parcours(page: Page, mainVide: boolean) {
  test.setTimeout(90_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?robocop')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard, seed: 4321, timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript(() => {
    try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'normal') } catch { /* */ }
  })
  // Mise en place SANS repondre a la question du tour (le pilote commun choisit « Action » et ouvre la recherche d'Alex Murphy).
  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)
  for (let i = 0; i < 60; i++) {
    const t = await (await request.get('/get_ask?p=0')).text()
    if (t.trim() && JSON.parse(t).event_name === 'WhenPlayerInTurn') break
    await repondre(request, 0)
    await page.waitForTimeout(500)
  }
  await page.waitForTimeout(3000)
  const cmd = async (c: string) => { const r = await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); console.log('CMD', c, r.status()); await page.waitForTimeout(1500) }
  await cmd("Puzzle.PutIntoPlay('rc005')")
  if (mainVide) await cmd('Puzzle.EmptyHand()')
  const dd = await lireDemande(request)
  console.log('OPTIONS', JSON.stringify(dd?.options.map((o) => [o.name, o.id, o.bind_id])))
  await page.screenshot({ path: path.join(SORTIE, '1-depart.png') })
  await page.mouse.click(320, 600)
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '2-menu-alterego.png') })
  await page.getByRole('button', { name: /changer de forme/i }).click()
  await page.waitForTimeout(3500)
  await page.mouse.click(320, 600)
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '3-menu-heros.png') })
  const d3 = await lireDemande(request)
  console.log('BOUTONS', JSON.stringify(await page.getByRole('button').allInnerTexts()))
  const a9 = page.getByRole('button').filter({ hasText: 'Auto-9' }).first()
  console.log('A9HTML', await a9.evaluate((e) => e.outerHTML.slice(0, 500)))
  console.log('BOX', JSON.stringify(await a9.boundingBox()))
  await page.mouse.click(799, 392) // la croix du menu
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '4-menu-ferme.png') })
  await page.mouse.click(418, 560)
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '5-clic-auto9.png') })
  console.log('OPTIONS4', JSON.stringify((await lireDemande(request))?.options.map((o) => [o.name, o.id, o.bind_id])))
  await page.mouse.click(799, 438) // le bouton AUTO-9
  await page.waitForTimeout(2000)
  await page.screenshot({ path: path.join(SORTIE, '6-cible.png') })
  const q = JSON.parse(await (await request.get('/get_ask?p=0')).text())
  console.log('Q6', q.event_name, q.prompt_text, q.show_cancel, (q.options_json ?? '').slice(0, 600))
  if (mainVide) {
    await page.waitForTimeout(1500)
    await page.screenshot({ path: path.join(SORTIE, '7-main-vide.png') })
    const qv = JSON.parse((await (await request.get('/get_ask?p=0')).text()) || '{}')
    console.log('VIDE', qv.event_name, qv.prompt_text, qv.show_cancel)
    console.log('VIDEBOUTONS', JSON.stringify(await page.getByRole('button').allInnerTexts()))
    await page.mouse.click(692, 440) // ANNULER
    await page.waitForTimeout(2000)
    await page.screenshot({ path: path.join(SORTIE, '8-main-vide-annule.png') })
    const m2 = await monde(request)
    const a9 = (m2.players[0].area_hero as any[]).find((c) => c.card_id === 'rc005')
    const d9 = await lireDemande(request)
    console.log('VIDEANNULE ready', a9?.is_ready, JSON.stringify(d9?.options.map((o) => o.name)), 'panneau', await page.getByText(/Il manque/).count())
    return
  }
  const avant = await monde(request)
  const main0 = (avant.players[0].hand_cards as any[]).map((c) => c.card_id)
  await page.mouse.click(567, 805) // Squad Car (ressource energie) : paiement en cliquant la carte
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, '7-paye.png') })
  await page.waitForTimeout(1500)
  const apres = await monde(request)
  const ar = JSON.stringify(apres).match(/"card_id": "01094"[^]{0,900}/)
  console.log('MAIN avant', JSON.stringify(main0))
  console.log('MAIN apres', JSON.stringify((apres.players[0].hand_cards as any[]).map((c) => c.card_id)))
  console.log('DEFAUSSE', JSON.stringify((apres.players[0].player_discard_pile as any[]).map((c) => c.card_id)))
  console.log('RHINO', JSON.stringify(ar)?.slice(0, 400))
  const auto9 = (apres.players[0].area_hero as any[]).find((c) => c.card_id === 'rc005')
  console.log('AUTO9 ready', auto9?.is_ready)
}
