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
export const EFFETS_METEO = ['rain', 'storm', 'snow', 'fog', 'stars', 'embers'] as const
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
}

/** La table est typée sur les effets connus : une faute de frappe ici
 *  demanderait un fichier HTML inexistant, et l'écran resterait vide. */
const METEO_PAR_CARTE: Record<string, EffetMeteo> = {
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
  // 21079 Rubblestorm reste volontairement de cote : ce sont des gravats qui
  // volent, pas du feu, et l'effet qui lui irait n'existe pas encore.
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

export function CoucheMeteo({
  world,
  active,
  apercu,
}: {
  world: World | undefined
  active: boolean
  /** Force un effet, quelles que soient les cartes. '' rend la main au jeu. */
  apercu?: string
}) {
  const duJeu = useMemo(() => meteoDuMonde(world), [world])
  // L'apercu est une demande EXPLICITE : il passe outre l'interrupteur. Sans
  // ca, choisir un apercu alors que la meteo est coupee n'affiche rien et
  // l'outil parait casse. L'interrupteur ne commande que la meteo du jeu.
  const meteo = apercu || (active ? duJeu : '')
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
