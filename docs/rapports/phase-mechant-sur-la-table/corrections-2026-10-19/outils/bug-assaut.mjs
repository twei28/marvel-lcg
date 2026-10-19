// BUG PRIORITAIRE : l'attaque declenchee par une carte REVELEE (Assaut 01187, Se Liguer 01189) se deroule-t-elle avec ses boosts ?
// Usage : OUT=<dossier> node bug-assaut.mjs <etiquette> [scenario=klaw] [carte=01187] [nbSbires=0] [mode=sur-table|detaille|instantane]
// Journalise : les facts (genre/etat/boosts) du monde, les bandeaux, les lectures, les PV du heros avant/apres, et les captures.
import * as L from '../../catalogue-phases/outils/lib.mjs'
import fs from 'fs'
const [etiquette = 'essai', scenario = 'klaw', carte = '01187', nbSbires = '0', mode = 'sur-table'] = process.argv.slice(2)
const sbires = ["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01110')"].slice(0, Number(nbSbires))
// L'ordre de sortie : boosts de l'activation (2 pour Klaw, 1 pour Rhino), puis la carte revelee, puis les boosts de son attaque, puis du remplissage.
const boostsActivation = scenario === 'klaw' ? 2 : 1
const deck = [...Array(boostsActivation).fill('01112'), carte, ...Array(4).fill('01112'), '01110', '01110', '01110']
await L.nouvellePartie({ scenario })
const { browser, ctx } = await L.contexte({ w: 1280, h: 720 })
if (mode !== 'sur-table') await ctx.addInitScript((m) => { localStorage.setItem('marvel-board-mode-phase-mechant', m); localStorage.removeItem('mc_phase_presentation') }, mode === 'detaille' ? 'detaille' : 'instantane')
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')", ...sbires])
await L.cmd(['Puzzle.EmptyEncounterDeck()', `Puzzle.CreateEncounterDeck(${[...deck].reverse().map((c) => `'${c}'`).join(',')})`])
const pv = async () => { const w = await L.monde(); const h = w.players[0].area_hero[0]; return { phase: w.phase, hp: h.info?.health, degats: h.damage ?? h.counters?.damage } }
const avant = await pv()
console.log('avant', JSON.stringify(avant), 'deck', deck.join(','))
await L.sleep(800)
for (let essai = 0; essai < 30; essai++) {
  const w0 = await L.monde()
  if (!/^Player(?: \d+)? Turn$/.test(w0.phase)) break
  if (essai % 4 === 0) { try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) } }
  else await L.prepa(page, false)
  await L.sleep(700)
}
const vus = new Set(); let n = 0; const lectures = []; const bandeaux = []
for (let i = 0; i < 800; i++) {
  const w = await L.monde()
  const sig = await L.signature(page); if (i % 40 === 0) console.log(i, w.phase, JSON.stringify(sig.bandeau.slice(0, 60)), sig.demande.slice(0, 80))
  if (sig.lecture) lectures.push(sig.lecture)
  const cle = JSON.stringify([w.phase, sig.bandeau.slice(0, 100), sig.lecture])
  if (!vus.has(cle) && (sig.bandeau || sig.lecture)) { vus.add(cle); n++; bandeaux.push(`${w.phase} | ${sig.bandeau.slice(0, 110)} | ${sig.lecture}`); await page.screenshot({ path: `${L.OUT}/bug-assaut-${etiquette}-${String(n).padStart(2, '0')}.png`, type: 'png' }) }
  if (sig.bilan) { await page.screenshot({ path: `${L.OUT}/bug-assaut-${etiquette}-bilan.png` }); break }
  if (sig.lecture === 'lecture') await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {})
  else if (!sig.question && !sig.demande && !sig.lecture && sig.bandeau) await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click())
  else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
  await L.sleep(150)
  if (mode === 'instantane' && /Player/.test(w.phase) && i > 30) break
}
const finW = await L.monde()
const h = finW.players[0].area_hero[0]
console.log('apres', JSON.stringify({ phase: finW.phase, degatsHeros: JSON.stringify(h.counters ?? h.info ?? {}).slice(0, 200) }))
console.log('faits :', (finW.faits_mechant ?? []).map((x) => `${x.genre}/${x.etat ?? ''}/${x.auteur ?? x.carte ?? ''}/boosts=${(x.boosts ?? []).length}/subi=${x.subi ?? ''}/base=${x.base ?? ''}`).join('\n  '))
console.log('bandeaux :\n ' + bandeaux.join('\n '))
console.log('lectures vues :', [...new Set(lectures)].join(','))
fs.writeFileSync(`${L.OUT}/bug-assaut-${etiquette}.json`, JSON.stringify({ avant, bandeaux, lectures: [...new Set(lectures)], faits: finW.faits_mechant }, null, 1))
await browser.close()
