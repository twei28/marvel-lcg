// LA PHASE DU MÉCHANT « Sur la table », DE A À Z.
//
// ⚠ POURQUOI CE FICHIER EXISTE. Le défaut « ça continue tout seul sans que je
// mette suivant » a été signalé TROIS FOIS le 14/09/2026, et corrigé trois fois
// sur trois causes différentes. À chaque fois j'avais vérifié LE MORCEAU que je
// venais d'écrire, jamais le déroulé. Reproche de l'utilisateur, textuel :
// « on dirait que tu ne vérifies pas et que tu ne vas pas jusqu'au bout des
// choses. Ce n'est pas vérifier de A à Z. »
//
// Ce test parcourt une phase ENTIÈRE, et à chaque étape :
//   1. il ATTEND sans rien toucher, et vérifie que RIEN n'a bougé ;
//   2. il clique une fois, et vérifie que l'étape a changé ;
//   3. il compte ce qui s'affiche au centre, pour qu'aucun panneau ne s'empile.
//
//   npm run phase-sur-table
//
// ⚠ IL NE LANCE AUCUNE PARTIE : il lit un état enregistré (`?etat=`), donc il
// ne détruit rien et peut tourner à tout moment.
import { test, expect, type Page } from '@playwright/test'

const ETAT = 'rhino__spider_man__phase-mechant-complet.js'
/** Le temps d'observation sans toucher à rien. Plus long que tous nos délais. */
const ATTENTE_MS = 5000

async function ouvrirLaPhase(page: Page, avanceAuto = false) {
  await page.goto('/get_version')
  await page.goto('/main.html')
  await page.evaluate((auto) => {
    localStorage.setItem('marvel-langue-choisie', '1')
    // ⚠ LE RÉGLAGE QUI A CAUSÉ LE DÉFAUT UNE PREMIÈRE FOIS. « Avance toute
    // seule » était grisé hors du mode Détaillé, mais sa VALEUR s'appliquait
    // quand même : griser ne désactive pas. Le mettre sur « on » ici est donc
    // le témoin de cette cause-là, et non un réglage de confort.
    localStorage.setItem('marvel-board-avance-auto', auto ? 'on' : 'off')
  }, avanceAuto)
  // La garde des essais : c'est le SERVEUR qui décide en vrai, on la force ici
  // pour que le test n'ait pas besoin d'un compte administrateur.
  await page.route('**/get_site_admin', (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ url: 'test' }) })
  )
  await page.goto(`/app/board.html?phase=sur-table&etat=${ETAT}`)
  await page.waitForSelector('.plateau-scene', { timeout: 30000 })
  // Le bandeau d'ouverture joue SEUL : la première étape ne paraît qu'après.
  await page.waitForSelector('.deroule-rond', { timeout: 15000 })
}

/** Ce que le joueur lit en ce moment. */
const phraseCourante = (page: Page) =>
  page.locator('.deroule-recit').first().innerText().catch(() => '')

test('⚠ RIEN n’avance sans un clic, du premier temps au dernier', async ({ page }) => {
  // Huit étapes × cinq secondes d'observation : ce test est lent PAR NATURE.
  // C'est le prix de la seule question qu'il pose, et elle vaut la minute.
  test.setTimeout(180000)
  await ouvrirLaPhase(page)

  const vues: string[] = []
  for (let etape = 0; etape < 8; etape += 1) {
    const avant = await phraseCourante(page)
    if (!avant) break
    vues.push(avant)

    // 1. ON NE TOUCHE À RIEN. C'est le cœur du test.
    await page.waitForTimeout(ATTENTE_MS)
    const apresAttente = await phraseCourante(page)
    expect(
      apresAttente,
      `l'étape a changé TOUTE SEULE après ${ATTENTE_MS} ms : « ${avant} » est devenu « ${apresAttente} »`
    ).toBe(avant)

    // 2. UN CLIC, UNE ÉTAPE.
    const bouton = page.locator('.deroule-rond')
    if ((await bouton.count()) === 0) break
    await bouton.first().click()
    await page.waitForTimeout(1500)
    const apresClic = await phraseCourante(page)
    if (apresClic === avant) break // dernière étape connue de la fixture
  }

  // Une phase du méchant a au moins la menace, une activation et une révélation.
  expect(vues.length, `seulement ${vues.length} étape(s) parcourue(s)`).toBeGreaterThanOrEqual(3)
  // Aucune étape ne doit être passée deux fois de suite : ce serait le signe
  // d'un clic qui n'avance pas, l'inverse du défaut ci-dessus.
  for (let i = 1; i < vues.length; i += 1) {
    expect(vues[i], `l'étape ${i} répète la précédente`).not.toBe(vues[i - 1])
  }
})

test('⚠ jamais deux panneaux au centre en même temps', async ({ page }) => {
  await ouvrirLaPhase(page)

  for (let etape = 0; etape < 8; etape += 1) {
    // Tout ce qui peut occuper le centre : le cartouche du déroulé, le panneau
    // du moteur, le sélecteur de cibles.
    const panneaux = await page
      .locator('.deroule-phase:visible, .demande-centrale:visible, .cibles-scene:visible')
      .count()
    const phrase = await phraseCourante(page)
    expect(panneaux, `${panneaux} panneaux empilés sur « ${phrase} »`).toBeLessThanOrEqual(1)

    const bouton = page.locator('.deroule-rond')
    if ((await bouton.count()) === 0) break
    await bouton.first().click()
    await page.waitForTimeout(1200)
  }
})

test('⚠ même avec « Avance toute seule » ALLUMÉE, rien ne bouge sur la table', async ({ page }) => {
  // LA PREMIÈRE DES TROIS CAUSES du « ça continue tout seul », re-vérifiée en
  // jeu le 14/09/2026 : le réglage était grisé hors du mode Détaillé, mais sa
  // valeur continuait de s'appliquer. Un réglage grisé doit AUSSI être sans
  // effet, et c'est `avanceAutoActive` (board.tsx) qui le garantit.
  test.setTimeout(90000)
  await ouvrirLaPhase(page, true)

  const avant = await phraseCourante(page)
  expect(avant, 'aucune étape à observer').not.toBe('')
  await page.waitForTimeout(ATTENTE_MS)
  const apres = await phraseCourante(page)
  expect(
    apres,
    `avec « Avance toute seule » allumée, l'étape a changé SANS CLIC : ` +
      `« ${avant} » est devenu « ${apres} »`
  ).toBe(avant)

  // Et le bouton est toujours là pour avancer à la main.
  await expect(page.locator('.deroule-rond').first()).toBeVisible()
})
