// ANNULER L'ACTION EN COURS (10/10/2026) : la croix de la boite de question et
// la touche Echap remettent la partie AVANT le choix de la carte, sur un vrai
// moteur. Nick Fury (01084) entre en jeu puis pose « choisis un effet » : la
// carte est deja payee et posee, seul `/undo action` la rend proprement.
//
// ⚠ JAMAIS SUR LE 2345 (la partie du joueur) : le cas cree une partie.
//   UI_CHECK_BASE=http://127.0.0.1:2331 ANNULER_ACTION=1 WSLENV=UI_CHECK_BASE:ANNULER_ACTION \
//     npx playwright test tests/annuler-action.spec.ts --project=pc
import { test, expect, type APIRequestContext, type Page } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { choisir, lireDemande, monde, ouvrirEtMettreEnPlace } from '../pilote-campagne'

test.skip(!process.env.ANNULER_ACTION, 'cree une partie : ANNULER_ACTION=1 et un moteur d’essai')

const SORTIE = path.resolve('..', '.planning', 'captures-annuler-action')
const NICK_FURY = '01084'

type Brut = { event_name?: string; annuler_action?: boolean }

async function questionBrute(request: APIRequestContext): Promise<Brut | undefined> {
  const brut = await (await request.get('/get_ask?p=0')).text()
  if (!brut.trim()) return undefined
  try {
    return JSON.parse(brut) as Brut
  } catch {
    return undefined
  }
}

async function attendreQuestion(request: APIRequestContext, accepte: (q: Brut) => boolean): Promise<Brut> {
  for (let i = 0; i < 120; i++) {
    const q = await questionBrute(request)
    if (q?.event_name && accepte(q)) return q
    await new Promise((r) => setTimeout(r, 500))
  }
  throw new Error('la question attendue n’est jamais venue')
}

/** Ce qui doit etre intact apres l'annulation : la main, la defausse, les allies. */
async function etatDuJoueur(request: APIRequestContext) {
  const joueur = (await monde(request)).players[0]
  const ids = (cartes: Array<{ id: number }>) => cartes.map((c) => c.id).sort((a, b) => a - b)
  return {
    main: ids(joueur.hand_cards ?? []),
    defausse: ids(joueur.player_discard_pile ?? []),
    allies: ids(joueur.allies ?? []),
  }
}

async function partie(page: Page) {
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  const scenario = await (await request.get('/get_scenario_json?rhino')).json()
  const charge = {
    campaign_json: JSON.stringify(scenario),
    campaign_log: {},
    challenges: scenario.challenges ?? [],
    encounter_set_names: [...new Set([...(scenario.encounter_sets ?? []), ...(scenario.modular_sets ?? [])])],
    hero_json: [JSON.stringify(await (await request.get('/get_hero_json?spider_man')).json())],
    rules: (contrat as { regles_partie_standard: string[] }).regles_partie_standard,
    seed: 4321,
    timeout: 0,
  }
  expect((await request.get('/new?data=' + encodeURIComponent(JSON.stringify(charge)))).status()).toBe(200)
  await page.addInitScript((langue) => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1')
      localStorage.setItem('marvel-langue', langue)
      localStorage.setItem('mc_affichage_v1', 'normal')
    } catch {
      /* */
    }
  }, process.env.ANNULER_ACTION_EN ? 'en' : 'fr')
  await ouvrirEtMettreEnPlace(page, request)
  const r = await request.post('/sandbox_command?p=0', { data: { commands: [`Puzzle.Gain('${NICK_FURY}')`] } })
  expect(r.status(), await r.text()).toBe(200)
  // Une decision ordinaire APRES le geste de console : rejoue par l'annulation,
  // un geste passe apres le calcul des options de SA question, et Nick Fury
  // reviendrait en main sans y etre jouable. En vraie partie, la carte arrive
  // par une pioche, jamais par un geste.
  await attendreQuestion(request, (q) => q.event_name === 'WhenPlayerInTurn')
  const attaque = (await lireDemande(request))?.options.find((o) => /^Attack$/i.test(o.name))
  expect(attaque, 'pas d’attaque possible pour Spider-Man').toBeTruthy()
  expect(await choisir(request, attaque!)).toBe(true)
}

/** Joue Nick Fury et s'arrete sur sa question « choisis un effet ». */
async function jouerNickFury(request: APIRequestContext): Promise<number> {
  await attendreQuestion(request, (q) => q.event_name === 'WhenPlayerInTurn')
  const joueur = (await monde(request)).players[0]
  const nick = (joueur.hand_cards as Array<{ id: number; code?: string; card_id?: string }>).find((c) =>
    String(c.code ?? c.card_id ?? '').startsWith(NICK_FURY)
  )
  expect(nick, 'Nick Fury n’est pas arrive en main').toBeTruthy()
  const demande = await lireDemande(request)
  const jouer = demande?.options.find((o) => /^Play$/i.test(o.name) && o.bind_id === nick!.id)
  expect(jouer, 'l’option « Play » de Nick Fury manque').toBeTruthy()
  expect(await choisir(request, jouer!), 'Nick Fury n’est pas payable').toBe(true)
  return nick!.id
}

test('Echap puis la croix remettent la partie avant le choix de Nick Fury', async ({ page }) => {
  test.setTimeout(300_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  const request = page.request
  await partie(page)

  const tour = await attendreQuestion(request, (q) => q.event_name === 'WhenPlayerInTurn')
  expect(tour.annuler_action, 'la question du tour n’est pas une action en cours').toBe(false)
  await expect(page.locator('.dc-croix')).toHaveCount(0)
  const avant = await etatDuJoueur(request)

  // 1. Echap.
  const nick = await jouerNickFury(request)
  const sous = await attendreQuestion(request, (q) => q.event_name !== 'WhenPlayerInTurn')
  expect(sous.annuler_action, `sous-question ${sous.event_name} : annuler_action`).toBe(true)
  expect((await etatDuJoueur(request)).allies, 'Nick Fury devrait etre en jeu').toContain(nick)
  await expect(page.locator('.dc-croix')).toBeVisible({ timeout: 15_000 })
  await page.screenshot({ path: path.join(SORTIE, `croix-${process.env.ANNULER_ACTION_EN ? 'en' : 'fr'}.png`) })
  await page.keyboard.press('Escape')
  await attendreQuestion(request, (q) => q.event_name === 'WhenPlayerInTurn')
  await expect.poll(() => etatDuJoueur(request), { timeout: 30_000 }).toEqual(avant)

  // 2. La croix.
  await jouerNickFury(request)
  await attendreQuestion(request, (q) => q.event_name !== 'WhenPlayerInTurn')
  await page.locator('.dc-croix').click({ timeout: 15_000 })
  await attendreQuestion(request, (q) => q.event_name === 'WhenPlayerInTurn')
  await expect.poll(() => etatDuJoueur(request), { timeout: 30_000 }).toEqual(avant)
  await expect(page.locator('.dc-croix')).toHaveCount(0)
})
