// Parcours souris d'Empathetic Advantage (Mantis, 01/11/2026) : forme heros -> carte jouee -> paiement par l'identite -> choix de la carte Desorientee -> limite par round.
//   UI_CHECK_BASE=http://127.0.0.1:2351 MANTIS_AVANTAGE=1 npx playwright test tests/mantis-avantage.spec.ts --project=pc
import { test, expect, type APIRequestContext, type Page } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { lireDemande, monde, repondre } from '../pilote-campagne'

test.skip(!process.env.MANTIS_AVANTAGE, 'cree une partie : MANTIS_AVANTAGE=1 et un moteur d’essai')
const SORTIE = path.resolve('..', 'captures', 'mantis-avantage')

async function preparer(page: Page, confus: string[], main: string[]) {
  test.setTimeout(150_000)
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
  const cmd = async (c: string) => { const r = await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); console.log('CMD', c, r.status()); await page.waitForTimeout(1500) }
  await page.mouse.click(320, 600)
  await page.waitForTimeout(1500)
  await page.getByRole('button', { name: /changer de forme/i }).click()
  await page.waitForTimeout(3500)
  await cmd('Puzzle.EmptyHand()')
  await cmd(`Puzzle.CreateHandCards(${main.map((c) => `'${c}'`).join(', ')})`)
  for (const c of confus) await cmd(`Puzzle.Confuse('${c}')`)
  return { request, cmd }
}

async function statuts(request: APIRequestContext) {
  const m = await monde(request)
  const tout = JSON.stringify(m)
  const i = tout.indexOf('"01172"')
  if (process.env.DEBUG_STATUTS && i >= 0) console.log('SNIPPET', tout.slice(i - 100, i + 700))
  const confus = (id: string) => new RegExp(`"card_id":\\s*"${id}"[^]{0,2500}?onfus`).test(tout)
  return { rhino: confus('01094'), mantis: confus('mt001a'), merc: confus('01172') }
}

async function payerMindlock(page: Page, request: APIRequestContext, nom: string, puis: () => Promise<void>) {
  await page.mouse.click(770, 830) // la carte de la main (Psionic Mindlock, seule)
  await page.waitForTimeout(1500)
  await page.mouse.click(799, 438)
  await page.waitForTimeout(2000)
  await page.screenshot({ path: path.join(SORTIE, `${nom}-1-paiement.png`) })
  const q = JSON.parse((await (await request.get('/get_ask?p=0')).text()) || '{}')
  console.log(nom, 'PAIEMENT-ASK', JSON.stringify(q).slice(0, 1800))
  await puis()
}

test('B : seul Mantis est confus, carte a 1 : origine personnage', async ({ page }) => {
  const { request } = await preparer(page, ['mt001a'], ['mt009'])
  console.log('B avant', JSON.stringify(await statuts(request)))
  await payerMindlock(page, request, 'B', async () => {
    await page.mouse.click(320, 590)
    await page.waitForTimeout(2000)
    await page.screenshot({ path: path.join(SORTIE, 'B-2-clic-mantis.png') })
    console.log('B boutons', JSON.stringify(await page.getByRole('button').allInnerTexts()))
    await page.mouse.move(800, 250)
    const valider = page.getByRole('button', { name: /jouer psionic/i })
    if (await valider.isVisible().catch(() => false)) await valider.click() // sinon le jeu a deja paye tout seul
    await page.waitForTimeout(2500)
    await page.screenshot({ path: path.join(SORTIE, 'B-3-valide.png') })
  })
  console.log('B apres', JSON.stringify(await statuts(request)))
})

test('C : Rhino ET Mantis confus, carte a 1 : un second toucher sur Mantis passe a la source personnage', async ({ page }) => {
  const { request } = await preparer(page, ['mt001a', '01094'], ['mt009'])
  console.log('C avant', JSON.stringify(await statuts(request)))
  await payerMindlock(page, request, 'C', async () => {
    await page.mouse.click(320, 590)
    await page.waitForTimeout(1200)
    await page.screenshot({ path: path.join(SORTIE, 'C-2a-premier-toucher.png') })
    await page.mouse.click(320, 590)
    await page.waitForTimeout(2000)
    await page.screenshot({ path: path.join(SORTIE, 'C-2-clic-mantis.png') })
    console.log('C boutons', JSON.stringify(await page.getByRole('button').allInnerTexts()))
    await page.mouse.move(800, 250)
    const valider = page.getByRole('button', { name: /jouer psionic/i })
    if (await valider.isVisible().catch(() => false)) await valider.click() // sinon le jeu a deja paye tout seul
    await page.waitForTimeout(2500)
    await page.screenshot({ path: path.join(SORTIE, 'C-3-valide.png') })
  })
  console.log('C apres', JSON.stringify(await statuts(request)))
})

test('D : choix de la carte Desorientee a defausser, puis limite une fois par round', async ({ page }) => {
  const { request, cmd } = await preparer(page, [], ['mt009', 'mt009'])
  await cmd("Puzzle.PutIntoPlay('01172')")
  await cmd("Puzzle.Confuse('01094')")
  await cmd("Puzzle.Confuse('01172')")
  const jouerMindlock = async (nom: string) => {
    const carte = page.locator('article[aria-label^="Psionic Mindlock"]').last()
    const box = await carte.boundingBox()
    if (!box) throw new Error('Mindlock absente de la main')
    await page.mouse.click(box.x + box.width / 2, box.y + 8)
    await page.waitForTimeout(1500)
    await page.getByRole('button', { name: /^jouer$/i }).click()
    await page.waitForTimeout(2000)
    const non = page.getByRole('button', { name: /non, je clique moi-m/i })
    if (await non.isVisible().catch(() => false)) { await non.click(); await page.waitForTimeout(1200) }
    await page.screenshot({ path: path.join(SORTIE, `D-${nom}-1-paiement.png`) })
    console.log('D', nom, 'boutons paiement', JSON.stringify(await page.getByRole('button').allInnerTexts()))
  }
  console.log('D avant', JSON.stringify(await statuts(request)))
  await jouerMindlock('premier')
  await page.mouse.click(320, 590) // Mantis
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, 'D-premier-2-mantis.png') })
  await page.mouse.move(800, 250)
  await page.getByRole('button', { name: /jouer psionic/i }).click()
  await page.waitForTimeout(2500)
  await page.screenshot({ path: path.join(SORTIE, 'D-premier-3-choix.png') })
  const q = JSON.parse((await (await request.get('/get_ask?p=0')).text()) || '{}')
  console.log('D choix', q.event_name, q.prompt_text, (q.options_json ?? '').slice(0, 500))
  console.log('D apres 1', JSON.stringify(await statuts(request)))
  console.log('D boutons choix', JSON.stringify(await page.getByRole('button').allInnerTexts()))
  await page.getByRole('button', { name: /empathetic advantage : d[ée]fausser/i }).click()
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, 'D-premier-3b-banniere.png') })
  await page.mouse.click(320, 160) // Rhino
  await page.waitForTimeout(1200)
  await page.screenshot({ path: path.join(SORTIE, 'D-premier-3c-rhino-vise.png') })
  await page.getByRole('button', { name: /empathetic advantage : d[ée]fausser/i }).click()
  await page.waitForTimeout(2500)
  await page.screenshot({ path: path.join(SORTIE, 'D-premier-4-rhino-choisi.png') })
  console.log('D apres choix Rhino', JSON.stringify(await statuts(request)), JSON.stringify(await page.getByRole('button').allInnerTexts()), ((await (await request.get('/get_ask?p=0')).text()) || '').slice(0, 300))
  // Seconde carte dans le MEME round : l'identite ne doit plus pouvoir payer (limite une fois par round), alors que Whiplash est toujours desoriente.
  await jouerMindlock('second')
  await page.mouse.click(320, 590)
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(SORTIE, 'D-second-2-mantis.png') })
  console.log('D second boutons', JSON.stringify(await page.getByRole('button').allInnerTexts()))
  console.log('D second statuts', JSON.stringify(await statuts(request)))
})
