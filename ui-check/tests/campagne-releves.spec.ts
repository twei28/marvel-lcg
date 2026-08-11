// Le carnet se remplit tout seul avec ce que la partie a produit.
//
// C'est la promesse du mode campagne : le joueur ne recopie rien. Le moteur
// releve son carnet SORTANT a la fin de partie (`campaign_log_last.json`), les
// detecteurs lisent le descripteur de monde pour ce que le moteur ne fournit
// pas, et le panneau de recompenses ecrit le tout.
//
// Trois relevés etaient jusqu'ici prouves SUR DES FORMES, jamais dans une vraie
// fin de partie — et un quatrieme n'existait pas du tout :
//
// * `Marauders Defeated` et `Morlocks Saved` (NeXt Evolution, scenario 1)
//   etaient LUS au scenario 2 et ECRITS par personne. Les deux recompenses du
//   premier scenario se perdaient en silence : le scenario 2 retirait zero
//   Maraudeur et ne donnait aucune carte. Cable dans `CollectNeXt` le 11/8/2026.
// * `pv_restants` (campagne experte) etait teste unitairement sur un descripteur
//   capture, jamais sur une identite reellement blessee en jeu.
// * `cartes_sous_complot` (les allies restes sous la Prison d'Hydra a la fin de
//   Zola) de meme — et c'est precisement la famille de detecteur ou un bug
//   s'etait deja glisse, celui des armes experimentales qui en relevait quatre
//   au lieu d'une.
//
//   npm run campagne-releves
//
// ATTENTION : ce test lance de VRAIES parties. Toute partie en cours sur le
// serveur visé est perdue. Meme precaution que lancement-partie.spec.ts.
import { test, expect } from '@playwright/test'
import {
  acheverLaPartie,
  blesserIdentite,
  lancer,
  monde,
  nettoyer,
  ouvrirEtMettreEnPlace,
  poserCampagne,
  repondre,
  relireCampagne,
  tuerLeVilainEnJeu,
  type Monde,
} from '../pilote-campagne'

const NOM = 'Essai automatique - releves'

const liste = (valeur?: string) => (valeur ?? '').split(';').filter(Boolean)

/** Les Morlocks encore en jeu, tous sieges confondus : ce que le releve compte. */
const morlocksEnJeu = (m: Monde) =>
  ((m.players ?? []) as Array<Record<string, any>>).reduce(
    (total, j) =>
      total + ((j?.allies ?? []) as Array<Record<string, unknown>>)
        .filter((a) => String(a.card_id) === MORLOCK).length,
    0
  )

/** Les sept Maraudeurs de Morlock Siege : trois sous « Routed » et c'est gagne. */
const MARAUDEURS = ['40070a', '40071a', '40072a', '40073a', '40074a', '40075a', '40076a']

/** Les quatre allies CAPTIVE du set Taskmaster, ceux que Zola peut retenir. */
const ALLIES_TASKMASTER = ['04097', '04098', '04099', '04100']
/** L'allie Morlock du set : c'est lui que le releve compte, en jeu, a la fin. */
const MORLOCK = '40079'
/** La piste de reputation deja marquee avant la partie : le releve s'y ajoute. */
const PISTE_AVANT = 8
/** La Prison d'Hydra : les allies qui finissent dessous quittent la campagne. */
const PRISON = '04122'

test.describe.serial('Campagne : ce que le jeu releve tout seul', () => {
  test.setTimeout(240000)

  let identifiant = ''

  test.beforeAll(async ({ request }) => {
    await nettoyer(request, NOM)
  })

  test.afterAll(async ({ request }) => {
    if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
  })

  test('NeXt Evolution 1 : les Maraudeurs mis en deroute et les Morlocks sauves', async ({
    page,
    request,
  }) => {
    identifiant = await poserCampagne(request, {
      code: 'next_evol',
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
        JSON.stringify({ id, scenario: 'morlock_siege' })
      )
    }, identifiant)

    await lancer(request, { scenario: 'morlock_siege', heros: ['colossus'] })
    await ouvrirEtMettreEnPlace(page, request)

    // Un Morlock pose a la main : ils n'entrent en jeu qu'a la revelation de
    // « Mutant Massacre », que rien ne garantit avant la victoire, et le relevé
    // compte les Morlocks EN JEU a la fin. Par card_id, et avec UN SEUL argument :
    // la console n'accepte que `PutIntoPlay(carte)`, et l'appeler autrement leve
    // une exception qui peut abattre le moteur (voir pilote-campagne.ts).
    await request.get('/debug?' + encodeURIComponent(`PutIntoPlay("${MORLOCK}")`))
    for (let i = 0; i < 3; i++) {
      await repondre(request)
      await page.waitForTimeout(500)
    }
    expect(
      morlocksEnJeu(await monde(request)),
      "Le Morlock n'a pas ete mis en jeu : le releve n a rien a compter."
    ).toBeGreaterThan(0)

    // Trois vilains sous « Routed » = victoire. Le vilain en jeu change apres
    // chaque defaite, d'ou la forme fonction : frapper un nom fixe ne tuerait
    // que le premier.
    const m: Monde = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait etre gagnee (trois vilains en deroute).').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    const maraudeurs = liste(apres.carnet?.['Marauders Defeated'])
    expect(
      maraudeurs.length,
      'Les Maraudeurs mis en deroute ne sont pas au carnet : le scenario 2 n en retirera aucun.'
    ).toBe(3)
    for (const id of maraudeurs) expect(MARAUDEURS).toContain(id)
    // Compare au monde FINAL, celui que `CollectNeXt` a lu : un compte en dur
    // dependrait du nombre de Morlocks qu'on a reussi a poser, pas du releve.
    expect(
      apres.carnet?.['Morlocks Saved'],
      'Les Morlocks sauves ne sont pas comptes : le scenario 2 ne donnera aucune carte.'
    ).toBe(String(morlocksEnJeu(m)))
  })

  test('Sinister Motives : la piste de reputation se calcule et s ajoute au total', async ({
    page,
    request,
  }) => {
    // Six conditions imprimees sous la piste (livret sm p.22), toutes des lectures
    // de la table a la fin du scenario — et le joueur les recopiait a la main dans
    // un champ « choix ». La piste part a 8 : le releve doit AJOUTER, pas remplacer.
    await poserCampagne(request, {
      id: identifiant,
      code: 'sm',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man' }],
      termines: [],
      carnet: { 'Reputation Track': String(PISTE_AVANT) },
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem('mc-campagne-partie', JSON.stringify({ id, scenario: 'sandman' }))
    }, identifiant)

    await lancer(request, {
      scenario: 'sandman',
      heros: ['spider_man'],
      carnet: { 'Reputation Track': String(PISTE_AVANT) },
    })
    await ouvrirEtMettreEnPlace(page, request)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait etre gagnee.').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    // Le champ n'est plus une case a remplir : il arrive DEJA rempli, et reste
    // corrigeable pour qui joue avec la piste papier.
    const champ = page.locator('.camp-champ', { hasText: /réputation/i }).first()
    await expect(champ.locator('.camp-champ-marque')).toBeVisible()
    const affiche = Number(await champ.locator('.camp-champ-int').inputValue())
    expect(affiche, 'La piste affichee est inferieure au total deja marque.').toBeGreaterThanOrEqual(
      PISTE_AVANT
    )

    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    const total = Number(apres.carnet?.['Reputation Track'])
    expect(total, 'La piste enregistree ne correspond pas a ce que le panneau affichait.').toBe(
      affiche
    )
    expect(total, 'La piste a REMPLACE le total au lieu de s y ajouter.').toBeGreaterThan(PISTE_AVANT)
  })

  test('Campagne experte : les PV restants sont ceux de l identite blessee', async ({
    page,
    request,
  }) => {
    await poserCampagne(request, {
      id: identifiant,
      code: 'next_evol',
      nom: NOM,
      difficulte: 'expert',
      equipe: [{ heros: 'colossus', nomHeros: 'Colossus' }],
      termines: [],
      carnet: {},
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'morlock_siege' })
      )
    }, identifiant)

    await lancer(request, { scenario: 'morlock_siege', heros: ['colossus'], expert: true })
    await ouvrirEtMettreEnPlace(page, request)

    // Cinq points de degats sur l'identite, avant la victoire : sans blessure, le
    // relevé rendrait les PV imprimes et un plafonnement casse passerait inapercu.
    const debut = await monde(request)
    for (const c of blesserIdentite(debut, 5)) {
      await request.get('/debug?' + encodeURIComponent(c))
    }
    // La console n'execute ses commandes qu'au prochain cycle du moteur : sans ces
    // reponses, on mesure l'etat d'AVANT et on croit que la commande a echoue.
    for (let i = 0; i < 4; i++) {
      await repondre(request)
      await page.waitForTimeout(500)
    }
    const avant = await monde(request)
    const identite = (avant.players?.[0]?.area_hero ?? [])[0]
    const pv = Number(identite?.info?.health)
    const max = Number(identite?.info?.max_health)
    expect(pv, 'Les degats n ont pas ete appliques a l identite.').toBeLessThan(max)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait etre gagnee.').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    const releve = Number(apres.carnet?.['Player 1 Remaining hit points'])
    expect(
      releve,
      'Les PV restants ne sont pas au carnet : le scenario suivant repartira a plein.'
    ).toBeGreaterThan(0)
    expect(releve, 'Les PV releves depassent les PV imprimes de l identite.').toBeLessThanOrEqual(
      max
    )
  })

  test('Zola : les allies restes sous la Prison d Hydra quittent la campagne', async ({
    page,
    request,
  }) => {
    // Le carnet arrive avec les quatre allies secourus au scenario 3 : c'est la
    // situation du livret, ou l'on peut en perdre une partie au scenario 4.
    await poserCampagne(request, {
      id: identifiant,
      code: 'trors',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'captain_america', nomHeros: 'Captain America' }],
      termines: ['crossbones', 'absorbing_man', 'taskmaster'],
      carnet: { 'Player 1 Rescued Allies': ALLIES_TASKMASTER.join(';') },
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem('mc-campagne-partie', JSON.stringify({ id, scenario: 'zola' }))
    }, identifiant)

    await lancer(request, {
      scenario: 'zola',
      heros: ['captain_america'],
      carnet: { 'Player 1 Rescued Allies': ALLIES_TASKMASTER.join(';') },
    })
    await ouvrirEtMettreEnPlace(page, request)

    // La Prison d'Hydra se remplit TOUTE SEULE a sa revelation : elle cherche un
    // allie propre a l'identite dans le deck, la main ou la defausse de chaque
    // joueur et le place sous elle (04122.py). On ne pose donc rien a la main —
    // c'est la vraie mecanique du scenario qui produit la forme a mesurer, et
    // c'est tout l'interet de l'eprouver ici plutot qu'a la sonde.
    await request.get('/debug?' + encodeURIComponent(`Reveal("${PRISON}")`))
    await page.waitForTimeout(1500)

    for (let i = 0; i < 3; i++) {
      await repondre(request)
      await page.waitForTimeout(500)
    }
    const etat = await monde(request)
    const prison = (etat.area_schemes_side ?? []).find(
      (c: Record<string, unknown>) => c.card_id === PRISON
    )
    expect(prison, "La Prison d'Hydra n'est pas en jeu : le releve n a rien a mesurer.").toBeTruthy()
    // Ce que le detecteur doit rendre : meme zone que le complot, avec
    // `bind_object_id` egal a son `id`. On lit l'etat REEL plutot que d'imposer
    // une liste : le test eprouve le detecteur, pas le contenu d'un deck.
    const captifs = (etat.area_schemes_side ?? [])
      .filter((c: Record<string, unknown>) => c.bind_object_id === (prison as Record<string, unknown>).id)
      .map((c: Record<string, unknown>) => String(c.card_id))
    expect(
      captifs.length,
      "Aucun allie n'a ete emprisonne : le scenario ne produit pas la forme attendue."
    ).toBeGreaterThan(0)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait etre gagnee.').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    const retires = liste(apres.carnet?.['Allies removed from the campaign'])
    expect(
      retires.sort(),
      'Les allies restes prisonniers ne sont pas notes : ils reviendraient au scenario 5.'
    ).toEqual(captifs.sort())
  })
})
