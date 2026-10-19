// T2 : le bandeau de question et l'apercu agrandi au survol d'une carte (heros, allie, sbire).
// Usage : OUT=<dossier> node t2-apercu.mjs <avant|apres>
// Pour chaque ecran : monte « Qui defend ? » (heros + 2 allies + un sbire engage), survole chaque carte, mesure le
// recouvrement entre le rectangle du bandeau et celui de l'apercu (.carte-apercu), prend une capture.
import * as L from '../../catalogue-phases/outils/lib.mjs'
import fs from 'fs'
const phase = process.argv[2] ?? 'avant'
const tailles = [['pc', 1280, 720, false], ['tablette', 1180, 820, true], ['paysage', 1050, 480, true], ['mobile-portrait', 390, 844, true]]
const res = []
for (const [nom, w, h, tac] of tailles) {
  await L.nouvellePartie({ scenario: 'rhino' })
  const { browser, ctx } = await L.contexte({ w, h, tactile: tac })
  const page = await L.ouvrir(ctx)
  await L.attendreTourJoueur([page])
  await L.cmd(["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)", "Puzzle.PutIntoPlay('01110')"])
  await L.sleep(600)
  try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) }
  let trouve = false
  for (let i = 0; i < 500 && !trouve; i++) {
    const sig = await L.signature(page)
    if (/Qui défend/.test(sig.bandeau)) trouve = true
    else if (sig.lecture === 'lecture') await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {})
    else if (!sig.question && !sig.demande && !sig.lecture && sig.bandeau) await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click())
    else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
    await L.sleep(250)
  }
  await L.sleep(800)
  const out = { ecran: nom, w, h, trouve, survols: [] }
  const rect = (sel) => page.evaluate((s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) } }, sel)
  out.bandeau = await rect('.tsm-bandeau')
  const cartes = (await page.evaluate(() => [...document.querySelectorAll('.tsm-utilisable')].map((e) => { const r = e.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 } }))).filter((c) => c.x > 230 && c.y > 50 && c.y < h - 10)
  const sbire = await page.evaluate(() => { const e = [...document.querySelectorAll('.plateau-cadre .scan-card.kind-minion')][0]; if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 } })
  const cibles = [...cartes.map((c, i) => ({ nom: 'defenseur-' + i, ...c })), ...(sbire ? [{ nom: 'sbire', ...sbire }] : [])]
  for (const c of cibles) {
    await page.mouse.move(c.x, c.y)
    await L.sleep(500)
    const ap = await rect('.carte-apercu')
    const ba = await rect('.tsm-bandeau')
    // Le bandeau est-il AU-DESSUS de l'apercu (c'est lui qui recouvre) ? On regarde ce qui est au point du recouvrement.
    const m = await page.evaluate(() => {
      const a = document.querySelector('.carte-apercu'), b = document.querySelector('.tsm-bandeau')
      if (!a || !b) return null
      const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect()
      const x0 = Math.max(ra.left, rb.left), x1 = Math.min(ra.right, rb.right), y0 = Math.max(ra.top, rb.top), y1 = Math.min(ra.bottom, rb.bottom)
      if (x1 <= x0 || y1 <= y0) return { recouvrement: 0 }
      const e = document.elementFromPoint((x0 + x1) / 2, (y0 + y1) / 2)
      return { recouvrement: Math.round((x1 - x0) * (y1 - y0)), dessus: e && (a.contains(e) ? 'apercu' : b.contains(e) ? 'bandeau' : e.className?.toString().slice(0, 40)) }
    })
    out.survols.push({ carte: c.nom, apercu: ap, bandeau: ba, ...m })
    await page.screenshot({ path: `${L.OUT}/t2-${phase}-${nom}-${c.nom}.png` })
    console.log(nom, c.nom, JSON.stringify({ ap, ba, m }))
  }
  res.push(out)
  await browser.close()
}
fs.writeFileSync(`${L.OUT}/t2-${phase}.json`, JSON.stringify(res, null, 1))
