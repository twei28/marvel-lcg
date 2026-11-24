// ANIMATION DE L'ANNULATION (16/11/2026, demande de l'utilisateur : « il faut que le undo, enfin l'animation, soit hyper propre, la c'est pas du
// tout qualitatif »). Ce test OBSERVE ce que le plateau fait pendant et juste apres une annulation : animations CSS actives, noeuds ajoutes,
// classes posees, journal, trames. Captures dans captures/undo_animation/.
//   UI_CHECK_BASE=http://127.0.0.1:2345 UNDO_ANIM=1 npx playwright test tests/undo-animation.spec.ts --project=pc
//
// (Repris de annuler-instantane.spec.ts, dont il reutilise le montage.)
//
// Le moteur trace « === Annuler : instantane restaure === » dans son journal
// quand il restaure : c'est la seule preuve que le rejeu n'a pas servi. Ce test,
// lui, mesure ce que le joueur voit : le monde d'avant, a l'identique.
//
// ⚠ JAMAIS SUR LE 2345 (la partie du joueur) : le cas cree une partie.
//   UI_CHECK_BASE=http://127.0.0.1:2346 ANNULER_INSTANTANE=1 \
//     npx playwright test tests/annuler-instantane.spec.ts --project=pc
import { test, expect, type APIRequestContext, type Page } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'
import contrat from '../contrat-nouvelle-partie.json' with { type: 'json' }
import { choisir, lireDemande, monde, ouvrirEtMettreEnPlace, repondre } from '../pilote-campagne'

const SORTIE = path.resolve('..', 'captures', 'undo_animation')
test.skip(!process.env.UNDO_ANIM, 'cree une partie')

type Brut = { event_name?: string }

async function attendreQuestionDuTour(request: APIRequestContext): Promise<void> {
  for (let i = 0; i < 120; i++) {
    const brut = await (await request.get('/get_ask?p=0')).text()
    try {
      if ((JSON.parse(brut) as Brut).event_name === 'WhenPlayerInTurn') return
    } catch {
      /* pas encore de question */
    }
    await new Promise((r) => setTimeout(r, 500))
  }
  throw new Error('la question du tour n’est jamais venue')
}

/** Le monde sans ce qui change tout seul d'une trame a l'autre. */
async function empreinte(request: APIRequestContext): Promise<string> {
  const m = (await monde(request)) as Record<string, unknown>
  return JSON.stringify(m, (cle, valeur) =>
    ['render_id', 'restaurations', 'restaure_depuis_render_id', 'frame', 'pause_epoch', 'timestamp', 'time', 'step_id', 'current_step_id', 'ask_id', 'is_new'].includes(cle) ? undefined : valeur
  )
}

async function agir(request: APIRequestContext): Promise<void> {
  await attendreQuestionDuTour(request)
  // Une action qui change la table : attaquer, changer de forme, sinon jouer une carte payable. Apres une attaque
  // le heros est epuise : il ne reste que les cartes.
  const options = (await lireDemande(request))?.options ?? []
  const candidates = [
    ...options.filter((o) => /^Attack$/i.test(o.name)),
    ...options.filter((o) => /^Change[ _]Form$/i.test(o.name)),
    ...options.filter((o) => /^Play$/i.test(o.name)),
  ]
  expect(candidates.length, `aucune action jouable (${options.map((o) => o.name).join(', ')})`).toBeGreaterThan(0)
  const avant = await (await request.get('/get_ask?p=0')).text()
  let joue = false
  for (const option of candidates) {
    if (await choisir(request, option)) {
      joue = true
      break
    }
  }
  expect(joue, 'aucune action payable').toBe(true)
  // Juste apres la reponse, `/get_ask` sert encore l'ancienne question : on attend qu'elle change.
  for (let i = 0; i < 40 && (await (await request.get('/get_ask?p=0')).text()) === avant; i++) {
    await new Promise((r) => setTimeout(r, 250))
  }
  await attendreQuestionDuTour(request)
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
  await page.addInitScript(() => {
    try {
      localStorage.setItem('marvel-langue-choisie', '1')
      localStorage.setItem('marvel-langue', 'fr')
      localStorage.setItem('mc_affichage_v1', 'normal')
      localStorage.removeItem('marvel-board-annuler-explique')
    } catch {
      /* */
    }
  })
  await ouvrirEtMettreEnPlace(page, request)
}


test('ce que le plateau fait pendant une annulation', async ({ page }) => {
  test.setTimeout(400_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  const request = page.request
  await partie(page)
  await agir(request)
  const avant = await empreinte(request)
  await agir(request)
  await page.waitForTimeout(3000)
  await page.screenshot({ path: path.join(SORTIE, '0-apres-la-seconde-action.png') })

  // L'enregistreur : tout ce qui bouge dans la page, a partir de maintenant.
  await page.evaluate(() => {
    const w = window as unknown as { __u: { t0: number; anims: Array<{ t: number; n: number; noms: string[] }>; noeuds: Array<{ t: number; classe: string; txt: string }>; classes: Array<{ t: number; cible: string; classe: string }>; bodyClasses: Array<{ t: number; classe: string }> } }
    const t0 = performance.now()
    w.__u = { t0, anims: [], noeuds: [], classes: [], bodyClasses: [] }
    const abr = (e: Element) => (e.tagName.toLowerCase() + '.' + (e.className?.toString() ?? '').split(' ').slice(0, 2).join('.')).slice(0, 60)
    new MutationObserver((muts) => {
      const t = Math.round(performance.now() - t0)
      for (const m of muts) {
        if (m.type === 'childList') {
          m.addedNodes.forEach((n) => {
            if (n instanceof Element) w.__u.noeuds.push({ t, classe: abr(n), txt: (n.textContent ?? '').trim().slice(0, 30) })
          })
        } else if (m.type === 'attributes' && m.attributeName === 'class' && m.target instanceof Element) {
          const c = (m.target as Element).className?.toString() ?? ''
          if (/delta|vol|anim|flip|reveal|entr|arrive|shake|pulse|appear|fly|tombe|pose/i.test(c)) w.__u.classes.push({ t, cible: abr(m.target as Element), classe: c.slice(0, 90) })
          if (m.target === document.body) w.__u.bodyClasses.push({ t, classe: c.slice(0, 120) })
        }
      }
    }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] })
    const tick = () => {
      const t = Math.round(performance.now() - t0)
      const a = document.getAnimations()
      w.__u.anims.push({ t, n: a.length, noms: [...new Set(a.map((x) => (x as CSSAnimation).animationName || (x as CSSTransition).transitionProperty || 'web-anim'))].slice(0, 8) })
      if (t < 6000) setTimeout(tick, 60)
    }
    tick()
  })

  // Le bandeau doit repondre TOUT DE SUITE au clic, bien avant que le moteur ait fini.
  const bouton = page.locator('.bh-undo')
  await bouton.click()
  const modale = page.getByRole('alertdialog')
  if (await modale.isVisible().catch(() => false)) {
    await page.getByRole('checkbox').check().catch(() => undefined)
    await page.getByRole('button', { name: 'Oui, annuler' }).click()
  }
  const debut = Date.now()
  // Des trames toutes les 120 ms pendant 2 s : ce que l'oeil voit.
  for (let i = 0; i < 16; i++) {
    await page.screenshot({ path: path.join(SORTIE, `trame-${String(i).padStart(2, '0')}.png`) })
    await page.waitForTimeout(40)
  }
  await attendreQuestionDuTour(request)
  await expect.poll(() => empreinte(request), { timeout: 30_000 }).toBe(avant)
  await page.waitForTimeout(3000)
  // Ouvrir le journal : l'action annulee y est barree, une ligne « Action annulée » la remplace.
  await page.getByText(/^journal$/i).first().click().catch(() => undefined)
  await page.waitForTimeout(1200)
  await page.screenshot({ path: path.join(SORTIE, '8-journal.png') })
  const journal = await page.evaluate(() => ({
    barrees: [...document.querySelectorAll('.est-annule')].map((e) => (e.textContent ?? '').trim().slice(0, 50)),
    marques: [...document.querySelectorAll('.est-annulation')].map((e) => (e.textContent ?? '').trim().slice(0, 50)),
  }))
  console.log('JOURNAL', JSON.stringify(journal))
  await page.screenshot({ path: path.join(SORTIE, '9-apres.png') })
  const rapport = await page.evaluate(() => (window as unknown as { __u: unknown }).__u)
  fs.writeFileSync(path.join(SORTIE, 'rapport.json'), JSON.stringify({ duree_ms: Date.now() - debut, ...(rapport as object) }, null, 1))
  const r = rapport as { anims: Array<{ t: number; n: number; noms: string[] }>; noeuds: Array<{ t: number; classe: string; txt: string }>; classes: Array<{ t: number; cible: string; classe: string }>; bodyClasses: Array<{ t: number; classe: string }> }
  console.log('ANIMS max', Math.max(...r.anims.map((a) => a.n)), 'noms', JSON.stringify([...new Set(r.anims.flatMap((a) => a.noms))]))
  console.log('NOEUDS', r.noeuds.length, JSON.stringify(r.noeuds.slice(0, 25)))
  console.log('CLASSES', r.classes.length, JSON.stringify(r.classes.slice(0, 25)))
  console.log('BODY', JSON.stringify(r.bodyClasses.slice(0, 8)))
  // CE QUI DOIT ETRE VRAI D'UNE ANNULATION PROPRE :
  expect(r.classes.filter((c) => /a-delta-/.test(c.classe)), 'aucun badge de variation (+N / −N) n\u2019est rejoue').toEqual([])
  expect(r.noeuds.filter((n) => /card-effect-delta|toast-effet/.test(n.classe)), 'aucun toast « perd N jetons »').toEqual([])
  const bandeau = r.noeuds.filter((n) => /bandeau-annulation/.test(n.classe))
  expect(bandeau.length, 'le bandeau d\u2019annulation est apparu').toBeGreaterThan(0)
  const premierChangementDeTable = r.noeuds.find((n) => /plateau-unite/.test(n.classe))
  expect(bandeau[0]!.t, 'et AVANT que la table ne change : l\u2019ecran ne semble jamais fige').toBeLessThan(premierChangementDeTable?.t ?? Infinity)
  expect(journal.marques.length, 'la ligne « Action annulée » est dans le journal').toBeGreaterThan(0)
  expect(journal.barrees.length, 'et l\u2019action annulee y est barree').toBeGreaterThan(0)
})

// L'AUTRE CHEMIN : hors de la question du tour (ici, apres « Fin du tour » : phase du mechant puis tour suivant), il n'y a pas d'instantane ;
// le moteur REJOUE la partie, le render_id recule et le compteur repart de zero. Meme exigence : aucun toast, aucun badge, bandeau, journal.
test('annulation par REJEU (apres la fin du tour) : aussi propre', async ({ page }) => {
  test.setTimeout(500_000)
  fs.mkdirSync(SORTIE, { recursive: true })
  const request = page.request
  // « D'un coup » : la phase du mechant se resout sans s'arreter (sinon quatre minutes d'etapes a traverser dans le test).
  await page.addInitScript(() => { try { localStorage.setItem('marvel-board-mode-phase-mechant', 'instantane') } catch { /* */ } })
  await partie(page)
  await agir(request)
  await page.getByRole('button', { name: /fin du tour/i }).first().click()
  // Le tour suivant : round 2, la question du tour est de nouveau posee.
  // La phase du mechant se traverse comme un joueur : on repond a ce que le moteur demande, et on clique « Continuer » quand la scene le propose.
  for (let i = 0; i < 400; i++) {
    const w = (await monde(request)) as { round_id?: number; phase?: string }
    const round = w.round_id ?? 0
    if (i % 25 === 0) console.log('BOUCLE', i, 'round', round, 'phase', w.phase)
    const ask = await (await request.get('/get_ask?p=0')).text()
    if (round >= 2 && ask.includes('WhenPlayerInTurn')) break
    const suite = page.getByRole('button', { name: /continuer|étape suivante|etape suivante/i }).first()
    if (await suite.isVisible().catch(() => false)) await suite.click().catch(() => undefined)
    else if (round < 2 || !ask.includes('WhenPlayerInTurn')) await repondre(request, 0).catch(() => undefined)
    await page.waitForTimeout(500)
  }
  expect(((await monde(request)) as { round_id?: number }).round_id ?? 0).toBeGreaterThanOrEqual(2)
  await attendreQuestionDuTour(request)
  await page.waitForTimeout(3000)
  await page.screenshot({ path: path.join(SORTIE, 'rejeu-0-avant.png') })
  await page.evaluate(() => {
    const w = window as unknown as { __r: { t0: number; noeuds: Array<{ t: number; classe: string }>; classes: Array<{ t: number; classe: string }> } }
    const t0 = performance.now()
    w.__r = { t0, noeuds: [], classes: [] }
    new MutationObserver((muts) => {
      const t = Math.round(performance.now() - t0)
      for (const m of muts) {
        if (m.type === 'childList') m.addedNodes.forEach((n) => { if (n instanceof Element) w.__r.noeuds.push({ t, classe: (n.tagName.toLowerCase() + '.' + (n.className?.toString() ?? '').split(' ').slice(0, 2).join('.')).slice(0, 60) }) })
        else if (m.type === 'attributes' && m.target instanceof Element && /a-delta-/.test((m.target as Element).className?.toString() ?? '')) w.__r.classes.push({ t, classe: (m.target as Element).className.toString().slice(0, 80) })
      }
    }).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] })
  })
  await page.locator('.bh-undo').click()
  const modale = page.getByRole('alertdialog')
  if (await modale.isVisible().catch(() => false)) {
    await page.getByRole('checkbox').check().catch(() => undefined)
    await page.getByRole('button', { name: 'Oui, annuler' }).click()
  }
  for (let i = 0; i < 10; i++) {
    await page.screenshot({ path: path.join(SORTIE, `rejeu-trame-${String(i).padStart(2, '0')}.png`) })
    await page.waitForTimeout(150)
  }
  await page.waitForTimeout(6000)
  await page.screenshot({ path: path.join(SORTIE, 'rejeu-9-apres.png') })
  const r = (await page.evaluate(() => (window as unknown as { __r: unknown }).__r)) as { noeuds: Array<{ t: number; classe: string }>; classes: Array<{ t: number; classe: string }> }
  console.log('REJEU NOEUDS', r.noeuds.length, JSON.stringify(r.noeuds.slice(0, 20)))
  console.log('REJEU DELTAS', JSON.stringify(r.classes.slice(0, 8)))
  expect(r.classes, 'aucun badge de variation rejoue').toEqual([])
  expect(r.noeuds.filter((n) => /card-effect-delta|toast-effet/.test(n.classe)), 'aucun toast').toEqual([])
  expect(r.noeuds.some((n) => /bandeau-annulation/.test(n.classe)), 'le bandeau a repondu').toBe(true)
})
