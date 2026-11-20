// Aller-retour complet : « Tout enregistrer (.zip) » sur un ordinateur, « Importer » sur un autre (navigateur vierge) -> la page
// doit etre identique (dossiers, genre, couleurs, nombre de cartes, template, lien recto-verso) ; puis les modes « Remplacer » et « Ajouter ».
//   node tools/createur-cartes/essai/aller-retour-complet.mjs [http://127.0.0.1:8792]   (serveur statique de public/)
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import { dossierVide, carteVide, attendreAccueil, ouvrirSections, versAccueil } from './aide-ui.mjs'
import path from 'node:path'; import fs from 'node:fs'; import os from 'node:os'
import { fileURLToPath } from 'node:url'
const U = (process.argv[2] ?? 'http://127.0.0.1:8792') + '/createur-cartes.html'
const PHOTO = path.join(path.dirname(fileURLToPath(import.meta.url)), '../../../public/createur-cartes/_essai/valkyrie-photo.png')
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'rt-'))
const b = await chromium.launch()
let rates = 0
const ok = (n, c, d = '') => { if (!c) rates++; console.log((c ? '  OK   ' : '  RATE ') + n + (c ? '' : ' | ' + d)) }
const errs = []
const nouvelle = async () => { const c = await b.newContext({ viewport: { width: 1500, height: 900 }, acceptDownloads: true }); const p = await c.newPage(); p.on('pageerror', (e) => errs.push(String(e))); p.on('dialog', (d) => d.accept()); return p }
const att = (p, ms = 600) => p.waitForTimeout(ms)
const suivant = async (p) => { await p.click('dialog[open] button:has-text("Next ▶")'); await att(p, 400) }
const resume = (p) => p.evaluate(() => ({
  tuiles: [...document.querySelectorAll('.rangee-dossiers:not(.rangee-pochettes) .tuile')].map((t) => t.querySelector('.nom').textContent.trim() + '|' + t.querySelector('.compte').textContent.trim() + '|' + (t.style.getPropertyValue('--teinte') || '')).sort(),
  total: Number(document.querySelector('#liste')?.dataset.total ?? -1),
  pochettes: [...document.querySelectorAll('.rangee-pochettes .tuile')].map((t) => t.querySelector('.nom').textContent.trim()),
}))
// ---- ordinateur A : un heros (wizard, Justice) + un scenario vide + une image sur une carte
const A = await nouvelle()
await A.goto(U); await attendreAccueil(A)
await A.click('.tuile-creer.cartes[data-creer="heros"]'); await att(A, 300)
await A.fill('dialog[open] input', 'Thor'); await A.click('dialog[open] button:has-text("With the wizard")'); await att(A, 800)
await A.locator('dialog[open] label:has-text("Alter-ego name") input').fill('Jane Foster'); await suivant(A)
await A.click('dialog[open] .pastille[title="Justice"]'); await att(A, 400)
for (let i = 0; i < 5; i++) await suivant(A)
await A.click('dialog[open] button:has-text("Finish")'); await att(A, 1500)
await ouvrirSections(A); await A.locator('#champs input[type=file]').first().setInputFiles(PHOTO); await att(A, 1200)
await versAccueil(A)
await dossierVide(A, 'Rhino', 'Scenario'); await carteVide(A); await versAccueil(A)
// une pochette independante, avec une image
await A.click('.tuile-creer.pochette[data-creer="heros"]'); await att(A, 800)
for (let k = 0; k < 9; k++) {
  const t = await A.locator('dialog[open] .assistant-titre').innerText()
  if (/THE NAME AND THE TITLE/i.test(t)) await A.locator('dialog[open] textarea').first().fill('Thor')
  if (/THE ARTWORK/i.test(t)) { await A.locator('dialog[open] input[type=file]').first().setInputFiles(PHOTO); await att(A, 1200) }
  if (!(await A.locator('dialog[open] button:has-text("Next ▶")').count())) break
  await suivant(A)
}
await A.click('dialog[open] button:has-text("Finish")'); await att(A, 1200)
await versAccueil(A)
const avant = await resume(A)
console.log('  A avant :', JSON.stringify(avant))
await att(A, 1500)
await A.click('.tuile:has-text("Thor")'); await att(A, 900)
const [d] = await Promise.all([A.waitForEvent('download', { timeout: 120000 }), A.click('#p-exporter')])
const zipf = path.join(TMP, d.suggestedFilename()); await d.saveAs(zipf)
ok('A : le fichier est un .zip', /\.zip$/.test(zipf), zipf)
console.log('  taille du zip :', Math.round(fs.statSync(zipf).size / 1024), 'Ko')
// ---- ordinateur B : navigateur vierge, on importe
const B = await nouvelle()
await B.goto(U); await attendreAccueil(B)
await B.setInputFiles('#p-fichier', zipf); await att(B, 2500)
const apres = await resume(B)
console.log('  B apres :', JSON.stringify(apres))
ok('B : on arrive sur la page des dossiers', await B.locator('#vue-accueil').isVisible())
ok('B : memes dossiers, memes nombres de cartes, memes couleurs', JSON.stringify(apres.tuiles) === JSON.stringify(avant.tuiles), JSON.stringify(apres.tuiles))
ok('B : la pochette independante est revenue', JSON.stringify(apres.pochettes) === JSON.stringify(avant.pochettes) && apres.pochettes.length === 1, JSON.stringify(apres.pochettes))
ok('B : Thor dans « Heroes », Rhino dans « Scenarios »', await B.evaluate(() => { const r = [...document.querySelectorAll('.rangee-dossiers')]; return /Thor/.test(r[0].textContent) && /Rhino/.test(r[1].textContent) }))
await B.click('.tuile:has-text("Thor")'); await att(B, 1500)
ok('B : 20 cartes dans le dossier', (await resume(B)).total >= 20)
await B.click('#panneau-template summary'); await att(B, 300)
ok('B : le template du dossier est la (« enregistre »)', /Template saved/.test(await B.locator('#panneau-template .origine').first().innerText()))
// lien recto-verso identite <-> alter-ego conserve
await B.click('#liste .carte-liste:has-text("Jane Foster")'); await att(B, 800)
await ouvrirSections(B)
const dos = await B.locator('#champs details[data-titre="Dos de la carte"] select').first().inputValue()
ok('B : le dos de l\'alter-ego est « une autre carte » (recto-verso conserve)', dos === 'carte', dos)
const cible = await B.locator('#champs details[data-titre="Dos de la carte"] select').nth(1).evaluate((s) => s.options[s.selectedIndex]?.textContent ?? '')
ok('B : ... et cette carte est bien l\'identite Thor', /Thor/.test(cible), cible)
// ---- mode « Remplacer » sur A (qui a deja un projet) : on ajoute un dossier parasite avant
await versAccueil(A)
await dossierVide(A, 'Parasite'); await carteVide(A); await versAccueil(A)
await A.setInputFiles('#p-fichier', zipf); await att(A, 1200)
const q = await A.locator('dialog[open]').innerText()
ok('A : import sur un projet existant : question « Ajouter / Remplacer »', /add/i.test(q) && /replace everything/i.test(q), q)
await A.click('dialog[open] button:has-text("Replace everything")'); await att(A, 2000)
const rem = await resume(A)
ok('A : « Remplacer » : le dossier parasite a disparu, le reste est identique', JSON.stringify(rem.tuiles) === JSON.stringify(avant.tuiles) && rem.pochettes.length === 1, JSON.stringify(rem))
// ---- mode « Ajouter » : on fusionne
await A.setInputFiles('#p-fichier', zipf); await att(A, 1200)
await A.click('dialog[open] button:has-text("Add")'); await att(A, 2000)
const ajout = await resume(A)
ok('A : « Ajouter » : les dossiers du meme nom sont fusionnes (cartes doublees)', ajout.tuiles.some((t) => /^THOR\|40 /i.test(t) || /Thor\|40/.test(t)) || ajout.tuiles.some((t) => /40 card/.test(t)), JSON.stringify(ajout.tuiles))
console.log(errs.length ? 'ERREURS ' + errs : 'sans erreur de page')
await b.close()
process.exit(rates ? 1 : 0)
