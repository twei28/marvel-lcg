import * as L from './lib.mjs'
import fs from 'fs'
const tailles = [['pc', 1280, 720, false], ['paysage', 1050, 480, true], ['tablette', 1180, 820, true], ['iphone-paysage', 844, 390, true], ['mobile', 390, 844, true]]
const res = {}
for (const [nom, w, h, tac] of tailles) {
  await L.nouvellePartie({ scenario: 'klaw' })
  const { browser, ctx } = await L.contexte({ w, h, tactile: tac })
  const page = await L.ouvrir(ctx)
  await L.attendreTourJoueur([page])
  await L.cmd(["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)", "Puzzle.PutIntoPlay('01075', under_control=True)"])
  await L.sleep(800)
  const finTour = await page.evaluate(() => { const b = [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent)); if (!b) return null; const r = b.getBoundingClientRect(); const e = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); return { w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y), cliquable: e === b || b.contains(e), couvertPar: e && !b.contains(e) ? (e.closest('section,div')?.className || e.tagName) : null } })
  try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) }
  let mes = null
  for (let i = 0; i < 500 && !mes; i++) {
    const sig = await L.signature(page)
    if (i % 10 === 0) console.log(nom, i, (await L.monde()).phase, sig.bandeau.slice(0, 80), '|', sig.demande.slice(0, 60))
    if (/Qui défend/.test(sig.bandeau)) {
      await L.sleep(500)
      mes = await page.evaluate(() => {
        const rect = (e) => { const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height } }
        const q = (sel) => [...document.querySelectorAll(sel)].filter((e) => e.getBoundingClientRect().width > 0).map(rect)
        const et = q('.tsm-etiquette'); const chevauche = []
        for (let i = 0; i < et.length; i++) for (let j = i + 1; j < et.length; j++) { const a = et[i], b = et[j]; const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x); const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y); if (ox > 1 && oy > 1) chevauche.push([i, j, Math.round(ox), Math.round(oy)]) }
        const mini = (arr) => arr.length ? { n: arr.length, minW: Math.round(Math.min(...arr.map((r) => r.w))), minH: Math.round(Math.min(...arr.map((r) => r.h))) } : null
        const band = document.querySelector('.tsm-bandeau')
        const cs = band ? getComputedStyle(band.querySelector('.tsm-phrase') || band) : null
        const boutons = q('.tsm-bandeau .tsm-bouton')
        const cartes = q('.plateau-cadre .scan-card').filter((r) => r.w > 20)
        return { viewport: [innerWidth, innerHeight], etiquettes: mini(et), chevauchements: chevauche, utilisables: mini(q('.tsm-utilisable')), boutonsBandeau: mini(boutons), policePhrase: cs && cs.fontSize, cartesTable: mini(cartes), bandeau: band ? rect(band) : null }
      })
      await page.screenshot({ path: `${L.OUT}/mesure-${nom}.png` })
      break
    }
    if (sig.lecture === 'lecture') { await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {}) }
    else if (!sig.question && !sig.demande && !sig.lecture && sig.bandeau) await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click())
    else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
    await L.sleep(250)
  }
  res[nom] = { finTour, defense: mes }
  console.log(nom, JSON.stringify(res[nom]))
  await browser.close()
}
fs.writeFileSync(`${L.OUT}/mesures.json`, JSON.stringify(res, null, 1))
