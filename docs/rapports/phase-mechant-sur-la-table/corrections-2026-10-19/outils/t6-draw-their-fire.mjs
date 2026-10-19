// Q4 / T6 : Draw Their Fire (53011) est-elle PROPOSEE au debut de la phase du mechant ?
// Sonde SANS `prepa` (qui clique « Ne pas utiliser » toute seule) : on clique « Fin du tour » une fois, puis on LIT
// l'ecran image par image sans rien toucher, et on imprime ce que le plateau affiche et ce que le moteur attend.
// Usage : BASE=http://127.0.0.1:<port> OUT=<dossier> node t6-draw-their-fire.mjs [accepter|refuser]
import * as L from '../../catalogue-phases/outils/lib.mjs'
const decision = process.argv[2] ?? 'accepter'
await L.nouvellePartie({ scenario: 'klaw', heros: ['falcon'] })
const { browser, ctx } = await L.contexte({ w: 1280, h: 720 })
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
for (const cmd of ["Puzzle.ChangeForm('53001b')", "Puzzle.PutIntoPlay('53011', under_control=True)"]) await L.cmd([cmd])
await L.sleep(800)
await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 5000 })
const vus = new Set()
let clique = false
for (let i = 0; i < 120; i++) {
  const w = await L.monde()
  const sig = await L.signature(page)
  const boutons = await page.evaluate(() => [...document.querySelectorAll('button')].filter((b) => b.offsetParent).map((b) => (b.getAttribute('aria-label') || b.textContent).trim().replace(/\s+/g, ' ').slice(0, 60)).filter(Boolean))
  const cle = JSON.stringify([w.phase, sig.bandeau.slice(0, 100), sig.demande.slice(0, 100)])
  if (!vus.has(cle)) {
    vus.add(cle)
    console.log(w.phase, '| bandeau:', sig.bandeau.slice(0, 110), '| demande:', sig.demande.slice(0, 110))
    console.log('   boutons:', JSON.stringify(boutons.filter((b) => /Draw|Falcon|Faucon|Réponse|utiliser|Défendre|défend|Continuer/i.test(b))))
    await page.screenshot({ path: `${L.OUT}/dtf-${String(vus.size).padStart(2, '0')}.png` })
  }
  if (w.phase === 'Enemy Activation' && sig.question) {
    // Qui defend ? : le Faucon doit etre propose ; on le choisit et on regarde s'il s'incline.
    const etiquettes = await page.evaluate(() => [...document.querySelectorAll('.tsm-etiquette, .tsm-bandeau .tsm-bouton')].map((b) => b.textContent.trim().replace(/\s+/g, ' ').slice(0, 80)))
    console.log('QUI DEFEND :', JSON.stringify(etiquettes))
    const f = page.locator('.tsm-etiquette').filter({ hasText: /Faucon|Falcon/ }).first()
    if (await f.count()) { await f.click({ timeout: 2000 }).catch(() => {}); await L.sleep(1500) }
    break
  }
  if (!clique && sig.demande && /Réponse de héros/i.test(boutons.join("|"))) {
    const re = decision === 'accepter' ? /^Réponse de héros/i : /^Ne pas/i
    const b = page.getByRole('button', { name: re }).first()
    if (await b.count()) { clique = true; console.log('>> clic', decision); await b.click({ timeout: 2000 }).catch(() => {}) }
  }
  else if (sig.demande && /Fin de phase/.test(sig.demande)) await page.locator('.demande-centrale .af-action:visible').first().click({ timeout: 1500 }).catch(() => {})
  else if (boutons.some((b) => /^Défausser \d/.test(b))) await L.prepa(page, false)
  if (sig.bandeau && !sig.question && !sig.bilan && sig.lecture !== 'lecture') await page.keyboard.press('Space')
  if (sig.lecture === 'lecture') await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {})
  await L.sleep(250)
}
const w2 = await L.monde()
const walk = (o, p, out) => { if (Array.isArray(o)) o.forEach((v, i) => walk(v, p + '[' + i + ']', out)); else if (o && typeof o === 'object') { if (o.card_id && 'is_ready' in o && /players\[0\]\.(allies|area_hero)/.test(p)) out.push([o.name, o.card_id, o.is_ready]); for (const [k, v] of Object.entries(o)) walk(v, p + '.' + k, out) } }
const out = []; walk(w2, '', out)
console.log('etat final :', w2.phase, JSON.stringify(out))
await browser.close()
