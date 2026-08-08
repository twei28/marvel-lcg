// CoucheMeteo — la météo du plateau.
//
// Un effet HTML autonome (public/effects/weather/) est superposé en iframe
// plein écran. À l'origine il ne servait qu'aux Soutiens météo de Storm ;
// il lit désormais aussi les cartes d'Environnement, qui vivent ailleurs.
//
// ON NE LIT QUE CE QUI EST EN JEU, par zones nommées. Le code d'origine
// parcourait tout l'objet joueur, main et decks compris : or Storm joue avec
// un DECK météo (`additional_deck`) qui contient ses trois autres cartes. Il
// ne s'en sortait que parce que `supports` précède `additional_deck` dans
// l'ordre des clés du descripteur, ce qui est un accident, pas une garantie.
//
// L'aperçu (sélecteur des réglages) prime sur les cartes tant qu'il est actif :
// c'est un outil de conception, il doit pouvoir montrer un effet sans partie.
import { useMemo } from 'react'
import type { World, WorldCard } from './world'

/** Les effets qu'on sait afficher, pour le sélecteur d'aperçu. */
export const EFFETS_METEO = [
  'rain', 'storm', 'snow', 'fog', 'stars', 'embers',
  'dust', 'neon', 'jungle',
  'noir', 'horror', 'cyber', 'sitcom', 'sepia', 'sandstorm',
] as const
export type EffetMeteo = (typeof EFFETS_METEO)[number]

/** Le nom affiché de chaque effet. Une table, et non une suite de ternaires :
 *  le sélecteur en compte six et en comptera davantage. */
export const LIBELLE_EFFET: Record<EffetMeteo, string> = {
  rain: 'Pluie',
  storm: 'Orage',
  snow: 'Neige',
  fog: 'Brume',
  stars: 'Étoiles',
  embers: 'Braises',
  dust: 'Poussière',
  neon: 'Néons',
  jungle: 'Jungle',
  noir: 'Noir et blanc',
  horror: 'Horreur',
  cyber: 'Cyber',
  sitcom: 'Sitcom',
  sepia: 'Sépia',
  sandstorm: 'Tempête de sable',
}

/** L'apercu a deux etats en plus des effets, et ils ne disent pas la meme
 *  chose. '' rend la main au jeu : ce sont les cartes qui decident, c'est le
 *  mode normal. AUCUN_EFFET impose le vide, meme si une carte en jeu
 *  declencherait quelque chose. Sans cette distinction, « Aucun » signifiait
 *  en realite « Auto » et il n'existait aucun moyen de couper temporairement
 *  l'ambiance sans toucher au reglage Meteo. */
export const AUCUN_EFFET = 'none'

/** Les valeurs par lesquelles passe le selecteur, dans l'ordre. */
export const CYCLE_APERCU = ['', AUCUN_EFFET, ...EFFETS_METEO] as const

export function libelleApercu(valeur: string): string {
  if (valeur === '') return 'Auto'
  if (valeur === AUCUN_EFFET) return 'Aucun'
  return LIBELLE_EFFET[valeur as EffetMeteo] ?? valeur
}

/** L'ambiance appartient au SCÉNARIO et aux modules, jamais aux cartes que le
 *  joueur monte dans son deck. Un lieu joué par un héros est sa base, une
 *  carte de sa main : il n'a pas à repeindre la table pour tout le monde.
 *  Seize Soutiens de héros ont été câblés le 8/8/2026 puis retirés pour cette
 *  raison ; un cas de test refuse désormais toute carte de deck de joueur.
 *
 *  La seule exception est le deck météo de Storm, et elle se justifie : son
 *  sujet EST la météo, changer le temps est sa capacité, et c'est pour ces
 *  trois cartes que la couche a été écrite.
 *
 *  La table est typée sur les effets connus : une faute de frappe ici
 *  demanderait un fichier HTML inexistant, et l'écran resterait vide. */
export const METEO_PAR_CARTE: Record<string, EffetMeteo> = {
  // Storm — deck météo. 36002 Clear Skies n'a volontairement aucun visuel.
  '36003': 'rain', // Hurricane
  '36004': 'storm', // Thunderstorm
  '36005': 'snow', // Blizzard
  // Environnements
  '04081': 'snow', // Snowy Hillside, Absorbing Man
  '29039': 'storm', // Air Static, Zzzax
  '50131a': 'storm', // Justice, Like Lightning, Thunderbolts
  // Lieux clos, souterrains ou boises
  '04080': 'fog', // Dense Forest, Tourist Trap
  '16085a': 'fog', // Library Labyrinth, Galaxy's Most Wanted
  '24060': 'fog', // Back-Alley Enclave, The Hood
  '24061': 'fog', // Secret Lair, The Hood
  '24062': 'fog', // Sewer Tunnels, The Hood
  '27077a': 'fog', // Bell Tower silencieux, Sinister Motives
  '27077b': 'fog', // Bell Tower qui sonne, Sinister Motives
  // Vaisseaux et espace
  '16063': 'stars', // Badoon Ship
  '16085b': 'stars', // Museum Ship
  '16093': 'stars', // Nebula's Ship
  '16108': 'stars', // Kree Command Ship
  '16143': 'stars', // Rogue Vessel
  '45139': 'stars', // Blue Area of the Moon, Age of Apocalypse
  // Feu
  '21076': 'embers', // Fireball, The Mad Titan's Shadow
  '90128': 'embers', // Burning Building, Rainy
  // Pierre, metal et gravats
  '04082': 'dust', // Rocky Outcrop, Tourist Trap
  '04083': 'dust', // Abandoned Facility, Tourist Trap
  '21079': 'dust', // Rubblestorm, The Mad Titan's Shadow
  // La rue la nuit
  '24063': 'neon', // Warehouse District, The Hood
  '27065': 'sandstorm', // City Streets : la rue de Sandman, dans son scenario
  '31037': 'neon', // Surge in Crime, SP//dr
  // Vegetation
  '45127': 'jungle', // The Savage Land, Age of Apocalypse
  '45133': 'jungle', // Genosha, Age of Apocalypse
  // --- Mojoverse -----------------------------------------------------------
  // Chaque decor est une parodie de genre televise. Le genre ne se devine pas
  // au titre mais aux figurants qui l'accompagnent dans le paquet : Dragnet et
  // Law & Order d'un cote, Dragon et Troll de l'autre, Vampire et Loup-garou,
  // des PROGRAMMES nommes Magneto 2.6, un Gunslinger.
  '39035': 'noir', // Dial M for Mojo : le polar rendu en noir et blanc
  '39041': 'embers', // A Game of Mojo's, fantasy : le souffle du Dragon
  '39047': 'horror', // The Mojo Files, vampires et loups-garous
  '39053': 'cyber', // Mojo Runner, ennemis PROGRAMME
  '39060': 'sitcom', // Mojo in the Middle, comedie familiale
  '39066': 'sepia', // Wild Wild Mojo, western

  // Sans ambiance, par choix : les trois Manhattan infestes (27117b, 27118b,
  // 27119b) et Skies Over New York (27116b). Leurs effets ont ete ecrits puis
  // retires, ils ne rendaient pas ce qu'ils devaient rendre.
  //
  // Sans ambiance egalement : la Roue des genres (39026a/b) et les faces de
  // foule (39003a/b, 39004a/b) restent muettes a dessein, car elles sont en
  // jeu EN MEME TEMPS que le decor et lui disputeraient l'affichage puisque
  // la couche ne montre qu'un effet.
}

/** Les zones où une carte est réellement EN JEU, et elles seules. */
const ZONES_JOUEUR = ['supports', 'environment_area'] as const
const ZONES_MONDE = ['area_environment'] as const

export const CLE_METEO = 'marvel-board-meteo'

export function lireMeteoActive(): boolean {
  try {
    return window.localStorage.getItem(CLE_METEO) !== 'off'
  } catch {
    return true
  }
}

function cartesDe(source: unknown, zones: readonly string[]): WorldCard[] {
  if (typeof source !== 'object' || source === null) return []
  const sortie: WorldCard[] = []
  for (const zone of zones) {
    const valeur = (source as Record<string, unknown>)[zone]
    // Certaines zones sont des listes de listes (decks multiples) : on aplatit.
    if (Array.isArray(valeur)) sortie.push(...(valeur.flat() as WorldCard[]))
  }
  return sortie
}

/** La météo dictée par les cartes en jeu, ou '' si aucune ne s'applique. */
export function meteoDuMonde(world: World | undefined): string {
  if (!world) return ''
  const enJeu: WorldCard[] = [...cartesDe(world, ZONES_MONDE)]
  for (const joueur of world.players ?? []) enJeu.push(...cartesDe(joueur, ZONES_JOUEUR))
  for (const carte of enJeu) {
    const effet = carte && typeof carte.card_id === 'string' ? METEO_PAR_CARTE[carte.card_id] : undefined
    if (effet) return effet
  }
  return ''
}

/** Les effets qui EFFACENT la couleur du plateau. Sous eux, la couleur du
 *  cadre d'une carte ne dit plus son aspect, et le plateau doit la redonner
 *  autrement. Seul le noir et blanc en fait partie : le sepia teinte mais
 *  laisse les teintes distinctes les unes des autres. */
export const EFFETS_DELAVANTS: readonly string[] = ['noir']

/** L'effet réellement affiché, aperçu et interrupteur compris. */
export function effetAffiche(
  world: World | undefined,
  active: boolean,
  apercu?: string
): string {
  if (apercu === AUCUN_EFFET) return ''
  return apercu || (active ? meteoDuMonde(world) : '')
}

export function CoucheMeteo({
  world,
  active,
  apercu,
}: {
  world: World | undefined
  active: boolean
  /** Force un effet, quelles que soient les cartes. '' rend la main au jeu,
   *  AUCUN_EFFET impose le vide. */
  apercu?: string
}) {
  const duJeu = useMemo(() => meteoDuMonde(world), [world])
  // Meme regle que effetAffiche(), gardee ici pour ne pas recalculer le monde.
  // L'apercu est une demande EXPLICITE : il passe outre l'interrupteur. Sans
  // ca, choisir un apercu alors que la meteo est coupee n'affiche rien et
  // l'outil parait casse. L'interrupteur ne commande que la meteo du jeu.
  const meteo = apercu === AUCUN_EFFET ? '' : apercu || (active ? duJeu : '')
  if (!meteo) return null
  return (
    <iframe
      className={`couche-meteo couche-meteo--${meteo}`}
      src={`/effects/weather/${meteo}.html`}
      title=""
      aria-hidden="true"
      tabIndex={-1}
    />
  )
}
