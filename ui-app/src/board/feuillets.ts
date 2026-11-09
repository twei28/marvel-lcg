// feuillets.ts — les feuillets (inserts) de regles propres a un heros (« Feuillet Dazzler », 08/11/2026).
//
// Un feuillet est une ou plusieurs images (feuillets/<prefixe>-<langue>[-<page>].jpg) : chaque image est inlinee par Vite
// (assetsInlineLimit) et chargee a l'ouverture de l'onglet seulement, pas dans le paquet du plateau.
// Langue : on montre le feuillet dans la langue du joueur s'il existe, sinon dans l'autre. Un heros qui n'a que
// l'insert anglais le montre donc aussi en francais, et inversement. Pas de feuillet = pas d'onglet.
import { langueActuelle } from './langue'

type Langue = 'fr' | 'en'

export interface Feuillet {
  /** Prefixe du pic_id de l'identite du heros (`dz` pour dz001a). */
  prefixe: string
  titre: string
  /** Une image par page, dans l'ordre (recto puis verso, ou page 1 puis 2). */
  pages: (() => Promise<string>)[]
}

interface Entree {
  titre: string
  /** Lots d'images a la suite (par defaut le lot du meme nom que la cle). Un lot peut servir plusieurs scenarios. */
  lots?: string[]
}

/**
 * Cle -> feuillet, dans l'ordre de l'onglet. Une cle de HEROS est le prefixe de ses cartes (`dz` pour dz001a) ;
 * une cle de SCENARIO est l'id exact d'une carte du vilain, ou du complot principal quand il n'a pas de vilain
 * (`gs161`). Une cle sans image n'apparait jamais.
 */
const ENTREES: Record<string, Entree> = {
  aa: { titre: 'Agatha Harkness' },
  al: { titre: 'Alligator Loki' },
  bg: { titre: 'Batgirl' },
  bm: { titre: 'Batman' },
  bw: { titre: 'Brawn' },
  ca: { titre: 'Carnage' },
  cn: { titre: 'Conan' },
  cr: { titre: 'Corsair' },
  dz: { titre: 'Dazzler' },
  il: { titre: 'Iron Lad' },
  ip: { titre: 'Iron Patriot' },
  ma: { titre: 'Ms. America' },
  mk: { titre: 'Moon Knight' },
  mm: { titre: 'Multiple Man' },
  ok: { titre: 'Okoye' },
  pu: { titre: 'Punisher' },
  rr: { titre: 'Sentry' },
  rz: { titre: 'Roz' },
  sd: { titre: 'Speed' },
  sm: { titre: 'Spider-Man 2099' },
  sp: { titre: 'The Spot' },
  st: { titre: 'Sentinel' },
  su: { titre: 'Superior Spider-Man' },
  sv: { titre: 'Silver Surfer' },
  td: { titre: 'Donatello' },
  tl: { titre: 'Leonardo' },
  tm: { titre: 'Michelangelo' },
  tr: { titre: 'Raphael' },
  vp: { titre: 'Venompool' },
  vz: { titre: 'Venomized' },
  wc: { titre: 'Wiccan' },
  wt: { titre: 'The Warriors Three' },
  '65': { titre: 'Wave' },
  // Scenarios
  ap005: { titre: 'Alien vs. Predator' },
  gs076: { titre: 'Kree Sentry', lots: ['gs076', 'gs-imperial-guard'] },
  gs114: { titre: "Majestrix's Verdict", lots: ['gs114', 'gs-imperial-guard'] },
  gs138: { titre: 'Hala Ultimatum' },
  gs161: { titre: 'Earth Under Siege', lots: ['gs161', 'gs-imperial-guard'] },
  gs195: { titre: 'Supreme Intelligence' },
  sk082: { titre: 'Skrull Empire', lots: ['sk082', 'sk-commun'] },
  sk117: { titre: 'Super-Skrull', lots: ['sk117', 'sk-commun'] },
  sk141: { titre: 'Paibok', lots: ['sk141', 'sk-commun'] },
  sk170: { titre: 'Skrull Pantheon', lots: ['sk170', 'sk-commun'] },
  sk189: { titre: 'Secret Invasion', lots: ['sk189', 'sk-commun'] },
  tk005: { titre: 'Bebop & Rocksteady' },
  ts001: { titre: 'Shredder' },
  tx001: { titre: 'Baxter Stockman' },
  vt017: { titre: 'The Vault' },
}

const IMAGES = import.meta.glob<string>('./feuillets/*.jpg', { import: 'default' })

interface Lot {
  fr: (() => Promise<string>)[]
  en: (() => Promise<string>)[]
}

/** Range les images par prefixe et par langue, pages dans l'ordre (`-en.jpg` = page 1, `-en-2.jpg` = page 2). */
function lotsParPrefixe(): Map<string, Lot> {
  const lots = new Map<string, Lot>()
  const fichiers = Object.keys(IMAGES).sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
  for (const chemin of fichiers) {
    const m = /\/([a-z0-9-]+?)-(fr|en)(?:-(\d+))?\.jpg$/.exec(chemin)
    if (!m) continue
    const [, prefixe, langue] = m
    const lot = lots.get(prefixe) ?? { fr: [], en: [] }
    lot[langue as Langue].push(IMAGES[chemin])
    lots.set(prefixe, lot)
  }
  return lots
}

const LOTS = lotsParPrefixe()

/** Les pages du feuillet dans la langue demandee, sinon dans l'autre ; `null` si le heros n'a aucun feuillet. */
export function pagesDansLaLangue(prefixe: string, langue: Langue): (() => Promise<string>)[] | null {
  const lot = LOTS.get(prefixe)
  if (!lot) return null
  const voulue = lot[langue]
  const autre = lot[langue === 'fr' ? 'en' : 'fr']
  return voulue.length > 0 ? voulue : autre.length > 0 ? autre : null
}

/** Une carte appartient a la cle : le prefixe d'un heros suivi de 3 chiffres, ou l'id exact d'un scenario. */
function correspond(cle: string, id: string): boolean {
  return new RegExp(/\d{3}$/.test(cle) ? `^${cle}(?!\\d)` : `^${cle}\\d{3}`).test(id)
}

/**
 * Les feuillets de la partie, sans doublon, dans l'ordre de ENTREES. `picIds` = les cartes qui identifient la partie :
 * l'identite de chaque heros, le vilain et les complots principaux.
 */
export function feuilletsDeLaPartie(picIds: readonly (string | undefined)[]): Feuillet[] {
  const langue = langueActuelle()
  const feuillets: Feuillet[] = []
  for (const [cle, { titre, lots = [cle] }] of Object.entries(ENTREES)) {
    if (!picIds.some((id) => id && correspond(cle, id))) continue
    const pages = lots.flatMap((lot) => pagesDansLaLangue(lot, langue) ?? [])
    if (pages.length > 0) feuillets.push({ prefixe: cle, titre, pages })
  }
  return feuillets
}
