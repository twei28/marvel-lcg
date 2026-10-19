// T2 (19/10/2026) : le bandeau de question se pose par défaut en colonne contre le bord gauche, se déplace à la poignée
// (souris ET doigt), reste entier dans l'écran, retient sa place, se remet en place (double-clic ou bouton ⟲) et ne
// bloque jamais le clic sur la carte dorée ni sur les boutons.
import { test, expect, type Page } from '@playwright/test'
import { avancerJusqua, commandes, creerPartie, finDuTour, jusquAuTourJoueur, reglagesSurTable } from '../pilote-corrections'

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'moteur de test séparé requis')

const rect = (page: Page, sel: string) =>
  page.evaluate((s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height, r: r.right, b: r.bottom } }, sel)

async function monter(browser: import('@playwright/test').Browser, { width, height, tactile, base }: { width: number; height: number; tactile: boolean; base: string }) {
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: tactile, isMobile: tactile, reducedMotion: 'no-preference', baseURL: base })
  await reglagesSurTable(ctx)
  const page = await ctx.newPage()
  await creerPartie(page.request)
  await page.goto('/app/board.html?phase=sur-table')
  await jusquAuTourJoueur(page, page.request)
  await commandes(page.request, ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)"])
  await finDuTour(page)
  await avancerJusqua(page, (b) => /Qui défend/.test(b))
  await page.waitForTimeout(600)
  return { ctx, page }
}

async function glisser(page: Page, tactile: boolean, de: { x: number; y: number }, vers: { x: number; y: number }) {
  if (!tactile) {
    await page.mouse.move(de.x, de.y)
    await page.mouse.down()
    await page.mouse.move((de.x + vers.x) / 2, (de.y + vers.y) / 2, { steps: 6 })
    await page.mouse.move(vers.x, vers.y, { steps: 6 })
    await page.mouse.up()
    return
  }
  const cdp = await page.context().newCDPSession(page)
  const pt = (p: { x: number; y: number }) => [{ x: p.x, y: p.y, id: 1 }]
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: pt(de) })
  for (let i = 1; i <= 8; i++) {
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: pt({ x: de.x + ((vers.x - de.x) * i) / 8, y: de.y + ((vers.y - de.y) * i) / 8 }) })
  }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
}

for (const ecran of [
  { nom: 'souris-1280', width: 1280, height: 720, tactile: false },
  { nom: 'doigt-tablette', width: 1180, height: 820, tactile: true },
]) {
  test(`bandeau déplaçable — ${ecran.nom}`, async ({ browser }, info) => {
    test.setTimeout(240_000)
    const { ctx, page } = await monter(browser, { ...ecran, base: process.env.UI_CHECK_BASE! })
    const origine = (await rect(page, '.tsm-bandeau'))!
    const poignee = (await rect(page, '.tsm-bandeau .tsm-poignee'))!
    info.annotations.push({ type: 'mesures', description: `origine ${JSON.stringify(origine)} poignée ${JSON.stringify(poignee)}` })
    // Par défaut : colonne étroite contre le bord gauche, et la poignée est visible (cible ≥ 44 px au doigt).
    expect(origine.x, 'colonne contre le bord gauche').toBeLessThan(20)
    expect(origine.w, 'colonne étroite').toBeLessThanOrEqual(260)
    expect(poignee.w).toBeGreaterThan(20)
    if (ecran.tactile) expect(poignee.h, 'poignée tactile').toBeGreaterThanOrEqual(44)
    await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + `t2-bandeau-1-origine-${ecran.nom}.png` })

    // 1. Glisser vers le milieu de la table.
    const depart = { x: poignee.x + poignee.w / 2, y: poignee.y + poignee.h / 2 }
    await glisser(page, ecran.tactile, depart, { x: depart.x + 420, y: depart.y + 180 })
    const deplace = (await rect(page, '.tsm-bandeau'))!
    expect(deplace.x - origine.x, 'déplacé de ~420 px à droite').toBeGreaterThan(380)
    expect(deplace.y - origine.y, 'déplacé de ~180 px en bas').toBeGreaterThan(150)
    await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + `t2-bandeau-2-deplace-${ecran.nom}.png` })

    // 2. Glisser très loin : le bandeau reste ENTIER dans l'écran, jamais sur la barre du haut.
    const p2 = (await rect(page, '.tsm-bandeau .tsm-poignee'))!
    const d2 = { x: p2.x + p2.w / 2, y: p2.y + p2.h / 2 }
    for (const [dx, dy] of [[4000, 4000], [-4000, -4000], [4000, -4000]]) {
      const p = (await rect(page, '.tsm-bandeau .tsm-poignee'))!
      await glisser(page, ecran.tactile, { x: p.x + p.w / 2, y: p.y + p.h / 2 }, { x: Math.min(Math.max(p.x + p.w / 2 + dx, 2), ecran.width - 2), y: Math.min(Math.max(p.y + p.h / 2 + dy, 2), ecran.height - 2) })
      const r = (await rect(page, '.tsm-bandeau'))!
      info.annotations.push({ type: 'mesures', description: `coin (${dx},${dy}) : ${JSON.stringify(r)}` })
      expect(r.x, 'gauche ≥ 0').toBeGreaterThanOrEqual(-0.5)
      expect(r.y, 'haut ≥ 0').toBeGreaterThanOrEqual(-0.5)
      expect(r.r, 'droite ≤ largeur').toBeLessThanOrEqual(ecran.width + 0.5)
      expect(r.b, 'bas ≤ hauteur').toBeLessThanOrEqual(ecran.height + 0.5)
      const entete = (await rect(page, '.plateau-cadre'))
      if (entete) expect(r.y, 'sous la barre du haut').toBeGreaterThanOrEqual(entete.y - 0.5)
    }
    void d2
    await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + `t2-bandeau-3-coin-${ecran.nom}.png` })

    // 3. La place est retenue (localStorage) et revient à l'étape suivante.
    const retenu = await page.evaluate(() => window.localStorage.getItem('marvel-tsm-bandeau-place'))
    expect(retenu, 'place retenue dans localStorage').not.toBeNull()
    const avant = (await rect(page, '.tsm-bandeau'))!
    await page.reload()
    await page.waitForTimeout(1500)
    const apresRechargement = await rect(page, '.tsm-bandeau')
    if (apresRechargement) {
      expect(Math.abs(apresRechargement.x - avant.x), 'même place après rechargement').toBeLessThan(2)
      expect(Math.abs(apresRechargement.y - avant.y), 'même place après rechargement').toBeLessThan(2)
    }

    // 4. Double-clic sur la poignée : retour à la place d'origine.
    const p3 = (await rect(page, '.tsm-bandeau .tsm-poignee'))!
    await page.mouse.dblclick(p3.x + p3.w / 2, p3.y + p3.h / 2)
    await page.waitForTimeout(300)
    const remis = (await rect(page, '.tsm-bandeau'))!
    expect(Math.abs(remis.x - origine.x), 'remis en place (x)').toBeLessThan(2)
    expect(Math.abs(remis.y - origine.y), 'remis en place (y)').toBeLessThan(2)
    expect(await page.evaluate(() => window.localStorage.getItem('marvel-tsm-bandeau-place'))).toBeNull()

    // 5. Le petit bouton ⟲ remet aussi en place.
    const p4 = (await rect(page, '.tsm-bandeau .tsm-poignee'))!
    await glisser(page, ecran.tactile, { x: p4.x + p4.w / 2, y: p4.y + p4.h / 2 }, { x: p4.x + p4.w / 2 + 300, y: p4.y + p4.h / 2 + 100 })
    await expect(page.locator('.tsm-remise')).toHaveCount(1)
    const remise = (await rect(page, '.tsm-remise'))!
    if (ecran.tactile) expect(remise.h, 'bouton de remise tactile').toBeGreaterThanOrEqual(44)
    await page.locator('.tsm-remise').click()
    await page.waitForTimeout(300)
    const remis2 = (await rect(page, '.tsm-bandeau'))!
    expect(Math.abs(remis2.x - origine.x)).toBeLessThan(2)
    expect(Math.abs(remis2.y - origine.y)).toBeLessThan(2)

    // 6. Jamais d'obstacle : posé SUR la carte du héros, le bandeau laisse le clic atteindre la carte verte
    //    (le fond est transparent aux clics) ; les boutons du bandeau restent cliquables.
    const carte = (await rect(page, '.tsm-utilisable'))!
    const cx = carte.x + carte.w / 2, cy = carte.y + carte.h / 2
    const b0 = (await rect(page, '.tsm-bandeau'))!
    const ph = (await rect(page, '.tsm-bandeau .tsm-poignee'))!
    // Place le CENTRE du bandeau sur le centre de la carte (la poignée est en haut, loin du centre).
    await glisser(page, ecran.tactile, { x: ph.x + ph.w / 2, y: ph.y + ph.h / 2 }, { x: ph.x + ph.w / 2 + (cx - (b0.x + b0.w / 2)), y: ph.y + ph.h / 2 + (cy - (b0.y + b0.h / 2)) })
    const sur = await page.evaluate(([x, y]) => {
      const e = document.elementFromPoint(x!, y!)
      return { classe: e?.className?.toString() ?? '', dansBandeau: !!e?.closest('.tsm-bandeau') }
    }, [cx, cy])
    await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + `t2-bandeau-4-sur-la-carte-${ecran.nom}.png` })
    info.annotations.push({ type: 'mesures', description: `au centre de la carte : ${JSON.stringify(sur)}` })
    expect(sur.dansBandeau && !/tsm-bouton|tsm-poignee|tsm-remise/.test(sur.classe), 'le fond du bandeau ne capte pas le clic').toBe(false)
    // Les boutons du bandeau restent cliquables, même après déplacement.
    const refus = page.locator('.tsm-bandeau .tsm-bouton').first()
    const rb = (await refus.boundingBox())!
    const touche = await page.evaluate(([x, y]) => !!document.elementFromPoint(x!, y!)?.closest('.tsm-bouton'), [rb.x + rb.width / 2, rb.y + rb.height / 2])
    expect(touche, 'le bouton du bandeau reçoit le clic').toBe(true)
    await ctx.close()
  })
}
