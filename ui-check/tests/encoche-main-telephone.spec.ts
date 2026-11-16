// Message d'un joueur (16/11/2026) : « j'ai replie ma main (cachee sur le cote a droite) et j'ai mis 5 mn a trouver ou elle etait. Elle se
// cachait en dessous des sur-menus « tchat et cie » » ; puis l'utilisateur : « le bouton chat est sur la main... le journal, aide et tout, ils
// gachent trop les trucs principaux, c'est-a-dire la main et les piles ». Decision : sur telephone, les languettes du bord droit (Aide,
// Feuillets, Tchat, Journal) sont rangees dans le menu « … » ; il ne reste, sur les cotes, que la main et les piles.
//   UI_CHECK_BASE=http://127.0.0.1:2345 ENCOCHE_MAIN=1 npx playwright test tests/encoche-main-telephone.spec.ts --project=s24
// Affichage « Normal » = `epure`. Captures dans captures/encoche_main/.
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.ENCOCHE_MAIN, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'encoche_main')
const GABARITS: Array<[number, number]> = [[360, 640], [390, 664], [390, 844], [412, 780], [480, 1050]]

test('telephone : plus de languette sur la main ; les volets s’ouvrent depuis le menu « … »', async ({ browser }) => {
  test.setTimeout(900_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  const bilan: string[] = []
  for (const [w, h] of GABARITS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 1 })
    const page = await ctx.newPage()
    page.setDefaultTimeout(40_000)
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
      try {
        localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'epure')
        localStorage.removeItem('marvel-encoche-droite')
      } catch { /* */ }
    })
    await page.goto('/app/board.html', { waitUntil: 'networkidle', timeout: 90_000 })
    await page.waitForTimeout(2500)
    for (let i = 0; i < 60; i++) {
      const t = await (await request.get('/get_ask?p=0')).text()
      if (t.trim() && JSON.parse(t).event_name === 'WhenPlayerInTurn') break
      await repondre(request, 0)
      await page.waitForTimeout(500)
    }
    await page.waitForTimeout(2500)
    const choix = page.getByRole('button', { name: /^Ronds/ })
    if (await choix.isVisible().catch(() => false)) { await choix.click(); await page.waitForTimeout(1200) }
    for (let i = 0; i < 8; i++) {
      const passer = page.getByRole('button', { name: /^Passer$/ })
      if (!(await passer.isVisible().catch(() => false))) break
      await passer.click(); await page.waitForTimeout(500)
    }
    const replier = page.getByRole('button', { name: /Replier la main/ })
    if (await replier.isVisible().catch(() => false)) { await replier.tap(); await page.waitForTimeout(1000) }

    // 1. Aucune languette du bord droit n'est visible : rien ne couvre plus la main ni les piles.
    const visibles = await page.evaluate(() =>
      [...document.querySelectorAll('[class*="-languette"]')]
        .filter((l) => /^volet-[a-z]+-languette$/.test((l as HTMLElement).className.toString().split(' ')[0]))
        .filter((l) => { const b = (l as HTMLElement).getBoundingClientRect(); return b.width > 0 && b.height > 0 && getComputedStyle(l as HTMLElement).visibility !== 'hidden' })
        .map((l) => (l as HTMLElement).className.toString().split(' ')[0])
    )
    // 2. L'encoche « Main » est entierement au-dessus de tout (grille d'echantillons).
    const main = await page.evaluate(() => {
      const e = document.querySelector('.encoche-main') as HTMLElement | null
      if (!e) return null
      const corps = (e.querySelector('.encoche-corps') as HTMLElement | null) ?? e
      const r = corps.getBoundingClientRect()
      let vus = 0, total = 0
      for (let i = 0; i < 4; i++) for (let j = 0; j < 8; j++) {
        const d = document.elementFromPoint(r.left + 3 + (r.width - 6) * (i / 3), r.top + 3 + (r.height - 6) * (j / 7))
        total++; if (d && d.closest('.encoche-main')) vus++
      }
      return { part: Math.round((vus / total) * 100), top: Math.round(r.top), bottom: Math.round(r.bottom), droite: Math.round(r.right) }
    })
    bilan.push(`${w}x${h} visibles=${JSON.stringify(visibles)} main=${JSON.stringify(main)}`)
    console.log('MESURE', w + 'x' + h, JSON.stringify({ visibles, main }))
    await page.screenshot({ path: path.join(SORTIE, `main-repliee-${w}x${h}.png`) })
    expect(visibles, `${w}x${h} : des languettes du bord droit sont encore visibles`).toEqual([])
    expect(main, `${w}x${h} : pas d'encoche Main`).not.toBeNull()
    expect(main!.part, `${w}x${h} : l'encoche Main est recouverte`).toBeGreaterThanOrEqual(95)

    // 3. Le menu « … » porte les volets ; un clic sur « Journal » ouvre le volet et referme le menu.
    if (w === 390 && h === 844) {
      await page.locator('.portrait-menu-bouton').tap()
      await page.waitForTimeout(800)
      await page.screenshot({ path: path.join(SORTIE, 'menu-avec-volets.png') })
      for (const nom of ['Aide', 'Tchat', 'Journal']) {
        await expect(page.locator('.portrait-menu .bh-volet', { hasText: new RegExp(`^${nom}`) }), `ligne « ${nom} » du menu`).toHaveCount(1)
      }
      await page.locator('.portrait-menu .bh-volet', { hasText: /^Journal/ }).tap()
      await page.waitForTimeout(1200)
      await expect(page.locator('.portrait-menu'), 'le menu se referme').toHaveCount(0)
      await expect(page.locator('.volet-journal'), 'le volet Journal est ouvert').toHaveCount(1)
      await page.screenshot({ path: path.join(SORTIE, 'journal-ouvert-depuis-le-menu.png') })
    }
    await ctx.close()
  }
  console.log('BILAN\n' + bilan.join('\n'))
})
