// LA TABLE PAR BRIQUES (decisions du 05/10/2026, .planning/todos/2026-10-05-table-par-briques-decisions.md).
//
// Une zone de la table n'est plus une case fixe : c'est un ASSEMBLAGE DE
// BRIQUES (Heros, Soutiens, Allies, Mechant, Sbires, Environnement, Manigance
// principale, Manigances annexes), au titre automatique. On sort une brique de
// sa zone = une nouvelle zone ; on la depose sur une autre zone = fusion, titre
// « X et Y ». Les piles (rencontre, heros), « Mises de cote » et la main
// restent des zones seules, comme avant.
//
// Module PUR : ni DOM ni stockage. Il remplacera disposition.ts a l'etape 2.

/** Toutes les briques, dans l'ORDRE FIXE du jeu (celui des zones fusionnees). */
export const BRIQUES = [
  'piles-rencontre',
  'heros',
  'soutiens',
  'allies',
  'mechant',
  'sbires',
  'environnements',
  'manigance-principale',
  'manigances-annexes',
  'piles-joueur',
  'annexes',
  'main',
] as const

export type CleBrique = (typeof BRIQUES)[number]

/** Les briques qui restent des zones seules : jamais separees ni fusionnees. */
export const EPINGLEES: readonly CleBrique[] = ['piles-rencontre', 'piles-joueur', 'annexes', 'main']

export const estEpinglee = (brique: CleBrique) => EPINGLEES.includes(brique)

/** Le nom d'une brique dans un titre de zone (singulier d'« Environnement » comme aujourd'hui). */
export const NOMS: Record<CleBrique, string> = {
  'piles-rencontre': 'Deck Rencontre',
  heros: 'Héros',
  soutiens: 'Soutiens',
  allies: 'Alliés',
  mechant: 'Méchant',
  sbires: 'Sbires',
  environnements: 'Environnement',
  'manigance-principale': 'Manigance principale',
  'manigances-annexes': 'Manigances annexes',
  'piles-joueur': 'Deck du héros',
  annexes: 'Mises de côté / autres piles',
  main: 'Ta main',
}

/**
 * Le titre d'une zone : « Heros », « Heros et soutiens »,
 * « Allies, sbires et environnement ». `nom` et `et` laissent le plateau
 * traduire.
 */
export function titreDeZone(
  briques: readonly CleBrique[],
  nom: (brique: CleBrique) => string = (b) => NOMS[b],
  et = 'et'
): string {
  const noms = briques.map((b, i) => {
    const texte = nom(b)
    return i === 0 ? texte : texte.charAt(0).toLowerCase() + texte.slice(1)
  })
  if (noms.length < 2) return noms.join('')
  return `${noms.slice(0, -1).join(', ')} ${et} ${noms[noms.length - 1]}`
}

/**
 * La place d'une zone : un rectangle de la grille (colonne et ligne de depart,
 * a partir de 1, largeur et hauteur en cases) et la TAILLE DE SES CARTES
 * (1 = la taille ordinaire de la table), UNE pour toute la zone.
 */
export type PlaceZone = { col: number; ligne: number; largeur: number; hauteur: number; taille: number }

/** Une zone : ses briques (dans l'ordre fixe) et sa place. Son identifiant est sa PREMIERE brique. */
export type Zone = PlaceZone & { briques: CleBrique[] }

export type Disposition = { colonnes: number; lignes: number; zones: Zone[] }

/** Les bornes de la poignee de taille des cartes. */
export const TAILLE_BORNES: [number, number] = [0.6, 1.6]

const rang = (brique: CleBrique) => BRIQUES.indexOf(brique)
const trier = (briques: readonly CleBrique[]) => [...briques].sort((a, b) => rang(a) - rang(b))

/** L'identifiant d'une zone : sa premiere brique. */
export const ancre = (zone: Zone): CleBrique => zone.briques[0]

/** La forme canonique : zones non vides, briques et zones dans l'ordre fixe. */
function canonique(zones: Zone[]): Zone[] {
  return zones
    .filter((z) => z.briques.length > 0)
    .map((z) => ({ ...z, briques: trier(z.briques) }))
    .sort((a, b) => rang(ancre(a)) - rang(ancre(b)))
}

export const zoneDe = (d: Disposition, brique: CleBrique): Zone | undefined =>
  d.zones.find((z) => z.briques.includes(brique))

const place = (col: number, ligne: number, largeur = 1, hauteur = 1, briques: CleBrique[]): Zone => ({
  briques,
  col,
  ligne,
  largeur,
  hauteur,
  taille: 1,
})

/**
 * La table d'origine : la bande des manigances en haut (piles rencontre,
 * mechant, manigance principale, annexes), puis le combat (allies, sbires,
 * environnement), le heros et ses soutiens, la main ; les piles a gauche.
 */
export const DISPOSITION_ORIGINE: Disposition = {
  colonnes: 4,
  lignes: 4,
  zones: canonique([
    place(1, 1, 1, 1, ['piles-rencontre']),
    place(2, 1, 1, 1, ['mechant']),
    place(3, 1, 1, 1, ['manigance-principale']),
    place(4, 1, 1, 1, ['manigances-annexes']),
    place(2, 2, 3, 1, ['allies', 'sbires', 'environnements']),
    place(1, 3, 1, 1, ['piles-joueur']),
    place(2, 3, 3, 1, ['heros', 'soutiens']),
    place(1, 4, 1, 1, ['annexes']),
    place(2, 4, 3, 1, ['main']),
  ]),
}

/** `grid-template-areas` de la disposition : chaque aire porte l'identifiant de sa zone. */
export function aireDeGrille(disposition: Disposition): string {
  const cases = Array.from({ length: disposition.lignes }, () =>
    Array.from({ length: disposition.colonnes }, () => '.')
  )
  for (const zone of disposition.zones) {
    for (let l = zone.ligne; l < zone.ligne + zone.hauteur; l++) {
      for (let c = zone.col; c < zone.col + zone.largeur; c++) {
        if (cases[l - 1]?.[c - 1] !== undefined) cases[l - 1][c - 1] = ancre(zone)
      }
    }
  }
  return cases.map((ligne) => `'${ligne.join(' ')}'`).join('\n')
}

const recouvre = (a: PlaceZone, b: PlaceZone) =>
  a.col < b.col + b.largeur && b.col < a.col + a.largeur && a.ligne < b.ligne + b.hauteur && b.ligne < a.ligne + a.hauteur

/** Les paires de zones (par identifiant) qui se chevauchent. */
export function chevauchements(disposition: Disposition): [CleBrique, CleBrique][] {
  const paires: [CleBrique, CleBrique][] = []
  disposition.zones.forEach((a, i) => {
    for (const b of disposition.zones.slice(i + 1)) {
      if (recouvre(a, b)) paires.push([ancre(a), ancre(b)])
    }
  })
  return paires
}

/**
 * Une disposition qu'on peut dessiner : chaque brique dans UNE zone et une
 * seule, les briques epinglees seules, chaque zone entiere dans la grille,
 * d'au moins une case, sa taille de cartes dans les bornes, aucun chevauchement.
 */
export function estValide(disposition: Disposition): boolean {
  const entier = (n: unknown) => typeof n === 'number' && Number.isInteger(n)
  const vues = new Set<CleBrique>()
  for (const zone of disposition.zones) {
    if (zone.briques.length === 0) return false
    if (zone.briques.length > 1 && zone.briques.some(estEpinglee)) return false
    for (const b of zone.briques) {
      if (!BRIQUES.includes(b) || vues.has(b)) return false
      vues.add(b)
    }
    if (![zone.col, zone.ligne, zone.largeur, zone.hauteur].every(entier)) return false
    if (zone.largeur < 1 || zone.hauteur < 1 || zone.col < 1 || zone.ligne < 1) return false
    if (zone.col + zone.largeur - 1 > disposition.colonnes || zone.ligne + zone.hauteur - 1 > disposition.lignes) return false
    if (!(zone.taille >= TAILLE_BORNES[0] && zone.taille <= TAILLE_BORNES[1])) return false
  }
  if (vues.size !== BRIQUES.length) return false
  return chevauchements(disposition).length === 0
}

/** Le style de la scene : ses aires, depuis les donnees. La grille d'origine
 *  garde les colonnes de board.css ; une grille personnalisee a des cases
 *  EGALES, c'est ce qui la rend aimantee. */
export function styleDeGrille(disposition: Disposition): Record<string, string> {
  if (disposition === DISPOSITION_ORIGINE) return { gridTemplateAreas: aireDeGrille(disposition) }
  return {
    gridTemplateAreas: aireDeGrille(disposition),
    gridTemplateColumns: `repeat(${disposition.colonnes}, minmax(0, 1fr))`,
    gridTemplateRows: `repeat(${disposition.lignes}, minmax(0, 1fr))`,
  }
}

// ----------------------------------------------------------------------------
// LA GRILLE AIMANTEE DE L'EDITEUR : 12 colonnes x 8 lignes, cases egales.

export const GRILLE = { colonnes: 12, lignes: 8 }

/** Une manigance principale posee en paysage (176 px), son liseré et l'ecart. */
export const LARGEUR_MANIGANCE_PRINCIPALE = 210

/**
 * PLUSIEURS MANIGANCES PRINCIPALES COTE A COTE (10/10/2026, Tower Defense) : sur
 * une table personnalisee, la zone principale gagne les cases qui lui manquent
 * sur celle des annexes, quand celle-ci la jouxte sur les memes rangees. Calcule
 * au rendu, rien n'est enregistre : quand une principale quitte le jeu, la table
 * du joueur revient d'elle-meme. La table d'origine, elle, s'elargit par sa
 * colonne `auto` (bande-manigances.css).
 */
export function elargirManigancePrincipale(d: Disposition, nombre: number, largeurScene: number): Disposition {
  if (d === DISPOSITION_ORIGINE || nombre <= 1) return d
  const principale = zoneDe(d, 'manigance-principale')
  const annexes = zoneDe(d, 'manigances-annexes')
  if (!principale || !annexes || principale === annexes) return d
  if (principale.ligne !== annexes.ligne || principale.hauteur !== annexes.hauteur) return d
  const caseL = largeurScene / d.colonnes
  const seule = principale.briques.length === 1
  const voulu = seule
    ? Math.ceil((nombre * LARGEUR_MANIGANCE_PRINCIPALE) / caseL)
    : principale.largeur + Math.ceil(((nombre - 1) * LARGEUR_MANIGANCE_PRINCIPALE) / caseL)
  const prendre = Math.min(voulu - principale.largeur, annexes.largeur - 1)
  if (prendre <= 0) return d
  const aDroite = annexes.col === principale.col + principale.largeur
  const aGauche = annexes.col + annexes.largeur === principale.col
  if (!aDroite && !aGauche) return d
  const zones = d.zones.map((z) => {
    if (z === principale) return { ...z, largeur: z.largeur + prendre, col: aGauche ? z.col - prendre : z.col }
    if (z === annexes) return { ...z, largeur: z.largeur - prendre, col: aDroite ? z.col + prendre : z.col }
    return z
  })
  return { ...d, zones }
}

const MINIMUM_EPINGLEE: Partial<Record<CleBrique, { largeur: number; hauteur: number }>> = {
  'piles-rencontre': { largeur: 1, hauteur: 2 },
  'piles-joueur': { largeur: 1, hauteur: 2 },
  annexes: { largeur: 1, hauteur: 1 },
  main: { largeur: 4, hauteur: 2 },
}

/**
 * Le plus petit rectangle d'une zone, en cases de la grille 12 x 8 : une
 * brique seule tient dans 2 x 2, deux briques ou plus ont de quoi aligner un
 * rang (3 x 2) ; les epinglees gardent leur minimum d'avant.
 */
export function minimumDeZone(briques: readonly CleBrique[]): { largeur: number; hauteur: number } {
  if (briques.length === 1 && MINIMUM_EPINGLEE[briques[0]]) return MINIMUM_EPINGLEE[briques[0]]!
  return { largeur: briques.length > 1 ? 3 : 2, hauteur: 2 }
}

/** La disposition d'origine reportee sur la grille 12 x 8 : le point de depart de l'editeur. */
export const DISPOSITION_DE_DEPART: Disposition = {
  ...GRILLE,
  zones: canonique([
    place(1, 1, 2, 2, ['piles-rencontre']),
    place(3, 1, 2, 2, ['mechant']),
    place(5, 1, 3, 2, ['manigance-principale']),
    place(8, 1, 5, 2, ['manigances-annexes']),
    place(3, 3, 10, 2, ['allies', 'sbires', 'environnements']),
    place(3, 5, 10, 2, ['heros', 'soutiens']),
    place(1, 5, 2, 2, ['piles-joueur']),
    place(1, 7, 2, 2, ['annexes']),
    place(3, 7, 10, 2, ['main']),
  ]),
}

const respecteLesMinimums = (d: Disposition) =>
  d.zones.every((z) => {
    const m = minimumDeZone(z.briques)
    return z.largeur >= m.largeur && z.hauteur >= m.hauteur
  })

/** Les zones rangees en forme canonique, ou `undefined` si la disposition ne tient pas. */
function remplacer(d: Disposition, zones: Zone[]): Disposition | undefined {
  const suivante: Disposition = { ...d, zones: canonique(zones) }
  return estValide(suivante) && respecteLesMinimums(suivante) ? suivante : undefined
}

const modifier = (d: Disposition, cible: Zone, changement: Partial<Zone>): Zone[] =>
  d.zones.map((z) => (z === cible ? { ...z, ...changement } : z))

const zoneParAncre = (d: Disposition, cle: CleBrique) => d.zones.find((z) => ancre(z) === cle)

/** La zone `cle` (son identifiant) posee ailleurs, ou `undefined` si elle ne tient pas. */
export function deplacer(d: Disposition, cle: CleBrique, col: number, ligne: number): Disposition | undefined {
  const zone = zoneParAncre(d, cle)
  return zone && remplacer(d, modifier(d, zone, { col, ligne }))
}

/** La zone agrandie ou reduite, sans descendre sous son minimum ni chevaucher. */
export function redimensionner(d: Disposition, cle: CleBrique, largeur: number, hauteur: number): Disposition | undefined {
  const zone = zoneParAncre(d, cle)
  return zone && remplacer(d, modifier(d, zone, { largeur, hauteur }))
}

/** La taille des cartes de la zone, bornee et arrondie au vingtieme. */
export function changerTaille(d: Disposition, cle: CleBrique, taille: number): Disposition {
  const zone = zoneParAncre(d, cle)
  if (!zone) return d
  const bornee = Math.min(TAILLE_BORNES[1], Math.max(TAILLE_BORNES[0], Math.round(taille * 20) / 20))
  return { ...d, zones: modifier(d, zone, { taille: bornee }) }
}

/**
 * Sort `brique` de sa zone : elle devient une zone a elle, posee en (`col`,
 * `ligne`) a son plus petit, avec la taille de cartes de la zone d'ou elle
 * vient. `undefined` si elle est seule dans sa zone, epinglee, ou si la place
 * est prise.
 */
export function separer(d: Disposition, brique: CleBrique, col: number, ligne: number): Disposition | undefined {
  const source = zoneDe(d, brique)
  if (!source || source.briques.length < 2 || estEpinglee(brique)) return undefined
  const m = minimumDeZone([brique])
  const nouvelle: Zone = { briques: [brique], col, ligne, largeur: m.largeur, hauteur: m.hauteur, taille: source.taille }
  return remplacer(d, [...modifier(d, source, { briques: source.briques.filter((b) => b !== brique) }), nouvelle])
}

/**
 * Depose `brique` sur la zone `cle` : elles ne font plus qu'une, au titre
 * combine, a la taille de cartes de la zone d'accueil (agrandie au besoin pour
 * son nouveau minimum). La zone d'ou vient la brique disparait si elle
 * devient vide. `undefined` si une brique est epinglee ou si l'agrandissement
 * ne tient pas.
 */
export function fusionner(d: Disposition, brique: CleBrique, cle: CleBrique): Disposition | undefined {
  const source = zoneDe(d, brique)
  const cible = zoneParAncre(d, cle)
  if (!source || !cible || source === cible || estEpinglee(brique) || cible.briques.some(estEpinglee)) return undefined
  const briques = [...cible.briques, brique]
  const m = minimumDeZone(briques)
  const accueil: Zone = {
    ...cible,
    briques,
    largeur: Math.max(cible.largeur, m.largeur),
    hauteur: Math.max(cible.hauteur, m.hauteur),
  }
  const reste = d.zones
    .filter((z) => z !== cible)
    .map((z) => (z === source ? { ...z, briques: z.briques.filter((b) => b !== brique) } : z))
  return remplacer(d, [...reste, accueil])
}

/** La zone qui couvre cette case, s'il y en a une. */
export const zoneSousLaCase = (d: Disposition, col: number, ligne: number): Zone | undefined =>
  d.zones.find((z) => col >= z.col && col < z.col + z.largeur && ligne >= z.ligne && ligne < z.ligne + z.hauteur)

/**
 * Le geste de l'editeur : la pastille `brique` est lachee sur la case (`col`,
 * `ligne`). Sur une AUTRE zone, elles fusionnent ; sur sa propre zone, rien ne
 * change ; ailleurs, la brique sort de sa zone (si elle n'y est pas seule).
 * `undefined` si le geste ne tient pas.
 */
export function deposerBrique(d: Disposition, brique: CleBrique, col: number, ligne: number): Disposition | undefined {
  const source = zoneDe(d, brique)
  if (!source) return undefined
  const dessous = zoneSousLaCase(d, col, ligne)
  if (dessous === source) return d
  if (dessous) return fusionner(d, brique, ancre(dessous))
  return separer(d, brique, col, ligne)
}

// ----------------------------------------------------------------------------
// LE TEXTE COMPACT, partage avec le serveur (`_table_valide`, server_get.py) :
//   « 12x8|he+so:col,ligne,largeur,hauteur,taille% ; ... »
// Chaque zone : les codes de ses briques separes par « + », puis sa place.
// L'ANCIEN texte (neuf zones, sans codes) reste lu et converti : les briques
// nouvelles restent dans la zone d'ou elles viennent.

const CODES: Record<CleBrique, string> = {
  'piles-rencontre': 'pr',
  heros: 'he',
  soutiens: 'so',
  allies: 'al',
  mechant: 'me',
  sbires: 'sb',
  environnements: 'en',
  'manigance-principale': 'mp',
  'manigances-annexes': 'mx',
  'piles-joueur': 'pj',
  annexes: 'an',
  main: 'ma',
}

const BRIQUE_DU_CODE = new Map(BRIQUES.map((b) => [CODES[b], b] as const))

/** Les neuf zones de l'ancien format, dans leur ordre, et les briques qu'elles contiennent. */
const ANCIENNES_ZONES: CleBrique[][] = [
  ['piles-rencontre'],
  ['mechant'],
  ['manigance-principale'],
  ['manigances-annexes'],
  ['allies', 'sbires', 'environnements'],
  ['heros', 'soutiens'],
  ['piles-joueur'],
  ['annexes'],
  ['main'],
]

export function ecrireTable(d: Disposition): string {
  const zones = d.zones.map((z) => {
    const codes = z.briques.map((b) => CODES[b]).join('+')
    return `${codes}:${z.col},${z.ligne},${z.largeur},${z.hauteur},${Math.round(z.taille * 100)}`
  })
  return `${d.colonnes}x${d.lignes}|${zones.join(';')}`
}

const lirePlace = (texte: string): PlaceZone | undefined => {
  const nombres = texte.split(',')
  if (nombres.length !== 5 || !nombres.every((n) => /^\d+$/.test(n))) return undefined
  const [col, ligne, largeur, hauteur, pourcent] = nombres.map(Number)
  return { col, ligne, largeur, hauteur, taille: pourcent / 100 }
}

/**
 * Relit un texte compact (nouveau ou ancien format). Tout ce qui ne tient pas
 * (forme, brique manquante ou en double, bornes, chevauchement, zone sous son
 * minimum) rend `undefined` : la table REVIENT ALORS A L'ORIGINE, c'est la
 * remise en ordre automatique.
 */
export function lireTable(brut: unknown): Disposition | undefined {
  if (typeof brut !== 'string') return undefined
  const [tete, corps, ...reste] = brut.split('|')
  if (tete !== `${GRILLE.colonnes}x${GRILLE.lignes}` || corps === undefined || reste.length > 0) return undefined
  const morceaux = corps.split(';')
  const ancien = morceaux.every((m) => !m.includes(':'))
  if (ancien && morceaux.length !== ANCIENNES_ZONES.length) return undefined
  const zones: Zone[] = []
  for (const [rang, morceau] of morceaux.entries()) {
    let briques: CleBrique[]
    let nombres: string
    if (ancien) {
      briques = ANCIENNES_ZONES[rang]
      nombres = morceau
    } else {
      const [codes, suite, ...trop] = morceau.split(':')
      if (suite === undefined || trop.length > 0) return undefined
      const lues = codes.split('+').map((c) => BRIQUE_DU_CODE.get(c))
      if (lues.some((b) => b === undefined)) return undefined
      briques = lues as CleBrique[]
      nombres = suite
    }
    const p = lirePlace(nombres)
    if (!p) return undefined
    zones.push({ briques, ...p })
  }
  return remplacer({ ...GRILLE, zones: [] }, zones)
}

/** La cle de preference du compte pour ce nombre de joueurs (1 a 4). */
export function cleTable(nombreDeJoueurs: number): string {
  return `table-${Math.min(4, Math.max(1, Math.round(nombreDeJoueurs) || 1))}`
}

/** Le style d'une zone : la taille de ses cartes, quand elle n'est pas 1. */
export function styleDeZone(zone: Zone | undefined): Record<string, string> {
  if (!zone || zone.taille === 1) return {}
  return { '--taille-zone': String(zone.taille) }
}
