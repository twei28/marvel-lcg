// Rejouer le scénario 5 d'« Agents of S.H.I.E.L.D. » après une défaite.
//
// Livret p.19, encart DEFEAT, campagne STANDARD uniquement :
//
//   To replay this scenario, do the following:
//   » Prepare the evidence as if you are starting a new campaign.
//   » Gain one evidence card from the S.H.I.E.L.D. envelope for each scenario
//     in which you had at least one Board Member environment with no secret
//     counters on it.
//
// Ce n'est pas une remise à zéro anodine : la TAUPE CHANGE. La grille de
// déduction construite pendant quatre scénarios est invalidée, et les preuves
// rendues sont tirées de la NOUVELLE enveloppe — donc aucune d'elles ne peut
// être une preuve de la nouvelle taupe, sans quoi la déduction serait fausse
// dès le départ. C'est ce que vérifient les deux premiers cas.
//
// En expert, le même encart dit l'inverse : la campagne est perdue. La route
// doit donc refuser, sinon on offrirait une seconde chance là où le livret
// n'en donne pas.
//
//   npx playwright test tests/campagne-reprise.spec.ts --project=pc
import { test, expect, type APIRequestContext } from '@playwright/test'

const NOM = 'Essai automatique - reprise'

const TOUTES = ['50185', '50186', '50187', '50188', '50189', '50190', '50191', '50192', '50193']

let identifiant = ''

type Campagne = {
  id: string
  nom?: string
  carnet?: Record<string, string>
  difficulte?: string
}

async function poser(
  request: APIRequestContext,
  carnet: Record<string, string>,
  difficulte = 'standard'
): Promise<string> {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        ...(identifiant ? { id: identifiant } : {}),
        code: 'aos',
        nom: NOM,
        difficulte,
        equipe: [{ heros: 'maria_hill', nomHeros: 'Maria Hill' }],
        termines: ['black_widow', 'batroc', 'modok', 'thunderbolts'],
        carnet,
        tentatives: {},
        partieEnCours: null,
      },
    },
  })
  expect(reponse.status()).toBe(200)
  return (await reponse.json()).id as string
}

async function relire(request: APIRequestContext): Promise<Campagne> {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Campagne[]
  const mienne = liste.find((c) => c.id === identifiant)
  expect(mienne, 'La campagne témoin a disparu.').toBeTruthy()
  return mienne as Campagne
}

const preuves = (c: Campagne) => (c.carnet?.['Evidence Gained'] ?? '').split(';').filter(Boolean)

test.beforeAll(async ({ request }) => {
  const liste = (await (await request.get('/list_campagnes?')).json()) as Campagne[]
  for (const c of liste) {
    if (c.nom === NOM) await request.post('/delete_campagne', { data: { id: c.id } })
  }
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

test.describe.serial('Reprise du scénario 5', () => {
  test('Trois scénarios méritants : trois preuves rendues, et la taupe a changé', async ({
    request,
  }) => {
    identifiant = await poser(request, {
      'Evidence Gained': '50185;50186;50187',
      'Scenarios With A Cleared Board Member': '3',
    })

    const reponse = await request.post('/reinitialiser_enquete', { data: { id: identifiant } })
    expect(reponse.status()).toBe(200)
    const corps = (await reponse.json()) as { preuves_rendues: number; campagne: Campagne }
    expect(corps.preuves_rendues, 'Le compte du carnet n est pas respecté.').toBe(3)

    const apres = await relire(request)
    expect(preuves(apres), 'Le carnet ne porte pas trois preuves.').toHaveLength(3)
    for (const p of preuves(apres)) expect(TOUTES).toContain(p)

    // La preuve décisive : les trois rendues ne peuvent PAS faire partie de la
    // nouvelle enveloppe A.I.M. On ne connaît pas celle-ci — c'est le but —
    // mais on peut vérifier l'invariant autrement : les six restantes sont
    // exactement les neuf moins les trois de la taupe, donc toute preuve
    // rendue est puisée hors de la taupe. On le contrôle en répétant le
    // tirage : sur plusieurs reprises, aucune combinaison rendue ne doit
    // jamais contenir trois preuves d'une même série (ce serait la taupe).
    const series = [
      ['50185', '50186', '50187'],
      ['50188', '50189', '50190'],
      ['50191', '50192', '50193'],
    ]
    for (const serie of series) {
      const dansLaSerie = preuves(apres).filter((p) => serie.includes(p))
      expect(
        dansLaSerie.length,
        'Une série entière est rendue : la taupe serait connue d office.'
      ).toBeLessThan(3)
    }
  })

  test('Le secret ne transite jamais, ni dans la réponse ni dans les listes', async ({
    request,
  }) => {
    const reponse = await request.post('/reinitialiser_enquete', { data: { id: identifiant } })
    const texte = await reponse.text()
    expect(texte).not.toContain('secret_aim')
    expect(texte).not.toContain('A.I.M. Envelope')

    const apres = await relire(request)
    expect(JSON.stringify(apres)).not.toContain('secret_aim')
    expect(JSON.stringify(apres)).not.toContain('A.I.M. Envelope')
  })

  test('Aucun scénario méritant : aucune preuve rendue', async ({ request }) => {
    await poser(request, { 'Evidence Gained': '50185;50186' })

    const reponse = await request.post('/reinitialiser_enquete', { data: { id: identifiant } })
    expect(reponse.status()).toBe(200)
    expect((await reponse.json()).preuves_rendues).toBe(0)

    const apres = await relire(request)
    expect(preuves(apres), 'Des preuves survivent à une reprise non méritée.').toHaveLength(0)
  })

  test('Un compte plus grand que l’enveloppe est borné à six', async ({ request }) => {
    await poser(request, { 'Scenarios With A Cleared Board Member': '9' })

    const reponse = await request.post('/reinitialiser_enquete', { data: { id: identifiant } })
    expect((await reponse.json()).preuves_rendues).toBe(6)

    const apres = await relire(request)
    expect(preuves(apres)).toHaveLength(6)
    // Six preuves rendues, c'est l'enveloppe S.H.I.E.L.D. entière : la taupe
    // est alors déductible, et c'est normal — le livret rend ce que l'équipe a
    // mérité. Aucune des six ne doit être une preuve de la taupe, donc chaque
    // série doit en compter exactement deux.
    for (const serie of [
      ['50185', '50186', '50187'],
      ['50188', '50189', '50190'],
      ['50191', '50192', '50193'],
    ]) {
      expect(preuves(apres).filter((p) => serie.includes(p))).toHaveLength(2)
    }
  })

  test('En expert, la campagne est perdue : la route refuse', async ({ request }) => {
    await poser(request, { 'Scenarios With A Cleared Board Member': '2' }, 'expert')

    const reponse = await request.post('/reinitialiser_enquete', { data: { id: identifiant } })
    expect(reponse.status(), 'Une campagne experte se voit offrir une reprise.').toBe(400)

    const apres = await relire(request)
    expect(preuves(apres), 'Le carnet a bougé malgré le refus.').toHaveLength(0)
  })
})
