// Le mode manuel, dans une VRAIE partie : la preuve à l'écran.
//
// Tout le mode manuel (ui-app/src/board/manuel/) est couvert par des tests
// unitaires et par un harnais moteur (Fusion/marvel-lcg-src/tools/
// test_mode_manuel.py). Aucun des deux ne prouve que le PLATEAU dessine ce
// qu'on croit : un moteur vert ne prouve rien sur le rendu (règle du projet,
// docs/reference/PROCESSUS-CARTE.md, étape 8 bis).
//
// Calqué sur glisser-plateau.spec.ts pour la mécanique de geste, avec deux
// différences dictées par le mode manuel lui-même :
//
//  1. Pas de mulligan à confirmer, et la règle `disable_resolve_mulligans`
//     dans la charge. DÉCOUVERTE EN ÉCRIVANT CE TEST (voir task-8-report.md) :
//     `estModeManuel(world)` vaut vrai dès la création de la partie, bien
//     AVANT que `world.manuel_actif` ne coupe la boucle de jeu — donc
//     `AssistantAction` et `DemandeCentrale`, qui portent le mulligan
//     (« Garder cette main » / « Annuler »), sont déjà masqués pendant la
//     MISE EN PLACE elle-même. Sans `disable_resolve_mulligans`, une partie
//     manuelle reste bloquée à « Resolve Mulligans » pour toujours : aucun
//     geste de mode manuel (glisser, clavier) ne prend effet tant que
//     `World.Initialize` n'a pas rendu la main à `ManualLoop`. Ce n'est pas
//     un artefact de ce test : c'est reproductible sur partie fraîche, et un
//     joueur réel serait bloqué de la même façon. À signaler.
//
//  2. La preuve des dégâts passe par l'ÉCRAN (la pastille de vie,
//     `.jauge-texte`), jamais par `/get_world` : ce point de terminaison ne
//     calcule `info.health` que pour les cartes visées par une action légale
//     (`all_legal_targets`), qui n'existe pas en mode manuel. Un vilain
//     interrogé par `/get_world` y répond donc `info: {}` que le coup ait
//     porté ou non — un silence qui ne dit RIEN sur ce que le moteur a fait,
//     à l'inverse du plateau réellement affiché au joueur.
//
// ⚠ Comme glisser-plateau.spec.ts : ce test lance une NOUVELLE partie sur le
// serveur de jeu. Il se lance à la main, jamais dans les captures, et jamais
// pendant que quelqu'un joue. Prévenir avant.
import { test, expect, type Page, type APIRequestContext } from '@playwright/test'

const AVERTISSEMENT =
  'Attention : ce test lance une NOUVELLE partie MANUELLE. Si une partie est en cours, elle sera perdue.'

test.beforeAll(() => {
  console.log('')
  console.log('  ' + AVERTISSEMENT)
  console.log('')
})

/** Une partie manuelle solo Spider-Man contre Rhino, graine figée. */
async function nouvellePartieManuelle(request: APIRequestContext) {
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const deck = await (await request.get('/get_hero_json?spider_man')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario),
    campaign_log: {},
    challenges: scenario.challenges ?? [],
    encounter_set_names: [
      ...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])]),
    ],
    hero_json: [JSON.stringify(deck)],
    // `disable_resolve_mulligans` : voir l'en-tête de ce fichier. Sans elle,
    // la mise en place ne se termine jamais (mulligan invisible en manuel).
    rules: ['mode_manuel', 'disable_resolve_mulligans'],
    seed: 2026091801,
    timeout: 0,
  }
  const reponse = await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))
  expect(reponse.status(), 'le moteur a refusé la partie manuelle').toBe(200)
}

/** Le compteur de tour, lu chez le MOTEUR (le bandeau qui le montrait est masqué). */
async function tourCourant(page: Page): Promise<number> {
  return page.evaluate(async () => {
    const monde = await (await fetch('/get_world?p=0')).json()
    return monde.round_id
  })
}

/** Le texte de la pastille de vie du vilain, tel qu'affiché à l'écran. */
async function vieVilainAffichee(page: Page): Promise<string | null> {
  return page.locator('.scan-card.kind-villain .jauge-texte').first().textContent()
}

test('la table manuelle : nue, silencieuse, manipulable, annulable', async ({ page, request }) => {
  await nouvellePartieManuelle(request)
  await page.goto('/app/board.html?p=0')
  await page.waitForSelector('.scan-card[data-card-id]', { timeout: 30000 })

  // Laisse la mise en place (mulligan compris) se terminer toute seule avant
  // de commencer à mesurer quoi que ce soit : « automatique et intégrale »
  // (docs/superpowers/specs/2026-09-18-mode-manuel-design.md).
  await page.waitForTimeout(3000)

  // 1. LE PLATEAU EST NU : aucune couche du moteur à l'écran.
  await expect(page.locator('.bandeau-phase')).toHaveCount(0)
  await expect(page.locator('.deroule-phase')).toHaveCount(0)
  await expect(page.locator('.demande-centrale')).toHaveCount(0)
  await expect(page.locator('.assistant-action')).toHaveCount(0)

  // 2. LE MOTEUR NE CONDUIT PLUS : le tour ne bouge pas tout seul.
  // (Le compteur lui-même n'a plus d'affichage — BandeauPhase est masqué —
  // donc on l'interroge où il vit réellement : le monde du moteur.)
  const tourAvant = await tourCourant(page)
  await page.waitForTimeout(10000)
  const tourApres = await tourCourant(page)
  expect(tourApres, 'le tour a avancé tout seul : le moteur conduit encore').toBe(tourAvant)

  // 3. LES GESTES MARCHENT : un glisser d'une carte vers une autre pile la
  // déplace vraiment.
  //
  // ⚠ ADAPTATION AU BRIEF : la défausse Rencontre est VIDE à la mise en
  // place. `zones.ts` ne dessine une pile QUE si elle porte au moins une
  // carte (`toPileCard`, `if (!carte) return []`) : une pile vide n'a donc
  // aucun `.plateau-unite[data-pile=...]` à viser, et un lâcher dessus est
  // structurellement impossible tant qu'elle est vide. On l'amorce d'abord
  // avec UNE carte via le clic droit (« Déplacer vers », déjà un geste du
  // mode manuel, pas de la triche de test) pour lui donner une pile
  // atteignable, puis on prouve le GLISSER avec une AUTRE carte.
  const mainAvantAmorce = await page.locator('[data-zone="main"] .scan-card[data-card-id]').count()
  expect(mainAvantAmorce, 'la main est vide, impossible de continuer').toBeGreaterThan(1)

  const carteAmorce = page.locator('[data-zone="main"] .scan-card[data-card-id]').first()
  await carteAmorce.click({ button: 'right' })
  await page.getByRole('button', { name: 'Déplacer vers' }).click()
  await page.getByRole('button', { name: 'Défausse Rencontre', exact: true }).click()
  await page.waitForSelector('.plateau-unite[data-pile="rencontre-encounter-discard"]', {
    timeout: 10000,
  })
  await expect(page.locator('[data-zone="main"] .scan-card[data-card-id]')).toHaveCount(
    mainAvantAmorce - 1
  )

  const carteGlissee = page
    .locator('[data-zone="main"] .scan-card[data-card-id]')
    .first()
  const idGlissee = await carteGlissee.getAttribute('data-card-id')
  expect(idGlissee, 'aucune carte à glisser en main').toBeTruthy()

  await page.waitForSelector('.plateau-cadre[data-glisser="offert"]', { timeout: 10000 })
  const boiteSource = await carteGlissee.boundingBox()
  const boiteCible = await page
    .locator('.plateau-unite[data-pile="rencontre-encounter-discard"]')
    .boundingBox()
  expect(boiteSource, 'la carte à glisser est hors écran').not.toBeNull()
  expect(boiteCible, 'la défausse Rencontre est hors écran').not.toBeNull()

  await page.mouse.move(
    boiteSource!.x + boiteSource!.width / 2,
    boiteSource!.y + boiteSource!.height / 2
  )
  await page.mouse.down()
  await page.mouse.move(
    boiteCible!.x + boiteCible!.width / 2,
    boiteCible!.y + boiteCible!.height / 2,
    { steps: 12 }
  )
  await expect(page.locator('.plateau-cadre.est-en-glisser')).toBeVisible()
  await page.mouse.up()
  await page.waitForTimeout(1500)

  await expect(page.locator('[data-zone="main"] .scan-card[data-card-id]')).toHaveCount(
    mainAvantAmorce - 2
  )
  await expect(page.locator('.plateau-unite[data-pile="rencontre-encounter-discard"]')).toHaveCount(1)

  // 4. UN REFUS SE VOIT : lâcher une carte dans le vide (aucune pile visée)
  // doit refuser poliment, pas agir en silence — la garantie sur laquelle le
  // chantier a passé le plus de temps.
  const carteRefus = page.locator('[data-zone="main"] .scan-card[data-card-id]').first()
  const boiteRefusSource = await carteRefus.boundingBox()
  expect(boiteRefusSource).not.toBeNull()
  await page.mouse.move(
    boiteRefusSource!.x + boiteRefusSource!.width / 2,
    boiteRefusSource!.y + boiteRefusSource!.height / 2
  )
  await page.mouse.down()
  // Un point du plateau qui n'est ni une pile, ni une carte : le centre du
  // grand vide sous la zone Rencontre. Aucune étiquette PENDANT le glisser
  // (`glisser-manuel.ts`, `libelle` rend `undefined` sur du vide pur) : le
  // refus se voit APRÈS le lâcher, dans la bulle `.glisser-refus`.
  await page.mouse.move(600, 450, { steps: 12 })
  await page.mouse.up()
  await expect(page.locator('.glisser-refus')).toContainText('Lâche la carte sur une pile')
  await page.waitForTimeout(500)

  // 5. SURVOLER LE VILAIN ET TAPER « 3 » LUI POSE TROIS DÉGÂTS, lus À L'ÉCRAN
  // (voir l'en-tête de ce fichier : `/get_world` ne calcule pas `info.health`
  // en dehors d'une action légale, qui n'existe pas en mode manuel).
  const vieAvant = await vieVilainAffichee(page)
  expect(vieAvant, 'la pastille de vie du vilain ne se lit pas').toBeTruthy()

  const vilain = page.locator('.scan-card.kind-villain[data-card-id]').first()
  const boiteVilain = await vilain.boundingBox()
  expect(boiteVilain).not.toBeNull()
  await page.mouse.move(
    boiteVilain!.x + boiteVilain!.width / 2,
    boiteVilain!.y + boiteVilain!.height / 2
  )
  await page.keyboard.press('3')
  await page.waitForTimeout(1500)
  const vieApres = await vieVilainAffichee(page)
  expect(vieApres, "le vilain n'a pas visiblement encaissé les dégâts").not.toBe(vieAvant)

  // 6. CTRL+Z RAMÈNE L'ÉTAT D'AVANT.
  await page.keyboard.press('Control+z')
  await page.waitForTimeout(2500)
  const vieRestauree = await vieVilainAffichee(page)
  expect(vieRestauree, "Ctrl+Z n'a pas rendu les points de vie d'avant").toBe(vieAvant)
})
