// « Professor X cannot enter play during this game » (aoa, scénario 5).
//
// Instruction SETUP du scénario 5, dans le bloc CAMPAIGN INSTRUCTIONS (livret p.20).
// Elle ne vaut donc qu'en campagne : hors campagne, En Sabah Nur se joue seul et
// rien n'interdit Charles Xavier.
//
// CE QUI A ÉTÉ MESURÉ AVANT DE TROUVER OÙ POSER L'INTERDICTION
//
// Posée sur la manigance principale (45147a), `PlayersCannotPlayCardWhile` n'a
// AUCUN effet : Professor X mis en main par la console, l'option « Play » reste
// offerte sans `failure_reason`, y compris sans la condition de campagne et même
// avec `which_card=None` (donc pour toutes les cartes). Le mécanisme ne se diffuse
// pas depuis le scénario ; les quatre usages du moteur sont tous des cartes JOUEUR.
// Elle est donc portée par l'IDENTITÉ de chaque joueur, enregistrée à la mise en
// place de campagne.
//
// APPROXIMATION ASSUMÉE : ce qui est bloqué, c'est JOUER la carte, le seul chemin
// qu'un joueur emprunte pour la poser. Une capacité qui la mettrait en jeu depuis le
// deck ou la défausse passerait encore — le moteur n'a aucun crochet
// « cannot enter play », et en fabriquer un toucherait la mise en jeu de toutes les
// cartes du jeu.
//
// Colossus est le héros du test parce que son deck de départ contient Professor X.
//
//   npm run campagne-professor-x
//
// ATTENTION : ce test lance de VRAIES parties. Toute partie en cours sur le
// serveur visé est perdue.
import { test, expect, type APIRequestContext, type Page } from '@playwright/test'
import { lireDemande, monde, ouvrirEtMettreEnPlace, repondre, REGLES_CAMPAGNE } from '../pilote-campagne'

const PROFESSOR_X = '32019'

/** Monte la partie sans passer par `lancer`, pour pouvoir retirer `mode_campaign`. */
async function lancerAvecRegles(request: APIRequestContext, regles: readonly string[]) {
  const definition = await (await request.get('/get_scenario_json?en_sabah_nur')).json()
  const deck = await (await request.get('/get_hero_json?colossus')).json()
  await request.get(
    '/new?data=' +
      encodeURIComponent(
        JSON.stringify({
          campaign_json: JSON.stringify(definition),
          campaign_log: {},
          challenges: definition.challenges ?? [],
          encounter_set_names: [
            ...new Set([...(definition.encounter_sets ?? []), ...(definition.modular_sets ?? [])]),
          ],
          hero_json: [JSON.stringify(deck)],
          rules: [...regles],
          seed: 1234,
          timeout: 0,
        })
      )
  )
}

/**
 * Met Professor X en main et rend l'option qui permettrait de le jouer.
 *
 * Par son NOM : `Gain` cherche la carte dans le deck du joueur, et un card_id n'y
 * correspond à aucun nom (il en fabriquerait une copie détachée).
 */
async function optionPourJouerProfessorX(page: Page, request: APIRequestContext) {
  await request.get('/debug?' + encodeURIComponent('Gain("Professor X")'))
  for (let i = 0; i < 4; i++) {
    await repondre(request)
    await page.waitForTimeout(400)
  }
  const m = await monde(request)
  const enMain = ((m.players?.[0]?.hand_cards ?? []) as Array<Record<string, any>>).find(
    (c) => String(c.card_id) === PROFESSOR_X
  )
  expect(enMain, "Professor X n'est pas en main : le test ne mesure rien.").toBeTruthy()

  const demande = await lireDemande(request)
  // `lireDemande` écarte les options refusées : l'absence d'option « Play » sur
  // cette carte EST le refus, du point de vue du joueur comme du plateau.
  const jouable = (demande?.options ?? []).find(
    (o) => /^Play$/i.test(o.name) && o.bind_id === Number(enMain!.id)
  )
  return { jouable, enMain: enMain! }
}

test.describe.serial('AoA, scénario 5 : Professor X ne peut pas entrer en jeu', () => {
  test.setTimeout(240000)

  test('En campagne, le jeu refuse de le jouer', async ({ page, request }) => {
    await lancerAvecRegles(request, REGLES_CAMPAGNE)
    await ouvrirEtMettreEnPlace(page, request)
    const { jouable } = await optionPourJouerProfessorX(page, request)
    expect(
      jouable,
      'Professor X est jouable alors que le livret l’interdit au scénario 5.'
    ).toBeUndefined()
  })

  test('Hors campagne, rien ne l’interdit : le témoin', async ({ page, request }) => {
    // Sans ce témoin, une interdiction qui bloquerait Professor X PARTOUT passerait
    // pour bonne — et elle serait fausse : l'instruction est une CAMPAIGN
    // INSTRUCTION, elle ne vaut que dans la campagne.
    await lancerAvecRegles(
      request,
      REGLES_CAMPAGNE.filter((r) => r !== 'mode_campaign')
    )
    await ouvrirEtMettreEnPlace(page, request)
    const { jouable } = await optionPourJouerProfessorX(page, request)
    expect(
      jouable,
      'Hors campagne, Professor X devrait rester jouable : l’interdiction déborde.'
    ).toBeTruthy()
  })
})
