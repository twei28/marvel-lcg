// Une campagne perdue ne se rejoue pas.
//
// Les six livrets portent la règle à la dernière page des instructions du
// scénario final (trors p.15, mts p.25, sm p.17, mut_gen p.19, next_evol p.18,
// aoa p.20). Le jeu l'affichait au joueur à la création de la campagne et ne
// l'appliquait nulle part : on pouvait perdre Magnéto en campagne experte et
// relancer le scénario comme si de rien n'était.
//
// La DÉCISION est éprouvée à part, sans navigateur, dans
// ui-app/src/board/campagne/defaite-campagne.test.ts — neuf cas, dont ceux qui
// ne doivent PAS perdre la campagne. Ce test-ci ne vérifie que l'écran : une
// campagne marquée perdue s'arrête, et elle seule.
//
//   npm run campagne-defaite
//
// Il n'ouvre aucune partie : la campagne est posée par l'API, et la défaite
// simulée par le drapeau que le plateau écrit en fin de partie.
import { test, expect, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - defaite'

/** Quatre scénarios gagnés, le cinquième en travers : l'état d'une fin de campagne. */
const QUATRE_GAGNES = ['sabretooth', 'project_wideawake', 'master_mold', 'mansion_attack']

const TEXTE_LIVRET = /Magnéto règne sur le monde/i

let identifiant = ''

async function poser(request: APIRequestContext, perdue: boolean): Promise<string> {
  const campagne = {
    ...(identifiant ? { id: identifiant } : {}),
    code: 'mut_gen',
    nom: NOM,
    difficulte: 'expert',
    equipe: [{ heros: 'colossus', nomHeros: 'Colossus', identite: ['32001a,32001b'], deck: {} }],
    termines: QUATRE_GAGNES,
    carnet: {},
    tentatives: { magneto: 2 },
    partieEnCours: null,
    ...(perdue ? { perdue: true } : {}),
  }
  const reponse = await request.post('/save_campagne', { data: { campagne } })
  expect(reponse.status(), "Le serveur a refusé la campagne d'essai.").toBe(200)
  return (await reponse.json()).id as string
}

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{
    id: string
    nom?: string
  }>
  for (const c of liste) {
    if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
  }
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test.describe.serial('Fin de campagne', () => {
  test('Tant que la campagne n est pas perdue, le dernier scénario se lance', async ({
    page,
    request,
  }) => {
    identifiant = await poser(request, false)

    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
    await expect(page.locator('.cmp-page-campagne')).toBeVisible()

    // Le témoin de ce test : sans lui, un écran cassé qui n'afficherait plus
    // aucun bouton passerait pour une campagne correctement arrêtée.
    await expect(page.getByRole('button', { name: /lancer le scénario/i })).toBeVisible()
    await expect(page.locator('.cmp-conclusion')).toHaveCount(0)
  })

  test('Perdue, elle s arrête : plus rien à lancer, et le livret a le dernier mot', async ({
    page,
    request,
  }) => {
    await poser(request, true)

    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()

    const conclusion = page.locator('.cmp-conclusion.perdue')
    await expect(conclusion, "La campagne perdue n'affiche pas sa fin.").toBeVisible()
    await expect(conclusion).toContainText(TEXTE_LIVRET)

    await expect(
      page.getByRole('button', { name: /lancer le scénario/i }),
      'Une campagne perdue propose encore de rejouer le scénario.'
    ).toHaveCount(0)
    await expect(
      page.getByRole('button', { name: /modifier les decks/i }),
      'Une campagne perdue propose encore de refaire les decks.'
    ).toHaveCount(0)

    // La progression reste lisible : on a perdu, on n'a pas tout effacé.
    await expect(conclusion).toContainText('4 / 5')
  })
})
