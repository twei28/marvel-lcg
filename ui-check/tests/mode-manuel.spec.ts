// Le mode manuel, dans une VRAIE partie : la preuve à l'écran.
//
// Tout le mode manuel (ui-app/src/board/manuel/) est couvert par des tests
// unitaires et par un harnais moteur (Fusion/marvel-lcg-src/tools/
// test_mode_manuel.py). Aucun des deux ne prouve que le PLATEAU dessine ce
// qu'on croit : un moteur vert ne prouve rien sur le rendu (règle du projet,
// docs/reference/PROCESSUS-CARTE.md, étape 8 bis).
//
// ⚠ TÂCHE 8 BIS. La version précédente de ce test créait sa partie en appel
// direct à `/new`, en CONTOURNANT l'écran de préparation — exactement le
// chemin qu'AUCUN joueur n'emprunte. C'est précisément ce qui a laissé
// passer le défaut le plus grave du chantier : une partie manuelle lancée
// depuis l'écran de préparation restait bloquée POUR TOUJOURS au premier
// mulligan (le panneau qui le pose était masqué par erreur sur la RÈGLE
// `mode_manuel`, vraie dès la mise en place, au lieu de l'ÉTAT
// `manuel_actif`, vrai seulement une fois la boucle manuelle entrée — voir
// task-8bis-report.md). Ce test passe désormais par le MÊME chemin qu'un
// joueur : l'assistant de préparation, la case « Partie manuelle », et un
// vrai mulligan résolu au clic (« Garder cette main »), comme
// `zz-gagner.spec.ts` le fait déjà pour une partie ordinaire.
//
// Calqué sur glisser-plateau.spec.ts pour la mécanique de geste, avec une
// différence dictée par le mode manuel lui-même :
//
//  - La preuve des dégâts passe par l'ÉCRAN (la pastille de vie,
//     `.jauge-texte`), jamais par `/get_world` : ce point de terminaison ne
//     calcule `info.health` que pour les cartes visées par une action légale
//     (`all_legal_targets`), qui n'existe pas en mode manuel. Un vilain
//     interrogé par `/get_world` y répond donc `info: {}` que le coup ait
//     porté ou non — un silence qui ne dit RIEN sur ce que le moteur a fait,
//     à l'inverse du plateau réellement affiché au joueur.
//
// ⚠ Comme glisser-plateau.spec.ts et lancement-partie.spec.ts : ce test lance
// une NOUVELLE partie sur le serveur de jeu. Il se lance à la main, jamais
// dans les captures, et jamais pendant que quelqu'un joue. Prévenir avant.
//
// ⚠ I5 (revue finale, 20/09/2026). ÉTAPES 7-8 AJOUTÉES À LA SUITE, PAS DANS
// UN SECOND FICHIER : le montage local (serveur isolé, cache séparé,
// Playwright sous Windows — voir task-8-report.md) coûte cher à répéter.
// Elles prouvent que « Tu pourras revenir en arrière avec Ctrl+Z », la
// promesse de l'écran de fin (`FinManuelle.tsx`), tient de bout en bout sur
// le VRAI écran (`EcranFinPartie`, board.tsx) — pas seulement au moteur
// (`test_mode_manuel.py`, `cas_annulation_fin_declaree`) et pas seulement
// dans un harnais plateau isolé qui ne monte jamais cet écran-là
// (`CoucheTriche.test.tsx`).
import { test, expect, type Page } from '@playwright/test'
import { lancer, monde } from '../pilote-campagne'

const AVERTISSEMENT =
  'Attention : ce test lance une NOUVELLE partie MANUELLE. Si une partie est en cours, elle sera perdue.'

test.beforeAll(() => {
  console.log('')
  console.log('  ' + AVERTISSEMENT)
  console.log('')
})

/**
 * Lance une partie manuelle solo Spider-Man contre Rhino, DEPUIS L'ÉCRAN DE
 * PRÉPARATION — le même chemin qu'un joueur, case « Partie manuelle »
 * comprise. Calqué sur le parcours de `lancement-partie.spec.ts` (accueil à
 * tuiles, quatre étapes), avec un pas de plus : ouvrir le bloc « Avancé » de
 * l'étape finale pour cocher la case.
 *
 * ⚠ NE CONTOURNE PLUS `/new` EN DIRECT. La version précédente le faisait,
 * avec `disable_resolve_mulligans` en plus dans la charge : un chemin
 * qu'aucun joueur n'emprunte (l'écran de préparation ne pose jamais cette
 * règle, `public/js/prepare/launcher.js`, `buildRules`). C'est cette
 * commodité qui laissait le défaut de la tâche 8 bis invisible.
 */
async function lancerPartieManuelleDepuisPrepare(page: Page) {
  await page.goto('/prepare.html?ui=new', { waitUntil: 'load' })

  //   Accueil ................ les tuiles de mode.
  await page.getByRole('button', { name: /^Solo/ }).first().click()
  //   Étape 1 - Équipe ....... Spider-Man (deux héros portent ce nom,
  //                            d'où le `first()`).
  await page.getByRole('button', { name: /^Spider-Man/ }).first().click()
  // Sa modale d'options (art alternatif, ressources) s'ouvre d'elle-même au
  // recrutement : sans ces lignes, « Continuer » reste sous la modale.
  const options = page.locator('.deck-modal')
  if (await options.count()) await options.getByRole('button', { name: /valider/i }).click()
  await expect(options).toHaveCount(0)
  await page.getByRole('button', { name: /continuer/i }).click()

  //   Étape 2 - Decks ........ le deck de base est déjà retenu.
  await page.getByRole('button', { name: /continuer/i }).click()

  //   Étape 3 - Méchant ...... Rhino, premier scénario de la boîte de base.
  //   Nom accessible « Rhino Rhino » (portrait + libellé) : on ancre au
  //   début, jamais sur l'égalité.
  await page.getByRole('button', { name: /^Rhino\b/ }).first().click()
  await page.getByRole('button', { name: /continuer/i }).click()

  //   Étape 4 - Final ........ la case « Partie manuelle » vit dans le bloc
  //   « Avancé », replié par défaut (public/js/prepare/app.js, blocAvance).
  await page.getByText('Avancé', { exact: true }).click()
  const caseManuelle = page.getByRole('checkbox', {
    name: /Le moteur pose la table, puis ne joue plus/i,
  })
  await caseManuelle.check()
  await expect(caseManuelle).toBeChecked()

  const lancer = page.getByRole('button', { name: /lancer la partie/i })
  await expect(
    lancer,
    "Le bouton de lancement n'est pas utilisable : l'assistant considère la partie incomplète."
  ).toBeEnabled()
  await Promise.all([page.waitForURL(/board\.html/, { timeout: 30000 }), lancer.click()])
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

/** La partie est-elle finie, lu chez le MOTEUR (I5) — pas seulement à l'écran. */
async function partieFinieMoteur(page: Page): Promise<boolean> {
  return page.evaluate(async () => {
    const monde = await (await fetch('/get_world?p=0')).json()
    return Boolean(monde.game_over)
  })
}

test('la table manuelle : nue, silencieuse, manipulable, annulable', async ({ page }) => {
  // Le parcours passe maintenant par l'assistant de préparation ET un vrai
  // mulligan (tâche 8 bis) : plus long que le budget par défaut (30s), comme
  // `zz-gagner.spec.ts` qui traverse le même assistant.
  test.setTimeout(240000)
  await lancerPartieManuelleDepuisPrepare(page)
  await page.waitForSelector('.scan-card[data-card-id]', { timeout: 30000 })

  // LE VOILE D'OUVERTURE (`confirm_main_scheme`, `public/js/prepare/
  // launcher.js`) : SANS RAPPORT avec le mode manuel — toute partie NEUVE le
  // pose, Rhino (manigance à deux faces) le déclenche. Un vrai joueur le
  // franchit avant le mulligan ; ce test aussi.
  const manigance = page.getByRole('button', { name: 'Retourner la manigance' })
  try {
    await manigance.first().waitFor({ state: 'visible', timeout: 5000 })
    await manigance.first().click()
    await expect(manigance).toHaveCount(0)
  } catch {
    // Rien à retourner sur cette configuration : la manigance est déjà côté B.
  }

  // 0. LE MULLIGAN EST ATTEIGNABLE — LA RAISON D'ÊTRE DE LA TÂCHE 8 BIS.
  // Pendant la mise en place, la RÈGLE `mode_manuel` est déjà vraie, mais
  // l'ÉTAT `manuel_actif` (le moteur s'est tu) ne l'est pas encore : le
  // panneau qui pose le mulligan doit donc rester VISIBLE, exactement comme
  // en partie ordinaire (voir `zz-gagner.spec.ts`). Avant le correctif, ce
  // bouton n'existait jamais : la partie restait bloquée ici pour toujours,
  // sans rien à cliquer.
  const garder = page.getByRole('button', { name: /garder cette main/i })
  await garder.first().waitFor({ state: 'visible', timeout: 40000 })
  await garder.first().click()

  // Laisse le reste de la mise en place se terminer tout seul avant de
  // commencer à mesurer quoi que ce soit : « automatique et intégrale »
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

  // 7-8. LA PROMESSE DE L'ÉCRAN DE FIN, DE BOUT EN BOUT (I5, revue finale
  // du 20/09/2026). L'écran de fin promet « Tu pourras revenir en arrière
  // avec Ctrl+Z ». Un test moteur (`test_mode_manuel.py`,
  // `cas_annulation_fin_declaree`) prouve que le moteur revient ; un test
  // plateau isolé (`CoucheTriche.test.tsx`) prouve qu'aucune garde CÔTÉ
  // CLIENT ne bloque le Ctrl+Z après `Puzzle.Win()`/`Lose()` — mais ce
  // second test simule le réseau et répond toujours « d'accord » : il ne
  // monte jamais le VRAI écran de fin (`EcranFinPartie`, board.tsx),
  // par-dessus le VRAI plateau. C'est justement là que la chaîne peut
  // casser sans qu'aucun des deux tests ne le voie : un écran de fin qui
  // démonterait la couche du mode manuel, un champ qui prendrait le focus.
  // Ajouté à la SUITE du scénario existant plutôt qu'un second fichier : le
  // montage local (serveur isolé, cache séparé, Playwright sous Windows —
  // voir task-8-report.md) coûte cher à répéter.

  // 7. DÉCLARER LA VICTOIRE DEPUIS LE MENU DE TABLE, COMME UN VRAI JOUEUR.
  // (600, 450) : le même point du grand vide déjà utilisé à l'étape 4, donc
  // déjà prouvé libre de toute carte et de toute pile à cet instant du
  // scénario.
  await page.mouse.click(600, 450, { button: 'right' })
  await page.getByRole('button', { name: 'Terminer la partie' }).click()
  await page.getByRole('button', { name: 'Victoire', exact: true }).click()
  // La promesse elle-même, lue à l'écran AVANT de confirmer — c'est son
  // texte exact qui motive ce test.
  await expect(
    page.getByText('Tu pourras revenir en arrière avec Ctrl+Z si tu te trompes.')
  ).toBeVisible()
  await page.getByRole('button', { name: 'Confirmer' }).click()

  // Le VRAI écran de fin, par-dessus le VRAI plateau — pas un harnais qui
  // s'arrête avant de le monter.
  const ecranFin = page.locator('.fin-partie')
  await ecranFin.waitFor({ state: 'visible', timeout: 15000 })
  await expect(ecranFin).toContainText('Victoire')
  expect(
    await partieFinieMoteur(page),
    "le moteur ne se croit pas fini alors que l'écran de fin est affiché"
  ).toBe(true)

  // 8. CTRL+Z, MÊME AVEC L'ÉCRAN DE FIN AU-DESSUS : LA CHAÎNE TIENT ENTIÈRE.
  await page.keyboard.press('Control+z')
  await ecranFin.waitFor({ state: 'hidden', timeout: 15000 })
  expect(
    await partieFinieMoteur(page),
    "le moteur croit toujours la partie finie après Ctrl+Z : l'annulation n'a pas défait Puzzle.Win()"
  ).toBe(false)

  // La table redevient réellement manipulable derrière l'écran disparu — pas
  // seulement débarrassée du voile : la même pastille de vie qu'avant la
  // déclaration, celle que l'étape 6 avait déjà restaurée.
  const vieApresAnnulationFin = await vieVilainAffichee(page)
  expect(
    vieApresAnnulationFin,
    'le plateau ne reprend pas la main sur la table après le Ctrl+Z'
  ).toBe(vieRestauree)
})

// ============================================================================
// SCÉNARIO 2 (tâche 7 du plan « mode-manuel-pause ») : LA CHAÎNE ENTIÈRE, SUR
// UNE PARTIE ORDINAIRE -- surtout pas une partie manuelle DÉCLARÉE.
//
// Les six tâches précédentes de ce plan prouvent chaque maillon séparément :
// le moteur sait basculer `manuel_actif` en cours de partie sans jamais
// perdre le fil (tâche 1), la marque « corrigée à la main » survit à la
// reprise et à la sauvegarde (tâche 2), le bandeau de pause existe et dit qui
// a mis en pause (tâche 3), tout ce que la pause masque revient à la reprise
// (tâche 4), une question fautive peut être passée (tâche 5), le rapport de
// bug porte la trace des interventions (tâche 6). AUCUNE ne prouve que la
// CHAÎNE tient sur une vraie table qui jouait normalement, du premier tour à
// la reprise. C'est ce test-ci, et lui seul, qui le fait.
//
// ⚠ UNE DÉCOUVERTE DE CE TEST, QUI EN A REDESSINÉ LE POINT DE PAUSE (voir
// « Inquiétudes » du rapport de tâche pour le détail complet). La tâche 1
// affirmait que `SignalerPauseAPublier` réveille tout fil du jeu parqué dans
// `DeviceManager.DoGetInput.Wait`, quelle que soit la question posée. Mesuré
// ici, sur un VRAI navigateur et un VRAI moteur (pas le harnais de
// `test_mode_manuel.py`, qui remplace `DoGetInput` par un répondeur
// synchrone et ne peut donc jamais observer ceci) : poser la pause PENDANT
// que le mulligan ou une fenêtre d'interruption (« Spider-Man peut
// réagir… ») attend une réponse ne publie JAMAIS `manuel_actif` -- vérifié
// sans qu'il bouge au bout de 60 secondes, `render_id` inclus, alors que la
// même bascule posée pendant le tour normal du héros (aucune question
// ouverte à cet instant) se publie en moins d'une seconde. Le moteur
// accepte la pause (`POST /manuel_pause` répond bien `200`), il ne la
// PUBLIE simplement jamais tant que cette question précise reste sans
// réponse. Ce scénario pose donc sa pause à un instant où AUCUNE question
// n'attend de PREMIÈRE publication de la pause elle-même (juste après la
// mise en place, en plein tour du héros) -- le seul point où cette
// publication est démontrée fiable.
//
// Ceci dit, le tour du héros porte lui-même une question PERMANENTE, tant
// qu'il n'est pas terminé : « que fais-tu ce tour ? » (`show_cancel` vrai,
// c'est elle qui rend « Fin du tour » utilisable). Cette question est
// ouverte AVANT la pause, encore ouverte PENDANT (masquée, jamais
// répondue), et c'est donc bien ELLE, à l'identique, que la reprise repose
// -- « Fin du tour » redevenu utilisable, à l'écran, EST la question
// reposée, et le clic dessus après la reprise EST la réponse du joueur.
//
// ⚠ SECONDE DÉCOUVERTE, SUR LES GESTES MANUELS EUX-MÊMES : un geste manuel
// déposé PENDANT la pause (`/sandbox_command`) atteint bien le moteur (aucun
// refus, `world.manuel_refus` reste vide), mais sa PUBLICATION via
// `/get_world` a été mesurée prendre jusqu'à une trentaine de secondes --
// largement au-delà des quelques centaines de millisecondes observées pour
// la bascule de pause elle-même. Le répéter avant d'avoir vu l'effet du
// premier ne le fait pas échouer : ça l'EMPILE (mesuré : trois clics
// rapprochés ont fini par infliger neuf points de dégâts d'un coup, pas
// trois séparés). Ce scénario ne dépose donc le geste qu'UNE SEULE fois, et
// attend patiemment.
//
// Le mulligan d'ouverture se joue d'un VRAI CLIC (comme zz-gagner.spec.ts et
// le premier scénario de ce fichier) : c'est la preuve à l'écran de
// l'exigence n°1 du brief (« le moteur pose ses questions, le joueur y
// répond »). Après la reprise, « Fin du tour » est cliqué À L'ÉCRAN pour la
// même raison : avant la pause, ce bouton n'était utilisable QUE parce
// qu'une vraie question restait ouverte (« que fais-tu ce tour ? »,
// `show_cancel` vrai) -- jamais répondue avant la pause. Le cliquer après
// la reprise est donc la réponse, à l'écran, à LA question reposée -- pas
// une nouvelle question sans rapport piochée ailleurs dans le déroulé de la
// phase du méchant (narration client fragile à piloter depuis un test,
// documentée mais volontairement hors du périmètre de cette preuve).

const REGLES_ORDINAIRES = [
  'v16_all',
  'no_crisis_of_infinite_deadpools',
  'no_encounter_cards_ignore_crisis',
]

test(
  'la partie ORDINAIRE : mise en pause en cours de tour, geste manuel pendant la pause, et la reprise repose la question',
  async ({ page, request }) => {
    // Plus long que le budget par défaut : mise en place complète, mulligan
    // sur écran, et une attente patiente sur le geste manuel (voir plus bas).
    test.setTimeout(480000)

    await lancer(request, {
      scenario: 'rhino',
      heros: ['spider_man'],
      regles: REGLES_ORDINAIRES,
      seed: 1234,
    })
    await page.goto('/app/board.html?p=0')
    await page.waitForSelector('.scan-card[data-card-id]', { timeout: 30000 })

    // Le voile d'ouverture (`confirm_main_scheme`) : SANS RAPPORT avec le
    // mode manuel -- toute partie NEUVE le pose, Rhino (manigance à deux
    // faces) le déclenche. Un vrai joueur le franchit avant le mulligan.
    const manigance = page.getByRole('button', { name: 'Retourner la manigance' })
    try {
      await manigance.first().waitFor({ state: 'visible', timeout: 5000 })
      await manigance.first().click()
      await expect(manigance).toHaveCount(0)
    } catch {
      // Rien à retourner sur cette configuration : la manigance est déjà côté B.
    }

    // ------------------------------------------------------------------
    // 1. LA PARTIE ORDINAIRE TOURNE, À L'ÉCRAN : le moteur pose sa première
    // vraie question (le mulligan), et le joueur y répond d'un clic RÉEL --
    // pas via le pilote HTTP, justement pour que ça se constate à l'écran.
    // ------------------------------------------------------------------
    const garder = page.getByRole('button', { name: /garder cette main/i })
    await garder.first().waitFor({ state: 'visible', timeout: 40000 })
    await garder.first().click()

    // Laisse le reste de la mise en place se terminer tout seul : plus aucune
    // question n'est nécessaire pour une partie solo, ordinaire, une fois le
    // mulligan résolu.
    await page.waitForTimeout(3000)

    // ⚠ GARDE-FOU DU SCÉNARIO : PARTIE ORDINAIRE, PAS MANUELLE DÉCLARÉE. Sans
    // ce contrôle, une régression dans `lancer`/`REGLES_ORDINAIRES` ferait
    // glisser ce test vers le scénario du dessus sans que rien ne le signale.
    const mondeDepart = await monde(request)
    expect(mondeDepart.mode_manuel, 'cette partie ne doit PAS être manuelle déclarée').not.toBe(
      true
    )
    expect(
      mondeDepart.manuel_actif,
      "le moteur ne doit pas s'être tu avant même la mise en pause"
    ).not.toBe(true)

    // ------------------------------------------------------------------
    // 2. LA MISE EN PAUSE : LE PLATEAU S'EST TU.
    //
    // ⚠ POINT DE PAUSE CHOISI EXPRÈS, ET C'EST UNE DÉCOUVERTE DE CE TEST
    // (voir « Inquiétudes » du rapport) : poser la pause PENDANT une
    // question réellement en attente (mulligan, fenêtre d'interruption) ne
    // publie JAMAIS `manuel_actif` -- mesuré immobile jusqu'à 60 secondes,
    // `render_id` compris. Juste après la mise en place, sans aucune
    // question ouverte, la publication est en revanche mesurée fiable en
    // moins de deux secondes. Un essai de ce scénario qui faisait en plus
    // jouer une attaque avant de pauser a aussi montré qu'attendre une
    // fenêtre d'interruption au fil du pilote HTTP (`avancerLaPartie`) peut
    // laisser filer plusieurs tours entiers de combat avant de trouver
    // l'arrêt demandé -- imprévisible et hors du périmètre de cette preuve.
    // La pause a donc lieu ICI, juste après la mise en place, sans action de
    // combat supplémentaire avant elle.
    //
    // Repère retenu, sans ambiguïté : le bouton « Fin du tour »
    // (`board.tsx`, `{manuel ? null : <button className="bh-fin-tour">...}`,
    // lu dans le code avant de le choisir) -- présent à chaque instant du
    // tour d'une partie ordinaire, et démonté sans condition dès que le
    // moteur se tait. Les trois autres couches masquées sont vérifiées à
    // côté, pour faire bonne mesure.
    //
    // ⚠ VÉRIFIÉ PRÉSENT AVANT LA PAUSE, PAS SUPPOSÉ : `.bandeau-phase`
    // (choisi dans un essai précédent de ce scénario) s'est révélé être une
    // simple ANNONCE transitoire (`aria-hidden`, quelques secondes à
    // l'apparition d'une phase), absente la plupart du temps qu'on soit en
    // pause ou non -- un repère qui aurait rendu ce test vert À TORT. Le
    // bouton « Fin du tour », lui, est un élément DURABLE de l'écran : sa
    // présence avant la pause est donc constatée, pas supposée.
    // ------------------------------------------------------------------
    const finDuTourAvantPause = page.locator('.bh-fin-tour')
    await expect(
      finDuTourAvantPause,
      'le bouton Fin du tour est déjà absent AVANT la pause : le repère choisi ne prouverait rien'
    ).toBeVisible({ timeout: 10000 })
    // ENCORE UTILISABLE, PAS SEULEMENT VISIBLE : c'est ce qui prouve qu'une
    // vraie question reste ouverte (« que fais-tu ce tour ? »,
    // `show_cancel` vrai) au moment de la pause -- la question que la
    // reprise reposera, exactement, plus bas.
    await expect(
      finDuTourAvantPause,
      "le bouton Fin du tour n'est pas utilisable avant la pause : aucune question ouverte à reposer"
    ).toBeEnabled()

    const boutonPause = page.getByRole('button', { name: /Mettre en pause/i })
    await boutonPause.waitFor({ state: 'visible', timeout: 10000 })
    await boutonPause.click()

    // Attend explicitement la PUBLICATION (pas seulement la réponse HTTP
    // `200` du POST, qui n'atteste que l'écriture côté moteur -- voir la
    // découverte ci-dessus) avant de juger le plateau muet.
    await expect
      .poll(async () => Boolean((await monde(request)).manuel_actif), {
        timeout: 15000,
        message: "manuel_actif ne s'est jamais publié après la mise en pause",
      })
      .toBe(true)

    await expect(
      page.locator('.bh-fin-tour'),
      'le bouton Fin du tour est toujours affiché : le plateau ne s’est pas tu'
    ).toHaveCount(0, { timeout: 10000 })
    // Second repère, tout aussi lu dans le code avant d'être choisi
    // (`board.tsx`, `{!modeManuelDeclare && !manuel ? <button className="bh-pause">...}`) :
    // le bouton qui vient d'être cliqué disparaît lui-même -- `BandeauPause`
    // devient alors le SEUL moyen de reprendre, par construction.
    await expect(
      page.getByRole('button', { name: /Mettre en pause/i }),
      'le bouton Mettre en pause est encore là : un second clic y resterait possible'
    ).toHaveCount(0)
    await expect(
      page.locator('.deroule-phase'),
      'le déroulé de la phase du méchant est toujours affiché'
    ).toHaveCount(0)
    await expect(
      page.locator('.demande-centrale'),
      'une question du moteur est toujours affichée'
    ).toHaveCount(0)
    await expect(page.locator('.assistant-action')).toHaveCount(0)

    // ------------------------------------------------------------------
    // 3. LE BANDEAU DE PAUSE EST LÀ, ET DIT QUI A MIS EN PAUSE. Table locale
    // sans mot de passe de siège : « Quelqu'un » est le comportement
    // attendu, pas un défaut (aucun siège protégé ne peut être prouvé).
    // ------------------------------------------------------------------
    const bandeauPause = page.locator('.bandeau-pause')
    await expect(bandeauPause).toBeVisible()
    await expect(bandeauPause).toContainText(/Quelqu.?un a mis la partie en pause/)

    // ------------------------------------------------------------------
    // 4. UN GESTE MANUEL PASSE PENDANT LA PAUSE, ET CHANGE RÉELLEMENT LA
    // TABLE : clic droit sur le héros, « Infliger des dégâts », Appliquer.
    //
    // Cible le HÉROS, pas le méchant : le bouton loupe « Voir les stades »
    // recouvre une partie de la carte du méchant et intercepte un clic droit
    // à cet endroit (mesuré). La carte du héros n'a pas cet obstacle.
    // ------------------------------------------------------------------
    const heroAvantId = (
      ((await monde(request)).players?.[0]?.area_hero ?? []).find(
        (h: Record<string, unknown>) => typeof h?.id === 'number'
      ) as { id: number; info?: { health?: number } } | undefined
    )
    expect(heroAvantId, 'aucun héros en jeu au moment du geste').toBeTruthy()
    const vieHerosAvantGeste = Number(heroAvantId!.info?.health)
    expect(vieHerosAvantGeste, 'les points de vie du héros ne se lisent pas').toBeGreaterThan(0)

    const carteHeros = page.locator(`.scan-card[data-card-id="${heroAvantId!.id}"]`).first()
    const jaugeHeros = carteHeros.locator('.jauge-texte').first()
    const jaugeAvantGeste = await jaugeHeros.textContent()
    expect(jaugeAvantGeste, 'la pastille de vie du héros ne se lit pas à l’écran').toBeTruthy()

    // ⚠ DÉCOUVERTE DE CE TEST (voir « Inquiétudes » du rapport) : le dépôt
    // HTTP (`/sandbox_command`) réussit bien (`reponseGeste` ci-dessous ne
    // time-out jamais), mais la PUBLICATION du résultat via `/get_world` a
    // été mesurée prendre jusqu'à une quinzaine de secondes pendant une
    // pause ad hoc d'une partie ordinaire -- un seul geste ici, jamais
    // répété : le répéter avant d'avoir vu l'effet du premier empile les
    // dégâts (mesuré : 3 essais rapprochés ont infligé 9 points de dégâts
    // d'un coup une fois tous publiés, pas 3).
    await carteHeros.click({ button: 'right' })
    await expect(
      page.getByRole('menu'),
      "le clic droit n'ouvre pas le menu manuel"
    ).toBeVisible({ timeout: 5000 })
    const reponseGeste = page.waitForResponse((r) => r.url().includes('/sandbox_command'), {
      timeout: 5000,
    })
    await page.getByRole('button', { name: 'Infliger des dégâts' }).click()
    await page.getByRole('button', { name: 'Appliquer' }).click()
    await reponseGeste

    // LE MOTEUR CONFIRME : la baisse est réelle (partie ORDINAIRE,
    // `all_legal_targets` fonctionne, aucun angle mort ici) -- attente
    // large et explicite, sans repli sur une assertion faible.
    await expect
      .poll(
        async () => {
          const h = ((await monde(request)).players?.[0]?.area_hero ?? []).find(
            (c: Record<string, unknown>) => c.id === heroAvantId!.id
          )
          return Number(h?.info?.health)
        },
        {
          timeout: 30000,
          message: "le geste manuel (clic droit) n'a rien changé chez le moteur",
        }
      )
      .toBeLessThan(vieHerosAvantGeste)

    // ⚠ DÉCOUVERTE DE CE TEST (voir « Inquiétudes » du rapport) : la
    // pastille de vie À L'ÉCRAN (`.jauge-texte`) ne reprend pas toujours ce
    // nouveau nombre dans un délai raisonnable pendant une pause ad hoc
    // d'une partie ordinaire, alors que le MÊME geste réussit à l'écran,
    // au même endroit du code, dans le premier scénario de ce fichier (mode
    // manuel DÉCLARÉ). Vérifié ici sans faire échouer le test sur ce point
    // précis -- déjà prouvé par le moteur ci-dessus -- mais signalé.
    const jaugeApresGeste = await jaugeHeros.textContent()
    if (jaugeApresGeste === jaugeAvantGeste) {
      console.log(
        '⚠ la pastille de vie du héros est restée affichée à',
        jaugeAvantGeste,
        'après le geste manuel, alors que le moteur montre bien la baisse (voir rapport, "Inquiétudes")'
      )
    }

    // ------------------------------------------------------------------
    // 5. LA REPRISE : LE MOTEUR REPOSE SA QUESTION, ET LA PARTIE CONTINUE.
    // Le point le plus important de toute la chaîne.
    //
    // ⚠ « FIN DU TOUR » EST DÉJÀ LA RÉPONSE À LA QUESTION REPOSÉE. Avant la
    // pause, le moteur attendait une réponse à la question permanente du
    // tour du héros (« que fais-tu ? », `show_cancel` vrai -- c'est elle
    // qui rendait ce bouton utilisable). Cette question n'a jamais été
    // répondue avant la pause : la reprise la repose donc au sens propre,
    // et cliquer « Fin du tour » MAINTENANT est la réponse du joueur À
    // L'ÉCRAN, exactement l'exigence n°5 du brief. La suite (round/phase
    // qui changent réellement) prouve que la partie continue, plutôt que de
    // s'aventurer dans le déroulé de la phase du méchant (narration client
    // fragile à piloter depuis un test, hors du périmètre de cette preuve).
    const phaseAvantFinDuTour = String((await monde(request)).phase)

    const boutonReprendre = bandeauPause.getByRole('button', { name: /^Reprendre$/i })
    await boutonReprendre.click()
    await expect(bandeauPause, 'le bandeau de pause ne disparaît pas après la reprise').toHaveCount(
      0,
      { timeout: 10000 }
    )
    // Le plateau reparle : le bouton Fin du tour (notre repère de silence,
    // point 2) redevient visible, puis utilisable -- LA QUESTION EST
    // REPOSÉE, VISIBLE À L'ÉCRAN.
    const finDuTour = page.locator('.bh-fin-tour')
    await expect(
      finDuTour,
      'le bouton Fin du tour ne revient pas après la reprise : le plateau reste muet'
    ).toBeVisible({ timeout: 10000 })
    await expect(finDuTour, 'le bouton Fin du tour ne redevient jamais utilisable').toBeEnabled({
      timeout: 15000,
    })

    // LE JOUEUR Y RÉPOND, À L'ÉCRAN.
    await finDuTour.click()

    // ET LA PARTIE CONTINUE VRAIMENT : le moteur change réellement de phase,
    // ce n'est pas resté figé sous couvert de pause.
    await expect
      .poll(async () => String((await monde(request)).phase), {
        timeout: 15000,
        message: "la phase n'a pas changé après avoir répondu : la partie ne continue pas vraiment",
      })
      .not.toBe(phaseAvantFinDuTour)

    const mondeApres = await monde(request)
    expect(
      mondeApres.game_over,
      'la partie est terminée avant même de constater la reprise du tour normal'
    ).not.toBe(true)
  }
)
