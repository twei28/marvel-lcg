// T3 : l'ordre d'activation de 6 sbires. Usage : OUT=<dossier> node t3-ordre.mjs <avant|apres>
// avant : on clique chaque sbire (6 clics) puis Valider ; apres : un seul clic sur « Garder l'ordre de la table ».
// Mesure : nombre de clics, ordre de la table (gauche -> droite) et ordre reel d'activation des sbires (phrases du bandeau).
import * as L from '../../catalogue-phases/outils/lib.mjs'
import fs from 'fs'
const phase = process.argv[2] ?? 'avant'
await L.nouvellePartie({ scenario: 'rhino' })
const { browser, ctx } = await L.contexte({ w: 1280, h: 720 })
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')", "Puzzle.PutIntoPlay('01103')", "Puzzle.PutIntoPlay('01182')", "Puzzle.PutIntoPlay('01121')", "Puzzle.PutIntoPlay('01102')"])
await L.sleep(800)
try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) }
const res = { phase, clics: 0, ordreTable: [], ordreActivation: [] }
let ordreFait = false
const vus = new Set()
for (let i = 0; i < 900; i++) {
  const sig = await L.signature(page); if (i === 10) await page.screenshot({ path: '/tmp/t3dbg.png' }); if (i % 15 === 0) console.log(i, (await L.monde()).phase, JSON.stringify(sig.bandeau.slice(0, 90)), sig.demande.slice(0,60))
  if (!ordreFait && /ordre/i.test(sig.bandeau) && sig.question) {
    await L.sleep(800)
    await page.screenshot({ path: `${L.OUT}/t3-${phase}-1-question.png` })
    // l'ordre de la table : positions x/y des cartes ciblables, par noms
    res.ordreTable = await page.evaluate(() => [...document.querySelectorAll('.tsm-utilisable')].map((e) => { const r = e.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), nom: e.getAttribute('aria-label') } }))
    res.sbiresGaucheDroite = await page.evaluate(() => [...document.querySelectorAll('.plateau-cadre .scan-card.kind-minion')].filter((e) => !e.closest('.rencontre-sur-table, .carte-apercu')).map((e) => ({ x: e.getBoundingClientRect().x, nom: e.getAttribute('aria-label') || e.dataset.cardId })).sort((a, b) => a.x - b.x).map((o) => o.nom))
    if (phase === 'avant') {
      const cartes = page.locator('.tsm-utilisable')
      const n = await cartes.count()
      for (let k = 0; k < n; k++) { await cartes.nth(k).click(); res.clics++ }
      await L.sleep(500)
      await page.screenshot({ path: `${L.OUT}/t3-${phase}-2-numerotes.png` })
      await page.getByRole('button', { name: /^Valider/ }).click(); res.clics++
    } else {
      const b = page.locator('[data-ordre-table]')
      res.boutonPresent = await b.count()
      res.libelle = res.boutonPresent ? (await b.textContent()) : null
      await page.screenshot({ path: `${L.OUT}/t3-${phase}-1b-bouton.png` })
      await b.click(); res.clics++
      await L.sleep(800)
    }
    ordreFait = true
    continue
  }
  const m = sig.bandeau.match(/^‹?\s*(.+?) va attaquer/)
  if (m && !vus.has(sig.bandeau)) { vus.add(sig.bandeau); res.ordreActivation.push(m[1]) }
  if (sig.bilan) break
  if (sig.lecture === 'lecture') await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {})
  else if (!sig.question && !sig.demande && !sig.lecture && sig.bandeau) await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click())
  else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
  await L.sleep(200)
}
console.log(JSON.stringify(res, null, 1))
fs.writeFileSync(`${L.OUT}/t3-${phase}.json`, JSON.stringify(res, null, 1))
await browser.close()
