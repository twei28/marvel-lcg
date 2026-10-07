// UN DECK IMPORTÉ NE S'AFFICHE QU'UNE FOIS (signalement du 07/10/2026).
//
// Cause : un deck importé vit dans `deck/serveur-<place>/`. Le catalogue le
// listait (`catalog.decksForHero`, toutes les sources de `/list_deck`) ET
// l'assistant l'ajoutait une seconde fois (`decksSauvegardesPourHeros`) : deux
// entrées identiques, cliquables toutes les deux.
//
// Le test simule un deck importé en répondant à `/list_deck` et à
// `/get_hero_json` ; le reste vient du vrai moteur.
//
//   UI_CHECK_BASE=http://127.0.0.1:<port> WSLENV=UI_CHECK_BASE npx playwright test tests/decks-importes-une-fois.spec.ts --project=pc
import { expect, test } from '@playwright/test'

test.use({ viewport: { width: 1500, height: 950 } })

const NOM = 'mcdb-Cyclops_importe_test'

test('un deck importé apparaît une seule fois dans la liste des decks', async ({ page }) => {
  test.setTimeout(120_000)
  // Le vrai deck de départ de Cyclops, rebaptisé : un deck valide pour ce héros.
  const base = await (await page.request.get('/get_hero_json?cyclops')).json()
  const importe = { ...base, name: 'Cyclops importé (test)' }

  await page.route('**/list_deck?*', async (route) => {
    const reponse = await route.fetch()
    const chemins: string[] = await reponse.json()
    await route.fulfill({ response: reponse, json: [...chemins, `./deck/serveur-1/${NOM}.json`] })
  })
  await page.route(`**/get_hero_json?${NOM}`, (route) => route.fulfill({ json: importe }))

  await page.goto('/prepare.html')
  await page.waitForSelector('.acc-mode', { timeout: 20000 })
  await page.getByRole('button', { name: /^Solo/ }).first().click()
  await page.waitForSelector('#hero-grid .tb-port', { timeout: 20000 })
  await page.locator('#hero-grid .tb-port').filter({ hasText: /^Cyclops/i }).first().click()
  await page.waitForTimeout(800)
  const choisir = page.getByRole('button', { name: /Choisir ce h/i })
  if (await choisir.count()) await choisir.first().click()
  await page.waitForTimeout(800)
  const options = page.locator('.deck-modal')
  if (await options.count()) {
    const valider = options.getByRole('button', { name: /valider/i })
    if (await valider.count()) await valider.click()
  }
  await page.getByRole('button', { name: /continuer/i }).click()
  await page.waitForSelector('#deck-liste .tb-deck', { timeout: 20000 })
  await page.waitForTimeout(800)

  const noms = await page.evaluate(() =>
    [...document.querySelectorAll('#deck-liste .tb-deck .do-name')].map((e) => (e as HTMLElement).innerText.trim())
  )
  expect(noms.filter((n) => n.includes('importé (test)')), `liste : ${noms.slice(0, 6).join(' | ')}`).toHaveLength(1)
})
