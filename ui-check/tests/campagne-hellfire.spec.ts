// Hellfire Hunt dans l'ecran des campagnes, dans un VRAI navigateur : la boite et son livret, la creation de la campagne avec Sunspot,
// le scenario 1 jusqu'au plateau, puis le parcours de fin (victoire forcee) avec le carnet.
//
//   UI_CHECK_BASE=http://127.0.0.1:11060 npx playwright test tests/campagne-hellfire.spec.ts --project=pc
//
// ATTENTION : lance de VRAIES parties sur le serveur vise.
import { test, expect, type APIRequestContext } from '@playwright/test'
import { monde, repondre, sieges } from '../pilote-campagne'
import { parcoursOuvert, allerA, validerParcours } from './aide-parcours-fin'

const NOM = 'Essai automatique - hellfire'
const SORTIE = '/home/oem/Desktop/Marvel-LCG-campagnes/captures/hellfire-campagne'
let identifiant = ''

type Campagne = { id: string; nom?: string; code?: string; termines?: string[]; carnet?: Record<string, string>; equipe?: Array<{ nomHeros?: string }> }
const campagnes = async (request: APIRequestContext) => (await (await request.get('/list_campagnes?')).json()) as Campagne[]

test.beforeAll(async ({ request }) => {
  for (const c of await campagnes(request)) if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
})
test.afterAll(async ({ request }) => { if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } }) })

test.describe.serial('Hellfire Hunt : ecran des campagnes', () => {
  test.setTimeout(300000)

  test('la boite Hellfire Hunt : couverture, resume, regles et scenarios dans l ordre', async ({ page }) => {
    await page.goto('/campagne.html')
    await page.evaluate(() => localStorage.setItem('marvel-langue', 'fr'))
    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.getByRole('button', { name: /nouvelle campagne/i }).click()
    const boite = page.locator('.cmp-boite', { hasText: /hellfire/i }).first()
    await expect(boite, 'Hellfire Hunt absente de la liste des boites').toBeVisible()
    await boite.click()
    await page.waitForTimeout(800)
    await page.screenshot({ path: `${SORTIE}/01-boite.png` })
    // La couverture : le fond de la tuile pointe sur le scan.
    const fond = await boite.locator('.cmp-boite-illus').first().evaluate((e) => getComputedStyle(e).backgroundImage)
    console.log('FOND', fond)
    expect(fond).toContain('hellfire_hunt/00-couverture.jpg')
    await expect(page.getByText(/Cinq scénarios à gagner dans l'ordre/)).toBeVisible()
  })

  test('creation avec Sunspot, livret en double page, scenario 1 jusqu au plateau', async ({ page, request }) => {
    await page.addInitScript(() => localStorage.setItem('marvel-langue', 'fr'))
    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.getByRole('button', { name: /nouvelle campagne/i }).click()
    await page.locator('.cmp-boite', { hasText: /hellfire/i }).first().click()
    await page.locator('.cmp-saisie').fill(NOM)
    await page.getByRole('button', { name: /choisir l'équipe/i }).click()
    await expect(page.getByText('Campagne — ' + NOM)).toBeVisible({ timeout: 30000 })
    await page.getByRole('button', { name: /fan-made/i }).click()
    await page.getByPlaceholder(/Rechercher un héros/).fill('Sunspot')
    await page.waitForTimeout(800)
    await page.screenshot({ path: `${SORTIE}/02a-recherche-sunspot.png` })
    await page.getByRole('button', { name: /sunspot/i }).first().click()
    const modale = page.locator('.deck-modal')
    if (await modale.isVisible().catch(() => false)) await modale.getByRole('button', { name: /valider|confirm/i }).click()
    await page.getByRole('button', { name: /continuer/i }).click()
    await expect(page.locator('#deck-liste')).toBeVisible()
    await page.screenshot({ path: `${SORTIE}/02-equipe-decks.png` })
    await page.getByRole('button', { name: /valider l'équipe/i }).click()
    await expect(page.locator('.cmp-page-campagne')).toBeVisible()
    const creee = (await campagnes(request)).filter((c) => c.nom === NOM)
    expect(creee).toHaveLength(1)
    identifiant = creee[0].id
    expect(creee[0].code).toBe('hellfire_hunt')
    expect(creee[0].equipe?.[0]?.nomHeros).toMatch(/Sunspot/)

    // Le livre ouvert : couverture + premiere page (introduction), et les onglets.
    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
    await expect(page.locator('.cmp-livre-scene')).toBeVisible()
    await page.waitForTimeout(1000)
    const sources = () => page.locator('.cmp-livre-double img.cmp-page').evaluateAll((i) => i.map((x) => (x as HTMLImageElement).src.split('/').pop()))
    console.log('PAGES 1', JSON.stringify(await sources()))
    await page.screenshot({ path: `${SORTIE}/03-livre-debut.png` })
    await page.locator('.cmp-livre-fleche.droite').click(); await page.waitForTimeout(500)
    console.log('PAGES 2', JSON.stringify(await sources()))
    await page.screenshot({ path: `${SORTIE}/04-livre-suite.png` })
    await page.locator('.cmp-livre-onglet', { hasText: 'Règles de la campagne' }).click(); await page.waitForTimeout(500)
    await page.screenshot({ path: `${SORTIE}/05-regles-campagne.png` })
    await page.locator('.cmp-livre-onglet').first().click()
    await page.screenshot({ path: `${SORTIE}/06-ecran-complet.png`, fullPage: true })

    // Lancer le scenario 1 depuis l'ecran, jusqu'au plateau.
    await page.locator('.cmp-bloc-lancer .btn.launch').click()
    await page.waitForTimeout(6000); console.log('URL APRES LANCER', page.url()); await page.screenshot({ path: `${SORTIE}/06b-apres-lancer.png` })
    await page.waitForURL(/board\.html/, { timeout: 60000 })
    await page.waitForTimeout(2500)
    for (let i = 0; i < 60; i++) {
      for (const s of await sieges(request)) await repondre(request, s)
      const m = await monde(request)
      const phase = String(m.phase ?? '')
      if (phase && !phase.includes('Setup') && !phase.includes('Mulligan') && !phase.includes('Init')) break
      await page.waitForTimeout(400)
    }
    await page.waitForTimeout(1500)
    await page.screenshot({ path: `${SORTIE}/07-plateau-scenario1.png` })
    const m = await monde(request)
    const tout = JSON.stringify(m)
    expect(tout, 'Xavier\'s Institute (hf048) devait etre en jeu').toContain('hf048')
    expect(tout, 'Cerebro Insights (hf041) devait etre revelee').toContain('hf041')

    // Victoire forcee, puis le parcours de fin avec le carnet.
    for (let i = 0; i < 40; i++) {
      await request.get('/debug?' + encodeURIComponent('puzzle.PutIntoPlay("hf013", True)'))
      await request.get('/debug?' + encodeURIComponent('puzzle.Win()'))
      await repondre(request)
      if ((await monde(request)).game_over) break
      await page.waitForTimeout(500)
    }
    expect((await monde(request)).players_won, 'victoire attendue').toBe(true)
    await parcoursOuvert(page)
    await page.screenshot({ path: `${SORTIE}/08-parcours-victoire.png` })
    await allerA(page, 'bilan'); await page.waitForTimeout(500)
    await page.screenshot({ path: `${SORTIE}/09-parcours-bilan.png` })
    await allerA(page, 'carnet'); await page.waitForTimeout(500)
    await page.screenshot({ path: `${SORTIE}/10-parcours-carnet.png`, fullPage: true })
    const texte = await page.locator('.parcours-fin').innerText()
    console.log('CARNET TEXTE', texte.slice(0, 600))
    await validerParcours(page)
    await page.waitForURL(/\/campagne\.html/, { timeout: 30000 })
    await page.waitForTimeout(1000)
    await page.screenshot({ path: `${SORTIE}/11-apres-scenario1.png` })
    const apres = (await campagnes(request)).find((c) => c.id === identifiant)!
    console.log('CARNET ENREGISTRE', JSON.stringify(apres.carnet))
    expect(apres.termines).toContain('hellfire_white_queen')
    expect(apres.carnet?.['Recruited Allies'] ?? '').toContain('hf013')
  })
})
