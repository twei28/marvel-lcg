// Mener une VRAIE partie de campagne depuis un test, et rien de plus.
//
// Ce pilote est la recette du §10 de docs/rapports/CAMPAGNES.md, sortie de
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
// Le contrat des demandes et du PAIEMENT est importe du client, pas recopie :
// `ui-app/src/board/ask.ts` est un module pur, sans un seul import, et c'est lui
// que le plateau utilise pour decider qu'une action est prete a partir. Le pilote
// paie donc exactement comme un joueur, et suivra le client s'il change. Le
// dupliquer aurait produit deux verites qui derivent en silence.
import {
  lireDemande as normaliserDemande,
  paiementCourant,
  paiementFacultatif,
  reponsePrete,
  type Option,
} from '../ui-app/src/board/ask'

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
export async function repondre(request: APIRequestContext, siege = 0): Promise<boolean> {
  const brut = await (await request.get(`/get_ask?p=${siege}`)).text()
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
      await request.post(`/post?p=${siege}`, { data: encodeURIComponent(JSON.stringify(reponse)) })
      return true
    }
  }
  return false
}

/* ------------------------------------------------- jouer, pas seulement finir -- */

/**
 * Une demande du moteur, telle que `/get_ask` la rend.
 *
 * `show_cancel` est la clef de tout : quand il est vrai, le joueur a le DROIT de
 * ne rien faire, et le contrat dit qu'on l'exprime en postant `{}` (voir
 * `ui-app/src/board/moteur.ts`, `envoyerReponse(null)`). C'est ce qui manquait au
 * pilote : sans jamais passer, il restait bloque dans le tour du joueur, aucune
 * phase ne se terminait, et tout ce qui pend a une fin de phase — la Reponse de
 * l'etape 1B d'aos, le tour du vilain, la montee de la menace — n'arrivait jamais.
 */
export type Demande = {
  /** Options JOUABLES seulement : celles que le moteur refuse sont ecartees. */
  options: Option[]
  show_cancel: boolean
  ability_type: string
}

export async function lireDemande(
  request: APIRequestContext,
  siege = 0
): Promise<Demande | undefined> {
  const brut = await (await request.get(`/get_ask?p=${siege}`)).text()
  if (!brut.trim()) return undefined
  let ask: Record<string, unknown>
  try {
    ask = JSON.parse(brut) as Record<string, unknown>
  } catch {
    return undefined
  }
  const normalisee = normaliserDemande(ask)
  if (!normalisee) return undefined
  return {
    options: normalisee.options.filter((o) => o.failure_reason === ''),
    show_cancel: normalisee.show_cancel,
    ability_type: normalisee.ability_type,
  }
}

/** Ne rien faire, et le dire : c'est ce qui termine une phase de joueur. */
export async function passer(request: APIRequestContext, siege = 0): Promise<void> {
  await request.post(`/post?p=${siege}`, { data: encodeURIComponent('{}') })
}

/** Le moteur peut-il satisfaire les cibles que cette option exige ? */
const cibleTenable = (option: Option): boolean =>
  option.target_num_range[0] <= option.all_legal_targets.length

/**
 * Les ressources a depenser pour cette option, ou `undefined` si le pilote ne
 * peut pas la payer.
 *
 * On empile les moyens que le moteur propose (`target_payment[cible].payment`)
 * jusqu'a ce que `reponsePrete` dise oui. C'est la MEME fonction que celle qui
 * debloque le bouton « Valider » du plateau, donc la meme reponse : un cout
 * exprime en types (« BY » = une energie ET une mentale) ne se satisfait pas en
 * comptant, et un cout « UpTo » se paie a zero.
 *
 * Les exemplaires comptent : le moteur repete un effet dans `payment` autant de
 * fois qu'il est disponible, et une carte a double ressource vaut 2 d'un coup.
 */
export function ressourcesPour(option: Option, cibles: number[]): number[] | undefined {
  const paiement = paiementCourant(option, cibles)
  if (reponsePrete(option, cibles, []).prete) return []
  if (!paiement || paiementFacultatif(paiement)) return []

  const choisies: number[] = []
  for (const moyen of paiement.payment) {
    choisies.push(moyen.effect_id)
    if (reponsePrete(option, cibles, choisies).prete) return choisies
  }
  return undefined
}

/** Les cibles retenues pour cette option : celles voulues d'abord, sinon les premieres. */
function ciblesPour(option: Option, voulues: readonly number[] = []): number[] {
  const [mini, maxi] = option.target_num_range
  if (maxi === 0) return []
  const legales = option.all_legal_targets
  const preferees = voulues.filter((id) => legales.includes(id))
  const reste = legales.filter((id) => !preferees.includes(id))
  return [...preferees, ...reste].slice(0, Math.max(mini, Math.min(1, maxi)))
}

/**
 * Retient cette option, cibles et ressources comprises.
 *
 * Rend `false` sans rien envoyer si le cout n'est pas payable : c'est ce qui
 * permet a la conduite de passer a l'option suivante plutot que d'envoyer une
 * reponse que le moteur refusera sans explication.
 */
export async function choisir(
  request: APIRequestContext,
  option: Option,
  voulues: readonly number[] = [],
  siege = 0
): Promise<boolean> {
  const cibles = ciblesPour(option, voulues)
  const ressources = ressourcesPour(option, cibles)
  if (ressources === undefined) return false
  await request.post(`/post?p=${siege}`, {
    data: encodeURIComponent(
      JSON.stringify({ id: String(option.id), targets: cibles.map(String), resources: ressources })
    ),
  })
  return true
}

/** Les noms d'options du moteur. Mesures sur une vraie partie, jamais devines. */
const estFinDePhase = (option: Option) => /^End[ _]Phase$/i.test(option.name)
const estAttaque = (option: Option) => /^Attack$/i.test(option.name)
const estDejouement = (option: Option) => /^Thwart$/i.test(option.name)
const estDefense = (option: Option) => /^Defense$/i.test(option.name)
const estChangementDeForme = (option: Option) => /^Change[ _]Form$/i.test(option.name)
const estJouerUneCarte = (option: Option) => /^Play$/i.test(option.name)

/** Une option utilisable : jouable, et avec de quoi cibler si elle l'exige. */
const utilisable = (option: Option) =>
  cibleTenable(option) && (option.target_num_range[1] > 0 || option.target_num_range[0] === 0)

export type Arret = (etat: { monde: Monde; demande?: Demande }) => boolean

/**
 * Comment le pilote se conduit pendant le tour du joueur.
 *
 * Sans conduite il ne fait RIEN et passe : c'est le comportement d'origine, celui
 * qui suffit a faire tourner les phases. Avec une conduite, il joue.
 */
export type Conduite = {
  /**
   * Complots a DEJOUER en priorite, par object_id. Le pilote y consacre son
   * activation tant qu'ils sont sur la table : c'est ainsi qu'on vainc une
   * manigance MISSION, ce qu'aucune commande de console ne sait faire.
   */
  dejouer?: readonly number[]
  /** Attaquer l'ennemi quand il n'y a rien a dejouer. */
  attaquer?: boolean
  /** Cibles d'attaque preferees, par object_id (le vilain plutot qu'un sbire). */
  attaquerDAbord?: readonly number[]
  /** Jouer les cartes de la main qu'on peut payer. Defaut : false. */
  jouerDesCartes?: boolean
  /**
   * Types de cartes a jouer EN PRIORITE (« Ally », « Upgrade », « Event »…).
   *
   * L'option de jeu s'appelle « Play » quelle que soit la carte : c'est son
   * `bind_id` qui dit laquelle, et on le retrouve dans la main du joueur. Sans
   * cette preference, le pilote joue la premiere carte payable, ce qui ne suffit
   * pas quand une regle attend un type precis — la tentative de mission d'aoa
   * exige un ALLIE a la mission, et un allie n'arrive a la mission que joue.
   */
  jouerDAbord?: readonly string[]
  /**
   * Actions a declencher en priorite, par motif sur leur nom.
   *
   * C'est ainsi qu'on utilise une carte pour ce qu'elle fait, et non pour son
   * type : « Make a mission attempt » (Mission Team, aoa) est la SEULE facon de
   * retirer de la menace d'une manigance MISSION — la carte 45170a annule tout
   * retrait dont la source n'est pas Mission Team, donc l'action Thwart du heros
   * n'y fait rien du tout (mesure : menace 5/5 inchangee sur dix tours de
   * dejouement).
   */
  actions?: readonly RegExp[]
  /** Rester en forme HEROS : sans cela, un alter-ego ne peut ni attaquer ni dejouer. */
  resterEnHeros?: boolean
  /**
   * Se defendre contre les attaques. Defaut : NON, et c'est important.
   *
   * Une defense coute l'activation du heros. En se defendant a chaque attaque, il
   * arrive epuise a son tour et le moteur ne lui propose plus ni Attack ni Thwart :
   * mesure sur Rhino, ou le pilote « dejouait » sans qu'aucune option Thwart ne
   * soit jamais offerte, la menace montant jusqu'a la defaite. Encaisser est
   * d'ailleurs le choix courant d'un joueur.
   */
  seDefendre?: boolean
  /**
   * Dejouer la manigance principale quand sa menace approche sa cible, attaquer
   * sinon. C'est l'arbitrage que fait tout joueur, et sans lui le pilote frappe
   * le vilain jusqu'a ce que le complot se complete : mesure sur Morlock Siege,
   * un Maraudeur mis en deroute puis la partie perdue sur la manigance.
   */
  equilibrer?: boolean
}

/** Le joueur est-il en forme alter-ego ? Il ne peut alors ni attaquer ni dejouer. */
function enAlterEgo(m: Monde, siege = 0): boolean {
  const identite = ((m.players?.[siege]?.area_hero ?? []) as Array<Record<string, unknown>>)[0]
  return String(identite?.card_type ?? '') === 'AlterEgo'
}

/**
 * Une action du tour de joueur, dans l'ordre de la conduite. Rend `true` si
 * quelque chose a ete envoye.
 *
 * L'ordre compte : reprendre la forme heros AVANT tout, parce qu'un alter-ego
 * n'a ni attaque ni deviation ; puis dejouer ce qu'on a demande de dejouer ;
 * puis attaquer ; puis jouer une carte payable ; sinon passer.
 */
async function agir(
  request: APIRequestContext,
  demande: Demande,
  conduite: Conduite,
  m: Monde,
  siege = 0
): Promise<boolean> {
  const options = demande.options.filter(utilisable)

  if (conduite.resterEnHeros && enAlterEgo(m, siege)) {
    const forme = options.find(estChangementDeForme)
    if (forme && (await choisir(request, forme, [], siege))) return true
  }

  for (const motif of conduite.actions ?? []) {
    const action = options.find((o) => motif.test(o.name))
    if (action && (await choisir(request, action, [], siege))) return true
  }

  const aDejouer = conduite.dejouer ?? []
  if (aDejouer.length) {
    const thwart = options.find(
      (o) => estDejouement(o) && o.all_legal_targets.some((id) => aDejouer.includes(id))
    )
    if (thwart && (await choisir(request, thwart, aDejouer, siege))) return true
  }

  if (conduite.equilibrer) {
    const principale = ((m.area_schemes_main ?? []) as Array<Record<string, any>>)[0]
    const menace = Number(principale?.info?.k_threat ?? 0)
    const cible = Number(principale?.info?.target_threat ?? Number.POSITIVE_INFINITY)
    const vilain = ((m.area_villain ?? []) as Array<Record<string, any>>).find(
      (v) => v?.card_type === 'EncounterVillain'
    )
    const presqueMort = Number(vilain?.info?.health ?? 99) <= 4
    // A MI-CHEMIN, pas a deux pions de la fin : la menace saute par paliers (une
    // manigance qui s'avance, un pion acceleration, un boost), et attendre le
    // dernier moment fait perdre la partie sur un seul tour de vilain. Mesure sur
    // Rhino : avec un seuil a « cible - 2 », la menace est passee de 2/7 a 7/7
    // dans le meme bloc de tours, le vilain a 3 points de vie.
    // Exception : un vilain presque mort se termine, sinon on dejoue pour rien
    // pendant que la partie etait gagnable.
    if (principale && Number.isFinite(cible) && !presqueMort && menace * 2 >= cible) {
      const thwart = options.find(estDejouement)
      if (thwart && (await choisir(request, thwart, [Number(principale.id)], siege))) return true
    }
  }

  if (conduite.attaquer) {
    const attaque = options.find(estAttaque)
    if (attaque && (await choisir(request, attaque, conduite.attaquerDAbord ?? [], siege))) return true
  }

  if (conduite.jouerDesCartes) {
    const main = (m.players?.[siege]?.hand_cards ?? []) as Array<Record<string, any>>
    const typeDe = (option: Option) =>
      String(main.find((c) => Number(c.id) === option.bind_id)?.card_type ?? '')
    const jouables = options.filter(estJouerUneCarte)
    const prefs = conduite.jouerDAbord ?? []
    const ordonnees = [
      ...prefs.flatMap((type) => jouables.filter((o) => typeDe(o) === type)),
      ...jouables.filter((o) => !prefs.includes(typeDe(o))),
    ]
    for (const carte of ordonnees) {
      if (await choisir(request, carte, [], siege)) return true
    }
  }

  return false
}

/**
 * Fait TOURNER la partie jusqu'a `arret`, et la JOUE si on lui donne une conduite.
 *
 * La regle de conduite, dans cet ordre :
 *
 * 1. une REPONSE ou une INTERRUPTION proposee est acceptee. Ce sont les crochets
 *    du scenario (« Place 2 secret counters… », « Advance to stage 2A ») : les
 *    refuser fige l'histoire, et c'est precisement ce qu'on veut voir se
 *    declencher ;
 * 2. « Defense » est retenue : se defendre coute une activation mais evite de
 *    perdre le heros, et un heros elimine ne touche plus aucune recompense ;
 * 3. la conduite agit (forme heros, dejouer, attaquer, jouer) ;
 * 4. « End Phase » est retenu : c'est lui qui fait tourner les phases ;
 * 5. si le moteur autorise de ne rien faire (`show_cancel`), on passe ;
 * 6. sinon la question est FORCEE : on repond la premiere option tenable.
 */
export async function avancerLaPartie(
  page: Page,
  request: APIRequestContext,
  arret: Arret,
  tours = 60,
  conduite: Conduite = {}
): Promise<Monde> {
  for (let i = 0; i < tours; i++) {
    // Le siege QUI PARLE : on prend le premier qui a une question. A un joueur
    // c'est toujours 0, a plusieurs c'est celui dont c'est le tour.
    let siege = 0
    let demande: Demande | undefined
    for (const candidat of await sieges(request)) {
      const vue = await lireDemande(request, candidat)
      if (vue) {
        siege = candidat
        demande = vue
        break
      }
    }
    const m = await monde(request)
    // L'arret est evalue AVANT de repondre : c'est la seule facon de s'arreter
    // SUR une question, ce que demande la verification de l'interface — y
    // repondre la ferait disparaitre avant que le DOM n'ait bouge.
    if (arret({ monde: m, demande })) return m
    if (m.game_over) return m

    if (!demande) {
      // Le carre de la phase du mechant (397331a5, 05/10/2026) attend un clic sur
      // « Suivant » a chaque etape : sans question au moteur, c'est lui qui retient
      // la partie. Un joueur le clique ; le pilote aussi.
      // Sur la table, le carre se replie en un bouton rond numerote (18969bfe) :
      // c'est lui qu'on clique alors, comme dans annonce-attend-le-clic.spec.ts.
      // Le bouton s'appelle « Suivant (Espace) », puis « Terminer » au bilan : on vise
      // sa classe, `.deroule-suivant`, plutot que son libelle.
      const suivant = page.locator('.deroule-suivant').first()
      const rond = page.locator('.deroule-rond').first()
      // Clic BORNE : un bouton visible mais recouvert ferait attendre Playwright
      // jusqu'a la fin du test. A defaut, la touche Espace que le bouton annonce.
      if ((await suivant.count()) && (await suivant.isVisible().catch(() => false))) {
        await suivant.click({ timeout: 2000 }).catch(() => page.keyboard.press('Space').catch(() => undefined))
      } else if ((await rond.count()) && (await rond.isVisible().catch(() => false))) {
        await rond.click({ timeout: 2000 }).catch(() => undefined)
      }
    }
    if (demande) {
      const tenables = demande.options.filter(cibleTenable)
      const reponse = /Response|Interrupt/i.test(demande.ability_type) ? tenables[0] : undefined
      const defense = conduite.seDefendre ? tenables.find(estDefense) : undefined
      const finDePhase = tenables.find(estFinDePhase)
      if (reponse) await choisir(request, reponse, [], siege)
      else if (defense) await choisir(request, defense, [], siege)
      else if (await agir(request, demande, conduite, m, siege)) {
        /* la conduite a joue */
      } else if (finDePhase) await choisir(request, finDePhase, [], siege)
      else if (demande.show_cancel) await passer(request, siege)
      else {
        // Question FORCEE. On ecarte quand meme la defense si elle n'est pas
        // demandee : elle est toujours facultative, et elle couterait l'activation.
        const forcee = tenables.find((o) => conduite.seDefendre || !estDefense(o))
        if (!forcee || !(await choisir(request, forcee, [], siege))) await passer(request, siege)
      }
    }
    await page.waitForTimeout(300)
  }
  return await monde(request)
}

/**
 * Avance jusqu'a ce que le moteur pose une question dont une option porte ce
 * motif, et s'arrete SANS y repondre.
 *
 * `AskChoosePaper` prefixe ses options de « p_ » (player_ask.py) et le plateau les
 * affiche comme des boutons ordinaires, texte nettoye : c'est le seul moyen de
 * voir une question de l'accusation dans l'interface.
 */
export async function avancerJusquALaQuestion(
  page: Page,
  request: APIRequestContext,
  motif: RegExp,
  tours = 60,
  conduite: Conduite = {}
): Promise<Demande | undefined> {
  let trouvee: Demande | undefined
  await avancerLaPartie(
    page,
    request,
    ({ demande }) => {
      if (demande && demande.options.some((o) => motif.test(o.name))) {
        trouvee = demande
        return true
      }
      return false
    },
    tours,
    conduite
  )
  return trouvee
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
  /**
   * Les regles de la partie. Defaut : `REGLES_CAMPAGNE`.
   *
   * Une partie ORDINAIRE (hors campagne) se lance avec les trois premieres,
   * sans `mode_campaign` : c'est ce que `ui-check/contrat-nouvelle-partie.json`
   * appelle `regles_partie_standard`, et ce qu'envoie l'ecran de preparation
   * quand on ne coche aucun mode.
   */
  regles?: readonly string[]
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
          rules: [...(options.regles ?? REGLES_CAMPAGNE)],
          seed: options.seed ?? 1234,
          timeout: 0,
        })
      )
  )
}

/** Les sieges de la partie, dans l'ordre. Un seul en solo. */
export async function sieges(request: APIRequestContext): Promise<number[]> {
  const m = await monde(request)
  const total = ((m.players ?? []) as unknown[]).length || 1
  return [...Array(total).keys()]
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
  for (let i = 0; i < 60; i++) {
    // TOUS les sieges, pas seulement le premier : a plusieurs heros, chacun a ses
    // propres questions de mise en place sur `/get_ask?p=<siege>`, et n'en servir
    // qu'un fait attendre le moteur indefiniment (mesure a deux heros : la mise en
    // place ne se terminait jamais).
    for (const siege of await sieges(request)) await repondre(request, siege)
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
