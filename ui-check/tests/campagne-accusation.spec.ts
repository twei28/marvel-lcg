// Le scénario 5 d'Agents of S.H.I.E.L.D., joué pour de vrai.
//
// Deux entrées de la famille « câblé mais jamais vu en vraie partie », et elles
// tombent ensemble parce qu'elles butaient sur le même mur : le pilote savait
// lancer une partie et la finir de force, mais pas la JOUER. Or les deux moments
// visés n'arrivent qu'au fil d'un tour normal.
//
//   1. LES PREUVES GAGNÉES EN PARTIE. Le livret p.19 ne donne aucune preuve à la
//      victoire du scénario 5, contrairement aux scénarios 1 à 4 : au 5, elles se
//      gagnent EN JEU, par la Réponse de l'étape 1B (« Zemo's Manipulations »,
//      50167b). Cette Réponse est un `AfterPhaseEnd` : elle ne part qu'à la fin
//      d'une phase de joueur. `GainCardsFromShieldEnvelope` était éprouvée en
//      l'appelant directement, jamais par ce déclencheur.
//
//   2. L'ACCUSATION VUE DE L'ÉCRAN. `50168a` demande trois preuves au joueur
//      (`AskChoosePaper`, une par série : moyen, mobile, occasion) et en déduit
//      l'accusé. La chaîne 2A→3B était éprouvée en avançant la manigance à la
//      main ; les questions n'avaient jamais été vues dans l'interface.
//
// CE QUI DÉBLOQUE TOUT ÇA : poster `{}` pour PASSER. Le contrat le dit
// (`ui-app/src/board/moteur.ts`, `envoyerReponse(null)`), et sans lui le pilote
// restait bloqué dans le tour du joueur — aucune phase ne se terminait, la menace
// ne montait jamais, et le vilain ne jouait pas. Voir `avancerLaPartie`.
//
//   npm run campagne-accusation
//
// ATTENTION : ce test lance de VRAIES parties. Toute partie en cours sur le
// serveur visé est perdue.
import { test, expect } from '@playwright/test'
import {
  avancerJusquALaQuestion,
  avancerLaPartie,
  lancer,
  monde,
  ouvrirEtMettreEnPlace,
  REGLES_CAMPAGNE,
  type Monde,
} from '../pilote-campagne'

/**
 * L'enveloppe A.I.M. du carnet : la combinaison de la taupe.
 *
 * Elle est imposée ici pour que l'invariant se mesure : une preuve GAGNÉE ne peut
 * jamais être une preuve de la taupe, puisque l'enveloppe S.H.I.E.L.D. est
 * exactement le complément. Si une des trois sortait, toute la déduction serait
 * fausse et le joueur accuserait le mauvais membre.
 */
const TAUPE = ['50185', '50188', '50191']

/** Le carnet d'arrivée au scénario 5 : un membre du Conseil déjà vidé. */
const CARNET = {
  'A.I.M. Envelope': TAUPE.join(';'),
  'Secret Counters: Chief Medical Officer': '0',
  'Secret Counters: Chief Surveillance Officer': '2',
  'Secret Counters: Chief Tactical Officer': '2',
}

/** Les neuf preuves, par série. La question de l'accusation en propose trois. */
const MOYENS = ['50185', '50186', '50187']
const MOBILES = ['50188', '50189', '50190']
const OCCASIONS = ['50191', '50192', '50193']

const preuvesEnJeu = (m: Monde): string[] =>
  ((m.area_evidence ?? []) as Array<Record<string, unknown>>).map((c) => String(c.card_id))

test.describe.serial("Campagne : le scénario 5 d'Agents of S.H.I.E.L.D., joué", () => {
  test.setTimeout(300000)

  test('La Réponse de l’étape 1B gagne une preuve EN PARTIE', async ({ page, request }) => {
    await lancer(request, { scenario: 'baron_zemo', heros: ['maria_hill'], carnet: CARNET })
    await ouvrirEtMettreEnPlace(page, request)

    const depart = await avancerLaPartie(page, request, () => false, 1)
    expect(
      preuvesEnJeu(depart),
      'Une preuve est en jeu avant la moindre fin de phase : la mise en place en a posé une.'
    ).toHaveLength(0)

    // On avance jusqu'à ce qu'une preuve entre en jeu, ce qui ne peut venir que
    // de la Réponse de l'étape 1B — rien d'autre n'en donne au scénario 5.
    const m = await avancerLaPartie(page, request, ({ monde }) => preuvesEnJeu(monde).length > 0, 40)
    const gagnees = preuvesEnJeu(m)
    expect(
      gagnees.length,
      "Aucune preuve gagnée en partie : la Réponse de l'étape 1B ne s'est jamais déclenchée."
    ).toBeGreaterThan(0)

    // L'invariant qui compte : la preuve vient de l'enveloppe S.H.I.E.L.D., donc
    // jamais de la combinaison de la taupe.
    for (const preuve of gagnees) {
      expect(
        TAUPE,
        `La preuve ${preuve} appartient à la taupe : la déduction repartirait fausse.`
      ).not.toContain(preuve)
    }
    // Et elle est bien une des neuf, pas une carte fabriquée au hasard.
    for (const preuve of gagnees) {
      expect([...MOYENS, ...MOBILES, ...OCCASIONS]).toContain(preuve)
    }
  })

  test('La répartition des preuves ne part plus au navigateur, même hors campagne', async ({
    page,
    request,
  }) => {
    // LE SECRET N'EST PAS L'EXISTENCE DES NEUF PREUVES — elle est imprimée dans le
    // livret — C'EST LEUR RÉPARTITION : savoir lesquelles trois dorment dans
    // l'enveloppe A.I.M., c'est connaître la taupe sans jouer.
    //
    // Le pack montait les deux enveloppes en piles (`SetAsideDeck`), et
    // `to_descriptor` rend toutes ces piles au navigateur avec le `card_id` réel de
    // chaque carte, face cachée ou non : la réponse partait au client, triée par
    // enveloppe. La campagne fermait déjà la fuite en ne fabriquant aucune carte
    // avant le droit de la voir ; hors campagne, les neuf preuves quittent
    // maintenant le jeu TOUTES ENSEMBLE, et la combinaison vit dans le store, sous
    // une clé filtrée du carnet sortant.
    //
    // Hors campagne EXPRÈS : c'était le dernier endroit où la fuite subsistait.
    const definition = await (await request.get('/get_scenario_json?baron_zemo')).json()
    const deck = await (await request.get('/get_hero_json?maria_hill')).json()
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
            rules: REGLES_CAMPAGNE.filter((r) => r !== 'mode_campaign'),
            seed: 1234,
            timeout: 0,
          })
        )
    )
    await ouvrirEtMettreEnPlace(page, request)
    const m = await monde(request)

    const toutes = [...MOYENS, ...MOBILES, ...OCCASIONS]
    const parZone: Record<string, string[]> = {}
    for (const [zone, valeur] of Object.entries(m)) {
      if (!Array.isArray(valeur)) continue
      const ids = (valeur as unknown[])
        .flat()
        .filter((c): c is Record<string, unknown> => Boolean(c) && typeof c === 'object')
        .map((c) => String(c.card_id))
        .filter((id) => toutes.includes(id))
      if (ids.length) parZone[zone] = ids
    }

    // Aucun deck additionnel : c'est par là que la répartition sortait.
    expect(
      ((m.additional_decks ?? []) as unknown[][]).flat().length,
      'Une pile additionnelle est montée : la répartition repart au navigateur.'
    ).toBe(0)
    // Les neuf au même endroit, donc rien à en déduire.
    const zones = Object.keys(parZone)
    expect(
      zones.length,
      `Les preuves sont réparties sur plusieurs zones (${JSON.stringify(parZone)}) : la répartition se lit.`
    ).toBe(1)
    expect(parZone[zones[0]!]!.length, 'Les neuf preuves ne sont pas toutes au même endroit.').toBe(9)
  })

  test('Les trois questions de l’accusation s’affichent dans le plateau', async ({
    page,
    request,
  }) => {
    await lancer(request, { scenario: 'baron_zemo', heros: ['maria_hill'], carnet: CARNET })
    await ouvrirEtMettreEnPlace(page, request)

    // La chaîne d'étapes avance par ses propres Réponses (« Advance to stage 2A »),
    // jusqu'à ce que « The Accusation » (50168a) demande sa première preuve.
    const demande = await avancerJusquALaQuestion(page, request, /^p_(50185|50186|50187)$/, 50)
    expect(
      demande,
      "La question du MOYEN n'a jamais été posée : l'accusation n'a pas été atteinte."
    ).toBeTruthy()

    const noms = (demande?.options ?? []).map((o) => String(o.name ?? ''))
    expect(noms.sort(), 'La question du moyen ne propose pas les trois preuves de sa série.').toEqual(
      MOYENS.map((id) => `p_${id}`).sort()
    )

    // CE QUE LE JOUEUR VOIT. La question s'affiche dans la « demande centrale »
    // (DemandeCentrale.tsx), qui nettoie le préfixe « p_ » et rend un bouton par
    // option. Sans elle, la question existerait côté moteur et personne ne
    // pourrait y répondre autrement qu'à la console.
    const panneau = page.locator('.demande-centrale')
    await expect(panneau, "La demande n'est pas affichée au joueur.").toBeVisible()
    const choix = panneau.locator('button.af-action:not(.dc-pass)')
    await expect(choix, "Le plateau n'affiche pas les trois choix de la question.").toHaveCount(3)
    for (const id of MOYENS) {
      await expect(
        choix.filter({ hasText: id }),
        `Le choix ${id} n'est pas proposé à l'écran.`
      ).toHaveCount(1)
    }

    // On répond EN CLIQUANT, comme un joueur, et la question suivante arrive :
    // c'est la preuve que la chaîne des trois questions tourne dans l'interface.
    await choix.filter({ hasText: MOYENS[0]! }).click()
    const mobile = await avancerJusquALaQuestion(page, request, /^p_(50188|50189|50190)$/, 20)
    expect(mobile, "La question du MOBILE n'a pas suivi celle du moyen.").toBeTruthy()
    expect((mobile?.options ?? []).map((o) => String(o.name)).sort()).toEqual(
      MOBILES.map((id) => `p_${id}`).sort()
    )

    await page
      .locator('.demande-centrale button.af-action:not(.dc-pass)')
      .filter({ hasText: MOBILES[0]! })
      .click()
    const occasion = await avancerJusquALaQuestion(page, request, /^p_(50191|50192|50193)$/, 20)
    expect(occasion, "La question de l'OCCASION n'a pas suivi celle du mobile.").toBeTruthy()
    expect((occasion?.options ?? []).map((o) => String(o.name)).sort()).toEqual(
      OCCASIONS.map((id) => `p_${id}`).sort()
    )

    // La troisième réponse close l'accusation : l'accusé DÉCOULE de la
    // combinaison (correctif du 11/8/2026 dans 50168a), le joueur ne le choisit
    // pas. Aucune question ne doit donc demander un membre du Conseil ensuite.
    await page
      .locator('.demande-centrale button.af-action:not(.dc-pass)')
      .filter({ hasText: OCCASIONS[0]! })
      .click()
    const membre = await avancerJusquALaQuestion(page, request, /Chief|Officer/i, 12)
    expect(
      membre,
      "Un membre du Conseil est demandé au joueur : l'accusé doit découler de la combinaison."
    ).toBeUndefined()
  })
})
