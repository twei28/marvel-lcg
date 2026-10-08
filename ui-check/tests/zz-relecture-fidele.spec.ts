// JETABLE : relecture fidele (08/10/2026). Un joueur joue, un spectateur le
// regarde en direct, puis la partie se relit : fenetres, selection, loupe,
// taille d'ecran, barre qui se cache, clavier.
import { mkdirSync, writeFileSync } from 'node:fs'
import { gunzipSync } from 'node:zlib'
import { expect, test, type Frame, type Page } from '@playwright/test'
import { lancer, monde, ouvrirEtMettreEnPlace } from '../pilote-campagne'

const DOSSIER = 'captures-tmp/relecture-fidele'
const FICHIER = `${DOSSIER}/partie.marvelreplay`
const STANDARD = ['v16_all', 'no_crisis_of_infinite_deadpools', 'no_encounter_cards_ignore_crisis']

async function cadreDe(page: Page): Promise<Frame> {
  const poignee = await page.waitForSelector('iframe.cadre-joueur', { timeout: 20000 })
  const cadre = await poignee.contentFrame()
  if (!cadre) throw new Error('cadre sans document')
  await cadre.waitForSelector('.plateau-scene, .scan-card', { timeout: 30000 })
  return cadre
}

test('relecture fidele : ce que le joueur a vu', async ({ browser, request }) => {
  test.setTimeout(600_000)
  mkdirSync(DOSSIER, { recursive: true })
  await lancer(request, { scenario: 'rhino', heros: ['spider_man'], regles: STANDARD, seed: 4321 })

  // Le joueur, sur un petit ecran, en affichage detaille.
  const ctxJoueur = await browser.newContext({ viewport: { width: 1280, height: 720 } })
  const joueur = await ctxJoueur.newPage()
  await joueur.goto('/main.html')
  await joueur.evaluate(() => {
    localStorage.setItem('marvel-board-avance-auto', 'off')
    localStorage.setItem('marvel-langue-choisie', '1')
    localStorage.setItem('marvel-board-volume-sons', '37')
  })
  await ouvrirEtMettreEnPlace(joueur, request)
  await joueur.waitForTimeout(2500)
  console.log('PHASE', (await monde(request)).phase)

  // Le spectateur, sur un grand ecran.
  const ctxSpectateur = await browser.newContext({ viewport: { width: 1600, height: 900 } })
  const spectateur = await ctxSpectateur.newPage()
  const erreursSpectateur: string[] = []
  spectateur.on('pageerror', (e) => erreursSpectateur.push(String(e)))
  await spectateur.goto('/app/board.html?spectateur&p=0')
  const cadreDirect = await cadreDe(spectateur)
  const tailleCadre = await spectateur.locator('iframe.cadre-joueur').evaluate((f) => ({
    w: (f as HTMLIFrameElement).offsetWidth,
    h: (f as HTMLIFrameElement).offsetHeight,
    transform: getComputedStyle(f).transform,
  }))
  console.log('CADRE DIRECT', JSON.stringify(tailleCadre))
  expect(tailleCadre.w).toBe(1280)
  expect(tailleCadre.h).toBe(720)
  const volumeDansLeCadre = await cadreDirect.evaluate(() => localStorage.getItem('marvel-board-volume-sons'))
  console.log('VOLUME DANS LE CADRE', volumeDansLeCadre)

  // 1. La loupe : le joueur survole une carte de sa main.
  const main = joueur.locator('.zone-main .scan-card')
  console.log('CARTES EN MAIN', await main.count())
  await main.nth(1).hover()
  await joueur.waitForTimeout(1500)
  const loupeJoueur = await joueur.locator('.carte-apercu, .apercu-carte, [class*="apercu"]').count()
  const loupeSpectateur = await cadreDirect.locator('.carte-apercu, .apercu-carte, [class*="apercu"]').count()
  console.log('LOUPE joueur', loupeJoueur, 'spectateur', loupeSpectateur)
  await joueur.screenshot({ path: `${DOSSIER}/01-joueur-loupe.png` })
  await spectateur.screenshot({ path: `${DOSSIER}/02-spectateur-loupe.png` })

  // 2. Une fenetre de jeu : le joueur clique les cartes de sa main jusqu'a ouvrir un paiement.
  // Lance-toile, puis « Jouer » : la fenetre de paiement s'ouvre.
  const relever = async (nom: string) => {
    const carte = joueur.locator('.zone-main .scan-card').filter({ hasText: nom }).first()
    const b0 = await carte.boundingBox()
    if (b0) await joueur.mouse.move(b0.x + b0.width / 2, b0.y + 8, { steps: 4 })
    await joueur.waitForTimeout(600)
    return carte.boundingBox()
  }
  const lance = await relever('Lance-toile')
  if (lance) await joueur.mouse.click(lance.x + lance.width / 2, lance.y + lance.height / 2)
  await joueur.waitForTimeout(1200)
  await spectateur.screenshot({ path: `${DOSSIER}/03b-spectateur-menu-carte.png`, timeout: 15000 }).catch(() => undefined)
  const jouer = await joueur.getByRole('button', { name: /^Jouer$/i }).first().boundingBox({ timeout: 3000 }).catch(() => null)
  if (jouer) await joueur.mouse.click(jouer.x + jouer.width / 2, jouer.y + jouer.height / 2)
  await joueur.waitForTimeout(1500)
  await spectateur.screenshot({ path: `${DOSSIER}/03c-spectateur-paiement.png`, timeout: 15000 }).catch(() => undefined)
  // Une ressource cochee : Energie.
  const energie = await relever('Énergie')
  if (energie) await joueur.mouse.click(energie.x + energie.width / 2, energie.y + energie.height / 2)
  await joueur.waitForTimeout(1500)
  const fenetre = (await joueur.locator('.assistant-action, .is-target-pulse, .cibles-scene, .barre-cibles').count()) > 0
  const texte = async (cible: Page | Frame) =>
    (await cible.locator('body').innerText({ timeout: 3000 }).catch(() => '')).replace(/\s+/g, ' ')
  const tJ = await texte(joueur)
  const tS = await texte(cadreDirect)
  console.log('TEXTE joueur', tJ.slice(0, 260))
  console.log('TEXTE spectateur', tS.slice(0, 260))
  console.log('MEME TEXTE', tJ === tS)
  const choisies = async (c: Page | Frame) =>
    c.evaluate(() => [...document.querySelectorAll('.scan-card')].filter((e) => /state-(selected|chosen|paid|spent)|est-choisie|est-cochee/.test(e.className)).map((e) => (e as HTMLElement).dataset.cardId).join(','))
  console.log('CARTES CHOISIES joueur', await choisies(joueur), 'spectateur', await choisies(cadreDirect))
  console.log('FENETRE chez le joueur', fenetre)
  // Une carte cochee pour payer, si la fenetre en demande.
  await joueur.waitForTimeout(1500)
  const selJoueur = await joueur.locator('.assistant-action').first().innerText({ timeout: 2000 }).catch(() => '')
  const selSpectateur = await cadreDirect.locator('.assistant-action').first().innerText({ timeout: 2000 }).catch(() => '')
  console.log('FENETRE joueur :', selJoueur.replace(/\s+/g, ' ').slice(0, 160))
  console.log('FENETRE spectateur :', selSpectateur.replace(/\s+/g, ' ').slice(0, 160))
  await joueur.screenshot({ path: `${DOSSIER}/03-joueur-fenetre.png`, timeout: 15000 }).catch((e) => console.log('CAPTURE', String(e).slice(0, 120)))
  await spectateur.screenshot({ path: `${DOSSIER}/04-spectateur-fenetre.png`, timeout: 15000 }).catch((e) => console.log('CAPTURE', String(e).slice(0, 120)))

  // La vitre : un clic du spectateur sur une carte ne fait rien.
  const avant = await cadreDirect.locator('.assistant-action').count()
  await spectateur.mouse.click(700, 860)
  await spectateur.waitForTimeout(500)
  console.log('VITRE : fenetre toujours la', avant, await cadreDirect.locator('.assistant-action').count())

  // Le joueur abandonne la fenetre.
  await joueur.keyboard.press('Escape')
  await joueur.waitForTimeout(1500)
  console.log('ERREURS SPECTATEUR', JSON.stringify(erreursSpectateur))

  // 3. Le fichier.
  const reponse = await request.get('/get_enregistrement')
  expect(reponse.status()).toBe(200)
  const brut = await reponse.body()
  writeFileSync(FICHIER, brut)
  const lignes = gunzipSync(brut).toString('utf-8').split('\n').filter(Boolean)
  const genres: Record<string, number> = {}
  let tailleV = 0
  for (const l of lignes.slice(1)) {
    const o = JSON.parse(l)
    const cle = o.k === 'v' ? `v:${o.g}` : o.k
    genres[cle] = (genres[cle] ?? 0) + 1
    if (o.k === 'v') tailleV += l.length
  }
  console.log('FICHIER', brut.length, 'octets gzip,', gunzipSync(brut).length, 'octets bruts dont', tailleV, 'de lignes v', JSON.stringify(genres))
  const premiereSel = lignes
    .map((l) => JSON.parse(l))
    .filter((o) => o.k === 'v' && o.g === 'sel' && o.v?.o !== undefined && (o.v?.r?.length ?? 0) > 0)
    .at(-1)
  console.log('PREMIERE SELECTION', JSON.stringify(premiereSel))

  // 4. La relecture.
  const ctxRelecture = await browser.newContext({ viewport: { width: 1600, height: 900 } })
  const relecture = await ctxRelecture.newPage()
  const erreurs: string[] = []
  relecture.on('pageerror', (e) => erreurs.push(String(e)))
  await relecture.goto('/app/board.html?relecture=1')
  await relecture.locator('input[type=file]').setInputFiles(FICHIER)
  await relecture.waitForSelector('.relecture-fiche', { timeout: 15000 })
  const cadre = await cadreDe(relecture)
  await relecture.locator('.relecture-fiche .relecture-bouton-lecture').click()
  await relecture.waitForTimeout(300)
  await relecture.keyboard.press(' ')
  await relecture.waitForTimeout(300)
  const dims = await relecture.locator('iframe.cadre-joueur').evaluate((f) => [(f as HTMLIFrameElement).offsetWidth, (f as HTMLIFrameElement).offsetHeight])
  console.log('CADRE RELECTURE', JSON.stringify(dims))
  if (premiereSel) {
    await relecture.evaluate(
      (t) => (window as unknown as { lecteurRelecture?: { allerAuTemps(t: number): void } }).lecteurRelecture?.allerAuTemps(t + 50),
      premiereSel.t as number
    )
    await relecture.waitForTimeout(1500)
    console.log('RELECTURE fenetre :', (await cadre.locator('body').innerText({ timeout: 3000 }).catch(() => 'AUCUNE')).replace(/\s+/g, ' ').slice(0, 160))
    await relecture.screenshot({ path: `${DOSSIER}/05-relecture-fenetre.png`, timeout: 15000 }).catch(() => undefined)
    const choisiesR = await cadre.evaluate(() =>
      [...document.querySelectorAll('.scan-card')].filter((e) => /state-(selected|chosen|paid|spent)/.test(e.className)).map((e) => (e as HTMLElement).dataset.cardId).join(','))
    console.log('RELECTURE cartes choisies', choisiesR)
  }
  // La barre se cache apres 2 s sans bouger, revient en approchant du bas.
  await relecture.mouse.move(800, 300)
  await relecture.waitForTimeout(2600)
  console.log('BARRE cachee', await relecture.locator('.relecture-barre.est-cachee').count())
  await relecture.screenshot({ path: `${DOSSIER}/06-relecture-barre-cachee.png`, timeout: 15000 }).catch(() => undefined)
  await relecture.mouse.move(800, 880, { steps: 3 })
  await relecture.waitForTimeout(400)
  console.log('BARRE revenue', await relecture.locator('.relecture-barre:not(.est-cachee)').count())
  // Clavier, meme le cadre ayant le focus.
  const avantIndex = await relecture.locator('.relecture-situation').innerText({ timeout: 3000 })
  await relecture.keyboard.press('ArrowRight')
  await relecture.waitForTimeout(400)
  console.log('CLAVIER', avantIndex, '->', await relecture.locator('.relecture-situation').innerText({ timeout: 3000 }))
  await relecture.keyboard.press('+')
  console.log('VITESSE', await relecture.locator('.relecture-barre select').first().inputValue({ timeout: 3000 }))
  console.log('ERREURS RELECTURE', JSON.stringify(erreurs))
  await ctxJoueur.close()
  await ctxSpectateur.close()
  await ctxRelecture.close()
})
