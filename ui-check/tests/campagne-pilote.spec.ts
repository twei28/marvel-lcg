// Le pilote joue : il paie, il joue, il attaque, il déjoue, il se défend.
//
// Jusqu'ici le harnais savait deux choses : répondre aux questions de mise en
// place, et forcer une fin de partie par `/debug`. Tout ce qui demandait de JOUER
// lui échappait, et deux entrées de couverture attendaient ça (elles sont tombées
// avec `campagne-accusation.spec.ts`).
//
// Ce test-ci ne vérifie aucune règle de campagne : il vérifie LE PILOTE, geste par
// geste, sur des faits mesurés. C'est le filet qui protège tous les autres tests
// de vraies parties — si le contrat de `/post` change, c'est ici que ça se voit,
// pas dans un test de campagne qui échouerait pour une raison obscure.
//
// LE GESTE QUI DÉBLOQUE TOUT LE RESTE : payer. Le pilote importe le contrat du
// client (`ui-app/src/board/ask.ts`), donc il paie exactement comme un joueur :
// `reponsePrete` est la fonction qui débloque le bouton « Valider » du plateau.
//
// CE QUE LE PILOTE NE SAIT PAS FAIRE : gagner. Il joue les gestes, il ne joue pas
// une STRATÉGIE. Mesure sur Rhino, en attaquant et en déjouant au seuil de la
// moitié : le vilain descend de 14 à 3 points de vie, et la manigance principale
// se complète quand même (2/7 → 7/7 dans le même bloc de tours). Achever une
// partie reste donc l'affaire de `/debug`, et un bot qui gagnerait vraiment est un
// autre chantier — une IA de jeu, pas un pilote de test.
//
//   npm run campagne-pilote
//
// ATTENTION : ce test lance de VRAIES parties. Toute partie en cours sur le
// serveur visé est perdue.
import { test, expect } from '@playwright/test'
import { avancerLaPartie, lancer, monde, ouvrirEtMettreEnPlace, type Monde } from '../pilote-campagne'

/** Rhino : un vilain, une manigance, aucune subtilité. Le banc d'essai idéal. */
const SCENARIO = 'rhino'
const HEROS = 'colossus'

const vilain = (m: Monde): Record<string, any> | undefined =>
  ((m.area_villain ?? []) as Array<Record<string, any>>).find(
    (v) => v?.card_type === 'EncounterVillain'
  )
const pvDuVilain = (m: Monde): number => Number(vilain(m)?.info?.health ?? 0)
const menacePrincipale = (m: Monde): number =>
  Number(((m.area_schemes_main ?? []) as Array<Record<string, any>>)[0]?.info?.k_threat ?? 0)
const idPrincipale = (m: Monde): number =>
  Number(((m.area_schemes_main ?? []) as Array<Record<string, any>>)[0]?.id ?? 0)
const cartesEnMain = (m: Monde): number => ((m.players?.[0]?.hand_cards ?? []) as unknown[]).length
/** Ce que le joueur a posé devant lui : alliés, soutiens, améliorations. */
const cartesPosees = (m: Monde): Array<Record<string, any>> => {
  const joueur = m.players?.[0]
  const hero = ((joueur?.area_hero ?? []) as Array<Record<string, any>>).slice(1)
  return [
    ...((joueur?.allies ?? []) as Array<Record<string, any>>),
    ...((joueur?.supports ?? []) as Array<Record<string, any>>),
    ...hero,
  ]
}

/**
 * Les cartes posées qui ont COÛTÉ quelque chose.
 *
 * C'est la seule mesure honnête du paiement : compter les cartes qui quittent la
 * main ne prouve rien, puisque la main se recharge à chaque fin de tour, et une
 * carte gratuite s'y voit comme une carte payée. Une carte de coût 2 posée devant
 * le joueur, en revanche, a forcément été payée.
 */
const cartesPayantes = (m: Monde): Array<Record<string, any>> =>
  cartesPosees(m).filter((c) => Number(c.cost ?? 0) > 0)

test.describe.serial('Le pilote joue une vraie partie', () => {
  test.setTimeout(300000)

  test('Il paie un coût et pose la carte devant lui', async ({ page, request }) => {
    await lancer(request, { scenario: SCENARIO, heros: [HEROS] })
    await ouvrirEtMettreEnPlace(page, request)
    const avant = await monde(request)
    expect(cartesPayantes(avant), 'Le joueur a déjà une carte payante en jeu au départ.').toHaveLength(0)

    const apres = await avancerLaPartie(
      page,
      request,
      ({ monde: m }) => cartesPayantes(m).length > 0,
      30,
      { jouerDesCartes: true, resterEnHeros: true }
    )
    const payantes = cartesPayantes(apres)
    expect(
      payantes.length,
      "Aucune carte payante posée : le pilote ne sait pas payer un coût."
    ).toBeGreaterThan(0)
    // Le coût est lu sur la carte elle-même : elle est devant le joueur, donc elle
    // a été payée, ressource par ressource, par la même fonction que le plateau.
    expect(
      Math.max(...payantes.map((c) => Number(c.cost ?? 0))),
      'La carte posée ne coûtait rien : le paiement n’est pas prouvé.'
    ).toBeGreaterThan(0)
    expect(cartesEnMain(apres), 'La main n’a pas bougé.').toBeLessThan(cartesEnMain(avant))
  })

  test('Il attaque, et le vilain perd vraiment des points de vie', async ({ page, request }) => {
    await lancer(request, { scenario: SCENARIO, heros: [HEROS] })
    await ouvrirEtMettreEnPlace(page, request)
    const avant = await monde(request)
    const pvDepart = pvDuVilain(avant)
    expect(pvDepart, "Le vilain n'est pas en jeu.").toBeGreaterThan(0)

    const apres = await avancerLaPartie(
      page,
      request,
      ({ monde: m }) => pvDuVilain(m) < pvDepart,
      25,
      { attaquer: true, jouerDesCartes: true, resterEnHeros: true }
    )
    expect(
      pvDuVilain(apres),
      "Le vilain n'a pas perdu un seul point de vie : aucune attaque n'a abouti."
    ).toBeLessThan(pvDepart)
  })

  test('Il déjoue, et la menace de la manigance baisse', async ({ page, request }) => {
    await lancer(request, { scenario: SCENARIO, heros: [HEROS] })
    await ouvrirEtMettreEnPlace(page, request)
    // La manigance part à ZÉRO menace : il n'y a rien à déjouer avant que le vilain
    // n'ait manigancé. On laisse donc le temps tourner sans rien faire, ce qui est
    // exactement le comportement du pilote sans conduite.
    const montee = await avancerLaPartie(page, request, ({ monde: m }) => menacePrincipale(m) >= 2, 25)
    const menaceDepart = menacePrincipale(montee)
    expect(menaceDepart, "La menace n'a jamais monté : rien à déjouer.").toBeGreaterThanOrEqual(2)

    // On ne demande QUE le déjouement : sans cela une attaque prendrait
    // l'activation, et la baisse ne prouverait rien.
    const apres = await avancerLaPartie(
      page,
      request,
      ({ monde: m }) => menacePrincipale(m) < menaceDepart,
      25,
      { dejouer: [idPrincipale(montee)], attaquer: false, resterEnHeros: true }
    )
    expect(
      menacePrincipale(apres),
      "La menace n'a jamais baissé : le pilote ne sait pas déjouer."
    ).toBeLessThan(menaceDepart)
  })

  test('Il vainc un stade de vilain sans aucun /debug', async ({ page, request }) => {
    // Morlock Siege : sept Maraudeurs de 9 à 11 points de vie, et le premier
    // vaincu part sous « Routed ». C'est la mesure la plus nette qu'on puisse
    // faire : une carte quitte la table par le seul effet du jeu.
    await lancer(request, { scenario: 'morlock_siege', heros: [HEROS] })
    await ouvrirEtMettreEnPlace(page, request)

    const routed = (m: Monde) =>
      ((m.area_environment ?? []) as Array<Record<string, any>>).find(
        (e) => String(e.card_id) === '40081a'
      )
    const enDeroute = (m: Monde) => {
      const carte = routed(m)
      return ((m.area_environment ?? []) as Array<Record<string, any>>).filter(
        (e) => carte && e.bind_object_id === carte.id
      ).length
    }

    const apres = await avancerLaPartie(page, request, ({ monde: m }) => enDeroute(m) > 0, 60, {
      attaquer: true,
      jouerDesCartes: true,
      resterEnHeros: true,
      equilibrer: true,
    })
    expect(
      enDeroute(apres),
      'Aucun Maraudeur mis en déroute : le pilote n’a pas vaincu un seul vilain en jouant.'
    ).toBeGreaterThan(0)
  })

  test('Il mène une tentative de mission, à deux héros (aoa)', async ({ page, request }) => {
    // C'EST LE GESTE LE PLUS COMPLET DU JEU, et il n'avait jamais été joué :
    //
    //   1. jouer un ALLIÉ, donc payer, et l'allié rejoint la mission
    //      (`AllyToMission` lui pose un compteur « mission ») ;
    //   2. déclencher l'action nommée « Make a mission attempt » de Mission Team,
    //      qui exige au moins un allié à la mission ;
    //   3. la tentative défausse des cartes du deck, apparie leurs icônes à celles
    //      des alliés, frappe le surveillant posté avec leur ATK et retire de la
    //      menace avec leur THW, puis pose un compteur d'essai.
    //
    // Rien de tout cela ne se pilote autrement : la manigance MISSION annule tout
    // retrait de menace dont la source n'est pas Mission Team (45170a), et un
    // surveillant posté à la mission est immunisé à tout ce qui ne vient pas d'une
    // tentative (missions.py). Mesuré : dix tours d'action Thwart la laissent à
    // 5/5, et `Damage` par la console ne l'entame pas.
    //
    // À DEUX HÉROS, parce que la mission compte 5 menaces PAR JOUEUR et qu'un seul
    // allié ne fait rien avancer.
    await lancer(request, { scenario: 'en_sabah_nur', heros: [HEROS, 'cyclops'], carnet: {} })
    await ouvrirEtMettreEnPlace(page, request)

    const mission = (m: Monde) =>
      ((m.area_schemes_side ?? []) as Array<Record<string, any>>).find(
        (c) => String(c.card_id) === '45170a'
      )
    const alliesALaMission = (m: Monde) =>
      ((m.players ?? []) as Array<Record<string, any>>).flatMap((j) =>
        ((j?.allies ?? []) as Array<Record<string, any>>).filter(
          (a) => Number(a?.info?.c_mission ?? 0) > 0
        )
      ).length
    /** Le surveillant posté à la mission, et ses points de vie. */
    const surveillant = (m: Monde) =>
      [
        ...((m.area_villain ?? []) as Array<Record<string, any>>),
        ...((m.players ?? []) as Array<Record<string, any>>).flatMap(
          (j) => (j?.engaged_enemies ?? []) as Array<Record<string, any>>
        ),
      ].find((c) => Number(c?.info?.c_mission ?? 0) > 0)

    const avant = await monde(request)
    expect(mission(avant), "La mission « Protect the Professor » n'est pas en jeu.").toBeTruthy()
    const pvSurveillantDepart = Number(surveillant(avant)?.info?.health ?? 0)
    expect(pvSurveillantDepart, "Aucun surveillant n'est posté à la mission.").toBeGreaterThan(0)

    const conduite = {
      actions: [/mission[ _]attempt/i],
      jouerDesCartes: true,
      // Un ALLIÉ d'abord : c'est la seule carte qui rejoint la mission, et sans
      // allié à la mission l'action « Make a mission attempt » n'est pas offerte.
      jouerDAbord: ['Ally'],
      resterEnHeros: true,
      attaquer: false,
    }

    let etat = avant
    for (let bloc = 0; bloc < 12; bloc++) {
      etat = await avancerLaPartie(
        page,
        request,
        ({ monde: m }) =>
          Boolean(m.game_over) ||
          (Number(mission(m)?.info?.c_mission ?? 0) > 0 &&
            Number(surveillant(m)?.info?.health ?? 99) < pvSurveillantDepart),
        6,
        conduite
      )
      if (
        etat.game_over ||
        (Number(mission(etat)?.info?.c_mission ?? 0) > 0 &&
          Number(surveillant(etat)?.info?.health ?? 99) < pvSurveillantDepart)
      ) {
        break
      }
    }

    expect(alliesALaMission(etat), "Aucun allié n'a rejoint la mission.").toBeGreaterThan(0)
    expect(
      Number(mission(etat)?.info?.c_mission ?? 0),
      "Aucune tentative de mission n'a été menée : l'action nommée n'a jamais été utilisée."
    ).toBeGreaterThan(0)
    expect(
      Number(surveillant(etat)?.info?.health ?? 99),
      "Le surveillant n'a rien pris : les dégâts d'une tentative ne portent pas."
    ).toBeLessThan(pvSurveillantDepart)
  })

  test('Il sert TOUS les sièges : à deux héros, la mise en place aboutit', async ({
    page,
    request,
  }) => {
    // Chaque siège a ses propres questions sur `/get_ask?p=<siège>`. N'en servir
    // qu'un fait attendre le moteur indéfiniment : mesuré à deux héros, la mise en
    // place ne se terminait jamais et le pilote levait au bout de 40 tours.
    await lancer(request, { scenario: 'rhino', heros: [HEROS, 'cyclops'] })
    await ouvrirEtMettreEnPlace(page, request)
    const m = await monde(request)
    expect(((m.players ?? []) as unknown[]).length, 'La partie n’a pas deux joueurs.').toBe(2)
    for (const [index, joueur] of ((m.players ?? []) as Array<Record<string, any>>).entries()) {
      expect(
        ((joueur?.hand_cards ?? []) as unknown[]).length,
        `Le joueur ${index + 1} n'a pas de main : sa mise en place n'a pas été jouée.`
      ).toBeGreaterThan(0)
    }
  })
})
