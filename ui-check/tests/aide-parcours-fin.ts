// Le parcours de fin de scénario de campagne (Victoire → Bilan → Carnet → Suite), vu par les tests :
// remplace l'ancien panneau unique (`.camp-recomp`, bouton `.camp-recomp-valider`).
import { expect, type Locator, type Page } from '@playwright/test'

export type PageParcours = 'victoire' | 'bilan' | 'carnet' | 'suite'
const ORDRE: PageParcours[] = ['victoire', 'bilan', 'carnet', 'suite']

export const parcours = (page: Page): Locator => page.locator('.parcours-fin')

/** Le parcours est ouvert (la partie est finie et la campagne l'a pris en charge). */
export async function parcoursOuvert(page: Page, delai = 20000): Promise<void> {
  await expect(parcours(page)).toBeVisible({ timeout: delai })
}

/** Le bouton « Continuer » (pas « Retour », pas le bouton doré de la dernière page). */
const continuer = (page: Page): Locator => page.locator('.pf-bas .pf-btn:not(.pf-btn-sec):not(.pf-btn-or)')

/** Avance à la page demandée, en cliquant « Continuer » autant de fois qu'il faut. */
export async function allerA(page: Page, cible: PageParcours): Promise<void> {
  await parcoursOuvert(page)
  const courante = (await parcours(page).getAttribute('data-page')) as PageParcours | null
  for (let i = ORDRE.indexOf(courante ?? 'victoire') + 1; i <= ORDRE.indexOf(cible); i++) {
    await continuer(page).click()
    await expect(parcours(page)).toHaveAttribute('data-page', ORDRE[i]!)
  }
}

/** Mène l'hôte jusqu'à la dernière page et clique son bouton doré (Commencer, Voir la conclusion...). */
export async function validerParcours(page: Page): Promise<void> {
  await allerA(page, 'suite')
  // Quand le scénario suivant peut se lancer d'office, « Options du scénario » ouvre l'écran de la campagne
  // sans le lancer (l'atterrissage d'avant) ; sinon il n'y a que le bouton doré.
  const options = page.locator('.pf-bas .pf-actions .pf-btn-sec')
  if (await options.count()) await options.click()
  else await page.locator('.pf-bas .pf-btn-or').click()
}
