// T6 (19/10/2026) : défendre sans s'incliner, héros ET allié déjà inclinés, dans « Sur la table ».
//  - Usagi Yōjimbō (up041, « ne s'incline pas pour défendre ») est PROPOSÉ dans « Qui défend ? » ;
//  - TÉMOIN : un allié incliné ordinaire (Hulk) ne peut pas défendre : pas de question, pas de message ;
//  - « Je peux faire ça toute la journée » (56047) est proposé à l'annonce de l'attaque et désigne le héros incliné comme défenseur ;
//  - Bodyguard / Yōjimbō (se011) idem.
import { test, expect, type Page } from '@playwright/test'
import { avancerJusqua, commandes, creerPartie, finDuTour, jusquAuTourJoueur, monde, reglagesSurTable } from '../pilote-corrections'

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'moteur de test séparé requis')
test.use({ reducedMotion: 'no-preference', viewport: { width: 1280, height: 720 } })

async function monter(page: Page, heros: string, avant: string[], inclines: string[]) {
  const req = page.request
  await creerPartie(req, { heros: [heros] })
  await reglagesSurTable(page)
  await page.goto('/app/board.html?phase=sur-table')
  await jusquAuTourJoueur(page, req)
  for (const c of avant) { await commandes(req, [c]); await page.waitForTimeout(500) }
  await finDuTour(page)
  // dès l'ouverture de l'activation (avant l'annonce), on incline : la phase redresse tout à son ouverture
  await avancerJusqua(page, () => false, { aussi: async () => (await monde(req)).phase === 'Enemy Activation' })
  for (const c of inclines) { await commandes(req, [c]); await page.waitForTimeout(500) }
  if (process.env.DEBUG_PILOTE) { const w = await monde(req); const out: unknown[] = []; const walk = (o: unknown, p: string): void => { if (Array.isArray(o)) o.forEach((v, i) => walk(v, `${p}[${i}]`)); else if (o && typeof o === 'object') { const c = o as Record<string, unknown>; if (c.card_id && 'is_ready' in c && /players\[0\]\.(allies|area_hero)/.test(p)) out.push([c.name, c.is_ready]); for (const [k, v] of Object.entries(c)) walk(v, `${p}.${k}`) } }; walk(w, ''); console.log('PRETS', JSON.stringify(out), w.phase) }
  await page.waitForTimeout(600)
}

/** Avance jusqu'à « Qui défend ? » en ne répondant QU'À la réponse de héros (Sens d'Araignée) : jamais à la question de défense. */
async function jusquALaQuestionDeDefense(page: Page) {
  for (let i = 0; i < 400; i++) {
    const b = (await page.locator('.tsm-bandeau').first().textContent({ timeout: 500 }).catch(() => null)) ?? ''
    if (/Qui défend/.test(b)) { await page.waitForTimeout(500); return }
    if (await page.locator('.tsm-bandeau.est-question').count()) {
      await page.getByRole('button', { name: /^Ne pas utiliser|^Ne rien jouer/ }).first().click({ timeout: 800 }).catch(() => undefined)
    } else if (await page.locator('.rencontre-sur-table[data-lecture="lecture"]').count()) {
      await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 800 }).catch(() => undefined)
    } else if (!(await page.locator('.rencontre-sur-table:not([data-lecture="termine"])').count())) {
      await page.evaluate(() => document.querySelector<HTMLButtonElement>('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-question):not(.est-bilan) .tsm-bouton:not([disabled])')?.click())
    }
    await page.waitForTimeout(120)
  }
  throw new Error('« Qui défend ? » n’est jamais apparu')
}

const boutonsDuBandeau = (page: Page) => page.locator('.tsm-bandeau .tsm-bouton, .tsm-etiquette').allTextContents().then((l) => l.map((t) => t.replace(/\s+/g, ' ').trim()))

test('Usagi (ne s’incline pas pour défendre) est proposé, héros et allié inclinés', async ({ page }, info) => {
  test.setTimeout(240_000)
  await monter(page, 'spider_man', ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('up041', under_control=True)"], ["Puzzle.Exhaust('01001a')", "Puzzle.Exhaust('up041')"])
  await jusquALaQuestionDeDefense(page)
  const boutons = await boutonsDuBandeau(page)
  info.annotations.push({ type: 'boutons', description: JSON.stringify(boutons) })
  await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + 't6-test-usagi.png' })
  expect(boutons.some((b) => /Défendre avec\s*Usagi/.test(b)), 'Usagi proposé').toBe(true)
  expect(boutons.some((b) => /Défendre avec\s*Spider-Man/.test(b)), 'Spider-Man incliné non proposé').toBe(false)
  // le clic désigne bien Usagi : le calcul dit sa DÉF
  await page.locator('.tsm-etiquette', { hasText: /Usagi/ }).first().click()
  const calcul = await avancerJusqua(page, (b) => /Klaw attaque/.test(b))
  expect(calcul, 'Usagi est le défenseur désigné').toMatch(/Klaw attaque Usagi/)
})

test('TÉMOIN : un allié ordinaire incliné ne défend pas, et aucune question ni message ne s’affiche', async ({ page }) => {
  test.setTimeout(240_000)
  await monter(page, 'spider_man', ["Puzzle.ChangeForm('01001b')", "Puzzle.PutIntoPlay('01050', under_control=True)"], ["Puzzle.Exhaust('01001a')", "Puzzle.Exhaust('01050')"])
  // l'attaque se résout sans question de défense
  const resultat = await avancerJusqua(page, (b) => /Klaw attaque/.test(b))
  expect(resultat).not.toMatch(/Qui défend/)
})

test('« Je peux faire ça toute la journée » (56047) désigne le héros incliné comme défenseur', async ({ page }) => {
  test.setTimeout(240_000)
  await monter(page, 'spider_man', ["Puzzle.ChangeForm('01001b')", "Puzzle.Gain('56047')"], ["Puzzle.Exhaust('01001a')"])
  await avancerJusqua(page, (b) => /Ne rien jouer|Ne pas jouer/.test(b))
  const noms = await boutonsDuBandeau(page)
  expect(noms.some((b) => /^Jouer$/.test(b)), 'la carte est proposée (bouton Jouer)').toBe(true)
  await page.getByRole('button', { name: /^Jouer$/ }).first().click()
  await page.waitForTimeout(1500)
  // payer avec une carte de la main
  const main = page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/, pressed: false })
  for (let k = 0; k < (await main.count()); k++) {
    const b = main.nth(k)
    if (!/Journée|Toute la/i.test((await b.getAttribute('aria-label')) ?? '')) { await b.click({ timeout: 2000 }).catch(() => undefined); break }
  }
  const calcul = await avancerJusqua(page, (b) => /Klaw attaque/.test(b))
  expect(calcul, 'le héros incliné défend : la DÉF est retranchée').toMatch(/DÉF 3/)
})

test('Bodyguard (Yōjimbō, se011) désigne le héros incliné comme défenseur', async ({ page }) => {
  test.setTimeout(240_000)
  await monter(page, 'leonardo', ["Puzzle.ChangeForm('tl001b')", "Puzzle.PutIntoPlay('se011', under_control=True)"], ["Puzzle.Exhaust('tl001a')"])
  await avancerJusqua(page, (b) => /Ne pas utiliser/.test(b))
  const noms = await boutonsDuBandeau(page)
  expect(noms.some((b) => /Interruption de héros/.test(b)), 'l’interruption est proposée').toBe(true)
  await page.getByRole('button', { name: /^Interruption de héros/ }).first().click()
  const calcul = await avancerJusqua(page, (b) => /Klaw attaque/.test(b))
  expect(calcul).toMatch(/DÉF 2/)
})
