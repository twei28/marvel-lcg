import { chromium } from '@playwright/test'
const DOSSIER = 'captures-tmp/cotes'
const nav = await chromium.launch()
const page = await nav.newPage({ viewport: { width: 1600, height: 900 } })
const erreurs = []
page.on('pageerror', (e) => erreurs.push(String(e)))
await page.goto('http://127.0.0.1:8771/app/board.html?relecture=1')
await page.evaluate(() => localStorage.clear())
await page.reload()
await page.setInputFiles('input[type=file]', `${DOSSIER}/test.marvelreplay`)
await page.click('.relecture-fiche .relecture-bouton-lecture')
await page.waitForSelector('[data-card-id="61"]')
await page.waitForTimeout(600)
const pastilles = () => page.evaluate(() => {
  const vue = (el) => { const s = getComputedStyle(el); const r = el.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 }
  const enJeu = [...document.querySelectorAll('.plateau-emplacement:not(.zone-main) .kind-pill')].filter(vue).length
  const main = [...document.querySelectorAll('.zone-main .kind-pill')].filter(vue).length
  const mainTotal = document.querySelectorAll('.zone-main .scan-card').length
  return { enJeu, main, mainTotal }
})
console.log('PASTILLES', JSON.stringify(await pastilles()))
await page.screenshot({ path: `${DOSSIER}/8-sans-etiquettes.png` })
await page.hover('[data-card-id="1"]')
await page.waitForTimeout(600)
console.log('APERCU', await page.evaluate(() => [...document.querySelectorAll('.carte-apercu .kind-pill')].filter((e) => getComputedStyle(e).display !== 'none').length))
await page.mouse.move(5, 5)
console.log('REGLAGES', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('button')].filter((b) => /Réglages/.test(b.getAttribute('aria-label') || b.title || b.textContent)).map((b) => [b.className, b.getAttribute('aria-label'), b.title, b.getBoundingClientRect().width, getComputedStyle(b).visibility]))))
await page.evaluate(() => [...document.querySelectorAll('button')].find((b) => /Réglages/.test(b.getAttribute('aria-label') || b.title || b.textContent))?.click())
await page.waitForTimeout(300)
const interrupteur = page.getByText('Étiquettes de type sur la table')
console.log('INTERRUPTEUR', await interrupteur.count())
if (await interrupteur.count()) {
  await interrupteur.first().click()
  await page.waitForTimeout(300)
  console.log('AVEC', JSON.stringify(await pastilles()), await page.evaluate(() => document.body.classList.contains('etiquettes-sur-la-table')))
  await interrupteur.first().click()
  await page.waitForTimeout(200)
}
const modif = page.getByRole('button', { name: 'Modifier la table' })
console.log('MODIFIER', await modif.count())
if (await modif.count()) {
  await modif.first().click()
  await page.waitForSelector('.editeur-zone')
  console.log('ZONES', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('.editeur-zone')].map((z) => z.dataset.zone))))
  await page.locator('.editeur-zone[data-zone="heros"] .editeur-zone-nom').dblclick()
  await page.fill('.editeur-zone-saisie', 'Mon camp')
  await page.keyboard.press('Enter')
  console.log('EDITEUR', await page.locator('.editeur-zone[data-zone="heros"] .editeur-zone-nom').innerText())
  await page.screenshot({ path: `${DOSSIER}/6-editeur.png` })
  await page.getByRole('button', { name: 'Terminer' }).first().click()
  await page.waitForTimeout(400)
  console.log('TABLE', JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('.plateau-emplacement-titre')].map((h) => h.textContent))))
  await page.screenshot({ path: `${DOSSIER}/7-table.png` })
}
console.log('ERREURS', JSON.stringify(erreurs))
await nav.close()
