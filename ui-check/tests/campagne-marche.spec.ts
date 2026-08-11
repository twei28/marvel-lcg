// Le Marché de « Galaxy's Most Wanted » : dépenser ses unités entre deux scénarios.
//
// C'est la seule boîte du jeu où une MONNAIE traverse les scénarios. Le livret
// p.5 : « Choose a card with a Unit Cost value that is equal to or less than
// the number of units recorded in your Unspent Units box. Subtract that card's
// Unit Cost value... then add that card to your deck. Cards added to a player's
// deck this way must be included in that player's deck for the rest of the
// campaign. »
//
// Trois choses peuvent casser séparément, d'où trois cas : le prix lu sur la
// carte, la soustraction au carnet, et l'écriture qui survit à l'enregistrement.
// Le moteur, lui, remet ces cartes au deck à chaque mise en place ; c'est
// éprouvé à la sonde, pas ici.
//
//   npm run campagne-marche
import { test, expect, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - marche'
/** Brainstorm (16150) coûte 1 unité, Armor Plating (16162) en coûte 4. */
const PAS_CHERE = '16150'
const CHERE = '16162'

let identifiant = ''

async function poser(request: APIRequestContext, unites: number): Promise<string> {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        ...(identifiant ? { id: identifiant } : {}),
        code: 'gmw',
        nom: NOM,
        difficulte: 'standard',
        equipe: [{ heros: 'rocket_raccoon', nomHeros: 'Rocket Raccoon', identite: ['16021a,16021b'] }],
        termines: ['brotherhood_of_badoon'],
        carnet: { 'Player 1 Unspent Units': String(unites) },
        tentatives: {},
        partieEnCours: null,
      },
    },
  })
  expect(reponse.status()).toBe(200)
  return (await reponse.json()).id as string
}

const carnet = async (request: APIRequestContext) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<{
    id: string
    carnet?: Record<string, string>
  }>
  return liste.find((c) => c.id === identifiant)?.carnet ?? {}
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

test.describe.serial('Le Marché', () => {
  test('Avec 3 unités, on peut acheter à 1 et pas à 4', async ({ page, request }) => {
    identifiant = await poser(request, 3)

    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
    await page.getByRole('button', { name: /marché|market/i }).click()

    await expect(page.locator('.cmp-marche-solde strong')).toHaveText('3')

    const abordable = page.locator('.cmp-marche-carte').filter({ has: page.locator(`img[src*="${PAS_CHERE}"]`) })
    const trop = page.locator('.cmp-marche-carte').filter({ has: page.locator(`img[src*="${CHERE}"]`) })

    // Le prix est lu sur la carte elle-même, pas recopié à la main.
    await expect(abordable.locator('.cmp-marche-cout')).toHaveText('1')
    await expect(trop.locator('.cmp-marche-cout')).toHaveText('4')

    await expect(abordable, 'La carte à 1 unité est refusée alors qu on en a 3.').toBeEnabled()
    await expect(trop, 'La carte à 4 unités est achetable avec 3 unités.').toBeDisabled()
  })

  test('Acheter retire le prix du solde et inscrit la carte au carnet', async ({
    page,
    request,
  }) => {
    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
    await page.getByRole('button', { name: /marché|market/i }).click()

    const abordable = page.locator('.cmp-marche-carte').filter({ has: page.locator(`img[src*="${PAS_CHERE}"]`) })
    await abordable.click()

    await expect(page.locator('.cmp-marche-solde strong'), 'Le solde n a pas bougé.').toHaveText('2')
    await expect(abordable, 'La carte achetée reste proposée à l achat.').toBeDisabled()

    const apres = await carnet(request)
    expect(apres['Player 1 Unspent Units'], 'Le solde du carnet est faux.').toBe('2')
    expect(
      (apres['Player 1 Market Cards'] ?? '').split(';'),
      'La carte achetée n est pas inscrite au carnet.'
    ).toContain(PAS_CHERE)
  })

  test('Une carte déjà achetée ne se rachète pas, même avec les unités', async ({
    page,
    request,
  }) => {
    // On remet 9 unités : la carte reste hors de portée, non par son prix.
    await request.post('/save_campagne', {
      data: {
        campagne: {
          id: identifiant,
          code: 'gmw',
          nom: NOM,
          equipe: [{ heros: 'rocket_raccoon', nomHeros: 'Rocket Raccoon' }],
          carnet: { 'Player 1 Unspent Units': '9', 'Player 1 Market Cards': PAS_CHERE },
          termines: ['brotherhood_of_badoon'],
          partieEnCours: null,
        },
      },
    })

    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
    await page.getByRole('button', { name: /marché|market/i }).click()

    const deja = page.locator('.cmp-marche-carte').filter({ has: page.locator(`img[src*="${PAS_CHERE}"]`) })
    await expect(deja).toBeDisabled()
    await expect(deja).toHaveClass(/achetee/)
    // Et le témoin : avec 9 unités, la carte à 4 est bien redevenue achetable.
    await expect(
      page.locator('.cmp-marche-carte').filter({ has: page.locator(`img[src*="${CHERE}"]`) })
    ).toBeEnabled()
  })
})
