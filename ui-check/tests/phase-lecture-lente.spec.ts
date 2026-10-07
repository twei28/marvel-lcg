// LA PHASE DU MÉCHANT, LUE LENTEMENT : LE MOTEUR NE DOIT JAMAIS AVANCER SEUL.
//
// ⚠ POURQUOI CE FICHIER EXISTE (07/10/2026). Deux défauts, tous deux mesurés en
// laissant UNE ÉTAPE à l'écran pendant 8 s sans toucher à rien :
//
//  1. Le battement de resynchronisation (toutes les 4 s) acquittait une trame
//     RETENUE : le moteur avançait de 18 rendus pendant que le joueur lisait.
//     C'est « l'étape suivante part sans mon Suivant », sur toutes les étapes.
//  2. Le moteur ne retenait que les trames des quatre phases : il filait de
//     « End Phase » à « Player 1 Turn » du round 2 pendant que le Bilan
//     s'affichait, table, « À toi de jouer » et bandeau de round compris.
//
// Les gardes unitaires (`bilan-retient-le-moteur.test.ts`) prouvent la règle ;
// celui-ci prouve la CHAÎNE entière, sur un vrai moteur, en mode « Étape par
// étape ». Les spécifications rapides (`phase-detaille-defense`) cliquent en
// moins de 4 s et ne peuvent donc pas voir ces défauts.
//
//   ~/marvel-work/python/bin/python3.10 <moteur d'essai sur un port < 32768>
//   UI_CHECK_BASE=http://127.0.0.1:2330 WSLENV=UI_CHECK_BASE npx playwright test tests/phase-lecture-lente.spec.ts --project=pc
//
// ⚠ IL LANCE UNE NOUVELLE PARTIE sur le serveur visé (jamais le 2345 du joueur).
import { expect, test } from '@playwright/test'
import { avancerLaPartie, lancer, monde, ouvrirEtMettreEnPlace, type Conduite } from '../pilote-campagne'

const PHASES = ['Main Scheme Place Threat', 'Enemy Activation', 'Deal Encounter Cards', 'Reveal Encounter Cards']
const STANDARD = ['v16_all', 'no_crisis_of_infinite_deadpools', 'no_encounter_cards_ignore_crisis']
const CONDUITE: Conduite = { resterEnHeros: true, attaquer: true }
/** Plus que le battement de resynchronisation (4 s), moins que le filet (90 s). */
const LECTURE_MS = 8000

test('⚠ une étape lue lentement ne laisse JAMAIS le moteur avancer, Bilan compris', async ({ page, request }) => {
  test.setTimeout(420_000)
  await lancer(request, { scenario: 'rhino', heros: ['spider_man'], regles: STANDARD, seed: 1234 })
  await page.goto('/main.html')
  await page.evaluate(() => {
    localStorage.setItem('marvel-board-mode-phase-mechant', 'detaille')
    localStorage.setItem('marvel-board-avance-auto', 'off')
  })
  await ouvrirEtMettreEnPlace(page, request)
  await avancerLaPartie(page, request, ({ monde: m }) => PHASES.includes(String(m.phase)), 60, CONDUITE)

  const suivant = page.locator('.deroule-phase.est-scene .deroule-suivant')
  const refus = page.locator('.deroule-phase.est-scene [data-refus]')
  let etapesLues = 0
  let bilanLu = false

  for (let n = 0; n < 40 && !bilanLu; n += 1) {
    const avant = await monde(request)
    const boutonSuivant = (await suivant.count()) > 0 && (await suivant.first().isVisible())
    if (boutonSuivant) {
      await page.waitForTimeout(LECTURE_MS)
      const apres = await monde(request)
      expect(
        apres.render_id,
        `étape ${n} (${avant.phase}) : le moteur a avancé SEUL pendant la lecture (rendu ${avant.render_id} → ${apres.render_id}, ${apres.phase})`
      ).toBe(avant.render_id)
      etapesLues += 1
      const libelle = (await suivant.first().innerText()).trim().toLowerCase()
      if (libelle.startsWith('terminer')) {
        // LE BILAN : le moteur doit attendre à « End Phase », au round 1.
        expect(avant.phase, 'le Bilan s\'affiche alors que le moteur est déjà passé à la suite').toBe('End Phase')
        expect(avant.round_id).toBe(1)
        bilanLu = true
      }
      await suivant.first().click()
    } else if ((await refus.count()) > 0 && (await refus.first().isVisible())) {
      await refus.first().click()
    } else {
      await page.waitForTimeout(300)
    }
    await page.waitForTimeout(500)
  }

  expect(bilanLu, 'le Bilan n\'a jamais été atteint').toBe(true)
  expect(etapesLues, 'aucune étape lue').toBeGreaterThan(2)
  // Le clic sur « Terminer » libère le moteur : le tour du joueur du round 2 arrive.
  await expect.poll(async () => (await monde(request)).round_id, { timeout: 15_000 }).toBe(2)
})
