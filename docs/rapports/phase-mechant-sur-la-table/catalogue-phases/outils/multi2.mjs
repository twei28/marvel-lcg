import * as L from './lib.mjs'
import fs from 'fs'
const politique = process.argv[2] ?? 'concerne'
const tag = `multi2-${politique}${process.argv[3] ? '-seed' + process.argv[3] : ''}`
await L.nouvellePartie({ scenario: 'klaw', heros: ['spider_man', 'she_hulk'], seed: Number(process.argv[3] || 4321) })
const { browser, ctx } = await L.contexte()
const pages = [await L.ouvrir(ctx, 0, true), await L.ouvrir(ctx, 1, true)]
await L.attendreTourJoueur(pages, 300)
await L.cmd(["Puzzle.ChangeForm('01001b')"])
await L.sleep(500)
const sigm = async (p) => p.evaluate(() => ({
  bandeau: Array.from(document.querySelectorAll('.tsm-bandeau')).map((e) => e.textContent.trim().replace(/\s+/g, ' ')).join(' | '),
  multi: Array.from(document.querySelectorAll('.tsm-multi')).map((e) => e.textContent.trim().replace(/\s+/g, ' ')).join(' | '),
  demande: Array.from(document.querySelectorAll('.demande-centrale')).map((e) => e.textContent.trim().replace(/\s+/g, ' ')).join(' | '),
  lecture: Array.from(document.querySelectorAll('.rencontre-sur-table')).map((e) => e.getAttribute('data-lecture')).join(','),
  politique: document.querySelectorAll('[data-politique]').length,
}))
const vus = [new Set(), new Set()]; const n = [0, 0]; const journal = []
const bilans = new Set()
// Les deux terminent leur tour joueur.
for (const p of pages) { await p.getByRole('button', { name: /Fin du tour/ }).first().click().catch(() => {}) }
let commencee = false
let derniereCapture = 0; let essais = 0
for (let i = 0; i < 700 && bilans.size < 2; i++) {
  if (n[0] + n[1] > derniereCapture) { derniereCapture = n[0] + n[1]; var dernierI = i }
  if (i - (dernierI ?? 0) > 50 && essais < 6) { essais++; console.log('BLOQUE depuis 50 tours : essai', essais); for (const [s, p] of pages.entries()) { await p.screenshot({ path: `${L.OUT}/${tag}-bloque-s${s}-${essais}.png` }); if (essais === 1) await p.keyboard.press('Space'); if (essais === 2) { const a = p.locator('.tsm-acteur').first(); if (await a.count()) await a.click({ force: true }).catch(() => {}) } if (essais === 3) { const b = p.locator('.tsm-multi [data-pret]').first(); console.log('pret', s, await b.count() ? await b.evaluate((e) => e.outerHTML.slice(0, 300)) : 'aucun') } } dernierI = i }
  const w = await L.monde()
  commencee ||= ['Main Scheme Place Threat', 'Enemy Activation', 'Deal Encounter Cards', 'Reveal Encounter Cards'].includes(w.phase)
  for (const [s, p] of pages.entries()) {
    if (bilans.has(s)) continue
    const sig = await sigm(p)
    const cle = JSON.stringify([w.phase, sig])
    if (!vus[s].has(cle) && (sig.bandeau || sig.demande || sig.multi || sig.lecture)) {
      vus[s].add(cle); await L.sleep(sig.lecture ? 1500 : 400); n[s]++
      const nom = `${tag}-s${s}-${String(n[s]).padStart(2, '0')}`
      await p.screenshot({ path: `${L.OUT}/${nom}.png` })
      journal.push({ nom, phase: w.phase, ...sig }); console.log(nom, w.phase, '|', sig.bandeau.slice(0, 90), '|', sig.multi.slice(0, 80), '|', sig.lecture, sig.politique)
    }
    if (sig.bandeau.includes('Terminer la phase') && await p.locator('.tsm-bandeau.est-bilan').count()) { bilans.add(s); await p.screenshot({ path: `${L.OUT}/${tag}-s${s}-bilan.png` }); console.log('bilan', s); continue }
    const choix = p.locator(`[data-politique="${politique}"]`)
    if (await choix.count()) { await choix.first().click().catch(() => {}); continue }
    const pret = p.locator('.tsm-multi [data-pret]:not([disabled])')
    if (await pret.count()) { await pret.first().click({ timeout: 1500 }).catch(() => {}); continue }
    const lec = p.locator('.rencontre-sur-table[data-lecture="lecture"]')
    if (await lec.count()) { const b = p.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])'); if (await b.count()) { await b.first().click({ timeout: 1500 }).catch(() => {}); continue } }
    if (await p.locator('.rencontre-sur-table:not([data-lecture="termine"])').count()) continue
    if (await p.locator('.tsm-bandeau.est-question').count()) { await L.prepa(p); continue }
    await p.evaluate(() => {
      if (document.querySelector('.tsm-bandeau.est-question, .tsm-bandeau.est-bilan, .rencontre-sur-table:not([data-lecture="termine"])')) return
      document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-question):not(.est-bilan) .tsm-bouton:not([disabled])')?.click()
    })
    if (!commencee || sig.demande) await L.prepa(p, true)
  }
  await L.sleep(100)
}
fs.writeFileSync(`${L.OUT}/${tag}.json`, JSON.stringify(journal, null, 1))
console.log('fini', [...bilans])
await browser.close()
