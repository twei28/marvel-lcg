// L'ecran de campagne en « livre ouvert » (decide le 09/10/2026, fiche
// .planning/todos/2026-10-09-ecran-campagne-livre-ouvert.md) : les pages du
// livret en double page, tournees par fleches ou clavier, et le bouton Lancer
// visible SANS defiler sur un ecran de PC.
//
//   UI_CHECK_BASE=http://127.0.0.1:2330 WSLENV=UI_CHECK_BASE \
//     npx playwright test tests/campagne-livre-ouvert.spec.ts --project=pc
import { test, expect, type APIRequestContext, type Page } from '@playwright/test'

const PREFIXE = 'Essai livre ouvert'
const AOS = ['black_widow', 'batroc', 'modok', 'thunderbolts', 'baron_zemo']
const ids: string[] = []

async function poser(request: APIRequestContext, nom: string, code: string, termines: string[]) {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        code, nom, difficulte: 'standard',
        equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'] }],
        termines, carnet: {}, tentatives: {}, partieEnCours: null,
      },
    },
  })
  expect(reponse.status()).toBe(200)
  ids.push((await reponse.json()).id as string)
}

async function ouvrir(page: Page, nom: string) {
  await page.goto('/campagne.html')
  await page.evaluate(() => localStorage.setItem('marvel-langue', 'fr'))
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: nom }).locator('.cmp-carte-ouvrir').click()
  await expect(page.locator('.cmp-livre-scene')).toBeVisible()
  await page.waitForTimeout(800)
}

const sources = (page: Page) => page.locator('.cmp-livre-double img.cmp-page').evaluateAll(
  (imgs) => imgs.map((i) => (i as HTMLImageElement).src.split('/').pop()))

/** Le bouton Lancer tient dans la fenetre, et la page ne defile pas. */
async function sansDefiler(page: Page) {
  const mesure = await page.evaluate(() => {
    const b = document.querySelector('.cmp-bloc-lancer .btn.launch')!.getBoundingClientRect()
    return { bas: b.bottom, haut: innerHeight, defile: document.documentElement.scrollHeight - innerHeight }
  })
  console.log('MESURE', JSON.stringify(mesure))
  expect(mesure.bas, 'bouton Lancer sous le bord de la fenetre').toBeLessThanOrEqual(mesure.haut)
  expect(mesure.defile, 'la page defile').toBeLessThanOrEqual(1)
}

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{ id: string; nom?: string }>
  for (const c of liste) if ((c.nom || '').startsWith(PREFIXE)) await request.post('/delete_campagne', { data: { id: c.id } })
  await poser(request, PREFIXE + ' debut', 'hunting_season', [])
  await poser(request, PREFIXE + ' entre', 'aos', [AOS[0]])
  await poser(request, PREFIXE + ' fin', 'aos', AOS)
})

test.afterAll(async ({ request }) => {
  for (const id of ids) await request.post('/delete_campagne', { data: { id } })
})

for (const [largeur, hauteur] of [[1366, 768], [1920, 1080]]) {
  test(`debut de campagne en ${largeur}x${hauteur} : double page, fleches, clavier, Lancer visible`, async ({ page }) => {
    await page.setViewportSize({ width: largeur, height: hauteur })
    await ouvrir(page, PREFIXE + ' debut')
    expect(await sources(page)).toEqual(['00-couverture.jpg', '00-campagne-regles-1.jpg'])
    await expect(page.locator('.cmp-livre-compteur')).toHaveText('1-2 / 4')
    await sansDefiler(page)
    await page.screenshot({ path: `test-results/livre-debut-${largeur}.png` })

    await page.locator('.cmp-livre-fleche.droite').click()
    await expect(page.locator('.cmp-livre-compteur')).toHaveText('3-4 / 4')
    await page.waitForTimeout(150)
    await page.screenshot({ path: `test-results/livre-tourne-${largeur}.png` })
    expect(await sources(page)).toEqual(['00-campagne-regles-2.jpg', '01-hs_vermin-regles-1.jpg'])
    await expect(page.locator('.cmp-livre-fleche.droite')).toBeDisabled()
    await page.keyboard.press('ArrowLeft')
    await expect(page.locator('.cmp-livre-compteur')).toHaveText('1-2 / 4')
    await page.keyboard.press('ArrowRight')
    await expect(page.locator('.cmp-livre-compteur')).toHaveText('3-4 / 4')

    await page.locator('.cmp-livre-onglet', { hasText: 'Règles de la campagne' }).click()
    await expect(page.locator('.cmp-livre-compteur')).toHaveText('1-2 / 2')

    // La loupe reste : clic sur une page, Echap la ferme.
    await page.locator('.cmp-livre-double img.cmp-page').first().click()
    await expect(page.locator('.cmp-loupe')).toBeVisible()
    await page.keyboard.press('Escape')
    await expect(page.locator('.cmp-loupe')).toHaveCount(0)
  })
}

test('entre deux scenarios : epilogue du precedent puis le suivant', async ({ page }) => {
  await page.setViewportSize({ width: 1366, height: 768 })
  await ouvrir(page, PREFIXE + ' entre')
  expect(await sources(page)).toEqual(['01-black_widow-epilogue-1.jpg', '02-batroc-regles-1.jpg'])
  await sansDefiler(page)
  await page.screenshot({ path: 'test-results/livre-entre.png' })
})

test('fin de campagne : epilogue final dans le livre', async ({ page }) => {
  await page.setViewportSize({ width: 1366, height: 768 })
  await ouvrir(page, PREFIXE + ' fin')
  const epilogue = await sources(page)
  expect(epilogue.length).toBeGreaterThan(0)
  expect(epilogue.every((f) => /^05-.*epilogue/.test(f || ''))).toBe(true)
  await page.screenshot({ path: 'test-results/livre-fin.png' })
})

test('ecran etroit : une page a la fois, balayage du doigt', async ({ browser }) => {
  const contexte = await browser.newContext({ viewport: { width: 412, height: 915 }, hasTouch: true, isMobile: true })
  const page = await contexte.newPage()
  await ouvrir(page, PREFIXE + ' debut')
  expect(await sources(page)).toEqual(['00-couverture.jpg'])
  await expect(page.locator('.cmp-livre-compteur')).toHaveText('1 / 4')
  const scene = await page.locator('.cmp-livre-scene').boundingBox()
  const y = scene!.y + scene!.height / 2
  await page.evaluate(([x0, x1, yy]) => {
    const s = document.querySelector('.cmp-livre-scene')!
    const ev = (type: string, x: number) => s.dispatchEvent(new PointerEvent(type, { clientX: x, clientY: yy, pointerType: 'touch', bubbles: true }))
    ev('pointerdown', x0); ev('pointerup', x1)
  }, [scene!.x + scene!.width * 0.8, scene!.x + scene!.width * 0.2, y])
  await expect(page.locator('.cmp-livre-compteur')).toHaveText('2 / 4')
  expect(await sources(page)).toEqual(['00-campagne-regles-1.jpg'])
  await page.waitForTimeout(600)
  await page.screenshot({ path: 'test-results/livre-mobile.png' })
  await contexte.close()
})
