import { test } from '@playwright/test'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'
const DECK = JSON.parse(readFileSync(join(process.cwd(), '..', 'Fusion', 'marvel-lcg-src', 'deck', 'starter', 'spider_man.json'), 'utf-8'))
test('la commande Gagner termine-t-elle la partie', async ({ page, request }) => {
  test.setTimeout(240000)
  const liste = (await (await request.get('/list_campagnes?')).json()) as Array<any>
  for (const c of liste) if (c.nom === 'zzgagner') await request.post('/delete_campagne', { data: { id: c.id } })
  const r = await request.post('/save_campagne', { data: { campagne: {
    code: 'fne', nom: 'zzgagner', difficulte: 'standard',
    equipe: [{ heros: 'spider_man', nomHeros: 'Spider-Man', identite: ['01001a,01001b'], deck: DECK }],
    termines: [], carnet: {}, tentatives: {}, partieEnCours: null, tirage: null } } })
  const id = (await r.json()).id
  await page.goto('/campagne.html', { waitUntil: 'networkidle' })
  await page.locator('.cmp-carte', { hasText: 'zzgagner' }).locator('.cmp-carte-ouvrir').click()
  await page.getByRole('button', { name: /tirer la progression/i }).click()
  await page.getByRole('button', { name: /^Le casse du musée/ }).click()
  await page.locator('.cmp-mission button', { hasText: /Lancer le scénario/ }).click()
  await page.waitForURL(/board\.html/, { timeout: 120000 })
  // La partie s'ouvre sur les mulligans : tant qu'on n'a pas garde sa main,
  // la boucle de jeu attend une reponse et ne regarde pas la fin de partie.
  const garder = page.getByRole('button', { name: /garder cette main/i })
  await garder.first().waitFor({ state: 'visible', timeout: 120000 })
  await garder.first().click()
  console.log('MULLIGAN gardé')
  await page.waitForTimeout(10000)
  console.log('APRES MULLIGAN', await page.evaluate(() => document.body.innerText.slice(0, 160).replace(/\n+/g, ' | ')))
  const rep = await page.evaluate(async () => {
    const r = await fetch('/debug?Gagner()')
    return { status: r.status, texte: (await r.text()).slice(0, 120) }
  })
  console.log('DEBUG REPONSE', JSON.stringify(rep))
  await page.waitForTimeout(8000)
  const texte = await page.evaluate(() => document.body.innerText.slice(0, 400).replace(/\n+/g, ' | '))
  console.log('ECRAN', texte)
  console.log('PANNEAU', await page.locator('section.camp-recomp').count(), 'FIN', await page.locator('.fin-partie').count())
  await request.post('/delete_campagne', { data: { id } })
})
