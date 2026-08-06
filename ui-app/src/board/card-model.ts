// La seule couche qui traduit une carte de partie en props d'affichage.
//
// Tout ce que le plateau sait du moteur passe par ici. Le composant ScanCard ne
// connait aucun card_type, aucun champ info, aucune route serveur.

import type { CardKind, CardState, ScanCardProps } from '../components/ScanCard'
import type { Catalogue } from './catalogue'
import { isScheme, isUnit, isVisibleFor, type WorldCard } from './world'
import { t } from './langue'
import { picIdAffiche } from './variantes'
import { picIdFr } from './scans-fr'

/**
 * card_type du moteur -> famille visuelle.
 * Les types inconnus (nouveaux paquets) tombent sur 'unknown' : la carte
 * s'affiche quand meme, avec son scan, sans etiquette mensongere.
 */
const KIND_PAR_TYPE: Partial<Record<string, CardKind>> = {
  Hero: 'hero',
  AlterEgo: 'alter-ego',
  Ally: 'ally',
  Support: 'support',
  Upgrade: 'upgrade',
  Event: 'event',
  Resource: 'resource',
  EncounterVillain: 'villain',
  Minion: 'minion',
  MainScheme: 'main-scheme',
  EncounterSideScheme: 'side-scheme',
  PlayerSideScheme: 'side-scheme',
  Attachment: 'attachment',
  Treachery: 'treachery',
  Environment: 'environment',
  Obligation: 'obligation',
  StatusCard: 'status',
}

export function kindOf(card: WorldCard): CardKind {
  return KIND_PAR_TYPE[card.card_type] ?? 'unknown'
}

/**
 * Camp d'une carte : « joueur » (nos cartes) ou « rencontre » (le mechant). Sert
 * a poser un halo vert / rouge autour de la carte, pour distinguer d'un coup
 * d'oeil qui est a qui dans les zones qui melangent les deux (allies + sbires +
 * environnement + treacheries) et pour les complots (joueur vs mechant).
 *
 * On le tire du card_type et NON de la famille visuelle : un side scheme peut
 * etre joueur (PlayerSideScheme) ou rencontre (EncounterSideScheme), or les deux
 * partagent le meme `kind` d'affichage. Les cartes sans camp franc (statut posee
 * indifferemment sur un heros ou un vilain) n'ont pas de halo.
 */
const CAMP_PAR_TYPE: Partial<Record<string, 'player' | 'encounter'>> = {
  Hero: 'player',
  AlterEgo: 'player',
  Ally: 'player',
  Support: 'player',
  Upgrade: 'player',
  Event: 'player',
  Resource: 'player',
  PlayerSideScheme: 'player',
  EncounterVillain: 'encounter',
  Minion: 'encounter',
  MainScheme: 'encounter',
  EncounterSideScheme: 'encounter',
  Attachment: 'encounter',
  Treachery: 'encounter',
  Environment: 'encounter',
  Obligation: 'encounter',
}

function campDe(card: WorldCard): 'player' | 'encounter' | undefined {
  return CAMP_PAR_TYPE[card.card_type]
}

/**
 * Les complots se posent en paysage. Mesure sur les scans du jeu : MainScheme,
 * SideScheme et PlayerSideScheme sont imprimes en 1030x710, tous les autres
 * types en 710x1030.
 *
 * Un complot face cachee reste en portrait : c'est son DOS qui est affiche, et
 * les dos (encounter, player, villain) sont tous portrait.
 */
export function isLandscapeType(card: WorldCard, visible: boolean): boolean {
  // Complots ET cartes de statut (Stunned/Confused/Tough) sont imprimes en
  // paysage.
  return visible && (isScheme(card) || card.card_type === 'StatusCard')
}

/**
 * URL du scan.
 *
 * Le serveur du jeu n'a pas de route dediee aux images : sa route fourre-tout
 * `/{path:.+}` prend le DERNIER segment du chemin et le cherche dans
 * assets/pics, assets/textures puis assets/cache, en essayant .webp, .jpg et
 * .png. C'est exactement ce mecanisme que le runtime historique utilise deja
 * (ses CSS ecrivent url("04079b"), resolu en /css/marvel/04079b).
 *
 * Le prefixe /scan/ ne veut donc rien dire pour le serveur : il est la pour que
 * le serveur de developpement de Vite puisse relayer ces requetes au jeu
 * (voir server.proxy dans vite.config.ts) sans intercepter toute la page.
 *
 * Le nom demande passe par picIdFr() : une carte disponible en francais est
 * servie depuis assets/pics-fr sous le nom « fr_<code> ». Voir scans-fr.ts.
 */
export function scanUrl(picId: string): string {
  return `/scan/${picIdFr(picId)}`
}

/** Vide et 0 sont deux choses differentes : 0 PV se voit, 0 menace aussi. */
function nombre(valeur: number | undefined): number | undefined {
  return typeof valeur === 'number' ? valeur : undefined
}

/**
 * Pastille PV.
 *
 * ECART ASSUME avec la vitrine, qui n'affichait les PV que sur les allies :
 * ici tous les personnages en portent (heros, identite, allie, sbire, vilain).
 * Un plateau qui cache les PV du vilain est injouable, et c'est la meme
 * pastille, sans information supplementaire. A revalider avec l'utilisateur.
 */
function pvAffiches(card: WorldCard, catalogue: Catalogue): string | undefined {
  if (!isUnit(card)) return undefined

  if (card.info.is_infinite_health) return 'INF'

  const courants = nombre(card.info.health)
  if (courants === undefined) return undefined

  const max = catalogue.pvMax(card.card_id)
  // Pas de maximum fiable (PV variables selon le nombre de joueurs, ou carte
  // absente du catalogue) : on montre le courant seul plutot qu'un faux rapport.
  return max === undefined ? `${courants}` : `${courants}/${max}`
}

/**
 * Pastille menace.
 *
 * Le compteur courant est info.k_threat (« k_ » = jeton, confirme par
 * descriptor.js qui renomme k_threat en threat pour les complots). Le complot
 * principal a une cible a atteindre : on montre le rapport. Les complots annexes
 * descendent vers zero : le courant suffit.
 */
function menaceAffichee(card: WorldCard): string | undefined {
  if (!isScheme(card)) return undefined

  const courante = nombre(card.info.k_threat)
  if (courante === undefined) return undefined

  const cible = nombre(card.info.target_threat)
  return cible !== undefined && cible > 0 ? `${courante}/${cible}` : `${courante}`
}

/**
 * Petits badges de stats d'un personnage. On ne pose un badge QUE si la valeur
 * courante (moteur, deja modifiee par les ameliorations) DIFFERE de la valeur
 * imprimee sur la carte. Tant que rien ne modifie la stat, l'image de la carte
 * montre deja la bonne valeur : inutile de la recouvrir.
 *
 * C'est aussi ce qui regle le cas « X » : une carte a valeur variable (attaque X,
 * complot X) a une valeur imprimee de 0 et une valeur courante de 0 tant que X
 * n'est pas active -> pas de badge -> le « X » dessine sur le scan reste visible.
 * Le moteur n'envoie jamais « X », et rien ne distingue un vrai 0 d'un X : on ne
 * devine donc pas, on laisse simplement l'image parler quand rien n'a bouge.
 *
 * Ordre fixe et labels courts. Un vilain n'a ni THW ni DEF (il a ATK + SCH), un
 * alter ego a REC, un allie a ATK + THW.
 */
// [cle info, code catalogue (logique, ne pas traduire), libellé affiché]
const STATS_BASE: Array<[string, string, string]> = [
  ['thwart', 'THW', 'CTR'],
  ['attack', 'ATK', 'ATQ'],
  ['defense', 'DEF', 'DEF'],
  ['recover', 'REC', 'REC'],
  ['scheme', 'SCH', 'MNG'],
]
function statsAffichees(
  card: WorldCard,
  catalogue: Catalogue
): Array<{ label: string; value: number }> {
  if (!isUnit(card)) return []
  if (['player', 'encounter', 'villain', 'no_image'].includes(card.pic_id)) return []
  const info = card.info
  const badges: Array<{ label: string; value: number }> = []
  for (const [cle, code] of STATS_BASE) {
    const courante = info[cle]
    // Pas de valeur courante connue : l'image de la carte fait foi, pas de badge.
    if (typeof courante !== 'number') continue
    const imprimee = catalogue.statImprimee(card.card_id, code)
    // Stat NON modifiee (courante == imprimee) : l'image montre deja la bonne
    // valeur, y compris un « X ». On ne pose un badge que sur une vraie modif.
    if (imprimee !== undefined && courante === imprimee) continue
    // Le label transmis est le CODE logique (THW/ATK/...) : ScanCard s'en sert
    // comme cle (icone, position calibree, classe CSS) et n'affiche jamais ce
    // texte. Le libellé FR du triplet ne sert qu'aux affichages textuels, qui
    // passent par t() a leur point d'affichage (voir MenuActionsCarte).
    badges.push({ label: code, value: courante })
  }
  return badges
}

export type ContexteCarte = {
  /** Numero du joueur dont on regarde le plateau. */
  playerId: number
  /** world.active_card_ids : les cartes citees par l'evenement en cours. */
  actives: ReadonlySet<number>
  catalogue: Catalogue
  /**
   * Carte de notre main. Une main est physiquement face cachee mais son
   * proprietaire la lit : elle se dessine comme une carte normale.
   */
  dansLaMain?: boolean
  /** Nom du heros proprietaire (multi) : badge sur ses allies/sbires engages. */
  proprietaire?: string
  /**
   * Collection d'arts des ressources doubles du joueur PROPRIETAIRE de la zone
   * ('' = art standard). Choisie a la preparation, deja resolue.
   */
  collectionRessources?: string
  /** Force la pastille de hauteur de pile (voir toPileCard). */
  pileCount?: number
}

/**
 * Traduit une carte de partie en props de ScanCard.
 *
 * Regle de visibilite reprise du runtime : si le joueur a le droit de voir la
 * face, on montre le scan ; sinon on montre le dos, et alors ni le type ni les
 * compteurs ne doivent apparaitre.
 */
/**
 * Images des AUTRES faces d'une carte recto-verso reelle (heros/alter-ego,
 * complot a etapes...), a distinguer du dos classique. Le descripteur met les
 * autres faces dans down_card_ids : Ant-Man (3 formes) a par ex.
 * down_card_ids = ['12001b', '12001a'] quand 12001c est visible. Une entree est
 * une vraie face quand elle partage la meme base numerique que la face visible
 * et n'en differe que par le suffixe. Un dos generique ("player", "encounter")
 * ne matche pas ce motif.
 */
function autresFacesUrls(card: WorldCard): string[] {
  if (!card.is_face_up) return []
  const face = card.card_id?.match(/^(\d+)([a-z])$/)
  if (!face) return []
  const urls: string[] = []
  for (const dos of card.down_card_ids ?? []) {
    const autre = dos.match(/^(\d+)([a-z])$/)
    if (autre && autre[1] === face[1] && autre[2] !== face[2]) urls.push(scanUrl(dos))
  }
  return urls
}

/**
 * Compteurs poses sur la carte (supply, pym, charge...). Le moteur les envoie
 * dans info sous des cles « c_<nom> » (courant) et « c_<nom>_printed »
 * (imprime). On montre chaque compteur courant, MEME a zero quand la carte en
 * imprime (« Uses (2 supply) » epuise = information utile), mais pas les cles
 * purement techniques restees a zero sans version imprimee.
 */
function compteursAffiches(card: WorldCard): Array<{ label: string; value: number }> {
  const compteurs: Array<{ label: string; value: number }> = []
  for (const [cle, valeur] of Object.entries(card.info)) {
    if (!cle.startsWith('c_') || cle.endsWith('_printed')) continue
    if (typeof valeur !== 'number') continue
    const imprime = card.info[`${cle}_printed`]
    if (valeur === 0 && typeof imprime !== 'number') continue
    compteurs.push({ label: cle.slice(2).replace(/_/g, ' '), value: valeur })
  }
  return compteurs
}

export function toScanCard(card: WorldCard, contexte: ContexteCarte): ScanCardProps {
  const visible = isVisibleFor(card, contexte.playerId)
  const dos = card.down_card_ids[0]

  // Une carte visible mais posee face cachee sur la table : le cadre en
  // pointilles le dit. En main, il n'y a rien a signaler.
  const peeking = visible && !card.is_face_up && !contexte.dansLaMain

  const state: CardState = card.is_ready ? 'ready' : 'exhausted'
  // Drapeau independant de `state` : l'interaction remplace `state` par
  // « playable/source/... » quand la carte agit, ce qui effacait l'inclinaison
  // d'epuisement du heros (qui porte toujours des options). `exhausted` survit.
  const exhausted = card.is_ready === false

  if (!visible) {
    return {
      id: String(card.id),
      name: t('Carte face cachée'),
      kind: 'unknown',
      state,
      exhausted,
      imageUrl: scanUrl(dos ?? 'no_image'),
      isLandscape: false,
      facedown: true,
      pileCount: contexte.pileCount,
      highlight: contexte.actives.has(card.id),
    }
  }

  return {
    id: String(card.id),
    name: card.name,
    kind: kindOf(card),
    state,
    exhausted,
    // Art alternatif eventuel (promos FFG) : cosmetique, la carte reste la meme.
    imageUrl: scanUrl(picIdAffiche(card.pic_id, contexte.collectionRessources)),
    picId: card.pic_id,
    autresFaces: autresFacesUrls(card),
    // Un complot EN MAIN (side scheme joueur) est montre en PORTRAIT, pour tenir
    // dans l'eventail comme les autres cartes. Il reprend son format paysage a
    // l'agrandissement (voir CarteApercu, qui force isLandscape pour les complots).
    isLandscape: contexte.dansLaMain && isScheme(card) ? false : isLandscapeType(card, true),
    // Le serveur redresse tous ses scans en portrait : un cadre paysage doit
    // tourner l'image. Mesure : 21180a fait 1046x725 sur le disque, 725x1046
    // a l'arrivee.
    scanIsPortrait: true,
    allyHp: pvAffiches(card, contexte.catalogue),
    schemeThreat: menaceAffichee(card),
    counters: compteursAffiches(card),
    proprietaire: contexte.proprietaire,
    camp: campDe(card),
    stats: statsAffichees(card, contexte.catalogue),
    peeking,
    // Mots-cles (Guard, Piercing...) pour les tooltips de l'apercu.
    keywords: contexte.catalogue.motsCles(card.card_id),
    codeCarte: card.card_id,
    pileCount: contexte.pileCount,
    highlight: contexte.actives.has(card.id),
  }
}

/**
 * Une pile (deck, defausse) rendue comme UNE carte porteuse de sa hauteur.
 * Dessiner 34 dos de deck de rencontre cote a cote n'apprend rien et ruine la
 * lecture du plateau.
 */
export function toPileCard(
  pile: WorldCard[],
  contexte: Omit<ContexteCarte, 'pileCount'>,
  // Quelle carte represente la pile. Par defaut le DESSUS (derniere du tableau).
  // Certaines piles preferent une carte precise : la pile nemesis montre le
  // nemesis lui-meme plutot qu'une treachery quelconque (voir zones.ts).
  choisirRepresentant: (pile: WorldCard[]) => WorldCard | undefined = (p) => p.at(-1)
): ScanCardProps | undefined {
  const representant = choisirRepresentant(pile) ?? pile.at(-1)
  if (!representant) return undefined
  return toScanCard(representant, { ...contexte, pileCount: pile.length })
}

/**
 * Le nemesis d'un set : sa carte-signature. Dans un set nemesis, le nemesis est
 * toujours un Minion (Baron Zemo, le Beetle...), pose AVANT les eventuels sbires
 * d'appoint. On prend donc le premier Minion ; a defaut, le dessus habituel.
 */
export function representantNemesis(pile: WorldCard[]): WorldCard | undefined {
  return pile.find((carte) => carte.card_type === 'Minion') ?? pile.at(-1)
}
