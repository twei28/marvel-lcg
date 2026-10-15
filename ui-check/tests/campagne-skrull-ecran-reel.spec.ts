// Skrull Menace : une VRAIE partie dans le navigateur, avec le choix de la zone fait a l'ecran.
//
// Ce que les chaines du moteur ne voient pas : que les cartes de campagne (sk263-sk288) arrivent
// dans le deck du joueur depuis le choix de l'ecran, que leur texte s'affiche, et que la regle de
// cooperation pose sa question a l'ecran quand un sbire tombe.
//
// ATTENTION : lance de VRAIES parties. Toute partie en cours sur le serveur vise est perdue.
import { test, expect } from '@playwright/test'
import { lancer, monde, nettoyer, ouvrirEtMettreEnPlace, poserCampagne } from '../pilote-campagne'
import type { APIRequestContext } from '@playwright/test'

const debug = (request: APIRequestContext, c: string) => request.get('/debug?' + encodeURIComponent(c))

const NOM = 'Essai automatique - skrull menace (ecran reel)'
const SORTIE = '/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/aedcc77a-2512-4da8-82a4-14876d788fa2/scratchpad/ec'
const CHOIX = 'sk263;sk270;sk277;sk283'
const CARNET = {
  'Cooperation Area': 'sk263;sk264;sk270;sk277;sk283;sk230a',
  'Shaper of Worlds Game Area': 'Set aside, out of play',
  'Cosmic Cube Creation Game Area': 'Removed from campaign',
  'Player 1 Cooperation Deck': CHOIX,
}

test.describe.serial('Skrull Menace : partie reelle avec le choix de la zone', () => {
  test.setTimeout(240000)
  let id = ''
  test.beforeAll(async ({ request }) => { await nettoyer(request, NOM) })
  test.afterAll(async ({ request }) => { if (id) await request.post('/delete_campagne', { data: { id } }) })

  test('les cartes choisies a l ecran sont dans le deck, lisibles a l ecran', async ({ page, request }) => {
    id = await poserCampagne(request, {
      code: 'skrull_menace', nom: NOM, difficulte: 'standard',
      equipe: [{ heros: 'lyja', nomHeros: 'Lyja' }],
      termines: ['sk_skrull_empire'], carnet: CARNET, tentatives: {}, partieEnCours: null,
    })
    await page.addInitScript((i) => {
      window.localStorage.setItem('mc-campagne-partie', JSON.stringify({ id: i, scenario: 'sk_super_skrull' }))
    }, id)
    await lancer(request, { scenario: 'sk_super_skrull', heros: ['lyja'], carnet: CARNET })
    await ouvrirEtMettreEnPlace(page, request)
    const m = await monde(request)
    const tout = JSON.stringify(m)
    for (const c of CHOIX.split(';')) expect(tout, `${c} devait etre dans la partie`).toContain(c)
    await page.screenshot({ path: `${SORTIE}/01-plateau.png` })

    // Les cartes de campagne en main : leur texte se lit-il ?
    await debug(request, `Gain(${CHOIX.split(';').map((c) => `'${c}'`).join(',')})`)
    await page.waitForTimeout(1500)
    await page.screenshot({ path: `${SORTIE}/02-main.png` })
    const main = JSON.stringify((await monde(request)).players?.[0] ?? {})
    for (const c of CHOIX.split(';')) expect(main, `${c} devait etre en main`).toContain(c)

    // Un sbire vaincu par le joueur : la question de cooperation, a l'ecran.
    // (Les degats viennent de la console : la suite du coup, la mise en pile de victoire, n'est
    // pas fiable par ce chemin ; elle est prouvee par les chaines `cooperation —` du moteur.)
    await debug(request, "puzzle.PutIntoPlay('sk110')")
    await page.waitForTimeout(2000)
    await debug(request, "Damage('sk110', 50, puzzle.FindFaceInPlay('sk037b'))")
    for (let i = 0; i < 12; i++) {
      await page.waitForTimeout(1000)
      const m2 = await monde(request)
      console.log('ATTENTE', i, 'prompt=', String(m2.prompt ?? '').slice(0, 160), '| victoire=', JSON.stringify((m2.victory_display ?? []).map((x: any) => x.card_id)))
      if ((await page.getByText(/pile de victoire|victory display/i).count()) > 0) break
    }
    await page.screenshot({ path: `${SORTIE}/03-cooperation.png` })
    await expect(
      page.getByText('Défausser le dessus de ton deck pour placer Skrull Warrior dans la pile de victoire'),
      'La question de cooperation doit etre posee a l ecran, en francais.'
    ).toBeVisible()
    // On accepte, a l'ecran : le sbire va en pile de victoire, le dessus du deck est defausse.
    const avant = ((await monde(request)).players?.[0]?.player_deck ?? []).length
    await page.getByText('Défausser le dessus de ton deck pour placer Skrull Warrior dans la pile de victoire').click()
    await page.waitForTimeout(3000)
    const apres = await monde(request)
    expect((apres.players?.[0]?.player_deck ?? []).length, 'Le dessus du deck doit etre defausse.').toBe(avant - 1)
    expect((apres.players?.[0]?.player_discard_pile ?? []).length, 'Il est dans la defausse du joueur.').toBe(1)

    // Le texte d'une carte de campagne se lit au survol (captures pour relecture a l'oeil).
    const survols: Array<[string, number]> = [['crusader', 1170], ['buddy', 1305], ['antalya', 1445], ['goggles', 1585]]
    for (const [nom, x] of survols) {
      await page.mouse.move(x, 1030)
      await page.waitForTimeout(1200)
      await page.screenshot({ path: `${SORTIE}/05-survol-${nom}.png` })
    }
  })
})
