// Rapport 130 (Yarro, 13/11/2026) : dejouer Seized! (6 cartes dessous) pose « Simultaneous Discard » et la partie boucle.
//   UI_CHECK_BASE=http://127.0.0.1:2346 SEIZED=1 npx playwright test tests/seized-ordre-defausse.spec.ts --project=pc
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { choisir, lireDemande, monde, repondre } from '../pilote-campagne'

test.skip(!process.env.SEIZED, 'cree une partie : SEIZED=1 et un moteur d’essai')
const SORTIE = path.resolve('..', 'captures', 'seized-ordre')

test('Seized! vaincu : la question de defausse simultanee', async ({ page }) => {
  test.setTimeout(180_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  const large = process.env.SEIZED_MOBILE ? { width: 390, height: 844 } : { width: 1600, height: 900 }
  await page.setViewportSize(large)
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?magneto')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?rocket_raccoon')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard, seed: 4321, timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript(() => {
    try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'normal') } catch { /* */ }
  })
  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)
  const evenement = async () => { const t = await (await request.get('/get_ask?p=0')).text(); return t.trim() ? JSON.parse(t) : undefined }
  for (let i = 0; i < 80; i++) {
    if ((await evenement())?.event_name === 'WhenPlayerInTurn') break
    await repondre(request, 0)
    await page.waitForTimeout(500)
  }
  const forme = (await lireDemande(request))?.options.find((o) => /^Change_?Form$/i.test(o.name))
  if (forme) { await choisir(request, forme); await page.waitForTimeout(3500) }
  const cmd = async (c: string) => { const r = await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); console.log('CMD', c, r.status()); await page.waitForTimeout(1200) }
  await cmd("Puzzle.PutIntoPlay('32158')")
  await cmd("Puzzle.SetThreat('32158', 2)")
  await cmd("Puzzle.PlaceUnder('01088', '32158')")
  await cmd("Puzzle.PlaceUnder('01089', '32158')")
  await cmd("Puzzle.PlaceUnder('01090', '32158')")
  const ids: Record<string, number[]> = {}
  const chercher = (n: any): void => {
    if (!n || typeof n !== 'object') return
    if (typeof n.card_id === 'string' && typeof n.id === 'number') (ids[n.card_id] ??= []).push(n.id)
    for (const v of Object.values(n)) chercher(v)
  }
  chercher(await monde(request))
  console.log('IDS seized', ids['32158'], 'rocket', ids['16029a'], ids['16029b'])
  let d = await lireDemande(request)
  console.log('OPTIONS', JSON.stringify(d?.options.map((o) => [o.id, o.name, o.bind_id, o.all_legal_targets])))
  const thwart = d?.options.find((o) => /^Thwart$/i.test(o.name))
  expect(thwart, 'option Thwart').toBeTruthy()
  const ciblesSeized = new Set(ids['32158'] ?? [])
  expect(await choisir(request, thwart!, [...ciblesSeized])).toBe(true)
  let ask
  for (let i = 0; i < 40; i++) {
    ask = await evenement()
    const noms = ask?.options_json ? JSON.parse(ask.options_json).map((o: any) => o.name) : []
    console.log('ETAPE', i, ask?.event_name, JSON.stringify(noms).slice(0, 200))
    if (noms.some((n: string) => /Simultaneous/i.test(n))) break
    if (ask && ask.event_name === 'WhenPlayerInTurn') break
    if (ask) await repondre(request, 0)
    await page.waitForTimeout(700)
  }
  // Correctif : aucune question d'ordre, le tour du joueur reprend, Seized! est parti et ses cartes sont en defausse.
  expect(ask?.event_name).toBe('WhenPlayerInTurn')
  const tout = JSON.stringify(await monde(request))
  expect(tout.includes('Simultaneous')).toBe(false)
  await page.waitForTimeout(2000)
  await page.screenshot({ path: path.join(SORTIE, `3-apres-correctif${process.env.SEIZED_MOBILE ? '-mobile' : ''}.png`) })
  console.log('FIN', ask?.event_name, 'BOUTONS', JSON.stringify(await page.getByRole('button').allInnerTexts()))
})
