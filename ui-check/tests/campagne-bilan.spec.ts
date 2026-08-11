// Le score final que le livret fait noter APRES la campagne.
//
// Sinister Motives, p.5 et p.17 (encart VICTORY du scenario 5, sous
// « Optional ») : « Using the "Conditions" section of the reputation track,
// calculate your group's total reputation value, then mark that number of nodes.
// In the "Final Reputation Score" section of the campaign log, record a value
// equal to the number of nodes marked. The higher this score, the better you
// did! »
//
// C'etait la derniere case du carnet officiel de sm que le jeu ne demandait
// jamais. Sa place est le BILAN de fin de campagne et non le carnet : aucune
// mise en place ne le relit, et l'y mettre aurait exige une cle que le moteur ne
// connait pas — `verifier_campagnes.py` la refuserait, a juste titre.
//
// Le bloc est declare par les DONNEES (`bilan` dans data/campagnes/sm.json) :
// aucune autre boite ne l'affiche, et c'est ce que tient le dernier cas.
//
//   npm run campagne-bilan
//
// ATTENTION : ce test cree des campagnes sur le serveur puis les supprime. Il ne
// lance aucune partie.
import { test, expect, type Page, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - bilan'
const NOM_AUTRE = 'Essai automatique - bilan (autre boite)'

/** La piste cumulee deja au carnet, comme si quatre scenarios l'avaient nourrie. */
const PISTE = 14
/** Le dernier calcul des Conditions, saisi au bilan. */
const DERNIER = 5

type Campagne = {
  id: string
  nom?: string
  code?: string
  carnet?: Record<string, string>
  termines?: string[]
  scoreFinal?: number
}

const SCENARIOS_SM = ['sandman', 'venom', 'mysterio', 'sinister_six', 'venom_goblin']

async function campagnes(request: APIRequestContext): Promise<Campagne[]> {
  return (await request.get('/list_campagnes?')).json()
}

/** Pose une campagne TERMINEE, sans passer par une partie : le bilan seul est teste. */
async function poser(
  request: APIRequestContext,
  nom: string,
  code: string,
  termines: string[],
  carnet: Record<string, string>
): Promise<string> {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        code,
        nom,
        difficulte: 'standard',
        equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a'], deck: {} }],
        termines,
        carnet,
        tentatives: {},
        partieEnCours: null,
      },
    },
  })
  expect(reponse.status()).toBe(200)
  return (await reponse.json()).id as string
}

async function ouvrir(page: Page, nom: string) {
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  const carte = page.locator('.cmp-carte', { hasText: nom })
  await expect(carte, `La campagne « ${nom} » n'apparait pas dans la liste.`).toHaveCount(1)
  await carte.locator('.cmp-carte-ouvrir').click()
  await expect(page.locator('.cmp-conclusion')).toBeVisible()
}

test.beforeAll(async ({ request }) => {
  for (const c of await campagnes(request)) {
    if (c.nom === NOM || c.nom === NOM_AUTRE) {
      await request.post('/delete_campagne', { data: { id: c.id } })
    }
  }
})

test.describe.serial('Campagne : le score de reputation final', () => {
  let identifiant = ''
  let autre = ''

  test.afterAll(async ({ request }) => {
    for (const id of [identifiant, autre]) {
      if (id) await request.post('/delete_campagne', { data: { id } })
    }
  })

  test('Le bilan propose le score, l enregistre, et l ajoute a la piste', async ({
    page,
    request,
  }) => {
    identifiant = await poser(request, NOM, 'sm', SCENARIOS_SM, {
      'Reputation Track': String(PISTE),
    })

    await ouvrir(page, NOM)

    const bloc = page.locator('.cmp-bilan-score')
    await expect(bloc, "Le bloc du score final ne s'affiche pas sur une campagne gagnee.").toBeVisible()
    // La piste deja cumulee doit etre RAPPELEE : sans elle, le joueur ne sait pas
    // a quoi son dernier calcul s'ajoute, et croirait devoir ressaisir le total.
    await expect(bloc.locator('.cmp-bilan-score-base')).toContainText(String(PISTE))

    await bloc.locator('.cmp-saisie-score').fill(String(DERNIER))
    await bloc.getByRole('button', { name: /enregistrer le score/i }).click()

    // Affiche le total, pas le dernier calcul : c'est le nombre de noeuds marques.
    await expect(bloc.locator('.cmp-bilan-score-v')).toHaveText(String(PISTE + DERNIER))
    await expect(bloc.locator('.cmp-saisie-score')).toHaveCount(0)

    const enregistree = (await campagnes(request)).find((c) => c.id === identifiant)
    expect(enregistree?.scoreFinal, 'Le score n a pas ete ecrit sur le serveur.').toBe(
      PISTE + DERNIER
    )
  })

  test('Le score enregistre survit au rechargement', async ({ page }) => {
    await ouvrir(page, NOM)
    await expect(page.locator('.cmp-bilan-score-v')).toHaveText(String(PISTE + DERNIER))
    await expect(
      page.locator('.cmp-saisie-score'),
      'Le bilan redemande un score deja enregistre.'
    ).toHaveCount(0)
  })

  test('Une boite sans bloc bilan n affiche aucun score', async ({ page, request }) => {
    // Temoin : le bloc vient des DONNEES. Rise of Red Skull n'en declare pas, et
    // ne doit donc rien montrer — un affichage en dur passerait le test precedent
    // tout en inventant une case de carnet que ce livret n'a pas.
    autre = await poser(
      request,
      NOM_AUTRE,
      'trors',
      ['crossbones', 'absorbing_man', 'taskmaster', 'zola', 'red_skull'],
      {}
    )
    await ouvrir(page, NOM_AUTRE)
    await expect(page.locator('.cmp-bilan')).toBeVisible()
    await expect(page.locator('.cmp-bilan-score')).toHaveCount(0)
  })
})
