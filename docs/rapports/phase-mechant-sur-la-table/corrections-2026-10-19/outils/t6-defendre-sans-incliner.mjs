// T6 : defendre SANS s'incliner (Usagi up041, Draw Their Fire 53011, « I Can Do This All Day » 56047, Bodyguard se011) avec le
// heros ET l'allie deja inclines. Usage : OUT=<dossier> node t6-defendre-sans-incliner.mjs <cas> [apres]
// Cas : usagi | falcon | tous-les-jours | temoin-incline
import * as L from '../../catalogue-phases/outils/lib.mjs'
import fs from 'fs'
const cas = process.argv[2] ?? 'usagi'
const etiquette = process.argv[3] ?? 'essai'
const CAS = {
  // heros Spider-Man incline + Usagi (defend sans s'incliner) incline
  usagi: { heros: ['spider_man'], setup: ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('up041', under_control=True)", "Puzzle.Exhaust('01001a')", "Puzzle.Exhaust('up041')"], attendu: /Usagi/ },
  // TEMOIN : un allie incline ordinaire ne peut PAS defendre (Hulk incline) : pas de question
  'temoin-incline': { heros: ['spider_man'], setup: ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.Exhaust('01001a')", "Puzzle.Exhaust('01050')"], attendu: null },
  // Falcon incline avec Draw Their Fire
  falcon: { heros: ['falcon'], setup: ["Puzzle.ChangeForm('53001b')", "Puzzle.PutIntoPlay('53011', under_control=True)"], attendu: /Falcon/ },
  // Bodyguard (Voie Yojimbo) : heros incline
  bodyguard: { heros: ['leonardo'], setup: ["Puzzle.ChangeForm('tl001b')", "Puzzle.PutIntoPlay('se011', under_control=True)", "Puzzle.Exhaust('tl001a')"], attendu: /Bodyguard|Garde du corps/i },
  // 56047 en main, heros incline
  'tous-les-jours': { heros: ['spider_man'], setup: ["Puzzle.ChangeForm('01001b')", "Puzzle.Gain('56047')", "Puzzle.Exhaust('01001a')"], attendu: /All Day|Toute la journée|tout le jour/i },
}
const c = CAS[cas]
await L.nouvellePartie({ scenario: 'klaw', heros: c.heros })
const { browser, ctx } = await L.contexte({ w: 1280, h: 720 })
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
const w0 = await L.monde()
console.log('hero', w0.players[0].area_hero[0].card_id, w0.players[0].area_hero[0].name)
const inclinaisons = c.setup.filter((x) => /Exhaust/.test(x))
try { for (const cmd of c.setup.filter((x) => !/Exhaust/.test(x))) await L.cmd([cmd]) } catch (e) { console.log('setup', String(e).slice(0, 200)) }
let inclinesFait = false
await L.sleep(800)
await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-0-depart.png` })
const w1 = await L.monde()

for (let essai = 0; essai < 30; essai++) {
  if (!/^Player(?: \d+)? Turn$/.test((await L.monde()).phase)) break
  if (essai % 4 === 0) { try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) } }
  else await L.prepa(page, false)
  await L.sleep(700)
}
const vus = new Set(); const journal = []; let n = 0
for (let i = 0; i < 300 && n < (process.env.JOUER || process.env.CLIQUER ? 30 : 14); i++) {
  const w = await L.monde()
  if (!inclinesFait && w.phase === 'Enemy Activation') { inclinesFait = true; for (const cmd of inclinaisons) await L.cmd([cmd]); const w2 = await L.monde(); const walk = (o, p, out) => { if (Array.isArray(o)) o.forEach((v, i) => walk(v, p + '[' + i + ']', out)); else if (o && typeof o === 'object') { if (o.card_id && 'is_ready' in o && /players\[0\]\.(allies|area_hero)/.test(p)) out.push([o.name, o.card_id, o.is_ready]); for (const [k, v] of Object.entries(o)) walk(v, p + '.' + k, out) } }; const out = []; walk(w2, '', out); console.log('prets apres inclinaison :', JSON.stringify(out)) }
  const sig = await L.signature(page)
  const boutons = await page.evaluate(() => [...document.querySelectorAll('.tsm-bandeau .tsm-bouton, .tsm-etiquette')].map((b) => b.textContent.trim().replace(/\s+/g, ' ').slice(0, 70)))
  const cle = JSON.stringify([w.phase, sig.bandeau.slice(0, 80), boutons])
  if (!vus.has(cle) && sig.bandeau) {
    vus.add(cle); n++
    journal.push({ phase: w.phase, bandeau: sig.bandeau.slice(0, 100), boutons })
    await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-${String(n).padStart(2, '0')}.png` })
    console.log(w.phase, '|', sig.bandeau.slice(0, 90), '|', JSON.stringify(boutons))
  }
  if (sig.bilan) break
  if (sig.lecture === 'lecture') await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {})
  else if (sig.question && process.env.CLIQUER && !globalThis.clique && (await page.getByRole('button', { name: new RegExp(process.env.CLIQUER) }).count())) { globalThis.clique = true; await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-avant-clic.png` }); await page.getByRole('button', { name: new RegExp(process.env.CLIQUER) }).first().click(); console.log('>> clic', process.env.CLIQUER); await L.sleep(1500); await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-apres-clic.png` }) }
  else if (sig.question && process.env.JOUER && !globalThis.joue && (await page.getByRole('button', { name: /^Jouer$/ }).count())) { globalThis.joue = true; await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-jouer-avant.png` }); await page.getByRole('button', { name: /^Jouer$/ }).first().click(); console.log('>> clic Jouer'); await L.sleep(1500); await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-jouer-apres.png` })
    // payer : une carte de la main (n'importe quelle ressource), puis « Jouer »
    const main = page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/, pressed: false })
    for (let k = 0; k < (await main.count()); k++) { const b = main.nth(k); if (!/Journée|Toute la/i.test((await b.getAttribute('aria-label')) ?? '')) { await b.click({ timeout: 2000 }).catch(() => {}); break } }
    await L.sleep(600)
    await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-jouer-paye.png` })
    await page.getByRole('button', { name: /^Jouer «/ }).first().click({ timeout: 3000 }).catch((e) => console.log('jouer', String(e).slice(0, 120)))
    await L.sleep(1200) }
  else if (sig.question && cas === 'falcon' && (await page.getByRole('button', { name: /Draw Their Fire|Attirer|Feu/i }).count())) { await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-reponse.png` }); console.log('>> reponse Draw Their Fire proposee'); await page.getByRole('button', { name: /Draw Their Fire|Attirer|Feu/i }).first().click().catch(() => {}); await L.sleep(500); for (const cmd of ["Puzzle.Exhaust('53001a')"]) await L.cmd([cmd]) }
  else if (sig.question) { /* on regarde seulement : ne pas repondre aux questions de defense */ if (!process.env.JOUER && !process.env.CLIQUER && /Qui défend|défendre|Défendre/.test(sig.bandeau) && i > 5) { await page.screenshot({ path: `${L.OUT}/t6-${etiquette}-${cas}-question.png` }); break } await L.prepa(page, false) }
  else if (!sig.demande && !sig.lecture && sig.bandeau) await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click())
  else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
  await L.sleep(300)
}
fs.writeFileSync(`${L.OUT}/t6-${etiquette}-${cas}.json`, JSON.stringify({ cas, journal }, null, 1))
await browser.close()
