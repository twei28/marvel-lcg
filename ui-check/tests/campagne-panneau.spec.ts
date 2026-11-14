// Le panneau de récompenses, de bout en bout.
//
// C'est le point de passage OBLIGÉ de toutes les campagnes : rien n'entre dans
// un carnet sans lui. Et jusqu'ici, aucun test ne le traversait — seules ses
// briques pures étaient éprouvées (`preremplissage`, `detecteurs`,
// `defaite-campagne`, `reprise-campagne`). Trois câblages en dépendaient sans
// preuve : qu'il s'ouvre au bon moment, qu'il enregistre ce qu'il affiche, et
// qu'il appelle `/reinitialiser_enquete` à la défaite du scénario 5 d'aos.
//
// COMMENT UNE VRAIE PARTIE EST MENÉE ICI
//
// Le plateau doit être ouvert : le moteur attend un client avant de poser sa
// première question, et c'est lui qui affiche le panneau. Mais répondre à ses
// questions EN CLIQUANT serait fragile — la mise en place de Black Widow demande
// déjà de choisir un sbire parmi dix. On ouvre donc le plateau, et on répond par
// `/get_ask` + `/post`, exactement comme le fait le navigateur, en prenant la
// première option légale : c'est le même pilote que `tools/sonde_campagne.py`.
// La fin de partie est ensuite forcée par `/debug`, la console que le joueur a
// sous la main.
//
// ATTENTION : ce test lance de VRAIES parties. Toute partie en cours sur le
// serveur visé est perdue. Même précaution que lancement-partie.spec.ts.
//
//   npx playwright test tests/campagne-panneau.spec.ts --project=pc
import { test, expect, type APIRequestContext, type Page } from '@playwright/test'
import { allerA, parcoursOuvert, validerParcours } from './aide-parcours-fin'

const NOM = 'Essai automatique - panneau'
const REGLES = [
  'v16_all',
  'no_crisis_of_infinite_deadpools',
  'no_encounter_cards_ignore_crisis',
  'mode_campaign',
]

type Campagne = {
  id: string
  nom?: string
  carnet?: Record<string, string>
  termines?: string[]
}

let identifiant = ''

/* ------------------------------------------------------- le pilote HTTP -- */

/** Répond la première option légale, comme le pilote de la sonde. */
async function repondre(request: APIRequestContext): Promise<void> {
  const brut = await (await request.get('/get_ask?p=0')).text()
  if (!brut.trim()) return
  const ask = JSON.parse(brut) as { options_json?: string }
  const options = JSON.parse(ask.options_json ?? '[]') as Array<Record<string, unknown>>
  for (const o of options) {
    if (o && !o.failure_reason) {
      const legales = ((o.all_legal_targets as unknown[]) ?? []).map(String)
      const mini = ((o.target_num_range as number[]) ?? [0, 0])[0]
      const reponse = {
        id: String(o.id ?? 0),
        targets: mini ? legales.slice(0, mini) : [],
        resources: [],
      }
      await request.post('/post?p=0', { data: encodeURIComponent(JSON.stringify(reponse)) })
      return
    }
  }
}

const monde = async (request: APIRequestContext) =>
  (await (await request.get('/get_world?p=0')).json()) as Record<string, unknown>

/** Lance un scénario de campagne, plateau ouvert, et le mène jusqu'à sa fin. */
async function jouerJusquALaFin(
  page: Page,
  request: APIRequestContext,
  scenario: string,
  carnet: Record<string, string>,
  achever: string
) {
  const definition = await (await request.get(`/get_scenario_json?${scenario}`)).json()
  const deck = await (await request.get('/get_hero_json?maria_hill')).json()
  await request.get(
    '/new?data=' +
      encodeURIComponent(
        JSON.stringify({
          campaign_json: JSON.stringify(definition),
          campaign_log: carnet,
          challenges: definition.challenges ?? [],
          encounter_set_names: [
            ...new Set([...(definition.encounter_sets ?? []), ...(definition.modular_sets ?? [])]),
          ],
          hero_json: [JSON.stringify(deck)],
          rules: REGLES,
          seed: 1234,
          timeout: 0,
        })
      )
  )

  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)

  // Mise en place puis mulligans.
  for (let i = 0; i < 25; i++) {
    await repondre(request)
    const m = await monde(request)
    const phase = String(m.phase ?? '')
    if (phase && !phase.includes('Setup') && !phase.includes('Mulligan')) break
    await page.waitForTimeout(400)
  }

  await request.get('/debug?' + encodeURIComponent(achever))
  for (let i = 0; i < 40; i++) {
    await repondre(request)
    const m = await monde(request)
    if (m.game_over) return m
    if (i % 6 === 5) await request.get('/debug?' + encodeURIComponent(achever))
    await page.waitForTimeout(500)
  }
  throw new Error(`La partie de ${scenario} ne s'est jamais terminée.`)
}

/* ----------------------------------------------------------- la campagne -- */

async function poser(
  request: APIRequestContext,
  campagne: Partial<Campagne> & Record<string, unknown>
): Promise<string> {
  const reponse = await request.post('/save_campagne', {
    data: {
      campagne: {
        ...(identifiant ? { id: identifiant } : {}),
        code: 'aos',
        nom: NOM,
        difficulte: 'standard',
        equipe: [{ heros: 'maria_hill', nomHeros: 'Maria Hill' }],
        tentatives: {},
        partieEnCours: null,
        ...campagne,
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

test.describe.serial('Le panneau de récompenses', () => {
  test.setTimeout(180000)

  test('Victoire de campagne : le panneau s’ouvre et enregistre le relevé du moteur', async ({
    page,
    request,
  }) => {
    identifiant = await poser(request, { termines: [], carnet: {} })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'black_widow' })
      )
    }, identifiant)

    const m = await jouerJusquALaFin(
      page,
      request,
      'black_widow',
      { 'A.I.M. Envelope': '50185;50188;50191' },
      'Damage("Black Widow", 100)'
    )
    expect(m.players_won, 'La partie devait être gagnée.').toBe(true)

    // Le panneau ne s'ouvre que si le contexte de campagne existe ET que le
    // monde dit la partie finie : c'est ce câblage-là qui n'était pas prouvé.
    await parcoursOuvert(page)
    await expect(page.locator('.pf-sous-haut')).toContainText(/Sc[ée]nario 1/)

    await validerParcours(page)
    // Valider ramène à l'écran des campagnes : c'est le signe observable que
    // le panneau est allé au bout, contexte effacé compris. On ne peut pas
    // vérifier l'effacement lui-même — `addInitScript` repose la clé à chaque
    // navigation, y compris celle-ci.
    await page.waitForURL(/\/campagne\.html/, { timeout: 30000 })

    const apres = await relire(request)
    expect(apres.termines, 'Le scénario gagné n’est pas marqué terminé.').toContain('black_widow')
    // Les trois membres du Conseil sont relevés par le moteur à chaque partie :
    // leur présence prouve que ce que le panneau AFFICHAIT est bien ce qu'il a
    // ENREGISTRÉ, et pas une valeur reconstruite au hasard.
    for (const membre of [
      'Secret Counters: Chief Medical Officer',
      'Secret Counters: Chief Surveillance Officer',
      'Secret Counters: Chief Tactical Officer',
    ]) {
      expect(apres.carnet?.[membre], `${membre} manque au carnet.`).toBeDefined()
    }
  })

  test('Défaite hors dernier scénario : rien ne s’ouvre, rien ne se reporte', async ({
    page,
    request,
  }) => {
    await poser(request, { termines: [], carnet: {} })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'black_widow' })
      )
    }, identifiant)

    const m = await jouerJusquALaFin(
      page,
      request,
      'black_widow',
      { 'A.I.M. Envelope': '50185;50188;50191' },
      'Eliminate(0)'
    )
    expect(m.players_won, 'La partie devait être perdue.').toBe(false)

    await expect(page.locator('.fin-partie')).toBeVisible({ timeout: 20000 })
    await page.waitForTimeout(3000)
    await expect(
      page.locator('.parcours-fin'),
      'Le parcours s’ouvre sur une défaite qui se rejoue sans pénalité.'
    ).toHaveCount(0)

    const apres = await relire(request)
    expect(apres.termines ?? [], 'Un scénario perdu a été marqué terminé.').not.toContain(
      'black_widow'
    )
  })

  test('Défaite au scénario 5 : le panneau re-prépare l’enquête', async ({ page, request }) => {
    // Deux preuves en main, deux scénarios méritants : la reprise doit rendre
    // deux preuves, tirées d'une enveloppe NEUVE.
    await poser(request, {
      termines: ['black_widow', 'batroc', 'modok', 'thunderbolts'],
      carnet: {
        'Evidence Gained': '50185;50186',
        'Scenarios With A Cleared Board Member': '2',
      },
    })
    const avant = await relire(request)
    expect(preuves(avant)).toEqual(['50185', '50186'])

    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'baron_zemo' })
      )
    }, identifiant)

    const m = await jouerJusquALaFin(
      page,
      request,
      'baron_zemo',
      {
        'A.I.M. Envelope': '50187;50190;50193',
        'Evidence Gained': '50185;50186',
        'Scenarios With A Cleared Board Member': '2',
      },
      'Eliminate(0)'
    )
    expect(m.players_won, 'La partie devait être perdue.').toBe(false)

    // En standard, perdre le dernier scénario ne perd pas la campagne : le
    // panneau s'ouvre quand même, pour re-préparer les preuves.
    await parcoursOuvert(page)
    await allerA(page, 'bilan')
    await expect(page.locator('.pf-alerte').filter({ hasText: /preuve|evidence/i })).toBeVisible()
    await expect(page.locator('.pf-alerte').filter({ hasText: /preuve|evidence/i })).toContainText('2')

    await validerParcours(page)
    await page.waitForURL(/\/campagne\.html/, { timeout: 30000 })

    const apres = await relire(request)
    expect(apres.termines ?? [], 'Le dernier scénario perdu a été marqué terminé.').not.toContain(
      'baron_zemo'
    )
    expect(preuves(apres), 'Deux preuves devaient être rendues.').toHaveLength(2)
    // L'enveloppe est NEUVE : les preuves rendues n'ont aucune raison d'être
    // celles d'avant, et surtout la taupe a changé — ce que le client ne voit
    // pas, et ne doit pas voir.
    expect(JSON.stringify(apres)).not.toContain('secret_aim')
    expect(JSON.stringify(apres)).not.toContain('A.I.M. Envelope')
  })
})
