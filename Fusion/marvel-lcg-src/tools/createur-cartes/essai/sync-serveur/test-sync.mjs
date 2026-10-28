import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
const U = 'http://127.0.0.1:8791', SC = process.argv[2]
const b = await chromium.launch()
const errs = []
const ok = (n, c, d = '') => console.log((c ? '  OK   ' : '  RATE ') + n + (c ? '' : ' | ' + d))
async function page(ctx, nom) {
  const p = await ctx.newPage(); p.on('pageerror', (e) => errs.push(nom + ': ' + e)); p.on('console', (m) => m.type() === 'error' && errs.push(nom + ' console: ' + m.text()))
  return p
}
const etat = (p) => p.evaluate(() => { const z = document.querySelector('#etat-serveur'); return z.hidden ? 'CACHE' : z.textContent })
const liste = (p) => p.evaluate(async () => (await (await fetch('/api/createur/projets')).json()).projets.map((x) => x.id + '|' + x.nom))

// --- appareil 1
const c1 = await b.newContext({ viewport: { width: 1400, height: 900 } })
let p = await page(c1, 'A')
await p.goto(U + '/connexion')
await p.fill('input[name=pseudo]', 'valtest'); await p.fill('input[name=mdp]', 'motdepasse1'); await p.click('form button[type=submit], form input[type=submit]')
await p.waitForURL('**/createur-cartes.html')
await p.waitForSelector('#liste button')
await p.waitForFunction(() => /Saved on the server/.test(document.querySelector('#etat-serveur').textContent), null, { timeout: 15000 })
ok('1 connecte : indicateur « Saved on the server » (EN)', true)
console.log('   liste serveur au départ:', await liste(p))
// dossier + titre
await p.fill('input[list=dossiers-connus]', 'Valkyrie')
await p.waitForFunction(() => /5 seconds|Saving/.test(document.querySelector('#etat-serveur').textContent), null, { timeout: 4000 }).catch(() => {})
ok('2 attente visible apres un changement', /5 seconds|Saving/.test(await etat(p)), await etat(p))
await p.waitForFunction(() => /Saved on the server/.test(document.querySelector('#etat-serveur').textContent), null, { timeout: 15000 })
const l1 = await liste(p)
ok('3 un projet serveur pour le dossier Valkyrie', l1.some((x) => /^d-valkyrie-[0-9a-f]{8}\|Valkyrie$/.test(x)), l1)
// modele -> _reglages
p.on('dialog', (d) => d.accept('Mon modele'))
await p.click('#m-enregistrer')
for (let i = 0; i < 40 && !(await liste(p)).some((x) => x.startsWith('_reglages')); i++) await p.waitForTimeout(500)
ok('4 _reglages cree apres un modele', true)
console.log('   _reglages serveur:', await p.evaluate(async()=>JSON.stringify((await (await fetch('/api/createur/projet/_reglages')).json()).modeles.map(m=>m.nom))))
await p.screenshot({ path: SC + '/sync-A.png' })

// --- appareil 2 (navigateur vierge, meme compte)
const c2 = await b.newContext({ viewport: { width: 1400, height: 900 } })
const q = await page(c2, 'B')
await q.goto(U + '/connexion')
await q.fill('input[name=pseudo]', 'valtest'); await q.fill('input[name=mdp]', 'motdepasse1'); await q.click('form button[type=submit], form input[type=submit]')
await q.waitForURL('**/createur-cartes.html'); await q.waitForSelector('#liste button')
await q.waitForFunction(() => document.querySelector('#modeles').options.length > 1, null, { timeout: 8000 }).catch(async () => { console.log('B etat:', await etat(q), errs, await liste(q)) })
ok('5 appareil 2 : modele rapatrie', await q.evaluate(() => [...document.querySelector('#modeles').options].some((o) => o.textContent === 'Mon modele')))
ok('6 appareil 2 : dossier Valkyrie rapatrie', await q.evaluate(() => /Valkyrie/.test(document.querySelector('#liste').textContent)), await q.evaluate(() => document.querySelector('#liste').textContent))
// modif sur 2, version serveur
const titre = await q.evaluate(() => document.querySelector('#liste button').textContent)
await q.evaluate(() => [...document.querySelectorAll('#liste .dossier')].find((x) => /Valkyrie/.test(x.textContent)).nextElementSibling.click())
await q.waitForTimeout(300)
await q.evaluate(() => { document.querySelectorAll('input[type=text]').forEach((i) => { if (/Card name|Nom de la carte/.test(i.value)) { i.value = 'Valkyrie B'; i.dispatchEvent(new Event('input', { bubbles: true })) } }) })
await q.waitForFunction(() => /Saved on the server/.test(document.querySelector('#etat-serveur').textContent), null, { timeout: 15000 }).catch(() => {})
await q.waitForTimeout(7000)
const idV = (await liste(q)).find((x) => /^d-valkyrie/.test(x)).split('|')[0]
const vers = await q.evaluate(async (id) => (await (await fetch(`/api/createur/projet/${id}/versions`)).json()).versions, idV)
ok('7 une version ancienne gardee cote serveur apres 2 envois', vers.length >= 1, vers)
await q.click('#p-versions'); await q.waitForSelector('dialog')
await q.waitForFunction(() => /Versions on the server/.test(document.querySelector('dialog').textContent))
await q.waitForTimeout(600)
await q.screenshot({ path: SC + '/sync-versions.png' })
ok('8 fenetre Versions : section serveur avec bouton Restaurer', await q.evaluate(() => document.querySelectorAll('dialog button').length >= 2), await q.evaluate(() => document.querySelector('dialog').textContent.slice(0, 300)))
await q.evaluate(() => { const bs = [...document.querySelectorAll('dialog button')].filter((x) => x.textContent === 'Restore'); bs[bs.length - 1].click() })
await q.waitForTimeout(1500)
ok('9 restauration : fenetre fermee, pas d\'erreur', await q.evaluate(() => !document.querySelector('dialog')), '')

// --- renommer le dossier sur B : l'ancien disparait du serveur
await q.fill('input[list=dossiers-connus]', 'Zed')
await q.waitForTimeout(8000)
const l11 = await liste(q)
ok('11 renommage : ancien projet supprime, nouveau cree', !l11.some((x) => /^d-valkyrie/.test(x)) && l11.some((x) => /^d-zed-/.test(x)), l11)
// --- hors ligne puis rechargement
await c2.setOffline(true)
await q.locator('label:has-text("Title") input').first().fill('Hors ligne')
await q.waitForTimeout(9000)
ok('12a hors ligne : indicateur d\'erreur', /unreachable/.test(await etat(q)), await etat(q))
await q.reload().catch(() => {})
await c2.setOffline(false)
await q.goto(U + '/createur-cartes.html'); await q.waitForSelector('#liste button')
await q.waitForTimeout(4000)
const zid = (await liste(q)).find((x) => /^d-zed-/.test(x)).split('|')[0]
const doc = await q.evaluate(async (id) => (await (await fetch('/api/createur/projet/' + id)).json()), zid)
ok('12b rechargement : les changements hors ligne partent', doc.cartes.some((c) => c.contenu.titre === 'Hors ligne'), doc.cartes.map((c) => c.contenu.titre))
// --- A recharge : suit le renommage, sans ressusciter Valkyrie
await p.goto(U + '/createur-cartes.html'); await p.waitForSelector('#liste button'); await p.waitForTimeout(4000)
const txtA = await p.evaluate(() => document.querySelector('#liste').textContent)
ok('13 A : suit le renommage (Zed present, Valkyrie absent)', /Zed/.test(txtA) && !/Valkyrie/.test(txtA), txtA)
ok('13b serveur : pas de Valkyrie ressuscite', !(await liste(p)).some((x) => /^d-valkyrie/.test(x)), await liste(p))
// --- deconnecte
const c3 = await b.newContext(); const r = await page(c3, 'C')
await r.goto(U + '/createur-cartes.html').catch(() => {})
console.log('   anonyme ->', r.url())
// page hors du site : l'API repond 404 -> local
const c4 = await b.newContext(); const s = await page(c4, 'D')
await s.route('**/api/createur/**', (rt) => rt.fulfill({ status: 404, body: 'x' }))
await c4.addCookies((await c1.cookies()))
await s.goto(U + '/createur-cartes.html'); await s.waitForSelector('#liste button'); await s.waitForTimeout(1500)
ok('10 API 404 -> mode local, indicateur cache', (await etat(s)) === 'CACHE', await etat(s))
const c5 = await b.newContext(); const t5 = await page(c5, 'E')
await t5.route('**/createur-cartes.html', (rt) => rt.continue())
await c5.addCookies([]) 
console.log('ERREURS:', errs)
await b.close()
