// Le reglage « Inverser le deck et la defausse » (03/11/2026), dans un VRAI navigateur sur une VRAIE partie.
//
// Les tests unitaires (ui-app/src/board/inversion-piles.test.ts) prouvent le reglage et la regle CSS ; ils ne disent pas
// ce que voit le joueur : jsdom n'a pas de mise en page. Celui-ci mesure la position reelle de chaque pile.
//
//   npm run inversion-piles
//
// ATTENTION : lance une NOUVELLE partie sur le serveur de jeu (toute partie en cours est perdue), comme `npm run lancement`.
import { expect, test, type Page } from '@playwright/test'
import { creerPartie } from '../pilote-corrections'

const PAIRES = [
  { nom: 'joueur', deck: 'joueur-deck', defausse: 'joueur-defausse' },
  { nom: 'rencontre', deck: 'rencontre-encounter-deck', defausse: 'rencontre-encounter-discard' },
]

async function ouvrir(page: Page, inversees: boolean) {
  await page.goto('/get_version')
  await page.goto('/main.html')
  await page.evaluate((inv) => {
    localStorage.setItem('marvel-langue-choisie', '1')
    localStorage.setItem('marvel-langue', 'fr')
    localStorage.setItem('mc_aide_bulle_table', 'vue')
    localStorage.setItem('mc_affichage_v1', 'epure')
    localStorage.setItem('mc_piles_inversees', inv ? 'oui' : 'non')
  }, inversees)
  await page.goto('/app/board.html')
  await page.waitForSelector('.plateau-scene', { timeout: 30000 })
  await page.waitForSelector('[data-pile="joueur-deck"]', { timeout: 15000 })
}

/** Abscisse du bord gauche d'une pile, ou null si elle n'est pas affichee. */
async function gauche(page: Page, cle: string): Promise<number | null> {
  const pile = page.locator(`[data-pile="${cle}"]`)
  if ((await pile.count()) === 0) return null // une pile vide n'est pas toujours dessinee : `boundingBox` attendrait jusqu'au delai
  const boite = await pile.first().boundingBox()
  return boite ? boite.x : null
}

test('le deck est a gauche de la defausse par defaut, a droite une fois inverse', async ({ page, request }) => {
  test.setTimeout(120000)
  await creerPartie(request)

  await ouvrir(page, false)
  const normal: Record<string, [number | null, number | null]> = {}
  for (const p of PAIRES) normal[p.nom] = [await gauche(page, p.deck), await gauche(page, p.defausse)]
  await page.screenshot({ path: 'test-results/piles-normal.png' })

  await ouvrir(page, true)
  const inverse: Record<string, [number | null, number | null]> = {}
  for (const p of PAIRES) inverse[p.nom] = [await gauche(page, p.deck), await gauche(page, p.defausse)]
  await page.screenshot({ path: 'test-results/piles-inversees.png' })
  expect(await page.evaluate(() => document.documentElement.dataset.pilesInversees)).toBe('oui')

  for (const p of PAIRES) {
    const [dN, fN] = normal[p.nom]
    const [dI, fI] = inverse[p.nom]
    // Une pile vide peut ne pas etre dessinee : on ne juge que les paires dont les DEUX piles sont a l'ecran.
    if (dN === null || fN === null || dI === null || fI === null) continue
    expect(dN, `${p.nom} : normal, le deck est a gauche de la defausse`).toBeLessThan(fN)
    expect(dI, `${p.nom} : inverse, le deck est a droite de la defausse`).toBeGreaterThan(fI)
  }
  // Au moins la paire du joueur doit avoir ete mesuree : sinon le test ne prouve rien.
  expect(normal.joueur[0], 'le deck du joueur est affiche').not.toBeNull()
  expect(normal.joueur[1], 'la defausse du joueur est affichee').not.toBeNull()
})
