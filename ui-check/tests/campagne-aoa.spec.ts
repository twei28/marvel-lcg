// L'Ère d'Apocalypse : gagner le dernier scénario peut PERDRE la campagne.
//
// C'est le seul cas du jeu, et il vient du livret (aoa p.20, encart VICTORY du
// scénario 5) :
//
//   « If the Protect the Professor MISSION side scheme was defeated, the players
//     saved Professor X and win the campaign! If the Protect the Professor
//     MISSION side scheme was not defeated, the players failed to save Professor
//     X and lose the campaign. »
//
// Ni « Expert Campaign Only », ni conditionné à la défaite : on peut abattre En
// Sabah Nur et perdre quand même. La chaîne complète — `CollectAoA` qui n'écrit
// PAS `Professor Saved`, le panneau qui lit la règle `cle_absente` de
// `data/campagnes/aoa.json`, l'écran des campagnes qui conclut — n'avait jamais
// été traversée en vraie partie : seuls le module pur (`defaite-campagne.ts`, 9
// cas) et la sonde l'avaient vue.
//
// CE QUE CE TEST NE COUVRE PAS, ET POURQUOI
//
// La branche « Professeur sauvé » demande de DÉJOUER la manigance MISSION en
// jeu. La console du joueur ne sait pas le faire : `PlaceThreat`, `SetThreat` et
// leurs variantes n'ont AUCUN effet sur la menace (mesuré sur la mission 45170a,
// menace 5/5 inchangée après `SetThreat`, `PlaceThreat` positif et négatif), et
// `Remove` la retire de la table sans la faire entrer dans la pile de victoire —
// donc sans la « vaincre » au sens du moteur. La seule voie serait de jouer pour
// de vrai une carte de neutralisation, ce que le pilote ne sait pas faire.
//
//   npm run campagne-aoa
//
// ATTENTION : ce test lance une VRAIE partie. Toute partie en cours sur le
// serveur visé est perdue.
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

const NOM = 'Essai automatique - aoa'

/** Les quatre premiers scénarios d'aoa, pour arriver au dernier. */
const DEJA_JOUES = ['unus', 'four_horsemen', 'apocalypse', 'dark_beast']

test.describe.serial("Campagne : le dernier scénario de l'Ère d'Apocalypse", () => {
  test.setTimeout(240000)

  let identifiant = ''

  test.beforeAll(async ({ request }) => {
    await nettoyer(request, NOM)
  })

  test.afterAll(async ({ request }) => {
    if (identifiant) await request.post('/delete_campagne', { data: { id: identifiant } })
  })

  test('En Sabah Nur vaincu SANS sauver le Professeur : la campagne est perdue', async ({
    page,
    request,
  }) => {
    identifiant = await poserCampagne(request, {
      code: 'aoa',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'colossus', nomHeros: 'Colossus' }],
      termines: DEJA_JOUES,
      carnet: {},
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'en_sabah_nur' })
      )
    }, identifiant)

    await lancer(request, { scenario: 'en_sabah_nur', heros: ['colossus'], carnet: {} })
    await ouvrirEtMettreEnPlace(page, request)

    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait être GAGNÉE : tout le sel du cas est là.').toBe(true)

    // Le panneau s'ouvre sur une victoire, et doit annoncer la campagne perdue.
    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    await expect(
      page.locator('.camp-recomp-defaite'),
      "Le panneau n'annonce pas la campagne perdue alors que le Professeur n'a pas été sauvé."
    ).toBeVisible()
    // Le panneau doit dire les DEUX choses : le scénario est gagné, la campagne
    // s'arrête là. Ne dire que la seconde ferait croire à une défaite en partie.
    await expect(page.locator('.camp-recomp-titre')).toContainText(/perdue/i)
    await expect(page.locator('.camp-recomp-defaite')).toContainText(/gagné/i)

    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    expect(
      apres.carnet?.['Professor Saved'],
      'Le moteur a écrit « Professor Saved » alors que la mission n’a pas été vaincue.'
    ).toBeUndefined()
    expect(apres.perdue, 'La campagne n’est pas marquée perdue sur le serveur.').toBe(true)
    // Le carnet de la CAMPAGNE reste vide, et c'est voulu : une campagne perdue ne
    // rapporte rien, le panneau n'écrit aucun champ. La preuve que le relevé a bien
    // eu lieu se lit donc sur le carnet SORTANT du moteur — sans elle, l'absence de
    // « Professor Saved » ne prouverait rien, un moteur muet aurait le même air.
    const sortant = (await (await request.get('/get_carnet_suggere?')).json()) as {
      scenario: string | null
      suggestions: Record<string, string>
    }
    expect(sortant.scenario, "Le carnet sortant ne vient pas de la partie qu'on vient de jouer.").toBe(
      'en_sabah_nur'
    )
    expect(
      Object.keys(sortant.suggestions ?? {}).length,
      'Le moteur n’a rien relevé du tout : CollectAoA n’a pas tourné.'
    ).toBeGreaterThan(0)
    expect(
      sortant.suggestions?.['Professor Saved'],
      'Le moteur relève « Professor Saved » alors que la mission n’a pas été vaincue.'
    ).toBeUndefined()
  })

  test("L'écran des campagnes conclut sur la campagne perdue", async ({ page }) => {
    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    const carte = page.locator('.cmp-carte', { hasText: NOM })
    await expect(carte).toHaveCount(1)
    await carte.locator('.cmp-carte-ouvrir').click()

    const conclusion = page.locator('.cmp-conclusion')
    await expect(conclusion).toBeVisible()
    await expect(conclusion).toHaveClass(/perdue/)
    // Le texte du livret, déclaré dans aoa.json, et pas un message générique.
    await expect(conclusion).toContainText(/Professeur X n'a pas été sauvé|Professor X/i)
    // Pas d'épilogue sur une campagne perdue : celui du livret raconte la victoire.
    await expect(
      conclusion.locator('.cmp-bd'),
      'La planche d’épilogue raconte la victoire : elle ne doit pas s’afficher ici.'
    ).toHaveCount(0)
  })

  test('Le Professeur SAUVÉ : la campagne est GAGNÉE, pas perdue', async ({ page, request }) => {
    // LA BRANCHE GAGNANTE, l'autre moitié de la règle (livret p.20) : « If the Protect
    // the Professor MISSION side scheme was defeated, the players saved Professor X and
    // win the campaign! »
    //
    // CE QU'UNE PREMIÈRE VERSION DE CE TEST A RATÉ, et qui vaut d'être écrit : poser
    // une campagne déjà terminée avec la clé au carnet, puis regarder l'écran, ne
    // prouve RIEN. `vueConclusion` lit `campagne.perdue`, un drapeau posé par le
    // panneau de récompenses ; l'écran ne rejoue pas la règle. Le test passait avec ET
    // sans la clé.
    //
    // Il faut donc une vraie partie, pour que le PANNEAU évalue le verdict. La mission
    // n'est pas vaincue (hors de portée du pilote, §13), mais la clé est déjà au
    // carnet : le collecteur d'aoa ne la fournit pas, le pré-remplissage retombe donc
    // sur la valeur du carnet, et elle survit. C'est exactement la situation d'une
    // équipe qui a sauvé le Professeur à un scénario précédent de sa campagne.
    identifiant = await poserCampagne(request, {
      ...(identifiant ? { id: identifiant } : {}),
      code: 'aoa',
      nom: NOM,
      difficulte: 'standard',
      equipe: [{ heros: 'colossus', nomHeros: 'Colossus' }],
      termines: DEJA_JOUES,
      carnet: { 'Professor Saved': '1' },
      tentatives: {},
      partieEnCours: null,
    })
    await page.addInitScript((id) => {
      window.localStorage.setItem(
        'mc-campagne-partie',
        JSON.stringify({ id, scenario: 'en_sabah_nur' })
      )
    }, identifiant)

    await lancer(request, {
      scenario: 'en_sabah_nur',
      heros: ['colossus'],
      carnet: { 'Professor Saved': '1' },
    })
    await ouvrirEtMettreEnPlace(page, request)
    const m = await acheverLaPartie(page, request, tuerLeVilainEnJeu, 90)
    expect(m.players_won, 'La partie devait être gagnée.').toBe(true)

    await expect(page.locator('.camp-recomp')).toBeVisible({ timeout: 20000 })
    // Le panneau ne doit PAS annoncer la campagne perdue, et son titre doit dire la
    // victoire de campagne : c'est le verdict, calculé là et nulle part ailleurs.
    await expect(
      page.locator('.camp-recomp-defaite'),
      'Le panneau annonce la campagne perdue alors que le Professeur a été sauvé.'
    ).toHaveCount(0)
    await expect(page.locator('.camp-recomp-titre')).toContainText(/gagnée/i)

    await page.locator('.camp-recomp-valider').click()
    await page.waitForURL('**/campagne.html', { timeout: 30000 })

    const apres = await relireCampagne(request, identifiant)
    expect(apres.perdue, 'La campagne est marquée perdue sur le serveur.').toBeFalsy()
    expect(
      apres.carnet?.['Professor Saved'],
      'La clé a disparu du carnet : le relevé a effacé ce que le joueur avait gagné.'
    ).toBe('1')
    expect(apres.termines, 'Le dernier scénario n’est pas marqué terminé.').toContain('en_sabah_nur')

    // Et l'écran conclut sur la victoire, épilogue compris.
    await page.goto('/campagne.html', { waitUntil: 'networkidle' })
    const carte = page.locator('.cmp-carte', { hasText: NOM })
    await carte.first().locator('.cmp-carte-ouvrir').click()
    const conclusion = page.locator('.cmp-conclusion')
    await expect(conclusion).toBeVisible()
    await expect(conclusion, 'L’écran donne la campagne pour perdue.').not.toHaveClass(/perdue/)
    await expect(
      conclusion.locator('.cmp-bd img'),
      'La planche d’épilogue manque : elle ne s’affiche que sur une campagne gagnée.'
    ).toHaveCount(1)
  })
})
