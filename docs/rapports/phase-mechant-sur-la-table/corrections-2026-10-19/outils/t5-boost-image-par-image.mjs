// T5 : l'ordre reel « boost montre -> effet annonce -> carte sur la table » pour un boost de sbire (Weapons Runner 01121).
// Usage : OUT=<dossier> node t5-boost-image-par-image.mjs <avant|apres> [code=01121]
// Echantillonne l'etat toutes les ~100 ms (JPEG basse qualite pour tenir le rythme) ; le journal ne garde que les CHANGEMENTS.
import * as L from '../../catalogue-phases/outils/lib.mjs'
import fs from 'fs'
const phase = process.argv[2] ?? 'avant'
const code = process.argv[3] ?? '01121'
const deck = [code, '01110', '01110', '01122']
await L.nouvellePartie({ scenario: 'klaw' })
const { browser, ctx } = await L.contexte({ w: 1280, h: 720 })
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')"])
await L.cmd(['Puzzle.EmptyEncounterDeck()', `Puzzle.CreateEncounterDeck(${[...deck].reverse().map((c) => `'${c}'`).join(',')})`])
const idCarte = Math.max(...(await L.zone(code)).map((z) => z[1]))
console.log('carte', code, 'id moteur', idCarte)
const zoneDe = (w) => { let z; const walk = (o) => { if (Array.isArray(o)) o.forEach(walk); else if (o && typeof o === 'object') { if (o.id === idCarte && 'game_area' in o) z = o.game_area; for (const v of Object.values(o)) walk(v) } }; walk(w); return z }
await L.sleep(500)
const t0 = Date.now()
const journal = []
let dernier = ''
let n = 0
let attente = 0
let dernierClic = 0
const lire = () => page.evaluate((id) => {
  const el = (sel) => [...document.querySelectorAll(sel)]
  const vis = (e) => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 4 && r.height > 4 && cs.visibility !== 'hidden' && Number(cs.opacity) > 0.05 }
  const surTable = el(`.plateau-cadre .scan-card[data-card-id="${id}"]`).filter((e) => !e.closest('.rencontre-sur-table, .carte-apercu') && !e.classList.contains('is-facedown') && vis(e))
  const lue = el(`.rencontre-sur-table .scan-card[data-card-id="${id}"]`).filter(vis)
  const lectures = el('.rencontre-sur-table').map((e) => e.getAttribute('data-lecture')).join(',')
  const bandeau = (document.querySelector('.tsm-bandeau')?.textContent ?? '').replace(/\s+/g, ' ').trim().slice(0, 100)
  const r = surTable[0]?.getBoundingClientRect()
  return { surTable: surTable.length, x: r ? Math.round(r.x) : null, lue: lue.length, lectures, bandeau, question: !!document.querySelector('.tsm-bandeau.est-question'), bilan: !!document.querySelector('.tsm-bandeau.est-bilan'), bouton: !!document.querySelector('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])') }
}, idCarte)
try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) }
let arret = 0
for (let i = 0; i < 1500; i++) {
  const [s, w] = await Promise.all([lire(), L.monde()])
  const ligne = { t: Date.now() - t0, ...s, zoneMoteur: zoneDe(w), phaseMoteur: w.phase }
  const cle = JSON.stringify({ ...ligne, t: 0 })
  if (cle !== dernier) {
    dernier = cle
    journal.push(ligne)
    n++
    if (n <= 200) page.screenshot({ path: `${L.OUT}/t5-${phase}-${String(n).padStart(3, '0')}.jpg`, type: 'jpeg', quality: 55 }).catch(() => {})
  }
  if (s.bilan) break
  // Une fois le sbire en jeu sur la table et la lecture finie, on s'arrete apres un temps.
  if (ligne.t > 45000) break
  const now = Date.now()
  if (now - dernierClic > 1400) {
    if (s.lectures.includes('lecture') && s.bouton) { dernierClic = now; page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 800 }).catch(() => {}) }
    else if (s.question && !s.lectures) { dernierClic = now; L.prepa(page, false).catch(() => {}) }
    else if (!s.question && !s.lectures && s.bandeau) { dernierClic = now - 700; page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click()).catch(() => {}) }
    else if (!s.bandeau && !s.lectures) { dernierClic = now - 700; L.prepa(page, false).catch(() => {}) }
  }
  await L.sleep(30)
}
fs.writeFileSync(`${L.OUT}/t5-${phase}.json`, JSON.stringify(journal, null, 1))
for (const j of journal) console.log(String(j.t).padStart(6), 'surTable', j.surTable, 'x', j.x, 'lueGrand', j.lue, 'lectures', j.lectures || '-', 'zone', j.zoneMoteur, '|', j.bandeau)
await browser.close()
