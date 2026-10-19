// usage: node t14.mjs <n> <heros|allie> <w> <h> <tactile 0/1> <tag>
process.env.BASE ||= 'http://127.0.0.1:2496'; process.env.OUT ||= '/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/2ed3e66d-9fcf-45e1-aa7f-2debf9a42af0/scratchpad/t1314/out'
const L = await import('/home/oem/Desktop/Marvel LCG/.claude/worktrees/agent-accc7427d30e0af3e/docs/rapports/phase-mechant-sur-la-table/catalogue-phases/outils/lib.mjs')
const [n, cible, w, h, tac, tag] = process.argv.slice(2)
const CODES = n.split(',')
await L.nouvellePartie({ scenario: 'klaw', heros: ['spider_man'] })
const { browser, ctx } = await L.contexte({ w: +w, h: +h, tactile: tac === '1' })
const page = await L.ouvrir(ctx)
await L.attendreTourJoueur([page])
await L.cmd(["Puzzle.ChangeForm('01001b')"])
const cmds = []
if (cible === 'allie') cmds.push("Puzzle.PutIntoPlay('01050', under_control=True)")
for (const c of CODES) cmds.push("Puzzle.PutIntoPlay('" + c + "', under_control=True)")
for (const c of cmds) { try { await L.cmd([c]) } catch (e) { console.log('setup', c, String(e).slice(0, 150)) } }
if (cible === 'allie') { const wd = await L.monde(); const ups = CODES.flatMap((c) => L.trouve(wd, c)); console.log('ups', JSON.stringify(ups)); for (const u of ups) { try { await L.cmd([`Puzzle.Attach(${u[1]}, '01050')`]) } catch (e) { console.log('attach', String(e).slice(0, 150)) } } }
await L.sleep(600)
{ const wd = await L.monde(); console.log('en jeu', JSON.stringify(CODES.flatMap((c) => L.trouve(wd, c)))) }
await page.screenshot({ path: `${L.OUT}/${tag}-0-depart.png` })
for (let i = 0; i < 40; i++) { if (!/^Player(?: \d+)? Turn$/.test((await L.monde()).phase)) break; if (i % 4 === 0) { try { await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 3000 }) } catch { await page.evaluate(() => [...document.querySelectorAll('button')].find((x) => /Fin du tour/.test(x.textContent))?.click()) } } else await L.prepa(page, false); await L.sleep(500) }
let trouve = false
for (let i = 0; i < 300; i++) {
  const sig = await L.signature(page)
  const b = page.getByRole('button', { name: /— (Interruption|Réponse)/i })
  if (sig.question && (await b.count())) { trouve = true; break }
  if (sig.bilan) break
  if (sig.lecture === 'lecture') await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => {})
  else if (sig.question) await L.prepa(page, false)
  else if (!sig.demande && !sig.lecture && sig.bandeau) await page.evaluate(() => document.querySelector('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click())
  else if (!/entree|depart/.test(sig.lecture)) await L.prepa(page, false)
  await L.sleep(250)
}
console.log('question trouvee', trouve)
await L.sleep(2200)
await page.screenshot({ path: `${L.OUT}/${tag}-1-question.png` })
const SEL = tac === '1' ? '.tsm-utilisable' : '.tsm-eventail-carte'
const mesure = () => page.evaluate((SEL) => {
  const R = (e) => { const r = e.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), r: Math.round(r.right), b: Math.round(r.bottom) } }
  const cartes = [...document.querySelectorAll(SEL)].map((b) => {
    const img = b.querySelector('.tsm-eventail-image') || b; const nom = b.querySelector('.tsm-eventail-nom') || b
    const rb = b.getBoundingClientRect(); const cx = rb.left + rb.width / 2, cy = rb.top + rb.height / 2
    const el = document.elementFromPoint(cx, cy)
    return { nom: b.getAttribute('aria-label'), bouton: R(b), image: R(img), libelle: R(nom), dansEcran: rb.left >= 0 && rb.top >= 0 && rb.right <= innerWidth && rb.bottom <= innerHeight, centre: el === b || b.contains(el) ? 'OK' : (el?.className || el?.tagName).toString().slice(0, 40), nomTronque: nom.querySelector('b') ? nom.querySelector('b').scrollHeight > nom.querySelector('b').clientHeight + 1 : null }
  })
  const bd = document.querySelector('.tsm-bandeau.est-question'); const ap = document.querySelector('.carte-apercu')
  const heros = [...document.querySelectorAll('.plateau-cadre .scan-card[data-card-id="1"] .scan-frame')].map(R)[0]
  return { cartes, bandeau: bd && R(bd), apercu: ap && R(ap), heros, boutons: [...document.querySelectorAll('.tsm-bandeau .tsm-bouton')].map((b) => b.textContent.trim().slice(0, 50)) }
}, SEL)
const m = await mesure()
const inter = (a, b) => a && b && a.x < b.r && a.r > b.x && a.y < b.b && a.b > b.y
console.log('MESURE', JSON.stringify(m))
console.log('recouvre bandeau:', m.cartes.map((c) => inter(c.bouton, m.bandeau)), 'recouvre heros:', m.cartes.map((c) => inter(c.bouton, m.heros)))
if (tac !== '1') {
  await page.locator(SEL).first().hover(); await L.sleep(700)
  await page.screenshot({ path: `${L.OUT}/${tag}-2-survol.png` })
  const m2 = await mesure(); console.log('SURVOL apercu', JSON.stringify(m2.apercu), 'recouvre apercu:', m2.cartes.map((c) => inter(c.bouton, m2.apercu)))
}
const nb0 = await page.locator(SEL).count()
const cibleClic = page.locator(SEL).nth(Math.min(1, nb0 - 1))
if (tac === '1') await cibleClic.tap(); else await cibleClic.click()
await L.sleep(900)
await page.screenshot({ path: `${L.OUT}/${tag}-3-apres-choix.png` })
console.log('APRES CHOIX eventail restant:', await page.locator(SEL).count(), 'avant:', nb0)
await browser.close()
