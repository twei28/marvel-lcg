// Partie réelle sur un moteur d'essai uniquement : les animations sont actives.
import { test, expect } from '@playwright/test'
import { questionOuPreparation } from '../pilote-phase-sur-table'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }

test.skip(!process.env.UI_CHECK_BASE || /:2345\/?$/.test(process.env.UI_CHECK_BASE), 'serveur de test séparé requis')
test.use({ reducedMotion: 'no-preference', viewport: { width: 1280, height: 720 }, video: 'retain-on-failure' })

for (const scenario of ['rhino', 'klaw', 'klaw-ameliorations', 'klaw-defense', 'klaw-mobile', 'klaw-etoile', 'klaw-stade']) test(`lecture, arrivée et explication coordonnées — ${scenario}`, async ({ page }, info) => {
  test.setTimeout(240_000)
  if (scenario === 'klaw-mobile') await page.setViewportSize({ width: 1050, height: 480 })
  const req = page.request
  const s = await (await req.get(`/get_scenario_json?${scenario.split('-')[0]}`)).json()
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
  await page.addInitScript(() => {
    const changements: Array<{ id: string; dos: boolean; phrase: string }> = []
    ;(window as unknown as { facesAudit: typeof changements }).facesAudit = changements
    const precedents = new Map<string, boolean>()
    setInterval(() => {
      for (const el of document.querySelectorAll<HTMLElement>('.plateau-cadre .scan-card[data-card-id]')) {
        if (el.closest('.rencontre-sur-table, .carte-apercu, .deroule-phase') || getComputedStyle(el).visibility === 'hidden') continue
        const id = el.dataset.cardId!
        const dos = el.classList.contains('is-facedown')
        if (precedents.get(id) !== dos) {
          changements.push({ id, dos, phrase: document.querySelector('.tsm-phrase')?.textContent ?? '' })
          precedents.set(id, dos)
        }
      }
    }, 40)
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
  if (scenario.startsWith('klaw')) {
    const r = await req.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.ChangeForm('01001b')"] } })
    expect(r.ok()).toBe(true)
    await expect.poll(async () => (await monde()).players[0].area_hero[0].name).toBe('Spider-Man')
    await expect(page.locator('.zone-terrain-soutien .scan-card.kind-hero, .scan-card.kind-hero').first()).toBeVisible()
  }
  if (scenario === 'klaw-ameliorations') {
    const r = await req.post('/sandbox_command?p=0', { data: { commands: [
      "Puzzle.PutIntoPlay('01008', under_control=True)",
      "Puzzle.PutIntoPlay('05017', under_control=True)",
      "Puzzle.PutIntoPlay('01079', under_control=True)",
    ] } })
    expect(r.ok()).toBe(true)
    await expect(page.locator('.scan-card.kind-upgrade')).toHaveCount(3)
  }
  if (scenario === 'klaw-defense') {
    const r = await req.post('/sandbox_command?p=0', { data: { commands: [
      "Puzzle.PutIntoPlay('01050', under_control=True)", "Puzzle.PutIntoPlay('01068', under_control=True)", "Puzzle.Damage('01050', 4)",
    ] } })
    expect(r.ok()).toBe(true)
  }
  let ancienStade: number | undefined
  if (scenario === 'klaw-etoile') {
    expect((await req.post('/sandbox_command?p=0', { data: { commands: ["Puzzle.PutIntoDeck('01121')"] } })).ok()).toBe(true)
  }
  if (scenario === 'klaw-stade') {
    const villain = (await monde()).area_villain[0]
    ancienStade = villain.info.health
    expect((await req.post('/sandbox_command?p=0', { data: { commands: [
      "Puzzle.PutIntoPlay('10031', under_control=True)", `Puzzle.Damage(${villain.id}, ${villain.info.health - 1})`,
    ] } })).ok()).toBe(true)
  }
  const fin = page.getByRole('button', { name: /Fin du tour/ }).first()
  await expect(fin).toBeEnabled()
  await fin.click()
  console.log(`Phase du méchant : ${scenario}`)
  const cartesLues = new Set<string>()
  const boostsLus = new Set<string>()
  let defenseChoisie = false
  let barriereJouee = false
  let entreeTestee = false
  let lectures = 0
  let deuxBoosts = false
  let termine = false
  let phaseCommencee = false
  for (let i = 0; i < 300; i++) {
    const etat = await monde()
    phaseCommencee ||= ['Main Scheme Place Threat', 'Enemy Activation', 'Deal Encounter Cards', 'Reveal Encounter Cards'].includes(etat.phase)
    if (i % 30 === 0) console.log(`Étape ${scenario} : ${(await monde()).phase} — ${(await page.locator('.tsm-bandeau').allTextContents()).join(' ')}`)
    if ((scenario === 'klaw-defense' || scenario === 'klaw-stade') && !defenseChoisie && await page.locator('.tsm-bandeau.est-question').count()) {
      const hulk = page.getByRole('button', { name: scenario === 'klaw-stade' ? /Défendre avec Spider-Man/i : /Défendre avec Hulk/i }).first()
      if (await hulk.count()) {
        if (scenario === 'klaw-defense') expect(await page.locator('.tsm-utilisable:not([disabled])').count()).toBeGreaterThanOrEqual(3)
        await page.screenshot({ path: info.outputPath('defenseurs.png') })
        await hulk.click()
        defenseChoisie = true
        continue
      }
    }
    if (scenario === 'klaw-stade') {
      const armure = page.locator('.tsm-bandeau.est-question .tsm-bouton').filter({ hasText: /Armure électrostatique/i }).first()
      if (await armure.count()) { await armure.click(); continue }
    }
    if (scenario === 'klaw-ameliorations' && !barriereJouee) {
      const barriere = page.locator('.tsm-bandeau.est-question .tsm-bouton').filter({ hasText: /Barrière énergétique/i }).first()
      if (await barriere.count()) {
        expect(boostsLus.size, 'les boosts ont été lus avant de choisir la prévention de dégâts').toBeGreaterThan(0)
        await expect(barriere).toBeEnabled()
        await expect(page.locator('.tsm-utilisable[aria-label*="Barrière énergétique"]')).toHaveCount(0)
        await barriere.hover()
        await expect(page.locator('.carte-apercu')).toBeVisible()
        const source = page.locator('.plateau-cadre .scan-card.kind-upgrade[aria-label*="Barrière énergétique"] .scan-frame').first()
        await expect(source).toHaveCSS('box-shadow', /79, 209, 123/)
        await page.screenshot({ path: info.outputPath('amelioration-selection.png') })
        await barriere.click()
        barriereJouee = true
        continue
      }
    }
    const couche = page.locator('.rencontre-sur-table[data-lecture="lecture"]')
    if (await couche.count()) {
      lectures++
      console.log(`Lecture ${scenario} n°${lectures}`)
      const bandeau = page.locator('.tsm-bandeau')
      await expect(bandeau).toBeVisible()
      for (const jeton of await page.locator('.jeton-coup').all()) await expect(jeton).toBeHidden()
      const phraseElement = bandeau.locator('.tsm-phrase')
      const phrase = (await phraseElement.textContent()) ?? ''
      const boosts = couche.locator('.est-boost')
      const avecBoosts = await boosts.count() > 0
      const pv = page.locator('.scan-card.kind-hero .jauge-texte, .scan-card.kind-alter-ego .jauge-texte').first()
      const pvAvant = await pv.count() ? await pv.textContent() : null
      await expect(page.locator('.delta-sur-table')).toHaveCount(0)
      if (avecBoosts) {
        await expect(page.locator('.tsm-nombre')).toHaveCount(0)
        for (const id of await boosts.locator('[data-card-id]').evaluateAll((els) => els.map((e) => e.getAttribute('data-card-id')!))) boostsLus.add(id)
      }
      const continuer = bandeau.locator('.tsm-bouton')
      await expect(continuer).toBeEnabled()
      if (scenario === 'klaw-mobile') expect((await continuer.boundingBox())!.height).toBeGreaterThanOrEqual(44)
      const cartes = couche.locator('.rencontre-sortie')
      for (const id of await cartes.locator('[data-card-id]').evaluateAll((els) => els.map((e) => e.getAttribute('data-card-id')!))) cartesLues.add(id)
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
      await expect(phraseElement).toHaveText(phrase)
      await page.screenshot({ path: info.outputPath(`lecture-${lectures}.png`) })
      await continuer.click()
      await expect(page.locator('.rencontre-sur-table')).toHaveAttribute('data-lecture', 'depart')
      await expect(continuer).toBeDisabled()
      await expect(page.locator('.tsm-attente')).toContainText('se placent')
      await page.waitForTimeout(200)
      await expect(phraseElement).toHaveText(phrase)
      // Un deuxième clic ne saute ni le trajet ni l'explication suivante.
      await page.keyboard.press('Space')
      await expect(phraseElement).toHaveText(phrase)
      await page.waitForTimeout(1900)
      if (avecBoosts) {
        await expect(page.locator('.rencontre-sur-table')).toHaveCount(0)
        if (pvAvant !== null) await expect(pv).toHaveText(pvAvant)
        await page.screenshot({ path: info.outputPath(`resultat-${lectures}.png`) })
      }
      continue
    }
    const bilan = page.locator('.tsm-bandeau.est-bilan .tsm-bouton')
    if (await bilan.count()) { await bilan.click(); termine = true; break }
    if (!entreeTestee && await page.locator('.rencontre-sur-table[data-lecture="entree"]').count()) {
      entreeTestee = true
      await page.keyboard.press('Space')
      await expect(page.locator('.rencontre-sur-table')).toHaveAttribute('data-lecture', 'lecture', { timeout: 4000 })
      await page.waitForTimeout(300)
      await expect(page.locator('.rencontre-sur-table')).toHaveAttribute('data-lecture', 'lecture')
      continue
    }
    if (await page.locator('.rencontre-sur-table[data-lecture="entree"], .rencontre-sur-table[data-lecture="depart"]').count()) {
      await page.waitForTimeout(150)
      continue
    }
    const action = page.locator('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton').first()
    if (await action.count() && !await page.locator('.tsm-bandeau.est-question').count()) {
      // La trame peut changer entre deux requêtes Playwright. Vérifier et
      // cliquer dans le même passage évite qu'une touche préparée pour
      // l'étape précédente ne ferme le bilan qui vient d'apparaître.
      await page.evaluate(() => {
        if (document.querySelector('.tsm-bandeau.est-question, .tsm-bandeau.est-bilan, .rencontre-sur-table')) return
        document.querySelector<HTMLButtonElement>('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-bilan):not(.est-question) .tsm-bouton')?.click()
      })
    } else await questionOuPreparation(page, !phaseCommencee)
    await page.waitForTimeout(150)
  }
  const faces = await page.evaluate(() => (window as unknown as { facesAudit: Array<{ id: string; dos: boolean; phrase: string }> }).facesAudit)
  await info.attach('faces-rencontres', { body: JSON.stringify(faces, null, 2), contentType: 'application/json' })
  for (const id of boostsLus) {
    const etats = faces.filter((e) => e.id === id)
    const visible = etats.findIndex((e) => !e.dos)
    if (visible >= 0) expect(etats.slice(visible).every((e) => !e.dos), `le boost ${id} ne se recache pas après avoir été montré`).toBe(true)
  }
  expect(termine, 'la phase entière doit arriver au bilan').toBe(true)
  expect(lectures).toBeGreaterThan(0)
  if (scenario === 'klaw-defense') {
    expect(defenseChoisie).toBe(true)
    expect((await monde()).players[0].allies.some((c: { card_id: string }) => c.card_id === '01050'), 'Hulk vaincu après sa défense').toBe(false)
  }
  if (scenario === 'klaw-etoile') {
    const w = await monde()
    expect(w.players[0].engaged_enemies.some((c: { card_id: string }) => c.card_id === '01121'), 'le sbire du boost étoile est en jeu').toBe(true)
  }
  if (scenario === 'klaw-stade') {
    const suivant = (await monde()).area_villain[0]
    expect(suivant.info.health).toBeGreaterThan(ancienStade!)
    expect(cartesLues.has(String(suivant.id)), 'le nouveau stade a été lu au centre').toBe(true)
  }
  if (scenario === 'klaw-ameliorations') expect(barriereJouee, 'amélioration choisie par son bouton nommé').toBe(true)
  if (['klaw', 'klaw-ameliorations', 'klaw-defense', 'klaw-mobile'].includes(scenario)) expect(deuxBoosts, 'attaque de Klaw avec deux boosts effectivement observée').toBe(true)
})
