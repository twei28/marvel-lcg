// Partie réelle sur un moteur d'essai uniquement : les animations sont actives.
import { test, expect, type Page } from '@playwright/test'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'serveur de test séparé requis')
test.use({ reducedMotion: 'no-preference', viewport: { width: 1280, height: 720 }, video: 'retain-on-failure' })

async function bouton(page: Page, re: RegExp) {
  const candidats = page.getByRole('button', { name: re })
  for (const b of await candidats.all()) if (await b.isVisible() && await b.isEnabled()) return b
}

async function questionOuPreparation(page: Page, finTour = false) {
  const defausser = page.getByRole('button', { name: /^Défausser \d/ }).first()
  if (await defausser.isVisible().catch(() => false) && await defausser.isDisabled()) {
    const main = page.getByRole('button', { name: /, (Ressource|Événement|Amélioration|Soutien|Allié)$/, pressed: false }).first()
    if (await main.count()) { await main.click(); return }
  }
  const valider = page.locator('.plateau-selecteur-valider:not([disabled])').first()
  if (await valider.isVisible().catch(() => false)) { await valider.click(); return }
  const carte = page.locator('.plateau-selecteur.est-fenetre .plateau-selecteur-carte:not(.est-choisie)').first()
  if (await carte.isVisible().catch(() => false)) { await carte.click(); return }
  for (const re of [/^Garder ma main/, /^Oui, garder/, /^Ne pas (défendre|utiliser|jouer)/, /(^|— )Ne pas/, /^Aucune réponse/, /^Continuer sans rien jouer/, /^Passer/, /^Confirmer$/, /(^|— )Continuer/, /^OK$/, /^Défausser \d/, /^Fin de phase/]) {
    const b = await bouton(page, re)
    if (b) { await b.click(); return }
  }
  if (finTour) {
    const fin = await bouton(page, /Fin du tour/)
    if (fin) { await fin.click(); return }
  }
  const premier = page.locator('[data-choix]:visible, .tsm-utilisable:not(.est-choisie):not([disabled])').first()
  if (await premier.count()) await premier.click()
}

for (const scenario of ['rhino', 'klaw']) test(`lecture, arrivée et explication coordonnées — ${scenario}`, async ({ page }, info) => {
  test.setTimeout(240_000)
  const req = page.request
  const s = await (await req.get(`/get_scenario_json?${scenario}`)).json()
  const charge = {
    campaign_json: JSON.stringify(s), campaign_log: {}, challenges: s.challenges ?? [],
    encounter_set_names: [...new Set([...(s.encounter_sets ?? []), ...(s.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await req.get('/get_hero_json?spider_man')).json())],
    rules: [...contrat.regles_partie_standard, 'mode_sandbox'], seed: 4321, timeout: 0,
  }
  expect((await req.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).ok()).toBe(true)
  console.log(`Partie de test créée : ${scenario}`)
  await page.addInitScript(() => {
    localStorage.setItem('mc_affichage_v1', 'normal')
    localStorage.setItem('mc_phase_presentation', 'bis')
    localStorage.setItem('marvel-langue-choisie', '1')
    localStorage.setItem('marvel-langue', 'fr')
    localStorage.setItem('marvel-board-mode-phase-mechant', 'sur-table')
    localStorage.setItem('mc_aide_bulle_table', 'vue')
  })
  await page.goto('/app/board.html?phase=sur-table')
  const monde = async () => (await (await req.get('/get_world?hot_seat&p=0')).json())
  // Fin du tour est présent dès l'initialisation : attendre la vraie phase joueur.
  for (let i = 0; i < 180; i++) {
    const w = await monde()
    if (i % 30 === 0) console.log(`Préparation ${scenario} : ${w.phase}`)
    // Dès le tour du joueur, laisser la barre finir sa synchronisation ;
    // ne pas choisir une action de jeu à la place d'une question de mise en place.
    if (/^Player(?: \d+)? Turn$/.test(w.phase)) break
    await questionOuPreparation(page)
    await page.waitForTimeout(150)
  }
  if (scenario === 'klaw') {
    const r = await req.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001b')"] } })
    expect(r.ok()).toBe(true)
    await expect.poll(async () => (await monde()).players[0].area_hero[0].name).toBe('Spider-Man')
    await expect(page.locator('.zone-terrain-soutien .scan-card.kind-hero, .scan-card.kind-hero').first()).toBeVisible()
  }
  const fin = page.getByRole('button', { name: /Fin du tour/ }).first()
  await expect(fin).toBeEnabled()
  await fin.click()
  console.log(`Phase du méchant : ${scenario}`)
  let lectures = 0
  let deuxBoosts = false
  let termine = false
  let phaseCommencee = false
  for (let i = 0; i < 300; i++) {
    const etat = await monde()
    phaseCommencee ||= ['Main Scheme Place Threat', 'Enemy Activation', 'Deal Encounter Cards', 'Reveal Encounter Cards'].includes(etat.phase)
    if (i % 30 === 0) console.log(`Étape ${scenario} : ${(await monde()).phase} — ${(await page.locator('.tsm-bandeau').allTextContents()).join(' ')}`)
    const couche = page.locator('.rencontre-sur-table[data-lecture="lecture"]')
    if (await couche.count()) {
      lectures++
      console.log(`Lecture ${scenario} n°${lectures}`)
      const bandeau = page.locator('.tsm-bandeau')
      await expect(bandeau).toBeVisible()
      for (const jeton of await page.locator('.jeton-coup').all()) await expect(jeton).toBeHidden()
      const phrase = (await bandeau.textContent()) ?? ''
      const cartes = couche.locator('.rencontre-sortie')
      const n = await cartes.count()
      deuxBoosts ||= n === 2 && await couche.locator('.est-boost').count() === 2
      const mesures = await cartes.evaluateAll((els) => els.map((el) => {
        const r = el.getBoundingClientRect()
        const id = el.querySelector('[data-card-id]')?.getAttribute('data-card-id')
        const originaux = Array.from(document.querySelectorAll(`.scan-card[data-card-id="${id}"]`)).filter((e) => !e.closest('.rencontre-sur-table'))
        return { x: r.x, y: r.y, w: r.width, h: r.height, id, sourcesMasquees: originaux.every((e) => getComputedStyle(e).visibility === 'hidden') }
      }))
      for (const m of mesures) {
        expect(m.sourcesMasquees).toBe(true)
        expect(m.y).toBeGreaterThan(100)
        expect(m.x).toBeGreaterThanOrEqual(0)
        expect(m.x + m.w).toBeLessThanOrEqual(1281)
      }
      await page.waitForTimeout(2300)
      await expect(couche).toHaveAttribute('data-lecture', 'lecture')
      await expect(bandeau).toHaveText(phrase)
      await page.screenshot({ path: info.outputPath(`lecture-${lectures}.png`) })
      await page.keyboard.press('Space')
      await expect(page.locator('.rencontre-sur-table')).toHaveAttribute('data-lecture', 'depart')
      await page.waitForTimeout(200)
      await expect(bandeau).toHaveText(phrase)
      // Un deuxième clic ne saute ni le trajet ni l'explication suivante.
      await page.keyboard.press('Space')
      await expect(bandeau).toHaveText(phrase)
      await page.waitForTimeout(1900)
      continue
    }
    const bilan = page.locator('.tsm-bandeau.est-bilan .tsm-bouton')
    if (await bilan.count()) { await bilan.click(); termine = true; break }
    if (await page.locator('.rencontre-sur-table[data-lecture="entree"], .rencontre-sur-table[data-lecture="depart"]').count()) {
      await page.waitForTimeout(150)
      continue
    }
    const action = page.locator('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton').first()
    if (await action.count() && !await page.locator('.tsm-bandeau.est-question').count()) {
      // Le halo suit une carte encore en mouvement ; le clavier ne dépend
      // pas de sa stabilité géométrique. Une question peut remplacer l'étape.
      await action.press('Space', { timeout: 1500 }).catch((e) => { if (page.isClosed()) throw e })
    } else await questionOuPreparation(page, !phaseCommencee)
    await page.waitForTimeout(150)
  }
  expect(termine, 'la phase entière doit arriver au bilan').toBe(true)
  expect(lectures).toBeGreaterThan(0)
  if (scenario === 'klaw') expect(deuxBoosts, 'attaque de Klaw avec deux boosts effectivement observée').toBe(true)
})
