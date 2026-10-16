// Les trois boîtes qu'aucun test n'avait jamais jouées.
//
// Cinq boîtes sur huit avaient traversé une vraie partie (aos, next_evol, sm,
// trors, aoa). Les trois autres — The Mad Titan's Shadow, La Genèse des Mutants,
// Galaxy's Most Wanted — n'étaient validées que par l'audit texte-vs-code et par
// la sonde : leurs mises en place ont été relues encart par encart contre le
// livret, mais aucune partie n'avait été menée jusqu'à ce que le carnet s'écrive.
//
// Ce test comble ça, et chaque cas visé est le RELEVÉ que la boîte a de plus
// caractéristique :
//
//   mts     — « Campaign Pool: Cosmo » : l'allié Cosmo (21180b) reste dans le pool
//             de campagne s'il est en jeu à la fin du scénario 1.
//   mut_gen — « Role » : le rôle est choisi EN JEU à la mise en place, et remonte
//             au carnet par le STORE (`CampaignLog.SetStr`), pas par le collecteur.
//             C'est un chemin d'écriture que rien n'éprouvait.
//   gmw     — « Unspent Units » : la monnaie du Marché, qui s'ACCUMULE d'un
//             scénario à l'autre (« add these to units you already have »).
//
// La méthode est celle du §10 : vraie partie, plateau ouvert, réponses par
// `/get_ask` + `/post`, fin forcée par `/debug`. Les conditions de relevé sont
// posées par la console quand le hasard d'une partie ne les garantit pas — ce qu'on
// éprouve est le RELEVÉ, pas la chance.
//
//   npm run campagne-boites-restantes
//
// ATTENTION : ce test lance de VRAIES parties. Toute partie en cours sur le
// serveur visé est perdue.
import { test, expect } from '@playwright/test'
import {
  acheverLaPartie,
  lancer,
  monde,
  nettoyer,
  ouvrirEtMettreEnPlace,
  poserCampagne,
  relireCampagne,
  repondre,
  tuerLeVilainEnJeu,
} from '../pilote-campagne'

const NOM = 'Essai automatique - boites restantes'

/** Cosmo, verso de « Secure the Landing Pad » : en jeu à la fin, il rejoint le pool. */
const COSMO = '21180b'
/** Metro P.D., face vaincue de la manigance de campagne du scénario 1 de mut_gen. */
const METRO_PD = '32171b'
/** Les quatre rôles de Mutant Genesis, choisis une fois pour toute la campagne. */
const ROLES = ['Brawler', 'Commander', 'Defender', 'Peacekeeper']
/** Unités déjà au carnet : le relevé doit s'y AJOUTER, pas les remplacer. */
const UNITES_AVANT = 4

/** Envoie une commande de console, puis laisse le moteur l'exécuter. */
async function console_(page: import('@playwright/test').Page, request: any, commande: string) {
  await request.get('/debug?' + encodeURIComponent(commande))
  for (let i = 0; i < 3; i++) {
    await repondre(request)
    await page.waitForTimeout(400)
  }
}

test.describe.serial('Campagne : les trois boîtes jamais jouées par un test', () => {
  test.setTimeout(300000)

  let identifiant = ''

  test.beforeAll(async ({ request }) => {
    await nettoyer(request, NOM)
  })

  test.afterAll(async ({ request }) => {
    if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
  })

  test("The Mad Titan's Shadow : Cosmo rejoint le pool de campagne", async ({ page, request }) => {
    identifiant = await poserCampagne(request, {
      ...(identifiant ? { id: identifiant } : {}),
      code: 'mts',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'captain_america', nomHeros: 'Captain America' }],
      termines: [],
      carnet: {},
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'ebony_maw' })
      )
    }, identifiant)

    await lancer(request, { scenario: 'ebony_maw', heros: ['captain_america'], carnet: {} })
    await ouvrirEtMettreEnPlace(page, request)

    // Cosmo n'entre en jeu que si l'équipe sécurise la piste d'atterrissage : on
    // pose la condition, puisque ce qu'on mesure est le relevé, pas la partie.
    await console_(page, request, `PutIntoPlay("${COSMO}")`)
    const avant = await monde(request)
    const cosmoEnJeu = ((avant.players ?? []) as Array<Record<string, any>>).some((j) =>
      ((j?.allies ?? []) as Array<Record<string, any>>).some((a) => String(a.card_id) === COSMO)
    )
    expect(cosmoEnJeu, "Cosmo n'a pas été mis en jeu : le relevé n'a rien à voir.").toBe(true)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait être gagnée.').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    expect(
      apres.carnet?.['Campaign Pool: Cosmo'],
      "Cosmo était en jeu à la victoire et n'est pas au carnet : il manquera au scénario suivant."
    ).toBe('1')
    expect(apres.termines, 'Le scénario gagné n’est pas marqué terminé.').toContain('ebony_maw')
  })

  test("The Mad Titan's Shadow, témoin : sans Cosmo en jeu, rien n'est relevé", async ({
    page,
    request,
  }) => {
    // Le témoin de la mesure précédente. Sans lui, un carnet qui porterait
    // « Campaign Pool: Cosmo » à TOUTES les parties passerait pour une preuve.
    // On lit le carnet SORTANT du moteur, pas celui de la campagne : c'est le
    // collecteur qu'on interroge, et il ne demande pas de passer par le panneau.
    await lancer(request, { scenario: 'ebony_maw', heros: ['captain_america'], carnet: {} })
    await ouvrirEtMettreEnPlace(page, request)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait être gagnée.').toBe(true)
    await page.waitForTimeout(1500)

    const sortant = (await (await request.get('/get_carnet_suggere?')).json()) as {
      scenario: string | null
      suggestions: Record<string, string>
    }
    expect(sortant.scenario, "Le carnet sortant ne vient pas de la partie jouée.").toBe('ebony_maw')
    expect(
      Object.keys(sortant.suggestions ?? {}).length,
      "Le moteur n'a rien relevé : le témoin ne prouverait rien."
    ).toBeGreaterThan(0)
    expect(
      sortant.suggestions?.['Campaign Pool: Cosmo'],
      'Cosmo est relevé alors qu’il n’était pas en jeu : le relevé ne mesure pas ce qu’on croit.'
    ).toBeUndefined()
  })

  test('La Genèse des Mutants : le rôle choisi en jeu arrive au carnet', async ({
    page,
    request,
  }) => {
    identifiant = await poserCampagne(request, {
      id: identifiant,
      code: 'mut_gen',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'colossus', nomHeros: 'Colossus' }],
      termines: [],
      carnet: {},
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'sabretooth' })
      )
    }, identifiant)

    await lancer(request, { scenario: 'sabretooth', heros: ['colossus'], carnet: {} })
    await ouvrirEtMettreEnPlace(page, request)

    // La manigance de campagne vaincue : sa face B suffit au relevé (FaceExists).
    // La mise en place la pose déjà en jeu sur sa face A ; « PutIntoPlay » de la
    // face B ne fabrique plus de doublon (la recherche rend la face visible), il
    // faut donc la RETOURNER, comme le fait la partie quand la manigance est vaincue.
    await console_(page, request, `Flip("${METRO_PD.replace('b', 'a')}")`)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait être gagnée.').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    // LE CAS QUI COMPTE : le rôle est demandé au joueur pendant la mise en place et
    // écrit dans le STORE du moteur, pas par le collecteur de fin de partie. C'est
    // ce chemin-là qu'aucun test ne traversait, et le rôle décide de tout le
    // role-building de la campagne.
    expect(
      ROLES,
      `Le rôle n'est pas au carnet (« ${apres.carnet?.['Player 1 Role']} ») : les améliorations de toute la campagne seraient tirées au hasard.`
    ).toContain(apres.carnet?.['Player 1 Role'])
    expect(
      apres.carnet?.['Frightened Police Defeated'],
      'La manigance de campagne vaincue n’est pas relevée.'
    ).toBe('1')
  })

  test("Galaxy's Most Wanted : les unités du Marché s'accumulent", async ({ page, request }) => {
    identifiant = await poserCampagne(request, {
      id: identifiant,
      code: 'gmw',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'captain_america', nomHeros: 'Captain America' }],
      termines: [],
      carnet: { 'Player 1 Unspent Units': String(UNITES_AVANT) },
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'brotherhood_of_badoon' })
      )
    }, identifiant)

    await lancer(request, {
      scenario: 'brotherhood_of_badoon',
      heros: ['captain_america'],
      carnet: { 'Player 1 Unspent Units': String(UNITES_AVANT) },
    })
    await ouvrirEtMettreEnPlace(page, request)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait être gagnée.').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    const unites = Number(apres.carnet?.['Player 1 Unspent Units'])
    // « Record 1 unit for each player », plus les points de victoire, plus les
    // bonus du scénario : au moins une unité, et JAMAIS un remplacement du total.
    expect(
      unites,
      'Les unités du Marché ont remplacé le total au lieu de s’y ajouter.'
    ).toBeGreaterThan(UNITES_AVANT)
    expect(apres.termines, 'Le scénario gagné n’est pas marqué terminé.').toContain(
      'brotherhood_of_badoon'
    )
  })
})
