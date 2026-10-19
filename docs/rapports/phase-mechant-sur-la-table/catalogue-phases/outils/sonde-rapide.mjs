import * as L from './lib.mjs'
await L.nouvellePartie({ scenario: 'rhino' })
const { browser, ctx } = await L.contexte()
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01172')", "Puzzle.PutIntoPlay('01184')", "Puzzle.PutIntoPlay('01167')"])
for (let i = 0; i < 14; i++) { const s = await L.signature(page); console.log(i, (await L.monde()).phase, s.bandeau.slice(0,100), '|', s.demande.slice(0,80), s.lecture); await page.screenshot({ path: `${L.OUT}/zz-ret-${i}.png` }); await L.prepa(page); await L.sleep(500) }
await browser.close()
