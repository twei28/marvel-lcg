// Attaque de Klaw sur Spider-Man (ou autre cas) : compte les clics, journalise jetons / « −X PV » / PV, capture.
// Usage : DIST=<dossier du build> OUT=<captures> TAG=avant|apres CAS=klaw|zero node attaque.mjs
// Le build teste est servi a la place de /app/* du serveur de jeu (route Playwright), le reste va au vrai serveur.
import fs from 'fs'
import path from 'path'
import * as L from '../../catalogue-phases/outils/lib.mjs'
const DIST = process.env.DIST, TAG = process.env.TAG ?? 'apres', CAS = process.env.CAS ?? 'klaw'
const OUT = process.env.OUT
const TYPES = { '.js': 'text/javascript', '.css': 'text/css', '.html': 'text/html', '.png': 'image/png', '.webp': 'image/webp', '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.json': 'application/json', '.svg': 'image/svg+xml' }
const CFG = {
  klaw: { scenario: 'klaw', heros: ['spider_man'], cmds: ["Puzzle.ChangeForm('01001b')"], confus: true },
  zero: { scenario: 'klaw', heros: ['spider_man'], cmds: ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)"], confus: true },
  allie: { scenario: 'klaw', heros: ['spider_man'], cmds: ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)"], confus: true },
}[CAS]
await L.nouvellePartie({ scenario: CFG.scenario, heros: CFG.heros })
const { browser, ctx } = await L.contexte()
if (DIST !== 'serveur') await ctx.route(/127\.0\.0\.1:\d+\/app\//, (route) => {
  const u = new URL(route.request().url())
  const f = path.join(DIST, decodeURIComponent(u.pathname.replace(/^\/app\//, '')))
  if (fs.existsSync(f) && fs.statSync(f).isFile()) return route.fulfill({ body: fs.readFileSync(f), contentType: TYPES[path.extname(f)] ?? 'application/octet-stream', headers: { 'cache-control': 'no-store' } })
  return route.continue()
})
// Clics REELS sur les boutons du bandeau / la carte doree (evenements click recus), pas les tentatives du harnais.
await ctx.addInitScript(() => { window.__clics = []; document.addEventListener('click', (e) => { const b = e.target.closest?.('.tsm-bouton, .tsm-acteur'); if (b) window.__clics.push(Math.round(performance.now()) + ':' + (b.textContent || b.className).trim().slice(0, 30)) }, true) })
const page = await L.ouvrir(ctx)
if (process.env.DEBUG) { page.on('console', (m) => console.log('CONSOLE', m.type(), m.text().slice(0, 200))); page.on('response', (r) => { if (r.status() >= 400) console.log('HTTP', r.status(), r.url().slice(0, 120)) }) }
try { await L.attendreTourJoueur([page]) } catch (e) { await page.screenshot({ path: `${OUT}/../echec-demarrage.png` }); console.log('phase', (await L.monde()).phase); throw e }
await L.cmd(CFG.cmds)
if (CFG.confus) { const v = (await L.monde()).area_villain[0]; await L.cmd([`Puzzle.Confuse(${v.id})`]) }
await L.sleep(600)
for (let essai = 0; essai < 30; essai++) {
  if (!/^Player(?: \d+)? Turn$/.test((await L.monde()).phase)) break
  if (essai % 4 === 0) { try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch {} } else await L.prepa(page, false)
  await L.sleep(700)
}
let avantBilan, clics = 0, vuAttaque = false, capDelta = 0, capJeton = 0
const journal = []
let dernier = ''
const t0 = Date.now()
const relever = () => page.evaluate(() => {
  const jauges = [...document.querySelectorAll('.plateau-cadre .jauge-carte')].map((e) => e.textContent.trim().replace(/\s+/g, ' ')).filter(Boolean)
  return {
    phrase: (document.querySelector('.tsm-phrase')?.textContent ?? '').slice(0, 70),
    jetonsDegats: document.querySelectorAll('.jeton-coup.est-degats').length,
    jetonsTous: [...document.querySelectorAll('.jeton-coup')].map((e) => e.className.replace('jeton-coup ', '')).join(','),
    delta: [...document.querySelectorAll('.delta-sur-table')].map((e) => e.textContent).join(','),
    jauges: jauges.join(' | '),
  }
})
for (let i = 0; i < 900; i++) {
  const sig = await L.signature(page)
  const r = await relever()
  const cle = JSON.stringify([r.phrase, r.jetonsTous, r.delta, r.jauges, sig.lecture, !!sig.bilan])
  if (cle !== dernier) { dernier = cle; journal.push({ t: Date.now() - t0, clics, ...r, lecture: sig.lecture }); if (/attaque/.test(r.phrase)) vuAttaque = true }
  if (vuAttaque && r.delta && !capDelta) { capDelta = 1; for (const ms of [250, 450, 500, 700]) { await L.sleep(ms); await page.screenshot({ path: `${OUT}/${CAS}-${TAG}-delta-${ms}.png` }) } }
  if (r.jetonsDegats && !capJeton) { capJeton = 1; await L.sleep(150); await page.screenshot({ path: `${OUT}/${CAS}-${TAG}-jeton.png` }) }
  if (sig.bilan) { await page.screenshot({ path: `${OUT}/${CAS}-${TAG}-bilan.png` }); clics++; avantBilan = await page.evaluate(() => window.__clics); await page.locator('.tsm-bandeau.est-bilan .tsm-bouton').click().catch(() => {}); break }
  let agi = false
  // Cas allie : a la question « Qui defend », choisir le defenseur demande (CHOIX = regex du bouton).
  if (!agi && sig.question && process.env.CHOIX && !globalThis.choisi) {
    const b = page.getByRole('button', { name: new RegExp(process.env.CHOIX) })
    if (await b.count()) { globalThis.choisi = true; console.log('>> defenseur :', await b.first().textContent()); await b.first().click({ timeout: 1500 }).catch(() => {}); clics++; agi = true }
  }
  if (agi) { /* deja fait */ } else if (sig.lecture === 'lecture') { const b = page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first(); if (await b.count()) { await b.click({ timeout: 1500 }).catch(() => {}); clics++; agi = true } }
  else if (!sig.question && !sig.demande && !sig.lecture && sig.bandeau) {
    agi = await page.evaluate(() => { const b = document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton'); b?.click(); return !!b })
    if (agi) clics++
  } else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
  await L.sleep(agi ? 120 : 100)
}
const reels = avantBilan ?? []
console.log(JSON.stringify({ tag: TAG, cas: CAS, clicsHarnais: clics, clicsReels: reels.length, detail: reels.map((x) => x.split(':')[1]) }))
for (const j of journal.filter((x) => x.phrase || x.delta || x.jetonsTous)) console.log(j.t, 'clics=' + j.clics, '|', j.phrase, '| jetons:', j.jetonsTous, '| delta:', j.delta, '| PV:', j.jauges.slice(0, 90), '|', j.lecture)
await browser.close()
