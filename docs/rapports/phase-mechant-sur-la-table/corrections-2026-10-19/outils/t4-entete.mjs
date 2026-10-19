// T4 : « Fin du tour » et l'en-tete sur petit ecran. Usage : OUT=<dossier> node t4-entete.mjs <avant|apres>
// Pour chaque format : partie Klaw avec 3 manigances annexes en jeu, au tour du joueur. Mesure chaque bouton de
// l'en-tete (rectangle, cible tactile, element reellement touche au centre) et signale ce qui recouvre « Fin du tour ».
import * as L from '../../catalogue-phases/outils/lib.mjs'
import fs from 'fs'
const phase = process.argv[2] ?? 'avant'
const tailles = [['pc', 1280, 720, false], ['tablette', 1180, 820, true], ['paysage-1050', 1050, 480, true], ['iphone-paysage-844', 844, 390, true], ['mobile-portrait-390', 390, 844, true]]
const res = []
for (const [nom, w, h, tac] of tailles) {
  await L.nouvellePartie({ scenario: 'klaw' })
  const { browser, ctx } = await L.contexte({ w, h, tactile: tac })
  const page = await L.ouvrir(ctx)
  await L.attendreTourJoueur([page])
  await L.cmd(["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01109')", "Puzzle.PutIntoPlay('01125')", "Puzzle.PutIntoPlay('01151')"])
  await L.sleep(1200)
  const m = await page.evaluate(() => {
    const finTour = [...document.querySelectorAll('button')].filter((x) => /Fin du tour/.test(x.textContent) && x.getBoundingClientRect().width > 0)
    const mesure = (b) => {
      const r = b.getBoundingClientRect()
      const e = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2)
      const ok = e === b || b.contains(e)
      return { texte: b.textContent.trim().slice(0, 24), x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), recu: ok, couvertPar: ok ? null : (e?.closest('[class]')?.className?.toString().slice(0, 60) ?? e?.tagName), desactive: b.disabled }
    }
    const barre = [...document.querySelectorAll('.plateau-barre button')].filter((x) => { const r = x.getBoundingClientRect(); return r.width > 0 && r.y < 60 })
    const uniques = [...new Set([...finTour, ...barre])]
    const boutons = uniques.map(mesure)
    const chev = []
    for (let i = 0; i < boutons.length; i++) for (let j = i + 1; j < boutons.length; j++) { const a = boutons[i], b = boutons[j]; const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x), oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y); if (ox > 1 && oy > 1) chev.push([a.texte, b.texte, ox, oy]) }
    return { viewport: [innerWidth, innerHeight], finTour: finTour.map(mesure), boutons, chevauchements: chev, debordeEcran: boutons.filter((b) => b.x < 0 || b.x + b.w > innerWidth || b.y + b.h > innerHeight).map((b) => b.texte), pointeurTactile: matchMedia('(pointer: coarse)').matches }
  })
  await page.screenshot({ path: `${L.OUT}/t4-${phase}-${nom}.png` })
  console.log(nom, JSON.stringify(m.finTour), 'chevauchements', JSON.stringify(m.chevauchements), 'hors ecran', JSON.stringify(m.debordeEcran), 'tactile', m.pointeurTactile)
  res.push({ ecran: nom, ...m })
  await browser.close()
}
fs.writeFileSync(`${L.OUT}/t4-${phase}.json`, JSON.stringify(res, null, 1))
