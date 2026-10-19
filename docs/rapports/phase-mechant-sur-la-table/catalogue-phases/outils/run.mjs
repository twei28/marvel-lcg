import * as L from './lib.mjs'
import fs from 'fs'
import { P } from './parcours.mjs'
const noms = process.argv.slice(2)
for (const nom of noms) {
  const p = P[nom]
  if (!p) { console.log('inconnu', nom); continue }
  console.log('=== ', nom)
  const tag = p.tag ?? nom
  try {
    await L.nouvellePartie({ scenario: p.scenario ?? 'klaw', heros: p.heros ?? ['spider_man'], seed: p.seed ?? 4321, extraSets: p.extraSets ?? [] })
    const { browser, ctx } = await L.contexte({ w: p.w ?? 1280, h: p.h ?? 720, reduit: p.reduit, tactile: p.tactile })
    const page = await L.ouvrir(ctx)
    await L.attendreTourJoueur([page])
    if (p.form !== 'alter') await L.cmd(["Puzzle.ChangeForm('01001b')"])
    if (p.setup) await p.setup({ ...L, page })
    if (p.deck) await L.cmd(["Puzzle.EmptyEncounterDeck()", `Puzzle.CreateEncounterDeck(${[...p.deck].reverse().map((c) => `'${c}'`).join(',')})`])
    await L.sleep(800)
    await page.screenshot({ path: `${L.OUT}/${tag}-00-depart.png` })
    if (p.sansPhase) { await browser.close(); continue }
    const j = await L.phaseMechant(page, { tag, prefere: p.prefere ?? [], prefereSel: p.prefereSel ?? [], choisir: p.choisir && ((pg, sig, w) => p.choisir({ ...L, page: pg }, sig, w)), onState: p.onState, max: p.max ?? 400, rafale: p.rafale })
    fs.writeFileSync(`${L.OUT}/${tag}.json`, JSON.stringify(j, null, 1))
    if (p.apres) await p.apres({ ...L, page })
    await browser.close()
  } catch (e) { console.log('ERREUR', nom, String(e).slice(0, 400)) }
}
