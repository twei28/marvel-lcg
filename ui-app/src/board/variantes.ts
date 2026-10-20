// Arts ALTERNATIFS des ressources doubles (promos « Play-and-Share » de FFG).
//
// Purement COSMETIQUE : la carte reste 01088/01089/01090 pour le moteur (memes
// regles, meme « Max 1 per deck »). Seule l'image affichee change.
//
// Le choix se fait a la PREPARATION (public/js/prepare/app.js), par heros, et
// vaut pour les TROIS ressources a la fois : une collection est coherente. On
// relit ici la meme cle localStorage, ecrite par le wizard.

import { picIdCarte, serieDuHeros } from './arts-cartes'

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
  // Collection « Kajislav », livree avec le heros Binary (Galactic Storm, gs001, 20/10/2026).
  binary: ['01088_binary', '01089_binary', '01090_binary'],
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
  // Ressources TMNT (pack Basic, Inkwire) : art seul, meme regles. Par defaut
  // pour un heros TMNT (voir collectionPourJoueur).
  tmnt: ['ub011', 'ub016', 'ub054'],
  // Idem, ajoutes le 22/09/2026 : Angel, Beast, Gambit, Human Torch, Jubilee,
  // Magneto, The Thing, Wave. Chaque pack a ses PROPRES card_id (pas de
  // full_link vers 01088/89/90) ; sans objet ici, purement cosmetique.
  angel: ['42033', '42034', '42035'],
  beast: ['bt024', 'bt025', 'bt026'],
  gambit: ['37036', '37037', '37038'],
  human_torch: ['ht015', 'ht016', 'ht017'],
  jubilee: ['47035', '47036', '47037'],
  magneto: ['49043', '49044', '49045'],
  the_thing: ['th016', 'th017', 'th018'],
  wave: ['65017', '65018', '65019'],
}

/**
 * Arts ALTERNATIFS des cartes de HEROS, par FACE (la carte reste la meme pour
 * le moteur, seule l'image change). Trois series :
 *  - m3t  : planche « Alternate Art Hero Cards » de M3T4LB0X ;
 *  - cb   : zip « Marvel Champions Alt Art » (style comic, Core Set a Defenders) ;
 *  - rog, rog2 : album Flickr de The Rose of Gondolin.
 *
 * N'ont ete retenus que les arts dont les VALEURS et le TEXTE imprimes sont
 * identiques a notre carte. Ecartes : le Wasp, Beta Ray Bill et le Spider-Man
 * « Bag-Man » de M3T4LB0X ; War Machine et Wolverine alter ego « cb » (limite
 * ajoutee, recherche de Wolverine's Claws absente) ; Rogue heros « rog »
 * (« Action » au lieu de « Forced Response ») : la face heros de Rogue garde
 * donc son scan sous les codes rog et rog2, seuls l'alter ego et Touched changent.
 */
const ARTS_HEROS: Record<string, string[]> = {
  '01001a': ['m3t', 'cb'],
  '01001b': ['cb'],
  '01010a': ['m3t', 'cb'],
  '01010b': ['cb'],
  '01019a': ['m3t', 'cb', 'rog'],
  '01019b': ['cb', 'rog'],
  '01029a': ['m3t', 'cb'],
  '01029b': ['cb'],
  '01040a': ['cb'],
  '01040b': ['cb'],
  '03001a': ['m3t', 'cb'],
  '03001b': ['cb'],
  '04001a': ['m3t', 'cb'],
  '04001b': ['cb'],
  '04031a': ['cb'],
  '04031b': ['cb'],
  '05001a': ['cb', 'rog', 'rog2'],
  '05001b': ['cb', 'rog', 'rog2'],
  '06001a': ['cb'],
  '06001b': ['cb'],
  '08001a': ['cb'],
  '08001b': ['cb'],
  '09001a': ['cb'],
  '09001b': ['cb'],
  '10001a': ['cb'],
  '10001b': ['cb'],
  '12001a': ['cb'],
  '12001b': ['cb'],
  '12001c': ['cb'],
  '13001a': ['cb'],
  '13001b': ['cb'],
  '13001c': ['cb'],
  '14001a': ['cb'],
  '14001b': ['cb'],
  '15001a': ['cb', 'rog', 'rog2'],
  '15001b': ['cb', 'rog', 'rog2'],
  '16001a': ['cb'],
  '16001b': ['cb'],
  '16029a': ['cb'],
  '16029b': ['cb'],
  '17001a': ['cb'],
  '17001b': ['cb'],
  '18001a': ['cb'],
  '18001b': ['cb'],
  '19001a': ['cb'],
  '19001b': ['cb'],
  '20001a': ['cb'],
  '20001b': ['cb'],
  '21001a': ['cb'],
  '21001b': ['cb'],
  '21031a': ['cb', 'rog'],
  '21031b': ['cb', 'rog'],
  '22001a': ['cb'],
  '22001b': ['cb'],
  '23001a': ['cb'],
  '25001a': ['cb'],
  '25001b': ['cb'],
  '26001a': ['cb'],
  '26001b': ['cb'],
  '27001a': ['cb'],
  '27001b': ['cb'],
  '27030a': ['cb'],
  '27030b': ['cb'],
  '28001a': ['cb'],
  '28001b': ['cb'],
  '29001a': ['cb'],
  '29001b': ['cb'],
  '29002a': ['cb'],
  '29002b': ['cb'],
  '29003a': ['cb'],
  '29003b': ['cb'],
  '30001a': ['cb'],
  '30001b': ['cb'],
  '31001a': ['cb', 'rog'],
  '31001b': ['cb', 'rog'],
  '31002a': ['cb', 'rog'],
  '31002b': ['cb', 'rog'],
  '32001a': ['cb'],
  '32001b': ['cb'],
  '32030a': ['cb', 'rog'],
  '32030b': ['cb', 'rog'],
  '33001a': ['cb'],
  '33001b': ['cb'],
  '34001a': ['cb'],
  '34001b': ['cb'],
  '35001a': ['cb'],
  '36001a': ['cb'],
  '36001b': ['cb'],
  '37001a': ['cb'],
  '37001b': ['cb'],
  '38001a': ['cb', 'rog', 'rog2'],
  '38001b': ['cb', 'rog', 'rog2'],
  '38002': ['rog', 'rog2'],
  '40001a': ['cb'],
  '40001b': ['cb'],
  '40037a': ['cb', 'rog'],
  '40037b': ['cb', 'rog'],
  '41001a': ['cb'],
  '41001b': ['cb'],
  '42001a': ['cb'],
  '42001b': ['cb'],
  '42001c': ['cb'],
  '43001a': ['cb', 'rog'],
  '43001b': ['cb'],
  '44001a': ['cb'],
  '44001b': ['cb'],
  '45001a': ['cb'],
  '45001b': ['cb'],
  '45030a': ['cb'],
  '45030b': ['cb'],
  '46001a': ['cb'],
  '46001b': ['cb'],
  '47001a': ['cb'],
  '47001b': ['cb'],
  '48001a': ['cb'],
  '48001b': ['cb'],
  '49001a': ['cb'],
  '49001b': ['cb'],
  '50001a': ['cb'],
  '50001b': ['cb'],
  '50034a': ['cb'],
  '50034b': ['cb'],
  '51001a': ['cb'],
  '51001b': ['cb'],
  '52001a': ['cb'],
  '52001b': ['cb'],
  '53001a': ['cb'],
  '53001b': ['cb'],
  '54001a': ['cb'],
  '54001b': ['cb'],
  '56001a': ['cb'],
  '56001b': ['cb'],
  '56029a': ['cb'],
  '56029b': ['cb'],
  '58001a': ['cb'],
  '58001b': ['cb'],
  '59001a': ['cb'],
  '59001b': ['cb'],
  '60001a': ['cb'],
  '60001b': ['cb'],
  '60037a': ['cb'],
  '60037b': ['cb'],
  '61001a': ['cb'],
  '61001b': ['cb'],
  '62001a': ['cb'],
  '62001b': ['cb'],
}

/**
 * Cartes dont le choix d'art est celui d'un AUTRE identifiant de heros : le
 * choix est range sous la cle du heros du wizard (« 38001 » pour Rogue), et
 * Touched, les pieces de SP//dr ou les formes 2 et 3 d'Ironheart n'en portent
 * pas le numero.
 */
const HEROS_DE_LA_CARTE: Record<string, string> = {
  '29002': '29001',
  '29003': '29001',
  '31002': '31001',
  '38002': '38001',
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

/**
 * Applique l'art de heros choisi, s'il en existe un pour cette carte.
 *
 * Le choix est range sous la cle du heros (« 38001 ») et vaut pour toutes ses
 * faces. L'alter ego peut avoir le sien, sous « 38001b » : il l'emporte sur
 * celui du heros, y compris la valeur « standard » (qui n'est un code d'aucune
 * serie, donc rend le scan).
 */
function picIdHeros(picId: string): string {
  const codes = ARTS_HEROS[picId]
  if (!codes || codes.length === 0) return picId
  const cle = cleHeros(picId)
  const cleChoix = HEROS_DE_LA_CARTE[cle] ?? cle
  const choix = lireArtsHeros()
  const choisi = (picId.endsWith('b') ? choix[`${cleChoix}b`] : undefined) ?? choix[cleChoix]
  return choisi && codes.includes(choisi) ? `${picId}_${choisi}` : picId
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
  // Sans choix enregistre : la collection TMNT pour un heros TMNT, sinon l'art standard.
  const parDefaut = serieDuHeros(heroCardId) === 'tmnt' ? 'tmnt' : 'standard'
  const choix = arts[cleHeros(heroCardId)] ?? parDefaut
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
export function picIdAffiche(
  picId: string,
  collection: string | undefined,
  herosCardId?: string
): string {
  // Les mecanismes ne se croisent jamais : une carte est soit une des trois
  // ressources doubles, soit une carte de heros, soit une carte de deck a art
  // alternatif (arts-cartes.ts, table mc_card_art_v1).
  const avecArtHeros = picIdHeros(picId)
  if (avecArtHeros !== picId) return avecArtHeros
  const avecArtCarte = picIdCarte(picId, herosCardId)
  if (avecArtCarte !== picId) return avecArtCarte
  if (!collection) return picId
  const index = INDEX_RESSOURCE[picId]
  if (index === undefined) return picId
  return COLLECTIONS[collection]?.[index] ?? picId
}
