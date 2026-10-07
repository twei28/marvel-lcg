// UN DECK QUE NOTRE CODE JUGE ILLÉGAL PEUT ÊTRE FORCÉ, ET FORCER NOUS L'ENVOIE.
//
// Nos règles de construction sont du code écrit à la main et peuvent se tromper
// (le refus de Cable du 22/09/2026) : une joueuse ne doit pas être bloquée par
// NOTRE erreur. Au collage d'un lien marvelcdb, un deck jugé illégal ouvre une
// fenêtre « d'après notre code… tu peux l'importer quand même ». OK importe et
// envoie un rapport (deck + raisons du refus) ; Annuler n'importe rien et
// n'envoie rien.
//
// Le deck marvelcdb et l'envoi du rapport sont simulés (`page.route`) : le test
// ne touche ni marvelcdb, ni le site, ni aucune partie. Il ne lance rien et peut
// tourner sur n'importe quel moteur.
//
//   UI_CHECK_BASE=http://127.0.0.1:<port> WSLENV=UI_CHECK_BASE npx playwright test tests/deck-illegal-force.spec.ts --project=pc
import { expect, test, type Page } from '@playwright/test'

test.use({ viewport: { width: 1500, height: 950 } })

// Quatre aspects à la fois : illégal pour tout héros qui n'est pas Spider-Woman.
const CARTES = ['01050', '01051', '01052', '01058', '01059', '01060', '01066', '01067', '01068', '01075', '01076', '01077']
const SLOTS = Object.fromEntries(CARTES.map((c) => [c, 3]))

async function jusquAuChampImport(page: Page) {
  await page.route('https://marvelcdb.com/api/public/**', (route) =>
    route.fulfill({
      json: { name: 'Quatre aspects (test)', hero_code: '01001a', slots: SLOTS, investigator_code: null },
    })
  )
  await page.goto('/prepare.html')
  await page.waitForSelector('.acc-mode', { timeout: 20000 })
  await page.getByRole('button', { name: /^Solo/ }).first().click()
  await page.waitForSelector('#hero-grid .tb-port', { timeout: 20000 })
  await page.locator('#hero-grid .tb-port').filter({ hasText: /^Spider-Man/ }).first().click()
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
}

async function collerEtImporter(page: Page) {
  await page.locator('input[id^="mcdb-"]').first().fill('9999999')
  await page.getByRole('button', { name: /^import$/i }).first().click()
  await page.waitForTimeout(1500)
}

test('forcer un deck jugé illégal l’importe ET envoie un rapport', async ({ page }) => {
  test.setTimeout(120_000)
  const rapports: Array<Record<string, string>> = []
  await page.route('**/post_rapport_bug', async (route) => {
    rapports.push(JSON.parse(route.request().postData() ?? '{}'))
    await route.fulfill({ json: { ok: true, numero: 1 } })
  })
  const dialogues: string[] = []
  page.on('dialog', async (d) => {
    dialogues.push(d.message())
    await d.accept()
  })
  await jusquAuChampImport(page)
  await collerEtImporter(page)

  expect(dialogues.length, 'aucune fenêtre ouverte').toBeGreaterThanOrEqual(1)
  expect(dialogues[0]).toMatch(/notre code/i)
  expect(dialogues[0]).toMatch(/Spider-Man/)
  expect(dialogues[0]).toMatch(/envoy/i)
  expect(rapports, 'le rapport automatique n’est pas parti').toHaveLength(1)
  expect(rapports[0]!.nom).toMatch(/forc/i)
  expect(rapports[0]!.description).toMatch(/Raisons du refus/)
  expect(rapports[0]!.description).toMatch(/Hulk/)
  // Et le deck est bien importé : la fenêtre « sauvegarder ? » suit.
  expect(dialogues.some((m) => /import/i.test(m) && /sauvegard/i.test(m))).toBe(true)
})

test('annuler n’importe rien et n’envoie rien', async ({ page }) => {
  test.setTimeout(120_000)
  const rapports: unknown[] = []
  await page.route('**/post_rapport_bug', async (route) => {
    rapports.push(route.request().postData())
    await route.fulfill({ json: { ok: true, numero: 1 } })
  })
  const dialogues: string[] = []
  page.on('dialog', async (d) => {
    dialogues.push(d.type() + ':' + d.message().slice(0, 40))
    await d.dismiss()
  })
  await jusquAuChampImport(page)
  await collerEtImporter(page)

  expect(dialogues.length, 'une seule fenêtre : la demande de forçage').toBe(1)
  expect(dialogues[0]).toMatch(/^confirm:/)
  expect(rapports, 'rien ne doit partir si la joueuse renonce').toHaveLength(0)
})
