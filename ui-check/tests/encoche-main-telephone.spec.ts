// Message d'un joueur (16/11/2026) : « j'ai replie ma main (cachee sur le cote a droite) et j'ai mis 5 mn a trouver ou elle etait. Elle se
// cachait en dessous des sur-menus « tchat et cie » ». L'encoche « Main » (z-index 45) passait SOUS les languettes Aide / Feuillets /
// Tchat / Journal (z-index 606 a 615) sur un telephone peu haut. Ce test replie la main sur de vrais gabarits de telephone et lit, au
// centre de l'encoche, QUEL element est reellement au-dessus (`elementFromPoint`).
//   UI_CHECK_BASE=http://127.0.0.1:2345 ENCOCHE_MAIN=1 npx playwright test tests/encoche-main-telephone.spec.ts --project=s24
// Affichage « Normal » = `epure`. Captures dans captures/encoche_main/.
import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'

test.skip(!process.env.ENCOCHE_MAIN, 'cree une partie')
const SORTIE = path.resolve('..', 'captures', 'encoche_main')
const GABARITS: Array<[number, number]> = [[360, 640], [360, 740], [390, 664], [390, 844], [412, 780], [480, 1050]]

test('la main repliee : son encoche n’est jamais cachee sous une languette', async ({ browser }) => {
  test.setTimeout(280_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  const bilan: string[] = []
  for (const [w, h] of GABARITS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, hasTouch: true, isMobile: true, deviceScaleFactor: 1 })
    const page = await ctx.newPage()
    page.setDefaultTimeout(10_000)
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
    await page.goto('/app/board.html', { waitUntil: 'networkidle' })
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
    // Replier la main : la fleche du dock, ou rien si elle est deja rangee derriere son encoche.
    const replier = page.getByRole('button', { name: /Replier la main/ })
    if (await replier.isVisible().catch(() => false)) {
      // La fleche ▼ du dock doit pouvoir se toucher : au centre, c'est elle (et pas une languette) qui est au-dessus.
      const toucheable = await page.evaluate(() => {
        const b = document.querySelector('.main-dock-replier') as HTMLElement | null
        if (!b) return null
        const r = b.getBoundingClientRect()
        const d = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2)
        return { ok: !!d && !!d.closest('.main-dock-replier'), dessus: d ? d.className.toString().slice(0, 50) : null }
      })
      await page.screenshot({ path: path.join(SORTIE, `dock-${w}x${h}.png`) })
      expect(toucheable?.ok, `${w}x${h} : la fleche « Replier la main » est sous « ${toucheable?.dessus} »`).toBe(true)
      await replier.tap(); await page.waitForTimeout(1000)
    }
    const mesure = await page.evaluate(() => {
      const e = document.querySelector('.encoche-main') as HTMLElement | null
      if (!e) return null
      const corps = (e.querySelector('.encoche-corps') as HTMLElement | null) ?? e
      const r = corps.getBoundingClientRect()
      // Le CORPS visible (24 x 72 px) est echantillonne en grille : quelle part est reellement au-dessus ?
      let vus = 0, total = 0; const mauvais = new Set<string>()
      for (let i = 0; i < 4; i++) for (let j = 0; j < 8; j++) {
        const px = r.left + 3 + (r.width - 6) * (i / 3)
        const py = r.top + 3 + (r.height - 6) * (j / 7)
        const d = document.elementFromPoint(px, py)
        total++; if (d && d.closest('.encoche-main')) vus++; else mauvais.add(d ? d.className.toString().slice(0, 40) : 'null')
      }
      const x = r.left + r.width / 2
      const y = r.top + r.height / 2
      const dessus = document.elementFromPoint(x, y) as HTMLElement | null
      const languettes = [...document.querySelectorAll('[class*="-languette"]')]
        .map((l) => { const b = (l as HTMLElement).getBoundingClientRect(); return { cls: (l as HTMLElement).className.toString().split(' ')[0], top: Math.round(b.top), bottom: Math.round(b.bottom) } })
        .filter((b) => b.bottom > 0 && b.top < innerHeight)
      // Les languettes du bord droit (hors textes internes) : meme taille que le corps des encoches, jamais l'une sur l'autre.
      const boites = [...document.querySelectorAll('[class*="-languette"]')]
        .filter((l) => /^volet-[a-z]+-languette$/.test((l as HTMLElement).className.toString().split(' ')[0]))
        .map((l) => { const b = (l as HTMLElement).getBoundingClientRect(); return { nom: (l as HTMLElement).className.toString().split(' ')[0].replace('volet-', '').replace('-languette', ''), l: Math.round(b.left), r: Math.round(b.right), t: Math.round(b.top), b: Math.round(b.bottom) } })
        .filter((b) => b.r - b.l > 0)
      boites.push({ nom: 'ENCOCHE-MAIN', l: Math.round(r.left), r: Math.round(r.right), t: Math.round(r.top), b: Math.round(r.bottom) })
      const chevauchements: string[] = []
      for (let i = 0; i < boites.length; i++) for (let j = i + 1; j < boites.length; j++) {
        const a = boites[i]!, c = boites[j]!
        if (a.l < c.r && c.l < a.r && a.t < c.b && c.t < a.b) chevauchements.push(`${a.nom}/${c.nom}`)
      }
      const tailles = boites.map((b) => `${b.nom}:${b.r - b.l}x${b.b - b.t}`)
      return { chevauchements, tailles, top: Math.round(r.top), bottom: Math.round(r.bottom), dessus: dessus ? dessus.className.toString().slice(0, 60) : null, estEncoche: !!dessus && !!dessus.closest('.encoche-main'), partVisible: Math.round((vus / total) * 100), mauvais: [...mauvais], zEncoche: getComputedStyle(e).zIndex, languettes }
    })
    bilan.push(`${w}x${h} ${JSON.stringify(mesure)}`); console.log('MESURE', w + 'x' + h, JSON.stringify(mesure))
    await page.screenshot({ path: path.join(SORTIE, `main-repliee-${w}x${h}.png`) })
    await ctx.close()
    expect(mesure, `${w}x${h} : pas d'encoche Main`).not.toBeNull()
    expect(mesure!.chevauchements, `${w}x${h} : des languettes se chevauchent`).toEqual([])
    for (const t of mesure!.tailles.filter((x) => !x.startsWith('ENCOCHE'))) expect(t.split(':')[1], `${w}x${h} : ${t} : meme taille que le corps de l'encoche (24x84)`).toBe('24x84')
    expect(mesure!.partVisible, `${w}x${h} : seulement ${mesure!.partVisible} % du corps de l'encoche Main est au-dessus (le reste est sous une languette)`).toBeGreaterThanOrEqual(90)
  }
  console.log('BILAN\n' + bilan.join('\n'))
})
