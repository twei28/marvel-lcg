import * as L from './lib.mjs'
const tag = process.argv[2] || 'avant'
await L.nouvellePartie({ scenario: 'klaw' })
const { browser, ctx } = await L.contexte()
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01076', under_control=True)"])
await L.cmd(["Puzzle.ChangeForm('01001a')"])
await L.sleep(3000)
const v = (await L.monde()).area_villain[0]
const info = async (nom) => console.log(nom, JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('.evenement-centrale, .toast-effet-carte')].map((e) => { const r = e.getBoundingClientRect(); return { cls: e.className, carte: e.dataset.toastCarte ? (() => { const c = document.querySelector('[data-card-id="' + e.dataset.toastCarte + '"]').getBoundingClientRect(); return [Math.round(c.x), Math.round(c.y), Math.round(c.width), Math.round(c.height)] })() : null, t: e.textContent.trim().replace(/\s+/g, ' '), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) } }))))
const cas = async (nom, cmds) => {
  L.cmd(cmds)
  for (const ms of [250, 500, 900, 1500]) { await L.sleep(ms === 250 ? 250 : ms === 500 ? 250 : ms === 900 ? 350 : 600); await info(nom + '@' + ms); await page.screenshot({ path: `${L.OUT}/T15-${tag}-${nom}-${ms}.png` }) }
  await L.sleep(3000)
}
await cas('klaw-sonne', [`Puzzle.Stun(${v.id})`])
await cas('hulk-sonne-desoriente', ["Puzzle.Stun('01050')", "Puzzle.Confuse('01050')"])
await cas('jeton-rage', ["Puzzle.PlaceCounters('01001a', 'rage', 1)"])
await L.cmd(["Puzzle.Discard('01076')"])
await L.sleep(2500)
await cas('luke-tenace', ["Puzzle.PutIntoPlay('01076', under_control=True)"])
await cas('menace', [`Puzzle.SetThreat(${(await L.monde()).area_schemes_main[0].id}, 3)`])
await browser.close()
