// « ANNULER » PAR INSTANTANE (29/10/2026) : le bouton de la barre explique avant
// d'agir (info-bulle au survol, puis fenetre avec case « ne plus me montrer ça »),
// et le moteur remet la partie comme avant l'action SANS la rejouer.
//
// Le moteur trace « === Annuler : instantane restaure === » dans son journal
// quand il restaure : c'est la seule preuve que le rejeu n'a pas servi. Ce test,
// lui, mesure ce que le joueur voit : le monde d'avant, a l'identique.
//
// ⚠ JAMAIS SUR LE 2345 (la partie du joueur) : le cas cree une partie.
//   UI_CHECK_BASE=http://127.0.0.1:2346 ANNULER_INSTANTANE=1 \
//     npx playwright test tests/annuler-instantane.spec.ts --project=pc
import { test, expect, type APIRequestContext, type Page } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { choisir, lireDemande, monde, ouvrirEtMettreEnPlace } from '../pilote-campagne'

test.skip(!process.env.ANNULER_INSTANTANE, 'cree une partie : ANNULER_INSTANTANE=1 et un moteur d’essai')

const SORTIE = path.resolve('..', '.planning', 'captures-annuler-instantane')

type Brut = { event_name?: string }

async function attendreQuestionDuTour(request: APIRequestContext): Promise<void> {
  for (let i = 0; i < 120; i++) {
    const brut = await (await request.get('/get_ask?p=0')).text()
    try {
      if ((JSON.parse(brut) as Brut).event_name === 'WhenPlayerInTurn') return
    } catch {
      /* pas encore de question */
    }
    await new Promise((r) => setTimeout(r, 500))
  }
  throw new Error('la question du tour n’est jamais venue')
}

/** Le monde sans ce qui change tout seul d'une trame a l'autre. */
async function empreinte(request: APIRequestContext): Promise<string> {
  const m = (await monde(request)) as Record<string, unknown>
  return JSON.stringify(m, (cle, valeur) =>
    ['render_id', 'frame', 'pause_epoch', 'timestamp', 'time', 'step_id', 'current_step_id', 'ask_id', 'is_new'].includes(cle) ? undefined : valeur
  )
}

async function agir(request: APIRequestContext): Promise<void> {
  await attendreQuestionDuTour(request)
  // Une action qui change la table : attaquer, changer de forme, sinon jouer une carte payable. Apres une attaque
  // le heros est epuise : il ne reste que les cartes.
  const options = (await lireDemande(request))?.options ?? []
  const candidates = [
    ...options.filter((o) => /^Attack$/i.test(o.name)),
    ...options.filter((o) => /^Change[ _]Form$/i.test(o.name)),
    ...options.filter((o) => /^Play$/i.test(o.name)),
  ]
  expect(candidates.length, `aucune action jouable (${options.map((o) => o.name).join(', ')})`).toBeGreaterThan(0)
  const avant = await (await request.get('/get_ask?p=0')).text()
  let joue = false
  for (const option of candidates) {
    if (await choisir(request, option)) {
      joue = true
      break
    }
  }
  expect(joue, 'aucune action payable').toBe(true)
  // Juste apres la reponse, `/get_ask` sert encore l'ancienne question : on attend qu'elle change.
  for (let i = 0; i < 40 && (await (await request.get('/get_ask?p=0')).text()) === avant; i++) {
    await new Promise((r) => setTimeout(r, 250))
  }
  await attendreQuestionDuTour(request)
}

async function partie(page: Page) {
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario),
    campaign_log: {},
    challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?spider_man')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321,
    timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript(() => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1')
      localStorage.setItem('marvel-langue', 'fr')
      localStorage.setItem('mc_affichage_v1', 'normal')
      localStorage.removeItem('marvel-board-annuler-explique')
    } catch {
      /* */
    }
  })
  await ouvrirEtMettreEnPlace(page, request)
}

test('Annuler explique, puis remet la partie comme avant l’action', async ({ page }) => {
  test.setTimeout(300_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  const request = page.request
  await partie(page)

  // Deux actions : la premiere donne l'instantane vers lequel on revient.
  await agir(request)
  const avantSecondeAction = await empreinte(request)
  await agir(request)
  expect(await empreinte(request), 'premisse : la seconde attaque doit changer la table').not.toBe(avantSecondeAction)

  // 1. L'info-bulle apparait au survol (et pas avant).
  const bouton = page.locator('.bh-undo')
  const opacite = () => bouton.evaluate((el) => getComputedStyle(el, '::after').opacity)
  expect(await opacite()).toBe('0')
  await bouton.hover()
  await expect.poll(opacite, { timeout: 3000 }).toBe('1')
  expect(await bouton.getAttribute('data-infobulle')).toMatch(/Instantané pendant ton tour/)
  await page.screenshot({ path: path.join(SORTIE, 'infobulle.png') })

  // 2. La fenetre explique avant d'agir ; « Garder mon coup » n'annule rien.
  await bouton.click()
  const modale = page.getByRole('alertdialog')
  await expect(modale).toBeVisible()
  await expect(modale).toContainText('instantané')
  await page.screenshot({ path: path.join(SORTIE, 'modale.png') })
  await page.getByRole('button', { name: 'Garder mon coup' }).click()
  await expect(modale).toHaveCount(0)
  expect(await empreinte(request), '« Garder mon coup » ne doit rien annuler').not.toBe(avantSecondeAction)

  // 3. Case cochee + « Oui, annuler » : la table redevient celle d'avant la seconde action.
  await bouton.click()
  await page.getByRole('checkbox').check()
  const debut = Date.now()
  await page.getByRole('button', { name: 'Oui, annuler' }).click()
  await expect(modale).toHaveCount(0)
  await attendreQuestionDuTour(request)
  await expect.poll(() => empreinte(request), { timeout: 30_000 }).toBe(avantSecondeAction)
  console.log(`annulation en ${Date.now() - debut} ms`)

  // 4. La case est memorisee : plus de fenetre, l'annulation part directement.
  await agir(request)
  const avantTroisieme = await empreinte(request)
  await agir(request)
  await bouton.click()
  await expect(page.getByRole('alertdialog')).toHaveCount(0)
  await attendreQuestionDuTour(request)
  await expect.poll(() => empreinte(request), { timeout: 30_000 }).toBe(avantTroisieme)
})
