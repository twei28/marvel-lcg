// Aides des tests « corrections du 19/10/2026 » (phase du méchant sur la table).
import type { APIRequestContext, BrowserContext, Page } from '@playwright/test'
import contratPartie from './contrat-nouvelle-partie.json' with { type: 'json' }
import { questionOuPreparation } from './pilote-phase-sur-table'

/** Crée une partie de test (bac à sable) sur le moteur d'essai. */
export async function creerPartie(
  req: APIRequestContext,
  { scenario = 'klaw', heros = ['spider_man'], seed = 4321 }: { scenario?: string; heros?: string[]; seed?: number } = {}
) {
  const s = await (await req.get(`/get_scenario_json?${scenario}`)).json()
  const hero_json = await Promise.all(heros.map(async (h) => JSON.stringify(await (await req.get(`/get_hero_json?${h}`)).json())))
  const charge = {
    campaign_json: JSON.stringify(s), campaign_log: {}, challenges: s.challenges ?? [],
    encounter_set_names: [...new Set([...(s.encounter_sets ?? []), ...(s.modular_sets ?? [])])],
    hero_json, rules: [...contratPartie.regles_partie_standard, 'mode_sandbox'], seed, timeout: 0,
  }
  const r = await req.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))
  if (!r.ok()) throw new Error(`/new ${r.status()}`)
}

/** Les réglages de navigateur du mode « Sur la table » (français, présentation bis, aide déjà vue). */
export async function reglagesSurTable(ctx: BrowserContext | Page, extra: Record<string, string> = {}) {
  await ctx.addInitScript((e) => {
    localStorage.setItem('mc_phase_presentation', 'bis')
    localStorage.setItem('marvel-langue-choisie', '1')
    localStorage.setItem('marvel-langue', 'fr')
    localStorage.setItem('marvel-board-mode-phase-mechant', 'sur-table')
    localStorage.setItem('mc_aide_bulle_table', 'vue')
    localStorage.setItem('mc_affichage_v1', 'epure')
    for (const [k, v] of Object.entries(e)) localStorage.setItem(k, v)
  }, extra)
}

export const monde = async (req: APIRequestContext) => (await (await req.get('/get_world?hot_seat&p=0')).json())

export async function commandes(req: APIRequestContext, cmds: string[], p = 0) {
  const r = await req.post(`/sandbox_command?p=${p}`, { data: { commands: cmds } })
  if (!r.ok()) throw new Error(`commande refusée : ${await r.text()}`)
}

/** Joue la mise en place jusqu'au tour du joueur. */
export async function jusquAuTourJoueur(page: Page, req: APIRequestContext) {
  for (let i = 0; i < 200; i++) {
    if (/^Player(?: \d+)? Turn$/.test((await monde(req)).phase)) return
    await questionOuPreparation(page)
    await page.waitForTimeout(120)
  }
  throw new Error('tour du joueur non atteint')
}

export async function finDuTour(page: Page) {
  const req = page.request
  await page.waitForTimeout(700)
  for (let essai = 0; essai < 6; essai++) {
    await page.getByRole('button', { name: /Fin du tour/ }).first().click({ timeout: 4000 }).catch(() => undefined)
    await page.waitForTimeout(800)
    if (!/^Player(?: \d+)? Turn$/.test((await monde(req)).phase)) return
  }
  throw new Error('« Fin du tour » sans effet')
}

/**
 * Avance la phase du méchant (lectures, étapes, questions sans intérêt) jusqu'à ce que `predicat` soit vrai
 * pour le bandeau de question ou d'étape. Rend le texte du bandeau trouvé.
 */
export async function avancerJusqua(page: Page, predicat: (bandeau: string) => boolean, { max = 500 }: { max?: number } = {}): Promise<string> {
  for (let i = 0; i < max; i++) {
    const bandeau = (await page.locator('.tsm-bandeau').first().textContent({ timeout: 500 }).catch(() => null)) ?? ''
    if (process.env.DEBUG_PILOTE && i % 10 === 0) console.log('pilote', i, (await page.request.get('/get_world?hot_seat&p=0').then((r) => r.json()).then((w) => w.phase + '|' + w.prompt).catch(() => '?')), JSON.stringify(bandeau.slice(0, 100)), await page.locator('.rencontre-sur-table[data-lecture]').first().getAttribute('data-lecture', { timeout: 200 }).catch(() => null))
    if (bandeau && predicat(bandeau)) return bandeau
    const lecture = await page.locator('.rencontre-sur-table[data-lecture]').first().getAttribute('data-lecture', { timeout: 300 }).catch(() => null)
    if (lecture === 'lecture') {
      await page.locator('.tsm-bandeau:not(.est-question) .tsm-bouton:not([disabled])').first().click({ timeout: 1500 }).catch(() => undefined)
    } else if (lecture === 'entree' || lecture === 'depart') {
      // les cartes volent : attendre
    } else if (await page.locator('.tsm-bandeau.est-question').count()) {
      await questionOuPreparation(page)
    } else if (await page.locator('.tsm-bandeau.est-bilan').count()) {
      throw new Error('le bilan est arrivé avant la condition attendue')
    } else {
      await page.evaluate(() => {
        if (document.querySelector('.tsm-bandeau.est-question, .tsm-bandeau.est-bilan, .rencontre-sur-table:not([data-lecture="termine"])')) return
        document.querySelector<HTMLButtonElement>('.tsm-acteur:not([disabled]), .tsm-bandeau:not(.est-question):not(.est-bilan) .tsm-bouton:not([disabled])')?.click()
      })
      if (!(await page.locator('.tsm-bandeau').count())) await questionOuPreparation(page, false)
    }
    await page.waitForTimeout(150)
  }
  throw new Error('condition du bandeau non atteinte')
}
