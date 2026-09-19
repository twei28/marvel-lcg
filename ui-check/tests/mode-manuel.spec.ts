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
import { test, expect, type Page } from '@playwright/test'

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
})
