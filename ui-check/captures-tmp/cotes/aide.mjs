import { chromium } from '@playwright/test'
const DOSSIER = 'captures-tmp/cotes'
const nav = await chromium.launch()
const page = await nav.newPage({ viewport: { width: 1600, height: 900 } })
const erreurs = []
page.on('pageerror', (e) => erreurs.push(String(e)))
// (4) partie ordinaire sans moteur : l'ecran se monte-t-il quand meme ?
await page.goto('http://127.0.0.1:8771/app/board.html?p=0')
await page.waitForTimeout(3000)
const aide = await page.locator('button.volet-aide-languette').count()
console.log('LANGUETTE', aide)
if (aide) {
  await page.click('button.volet-aide-languette')
  console.log('VOLET', await page.locator('#volet-aide-auto').count(), (await page.locator('#volet-aide-auto').innerText()).slice(0, 120).replace(/\n/g, ' | '))
  await page.screenshot({ path: `${DOSSIER}/5-aide.png` })
}
// (5) relecture : reglages > apparence > modifier la table
await page.goto('http://127.0.0.1:8771/app/board.html?relecture=1')
await page.evaluate(() => { localStorage.removeItem('mc_noms_zones_v1'); localStorage.removeItem('mc_ameliorations_cote') })
await page.reload()
await page.setInputFiles('input[type=file]', `${DOSSIER}/test.marvelreplay`)
await page.click('.relecture-fiche .relecture-bouton-lecture')
await page.waitForSelector('[data-card-id="61"]')
const boutons = await page.evaluate(() => [...document.querySelectorAll('button')].map((b) => (b.getAttribute('aria-label') || b.title || b.textContent || '').trim()).filter(Boolean).slice(0, 40))
console.log('BOUTONS', JSON.stringify(boutons))
await page.click('button[aria-label="Réglages"], button[title="Réglages"]')
await page.waitForTimeout(300)
const modif = page.getByRole('button', { name: 'Modifier la table' })
console.log('MODIFIER', await modif.count())
if (await modif.count()) {
  await modif.click()
  await page.waitForSelector('.editeur-zone')
  const zones = await page.evaluate(() => [...document.querySelectorAll('.editeur-zone')].map((z) => [z.dataset.zone, z.querySelector('.editeur-zone-nom')?.textContent]))
  console.log('ZONES', JSON.stringify(zones))
  const cible = page.locator('.editeur-zone[data-zone="heros"] .editeur-zone-nom')
  await cible.dblclick()
  await page.fill('.editeur-zone-saisie', 'Mon camp')
  await page.keyboard.press('Enter')
  await page.screenshot({ path: `${DOSSIER}/6-editeur.png` })
  console.log('EDITEUR', await page.locator('.editeur-zone[data-zone="heros"] .editeur-zone-nom').innerText())
  await page.getByRole('button', { name: 'Terminer' }).click()
  await page.waitForTimeout(400)
  console.log('TABLE', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('.plateau-emplacement-titre')].map((h) => h.textContent))))
  await page.screenshot({ path: `${DOSSIER}/7-table.png` })
}
console.log('ERREURS', JSON.stringify(erreurs))
await nav.close()
