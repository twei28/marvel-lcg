// T12 (19/10/2026) : « Continuer (Espace) » est TOUJOURS dans le bandeau, à chaque étape ; plus de phrase « Clique la carte dorée,
// ou Espace » ; la carte dorée reste cliquable.
import { test, expect } from '@playwright/test'
import { commandes, creerPartie, finDuTour, jusquAuTourJoueur, reglagesSurTable } from '../pilote-corrections'
import { questionOuPreparation } from '../pilote-phase-sur-table'

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'moteur de test séparé requis')
test.use({ reducedMotion: 'no-preference', viewport: { width: 1280, height: 720 } })

test('chaque étape du bandeau porte « Continuer · Espace » ; la carte dorée avance aussi', async ({ page }, info) => {
  test.setTimeout(240_000)
  const req = page.request
  await creerPartie(req, { scenario: 'klaw' })
  await reglagesSurTable(page)
  await page.goto('/app/board.html?phase=sur-table')
  await jusquAuTourJoueur(page, req)
  await commandes(req, ["Puzzle.ChangeForm('01001b')"])
  await finDuTour(page)
  const etapes = new Map<string, { bouton: boolean; touche: boolean; consigne: boolean }>()
  let clicsCarteDoree = 0
  let dernier = 0
  for (let i = 0; i < 900 && !(await page.locator('.tsm-bandeau.est-bilan').count()); i++) {
    const s = await page.evaluate(() => {
      const b = document.querySelector('.tsm-bandeau:not(.est-question):not(.est-bilan)')
      const phrase = b?.querySelector('.tsm-phrase')?.textContent ?? ''
      const bouton = b?.querySelector('.tsm-bouton') as HTMLButtonElement | null
      const attente = !!b?.querySelector('.tsm-attente')
      return {
        phrase, bouton: !!bouton, desactive: !!bouton?.disabled, touche: !!bouton?.querySelector('kbd') && /Continuer/.test(bouton.textContent ?? ''),
        consigne: /Clique la carte dorée/.test(b?.textContent ?? ''), attente, existe: !!b,
        question: !!document.querySelector('.tsm-bandeau.est-question'), lecture: document.querySelector('.rencontre-sur-table')?.getAttribute('data-lecture') ?? '',
        acteur: !!document.querySelector('.tsm-acteur:not([disabled])'),
      }
    })
    if (s.existe && s.phrase && !s.attente && !s.question) {
      const cur = etapes.get(s.phrase)
      etapes.set(s.phrase, { bouton: (cur?.bouton ?? true) && s.bouton, touche: (cur?.touche ?? true) && s.touche, consigne: (cur?.consigne ?? false) || s.consigne })
    }
    const now = Date.now()
    if (now - dernier > 900) {
      if (s.question) { dernier = now; await questionOuPreparation(page) }
      else if (s.lecture === 'lecture') { dernier = now; await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1000 }).catch(() => undefined) }
      else if (s.existe && s.bouton && !s.desactive && !s.lecture) {
        dernier = now - 300
        // une étape sur deux : la CARTE DORÉE (elle doit toujours avancer) ; l'autre : le bouton Continuer
        if (s.acteur && clicsCarteDoree < 6 && etapes.size % 2 === 0) { clicsCarteDoree++; await page.locator('.tsm-acteur:not([disabled])').first().click({ timeout: 1000, force: true }).catch(() => undefined) }
        else await page.locator('.tsm-bandeau:not(.est-question):not(.est-bilan) .tsm-bouton:not([disabled])').first().click({ timeout: 1000 }).catch(() => undefined)
      } else if (!s.existe) { dernier = now - 500; await questionOuPreparation(page) }
    }
    await page.waitForTimeout(60)
  }
  await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + 't12-test-fin.png' })
  const liste = [...etapes.entries()]
  info.annotations.push({ type: 'etapes', description: JSON.stringify(liste) })
  expect(liste.length, 'plusieurs étapes vues').toBeGreaterThanOrEqual(4)
  for (const [phrase, e] of liste) {
    expect(e.bouton, `« ${phrase.slice(0, 50)} » porte le bouton Continuer`).toBe(true)
    expect(e.touche, `« ${phrase.slice(0, 50)} » : Continuer porte la touche Espace`).toBe(true)
    expect(e.consigne, `« ${phrase.slice(0, 50)} » : plus de « Clique la carte dorée »`).toBe(false)
  }
  expect(await page.locator('.tsm-bandeau.est-bilan').count(), 'la phase va au bout (carte dorée et bouton avancent)').toBe(1)
})
