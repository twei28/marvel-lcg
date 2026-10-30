// Test de fumee du createur de cartes dans Chromium : chaque fonction de la page, sans compte ni serveur (mode local).
//   cd public && python3 -m http.server 8792 --bind 127.0.0.1      (dans un autre terminal)
//   node tools/createur-cartes/essai/fumee-createur.mjs [http://127.0.0.1:8792]
// Images d'essai : Valkyrie (essai/valkyrie-*.png), jamais Kamala. Sort avec un code non nul si un controle rate.
// Interface du 30/10/2026 : page des dossiers, editeur d'un dossier, wizards (gestes communs dans aide-ui.mjs).
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import path from 'node:path'
import fs from 'node:fs'
import os from 'node:os'
import { fileURLToPath } from 'node:url'
import { attendreAccueil, dossierVide, versAccueil, ouvrirTuile, ouvrirSections, nbCartes as nbTotal, exporterVia } from './aide-ui.mjs'

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
const nbCartes = () => nbTotal(p)
const nbVisibles = () => p.locator('#liste .carte-liste').count()
const toileVide = () => p.evaluate(() => { const c = document.querySelector('#toile'); const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 400) if (d[i]) n++; return n === 0 })
const telechargement = async (clic, motif = /./) => { const [d] = await Promise.all([p.waitForEvent('download', { timeout: 120000, predicate: (x) => motif.test(x.suggestedFilename()) }), clic()]); const f = path.join(TMP, d.suggestedFilename()); await d.saveAs(f); return { nom: d.suggestedFilename(), taille: fs.statSync(f).size, f } }
const suivant = async () => { await p.click('dialog[open] button:has-text("Next ▶")'); await att(450) }

await p.goto(U + '/createur-cartes.html'); await attendreAccueil(p)
ok('page en anglais par defaut', (await p.locator('#ui-en').getAttribute('aria-pressed')) === 'true')
ok('carte en anglais par defaut', (await p.locator('#lang-en').getAttribute('aria-pressed')) === 'true')
ok('indicateur : « enregistré dans ce navigateur » affiché en mode local', await p.locator('#etat-serveur').isVisible())
ok('accueil : sept tuiles de creation (heros, scenario, modulaire, insert + 3 pochettes)', (await p.locator('.tuile-creer').count()) === 7 && (await p.locator('.tuile-creer.pochette').count()) === 3)
ok('accueil : aucun dossier au depart', (await p.locator('.tuile').count()) === 0)
ok('accueil : l\'editeur est cache', await p.locator('#vue-editeur').isHidden())

await essai('wizard de heros : dossier, template, 20 cartes, tuile avec l\'alter-ego', async () => {
  await p.click('.tuile-creer.cartes[data-creer="heros"]'); await att(300)
  await p.fill('dialog[open] input', 'Thor'); await p.click('dialog[open] button:has-text("With the wizard")'); await att(800)
  await p.locator('dialog[open] label:has-text("Alter-ego name") input').fill('Jane Foster')
  await suivant()
  await p.click('dialog[open] .pastille[title="Justice"]'); await att(400)
  ok('wizard heros : pickers de couleur (pastille, code hexa)', (await p.locator('dialog[open] input[type=color]').count()) >= 3 && (await p.locator('dialog[open] input.hex').count()) >= 3)
  for (let i = 0; i < 4; i++) await suivant()
  ok('wizard heros : 15 emplacements pour le paquet', (await p.locator('dialog[open] .quinze select').count()) === 15)
  await suivant()
  await p.click('dialog[open] button:has-text("Finish")'); await att(1500)
  ok('wizard heros : l\'editeur s\'ouvre sur le dossier (20 cartes)', (await nbCartes()) === 20 && /THOR/i.test(await p.locator('#fil').innerText()), await p.locator('#fil').innerText())
  ok('colonne des cartes : sections par type (identite, alter-ego, allies...)', (await p.locator('#liste .groupe-type').count()) >= 5)
  ok('sections du formulaire toutes repliees a l\'ouverture', (await p.locator('#champs details[open]').count()) === 0)
  await versAccueil(p)
  const tuile = await p.locator('.tuile').first().innerText()
  ok('tuile du heros : nom + alter-ego + nombre de cartes', /Thor/i.test(tuile) && /Jane Foster/.test(tuile) && /20/.test(tuile), tuile)
})

await essai('dossier vide + wizard de carte (passer partout)', async () => {
  await dossierVide(p, 'Loki')
  ok('dossier vide : l\'editeur propose « + Nouvelle carte »', (await p.locator('#vide-dossier').isVisible()) && !(await p.locator('#scene').isVisible()))
  await p.click('#vide-dossier button'); await att(900)
  await p.click('dialog[open] .assistant-types button:has-text("Ally")'); await att(300)
  let etapes = 0
  for (let k = 0; k < 14; k++) {
    const titre = await p.locator('dialog[open] .assistant-titre').innerText()
    etapes++
    if (/NAME AND TRAITS/i.test(titre)) await p.locator('dialog[open] label:has-text("Title") input').first().fill('Heimdall')
    if (!(await p.locator('dialog[open] button:has-text("Next ▶")').count())) break
    await suivant()
  }
  ok('wizard de carte : passe sur tout (>= 11 etapes)', etapes >= 11, etapes)
  await p.click('dialog[open] button:has-text("Finish")'); await att(1500)
  ok('wizard de carte : la carte est dans le dossier', /LOKI/i.test(await p.locator('#fil').innerText()) && (await nbVisibles()) === 1, await p.locator('#fil').innerText())
})

await essai('25 types', async () => {
  const types = await p.evaluate(() => [...document.querySelectorAll('#type option')].map((o) => o.value))
  ok('25 types proposes (dont 2 inserts)', types.length === 25, types.length)
  let vides = []
  for (const t of types) { await p.selectOption('#type', t); await att(350); if (await toileVide()) vides.push(t) }
  ok('chaque type se dessine', vides.length === 0, vides.join(','))
  await p.selectOption('#type', 'ally'); await att(300)
})

await essai('langue de la carte', async () => {
  await ouvrirSections(p); await p.locator('label:has-text("Set line") input').fill('hand size 6 / hit points 10'); await att(400)
  await p.click('#lang-fr'); await att(400)
  const ligne = () => p.evaluate(() => [...document.querySelectorAll('#champs input, #champs textarea')].map((i) => i.value).find((v) => /hand size|taille de main/i.test(v)) ?? '')
  const f = await ligne()
  await p.click('#lang-en'); await att(400)
  const e = await ligne()
  ok('FR puis EN : la ligne « Taille de main / Hand size » est traduite', /taille de main/i.test(f) && /hand size/i.test(e), f + ' / ' + e)
})

await essai('titre, annuler / retablir', async () => {
  await ouvrirSections(p)
  const champ = p.locator('label:has-text("Title") input').first()
  await champ.fill('Valkyrie'); await att(900)
  await champ.fill('Valkyrie X'); await att(900)
  await p.click('#b-annuler'); await att(500)
  ok('annuler', (await champ.inputValue()) === 'Valkyrie', await champ.inputValue())
  await p.click('#b-retablir'); await att(500)
  ok('retablir', (await champ.inputValue()) === 'Valkyrie X', await champ.inputValue())
  await p.keyboard.press('Escape')
})

await essai('cartes : dupliquer, deplacer, supprimer, recherche', async () => {
  const n0 = await nbCartes()
  await p.click('#c-dupliquer'); await att(500)
  ok('dupliquer', (await nbCartes()) === n0 + 1, `${n0} -> ${await nbCartes()}`)
  await p.fill('#recherche', 'Valkyrie X'); await att(400)
  ok('recherche filtre la colonne', (await nbVisibles()) < n0 + 1, await nbVisibles())
  await p.fill('#recherche', ''); await att(300)
  // deplacer vers un autre dossier (nouveau)
  await p.click('#c-deplacer'); await att(300)
  await p.fill('dialog[open] input[type=text]', 'Asgard'); await p.click('dialog[open] button:has-text("Move")'); await att(900)
  ok('deplacer : la carte suit dans le dossier Asgard', /ASGARD/i.test(await p.locator('#fil').innerText()), await p.locator('#fil').innerText())
  await p.click('#c-supprimer'); await att(600)
  ok('supprimer : on reste dans le dossier, devenu vide', await p.locator('#vide-dossier').isVisible())
  await versAccueil(p)
  ok('dossier Asgard vide visible a l\'accueil', (await p.locator('.tuile:has-text("Asgard")').count()) === 1)
})

await essai('template du dossier : couleurs, enregistrement, application', async () => {
  await ouvrirTuile(p, 'Loki')
  await p.click('#panneau-template summary'); await att(300)
  await p.locator('#panneau-template input.hex').first().fill('#2244aa'); await att(300)
  await p.click('#panneau-template button:has-text("Save the template")'); await att(500)
  ok('template : question « appliquer aux cartes ? » avec le nombre', /1 card/.test(await p.locator('dialog[open]').innerText()), await p.locator('dialog[open]').innerText())
  await p.click('dialog[open] button:has-text("The 1 cards")'); await att(900)
  ok('template : le panneau dit « enregistre »', /Template saved/.test(await p.locator('#panneau-template .origine').first().innerText()))
  await ouvrirSections(p)
  const origine = () => p.locator('#champs details[data-titre="Couleurs"] .origine').innerText()
  ok('couleurs : origine « template »', /Template colours/.test(await origine()), await origine())
  await p.locator('#champs details[data-titre="Couleurs"] input.hex').first().fill('#cc0000'); await att(500)
  ok('couleurs : origine « personnalisee »', /Custom colours/.test(await origine()))
  await p.click('#champs details[data-titre="Couleurs"] button:has-text("Back to the template")'); await att(600)
  ok('couleurs : retour au template', /Template colours/.test(await origine()))
})

await essai('menu ⋯ d\'un dossier : renommer, dupliquer, supprimer en tapant le nom', async () => {
  await versAccueil(p)
  await p.click('.tuile:has-text("Asgard") .menu-pt'); await p.click('.menu-flottant button:has-text("Rename")'); await att(300)
  await p.fill('dialog[open] input', 'Midgard'); await p.click('dialog[open] button:has-text("Rename")'); await att(500)
  ok('renommer', (await p.locator('.tuile:has-text("Midgard")').count()) === 1)
  await p.click('.tuile:has-text("Midgard") .menu-pt'); await p.click('.menu-flottant button:has-text("Duplicate")'); await att(500)
  ok('dupliquer un dossier', (await p.locator('.tuile:has-text("Midgard")').count()) === 2)
  await p.click('.tuile:has-text("Midgard (copy)") .menu-pt'); await p.click('.menu-flottant button:has-text("Delete…")'); await att(300)
  await p.fill('dialog[open] input', 'faux'); await p.click('dialog[open] button:has-text("Delete")'); await att(300)
  ok('supprimer : un mauvais nom ne supprime pas', (await p.locator('dialog[open]').count()) === 1)
  await p.fill('dialog[open] input', 'Midgard (copy)'); await p.click('dialog[open] button:has-text("Delete")'); await att(500)
  ok('supprimer : le bon nom supprime', (await p.locator('.tuile:has-text("Midgard")').count()) === 1)
})

await essai('chercher / remplacer, appliquer au dossier, versions', async () => {
  await ouvrirTuile(p, 'Thor')
  await p.click('#p-remplacer'); await p.waitForSelector('dialog')
  await p.locator('dialog input[type=text]').first().fill('Thor'); await p.locator('dialog input[type=text]').nth(1).fill('Odinson'); await att(300)
  ok('chercher : compte les occurrences', /match/i.test(await p.locator('dialog').textContent()), (await p.locator('dialog').textContent()).slice(0, 200))
  await p.click('dialog button:has-text("Replace all")'); await att(500)
  await p.fill('#recherche', 'Odinson'); await att(300)
  ok('remplacer', (await p.locator('#liste').textContent()).includes('Odinson'))
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
  await ouvrirSections(p)
  await p.locator('#champs input[type=file]').first().setInputFiles(photo); await att(1200)
  ok('illustration posee', !(await toileVide()))
  await p.locator('#champs input[type=file]').last().setInputFiles(tete).catch(() => {}); await att(1000)
  await ouvrirSections(p); await att(300)
  const bt = p.locator('#champs button:visible:has-text("Cut out")'); if (await bt.count()) { await bt.first().click(); await p.waitForSelector('dialog'); ok('recadrage : fenetre', true); const restes = await p.locator('dialog[open]').count(); await p.evaluate(() => document.querySelectorAll('dialog[open]').forEach((x) => x.close())); ok('recadrage : fenetre fermable', restes <= 1); await att(300) } else ok('bouton recadrage', false, 'absent')
})

await essai('pochettes : wizard, editeur, export PNG, rattachement a un dossier, pack .zip', async () => {
  const photo = path.join(ICI, '../../../public/createur-cartes/_essai/valkyrie-photo.png')
  await versAccueil(p)
  await p.click('.tuile-creer.pochette[data-creer="scenario"]'); await att(900)
  let etapes = 0
  for (let k = 0; k < 12; k++) {
    const titre = await p.locator('dialog[open] .assistant-titre').innerText()
    etapes++
    if (/THE NAME AND THE TITLE/i.test(titre)) await p.locator('dialog[open] textarea').first().fill('Rhino')
    if (/THE ARTWORK/i.test(titre)) { await p.locator('dialog[open] input[type=file]').first().setInputFiles(photo); await att(1200) }
    if (!(await p.locator('dialog[open] button:has-text("Next ▶")').count())) break
    await suivant()
  }
  ok('wizard de pochette : passe sur tout (>= 8 etapes)', etapes >= 8, etapes)
  await p.click('dialog[open] button:has-text("Finish")'); await att(1500)
  ok('pochette : l\'editeur s\'ouvre (fil d\'Ariane)', (await p.locator('#vue-pochette').isVisible()) && /RHINO/i.test(await p.locator('#fil').innerText()), await p.locator('#fil').innerText())
  ok('pochette : l\'apercu est dessine', await p.evaluate(() => { const c = document.querySelector('#toile-pochette'); return c.width === 938 && c.height === 1538 }))
  await p.evaluate(() => document.querySelectorAll('#form-pochette details').forEach((d) => { d.open = true }))
  const png = await telechargement(() => p.click('#form-pochette button:has-text("Download as PNG")'), /\.png$/); ok('pochette : export PNG', png.taille > 20000, png.nom + ' ' + png.taille)
  await versAccueil(p)
  ok('pochette independante : rangee « Pochettes » a l\'accueil', (await p.locator('.rangee-pochettes .tuile').count()) === 1)
  // rattachee a un dossier : depuis la colonne des cartes
  await ouvrirTuile(p, 'Thor')
  await p.click('#colonne-cartes .groupe-pochette button:has-text("New cover")'); await att(900)
  await p.click('dialog[open] .assistant-types button >> nth=0'); await suivant()
  ok('wizard de pochette dans un dossier : le dossier est preselectionne', /Thor/.test(await p.locator('dialog[open] .tuile-dossier.choisie').innerText()))
  for (let k = 0; k < 10 && (await p.locator('dialog[open] button:has-text("Next ▶")').count()); k++) await suivant()
  await p.click('dialog[open] button:has-text("Finish")'); await att(1500)
  await p.click('#fil button:has-text("Thor")'); await att(1200)
  ok('colonne des cartes : section « Pochette (1) »', /Cover \(1\)/i.test(await p.locator('#colonne-cartes .groupe-pochette summary').innerText()), await p.locator('#colonne-cartes .groupe-pochette summary').innerText())
  // le pack .zip du dossier contient la pochette
  await exporterVia(p, '#b-pack'); await p.waitForSelector('dialog')
  const zip = await telechargement(() => p.click('dialog button:has-text("Export")'))
  ok('pack .zip : contient « pochettes/ »', fs.readFileSync(zip.f).includes('pochettes/'), zip.nom)
})

await essai('exports', async () => {
  await exporterVia(p, '#b-export'); await p.waitForSelector('dialog')
  const png = await telechargement(() => p.click('dialog button:has-text("Export")')); ok('export PNG', /\.png$/.test(png.nom) && png.taille > 20000, png.nom + ' ' + png.taille)
  await exporterVia(p, '#b-pack'); await p.waitForSelector('dialog')
  const zip = await telechargement(() => p.click('dialog button:has-text("Export")')); ok('pack .zip', /\.zip$/.test(zip.nom) && zip.taille > 20000, zip.nom + ' ' + zip.taille)
  const tts = await telechargement(() => exporterVia(p, '#b-tts')); ok('planche TTS', tts.taille > 10000, tts.nom + ' ' + tts.taille)
  await att(1500)
  const proj = await telechargement(() => p.click('#p-exporter'), /\.zip$/); ok('tout enregistrer (.zip)', /\.zip$/.test(proj.nom) && proj.taille > 1000, proj.nom)
  const n = await nbCartes(); await p.setInputFiles('#p-fichier', proj.f); await att(1200)
  await p.click('dialog[open] button:has-text("Add")'); await att(1800)
  await p.click('#vue-accueil .tuile >> nth=0'); await att(900)
  ok('reimport de la sauvegarde complete (ajouter) : cartes ajoutees', (await nbCartes()) > n, `${n} -> ${await nbCartes()}`)
})

await essai('comparable (hors site : message de scan)', async () => {
  await p.click('#b-comparer'); await p.waitForSelector('dialog'); await att(800)
  ok('carte comparable : fenetre', /real comparable card/i.test(await p.locator('dialog').textContent())); await p.keyboard.press('Escape'); await att(300)
})

await essai('colonnes redimensionnables', async () => {
  await p.evaluate(() => scrollTo(0, 0)); await att(200)
  const w0 = await p.locator('#colonne-cartes').evaluate((e) => e.getBoundingClientRect().width)
  const h = await p.locator('#poignee-2').boundingBox()
  await p.mouse.move(h.x + 4, h.y + 100); await p.mouse.down(); await p.mouse.move(h.x - 80, h.y + 100, { steps: 6 }); await p.mouse.up(); await att(300)
  const w1 = await p.locator('#colonne-cartes').evaluate((e) => e.getBoundingClientRect().width)
  ok('glisser la poignee elargit la colonne des cartes', w1 > w0 + 40, `${Math.round(w0)} -> ${Math.round(w1)}`)
})

await essai('langue de la page', async () => {
  await p.click('#ui-fr'); await att(500)
  ok('page en francais', /dossiers/i.test(await p.locator('#fil').innerText()), await p.locator('#fil').innerText())
  await p.click('#ui-en'); await att(300)
})

await essai('persistance (IndexedDB)', async () => {
  await att(1200); await p.reload(); await attendreAccueil(p)
  ok('rechargement : on revient a la page des dossiers', await p.locator('#vue-accueil').isVisible())
  ok('rechargement : les dossiers sont toujours la', (await p.locator('.tuile').count()) >= 3, await p.locator('.tuile').count())
})

await essai('insert : dossier, carte, rendu', async () => {
  await p.locator('.tuile-creer[data-creer="insert"]').click()
  await p.fill('dialog input', 'Essai insert')
  await p.getByRole('button', { name: /create an insert|créer un insert/i }).click()
  await att(900)
  ok('insert : la carte est ouverte, de type insert', await p.evaluate(() => document.querySelector('select')?.value) === 'insert')
  await versAccueil(p)
  ok('insert : le dossier est dans la rangee Inserts', (await p.locator('.rangee-dossiers h3', { hasText: /^inserts$/i }).count()) === 1)
})

console.log(erreurs.length ? 'ERREURS PAGE :\n' + erreurs.join('\n') : 'Aucune erreur dans la page.')
await b.close()
process.exit(rates || erreurs.length ? 1 : 0)
