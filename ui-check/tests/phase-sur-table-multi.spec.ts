import { test, expect, errors } from '@playwright/test'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { questionOuPreparation } from '../pilote-phase-sur-table'

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'moteur de test séparé requis')
test.use({ reducedMotion: 'no-preference', viewport: { width: 1280, height: 720 } })

for (const politique of ['concerne', 'tous', 'quiconque'] as const) test(`deux sièges terminent la phase sur table — ${politique}`, async ({ page }, info) => {
  test.setTimeout(300_000)
  const req = page.request
  const scenario = await (await req.get('/get_scenario_json?klaw')).json()
  const heros = await Promise.all(['spider_man', 'she_hulk'].map(async (h) => JSON.stringify(await (await req.get('/get_hero_json?' + h)).json())))
  const charge = { campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [], encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])], hero_json: heros, rules: [...contrat.regles_partie_standard, 'mode_sandbox'], seed: 4321, timeout: 0 }
  expect((await req.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).ok()).toBe(true)
  await page.context().addInitScript(() => {
    localStorage.setItem('mc_phase_presentation', 'tris')
    localStorage.setItem('marvel-langue-choisie', '1')
    localStorage.setItem('marvel-langue', 'fr')
    localStorage.setItem('marvel-board-mode-phase-mechant', 'sur-table')
    localStorage.setItem('mc_aide_bulle_table', 'vue')
  })
  const distant = await page.context().newPage()
  const pages = [page, distant]
  await Promise.all(pages.map((p, i) => p.goto(`/app/board.html?p=${i}&multi=1`)))
  const monde = async () => (await (await req.get('/get_world?hot_seat&p=0')).json())
  for (let i = 0; i < 200; i++) {
    if (/^Player(?: \d+)? Turn$/.test((await monde()).phase)) break
    for (const p of pages) await questionOuPreparation(p)
    await page.waitForTimeout(100)
  }
  expect((await monde()).players).toHaveLength(2)
  await req.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001b')"] } })
  let commencee = false
  const lectures = [0, 0]
  const bilans = new Set<number>()
  for (let i = 0; i < 450 && bilans.size < 2; i++) {
    const w = await monde()
    commencee ||= ['Main Scheme Place Threat', 'Enemy Activation', 'Deal Encounter Cards', 'Reveal Encounter Cards'].includes(w.phase)
    if (i % 40 === 0) console.log('Multi', w.phase, await Promise.all(pages.map((p) => p.evaluate(() => ({ texte: document.querySelector('.tsm-bandeau')?.textContent, lectures: Array.from(document.querySelectorAll('.rencontre-sur-table')).map((e) => e.getAttribute('data-lecture')), acteurs: Array.from(document.querySelectorAll('.tsm-acteur')).map((e) => e.outerHTML) })))))
    for (const [siege, p] of pages.entries()) {
      if (bilans.has(siege)) continue
      if (await p.locator('.tsm-bandeau.est-bilan').count()) {
        bilans.add(siege)
        await p.screenshot({ path: info.outputPath(`bilan-siege-${siege}.png`) })
        // Attendre que les deux aient vu leur bilan avant de rendre la main.
        continue
      }
      const choixPolitique = p.locator(`[data-politique="${politique}"]`)
      if (await choixPolitique.count()) { await choixPolitique.click(); continue }
      const pret = p.locator('.tsm-multi [data-pret]:not([disabled])')
      if (await pret.count()) {
        if (await p.locator('.rencontre-sur-table[data-lecture="lecture"]').count()) lectures[siege]++
        await pret.click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); continue
      }
      const lecture = p.locator('.rencontre-sur-table[data-lecture="lecture"]')
      if (await lecture.count()) {
        const bouton = p.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])')
        if (await bouton.count()) { lectures[siege]++; await bouton.first().click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); continue }
      }
      if (await p.locator('.rencontre-sur-table:not([data-lecture="termine"])').count()) continue
      if (await p.locator('.tsm-bandeau.est-question').count()) { await questionOuPreparation(p); continue }
      await p.evaluate(() => {
        if (document.querySelector('.tsm-bandeau.est-question, .tsm-bandeau.est-bilan, .rencontre-sur-table:not([data-lecture="termine"])')) return
        document.querySelector<HTMLButtonElement>('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-question):not(.est-bilan) .tsm-bouton:not([disabled])')?.click()
      })
      if (!commencee) await questionOuPreparation(p, true)
    }
    await page.waitForTimeout(100)
  }
  expect([...bilans].sort(), 'chaque siège atteint le bilan').toEqual([0, 1])
  expect(lectures.every((n) => n > 0), 'chaque siège a lu des cartes').toBe(true)

})
