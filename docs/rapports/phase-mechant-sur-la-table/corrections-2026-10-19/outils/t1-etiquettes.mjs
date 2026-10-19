// T1 : mesure des etiquettes « Defendre avec … » (largeur vs carte, chevauchements) pour 1, 2, 3 allies
// et 4 formats d'ecran. Usage : OUT=<dossier> node t1-etiquettes.mjs <avant|apres>
import * as L from '../../catalogue-phases/outils/lib.mjs'
import fs from 'fs'
const phase = process.argv[2] ?? 'avant'
const tailles = [['pc', 1280, 720, false], ['tablette', 1180, 820, true], ['paysage', 1050, 480, true], ['iphone-paysage', 844, 390, true]]
const allies = ["Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)", "Puzzle.PutIntoPlay('01075', under_control=True)"]
const res = []
for (const [nom, w, h, tac] of tailles) for (const n of [1, 2, 3]) {
  await L.nouvellePartie({ scenario: 'klaw' })
  const { browser, ctx } = await L.contexte({ w, h, tactile: tac })
  const page = await L.ouvrir(ctx)
  await L.attendreTourJoueur([page])
  await L.cmd(["Puzzle.ChangeForm('01001b')", ...allies.slice(0, n)])
  await L.sleep(600)
  try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) }
  let mes = null
  for (let i = 0; i < 400 && !mes; i++) {
    const sig = await L.signature(page)
    if (/Qui défend/.test(sig.bandeau)) {
      await L.sleep(700)
      mes = await page.evaluate(() => {
        const R = (e) => { const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height } }
        const et = [...document.querySelectorAll('.tsm-etiquette')].map((e) => ({ ...R(e), txt: e.textContent, trop: e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1 }))
        const ca = [...document.querySelectorAll('.tsm-utilisable')].map(R)
        const chev = []
        for (let i = 0; i < et.length; i++) for (let j = i + 1; j < et.length; j++) { const a = et[i], b = et[j]; const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x); const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y); if (ox > 0.5 && oy > 0.5) chev.push([i, j, Math.round(ox)]) }
        const pires = et.map((e, i) => ({ nom: e.txt, wEtiquette: Math.round(e.w * 10) / 10, wCarte: ca[i] ? Math.round(ca[i].w * 10) / 10 : null, hEtiquette: Math.round(e.h), debordeTexte: e.trop }))
        return { n: et.length, chev, pires, ok: chev.length === 0 && pires.every((p) => p.wCarte !== null && p.wEtiquette <= p.wCarte + 0.6) }
      })
      await page.screenshot({ path: `${L.OUT}/t1-${phase}-${nom}-${n}allies.png` })
      break
    }
    if (sig.lecture === 'lecture') { await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {}) }
    else if (!sig.question && !sig.demande && !sig.lecture && sig.bandeau) await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click())
    else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
    await L.sleep(250)
  }
  console.log(nom, n, JSON.stringify(mes))
  res.push({ ecran: nom, w, h, allies: n, mesure: mes })
  await browser.close()
}
fs.writeFileSync(`${L.OUT}/t1-${phase}.json`, JSON.stringify(res, null, 1))
