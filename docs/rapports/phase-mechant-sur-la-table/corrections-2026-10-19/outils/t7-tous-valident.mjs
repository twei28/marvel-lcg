// T7 : blocage « Tout le monde valide » (multi, politique `tous`). Klaw, Spider-Man + She-Hulk, graine 4321.
// Usage : OUT=<dossier> node t7-tous-valident.mjs [politique=tous] [graine=4321]
// Joue la phase comme le spec multi ; quand plus rien ne change pendant 40 tours, vide l'etat des deux sieges
// (bandeau, pied multi, bouton Pret, /get_etapes) et celui du moteur (phase, invite).
import * as L from '../../catalogue-phases/outils/lib.mjs'
import fs from 'fs'
const politique = process.argv[2] ?? 'tous'
const graine = Number(process.argv[3] ?? 4321)
await L.nouvellePartie({ scenario: 'klaw', heros: ['spider_man', 'she_hulk'], seed: graine })
const { browser, ctx } = await L.contexte()
const journalConsole = []
const pages = [await L.ouvrir(ctx, 0, true), await L.ouvrir(ctx, 1, true)]
pages.forEach((p, s) => p.on('console', (m) => { if (/AVANCER/.test(m.text())) journalConsole.push(`s${s} ${m.text()}`) }))
await L.attendreTourJoueur(pages, 300)
await L.cmd(["Puzzle.ChangeForm('01001b')"])
await L.sleep(500)
const etat = (p) => p.evaluate(() => ({
  bandeau: Array.from(document.querySelectorAll('.tsm-bandeau')).map((e) => e.textContent.trim().replace(/\s+/g, ' ')).join(' | '),
  multi: Array.from(document.querySelectorAll('.tsm-multi')).map((e) => e.textContent.trim().replace(/\s+/g, ' ')).join(' | '),
  boutonPret: Array.from(document.querySelectorAll('.tsm-multi [data-pret]')).map((b) => ({ txt: b.textContent.trim(), desactive: b.disabled })),
  lectures: Array.from(document.querySelectorAll('.rencontre-sur-table')).map((e) => e.getAttribute('data-lecture')).join(','),
  acteurs: Array.from(document.querySelectorAll('.tsm-acteur')).map((e) => ({ inactif: e.disabled, label: e.getAttribute('aria-label') })),
  politiques: document.querySelectorAll('[data-politique]').length,
  question: !!document.querySelector('.tsm-bandeau.est-question'),
}))
for (const p of pages) await p.getByRole('button', { name: /Fin du tour/ }).first().click().catch(() => {})
const bilans = new Set(); let sansChangement = 0; let dernier = ''
for (let i = 0; i < 900 && bilans.size < 2; i++) {
  const w = await L.monde()
  const etats = await Promise.all(pages.map(etat))
  const cle = JSON.stringify([w.phase, etats])
  if (cle === dernier) sansChangement++; else { sansChangement = 0; dernier = cle }
  if (sansChangement === 40) {
    console.log('=== BLOQUE', i, 'phase moteur :', w.phase, '| invite :', w.prompt, '| evenement :', w.event_name)
    for (const [s, e] of etats.entries()) console.log('siege', s, JSON.stringify(e).slice(0, 700))
    console.log('/get_etapes', JSON.stringify(await (await fetch(L.BASE + '/get_etapes')).json()).slice(0, 900))
    console.log('console :', journalConsole.filter((x) => /etat/.test(x) && /activation:2/.test(x)).slice(-14).join(' || '))
    console.log('/get_avance_phase', JSON.stringify(await (await fetch(L.BASE + '/get_avance_phase')).json()))
    for (const [s, p] of pages.entries()) await p.screenshot({ path: `${L.OUT}/t7-bloque-s${s}.png` })
    break
  }
  for (const [s, p] of pages.entries()) {
    if (bilans.has(s)) continue
    if (await p.locator('.tsm-bandeau.est-bilan').count()) { bilans.add(s); continue }
    const choix = p.locator(`[data-politique="${politique}"]`)
    if (await choix.count()) { await choix.first().click().catch(() => {}); continue }
    const pret = p.locator('.tsm-multi [data-pret]:not([disabled])')
    if (await pret.count()) { await pret.first().click({ timeout: 1500 }).catch(() => {}); continue }
    const lec = p.locator('.rencontre-sur-table[data-lecture="lecture"]')
    if (await lec.count()) { const b = p.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])'); if (await b.count()) { await b.first().click({ timeout: 1500 }).catch(() => {}); continue } }
    if (await p.locator('.rencontre-sur-table:not([data-lecture="termine"])').count()) continue
    if (await p.locator('.tsm-bandeau.est-question').count()) { await L.prepa(p); continue }
    await p.evaluate(() => {
      if (document.querySelector('.tsm-bandeau.est-question, .tsm-bandeau.est-bilan, .rencontre-sur-table:not([data-lecture="termine"])')) return
      document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-question):not(.est-bilan) .tsm-bouton:not([disabled])')?.click()
    })
    if (i < 60) await L.prepa(p, true)
  }
  await L.sleep(100)
}
console.log('fini', [...bilans])
await browser.close()
