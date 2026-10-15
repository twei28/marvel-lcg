// Skrull Menace : le carnet voyage par le VRAI panneau de recompenses.
//
// `tools/test_campagne_chaine.py` joue les cinq scenarios cote moteur et EMULE ce que le panneau
// reporte (cles declarees dans data/campagnes/skrull_menace.json, champs d'un joueur elimine
// ignores). Ce test-ci joue le chemin reel : vraie partie, plateau ouvert, panneau de fin, bouton
// « Valider », campagne relue sur le serveur. Il garde donc ce que l'emulation ne peut pas garder :
// que le panneau sache AFFICHER et ECRIRE les champs de la campagne (Cooperation Area avec ses 30
// cartes cliquables, tableau, zones du Shaper et du Cube).
//
//   UI_CHECK_BASE=http://127.0.0.1:31900 npx playwright test tests/campagne-skrull-menace.spec.ts --project=pc
//
// Prerequis (dans une copie du depot, pas dans le depot principal) : un serveur sur un port a soi
// (copie de `.game-src` + `main.py`), `public/app` (plateau compile) et `public/stories/skrull_menace/`
// (scans du livret) : ni l'un ni l'autre n'est versionne, les lier vers ceux du depot principal.
//
// ATTENTION : ce test lance de VRAIES parties. Toute partie en cours sur le serveur vise est perdue.
import { test, expect } from '@playwright/test'
import {
  acheverLaPartie,
  lancer,
  nettoyer,
  ouvrirEtMettreEnPlace,
  poserCampagne,
  relireCampagne,
  tuerLeVilainEnJeu,
} from '../pilote-campagne'

const NOM = 'Essai automatique - skrull menace'

// Ce que le scenario 1 a laisse (zone des fragments seulement : les cartes sk263-sk288 sont portees
// a part, ce test n'en depend pas) : le Cube est en pile de victoire, donc retire, et ses quatre
// fragments sont dans la zone de cooperation.
const CARNET_APRES_LE_1 = {
  'Cooperation Area': 'sk230a;sk230b;sk230c;sk230d',
  'Shaper of Worlds Game Area': 'Set aside, out of play',
  'Cosmic Cube Creation Game Area': 'Removed from campaign',
  'Skrull Elite: Jazinda': 'In another game area',
}

test.describe('Campagne Skrull Menace : l interface de choix de campagne', () => {
  test('la boite est proposee a la creation, dans l ordre de parution, avec ses cinq scenarios', async ({ page, request }) => {
    const definies = (await (await request.get('/list_campagnes_definies')).json()) as Array<Record<string, any>>
    const boite = definies.find((b) => b.code === 'skrull_menace')
    expect(boite, 'La boite n est pas dans /list_campagnes_definies.').toBeTruthy()
    expect(boite!.nb_scenarios).toBe(5)
    const rangs = definies.map((b) => parseInt(String(b.cle_extension).split('.')[0], 10))
    expect(rangs).toEqual([...rangs].sort((a, b) => a - b))

    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    await page.getByRole('button', { name: 'Nouvelle campagne' }).click()
    const tuile = page.locator('.cmp-boite', { hasText: /Menace Skrull/ })
    await expect(tuile, 'La tuile « Menace Skrull » manque a l ecran de creation.').toBeVisible()
    await expect(tuile).toContainText('5')
  })

  test('une campagne creee montre ses sets de mise en place et ses reglages (sets alternatifs)', async ({ page, request }) => {
    const nom = 'Essai automatique - skrull menace (ecran)'
    await nettoyer(request, nom)
    const id = await poserCampagne(request, {
      code: 'skrull_menace',
      nom,
      difficulte: 'expert',
      equipe: [{ heros: 'lyja', nomHeros: 'Lyja' }],
      termines: [],
      carnet: {},
      tentatives: {},
      partieEnCours: null,
    })
    try {
      await page.goto('/campagne.html', { waitUntil: 'networkidle' })
      await page.locator('.cmp-carte', { hasText: nom }).locator('.cmp-carte-ouvrir').click()
      await expect(page.getByRole('button', { name: /Lancer le scénario/ })).toBeVisible()
      await expect(page.locator('.cmp-sets'), 'Les sets du scenario 1 ne sont pas listes.').toContainText(/Army of Skrulls/i)
      await expect(
        page.locator('img[src*="/stories/skrull_menace/"]').first(),
        'Le livret (pages de regles) n est pas branche a l ecran de la campagne.'
      ).toBeAttached()
      await expect(page.getByText('Standard Skrull à la place de Standard')).toBeVisible()
      await expect(page.getByText('Expert Skrull à la place d\'Expert'), 'Reglage reserve a la campagne experte.').toBeVisible()
    } finally {
      await request.post('/delete_campagne', { data: { id } })
    }
  })

  test('l ecran Cooperation montre la zone, le tableau (ligne complete) et le journal par scenario', async ({ page, request }) => {
    const nom = 'Essai automatique - skrull menace (cooperation)'
    await nettoyer(request, nom)
    const id = await poserCampagne(request, {
      code: 'skrull_menace',
      nom,
      difficulte: 'standard',
      equipe: [{ heros: 'lyja', nomHeros: 'Lyja' }],
      termines: ['sk_skrull_empire', 'sk_super_skrull'],
      carnet: {
        'Cooperation Area': 'sk263;sk267;sk274;sk230a;sk230b;sk230c;sk230d',
        'Cooperation Progress': 'Cadre K: Non-ELITE minion;Cadre K: Hijacked;Cadre K: GENIUS minion;Antalya: Nemesis minion',
        'Shaper of Worlds Game Area': 'Set aside, out of play',
        'Cosmic Cube Creation Game Area': 'Removed from campaign',
        'Skrull Elite: Xavin': 'In another game area',
      },
      historique: {
        sk_skrull_empire: { 'Shaper of Worlds Game Area': 'In another game area' },
        sk_super_skrull: { 'Shaper of Worlds Game Area': 'Set aside, out of play', 'Cosmic Cube Creation Game Area': 'Removed from campaign' },
      },
      tentatives: {},
      partieEnCours: null,
    })
    try {
      await page.goto('/campagne.html', { waitUntil: 'networkidle' })
      await page.locator('.cmp-carte', { hasText: nom }).locator('.cmp-carte-ouvrir').click()
      await page.getByRole('button', { name: 'Coopération' }).click()
      await expect(page.locator('.cmp-coop-carte')).toHaveCount(30)
      await expect(page.locator('.cmp-coop-carte.presente'), 'Les 7 cartes du carnet doivent etre en couleur.').toHaveCount(7)
      await expect(page.locator('.cmp-coop-ligne.complete'), 'Seule la ligne Cadre K est complete.').toHaveCount(1)
      await expect(page.locator('.cmp-coop-ligne.complete')).toContainText('Cadre K')
      await expect(page.locator('.cmp-coop-case.cochee')).toHaveCount(4)
      const shaper = page.locator('.cmp-coop-journal tr[data-cle="Shaper of Worlds Game Area"] td')
      await expect(shaper.nth(0)).toHaveText('In another game area')
      await expect(shaper.nth(1)).toHaveText('Set aside, out of play')
      await expect(page.locator('.cmp-coop-journal tr[data-cle="Skrull Elite: Xavin"] .cmp-coop-now')).toHaveText('In another game area')
      await page.screenshot({ path: '/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/aedcc77a-2512-4da8-82a4-14876d788fa2/scratchpad/cooperation.png', fullPage: true })
    } finally {
      await request.post('/delete_campagne', { data: { id } })
    }
  })

  test('le choix des cartes de la zone se fait sur vignettes, avant la partie, et se garde au carnet', async ({ page, request }) => {
    const nom = 'Essai automatique - skrull menace (choix zone)'
    await nettoyer(request, nom)
    const id = await poserCampagne(request, {
      code: 'skrull_menace',
      nom,
      difficulte: 'standard',
      equipe: [{ heros: 'lyja', nomHeros: 'Lyja' }, { heros: 'spider_man', nomHeros: 'Spider-Man' }],
      termines: ['sk_skrull_empire'],
      carnet: { 'Cooperation Area': 'sk263;sk264;sk270;sk277;sk230a' },
      tentatives: {},
      partieEnCours: null,
    })
    try {
      await page.goto('/campagne.html', { waitUntil: 'networkidle' })
      await page.locator('.cmp-carte', { hasText: nom }).locator('.cmp-carte-ouvrir').click()
      await page.locator('button[data-vue="zone"]').click()
      const j1 = page.locator('.cmp-zone-joueur[data-joueur="1"]')
      const j2 = page.locator('.cmp-zone-joueur[data-joueur="2"]')
      await expect(j1.locator('.cmp-zone-vignette')).toHaveCount(5)
      await expect(j1).toContainText('pas encore choisi')
      await j1.locator('[data-carte="sk263"]').click()
      await expect(j1.locator('[data-carte="sk263"]')).toHaveClass(/sel/)
      await expect(j2.locator('[data-carte="sk263"]'), 'Une carte unique prise par le joueur 1 n est plus offerte au joueur 2.').toBeDisabled()
      await j1.locator('[data-carte="sk264"]').click()   // meme type : remplace
      await j1.locator('[data-carte="sk270"]').click()
      await j2.locator('.cmp-zone-ligne[data-type="Ressources"] [data-carte="sk230a"]').click()
      await j2.locator('.cmp-zone-ligne[data-type="Alliés"] [data-aucune]').click()
      const apres = await relireCampagne(request, id)
      expect(apres.carnet?.['Player 1 Cooperation Deck']).toBe('sk264;sk270')
      expect(apres.carnet?.['Player 2 Cooperation Deck']).toBe('sk230a')
      await expect(j2).not.toContainText('pas encore choisi')
      await page.screenshot({ path: '/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/aedcc77a-2512-4da8-82a4-14876d788fa2/scratchpad/choix-zone.png', fullPage: true })
    } finally {
      await request.post('/delete_campagne', { data: { id } })
    }
  })
})

test.describe.serial('Campagne Skrull Menace : le panneau reporte la zone et les etats', () => {
  test.setTimeout(300000)

  let identifiant = ''

  test.beforeAll(async ({ request }) => {
    await nettoyer(request, NOM)
  })

  test.afterAll(async ({ request }) => {
    if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
  })

  test('scenario 2 gagne : Super-Skrull et Searching for Powers rejoignent la zone, les etats sont reportes', async ({
    page,
    request,
  }) => {
    identifiant = await poserCampagne(request, {
      code: 'skrull_menace',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'lyja', nomHeros: 'Lyja' }],
      termines: ['sk_skrull_empire'],
      carnet: CARNET_APRES_LE_1,
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'sk_super_skrull' })
      )
    }, identifiant)

    await lancer(request, { scenario: 'sk_super_skrull', heros: ['lyja'], carnet: CARNET_APRES_LE_1 })
    await ouvrirEtMettreEnPlace(page, request)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait etre gagnee.').toBe(true)

    // Le panneau de fin de partie montre les champs de la campagne.
    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    await expect(page.locator('.camp-champ-libelle', { hasText: 'Zone de coopération' })).toBeVisible()
    await expect(page.locator('.camp-champ-libelle', { hasText: 'Tableau de coopération' })).toBeVisible()
    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    expect(apres.termines, 'Le scenario gagne n est pas marque termine.').toContain('sk_super_skrull')
    expect(
      apres.historique?.sk_super_skrull?.['Cooperation Area'],
      'Le panneau n a pas garde la colonne du scenario 2 dans l historique.'
    ).toContain('sk267')
    const zone = String(apres.carnet?.['Cooperation Area'] ?? '').split(';').filter(Boolean)
    for (const id of ['sk267', 'sk274', 'sk230a', 'sk230b', 'sk230c', 'sk230d']) {
      expect(zone, `${id} devait etre dans la zone de cooperation : ${zone}`).toContain(id)
    }
    expect(
      apres.carnet?.['Shaper of Worlds Game Area'],
      'La zone du Shaper n a pas ete reportee par le panneau.'
    ).toBeTruthy()
    expect(
      apres.carnet?.['Cosmic Cube Creation Game Area'],
      'Le Cube retire de la campagne doit le rester.'
    ).toBe('Removed from campaign')
    expect(
      apres.carnet?.['Skrull Elite: Jazinda'],
      'Jazinda (laissee ailleurs, non vaincue) doit rester « In another game area ».'
    ).toBe('In another game area')
  })
})
