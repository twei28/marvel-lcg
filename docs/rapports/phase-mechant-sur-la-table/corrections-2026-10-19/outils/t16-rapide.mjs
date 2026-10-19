import * as L from './lib.mjs'
// usage: node rapide2.mjs <tag> <carte> <defendre|refuser|sens>
const tag = process.argv[2] || 'avant'
const carte = process.argv[3] || '16117'
const mode = process.argv[4] || 'defendre'
await L.nouvellePartie({ scenario: 'rhino' })
const { browser, ctx } = await L.contexte()
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')"])
await L.sleep(1500)
await L.cmd([`Puzzle.PutIntoPlay('${carte}')`])
const fin = page.getByRole('button', { name: /Fin du tour/ }).first()
const vus = new Set()
let n = 0
const prefere = mode === 'defendre' ? [/^Défendre avec Spider-Man/i] : mode === 'sens' ? [/^Sens d'Araignée/i] : []
for (let k = 0; k < 24; k++) {
  const sg = await L.signature(page)
  const w = await L.monde()
  const c = JSON.stringify([sg.bandeau, sg.demande, sg.lecture])
  if (!vus.has(c) && (sg.bandeau || sg.demande || sg.lecture)) {
    vus.add(c)
    await page.mouse.move(1000, 640)
    await L.sleep(500)
    n++
    await page.screenshot({ path: `${L.OUT}/T16-${tag}-${String(n).padStart(2, '0')}.png` })
    console.log(`${tag}-${n}`, w.phase, '|', sg.bandeau.slice(0, 140), '|', sg.demande.slice(0, 80), '|', sg.lecture)
  }
  let fait = false
  for (const re of prefere) {
    const b = page.getByRole('button', { name: re }).first()
    if (await b.count() && await b.isVisible() && await b.isEnabled()) { await b.click({ timeout: 1500 }).catch(() => {}); fait = true; break }
  }
  if (!fait) {
    const res = page.locator('.tsm-bandeau:not(.est-question)').first()
    if (await res.count()) { await page.mouse.move(1000, 640); await L.sleep(900); await page.screenshot({ path: `${L.OUT}/T16-${tag}-resultat.png` }); await page.keyboard.press('Space'); fait = true; console.log('Espace sur le resultat'); await L.sleep(700); console.log('apres Espace, bandeau:', (await L.signature(page)).bandeau.slice(0, 80)); const w2 = await L.monde(); const dom = await page.evaluate(() => ({ fenetre: document.querySelectorAll('.demande-centrale, .evenement-centrale, .deroule-phase.est-hors-phase').length, apercu: document.querySelectorAll('.carte-apercu, .apercu-carte').length })); const ok = (await fin.isEnabled()) && !(await L.signature(page)).bandeau && w2.phase.startsWith('Player') && dom.fenetre === 0; console.log('ASSERT parcours complet:', ok ? 'OK' : 'ECHEC', JSON.stringify({ phase: w2.phase, dom })); await page.screenshot({ path: `${L.OUT}/T16-${tag}-apres-continuer.png` }); break }
  }
  if (!fait) await L.prepa(page)
  await L.sleep(400)
}
console.log('fin du tour actif:', await fin.isEnabled().catch(() => false))
await page.screenshot({ path: `${L.OUT}/T16-${tag}-fin.png` })
await browser.close()
