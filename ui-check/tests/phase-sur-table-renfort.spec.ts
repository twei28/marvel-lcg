// T9 (19/10/2026) : un Renfort. Le bandeau reste court (une phrase, pas de surtitre ni de « Renfort : … » dedans) ; une pastille
// rouge « RENFORT » se pose contre la carte lue, sa phrase en petit dessous ; la carte lue n'est jamais rognée, y compris pour
// deux Renforts d'affilée.
import { test, expect } from '@playwright/test'
import { commandes, creerPartie, finDuTour, jusquAuTourJoueur, reglagesSurTable } from '../pilote-corrections'
import { questionOuPreparation } from '../pilote-phase-sur-table'

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'moteur de test séparé requis')
test.use({ reducedMotion: 'no-preference', viewport: { width: 1280, height: 720 } })

test('Renfort : pastille contre la carte lue, bandeau court, carte entière — deux Renforts d’affilée', async ({ page }, info) => {
  test.setTimeout(240_000)
  const req = page.request
  await creerPartie(req, { scenario: 'rhino' })
  await reglagesSurTable(page)
  await page.goto('/app/board.html?phase=sur-table')
  await jusquAuTourJoueur(page, req)
  await commandes(req, ["Puzzle.ChangeForm('01001b')"])
  await commandes(req, ['Puzzle.EmptyEncounterDeck()', "Puzzle.CreateEncounterDeck('01110','01121','01121','01112')"])
  await finDuTour(page)
  const vus: Array<{ pastille: string; phrase: string; bandeauH: number; bandeauLignes: number; carteDansEcran: boolean; surtitre: boolean }> = []
  let dernierClic = 0
  for (let i = 0; i < 1500 && vus.length < 4; i++) {
    const s = await page.evaluate(() => {
      const pastille = document.querySelector('.rencontre-renfort-pastille')?.textContent ?? ''
      const phrase = document.querySelector('.rencontre-renfort small')?.textContent ?? ''
      const b = document.querySelector('.tsm-bandeau')
      const r = b?.getBoundingClientRect()
      const carte = document.querySelector('.rencontre-sur-table .rencontre-sortie')?.getBoundingClientRect()
      const lecture = document.querySelector('.rencontre-sur-table')?.getAttribute('data-lecture') ?? ''
      const texteBandeau = b?.textContent ?? ''
      return {
        pastille, phrase, lecture, bandeauH: r?.height ?? 0,
        bandeauLignes: Math.round((r?.height ?? 0) / 20),
        carteDansEcran: !carte || (carte.top >= 0 && carte.left >= 0 && carte.bottom <= innerHeight && carte.right <= innerWidth),
        surtitre: !!document.querySelector('.tsm-bandeau .tsm-surtitre, .tsm-bandeau .tsm-suite') || /Renfort/.test(texteBandeau),
        bouton: !!document.querySelector('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])'),
        question: !!document.querySelector('.tsm-bandeau.est-question'),
      }
    })
    if (process.env.DEBUG_PILOTE && i % 25 === 0) console.log('renfort', i, JSON.stringify({ ...s }).slice(0, 300))
    if (s.pastille && s.lecture === 'lecture' && !vus.some((v) => v.phrase === s.phrase)) {
      vus.push({ pastille: s.pastille, phrase: s.phrase, bandeauH: s.bandeauH, bandeauLignes: s.bandeauLignes, carteDansEcran: s.carteDansEcran, surtitre: s.surtitre })
      await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + `t9-test-renfort-${vus.length}.png` })
    }
    const now = Date.now()
    if (now - dernierClic > 900) {
      if (s.lecture === 'lecture' && s.bouton) { dernierClic = now; await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1000 }).catch(() => undefined) }
      else if (s.question) { dernierClic = now; await questionOuPreparation(page) }
      else if (!s.lecture && s.bandeauH === 0) { dernierClic = now - 500; await questionOuPreparation(page) }
      else if (!s.lecture && s.pastille === '') { dernierClic = now - 500; await page.evaluate(() => document.querySelector<HTMLButtonElement>('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-question):not(.est-bilan) .tsm-bouton:not([disabled])')?.click()) }
    }
    await page.waitForTimeout(60)
  }
  info.annotations.push({ type: 'renforts', description: JSON.stringify(vus) })
  expect(vus.length, 'une pastille Renfort pour chaque carte de la chaîne').toBeGreaterThanOrEqual(2)
  for (const v of vus) {
    expect(v.pastille).toMatch(/Renfort/i)
    expect(v.surtitre, 'le bandeau ne porte ni surtitre ni « Renfort : … »').toBe(false)
    expect(v.carteDansEcran, 'la carte lue n’est pas rognée').toBe(true)
    expect(v.bandeauH, 'bandeau court (hauteur en px)').toBeLessThanOrEqual(180)
  }
  expect(vus[0]!.phrase).toMatch(/autre carte va être révélée/)
})
