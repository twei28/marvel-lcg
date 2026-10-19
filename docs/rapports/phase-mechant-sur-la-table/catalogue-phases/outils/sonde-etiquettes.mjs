import * as L from './lib.mjs'
await L.nouvellePartie({ scenario: 'klaw' })
const { browser, ctx } = await L.contexte()
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)", "Puzzle.PutIntoPlay('01075', under_control=True)"])
let done=false
await L.phaseMechant(page, { tag: 't7', log:false, prefere:[/^Sens d'Araignée$/], choisir: async (pg, sig) => {
  if (!done && sig.question && /Qui défend/.test(sig.bandeau)) { done=true
    for (const n of ['Hulk','Vision','Black Widow','Spider-Man']) {
      const b = pg.getByRole('button', { name: new RegExp('^Défendre avec '+n) }).first()
      const r = await b.boundingBox()
      try { await b.click({ timeout: 2500, trial: true }); console.log(n, 'clic possible', JSON.stringify(r)) } catch (e) { console.log(n, 'BLOQUE', JSON.stringify(r), (String(e).match(/<[^>]+>[^<]*<\/[a-z]+> intercepts|<[^>]*> intercepts/)||[''])[0].slice(0,200)) }
    }
    await pg.screenshot({ path: L.OUT + '/zz-etiquettes-3allies.png' })
    await pg.getByRole('button', { name: /^Ne pas défendre/ }).click()
  } return false }, max: 60 })
await browser.close()
