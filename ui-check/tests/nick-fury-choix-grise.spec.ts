// Bug 129 (12/11/2026) : Nick Fury joue sans menace nulle part -> le choix « retirer 2 menaces » se VOIT, grise, avec la raison.
//   UI_CHECK_BASE=http://127.0.0.1:2346 NICK_FURY=1 npx playwright test tests/nick-fury-choix-grise.spec.ts --project=pc
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { choisir, lireDemande, monde, repondre } from '../pilote-campagne'

test.skip(!process.env.NICK_FURY, 'cree une partie : NICK_FURY=1 et un moteur d’essai')
const SORTIE = path.resolve('..', 'captures', 'nick-fury-choix-grise')

test('le choix sans menace est montre grise, avec « aucune menace »', async ({ page }) => {
  test.setTimeout(180_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
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
    try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'normal') } catch { /* */ }
  })
  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)
  const evenement = async () => { const t = await (await request.get('/get_ask?p=0')).text(); return t.trim() ? JSON.parse(t) : undefined }
  for (let i = 0; i < 60; i++) {
    if ((await evenement())?.event_name === 'WhenPlayerInTurn') break
    await repondre(request, 0)
    await page.waitForTimeout(500)
  }
  const cmd = async (c: string) => { const r = await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); console.log('CMD', c, r.status()); await page.waitForTimeout(1500) }
  await cmd('Puzzle.EmptyHand()')
  await cmd("Puzzle.CreateHandCards('01084', '01088', '01089', '01090', '01091')")
  await cmd("Puzzle.SetThreat('01097b', 0)")
  await page.waitForTimeout(1500)

  const nicks: number[] = []
  const chercher = (n: any): void => {
    if (!n || typeof n !== 'object') return
    if (n.card_id === '01084' && typeof n.id === 'number') nicks.push(n.id)
    for (const v of Object.values(n)) chercher(v)
  }
  chercher(await monde(request))
  const nick = nicks.join(',')
  const demande = await lireDemande(request)
  console.log('NICK id', nick, 'OPTIONS', JSON.stringify(demande?.options.map((o) => [o.id, o.name, o.bind_id])))
  const jouer = demande?.options.find((o) => nicks.includes(o.bind_id))
  expect(jouer, 'option « jouer Nick Fury »').toBeTruthy()
  expect(await choisir(request, jouer!)).toBe(true)

  let ask
  for (let i = 0; i < 40; i++) {
    ask = await evenement()
    if (ask?.event_name === 'WhenPlayerChooseAbility') break
    await page.waitForTimeout(500)
  }
  console.log('ASK', ask?.event_name, 'OPTIONS', JSON.stringify(JSON.parse(ask?.options_json ?? '[]').map((o: any) => o.name)), 'REFUS', ask?.refus_json)
  expect(ask?.event_name).toBe('WhenPlayerChooseAbility')
  await page.waitForTimeout(3000)
  await page.screenshot({ path: path.join(SORTIE, '1-choix.png') })

  const grises = page.locator('[aria-disabled="true"]')
  const releve = await grises.evaluateAll((els) => els.map((e) => ({ texte: (e as HTMLElement).innerText, titre: e.getAttribute('title'), opacite: getComputedStyle(e).opacity, classe: e.className })))
  console.log('GRISES', JSON.stringify(releve))
  expect(releve.some((g) => /menace/i.test(g.titre ?? ''))).toBe(true)
  // Un clic sur le choix grise ne repond pas au moteur : la question reste posee.
  await grises.first().click({ force: true })
  await page.waitForTimeout(1500)
  expect((await evenement())?.event_name).toBe('WhenPlayerChooseAbility')
  await page.screenshot({ path: path.join(SORTIE, '2-apres-clic-grise.png') })
  console.log('BOUTONS', JSON.stringify(await page.getByRole('button').allInnerTexts()))
})
