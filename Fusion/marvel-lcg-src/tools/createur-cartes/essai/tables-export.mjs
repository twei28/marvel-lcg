// Fabrique un petit set (Valkyrie) dans la page, l'exporte en pack avec OCTGN + DragnCards, et laisse le .zip dans le dossier donne.
//   node tables-export.mjs <dossier de sortie> [http://127.0.0.1:8792]
import { chromium } from 'file:///home/oem/Desktop/Marvel%20LCG/ui-check/node_modules/@playwright/test/index.mjs'
import path from 'node:path'
const SORTIE = process.argv[2], U = process.argv[3] ?? 'http://127.0.0.1:8792'
const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1500, height: 950 }, acceptDownloads: true }); const p = await ctx.newPage()
const erreurs = []; p.on('pageerror', (e) => erreurs.push(String(e)))
await p.goto(U + '/createur-cartes.html'); await p.waitForSelector('#liste button'); await p.waitForTimeout(1500)
const att = (ms = 500) => p.waitForTimeout(ms)
async function carte(type, titre, dossier = 'Valkyrie') {
  await p.selectOption('#type', type); await att(300)
  await p.locator('label:has-text("Title") input').first().fill(titre)
  await p.fill('input[list=dossiers-connus]', dossier); await p.locator('input[list=dossiers-connus]').blur(); await att(400)
  // nouveau dossier : l'assistant propose de regler son gabarit (29/10/2026) - on decline pour ce script.
  if (await p.locator('dialog button:has-text("Later")').isVisible().catch(() => false)) { await p.click('dialog button:has-text("Later")'); await att(300) }
}
await carte('identity', 'Valkyrie')
for (const [t, n] of [['alter-ego', 'Brunnhilde'], ['ally', 'Skurge'], ['event', 'Death Glow'], ['sidescheme', 'Realm Under Siege'], ['main_scheme_a', 'Descent'], ['main_scheme_b', 'Descent B'], ['minion', 'Draugr'], ['villain', 'Fenrir'], ['environment', 'Bifrost'], ['resource', 'Valor'], ['upgrade', 'Sword'], ['support', 'Throne'], ['treachery', 'Ragnarok'], ['attachment', 'Curse'], ['obligation', 'Duty'], ['playersidescheme', 'Quest']]) {
  await p.click('#c-nouvelle'); await att(400); await carte(t, n)
}
// du texte, de la citation et « unique » sur une carte : Text / Quote / Unique dans le set OCTGN
await p.click('#liste button:has-text("Skurge")'); await att(500)
await p.locator('#champs .editeur').first().click(); await p.keyboard.type('Response: After Skurge attacks, draw 1 card & smile.'); await att(300)
await p.locator('#champs .editeur').nth(1).click(); await p.keyboard.type('Quote of the day'); await att(300)
await p.locator('#champs label:has-text("Unique") input[type=checkbox]').first().check(); await att(500)
// « par joueur » : menace de depart d'une manigance annexe, PV d'un mechant (icone en fin de ligne d'ensemble)
await p.click('#liste button:has-text("Realm Under Siege")'); await att(500)
await p.evaluate(() => document.querySelectorAll('#champs details').forEach((d) => { d.open = true }))
await p.locator('.nombre:has([data-champ=menaceDepart]) label.ligne input').last().check(); await att(400)
await p.click('#liste button:has-text("Fenrir")'); await att(500)
await p.evaluate(() => document.querySelectorAll('#champs details').forEach((d) => { d.open = true }))
await p.locator('[data-champ=ligneEnsemble]').fill('FENRIR (1/21) / HIT POINTS 14'); await att(300)
await p.locator('#champs label.ligne:has-text("Points de vie par joueur") input, #champs label.ligne:has-text("Hit points per hero") input').first().check(); await att(500)
console.log('ligne villain:', await p.locator('[data-champ=ligneEnsemble]').inputValue())
await p.click('#b-pack'); await p.waitForSelector('dialog')
const cases = p.locator('dialog label.ligne')
for (const nom of ['OCTGN', 'DragnCards']) await p.locator('dialog label.ligne', { hasText: nom }).locator('input').check()
await p.locator('dialog input[type=text]').fill('https://exemple.test/img/')
const [d] = await Promise.all([p.waitForEvent('download', { timeout: 180000 }), p.click('dialog button:has-text("Export")')])
await d.saveAs(path.join(SORTIE, 'pack.zip')); console.log('pack', d.suggestedFilename())
console.log(erreurs.length ? 'ERREURS ' + erreurs : 'sans erreur')
await b.close()
