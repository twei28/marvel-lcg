// Mener une VRAIE partie de campagne depuis un test, et rien de plus.
//
// Ce pilote est la recette du §10 de docs/CAMPAGNES.md, sortie de
// `campagne-panneau.spec.ts` pour servir aux autres epreuves de bout en bout
// (relevés automatiques du carnet, Professor Saved, accusation d'aos). Il est
// laisse VOLONTAIREMENT dans campagne-panneau, qui garde sa copie : ce test-la
// est la reference du montage, et le lier a un module partage voudrait dire
// qu'une retouche ici peut casser la preuve du panneau sans qu'on y pense.
//
// LES DEUX CONTRAINTES QUI SE CONTREDISENT PRESQUE
//
// * le plateau doit etre OUVERT : le moteur attend un client avant de poser sa
//   premiere question, et c'est le plateau qui affiche le panneau de fin ;
// * repondre en CLIQUANT serait intenable : la mise en place de Black Widow
//   demande deja de choisir un sbire parmi dix.
//
// D'ou le montage : on ouvre le plateau, mais on repond par `/get_ask` + `/post`,
// exactement comme le fait le navigateur, en prenant la premiere option legale.
// C'est le pilote de `tools/sonde_campagne.py`, transpose en HTTP. La fin de
// partie est ensuite forcee par `/debug`, la console que le joueur a sous la
// main.
//
// POURQUOI PAS LA SONDE
//
// `tools/sonde_campagne.py` execute ses commandes Puzzle « en direct, pas dans
// une file » : un `Puzzle.Damage(vilain, 100)` y retire bien les points de vie,
// mais la reponse forcee « After a villain is defeated » ne part jamais. Mesure
// faite sur Morlock Siege : sept vilains frappes a 100, zero vaincu, rien sous
// « Routed ». Tout ce qui depend d'une reaction en chaine se mesure donc EN
// PARTIE, ici, et pas a la sonde.
//
// ATTENTION : tout test qui importe ce module lance de VRAIES parties sur le
// serveur visé. Toute partie en cours y est perdue.
import { expect, type APIRequestContext, type Page } from '@playwright/test'

/** Les regles d'une partie de campagne, comme les compose `launcher.js`. */
export const REGLES_CAMPAGNE = [
  'v16_all',
  'no_crisis_of_infinite_deadpools',
  'no_encounter_cards_ignore_crisis',
  'mode_campaign',
]

export type Monde = Record<string, any>

/** Le descripteur de monde, tel que le plateau le recoit. */
export const monde = async (request: APIRequestContext): Promise<Monde> =>
  (await (await request.get('/get_world?p=0')).json()) as Monde

/**
 * Repond la premiere option legale, comme le pilote de la sonde.
 *
 * Rend `true` si une question attendait vraiment une reponse : sans ce retour,
 * une boucle d'attente ne saurait pas distinguer « rien a faire » de « le moteur
 * reflechit encore ».
 */
export async function repondre(request: APIRequestContext): Promise<boolean> {
  const brut = await (await request.get('/get_ask?p=0')).text()
  if (!brut.trim()) return false
  const ask = JSON.parse(brut) as { options_json?: string }
  const options = JSON.parse(ask.options_json ?? '[]') as Array<Record<string, unknown>>
  for (const o of options) {
    if (o && !o.failure_reason) {
      const legales = ((o.all_legal_targets as unknown[]) ?? []).map(String)
      const mini = ((o.target_num_range as number[]) ?? [0, 0])[0]
      const reponse = {
        id: String(o.id ?? 0),
        targets: mini ? legales.slice(0, mini) : [],
        resources: [],
      }
      await request.post('/post?p=0', { data: encodeURIComponent(JSON.stringify(reponse)) })
      return true
    }
  }
  return false
}

export type Lancement = {
  /** Identifiant de scenario, sans le suffixe `_expert`. */
  scenario: string
  /** Un ou plusieurs heros, par leur identifiant de deck de depart. */
  heros: string[]
  /** Le carnet de campagne applique a la mise en place. */
  carnet?: Record<string, string>
  /** Campagne experte : c'est le FICHIER de scenario qui change, pas une regle. */
  expert?: boolean
  seed?: number
}

/**
 * Monte la partie cote moteur, exactement comme le contrat `/new?data=`.
 *
 * L'expert prend la variante `<scenario>_expert` : c'est ce que fait
 * `resolveScenarioRaw` dans launcher.js, et une simple regle ne suffirait pas —
 * le fichier expert change le deck du vilain ET ajoute le set « expert ».
 */
export async function lancer(request: APIRequestContext, options: Lancement): Promise<void> {
  const nom = options.expert ? `${options.scenario}_expert` : options.scenario
  const definition = await (await request.get(`/get_scenario_json?${nom}`)).json()
  const decks: string[] = []
  for (const heros of options.heros) {
    decks.push(JSON.stringify(await (await request.get(`/get_hero_json?${heros}`)).json()))
  }
  await request.get(
    '/new?data=' +
      encodeURIComponent(
        JSON.stringify({
          campaign_json: JSON.stringify(definition),
          campaign_log: options.carnet ?? {},
          challenges: definition.challenges ?? [],
          encounter_set_names: [
            ...new Set([...(definition.encounter_sets ?? []), ...(definition.modular_sets ?? [])]),
          ],
          hero_json: decks,
          rules: REGLES_CAMPAGNE,
          seed: options.seed ?? 1234,
          timeout: 0,
        })
      )
  )
}

/**
 * Ouvre le plateau et traverse la mise en place et les mulligans.
 *
 * Sans navigateur, rien ne demarre : `/get_ask` reste vide tant qu'aucun client
 * ne s'est connecte. C'est pour ca que la page est ouverte ici et pas apres.
 */
export async function ouvrirEtMettreEnPlace(page: Page, request: APIRequestContext): Promise<void> {
  await page.goto('/app/board.html', { waitUntil: 'networkidle' })
  await page.waitForTimeout(2500)
  let vuLaMiseEnPlace = false
  for (let i = 0; i < 40; i++) {
    await repondre(request)
    const m = await monde(request)
    const phase = String(m.phase ?? '')
    const enPlace = phase.includes('Setup') || phase.includes('Mulligan') || phase.includes('Init')
    if (enPlace) vuLaMiseEnPlace = true
    if (phase && !enPlace) {
      // Garde contre le pire faux negatif du harnais : un moteur MORT continue de
      // repondre 200 sur `/get_world` avec l'etat FIGE de la partie precedente,
      // et `/new` n'y change rien. Sans ce controle, chaque commande semblait
      // n'avoir aucun effet et on accusait la commande. Ca s'est paye une heure :
      // `PutIntoPlay(carte, True)` (la console n'accepte qu'UN argument) avait
      // leve, puis une erreur fatale avait abattu le moteur, et tout ce qui
      // suivait mesurait un cadavre.
      if (!vuLaMiseEnPlace) {
        throw new Error(
          `Le moteur n'a pas pris la nouvelle partie (phase « ${phase} » des la premiere lecture). ` +
            'Serveur mort ou partie precedente encore en place : relancer serveur-dev.py.'
        )
      }
      return
    }
    await page.waitForTimeout(400)
  }
  throw new Error("La mise en place ne s'est jamais terminee.")
}

/** Les commandes `/debug` a envoyer, calculees sur l'etat courant du monde. */
export type Commandes = string | ((m: Monde) => string[])

async function debug(request: APIRequestContext, commande: string): Promise<void> {
  await request.get('/debug?' + encodeURIComponent(commande))
}

/**
 * Pousse la partie jusqu'a `game_over`, en repondant a tout ce qui vient.
 *
 * Les commandes sont rejouees regulierement, et non une fois : un scenario a
 * plusieurs vilains (Morlock Siege en a sept) demande de frapper CELUI QUI EST
 * EN JEU, et il change apres chaque defaite. D'ou la forme fonction.
 */
export async function acheverLaPartie(
  page: Page,
  request: APIRequestContext,
  commandes: Commandes,
  tours = 60
): Promise<Monde> {
  const envoyer = async () => {
    const m = await monde(request)
    const liste = typeof commandes === 'string' ? [commandes] : commandes(m)
    for (const c of liste) await debug(request, c)
  }
  for (let i = 0; i < tours; i++) {
    // A CHAQUE tour, pas tous les quatre : sur Morlock Siege le vilain change des
    // qu'il tombe, et un envoi espace laissait passer les nouveaux venus.
    await envoyer()
    await repondre(request)
    const m = await monde(request)
    if (m.game_over) return m
    await page.waitForTimeout(400)
  }
  throw new Error("La partie ne s'est jamais terminee.")
}

/**
 * Frappe a mort ce qui est dans la zone du vilain, quel qu'il soit.
 *
 * Par OBJECT ID (`c49`), et surtout pas par card_id ni par nom. Deux pieges,
 * mesures tous les deux :
 *
 * * le nom imprime des cartes uniques commence par une etoile (« * Blockbuster »),
 *   que le descripteur retire a l'affichage : une commande batie sur le nom du
 *   descripteur ne trouve rien, et la console ne s'en plaint pas ;
 * * une commande qui vise un card_id ABSENT DU JEU fabrique la carte
 *   (`FindOrCreateFace`), dans la zone mise de cote. Or le pilote lit le monde,
 *   puis envoie : au cycle suivant le vilain vient de mourir, la commande le
 *   recree — et `scenario.py` refuse alors la victoire, qui exige
 *   `aside_deck.FindCard(card_type=Villain) == None`. Mesure sur Sandman : les
 *   deux stades vaincus, la zone du vilain vide, et la partie qui ne se terminait
 *   JAMAIS. Deux doublons de Sandman I dormaient dans la zone mise de cote.
 *
 * L'object_id, lui, designe une carte qui existe deja : rien a fabriquer.
 * Les variables `c<id>` sont le langage de la console (« c: card # e.g. c19 c33 »).
 */
export const tuerLeVilainEnJeu = (m: Monde): string[] =>
  ((m.area_villain ?? []) as Array<Record<string, unknown>>)
    .filter((v) => v && typeof v.id === 'number')
    .map((v) => `Damage(c${Number(v.id)}, 100)`)

/** Blesse l'identite du joueur `siege`, par object_id pour les memes raisons. */
export function blesserIdentite(m: Monde, degats: number, siege = 0): string[] {
  const identite = ((m.players?.[siege]?.area_hero ?? []) as Array<Record<string, unknown>>)[0]
  return typeof identite?.id === 'number' ? [`Damage(c${Number(identite.id)}, ${degats})`] : []
}

/** Remet a zero la menace des manigances principales, pour ne pas perdre en route. */
export const viderLaMenacePrincipale = (m: Monde): string[] =>
  ((m.area_schemes_main ?? []) as Array<Record<string, unknown>>)
    .filter((s) => s && typeof s.id === 'number')
    .map((s) => `SetThreat(c${Number(s.id)}, 0)`)

/* --------------------------------------------------------- les campagnes -- */

export type Campagne = {
  id: string
  nom?: string
  code?: string
  carnet?: Record<string, string>
  termines?: string[]
  perdue?: boolean
  scoreFinal?: number
}

export const listeCampagnes = async (request: APIRequestContext): Promise<Campagne[]> =>
  (await (await request.get('/list_campagnes?')).json()) as Campagne[]

/** Supprime toutes les campagnes portant ce nom : un essai interrompu en laisse. */
export async function nettoyer(request: APIRequestContext, nom: string): Promise<void> {
  for (const c of await listeCampagnes(request)) {
    if (c.nom === nom) await request.post('/delete_campagne', { data: { id: c.id } })
  }
}

/** Pose (ou remplace) une campagne cote serveur et rend son identifiant. */
export async function poserCampagne(
  request: APIRequestContext,
  campagne: Record<string, unknown>
): Promise<string> {
  const reponse = await request.post('/save_campagne', { data: { campagne } })
  expect(reponse.status(), 'La campagne temoin n a pas pu etre ecrite.').toBe(200)
  return (await reponse.json()).id as string
}

export async function relireCampagne(
  request: APIRequestContext,
  identifiant: string
): Promise<Campagne> {
  const mienne = (await listeCampagnes(request)).find((c) => c.id === identifiant)
  expect(mienne, 'La campagne temoin a disparu du serveur.').toBeTruthy()
  return mienne as Campagne
}
