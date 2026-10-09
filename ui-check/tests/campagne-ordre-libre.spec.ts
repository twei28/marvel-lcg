// La campagne « Fear No Evil » se joue en ordre libre (livret mc60 p. 8-9) :
// avant chaque partie, deux affaires non résolues progressent au hasard ; à
// trois marques une affaire est Failed ; le vilain suit l'ordre recommandé au
// premier parcours ; une défaite en campagne experte fait progresser l'affaire
// perdue ; Kingpin n'est proposé que lorsque les cinq affaires sont résolues.
//
// Les règles pures sont éprouvées par tools/tests-lanceur/ordre-libre.test.mjs.
// Ici on vérifie que l'ÉCRAN les applique et les enregistre au carnet.
//
//   UI_CHECK_BASE=http://127.0.0.1:40000 WSLENV=UI_CHECK_BASE npx playwright test tests/campagne-ordre-libre.spec.ts --project=pc
import { test, expect, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - ordre libre'
let identifiant = ''

type Carnet = Record<string, string>

async function poser(
  request: APIRequestContext,
  extra: { carnet?: Carnet; difficulte?: string; partieEnCours?: unknown; termines?: string[] } = {},
): Promise<string> {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        ...(identifiant ? { id: identifiant } : {}),
        code: 'fne',
        nom: NOM,
        difficulte: extra.difficulte ?? 'standard',
        equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'] }],
        termines: extra.termines ?? [],
        carnet: extra.carnet ?? {},
        tentatives: {},
        partieEnCours: extra.partieEnCours ?? null,
        tirage: null,
      },
    },
  })
  expect(reponse.status()).toBe(200)
  return (await reponse.json()).id as string
}

async function lire(request: APIRequestContext) {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{
    id: string
    carnet?: Carnet
    perdue?: boolean
    partieEnCours?: unknown
    tirage?: { tirees: string[]; echouees: string[] } | null
  }>
  return liste.find((c) => c.id === identifiant)!
}

async function ouvrir(page: import('@playwright/test').Page) {
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
  await expect(page.locator('.cmp-affaires')).toBeVisible()
}

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{ id: string; nom?: string }>
  for (const c of liste) {
    if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
  }
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test.describe.serial('Fear No Evil en ordre libre', () => {
  test('les planches du livret sont là : ouverture, règles de campagne, puis BD et règles de l\'affaire choisie', async ({ page, request }) => {
    identifiant = await poser(request)
    await ouvrir(page)

    // Livre ouvert (09/10/2026) : la planche d'ouverture dans l'onglet du
    // livret, les trois pages de regles dans l'onglet de la campagne.
    const planche = (fichier: string) => page.locator(`img.cmp-page[src*="${fichier}"]`)
    const onglet = (nom: RegExp) => page.locator('.cmp-livre-onglet', { hasText: nom })
    await expect(planche('00-campagne-intro-1.jpg'), 'la planche d ouverture manque').toBeVisible()
    await onglet(/Règles de la campagne|Campaign rules/).click()
    await expect(planche('00-campagne-regles-1.jpg')).toBeVisible()
    await page.keyboard.press('ArrowRight')
    await expect(planche('00-campagne-regles-3.jpg')).toBeVisible()

    // Tant qu'aucune affaire n'est retenue, le livret n'a que la planche d'ouverture.
    await onglet(/Le livret|The rulebook/).click()
    await expect(page.locator('.cmp-livre-compteur')).toHaveText('1 / 1')

    await page.getByRole('button', { name: /tirer la progression|draw the progression/i }).click()
    await page.getByRole('button', { name: /^The Getaway|^La fuite/ }).click()

    // La BD et la page de règles de l'affaire retenue, et les portraits.
    await expect(planche('02-the_getaway-intro-1.jpg'), 'la BD de l affaire manque').toBeVisible()
    await page.keyboard.press('ArrowRight')
    await expect(planche('02-the_getaway-regles-1.jpg'), 'la page de règles de l affaire manque').toBeVisible()
    await page.keyboard.press('ArrowLeft')
    await expect(page.locator('details.cmp-vilains')).toBeVisible()

    // Une planche qui n'existe pas se retire d'elle-même (pageLivret.onerror) :
    // ce que le test mesure, c'est qu'elles se chargent VRAIMENT.
    const chargee = await planche('02-the_getaway-intro-1.jpg').evaluate(
      (img) => (img as HTMLImageElement).naturalWidth
    )
    expect(chargee, 'la planche est dans le DOM mais son image ne se charge pas').toBeGreaterThan(100)
  })

  test('Le tirage fait progresser deux affaires et le carnet le garde', async ({ page, request }) => {
    identifiant = await poser(request)
    await ouvrir(page)

    await expect(page.locator('.cmp-affaire.ouverte, .cmp-affaire.completed, .cmp-affaire.failed')).toHaveCount(5)
    await expect(page.locator('.cmp-affaire.fermee'), 'Kingpin est proposé avant que les affaires soient résolues.').toHaveCount(1)
    await expect(page.locator('.cmp-affaire-case.cochee')).toHaveCount(0)

    await page.getByRole('button', { name: /tirer la progression|draw the progression/i }).click()

    await expect(page.locator('.cmp-affaire.tiree'), 'Deux affaires doivent avoir été tirées.').toHaveCount(2)
    await expect(page.locator('.cmp-affaire-case.cochee')).toHaveCount(2)

    const c = await lire(request)
    expect(c.tirage?.tirees.length, 'Le tirage n est pas enregistré.').toBe(2)
    const marques = Object.entries(c.carnet ?? {}).filter(([k, v]) => k.startsWith('Progress: ') && v === '1')
    expect(marques.length, 'Le carnet ne porte pas deux marques.').toBe(2)
  })

  test('Choisir une affaire propose Hammerhead en premier et inscrit le vilain retenu', async ({ page }) => {
    await ouvrir(page)
    await expect(page.getByRole('button', { name: /tirer la progression|draw the progression/i }), 'Un rechargement ne doit pas retirer.').toHaveCount(0)

    await page.getByRole('button', { name: /^The Getaway|^La fuite/ }).click()
    const recommande = page.locator('.cmp-mission button.launch', { hasText: /recommand/ })
    await expect(recommande).toHaveText(/Hammerhead/)
    await expect(page.locator('.cmp-mission button', { hasText: /Lancer le scénario|Start the scenario/ })).toHaveText(/Hammerhead/)

    // Le joueur préfère Bullseye : le bouton de lancement le suit.
    await page.locator('.cmp-mission button', { hasText: /^Bullseye/ }).click()
    await expect(page.locator('.cmp-mission button', { hasText: /Lancer le scénario|Start the scenario/ })).toHaveText(/Bullseye/)
  })

  test('En campagne experte, déclarer la partie perdue fait progresser l affaire ; à trois marques elle est Failed', async ({ page, request }) => {
    await poser(request, {
      difficulte: 'expert',
      carnet: { 'Progress: the_getaway': '2', 'Villain: the_getaway': 'bullseye' },
      partieEnCours: { scenario: 'the_getaway', vilain: 'bullseye', depuis: new Date().toISOString() },
    })
    await ouvrir(page)
    await expect(page.locator('.cmp-mission .cmp-bloc-t').first()).toHaveText(/Getaway|fuite/)
    await expect(page.locator('.cmp-mission .cmp-bloc-t').first()).toHaveText(/Bullseye/)

    page.once('dialog', (d) => d.accept())
    await page.getByRole('button', { name: /la partie est perdue|the game was lost/i }).click()

    await expect(page.locator('.cmp-affaire.failed')).toHaveCount(1)
    await expect(page.locator('.cmp-affaire.failed .cmp-affaire-case.cochee')).toHaveCount(3)
    const c = await lire(request)
    expect(c.carnet?.['Progress: the_getaway']).toBe('3')
    expect((c.carnet?.['Failed Scenarios'] ?? '').split(';')).toContain('the_getaway')
    expect(c.partieEnCours, 'La partie perdue reste marquée en cours.').toBeFalsy()
  })

  test('Kingpin n est proposé que lorsque tout est résolu, et sa défaite experte retourne un environnement', async ({ page, request }) => {
    await poser(request, {
      difficulte: 'expert',
      carnet: {
        'Completed Scenarios': 'art_museum_heist;protection_racket',
        'Failed Scenarios': 'the_getaway;the_raft_breakout;stop_the_presses',
      },
    })
    await ouvrir(page)
    await expect(page.locator('.cmp-affaire.completed')).toHaveCount(2)
    await expect(page.locator('.cmp-affaire.failed')).toHaveCount(3)
    await expect(page.locator('.cmp-affaire.fermee')).toHaveCount(0)

    await page.getByRole('button', { name: /préparer la partie finale|prepare the final game/i }).click()
    await expect(page.locator('.cmp-affaire-case.cochee'), 'Rien ne doit progresser quand tout est résolu.').toHaveCount(0)
    await expect(page.locator('.cmp-mission .cmp-bloc-t').first()).toHaveText(/Kingpin|Caïd/)

    // Une défaite contre Kingpin en expert : on choisit l'environnement à retourner.
    await poser(request, {
      difficulte: 'expert',
      carnet: {
        'Completed Scenarios': 'art_museum_heist;protection_racket',
        'Failed Scenarios': 'the_getaway;the_raft_breakout;stop_the_presses',
      },
      partieEnCours: { scenario: 'kingpin', depuis: new Date().toISOString() },
    })
    await ouvrir(page)
    page.once('dialog', (d) => d.accept())
    await page.getByRole('button', { name: /la partie est perdue|the game was lost/i }).click()
    await page.locator('.cmp-mission button', { hasText: /Protection Racket|Le racket/ }).click()

    await expect(page.locator('.cmp-affaire.completed')).toHaveCount(1)
    await expect(page.locator('.cmp-affaire.failed')).toHaveCount(4)
    const c = await lire(request)
    expect(c.carnet?.['Completed Scenarios']).toBe('art_museum_heist')
    expect(c.perdue, 'Il restait un environnement Completed : la campagne continue.').toBeFalsy()

    // Plus aucun environnement Completed : la campagne est perdue.
    await poser(request, {
      difficulte: 'expert',
      carnet: { 'Failed Scenarios': 'art_museum_heist;protection_racket;the_getaway;the_raft_breakout;stop_the_presses' },
      partieEnCours: { scenario: 'kingpin', depuis: new Date().toISOString() },
    })
    await ouvrir(page)
    page.once('dialog', (d) => d.accept())
    await page.getByRole('button', { name: /la partie est perdue|the game was lost/i }).click()
    await expect(page.locator('.cmp-conclusion.perdue')).toBeVisible()
    expect((await lire(request)).perdue).toBe(true)
  })
})
