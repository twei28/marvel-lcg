// Test de fumee du createur de cartes dans Chromium : chaque fonction de la page, sans compte ni serveur (mode local).
//   cd public && python3 -m http.server 8792 --bind 127.0.0.1      (dans un autre terminal)
//   node tools/createur-cartes/essai/fumee-createur.mjs [http://127.0.0.1:8792]
// Images d'essai : Valkyrie (essai/valkyrie-*.png), jamais Kamala. Sort avec un code non nul si un controle rate.
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import path from 'node:path'
import fs from 'node:fs'
import os from 'node:os'
import { fileURLToPath } from 'node:url'

const U = process.argv[2] ?? 'http://127.0.0.1:8792'
const ICI = path.dirname(fileURLToPath(import.meta.url))
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'fumee-'))
const b = await chromium.launch()
const ctx = await b.newContext({ viewport: { width: 1500, height: 950 }, acceptDownloads: true })
const p = await ctx.newPage()
const erreurs = []
p.on('pageerror', (e) => erreurs.push('pageerror: ' + e))
p.on('console', (m) => m.type() === 'error' && !/404|ERR_/.test(m.text()) && erreurs.push('console: ' + m.text()))
p.on('dialog', (d) => d.accept(d.type() === 'prompt' ? 'Essai' : undefined))
let rates = 0
const ok = (nom, cond, detail = '') => { if (!cond) rates++; console.log((cond ? '  OK   ' : '  RATE ') + nom + (cond ? '' : ' | ' + detail)) }
async function essai(nom, fn) {
  try { await fn() } catch (e) {
    rates++; console.log('  RATE ' + nom + ' | exception : ' + String(e).split('\n').slice(0, 4).join(' / '))
    const d = await p.evaluate(() => [...document.querySelectorAll('dialog[open]')].map((x) => x.textContent.slice(0, 120))).catch(() => [])
    if (d.length) { console.log('         dialogue(s) reste(nt) ouvert(s) :', d); await p.evaluate(() => document.querySelectorAll('dialog[open]').forEach((x) => x.close())).catch(() => {}) }
  }
}
const att = (ms = 700) => p.waitForTimeout(ms)
// toutes les cartes du projet (la liste ne montre que le dossier ouvert, ou les tuiles des dossiers)
const nbCartes = async () => Number(await p.locator('#liste').getAttribute('data-total'))
const nbVisibles = () => p.locator('#liste .carte-liste').count()
// les sections du formulaire sont repliees a l'ouverture d'une carte (30/10/2026)
const ouvrirSections = () => p.evaluate(() => document.querySelectorAll('#champs details').forEach((d) => { d.open = true }))
const toileVide = () => p.evaluate(() => { const c = document.querySelector('#toile'); const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 400) if (d[i]) n++; return n === 0 })
const telechargement = async (clic) => { const [d] = await Promise.all([p.waitForEvent('download', { timeout: 120000 }), clic()]); const f = path.join(TMP, d.suggestedFilename()); await d.saveAs(f); return { nom: d.suggestedFilename(), taille: fs.statSync(f).size, f } }

await p.goto(U + '/createur-cartes.html'); await p.waitForSelector('#liste button'); await att(1500)
ok('page en anglais par defaut', (await p.locator('#ui-en').getAttribute('aria-pressed')) === 'true')
ok('carte en anglais par defaut', (await p.locator('#lang-en').getAttribute('aria-pressed')) === 'true')
ok('indicateur serveur cache en mode local', await p.locator('#etat-serveur').isHidden())

await essai('23 types', async () => {
  const types = await p.evaluate(() => [...document.querySelectorAll('#type option')].map((o) => o.value))
  ok('23 types proposes', types.length === 23, types.length)
  let vides = []
  for (const t of types) { await p.selectOption('#type', t); await att(350); if (await toileVide()) vides.push(t) }
  ok('chaque type se dessine', vides.length === 0, vides.join(','))
  await p.selectOption('#type', 'ally'); await att(300)
})

await essai('langue de la carte', async () => {
  // une carte neuve est vide (30/10/2026) : on pose la ligne du bas avant de changer de langue
  await ouvrirSections(); await p.locator('label:has-text("Set line") input').fill('hand size 6 / hit points 10'); await att(400)
  await p.click('#lang-fr'); await att(400)
  const ligne = () => p.evaluate(() => [...document.querySelectorAll('#champs input, #champs textarea')].map((i) => i.value).find((v) => /hand size|taille de main/i.test(v)) ?? '')
  const f = await ligne()
  await p.click('#lang-en'); await att(400)
  const e = await ligne()
  ok('FR puis EN : la ligne « Taille de main / Hand size » est traduite', /taille de main/i.test(f) && /hand size/i.test(e), f + ' / ' + e)
})

await essai('titre, annuler / retablir', async () => {
  await ouvrirSections()
  const champ = p.locator('label:has-text("Title") input').first()
  await champ.fill('Valkyrie'); await att(900)
  await champ.fill('Valkyrie X'); await att(900)
  await p.click('#b-annuler'); await att(500)
  ok('annuler', (await champ.inputValue()) === 'Valkyrie', await champ.inputValue())
  await p.click('#b-retablir'); await att(500)
  ok('retablir', (await champ.inputValue()) === 'Valkyrie X', await champ.inputValue())
  await p.keyboard.press('Escape')
})

await essai('cartes : nouvelle, dupliquer, supprimer, recherche, dossiers', async () => {
  const n0 = await nbCartes()
  // « + New » ouvre l'assistant (30/10/2026) ; son lien du bas cree une carte vide directement
  await p.click('#c-nouvelle'); await att(400)
  ok('+ New ouvre l\'assistant', /What kind of card/.test(await p.locator('dialog[open]').textContent()))
  await p.click('dialog[open] button.lien'); await att(400); await p.click('#c-dupliquer'); await att(400)
  ok('nouvelle + dupliquer', (await nbCartes()) === n0 + 2, `${n0} -> ${await nbCartes()}`)
  await p.fill('input[list=dossiers-connus]', 'Valkyrie'); await p.locator('input[list=dossiers-connus]').blur(); await att(500)
  // nouveau dossier : l'assistant propose de regler son gabarit (29/10/2026, se declenche au blur) - on decline pour ce test.
  if (await p.locator('dialog button:has-text("Later")').isVisible().catch(() => false)) { await p.click('dialog button:has-text("Later")'); await att(300) }
  ok('dossier : un en-tete', (await p.locator('#liste .dossier').allTextContents()).some((t) => /Valkyrie/.test(t)))
  ok('dossier : en tuile', (await p.locator('#liste .tuile-dossier').allTextContents()).some((t) => /Valkyrie/.test(t)), (await p.locator('#liste').innerHTML()).slice(0, 400))
  await p.fill('#recherche', 'Valkyrie X'); await att(400)
  ok('recherche filtre', (await nbVisibles()) < n0 + 2, await nbVisibles())
  await p.fill('#recherche', ''); await att(300)
  await p.click('#c-supprimer'); await att(400)
  ok('supprimer', (await nbCartes()) === n0 + 1, await nbCartes())
})

await essai('templates', async () => {
  // l'assistant « Template » : dossier de la carte actuelle, on garde aussi la carte comme carte de depart
  await p.click('#m-enregistrer'); await att(500)
  await p.fill('dialog[open] input[placeholder="e.g. Valkyrie"]', 'Valkyrie'); await att(200)
  for (let i = 0; i < 5; i++) { await p.click('dialog[open] button:has-text("Next ▶")'); await att(300) }
  await p.locator('dialog[open] label:has-text("Also keep the current card") input').check(); await att(200)
  await p.click('dialog[open] button:has-text("Next ▶")'); await att(300)
  await p.click('dialog[open] button:has-text("Finish")'); await att(500)
  const opts = await p.evaluate(() => [...document.querySelectorAll('#modeles option')].map((o) => o.value))
  ok('template du dossier + carte de depart', opts.some((v) => v === 'g:Valkyrie') && opts.some((v) => v.startsWith('m:')), opts.join(','))
  const m = opts.find((v) => v.startsWith('m:'))
  await p.selectOption('#modeles', m); const n = await nbCartes(); await p.click('#m-utiliser'); await att(500)
  ok('carte de depart utilisee : une carte de plus', (await nbCartes()) === n + 1)
  await p.selectOption('#modeles', m); await p.click('#m-supprimer'); await att(400)
  ok('carte de depart supprimee', (await p.locator('#modeles option').count()) === 2)
})

await essai('chercher / remplacer, appliquer au dossier, versions', async () => {
  await p.click('#p-remplacer'); await p.waitForSelector('dialog')
  await p.locator('dialog input[type=text]').first().fill('Valkyrie'); await p.locator('dialog input[type=text]').nth(1).fill('Brunnhilde'); await att(300)
  ok('chercher : compte les occurrences', /match/i.test(await p.locator('dialog').textContent()), (await p.locator('dialog').textContent()).slice(0, 200))
  await p.click('dialog button:has-text("Replace all")'); await att(500)
  await p.fill('#recherche', 'Brunnhilde'); await att(300)
  ok('remplacer', (await p.locator('#liste').textContent()).includes('Brunnhilde'))
  await p.fill('#recherche', ''); await att(300)
  await p.click('#p-appliquer'); await p.waitForSelector('dialog'); await p.click('dialog button:has-text("Cancel")'); await att(300)
  await p.click('#p-versions'); await p.waitForSelector('dialog'); ok('versions : fenetre', /Saved versions/.test(await p.locator('dialog').textContent())); await p.click('dialog button:has-text("Close")'); await att(300)
})

await essai('clic sur la carte pour editer', async () => {
  const z = await p.locator('#toile').boundingBox()
  await p.mouse.click(z.x + z.width * 0.5, z.y + z.height * 0.075); await att(700)
  ok('clic sur le titre : le champ titre prend le focus', await p.evaluate(() => document.activeElement?.dataset?.champ === 'titre'), await p.evaluate(() => document.activeElement?.tagName + ':' + document.activeElement?.dataset?.champ))
})

await essai('illustration, calques, recadrage', async () => {
  const photo = path.join(ICI, '../../../public/createur-cartes/_essai/valkyrie-photo.png'), tete = path.join(ICI, '../../../public/createur-cartes/_essai/valkyrie-head.png')
  await p.evaluate(() => document.querySelectorAll('#champs details').forEach((d) => { d.open = true }))
  await p.locator('#champs input[type=file]').first().setInputFiles(photo); await att(1200)
  ok('illustration posee', !(await toileVide()))
  await p.locator('#champs input[type=file]').last().setInputFiles(tete).catch(() => {}); await att(1000)
  await p.evaluate(() => document.querySelectorAll('#champs details').forEach((d) => { d.open = true })); await att(300)
  const b = p.locator('#champs button:visible:has-text("Cut out")'); if (await b.count()) { await b.first().click(); await p.waitForSelector('dialog'); ok('recadrage : fenetre', true); const restes = await p.locator('dialog[open]').count(); await p.evaluate(() => document.querySelectorAll('dialog[open]').forEach((x) => x.close())); ok('recadrage : fenetre fermable', restes <= 1); await att(300) } else ok('bouton recadrage', false, 'absent')
})

await essai('exports', async () => {
  await p.click('#b-export'); await p.waitForSelector('dialog')
  const png = await telechargement(() => p.click('dialog button:has-text("Export")')); ok('export PNG', /\.png$/.test(png.nom) && png.taille > 20000, png.nom + ' ' + png.taille)
  await p.click('#b-pack'); await p.waitForSelector('dialog')
  const zip = await telechargement(() => p.click('dialog button:has-text("Export")')); ok('pack .zip', /\.zip$/.test(zip.nom) && zip.taille > 20000, zip.nom + ' ' + zip.taille)
  const tts = await telechargement(() => p.click('#b-tts')); ok('planche TTS', tts.taille > 10000, tts.nom + ' ' + tts.taille)
  const proj = await telechargement(() => p.click('#p-exporter')); ok('projet .json', /\.json$/.test(proj.nom) && proj.taille > 1000, proj.nom)
  const n = await nbCartes(); await p.setInputFiles('#p-fichier', proj.f); await att(1500)
  ok('reimport du projet : cartes ajoutees', (await nbCartes()) > n, `${n} -> ${await nbCartes()}`)
})

await essai('comparable (hors site : message de scan)', async () => {
  await p.click('#b-comparer'); await p.waitForSelector('dialog'); await att(800)
  ok('carte comparable : fenetre', /real comparable card/i.test(await p.locator('dialog').textContent())); await p.keyboard.press('Escape'); await att(300)
})

await essai('langue de la page', async () => {
  await p.click('#ui-fr'); await att(500)
  ok('page en francais', /Créateur de cartes/.test(await p.locator('header h1').textContent()))
  await p.click('#ui-en'); await att(300)
})

await essai('persistance (IndexedDB)', async () => {
  await att(1200); await p.reload(); await p.waitForSelector('#liste button'); await att(1500)
  ok('rechargement : les cartes sont toujours la', (await nbCartes()) >= 3, await nbCartes())
})

console.log(erreurs.length ? 'ERREURS PAGE :\n' + erreurs.join('\n') : 'Aucune erreur dans la page.')
await b.close()
process.exit(rates || erreurs.length ? 1 : 0)
