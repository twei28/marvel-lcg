// Une campagne menée à plusieurs, chacun sur son appareil.
//
// Ce que ce fichier prouve, et que rien d'autre ne prouvait :
//
// * un siège qui n'a JAMAIS posé la clé `mc-campagne-partie` sait quand même
//   qu'il joue une campagne. C'est tout le chantier : avant, seul celui qui
//   avait lancé depuis l'écran des campagnes avait cette clé, et les autres
//   avaient un plateau ordinaire — ni panneau de récompenses, ni règle de
//   défaite, ni carnet ;
// * une case du carnet n'appartient qu'à un siège. Les autres la voient se
//   remplir mais ne peuvent pas l'écrire ;
// * « Valider » n'existe que chez l'hôte. Un distant qui l'aurait terminerait
//   le scénario pour toute la table depuis un écran où il n'a rempli qu'une
//   case ;
// * le carnet relu contient les DEUX saisies, celle de l'hôte et celle du
//   distant, sans que l'une écrase l'autre.
//
//   npx playwright test tests/campagne-multi.spec.ts --project=pc
//
// ATTENTION : ce test lance une VRAIE partie. Toute partie en cours sur le
// serveur visé est perdue. Même précaution que campagne-releves.spec.ts.
//
// Ce qu'il ne couvre PAS, et qui demande un humain : le SALON. Un invité qui
// ouvre son lien doit lire « Tu tiens <héros> » et non « Choisis ton héros ».
// Le salon vit hors du plateau, et rien ici ne l'atteint.
import { test, expect, type Browser, type Page } from '@playwright/test'
import { allerA, parcoursOuvert, validerParcours } from './aide-parcours-fin'
import {
  acheverLaPartie,
  lancer,
  monde,
  nettoyer,
  ouvrirEtMettreEnPlace,
  poserCampagne,
  relireCampagne,
  tuerLeVilainEnJeu,
} from '../pilote-campagne'

const NOM = 'Essai automatique - multi'

/** Les quatre améliorations Tech de Crossbones, le champ `parJoueur` du scénario 1. */
const TECH = ['04155', '04156', '04157', '04158']

/**
 * Les lignes d'un champ personnel, une par siège.
 *
 * On cible le champ par sa NATURE (« celui qui nomme des joueurs ») et non par
 * son rang, et les cartes DANS leur ligne plutôt que par un index global. La
 * première version comptait les boutons de tout le panneau : elle a compris
 * qu'un champ portait trois options quand il en porte quatre, et pointait la
 * mauvaise carte tout en ayant l'air juste.
 */
const lignesPersonnelles = (p: Page) =>
  p.locator('.camp-champ:has(.camp-champ-joueur)').first().locator('.camp-champ-ligne')

/** L'équipe figée de la campagne. Le siège N tient le N-ième membre. */
const EQUIPE = [
  { heros: 'spider_man', nomHeros: 'Spider-Man' },
  { heros: 'captain_america', nomHeros: 'Captain America' },
]

type Route = { id?: string; scenario?: string; nom?: string; equipe?: Array<Record<string, string>> }

let identifiant = ''

test.beforeAll(async ({ request }) => {
  await nettoyer(request, NOM)
})

test.afterAll(async ({ request }) => {
  if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
})

/**
 * Ouvre un plateau pour un siège donné, SANS jamais poser la clé de campagne.
 *
 * C'est la condition du test : ce siège doit apprendre du serveur qu'il joue
 * une campagne. Poser la clé ici rendrait le test vert pour la mauvaise raison,
 * et c'est exactement le piège de la première version de `campagne-aoa` (un
 * test qui passait avec ET sans la clé).
 */
async function ouvrirSiegeDistant(browser: Browser, siege: number): Promise<Page> {
  const contexte = await browser.newContext()
  const page = await contexte.newPage()
  await page.goto(`/app/board.html?p=${siege}`, { waitUntil: 'networkidle' })
  const cle = await page.evaluate(() => window.localStorage.getItem('mc-campagne-partie'))
  expect(cle, 'Le siège distant ne doit avoir AUCUNE clé de campagne.').toBeNull()
  return page
}

test.describe.serial('Campagne à plusieurs', () => {
  test.setTimeout(300000)

  test("hors campagne, le serveur ne désigne aucune campagne", async ({ request }) => {
    // Sans ce cas, la route pourrait rendre n'importe quoi en permanence et le
    // panneau de récompenses s'ouvrirait sur des parties ordinaires.
    await nettoyer(request, NOM)
    const brut = (await (await request.get('/get_campagne_en_cours?')).json()) as Route
    expect(brut.scenario ?? '', 'Aucune partie de campagne ne tourne encore.').toBe('')
  })

  test('un siège qui n’a jamais eu la clé voit le panneau, et n’écrit que ses cases', async ({
    page,
    request,
    browser,
  }) => {
    identifiant = await poserCampagne(request, {
      nom: NOM,
      code: 'trors',
      difficulte: 'standard',
      equipe: EQUIPE,
      termines: [],
      carnet: {},
      partieEnCours: { scenario: 'crossbones', depuis: new Date().toISOString() },
    })

    // L'HÔTE a la clé, comme l'écran des campagnes la lui pose.
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'crossbones' })
      )
    }, identifiant)

    await lancer(request, { scenario: 'crossbones', heros: EQUIPE.map((m) => m.heros), carnet: {} })
    await ouvrirEtMettreEnPlace(page, request)

    // La route désigne la campagne, et porte l'équipe dans l'ordre des sièges.
    const route = (await (await request.get('/get_campagne_en_cours?')).json()) as Route
    expect(route.id).toBe(identifiant)
    expect(route.scenario).toBe('crossbones')
    expect((route.equipe ?? []).map((m) => m.nomHeros)).toEqual(EQUIPE.map((m) => m.nomHeros))

    // Le secret et le carnet n'ont rien à faire dans cette réponse.
    const brut = await (await request.get('/get_campagne_en_cours?')).text()
    expect(brut, 'La route ne doit pas laisser filer le carnet.').not.toContain('carnet')

    const fin = await acheverLaPartie(page, request, tuerLeVilainEnJeu)
    expect(fin.players_won, 'La partie devait être gagnée.').toBe(true)

    // --- Le siège distant, celui qui n'a jamais rien posé --------------------
    const distant = await ouvrirSiegeDistant(browser, 1)
    await parcoursOuvert(distant, 30000) // le siège 1 voit le parcours sans avoir jamais eu la clé
    await allerA(distant, 'bilan')
    await allerA(page, 'bilan')

    // Le champ « Tech Upgrade » porte une ligne par siège. Chez le distant, la
    // ligne du siège 0 est inerte et la sienne est ouverte.
    const chezDistant = lignesPersonnelles(distant)
    await expect(chezDistant).toHaveCount(EQUIPE.length)
    await expect(chezDistant.nth(0).locator('.camp-carte').first()).toBeDisabled()
    await expect(chezDistant.nth(1).locator('.camp-carte').first()).toBeEnabled()
    // Et il lit à qui appartient la case qu'il ne peut pas remplir.
    await expect(chezDistant.nth(0)).toContainText(/à remplir par|to be filled in by/i)

    // Exactement l'inverse chez l'hôte.
    const chezHote = lignesPersonnelles(page)
    await expect(chezHote.nth(0).locator('.camp-carte').first()).toBeEnabled()
    await expect(chezHote.nth(1).locator('.camp-carte').first()).toBeDisabled()

    // --- Chacun remplit sa case, l'hôte lance la suite ----------------------
    await chezDistant.nth(1).locator('.camp-carte').nth(1).click() // le distant prend 04156
    // « Continuer » envoie SES champs, et rien d'autre : le serveur doit les avoir.
    await allerA(distant, 'carnet')
    await expect
      .poll(async () => (await relireCampagne(request, identifiant)).carnet?.['Player 2 Tech Upgrade'], {
        timeout: 20000,
      })
      .toBe(TECH[1])
    // La liste « À choisir avant de continuer » ne s'affiche PAS chez lui : elle
    // nommait des cases appartenant à d'autres joueurs, qu'il ne peut pas remplir.
    await expect(distant.locator('.pf-info')).not.toContainText(/choisir|choose/i)
    // « Commencer » est à l'hôte, et à lui seul : le distant attend.
    await allerA(distant, 'suite')
    await expect(distant.locator('.pf-bas .pf-btn-or')).toHaveCount(0)
    await expect(distant.locator('.pf-attente')).toBeVisible()

    await chezHote.nth(0).locator('.camp-carte').nth(0).click() // l'hôte prend 04155
    await validerParcours(page)
    await page.waitForURL(/\/campagne\.html/, { timeout: 30000 })

    // --- Le carnet porte les DEUX saisies -----------------------------------
    const campagne = await relireCampagne(request, identifiant)
    expect(campagne.carnet?.['Player 1 Tech Upgrade'], "La saisie de l'hôte manque.").toBe(TECH[0])
    expect(campagne.carnet?.['Player 2 Tech Upgrade'], 'La saisie du distant a été écrasée.').toBe(
      TECH[1]
    )
    expect(campagne.termines, 'Le scénario devait être reporté.').toContain('crossbones')

    await distant.context().close()
  })
})
