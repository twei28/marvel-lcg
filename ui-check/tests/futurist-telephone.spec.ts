import { test, expect } from '@playwright/test'
import fs from 'node:fs'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { repondre } from '../pilote-campagne'
test.use({ viewport: { width: 360, height: 760 }, hasTouch: true, isMobile: true })
test.skip(!process.env.FUTURIST_TEL, 'cree une partie')
test('telephone : la question « Futuriste » ne recouvre pas les cartes regardees, et se lit en francais', async ({ page }) => {
  test.setTimeout(240_000)
  fs.mkdirSync('../captures/futurist_telephone', { recursive: true })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario), campaign_log: {}, challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?iron_man')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard, seed: 4321, timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript(() => { try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'epure') } catch { /* */ } })
  await page.goto('/app/board.html', { waitUntil: 'networkidle', timeout: 90_000 })
  await page.waitForTimeout(2500)
  for (let i = 0; i < 60; i++) {
    const t = await (await request.get('/get_ask?p=0')).text()
    if (t.trim() && JSON.parse(t).event_name === 'WhenPlayerInTurn') break
    await repondre(request, 0); await page.waitForTimeout(500)
  }
  await page.waitForTimeout(2500)
  const choix = page.getByRole('button', { name: /^Ronds/ }); if (await choix.isVisible().catch(() => false)) { await choix.click(); await page.waitForTimeout(1200) }
  await page.screenshot({ path: '../captures/futurist_telephone/0.png' })
  for (let i = 0; i < 8; i++) {
    const passer = page.getByRole('button', { name: /^Passer$/ })
    if (!(await passer.isVisible().catch(() => false))) break
    await passer.click(); await page.waitForTimeout(500)
  }
  await page.mouse.click(48, 270)  // le rond du heros
  await page.waitForTimeout(1500)
  await page.screenshot({ path: '../captures/futurist_telephone/1-carte.png' })
  await page.getByRole('button', { name: /Utiliser cette carte/ }).click()
  await page.waitForTimeout(2500)
  await page.screenshot({ path: '../captures/futurist_telephone/2-menu.png' })
  console.log('BTNS', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('button')].map((b) => (b.textContent ?? '').trim()).filter(Boolean).slice(0, 20))))
  const act = page.getByRole('button', { name: /^Futuriste?$/i }).first()
  if (await act.count()) { await act.click().catch(() => undefined); await page.waitForTimeout(3000) }
  await page.screenshot({ path: '../captures/futurist_telephone/3-regard.png' })
  // Depuis le 18/11/2026 (rapport #152), une SEULE feuille « Choisis une carte » s'ouvre sur les 3 cartes regardees.
  const mesure = await page.evaluate(() => {
    const r = (s: string) => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return { top: Math.round(b.top), bottom: Math.round(b.bottom) } }
    return { entete: r('.plateau-selecteur.est-fenetre .plateau-selecteur-entete'), cartes: r('.plateau-selecteur.est-fenetre .plateau-selecteur-cartes'), boutons: r('.plateau-selecteur.est-fenetre .plateau-selecteur-boutons'), nb: document.querySelectorAll('.plateau-selecteur.est-fenetre .scan-card').length }
  })
  console.log('MESURE', JSON.stringify(mesure))
  expect(mesure.nb, 'les 3 cartes regardees').toBe(3)
  // 1. L'en-tete n'est pas recouvert par les cartes (revérification du 19/11/2026 : l'étiquette « ÉVÉNEMENT » cachait « FUTURISTE »).
  expect(mesure.entete!.bottom - mesure.entete!.top, 'en-tete visible').toBeGreaterThan(20)
  expect(mesure.cartes!.top, 'les cartes commencent sous l en-tete').toBeGreaterThanOrEqual(mesure.entete!.bottom - 1)
  // 2. La derniere carte s'atteint en faisant defiler, au-dessus des boutons.
  await page.evaluate(() => { const c = document.querySelector('.plateau-selecteur.est-fenetre .plateau-selecteur-cartes') as HTMLElement | null; if (c) c.scrollTop = c.scrollHeight })
  await page.waitForTimeout(500)
  const dernier = await page.evaluate(() => { const cartes = [...document.querySelectorAll('.plateau-selecteur.est-fenetre .scan-card')]; const c = cartes[cartes.length - 1]?.getBoundingClientRect(); const b = document.querySelector('.plateau-selecteur.est-fenetre .plateau-selecteur-boutons')?.getBoundingClientRect(); return c && b ? { bas: Math.round(c.bottom), hautBoutons: Math.round(b.top) } : null })
  expect(dernier, 'la derniere carte').not.toBeNull()
  expect(dernier!.bas, 'la derniere carte se voit en entier au-dessus des boutons').toBeLessThanOrEqual(dernier!.hautBoutons + 1)
  // 3. En francais.
  const texte = await page.locator('.plateau-selecteur.est-fenetre').innerText()
  expect(texte.toLowerCase()).toContain('futuriste')
  expect(texte).not.toMatch(/Futurist\b(?!e)/)
  expect(texte).toMatch(/Choisis une carte/i)
  await page.screenshot({ path: '../captures/futurist_telephone/4-fin.png' })
})
