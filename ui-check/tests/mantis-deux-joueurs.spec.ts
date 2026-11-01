// Mantis a deux joueurs, a la souris (01/11/2026) : Mindlink soigne l'identite de l'AUTRE joueur, Biopathy et Meditation Atrium un ami de l'autre joueur.
//   UI_CHECK_BASE=http://127.0.0.1:2351 MANTIS_DEUX=1 npx playwright test tests/mantis-deux-joueurs.spec.ts --project=pc
import { test, expect, type Page } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import { lancer, lireDemande, repondre } from '../pilote-campagne'

test.skip(!process.env.MANTIS_DEUX, 'cree une partie : MANTIS_DEUX=1 et un moteur d’essai')
const SORTIE = path.resolve('..', 'captures', 'mantis-deux-joueurs')

async function monter(page: Page, mains: string[], enHeros = true, blesserMantis = false) {
  test.setTimeout(180_000)
  page.setDefaultTimeout(10_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  await page.setViewportSize({ width: 1600, height: 900 })
  const request = page.request
  await lancer(request, { scenario: 'rhino', heros: ['mantis', 'spider_man'], regles: ['v16_all', 'no_crisis_of_infinite_deadpools', 'no_encounter_cards_ignore_crisis'], seed: 4321 })
  await page.addInitScript(() => {
    try { localStorage.setItem('marvel-langue-choisie', '1'); localStorage.setItem('marvel-langue', 'fr'); localStorage.setItem('mc_affichage_v1', 'normal') } catch { /* */ }
  })
  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)
  for (let i = 0; i < 120; i++) {
    const t = await (await request.get('/get_ask?p=0')).text()
    if (t.trim() && JSON.parse(t).event_name === 'WhenPlayerInTurn') break
    if (!(await repondre(request, 0))) await repondre(request, 1)
    await page.waitForTimeout(400)
  }
  await page.waitForTimeout(3000)
  const cmd = async (c: string) => { const r = await request.post('/sandbox_command?p=0', { data: { commands: [c] } }); console.log('CMD', c, r.status()); await page.waitForTimeout(1500) }
  if (enHeros) await cmd("Puzzle.ChangeToFace('mt001b', 'mt001a')")
  if (enHeros) await cmd("Puzzle.PutIntoPlay('mt002', under_control=True)")
  await cmd("Puzzle.Damage('01001b', 6)")
  if (blesserMantis) await cmd("Puzzle.Damage(" + (enHeros ? "'mt001a'" : "'mt001b'") + ", 2)")
  await cmd('Puzzle.EmptyHand()')
  await cmd(`Puzzle.CreateHandCards(${mains.map((c) => `'${c}'`).join(', ')})`)
  return { request, cmd }
}

test('Mindlink soigne l’identite de l’autre joueur', async ({ page }) => {
  const { request } = await monter(page, ['mt016', '01089'])
  await page.screenshot({ path: path.join(SORTIE, 'M-1-depart.png') })
  const d = await lireDemande(request)
  console.log('M options', JSON.stringify(d?.options.map((o) => [o.name, o.id, o.bind_id])))
  const boutons = async (nom: string) => { console.log('M', nom, JSON.stringify(await page.getByRole('button').allInnerTexts())); await page.screenshot({ path: path.join(SORTIE, `M-${nom}.png`) }) }
  await page.mouse.click(710, 828)
  await page.waitForTimeout(1500)
  await boutons('2-clic-mindlink')
  await page.getByRole('button', { name: /^jouer$/i }).click()
  await page.waitForTimeout(2000)
  const non = page.getByRole('button', { name: /non, je clique moi-m/i })
  if (await non.isVisible().catch(() => false)) { await non.click(); await page.waitForTimeout(1000) }
  await boutons('3-jouer')
  await page.getByRole('button', { name: /spend up to/i }).click()
  await page.waitForTimeout(2000)
  const non2 = page.getByRole('button', { name: /non, je clique moi-m/i })
  if (await non2.isVisible().catch(() => false)) { await non2.click(); await page.waitForTimeout(1000) }
  await boutons('4-spend')
  await page.mouse.click(800, 832) // Genius (BB) : la ressource de la main
  await page.waitForTimeout(1500)
  await boutons('5-paye')
  await page.getByRole('button', { name: /spend up to/i }).last().click().catch(() => undefined)
  await page.waitForTimeout(2000)
  await boutons('6-valide')
  const banniere = page.getByRole('button', { name: /^JOUER\s*MINDLINK/i })
  await banniere.click()
  await page.waitForTimeout(1500)
  await page.mouse.click(575, 590) // Peter Parker, identite de l'AUTRE joueur
  await page.waitForTimeout(1200)
  await boutons('7-peter-vise')
  await page.getByRole('button', { name: /^JOUER\s*MINDLINK/i }).click()
  await page.waitForTimeout(2500)
  await boutons('8-resolu')
  await expect(page.getByText(/^8 \/ 10$/).first()).toBeVisible()
  await page.getByRole('button', { name: /annuler\s*mindlink/i }).click()
  await page.waitForTimeout(1500)
  await boutons('9-fin')
  await expect(page.getByText(/^9 \/ 9$/).first()).toBeVisible()
})

const pointVie = async (page: Page, nom: RegExp) => (await page.getByRole('button', { name: nom }).first().innerText()).replace(/\s+/g, ' ')
async function sansModale(page: Page) {
  const non = page.getByRole('button', { name: /non, je clique moi-m/i })
  if (await non.isVisible().catch(() => false)) { await non.click(); await page.waitForTimeout(1000) }
}

test('Biopathy soigne un ami de l’autre joueur', async ({ page }) => {
  await monter(page, ['mt009', 'mt006'], true, true)
  const boutons = async (nom: string) => { console.log('B', nom, JSON.stringify(await page.getByRole('button').allInnerTexts())); await page.screenshot({ path: path.join(SORTIE, `B-${nom}.png`) }) }
  const mains = page.locator('article[aria-label^="Psionic Mindlock"]')
  const box = await mains.last().boundingBox()
  await page.mouse.click(box!.x + box!.width / 2, box!.y + 8)
  await page.waitForTimeout(1500)
  await page.getByRole('button', { name: /^jouer$/i }).click()
  await page.waitForTimeout(2000)
  await sansModale(page)
  await boutons('1-paiement')
  const bio = page.locator('article[aria-label^="Biopathy"]').last()
  const b2 = await bio.boundingBox()
  await page.mouse.click(b2!.x + b2!.width / 2, b2!.y + 8)
  await page.waitForTimeout(1500)
  await boutons('2-biopathy-posee')
  await page.getByRole('button', { name: /^R[ÉE]PONSE/i }).first().click()
  await page.waitForTimeout(2000)
  await boutons('3-reponse')
  // Le choix « Mantis, Drax » est celui de la desorientation : le soin est DEJA fait (Mantis a 7/9 ou Peter a 5/10) ; on regarde lequel.
  await page.getByRole('button', { name: /soigner 1 d[ée]g[âa]t/i }).click()
  await page.waitForTimeout(1500)
  await page.mouse.click(575, 590) // Peter Parker
  await page.waitForTimeout(1200)
  await page.getByRole('button', { name: /soigner 1 d[ée]g[âa]t/i }).click()
  await page.waitForTimeout(2500)
  await boutons('4-soigne')
  await expect(page.getByText(/^5 \/ 10$/).first()).toBeVisible() // Peter 4 -> 5
  await expect(page.getByText(/^7 \/ 9$/).first()).toBeVisible() // Mantis intacte
})

test('Meditation Atrium soigne un ami de l’autre joueur', async ({ page }) => {
  const { cmd } = await monter(page, ['01089'], false, true)
  const boutons = async (nom: string) => { console.log('A', nom, JSON.stringify(await page.getByRole('button').allInnerTexts())); await page.screenshot({ path: path.join(SORTIE, `A-${nom}.png`) }) }
  await cmd("Puzzle.PutIntoPlay('mt007', under_control=True)")
  await cmd('Puzzle.EmptyPlayerDeck()')
  await cmd("Puzzle.CreatePlayerDeck('01088', '01089', 'mt002')")
  await boutons('1-depart')
  const atrium = page.locator('article[aria-label^="Meditation Atrium"]').first()
  const ba = await atrium.boundingBox()
  await page.mouse.click(ba!.x + ba!.width / 2, ba!.y + ba!.height / 2)
  await page.waitForTimeout(1500)
  await boutons('2-clic-atrium')
  await page.getByRole('button', { name: /action d.alter ego/i }).click()
  await page.waitForTimeout(2500)
  await boutons('3-action')
  await page.getByRole('button', { name: /action d.alter ego/i }).click()
  await page.waitForTimeout(2500)
  await boutons('4-recherche')
  await page.getByRole('button', { name: /chercher dans le deck/i }).first().click()
  await page.waitForTimeout(2000)
  await boutons('5-fenetre')
  await page.getByRole('button', { name: /^RESSOURCE\s*Drax|Drax/i }).first().click().catch(async () => { console.log('A drax absent de la fenetre') })
  await page.waitForTimeout(800)
  await page.getByRole('button', { name: /^valider$/i }).click()
  await page.waitForTimeout(2500)
  await boutons('6-apres-recherche')
  await page.getByRole('button', { name: /soigner 1 d[ée]g[âa]t/i }).click()
  await page.waitForTimeout(1500)
  await page.mouse.click(575, 590) // Peter Parker
  await page.waitForTimeout(1200)
  await page.getByRole('button', { name: /soigner 1 d[ée]g[âa]t/i }).click()
  await page.waitForTimeout(2500)
  await boutons('7-soigne')
  await expect(page.getByText(/^5 \/ 10$/).first()).toBeVisible() // Peter 4 -> 5
  await expect(page.getByText(/^7 \/ 9$/).first()).toBeVisible() // Mantis intacte
})
