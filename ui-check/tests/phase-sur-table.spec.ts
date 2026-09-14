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
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ETAT = 'rhino__spider_man__phase-mechant-complet.js'
/**
 * ⚠ CE FILET NE GARDE PAS LE RYTHME DU MOTEUR, ET IL FAUT LE SAVOIR.
 *
 * Un état ENREGISTRÉ (`?etat=`) ne rejoue aucune trame : il n'y a rien à
 * relâcher, donc rien à retenir. Mesuré le 14/09/2026 — en retirant la garde
 * `!surTable` de `cartouche-a-jour.ts` et en reconstruisant le plateau, ces cas
 * restent VERTS.
 *
 * Ce qu'ils gardent vraiment : le CLIENT n'avance pas tout seul d'une étape à
 * la suivante (l'avance auto, PREMIÈRE cause du défaut « ça continue tout
 * seul »). La TROISIÈME cause — l'annonce qui acquitte le moteur — ne se voit
 * que dans une vraie partie, et elle n'est gardée à ce jour que par la gate
 * unitaire `ui-app/src/board/cartouche-a-jour.test.ts`.
 */
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


test('⚠ le jeton de menace part AU CLIC, pas avant', async ({ page }) => {
  // DEMANDE EXPLICITE DE L'UTILISATEUR, 14/09/2026 : « j'ai envie que la menace
  // sur le trafic clandestin SE METTE QUAND JE FAIS SUIVANT et qu'il ait déjà
  // la même forme que le triangle là. Pourquoi tu me fais un rond ? »
  //
  // DEUX demandes, et une seule avait été traitée. La FORME (le vrai jeton du
  // jeu, `components/jetons/menace.png`) a été prise le 14/09 ; le MOMENT ne
  // l'était pas : le jeton partait dès que l'étape s'affichait, donc avant tout
  // clic, pendant que le joueur lisait encore la phrase.
  test.setTimeout(90000)
  await ouvrirLaPhase(page)

  const jeton = page.locator('.jeton-menace-volant')
  const premiere = await phraseCourante(page)
  expect(premiere, 'la première étape devrait être la menace').toMatch(/menace/i)

  // AVANT le clic : rien ne vole. On laisse même passer du temps, pour qu'un
  // vol différé se voie.
  await page.waitForTimeout(2000)
  expect(
    await jeton.count(),
    `le jeton de menace a volé AVANT le clic, sur « ${premiere} »`
  ).toBe(0)

  // APRÈS le clic : il part.
  await page.locator('.deroule-rond').first().click()
  await expect(jeton.first(), 'le jeton de menace n’est pas parti au clic').toBeVisible({
    timeout: 5000,
  })

  // Et c'est le VRAI JETON DU JEU, pas un rond dessiné. Première version : un
  // disque jaune. Constat de l'utilisateur : « qu'il ait déjà la même forme que
  // le triangle là. Pourquoi tu me fais un rond ? »
  //
  // ⚠ ON COMPARE L'IMAGE ELLE-MÊME, pas son nom de fichier : le bundler inline
  // les petites images en `data:image/png;base64,…`, et aucun nom n'apparaît
  // plus dans la feuille de style. On lit donc le PNG sur le disque et on
  // vérifie que c'est bien lui que le jeton porte.
  const fond = await jeton.first().evaluate((e) => getComputedStyle(e).backgroundImage)
  const png = fs.readFileSync(
    path.join(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'ui-app', 'src', 'components', 'jetons', 'menace.png')
  )
  const debut = png.toString('base64').slice(0, 64)
  expect(
    fond.includes(debut),
    `le jeton ne porte pas l'image menace.png du jeu (fond reçu : ${fond.slice(0, 80)}…)`
  ).toBe(true)
})
