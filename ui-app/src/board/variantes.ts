// Arts ALTERNATIFS des ressources doubles (promos « Play-and-Share » de FFG).
//
// Purement COSMETIQUE : la carte reste 01088/01089/01090 pour le moteur (memes
// regles, meme « Max 1 per deck »). Seule l'image affichee change.
//
// Le choix se fait a la PREPARATION (public/js/prepare/app.js), par heros, et
// vaut pour les TROIS ressources a la fois : une collection est coherente. On
// relit ici la meme cle localStorage, ecrite par le wizard.

/**
 * Une collection donne l'image des TROIS ressources doubles. Deux origines :
 *  - les promos « Play-and-Share » de FFG, decoupees des PDF -> « 01088_th » ;
 *  - les reeditions d'extension, qui ont leur PROPRE code de carte -> « 27020 ».
 * Doit rester aligne avec public/js/prepare/app.js.
 */
const COLLECTIONS: Record<string, [string, string, string]> = {
  // Promos FFG (Energy, Genius, Strength)
  bp: ['01088_bp', '01089_bp', '01090_bp'],
  cm: ['01088_cm', '01089_cm', '01090_cm'],
  sm: ['01088_sm', '01089_sm', '01090_sm'],
  sh: ['01088_sh', '01089_sh', '01090_sh'],
  mm: ['01088_mm', '01089_mm', '01090_mm'],
  im: ['01088_im', '01089_im', '01090_im'],
  ca: ['01088_ca', '01089_ca', '01090_ca'],
  th: ['01088_th', '01089_th', '01090_th'],
  ds: ['01088_ds', '01089_ds', '01090_ds'],
  hk: ['01088_hk', '01089_hk', '01090_hk'],
  hu: ['01088_hu', '01089_hu', '01090_hu'],
  sw: ['01088_sw', '01089_sw', '01090_sw'],
  am: ['01088_am', '01089_am', '01090_am'],
  bw: ['01088_bw', '01089_bw', '01090_bw'],
  wa: ['01088_wa', '01089_wa', '01090_wa'],
  // Collections « DesignHacker » (Dropbox de l'auteur, 2021-2022).
  // Identification faite a l'oeil sur planche-contact.
  dh_quicksilver: ['01088_dh_quicksilver', '01089_dh_quicksilver', '01090_dh_quicksilver'],
  dh_scarletwitch: ['01088_dh_scarletwitch', '01089_dh_scarletwitch', '01090_dh_scarletwitch'],
  dh_rocket: ['01088_dh_rocket', '01089_dh_rocket', '01090_dh_rocket'],
  dh_groot: ['01088_dh_groot', '01089_dh_groot', '01090_dh_groot'],
  dh_starlord: ['01088_dh_starlord', '01089_dh_starlord', '01090_dh_starlord'],
  dh_gamora: ['01088_dh_gamora', '01089_dh_gamora', '01090_dh_gamora'],
  dh_drax: ['01088_dh_drax', '01089_dh_drax', '01090_dh_drax'],
  dh_venom: ['01088_dh_venom', '01089_dh_venom', '01090_dh_venom'],
  dh_nebula: ['01088_dh_nebula', '01089_dh_nebula', '01090_dh_nebula'],
  dh_vision: ['01088_dh_vision', '01089_dh_vision', '01090_dh_vision'],
  dh_valkyrie: ['01088_dh_valkyrie', '01089_dh_valkyrie', '01090_dh_valkyrie'],
  dh_warmachine: ['01088_dh_warmachine', '01089_dh_warmachine', '01090_dh_warmachine'],
  dh_adamwarlock: ['01088_dh_adamwarlock', '01089_dh_adamwarlock', '01090_dh_adamwarlock'],
  dh_spectrum: ['01088_dh_spectrum', '01089_dh_spectrum', '01090_dh_spectrum'],
  dh_miles: ['01088_dh_miles', '01089_dh_miles', '01090_dh_miles'],
  dh_ghostspider: ['01088_dh_ghostspider', '01089_dh_ghostspider', '01090_dh_ghostspider'],
  // Collection fan-made « ekAugust », livree avec le pack Jessica Jones (73xxx).
  ekaug_jj: ['01088_ekaug_jj', '01089_ekaug_jj', '01090_ekaug_jj'],
  // Reeditions d'extension (art different, vrais codes de carte).
  // Sinister Motives (27020-22) est exclu : meme visuel que le jeu de base.
  mutant: ['32022', '32023', '32024'],
  shield: ['50025', '50026', '50027'],
  civilwar: ['56020', '56021', '56022'],
  // Re-skins livres PAR un pack fan-made (memes regles, autre illustration).
  // Ajoutes le 31/08/2026 : ils existaient dans data/cards.json avec leurs
  // images, mais n'etaient proposes nulle part.
  gwenpool: ['gp015', 'gp016', 'gp017'],
  howard: ['hd018', 'hd019', 'hd020'],
  ms_america: ['ma027', 'ma028', 'ma029'],
}

/**
 * Arts ALTERNATIFS des cartes de HEROS (planche « Alternate Art Hero Cards »
 * de M3T4LB0X, hallofheroeslcg.com). Meme principe que les ressources : la
 * carte reste la meme pour le moteur, seule l'image change.
 *
 * N'ont ete retenus que les arts dont les VALEURS IMPRIMEES (statistiques,
 * points de vie, taille de main, traits) sont identiques a notre carte : un
 * art qui afficherait d'autres chiffres mentirait en pleine partie. Sont donc
 * ecartes le Wasp de la planche (statistiques et traits differents des deux
 * formes de 13001), Beta Ray Bill (c'est un autre heros, pas un art) et le
 * Spider-Man « Bombastic Bag-Man » (trait imprime FANTASTIC FOUR au lieu
 * d'AVENGER).
 */
const ARTS_HEROS: Record<string, string[]> = {
  '01001a': ['m3t'], // Spider-Man
  '01010a': ['m3t'], // Captain Marvel
  '01019a': ['m3t'], // She-Hulk
  '01029a': ['m3t'], // Iron Man
  '03001a': ['m3t'], // Captain America
  '04001a': ['m3t'], // Hawkeye
}

/** Cle partagee avec le frontend de preparation. */
const CLE_HEROS = 'mc_hero_art_v1'

let artsHerosCache: Record<string, string> | undefined

/** Choix par heros, lu une seule fois : la page est rechargee apres un choix. */
function lireArtsHeros(): Record<string, string> {
  if (artsHerosCache === undefined) {
    try {
      const brut = window.localStorage.getItem(CLE_HEROS)
      artsHerosCache = brut ? (JSON.parse(brut) as Record<string, string>) : {}
    } catch {
      artsHerosCache = {}
    }
  }
  return artsHerosCache
}

/** Liste des arts disponibles pour une carte de heros (vide si aucun). */
export function artsDisponiblesPourHeros(cardId: string | undefined): string[] {
  return ARTS_HEROS[String(cardId ?? '').split(',')[0]!] ?? []
}

/** Applique l'art de heros choisi, s'il en existe un pour cette carte. */
function picIdHeros(picId: string): string {
  const codes = ARTS_HEROS[picId]
  if (!codes || codes.length === 0) return picId
  const choix = lireArtsHeros()[cleHeros(picId)]
  return choix && codes.includes(choix) ? `${picId}_${choix}` : picId
}

/** Position de chaque ressource dans une collection. */
const INDEX_RESSOURCE: Record<string, number> = { '01088': 0, '01089': 1, '01090': 2 }

/** Cle partagee avec le frontend de preparation. */
const CLE = 'mc_resource_art_v1'

/** Choix par heros : identifiant de carte SANS suffixe de face -> code. */
export type ArtsRessources = Record<string, string>

export function lireArtsRessources(): ArtsRessources {
  try {
    const brut = window.localStorage.getItem(CLE)
    return brut ? (JSON.parse(brut) as ArtsRessources) : {}
  } catch {
    return {}
  }
}

/**
 * Cle de heros commune aux deux frontends : identifiant de carte sans le
 * suffixe de face (« 43001a » et « 43001b » -> « 43001 »), pour que le choix
 * suive le heros quelle que soit sa forme en jeu.
 */
export function cleHeros(cardId: string | undefined): string {
  return String(cardId ?? '').split(',')[0]!.replace(/[a-z]$/, '')
}

/** Hachage court et stable, pour un aleatoire qui ne scintille pas. */
function melange(valeur: number): number {
  let x = (valeur + 0x9e3779b9) | 0
  x = Math.imul(x ^ (x >>> 16), 0x85ebca6b)
  x = Math.imul(x ^ (x >>> 13), 0xc2b2ae35)
  return (x ^ (x >>> 16)) >>> 0
}

/**
 * Code de collection A APPLIQUER pour un joueur, deja resolu :
 * '' (art standard) ou un code de collection.
 *
 * « random » est tire ICI, une fois par joueur et par partie : les trois
 * ressources partagent donc la meme collection, et elle ne change pas d'un
 * rendu a l'autre (le tirage depend de l'identifiant d'objet du heros).
 */
export function collectionPourJoueur(
  heroCardId: string | undefined,
  heroObjectId: number | undefined,
  arts: ArtsRessources
): string {
  const choix = arts[cleHeros(heroCardId)] ?? 'standard'
  if (choix === 'standard') return ''
  if (choix === 'random') {
    const codes = Object.keys(COLLECTIONS)
    return codes[melange(heroObjectId ?? 0) % codes.length]!
  }
  return choix in COLLECTIONS ? choix : ''
}

/**
 * Identifiant d'image a afficher. Ne change QUE pour les trois ressources
 * doubles, et seulement si une collection est choisie.
 */
export function picIdAffiche(picId: string, collection: string | undefined): string {
  // Les deux mecanismes ne se croisent jamais : une carte est soit une des
  // trois ressources doubles, soit une carte de heros.
  const avecArtHeros = picIdHeros(picId)
  if (avecArtHeros !== picId) return avecArtHeros
  if (!collection) return picId
  const index = INDEX_RESSOURCE[picId]
  if (index === undefined) return picId
  return COLLECTIONS[collection]?.[index] ?? picId
}
