// Mot-clé Starting (signalement Yarro n°70) : la preuve À L'ÉCRAN que le plateau pose la question
// « Ajouter cette carte à ta main de départ » et que les deux réponses font ce qu'elles disent.
// Étape 8 bis de docs/reference/PROCESSUS-CARTE.md. Lance une NOUVELLE partie : moteur d'essai seulement.
//
//   UI_CHECK_BASE=http://127.0.0.1:<port> WSLENV=UI_CHECK_BASE:CAPTURES_N70 npx playwright test tests/starting-mise-en-place.spec.ts --project=pc
import { test, expect, type Page, type APIRequestContext } from '@playwright/test'
import { repondre } from '../pilote-campagne'

const DOSSIER = process.env.CAPTURES_N70 || ''
const REGLES = ['v16_all', 'no_crisis_of_infinite_deadpools', 'no_encounter_cards_ignore_crisis']
const LIBELLE = { fr: 'Ajouter cette carte à ta main de départ', en: 'Add this card to your starting hand' }
// Le bouton de l'OPTION (« Annuler » + nom de la carte), pas l'annulation de la barre du haut.
// Le nom de la carte vient du moteur, en français même en anglais (traduction côté serveur).
const ANNULER = { fr: /^Annuler\s*(Réflexes Innés|Innate Reflexes)/i, en: /^Cancel\s*(Réflexes Innés|Innate Reflexes)/i }

async function lancerStormAvecReflexes(request: APIRequestContext, seed: number) {
  const definition = await (await request.get('/get_scenario_json?rhino')).json()
  const storm = await (await request.get('/get_hero_json?storm')).json()
  storm.player_deck = ['60038', ...storm.player_deck.slice(1)]
  await request.get('/new?data=' + encodeURIComponent(JSON.stringify({
    campaign_json: JSON.stringify(definition),
    campaign_log: {},
    challenges: definition.challenges ?? [],
    encounter_set_names: [...new Set([...(definition.encounter_sets ?? []), ...(definition.modular_sets ?? [])])],
    hero_json: [JSON.stringify(storm)],
    rules: REGLES,
    seed,
    timeout: 0,
  })))
}

/** Les cartes de la mise en place (manigance principale…) passent devant la table : on les fait défiler. */
async function passerLaMiseEnPlace(page: Page) {
  const continuer = page.locator('.mep-couche .mep-continuer').first()
  for (let i = 0; i < 30 && (await page.locator('.mep-couche').count()) > 0; i++) {
    if (await continuer.isVisible().catch(() => false)) await continuer.click({ timeout: 1500, force: true }).catch(() => {})
    await page.waitForTimeout(400)
  }
}

const ask = async (request: APIRequestContext) => (await (await request.get('/get_ask?p=0')).text()).trim()
// Le moteur nomme l'option avec des soulignés : « Add_this_card_to_your_starting_hand ».
const estLaQuestion = (brut: string) => /starting[_ ]hand/.test(brut)

/** Où est Innate Reflexes, et combien de cartes en main ? Lu dans /get_world (players[0]). */
async function etatDeLaMain(request: APIRequestContext) {
  const monde = await (await request.get('/get_world')).json()
  const joueur = monde.players[0] as Record<string, unknown>
  const zones = Object.entries(joueur)
    .filter(([, v]) => Array.isArray(v) && (v as Array<Record<string, unknown>>).some((c) => c && String(c.card_id) === '60038'))
    .map(([k]) => k)
  return { zones, main: (joueur.hand_cards as unknown[]).length, tailleDeMain: joueur.hand_size }
}

async function capture(page: Page, nom: string) {
  if (DOSSIER) await page.screenshot({ path: `${DOSSIER}/${nom}.png` })
}

for (const langue of ['fr', 'en'] as const) {
  for (const choix of ['ajouter', 'annuler'] as const) {
    for (const [ecran, viewport] of [['1920', { width: 1920, height: 1080 }], ['360', { width: 360, height: 780 }]] as const) {
      test(`Starting ${langue} ${choix} ${ecran}`, async ({ browser, request }) => {
        test.setTimeout(240_000)
        const ctx = await browser.newContext({ viewport, hasTouch: ecran === '360', isMobile: ecran === '360', deviceScaleFactor: 1 })
        const page = await ctx.newPage()
        // Annuler : une graine où la carte n'est pas piochée dans la main de départ, sinon on ne prouve rien.
        await lancerStormAvecReflexes(request, choix === 'annuler' ? Number(process.env.SEED_N70 || 99) : 1234)
        await page.goto('/main.html')
        await page.evaluate((l) => {
          localStorage.setItem('marvel-langue', l)
          localStorage.setItem('marvel-langue-choisie', '1')
        }, langue)
        await page.goto('/app/board.html', { waitUntil: 'networkidle' })

        // Les questions de mise en place d'avant (météo de Storm...) sont servies par le pilote.
        let trouve = false
        for (let i = 0; i < 60 && !trouve; i++) {
          await passerLaMiseEnPlace(page)
          const brut = await ask(request)
          if (estLaQuestion(brut)) { trouve = true; break }
          if (brut) await repondre(request, 0)
          await page.waitForTimeout(500)
        }
        expect(trouve, 'le moteur pose la question Starting').toBe(true)

        await passerLaMiseEnPlace(page)
        const bouton = page.getByRole('button', { name: LIBELLE[langue] })
        await expect(bouton).toBeVisible({ timeout: 20_000 })
        await capture(page, `${langue}-${ecran}-1-question`)

        if (choix === 'ajouter') await bouton.click()
        else await page.getByRole('button', { name: ANNULER[langue] }).click()

        // Prochaine étape : les mulligans, main de départ affichée.
        await expect.poll(async () => estLaQuestion(await ask(request)), { timeout: 20_000 }).toBe(false)
        await page.waitForTimeout(2500)
        const etat = await etatDeLaMain(request)
        console.log(`[n70] ${langue} ${choix} ${ecran} : Innate Reflexes dans ${JSON.stringify(etat.zones)}, main ${etat.main}, taille de main ${etat.tailleDeMain}`)
        if (choix === 'ajouter') expect(etat.zones).toContain('hand_cards')
        else expect(etat.zones).not.toContain('hand_cards')
        await capture(page, `${langue}-${ecran}-2-main-apres-${choix}`)
        await ctx.close()
      })
    }
  }
}
