// T5 (19/10/2026) : un boost qui met une carte en jeu (sbire Weapons Runner 01121). Ordre voulu :
//   1. le boost est montré et lu en grand ; 2. le résultat de l'attaque ; 3. « X entre en jeu » ; 4. la carte paraît sur la table.
// La carte ne doit JAMAIS être visible sur la table avant l'étape « entre en jeu ».
import { test, expect } from '@playwright/test'
import { commandes, creerPartie, finDuTour, jusquAuTourJoueur, monde, reglagesSurTable } from '../pilote-corrections'
import { questionOuPreparation } from '../pilote-phase-sur-table'

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'moteur de test séparé requis')
test.use({ reducedMotion: 'no-preference', viewport: { width: 1280, height: 720 } })

test('boost sbire : lu, puis résultat, puis « entre en jeu », puis la carte sur la table', async ({ page }, info) => {
  test.setTimeout(240_000)
  const req = page.request
  await creerPartie(req)
  await reglagesSurTable(page)
  await page.goto('/app/board.html?phase=sur-table')
  await jusquAuTourJoueur(page, req)
  await commandes(req, ["Puzzle.ChangeForm('01001b')"])
  await commandes(req, ['Puzzle.EmptyEncounterDeck()', "Puzzle.CreateEncounterDeck('01122','01110','01110','01121')"])
  await page.waitForTimeout(700)
  const w = await monde(req)
  const ids: number[] = []
  const walk = (o: unknown): void => {
    if (Array.isArray(o)) o.forEach(walk)
    else if (o && typeof o === 'object') {
      const c = o as Record<string, unknown>
      if (c.card_id === '01121' && 'game_area' in c && typeof c.id === 'number') ids.push(c.id)
      Object.values(c).forEach(walk)
    }
  }
  walk(w)
  const idRunner = Math.max(...ids)
  await finDuTour(page)

  const evenements: string[] = []
  let visibleAvantEntree = 0
  let vuALEntree = false
  let dernierClic = 0
  for (let i = 0; i < 1200 && !vuALEntree; i++) {
    const s = await page.evaluate((id) => {
      const bandeau = (document.querySelector('.tsm-bandeau')?.textContent ?? '').replace(/\s+/g, ' ')
      const lecture = document.querySelector('.rencontre-sur-table')?.getAttribute('data-lecture') ?? ''
      const cartes = [...document.querySelectorAll(`.plateau-cadre .scan-card[data-card-id="${id}"]`)].filter((e) => !e.closest('.rencontre-sur-table, .carte-apercu') && !e.classList.contains('is-facedown'))
      const visibles = cartes.filter((e) => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 4 && cs.visibility !== 'hidden' && Number(cs.opacity) > 0.05 }).length
      return { bandeau, lecture, visibles, question: !!document.querySelector('.tsm-bandeau.est-question'), bouton: !!document.querySelector('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])') }
    }, idRunner)
    const etiquette = s.lecture === 'lecture' ? 'LECTURE' : /Klaw attaque/.test(s.bandeau) ? 'RESULTAT' : /Weapons Runner entre en jeu/.test(s.bandeau) ? 'ENTREE' : ''
    if (etiquette && evenements[evenements.length - 1] !== etiquette) evenements.push(etiquette)
    if (etiquette !== 'ENTREE' && !evenements.includes('ENTREE')) visibleAvantEntree += s.visibles
    if (etiquette === 'ENTREE') {
      // la carte paraît sur la table à cette étape (laisser le temps à son apparition)
      for (let k = 0; k < 20; k++) {
        const n = await page.evaluate((id) => [...document.querySelectorAll(`.plateau-cadre .scan-card[data-card-id="${id}"]`)].filter((e) => !e.closest('.rencontre-sur-table, .carte-apercu') && !e.classList.contains('is-facedown') && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().width > 4).length, idRunner)
        if (n > 0) { vuALEntree = true; break }
        await page.waitForTimeout(100)
      }
      await page.screenshot({ path: (process.env.CAPTURES_DIR ? process.env.CAPTURES_DIR + '/' : '') + 't5-test-entree.png' })
      break
    }
    const now = Date.now()
    if (now - dernierClic > 1200) {
      if (s.lecture === 'lecture' && s.bouton) { dernierClic = now; await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => undefined) }
      else if (s.question) { dernierClic = now; await questionOuPreparation(page) }
      else if (!s.lecture && s.bandeau) { dernierClic = now - 700; await page.evaluate(() => document.querySelector<HTMLButtonElement>('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click()) }
      else if (!s.bandeau && !s.lecture) { dernierClic = now - 700; await questionOuPreparation(page) }
    }
    await page.waitForTimeout(50)
  }
  info.annotations.push({ type: 'ordre', description: evenements.join(' > ') })
  expect(evenements, 'ordre : lecture du boost, résultat, entrée en jeu').toEqual(['LECTURE', 'RESULTAT', 'ENTREE'])
  expect(visibleAvantEntree, 'la carte n’est jamais visible sur la table avant son étape « entre en jeu »').toBe(0)
  expect(vuALEntree, 'la carte paraît sur la table à l’étape « entre en jeu »').toBe(true)
})
