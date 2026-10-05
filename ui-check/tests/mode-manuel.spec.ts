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
  const caseManuelle = page.getByRole('radio', {
    name: /Manuel façon OCTGN/i,
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
  // Le voile se franchit en deux clics : « Retourner la manigance », puis « OK ».
  const voile = page.getByRole('dialog').getByRole('button')
  try {
    await voile.first().waitFor({ state: 'visible', timeout: 5000 })
    for (let i = 0; i < 3 && (await voile.count()) > 0; i++) {
      await voile.first().click()
      await page.waitForTimeout(800)
    }
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
  const garder = page.getByRole('button', { name: /garder (?:cette|ma) main/i })
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
// ⚠ LE POINT DE PAUSE A ÉTÉ DÉPLACÉ (tâche 8, 20/09/2026), ET C'EST TOUTE
// L'HISTOIRE DE CE TEST. La première version de ce scénario posait sa pause
// juste après la mise en place, en plein tour du héros -- le SEUL instant
// où la publication marchait, donc le moins représentatif qui soit. Elle le
// faisait faute de mieux : elle avait mesuré, sur un VRAI navigateur et un
// VRAI moteur, que poser la pause PENDANT que le mulligan ou une fenêtre
// d'interruption attend une réponse ne publiait JAMAIS `manuel_actif`
// (immobile au bout de 60 secondes, `render_id` compris), alors que le
// `POST /manuel_pause` répondait bien `200`.
//
// Cette mesure était exacte, et le diagnostic qui a suivi en a donné la
// cause à la ligne : le fil du jeu se réveillait bien et reposait bien la
// même question, mais PERSONNE ne produisait de rendu sur ce chemin -- le
// seul rendu possible, `SenderPlayer.PlayerOnEvent_Text`, n'appelle
// `Present` que pour un `Message.WhenPlayerInTurn`. D'où le tour du héros
// qui publiait et tout le reste qui se taisait. `Controller.ChoiceOne`
// force désormais ce rendu quand il rend la main sans entrée pour une cause
// qui a muté le monde (une bascule de pause, un geste manuel drainé --
// jamais une expiration de minuterie).
//
// Ce scénario pose donc maintenant sa pause LÀ OÙ UN JOUEUR LA POSERAIT :
// pendant le MULLIGAN, une question ouverte qui le bloque, exactement le
// cas qui ne marchait pas. C'est la seule façon d'empêcher ce défaut de
// revenir : le test ne prouve quelque chose que s'il échoue quand le
// correctif disparaît.
//
// Ce que la reprise repose est donc LE MULLIGAN LUI-MÊME, à l'identique :
// « Garder cette main » réapparaît à l'écran, et le clic dessus est la
// réponse du joueur à LA question qui était restée ouverte pendant toute la
// pause. Rien à déduire, rien à supposer : le même panneau, avant et après.
//
// ⚠ LES GESTES MANUELS PENDANT LA PAUSE RELÈVENT DE LA MÊME FAMILLE, et le
// correctif les couvre : un geste déposé pendant la pause
// (`/sandbox_command`) atteignait bien le moteur, mais sa publication avait
// été mesurée prendre jusqu'à une trentaine de secondes -- la branche
// `DrainSandboxCommands` de `DoGetInput` rendait elle aussi la main sans
// forcer de rendu. Elle arme désormais le même marqueur. Le geste n'est
// malgré tout déposé qu'UNE SEULE FOIS ici : le répéter avant d'avoir vu
// l'effet du premier ne le fait pas échouer, ça l'EMPILE (mesuré : trois
// clics rapprochés ont fini par infliger neuf points de dégâts d'un coup).
//
// ⚠ LA PREUVE DU GESTE SE LIT À L'ÉCRAN (`.jauge-texte`), JAMAIS DANS
// `/get_world`. Ce point de terminaison ne calcule `info.health` que pour
// les cartes visées par une action légale du moment (`all_legal_targets`) :
// pendant le mulligan, les seules options du moteur sont des cartes de la
// main, aucun personnage n'y est visé, et `info` revient donc vide QUE le
// geste ait porté ou non. Un silence qui ne dit rien. C'est le plateau
// réellement dessiné au joueur qui tranche -- règle du projet, étape 8 bis
// de PROCESSUS-CARTE.

const REGLES_ORDINAIRES = [
  'v16_all',
  'no_crisis_of_infinite_deadpools',
  'no_encounter_cards_ignore_crisis',
]

test(
  'la partie ORDINAIRE : mise en pause PENDANT une question ouverte (le mulligan), geste manuel, et la reprise repose cette même question',
  async ({ page, request }) => {
    // Plus long que le budget par défaut : mise en place complète, pause
    // posée sur le mulligan, et une attente patiente sur le geste manuel
    // (voir plus bas).
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
    // Le voile se franchit en deux clics : « Retourner la manigance », puis « OK ».
    const voile = page.getByRole('dialog').getByRole('button')
    try {
      await voile.first().waitFor({ state: 'visible', timeout: 5000 })
      for (let i = 0; i < 3 && (await voile.count()) > 0; i++) {
        await voile.first().click()
        await page.waitForTimeout(800)
      }
    } catch {
      // Rien à retourner sur cette configuration : la manigance est déjà côté B.
    }

    // ------------------------------------------------------------------
    // 1. LE MOTEUR POSE UNE VRAIE QUESTION, ET ELLE BLOQUE LE JOUEUR : le
    // MULLIGAN. On l'attend, et on n'y répond PAS -- c'est tout l'objet de
    // ce scénario depuis la tâche 8. Un joueur ne met pas la table en pause
    // dans le calme entre deux tours : il la met en pause parce qu'il est
    // coincé sur une question, et c'est précisément ce cas-là qui ne
    // marchait pas.
    // ------------------------------------------------------------------
    const garder = page.getByRole('button', { name: /garder (?:cette|ma) main/i })
    await garder.first().waitFor({ state: 'visible', timeout: 40000 })

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
    // 2. LA MISE EN PAUSE, PENDANT CETTE QUESTION : LE PLATEAU SE TAIT.
    //
    // ⚠ C'EST LE CAS QUI ÉTAIT ROUGE, ET C'EST POUR ÇA QU'IL EST ICI. Tant
    // que `Controller.ChoiceOne` ne forçait pas son rendu, la bascule était
    // bien enregistrée par le moteur (`POST /manuel_pause` -> `200`) mais
    // jamais publiée : `/get_world` servait la trame précédente, immobile au
    // bout de 60 secondes, `render_id` compris. Si ce correctif disparaît,
    // l'attente de publication ci-dessous expire -- c'est exactement ce
    // qu'on demande à ce test de faire.
    //
    // Deux repères, tous deux lus dans le code avant d'être choisis :
    //  - le panneau du MULLIGAN lui-même (« Garder cette main ») : la
    //    question ouverte, constatée à l'écran juste avant la pause, et qui
    //    doit disparaître avec le reste ;
    //  - le bouton « Fin du tour » (`board.tsx`,
    //    `{manuel ? null : <button className="bh-fin-tour">...}`), élément
    //    DURABLE de la barre du haut d'une partie ordinaire, démonté sans
    //    condition dès que le moteur se tait.
    //
    // ⚠ NI L'UN NI L'AUTRE N'EST SUPPOSÉ PRÉSENT : `.bandeau-phase`, choisi
    // dans un essai précédent de ce scénario, s'est révélé n'être qu'une
    // ANNONCE transitoire (`aria-hidden`, quelques secondes), absente la
    // plupart du temps qu'on soit en pause ou non -- un repère qui aurait
    // rendu ce test vert À TORT. Les deux repères retenus sont donc
    // constatés à l'écran avant le clic.
    // ------------------------------------------------------------------
    const finDuTourAvantPause = page.locator('.bh-fin-tour')
    await expect(
      finDuTourAvantPause,
      'le bouton Fin du tour est déjà absent AVANT la pause : le repère choisi ne prouverait rien'
    ).toBeVisible({ timeout: 10000 })
    await expect(
      garder.first(),
      'le panneau du mulligan a disparu avant la pause : plus aucune question ouverte à reposer'
    ).toBeVisible()

    const boutonPause = page.getByRole('button', { name: 'Mode manuel', exact: true })
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
      page.getByRole('button', { name: 'Mode manuel', exact: true }),
      "l'interrupteur n'affiche pas Manuel comme actif après la pause"
    ).toHaveAttribute('aria-pressed', 'true')
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
    // 3. L'INTERRUPTEUR MONTRE « MANUEL » ET AUCUN BANDEAU NE S'AFFICHE.
    // ------------------------------------------------------------------
    await expect(page.getByRole('button', { name: 'Mode manuel', exact: true })).toHaveAttribute('aria-pressed', 'true')
    await expect(page.locator('.bandeau-pause')).toHaveCount(0)

    // ------------------------------------------------------------------
    // 4. UN GESTE MANUEL PASSE PENDANT LA PAUSE, ET CHANGE RÉELLEMENT LA
    // TABLE : clic droit sur le héros, « Infliger des dégâts », Appliquer.
    //
    // Cible le HÉROS, pas le méchant : le bouton loupe « Voir les stades »
    // recouvre une partie de la carte du méchant et intercepte un clic droit
    // à cet endroit (mesuré). La carte du héros n'a pas cet obstacle.
    //
    // ⚠ LA PREUVE SE LIT À L'ÉCRAN, PAS DANS `/get_world` -- et ce n'est pas
    // un repli, c'est le seul endroit où elle existe ici (voir l'en-tête de
    // ce scénario) : pendant le mulligan, les seules options du moteur sont
    // des cartes de la main, donc `all_legal_targets` ne vise aucun
    // personnage et `info.health` revient vide QUE le geste ait porté ou
    // non. La pastille de vie réellement dessinée, elle, tranche.
    // ------------------------------------------------------------------
    const heroAvantId = (
      ((await monde(request)).players?.[0]?.area_hero ?? []).find(
        (h: Record<string, unknown>) => typeof h?.id === 'number'
      ) as { id: number } | undefined
    )
    expect(heroAvantId, 'aucun héros en jeu au moment du geste').toBeTruthy()

    const carteHeros = page.locator(`.scan-card[data-card-id="${heroAvantId!.id}"]`).first()
    const jaugeHeros = carteHeros.locator('.jauge-texte').first()
    const jaugeAvantGeste = await jaugeHeros.textContent()
    // ⚠ LA VALEUR ATTENDUE, PAS « PAS LA MÊME » (ronde de correction 1) :
    // un simple `.not.toBe(avant)` accepterait n'importe quel changement, y
    // compris un passage à `null` si la carte se démontait. La pastille est
    // écrite `courants / max` (`card-model.ts`), et la quantité de dégâts est
    // LUE dans le champ du menu juste avant d'appliquer (voir plus bas)
    // plutôt que devinée : la deviner à 1 a rendu ce test rouge au premier
    // essai, `MenuTriche.tsx` proposant 3.
    const pv = /^\s*(\d+)\s*\/\s*(\d+)\s*$/.exec(jaugeAvantGeste ?? '')
    expect(
      pv,
      `la pastille de vie du héros ne se lit pas à l’écran (lu : ${JSON.stringify(jaugeAvantGeste)})`
    ).toBeTruthy()

    // UN SEUL DÉPÔT, JAMAIS RÉPÉTÉ : `/sandbox_command` réussit toujours,
    // c'est la publication qui se faisait attendre (jusqu'à une trentaine
    // de secondes avant le correctif de la tâche 8, la branche
    // `DrainSandboxCommands` de `DoGetInput` rendant elle aussi la main
    // sans forcer de rendu). Répéter le geste avant d'avoir vu l'effet du
    // premier ne le fait pas échouer : ça l'EMPILE (mesuré : trois clics
    // rapprochés ont fini par infliger neuf points de dégâts d'un coup).
    await carteHeros.click({ button: 'right' })
    await expect(
      page.getByRole('menu'),
      "le clic droit n'ouvre pas le menu manuel"
    ).toBeVisible({ timeout: 5000 })
    await page.getByRole('button', { name: 'Infliger des dégâts' }).click()

    // La quantité proposée par le menu EST celle qui sera appliquée : on la
    // lit à l'écran plutôt que de la recopier depuis le code, pour que ce
    // test n'ait pas à être retouché le jour où elle change.
    const champDegats = page.locator('.menu-triche-saisie input[type="number"]')
    const degats = Number(await champDegats.inputValue())
    expect(degats, 'la quantité de dégâts proposée par le menu ne se lit pas').toBeGreaterThan(0)
    const jaugeAttendue = `${Number(pv![1]) - degats} / ${pv![2]}`

    const reponseGeste = page.waitForResponse((r) => r.url().includes('/sandbox_command'), {
      timeout: 5000,
    })
    await page.getByRole('button', { name: 'Appliquer' }).click()
    await reponseGeste

    // LE PLATEAU LE MONTRE : la pastille de vie du héros affiche exactement
    // le point de vie en moins. Attente large et explicite, sans repli sur
    // une assertion faible.
    await expect
      .poll(async () => jaugeHeros.textContent(), {
        timeout: 30000,
        message:
          "la pastille de vie du héros n'affiche pas le dégât infligé : le geste manuel n'a pas été publié pendant la pause",
      })
      .toBe(jaugeAttendue)

    // ------------------------------------------------------------------
    // 5. LA REPRISE : LE MOTEUR REPOSE SA QUESTION, ET LA PARTIE CONTINUE.
    // Le point le plus important de toute la chaîne.
    //
    // ⚠ LA QUESTION REPOSÉE EST LE MULLIGAN LUI-MÊME. Il était ouvert avant
    // la pause, il est resté ouvert pendant (masqué, jamais répondu) : sa
    // réapparition à l'écran EST la re-pose, et le clic sur « Garder cette
    // main » EST la réponse du joueur. Rien à déduire d'un bouton voisin --
    // le même panneau, avant et après.
    const phaseAvantReponse = String((await monde(request)).phase)

    const boutonReprendre = page.getByRole('button', { name: 'Mode automatique', exact: true })
    await boutonReprendre.click()
    await expect(
      page.getByRole('button', { name: 'Mode automatique', exact: true }),
      'l’interrupteur ne repasse pas sur Auto après la reprise'
    ).toHaveAttribute('aria-pressed', 'true', { timeout: 10000 })
    // Le plateau reparle : le bouton Fin du tour (notre repère de silence,
    // point 2) redevient visible...
    await expect(
      page.locator('.bh-fin-tour'),
      'le bouton Fin du tour ne revient pas après la reprise : le plateau reste muet'
    ).toBeVisible({ timeout: 10000 })
    // ... et LA QUESTION EST REPOSÉE, VISIBLE À L'ÉCRAN : le mulligan.
    await expect(
      garder.first(),
      'le panneau du mulligan ne revient pas après la reprise : la question ouverte a été perdue'
    ).toBeVisible({ timeout: 15000 })

    // LE JOUEUR Y RÉPOND, À L'ÉCRAN.
    await garder.first().click()

    // ET LA PARTIE CONTINUE VRAIMENT : la mise en place s'achève et le
    // moteur change réellement de phase, ce n'est pas resté figé sous
    // couvert de pause.
    await expect
      .poll(async () => String((await monde(request)).phase), {
        timeout: 30000,
        message: "la phase n'a pas changé après avoir répondu : la partie ne continue pas vraiment",
      })
      .not.toBe(phaseAvantReponse)

    const mondeApres = await monde(request)
    expect(
      mondeApres.game_over,
      'la partie est terminée avant même de constater la reprise du tour normal'
    ).not.toBe(true)
  }
)
