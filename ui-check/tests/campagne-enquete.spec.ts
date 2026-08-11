// La grille de déduction d'« Agents of S.H.I.E.L.D. » : rayer les pistes mortes.
//
// Livret p.5 : « The campaign log contains a list of all possible combinations
// of means, motive, and opportunity, with each combination implicating one of
// the board members. By gathering evidence cards, the players narrow down the
// remaining possible combinations, one of which is secreted in the A.I.M.
// envelope. »
//
// Le raisonnement est à l'envers de l'intuition : une preuve qu'on TIENT est
// une preuve qui n'est PAS dans l'enveloppe A.I.M., donc toute combinaison qui
// la contient est morte. Se tromper de sens rayerait exactement le complément
// et désignerait le mauvais membre — d'où le premier test, qui compte.
//
// Les 27 combinaisons viennent du carnet imprimé et vivent dans le bloc
// `enquete` de `data/campagnes/aos.json`. Elles sont vérifiées ici sur un cas
// où la réponse se calcule à la main.
//
//   npx playwright test tests/campagne-enquete.spec.ts --project=pc
import { test, expect, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - enquete'

/** Écoute (moyen) et Voyages (occasion). */
const ECOUTE = '50186'
const VOYAGES = '50192'

let identifiant = ''

async function poser(request: APIRequestContext, preuves: string): Promise<string> {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        ...(identifiant ? { id: identifiant } : {}),
        code: 'aos',
        nom: NOM,
        difficulte: 'standard',
        equipe: [{ heros: 'maria_hill', nomHeros: 'Maria Hill' }],
        termines: ['black_widow'],
        carnet: preuves ? { 'Evidence Gained': preuves } : {},
        tentatives: {},
        partieEnCours: null,
      },
    },
  })
  expect(reponse.status()).toBe(200)
  return (await reponse.json()).id as string
}

async function ouvrirEnquete(page: import('@playwright/test').Page) {
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: NOM }).locator('.cmp-carte-ouvrir').click()
  await page.getByRole('button', { name: /enquête|investigation/i }).click()
  await expect(page.locator('.cmp-enq-bloc')).toHaveCount(3)
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

test.describe.serial("L'enquête", () => {
  test('Sans aucune preuve, les 27 combinaisons tiennent toutes', async ({ page, request }) => {
    identifiant = await poser(request, '')
    await ouvrirEnquete(page)

    await expect(page.locator('.cmp-enq-ligne')).toHaveCount(27)
    await expect(
      page.locator('.cmp-enq-ligne.eliminee'),
      'Une combinaison est rayée alors qu on n a aucune preuve.'
    ).toHaveCount(0)
    // Neuf par membre : c'est la répartition imprimée du carnet.
    for (let i = 0; i < 3; i++) {
      await expect(page.locator('.cmp-enq-bloc').nth(i).locator('.cmp-enq-ligne')).toHaveCount(9)
    }
    await expect(page.locator('.cmp-enq-carte.obtenue')).toHaveCount(0)
  })

  test('Chaque preuve obtenue raye les combinaisons qui la contiennent', async ({
    page,
    request,
  }) => {
    // Écoute et Voyages. Sur les 27 combinaisons, 9 contiennent Écoute, 9
    // contiennent Voyages, et 3 contiennent les deux : 15 rayées, 12 restent.
    await poser(request, `${ECOUTE};${VOYAGES}`)
    await ouvrirEnquete(page)

    await expect(page.locator('.cmp-enq-ligne.eliminee')).toHaveCount(15)
    await expect(page.locator('.cmp-enq-ligne:not(.eliminee)')).toHaveCount(12)

    // Aucune ligne survivante ne peut porter une preuve obtenue : ce serait le
    // raisonnement pris à l'envers.
    const survivantes = page.locator('.cmp-enq-ligne:not(.eliminee)')
    const textes = await survivantes.allInnerTexts()
    for (const texte of textes) {
      expect(texte, 'Une combinaison survivante contient une preuve déjà obtenue.').not.toMatch(
        /Écoute|Voyages|Wiretap|Travel/
      )
    }

    // Les deux cartes tenues sont mises en avant dans la légende, les sept
    // autres restent en retrait.
    await expect(page.locator('.cmp-enq-carte.obtenue')).toHaveCount(2)
    await expect(page.locator('.cmp-enq-carte')).toHaveCount(9)
  })

  test('Un membre sans combinaison restante est mis hors de cause', async ({ page, request }) => {
    // Dossiers médicaux + Argent + Habilitation. Les neuf combinaisons du
    // Médecin en chef contiennent chacune au moins une des trois : il est le
    // seul que ce lot disculpe entièrement. Il reste 8 combinaisons ailleurs,
    // donc l'écran ne doit pas encore crier victoire.
    await poser(request, '50185;50188;50191')
    await ouvrirEnquete(page)

    const medecin = page.locator('.cmp-enq-bloc', { hasText: /medecin|médecin/i })
    await expect(medecin.locator('.cmp-enq-ligne:not(.eliminee)')).toHaveCount(0)
    await expect(medecin).toHaveClass(/disculpe/)
    await expect(medecin.locator('.cmp-enq-compte')).toHaveText(/hors de cause|cleared/i)

    await expect(page.locator('.cmp-enq-ligne:not(.eliminee)')).toHaveCount(8)
    await expect(page.locator('.cmp-enq-bloc.disculpe')).toHaveCount(1)
  })

  test('Une seule combinaison restante : la taupe est démasquée', async ({ page, request }) => {
    // Six preuves sur neuf, soit l'enveloppe S.H.I.E.L.D. vidée : il ne reste
    // qu'une combinaison possible, celle de l'enveloppe A.I.M. Ici on garde
    // Dossiers (50185), Chantage (50189) et Autorité (50193) hors du lot.
    await poser(request, '50186;50187;50188;50190;50191;50192')
    await ouvrirEnquete(page)

    await expect(page.locator('.cmp-enq-ligne:not(.eliminee)')).toHaveCount(1)
    await expect(page.locator('.cmp-enq-bilan')).toContainText(/démasquée|unmasked/i)

    // Et c'est bien Dossiers · Chantage · Autorité, la combinaison restée dans
    // l'enveloppe, chez le membre que le carnet imprimé lui attribue.
    const restante = page.locator('.cmp-enq-ligne:not(.eliminee)')
    await expect(restante).toContainText('Dossiers')
    await expect(restante).toContainText('Chantage')
    await expect(restante).toContainText('Autorité')
    const bloc = page.locator('.cmp-enq-bloc', { has: restante })
    await expect(bloc.locator('.cmp-enq-membre')).toHaveText(/medecin|médecin|medical/i)
  })

  test("Le secret de la taupe n'arrive jamais au navigateur", async ({ request }) => {
    // La campagne est passée par /save_campagne, donc le serveur lui a tiré un
    // secret. Aucune des routes ne doit le rendre : l'écran affiche le carnet
    // en entier, le montrer ouvrirait l'enveloppe.
    const liste = (await (await request.get('/list_campagnes?')).json()) as Array<
      Record<string, unknown>
    >
    const mienne = liste.find((c) => c.id === identifiant)
    expect(mienne, 'La campagne témoin a disparu.').toBeTruthy()
    expect(JSON.stringify(mienne)).not.toContain('secret_aim')
    expect(JSON.stringify(mienne)).not.toContain('A.I.M. Envelope')
  })
})
