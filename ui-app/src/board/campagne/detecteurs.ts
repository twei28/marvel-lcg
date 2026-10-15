// Détecteurs de campagne — ce que la partie qui vient de s'achever a produit.
//
// Le livret demande au joueur de reporter des résultats à la main dans son
// carnet : les pions retard laissés sur la manigance, les alliés secourus, qui
// était encore engagé, les PV restants. Le moteur connaît déjà tout cela — il
// n'y a aucune raison de le redemander. Ces fonctions lisent le descripteur de
// monde et rendent la valeur EXACTEMENT dans la forme qu'attend le carnet
// (`campaign_log`), pour qu'il n'y ait pas de traduction entre les deux.
//
// Le format du carnet, côté moteur (game/operate/campaign_logs.py) :
//   liste  -> "id1;id2"      (Get*List découpe sur « ; »)
//   entier -> "3"
// Une clé absente vaut « rien » : on n'écrit donc jamais de chaîne vide.
//
// TOUT ce qui est lu ici a été constaté sur des parties réelles, jamais déduit
// du code du moteur : voir detecteurs.test.ts, dont les cas viennent de
// descripteurs capturés en jouant les scénarios de Rise of Red Skull.
import type { World, WorldCard, WorldPlayer } from '../world'

/** Un champ de victoire, tel que data/campagnes/<code>.json le décrit. */
export type ChampVictoire = {
  cle: string
  type: 'auto' | 'choix'
  format?: 'liste' | 'int' | 'liste-joueurs'
  parJoueur?: boolean
  obligatoire?: boolean
  detection?: string
  condition?: string
  /**
   * Le carnet CUMULE ce champ d'un scénario à l'autre : la valeur détectée est
   * ce que la partie vient d'ajouter, pas le total. Voir `preRemplir`.
   */
  cumulatif?: boolean
  /**
   * Ce champ se TIRE AU SORT, aux paliers d'une piste chiffrée du carnet.
   *
   * Le livret de Sinister Motives (piste de réputation, p.22) dit trois fois
   * « Choose one "Osborn Tech" attachment at random » : ce n'est pas une décision
   * du joueur, c'est un tirage, donc le jeu peut le faire. `paliers` donne les
   * valeurs de piste qui déclenchent chacun un tirage, et `cle_piste` la clé qui
   * porte le total.
   */
  tirage?: {
    cle_piste: string
    paliers: number[]
  }
  parametres?: {
    compteur?: string
    complot?: string
    type?: string
    zone?: string
    trait?: string
  }
  libelle: string
  aide?: string
  options?: string[]
  /**
   * Un tableau de cases à cocher (« Cooperation Progress » de Skrull Menace) : une ligne par carte,
   * une case par exigence. Le carnet garde « Titre: exigence » pour chaque case cochée.
   */
  cases?: Array<{ titre: string; exigences: string[] }>
}

const SEP = ';'

export const enListe = (ids: readonly string[]): string => ids.join(SEP)
export const deListe = (valeur: string | undefined): string[] =>
  (valeur ?? '').split(SEP).filter(Boolean)

/**
 * Zones où une carte n'est PAS considérée comme entrée en jeu.
 *
 * Les armes expérimentales attendent dans un deck ; elles ne comptent que si
 * elles en sont sorties. Le deck de rencontre en fait partie : une arme qui y a
 * été mélangée sans jamais être révélée n'est pas entrée en jeu non plus.
 *
 * `additional_decks` EST dans la liste, et ce n'est pas theorique : mesuré sur
 * une vraie partie de Crossbones, le deck des Armes Experimentales est un deck
 * ADDITIONNEL. Sans cette exclusion, les quatre armes etaient declarees entrees
 * en jeu alors qu'une seule etait attachee au vilain — et la campagne entiere
 * en heritait, chaque scenario suivant recevant trois armes de trop.
 *
 * `additional_discard_piles` n'y est PAS, volontairement : le livret dit qu'une
 * arme entree en jeu puis defaussee part a la defausse de rencontre, donc tout
 * ce qui atterrit dans une defausse est bien passe par le jeu.
 */
const ZONES_EN_ATTENTE = [
  'area_set_aside',
  'encounter_deck',
  'main_schemes_deck',
  'villain_deck',
  'additional_decks',
] as const

/** Toutes les cartes d'une zone de monde, quelle que soit sa forme. */
function cartesDe(monde: World, zone: string): WorldCard[] {
  const valeur = (monde as unknown as Record<string, unknown>)[zone]
  if (!Array.isArray(valeur)) return []
  // additional_decks et additional_discard_piles contiennent des DECKS, pas des
  // cartes : le piège est documenté dans world.ts, on l'aplatit ici.
  return valeur.flat() as WorldCard[]
}

/** Toutes les zones de cartes du monde, joueurs compris. */
function toutesLesCartes(monde: World, sauf: readonly string[] = []): WorldCard[] {
  const exclues = new Set(sauf)
  const sortie: WorldCard[] = []
  for (const zone of Object.keys(monde)) {
    if (exclues.has(zone) || zone === 'players') continue
    sortie.push(...cartesDe(monde, zone))
  }
  for (const joueur of monde.players ?? []) {
    sortie.push(...cartesDuJoueur(joueur))
  }
  return sortie
}

/** Toutes les cartes que ce joueur possède, où qu'elles soient. */
function cartesDuJoueur(joueur: WorldPlayer): WorldCard[] {
  const zones: Array<keyof WorldPlayer> = [
    'area_hero',
    'allies',
    'supports',
    'player_deck',
    'player_discard_pile',
    'hand_cards',
    'reserve',
    'additional_deck',
    'additional_discard_pile',
    'obligations_area',
    'environment_area',
  ]
  const sortie: WorldCard[] = []
  for (const zone of zones) {
    const valeur = joueur[zone]
    if (Array.isArray(valeur)) sortie.push(...(valeur as WorldCard[]))
  }
  return sortie
}

/**
 * Parmi `options`, celles qui sont ENTRÉES EN JEU pendant la partie.
 *
 * Sert aux attachements EXPERIMENTAL de Crossbones : le livret demande de noter
 * ceux qui sont entrés en jeu, pour les remélanger dans le deck de rencontre
 * des scénarios suivants. Une arme attachée au vilain a été mesurée dans
 * `area_villain` avec un `bind_object_id` pointant sur lui ; une fois défaussée
 * elle passe dans la défausse de rencontre. Dans les deux cas elle a bien été
 * en jeu. Celles qui dorment encore dans un deck mis de côté, non.
 */
export function cartesEnJeu(monde: World, options: readonly string[]): string[] {
  const vises = new Set(options)
  const vus = new Set<string>()
  for (const carte of toutesLesCartes(monde, ZONES_EN_ATTENTE)) {
    if (vises.has(carte.card_id)) vus.add(carte.card_id)
  }
  return options.filter((id) => vus.has(id))
}

/**
 * Valeur d'un compteur posé sur la manigance principale.
 *
 * Les compteurs sortent préfixés `c_` dans le descripteur (les JETONS, eux,
 * sortent en `k_` — d'où `k_threat` pour la menace). Mesuré : trois pions
 * retard sur The Island of Dr. Zola donnent `info.c_delay === 3`.
 *
 * On prend le MAXIMUM et non la somme : plusieurs manigances principales
 * peuvent coexister (une par étape), et c'est la manigance active qui porte le
 * compte que le livret demande de reporter.
 */
export function compteurManigance(monde: World, compteur: string): number {
  const cle = `c_${compteur}`
  let maximum = 0
  for (const carte of monde.area_schemes_main ?? []) {
    const valeur = carte.info?.[cle]
    if (typeof valeur === 'number' && valeur > maximum) maximum = valeur
  }
  return maximum
}

/**
 * Parmi `options`, les cartes que CE joueur possède désormais.
 *
 * Sert aux alliés secourus de Taskmaster (« Captured by Hydra » les remet au
 * joueur qui déjoue la manigance) et aux obligations de campagne experte. Les
 * alliés non secourus restent dans la zone mise de côté du SCÉNARIO, pas dans
 * celle du joueur : mesuré sur une mise en place de Taskmaster, les quatre
 * captifs sont dans `area_set_aside` du monde, aucun chez le joueur.
 */
export function cartesDuJoueurParmi(
  monde: World,
  joueurId: number,
  options: readonly string[]
): string[] {
  const joueur = monde.players?.[joueurId]
  if (!joueur) return []
  const possedees = new Set(cartesDuJoueur(joueur).map((c) => c.card_id))
  return options.filter((id) => possedees.has(id))
}

/**
 * Les joueurs encore engagés avec au moins un ennemi.
 *
 * Rendu en indices de joueur (« 0 », « 1 »…) : c'est ce que le moteur relit
 * dans « Players engaged with minions », comparé à `player.player_id` par
 * The Rise of Red Skull (04128a).
 */
export function joueursEngages(monde: World): string[] {
  const sortie: string[] = []
  ;(monde.players ?? []).forEach((joueur, index) => {
    if ((joueur.engaged_enemies ?? []).length > 0) sortie.push(String(index))
  })
  return sortie
}

/** Le complot `carteId` est-il encore en jeu ? */
export function complotEnJeu(monde: World, carteId: string): boolean {
  return (monde.area_schemes_side ?? []).some((c) => c.card_id === carteId)
}

/**
 * Les cartes posées SOUS un complot encore en jeu.
 *
 * Sert à la Prison d'Hydra de Zola : les alliés qu'elle retient encore à la fin
 * sont retirés de la campagne. Mesuré : la prison est dans `area_schemes_side`
 * avec `bind_object_id: 0`, et l'allié qu'elle retient est dans LA MÊME zone,
 * avec `bind_object_id` égal à l'`id` de la prison.
 */
export function cartesSousComplot(
  monde: World,
  complotId: string,
  typeCarte?: string
): string[] {
  const complots = (monde.area_schemes_side ?? []).filter((c) => c.card_id === complotId)
  if (!complots.length) return []
  const ids = new Set(complots.map((c) => c.id))
  return (monde.area_schemes_side ?? [])
    .filter((c) => ids.has(c.bind_object_id))
    .filter((c) => !typeCarte || c.card_type === typeCarte)
    .map((c) => c.card_id)
}

/**
 * PV restants d'un héros, plafonnés à ses PV imprimés.
 *
 * Règle du livret (p17) : « si les PV restants dépassent les PV de base, noter
 * les PV de base ». Le moteur expose les deux sur la carte d'identité :
 * `info.health` et `info.max_health`, mesurés à 11/11 sur Steve Rogers.
 *
 * Un héros ÉLIMINÉ ne reporte rien : le livret le fait revenir au scénario
 * suivant à pleins PV, en échange d'une obligation.
 */
export function pvRestants(monde: World, joueurId: number): number | undefined {
  const joueur = monde.players?.[joueurId]
  if (!joueur || joueur.is_eliminated) return undefined
  const identite = joueur.area_hero?.[0]
  if (!identite) return undefined
  const courants = identite.info?.health
  if (typeof courants !== 'number') return undefined
  const maximum = identite.info?.max_health
  return typeof maximum === 'number' && maximum > 0 ? Math.min(courants, maximum) : courants
}

/** Ce joueur a-t-il été éliminé ? Il ne touche alors aucune récompense. */
export function joueurElimine(monde: World, joueurId: number): boolean {
  return Boolean(monde.players?.[joueurId]?.is_eliminated)
}

/**
 * Parmi `options`, celles qui sont dans la PILE DE VICTOIRE.
 *
 * Sinister Motives : « si une manigance Community Service est dans la pile de
 * victoire, note son titre ». Une manigance annexe déjouée y atterrit ; une
 * manigance encore en jeu, ou jamais révélée, non.
 */
export function cartesEnPileVictoire(monde: World, options: readonly string[]): string[] {
  const dedans = new Set((monde.victory_display ?? []).map((c) => c.card_id))
  return options.filter((id) => dedans.has(id))
}

/**
 * Parmi `options`, celles présentes dans une zone nommée du monde.
 *
 * Sinister Motives, scénario 4 : « note le nom de chaque vilain EN JEU ». On
 * gagne ce scénario en achevant la manigance principale, pas forcément en
 * abattant les six — ceux qui tiennent encore debout reviennent au scénario 5
 * sous forme de sbires. C'est donc bien une PÉNALITÉ, pas un trophée : l'ancien
 * schéma de `prepare/app.js` l'avait noté à l'envers (« Sinistres Six vaincus »).
 */
export function cartesDansZone(
  monde: World,
  zone: string,
  options: readonly string[]
): string[] {
  const presentes = new Set(cartesDe(monde, zone).map((c) => c.card_id))
  return options.filter((id) => presentes.has(id))
}

/**
 * Nombre de cartes portant un trait donné dans les decks des joueurs.
 *
 * Sinister Motives, scénario 3 : « compte le nombre total de cartes ILLUSION
 * dans tous les decks des joueurs » — ce total devient la menace posée sur
 * « Light at the End » au scénario 4.
 *
 * Les traits sortent préfixés `t_` dans le descripteur (mesuré : une carte
 * SYMBIOTE porte `traits: { t_SYMBIOTE: 1 }`). On regarde le deck, la main et
 * la défausse : c'est là que les cartes de rencontre ajoutées par Mysterio se
 * trouvent à la fin du scénario.
 */
export function compterTrait(monde: World, trait: string): number {
  const cle = `t_${trait.toUpperCase()}`
  let total = 0
  for (const joueur of monde.players ?? []) {
    for (const zone of ['player_deck', 'hand_cards', 'player_discard_pile'] as const) {
      for (const carte of joueur[zone] ?? []) {
        if (carte.traits?.[cle]) total += 1
      }
    }
  }
  return total
}

/**
 * Valeur détectée pour un champ, dans la forme du carnet.
 *
 * Rend `undefined` quand il n'y a rien à écrire — une clé absente et une clé
 * vide ne sont pas la même chose pour le moteur, qui traite « » comme
 * « aucune valeur » mais garderait une entrée inutile dans la sauvegarde.
 */
export function detecter(
  champ: ChampVictoire,
  monde: World,
  joueurId: number
): string | undefined {
  const options = champ.options ?? []
  const parametres = champ.parametres ?? {}

  const rendreListe = (ids: string[]) => (ids.length ? enListe(ids) : undefined)

  switch (champ.detection) {
    case 'cartes_en_jeu':
      return rendreListe(cartesEnJeu(monde, options))
    case 'compteur_manigance': {
      const valeur = compteurManigance(monde, parametres.compteur ?? 'delay')
      return valeur > 0 ? String(valeur) : undefined
    }
    case 'cartes_du_joueur':
      return rendreListe(cartesDuJoueurParmi(monde, joueurId, options))
    case 'joueurs_engages':
      return rendreListe(joueursEngages(monde))
    case 'cartes_sous_complot':
      return rendreListe(cartesSousComplot(monde, parametres.complot ?? '', parametres.type))
    case 'cartes_en_pile_victoire':
      return rendreListe(cartesEnPileVictoire(monde, options))
    case 'cartes_dans_zone':
      return rendreListe(cartesDansZone(monde, parametres.zone ?? '', options))
    case 'compter_trait': {
      const valeur = compterTrait(monde, parametres.trait ?? '')
      return valeur > 0 ? String(valeur) : undefined
    }
    case 'conditions_reputation':
      return String(conditionsReputation(monde))
    case 'pv_restants': {
      const valeur = pvRestants(monde, joueurId)
      return valeur === undefined ? undefined : String(valeur)
    }
    default:
      return undefined
  }
}

/**
 * Zones où une carte est EN JEU, au sens des conditions de la piste de réputation.
 *
 * Ni les decks, ni les défausses, ni les mises de côté, ni la pile de victoire :
 * une carte qui y dort n'est pas « in play ». Les sbires engagés avec un joueur
 * comptent, eux, et c'est justement le cas que la seule lecture de
 * `area_villain` raterait.
 */
const ZONES_EN_JEU = [
  'area_schemes_main',
  'area_schemes_side',
  'area_villain',
  'area_environment',
  'area_status_cards',
] as const

const ZONES_EN_JEU_JOUEUR: Array<keyof WorldPlayer> = [
  'area_hero',
  'allies',
  'supports',
  'engaged_enemies',
  'obligations_area',
  'environment_area',
]

/** Toutes les cartes réellement EN JEU, joueurs compris. */
function cartesEnJeuToutes(monde: World): WorldCard[] {
  const sortie: WorldCard[] = []
  for (const zone of ZONES_EN_JEU) sortie.push(...cartesDe(monde, zone))
  for (const joueur of monde.players ?? []) {
    for (const zone of ZONES_EN_JEU_JOUEUR) {
      const valeur = joueur[zone]
      if (Array.isArray(valeur)) sortie.push(...(valeur as WorldCard[]))
    }
  }
  return sortie
}

/** Un complot ANNEXE, quelle qu'en soit l'origine (rencontre ou joueur). */
const TYPES_ANNEXES = ['EncounterSideScheme', 'PlayerSideScheme']

/**
 * Le total de réputation gagné par la partie qui vient de s'achever (sm).
 *
 * Les six conditions sont imprimées sous la piste de réputation (livret sm,
 * p.22), et le livret les fait recalculer à la fin de CHAQUE scénario :
 *
 *   (+X) Victory points in the victory display
 *   (+1) No minions in play
 *   (+1) No side schemes in play
 *   (+1) No threat on the main scheme
 *   (+1) Fewer than 1 acceleration tokens in play
 *   (+1) No defeated identities
 *
 * Aucune n'est une décision : ce sont six lectures de la table, et le joueur les
 * recopiait à la main dans un champ `choix`. Tout est dans le descripteur, et les
 * clés ci-dessous sont MESURÉES sur une vraie partie de Sandman, jamais déduites :
 * la menace de la manigance principale est `info.k_threat` (un JETON, pas un
 * compteur), les pions accélération `info.k_acceleration_token`, et les points de
 * victoire `info.victory` sur chaque carte de la pile de victoire.
 *
 * La valeur rendue est ce que CETTE partie ajoute. Le cumul sur toute la
 * campagne est fait par `preRemplir` à partir du carnet (attribut `cumulatif`) :
 * le détecteur ne voit pas le carnet, et un détecteur qui rendrait le total
 * ferait dépendre son résultat de ce qu'il ignore.
 */
export function conditionsReputation(monde: World): number {
  const enJeu = cartesEnJeuToutes(monde)

  const pointsDeVictoire = (monde.victory_display ?? []).reduce(
    (total, carte) => total + (carte.info?.victory ?? 0),
    0
  )
  const sbires = enJeu.filter((c) => c.card_type === 'Minion').length
  const annexes = enJeu.filter((c) => TYPES_ANNEXES.includes(c.card_type)).length
  const menace = (monde.area_schemes_main ?? []).reduce(
    (total, carte) => total + (carte.info?.k_threat ?? 0),
    0
  )
  const acceleration = enJeu.reduce(
    (total, carte) => total + (carte.info?.k_acceleration_token ?? 0),
    0
  )
  const vaincus = (monde.players ?? []).filter((j) => j.is_eliminated).length

  return (
    pointsDeVictoire +
    (sbires === 0 ? 1 : 0) +
    (annexes === 0 ? 1 : 0) +
    (menace === 0 ? 1 : 0) +
    (acceleration < 1 ? 1 : 0) +
    (vaincus === 0 ? 1 : 0)
  )
}

/**
 * Ce champ s'applique-t-il à cette partie ?
 *
 * Zola : le choix « passer l'amélioration en version supérieure » n'existe que
 * si la Prison d'Hydra est tombée. Le champ est sinon masqué, pas grisé : on ne
 * propose pas une récompense que les règles refusent.
 */
export function conditionRemplie(champ: ChampVictoire, monde: World): boolean {
  const parametres = champ.parametres ?? {}
  switch (champ.condition) {
    case 'complot_absent':
      return !complotEnJeu(monde, parametres.complot ?? '')
    case undefined:
      return true
    default:
      // Condition inconnue : on préfère masquer le champ plutôt que d'accorder
      // une récompense sur une règle qu'on ne sait pas évaluer.
      return false
  }
}

/** Clé du carnet pour ce champ et ce joueur (« Player 2 Tech Upgrade »). */
export function cleCarnet(champ: ChampVictoire, joueurId: number): string {
  return champ.parJoueur ? `Player ${joueurId + 1} ${champ.cle}` : champ.cle
}
