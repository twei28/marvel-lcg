import { errors, type Page } from '@playwright/test'

export async function bouton(page: Page, re: RegExp) {
  const candidats = page.getByRole('button', { name: re })
  for (const b of await candidats.all()) if (await b.isVisible() && await b.isEnabled()) return b
}

export async function questionOuPreparation(page: Page, finTour = false) {
  const mulligan = page.getByRole('dialog', { name: 'Résoudre les mulligans' })
  if (await mulligan.count()) { await mulligan.getByRole('button', { name: 'Annuler', exact: true }).click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); return }
  const defausser = page.getByRole('button', { name: /^Défausser \d/ }).first()
  if (await defausser.isVisible().catch(() => false) && await defausser.isDisabled()) {
    const main = page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/, pressed: false }).first()
    if (await main.count()) { await main.click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); return }
  }
  const valider = page.locator('.plateau-selecteur-valider:not([disabled]), .tsm-bandeau .tsm-bouton:not([disabled])').filter({ hasText: /^Valider/ }).first()
  if (await valider.isVisible().catch(() => false)) { await valider.click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); return }
  for (const re of [/^Garder ma main/, /^Oui, garder/, /^Ne pas (défendre|utiliser|jouer)/, /(^|— )Ne pas/, /^Aucune réponse/, /^Continuer sans rien jouer/, /^Passer/, /^Confirmer$/, /(^|— )Continuer/, /^OK$/, /^Défausser \d/, /^Fin de phase/]) {
    const b = await bouton(page, re)
    if (b) { await b.click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); return }
  }
  const carte = page.locator('.plateau-selecteur.est-fenetre .plateau-selecteur-carte:not(.est-choisie)').first()
  if (await carte.isVisible().catch(() => false)) { await carte.click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); return }
  const unique = page.locator('[data-choix-unique]:visible').first()
  if (await unique.count()) { await unique.click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); return }
  if (finTour) {
    const fin = await bouton(page, /Fin du tour/)
    if (fin) { await fin.click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e }); return }
  }
  const premier = page.locator('[data-choix]:visible, .tsm-utilisable:not(.est-choisie):not([disabled])').first()
  if (await premier.count()) await premier.click({ timeout: 1500 }).catch((e) => { if (!(e instanceof errors.TimeoutError)) throw e })
}

