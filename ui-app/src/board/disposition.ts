// LA DISPOSITION DE LA TABLE (plateau PC), decrite par des DONNEES.
//
// Table personnalisable, decisions du 04/10/2026 (questions une a une) :
// Reglages → « Modifier la table », grille AIMANTEE sans chevauchement, TOUTES
// les zones deplacables (main comprise), deux poignees par zone (la place, la
// taille des cartes), une disposition par nombre de joueurs, « Disposition
// d'origine » remet tout. Telephone inchange.
//
// Etape 1 : la disposition d'ORIGINE, celle de bande-manigances.css, ecrite ici
// sans rien changer a l'ecran (`disposition.test.ts` compare les deux).
//
// Module PUR : ni DOM ni stockage.

/** Les zones de la table PC, une par aire de la grille (board.css). */
export const ZONES = [
  'piles-rencontre',
  'rencontre',
  'complot-principal',
  'complots-secondaires',
  'terrain-combat',
  'terrain-soutien',
  'piles-joueur',
  'annexes',
  'main',
] as const

export type CleZone = (typeof ZONES)[number]

/**
 * La place d'une zone : un rectangle de la grille (colonne et ligne de depart,
 * a partir de 1, largeur et hauteur en cases) et la TAILLE DE SES CARTES
 * (1 = la taille ordinaire de la table).
 */
export type PlaceZone = { col: number; ligne: number; largeur: number; hauteur: number; taille: number }

export type Disposition = { colonnes: number; lignes: number; zones: Record<CleZone, PlaceZone> }

/** Les bornes de la poignee de taille des cartes. */
export const TAILLE_BORNES: [number, number] = [0.6, 1.6]

const place = (col: number, ligne: number, largeur = 1, hauteur = 1): PlaceZone => ({
  col,
  ligne,
  largeur,
  hauteur,
  taille: 1,
})

/**
 * La table d'origine, celle de bande-manigances.css : la bande des manigances
 * en haut (piles rencontre, mechant, manigance principale, annexes), puis le
 * combat, le heros et ses soutiens, la main ; les piles a gauche.
 */
export const DISPOSITION_ORIGINE: Disposition = {
  colonnes: 4,
  lignes: 4,
  zones: {
    'piles-rencontre': place(1, 1),
    rencontre: place(2, 1),
    'complot-principal': place(3, 1),
    'complots-secondaires': place(4, 1),
    'terrain-combat': place(2, 2, 3),
    'piles-joueur': place(1, 3),
    'terrain-soutien': place(2, 3, 3),
    annexes: place(1, 4),
    main: place(2, 4, 3),
  },
}

/** `grid-template-areas` de la disposition, une ligne de grille par ligne. */
export function aireDeGrille(disposition: Disposition): string {
  const cases = Array.from({ length: disposition.lignes }, () =>
    Array.from({ length: disposition.colonnes }, () => '.')
  )
  for (const zone of ZONES) {
    const p = disposition.zones[zone]
    for (let l = p.ligne; l < p.ligne + p.hauteur; l++) {
      for (let c = p.col; c < p.col + p.largeur; c++) {
        if (cases[l - 1]?.[c - 1] !== undefined) cases[l - 1][c - 1] = zone
      }
    }
  }
  return cases.map((ligne) => `'${ligne.join(' ')}'`).join('\n')
}

const recouvre = (a: PlaceZone, b: PlaceZone) =>
  a.col < b.col + b.largeur && b.col < a.col + a.largeur && a.ligne < b.ligne + b.hauteur && b.ligne < a.ligne + a.hauteur

/** Les paires de zones qui se chevauchent (dans l'ordre de `ZONES`). */
export function chevauchements(disposition: Disposition): [CleZone, CleZone][] {
  const paires: [CleZone, CleZone][] = []
  ZONES.forEach((a, i) => {
    for (const b of ZONES.slice(i + 1)) {
      if (recouvre(disposition.zones[a], disposition.zones[b])) paires.push([a, b])
    }
  })
  return paires
}

/**
 * Une disposition qu'on peut dessiner : chaque zone presente, entiere dans la
 * grille, d'au moins une case, sa taille de cartes dans les bornes, et aucun
 * chevauchement.
 */
export function estValide(disposition: Disposition): boolean {
  const entier = (n: unknown) => typeof n === 'number' && Number.isInteger(n)
  for (const zone of ZONES) {
    const p = disposition.zones[zone]
    if (!p || ![p.col, p.ligne, p.largeur, p.hauteur].every(entier)) return false
    if (p.largeur < 1 || p.hauteur < 1 || p.col < 1 || p.ligne < 1) return false
    if (p.col + p.largeur - 1 > disposition.colonnes || p.ligne + p.hauteur - 1 > disposition.lignes) return false
    if (!(p.taille >= TAILLE_BORNES[0] && p.taille <= TAILLE_BORNES[1])) return false
  }
  return chevauchements(disposition).length === 0
}

/** Le style de la scene : ses aires, depuis les donnees. La grille d'origine
 *  garde les colonnes de board.css (300px, auto, auto, 1fr) ; une grille
 *  personnalisee a des cases EGALES, c'est ce qui la rend aimantee. */
export function styleDeGrille(disposition: Disposition): Record<string, string> {
  if (disposition === DISPOSITION_ORIGINE) return { gridTemplateAreas: aireDeGrille(disposition) }
  return {
    gridTemplateAreas: aireDeGrille(disposition),
    gridTemplateColumns: `repeat(${disposition.colonnes}, minmax(0, 1fr))`,
    gridTemplateRows: `repeat(${disposition.lignes}, minmax(0, 1fr))`,
  }
}

// ----------------------------------------------------------------------------
// LA GRILLE AIMANTEE DE L'EDITEUR (etape 2) : 12 colonnes x 8 lignes, cases
// egales. Une disposition personnalisee y vit toujours ; « Disposition
// d'origine » rend la grille de board.css.

export const GRILLE = { colonnes: 12, lignes: 8 }

/**
 * Le plus petit rectangle de chaque zone, en cases de la grille 12 x 8 :
 * assez pour qu'une carte y tienne (la main garde de quoi poser plusieurs
 * cartes, le combat et le heros de quoi aligner un rang). Garde-fou de
 * l'editeur et de la relecture.
 */
export const MINIMUMS: Record<CleZone, { largeur: number; hauteur: number }> = {
  'piles-rencontre': { largeur: 1, hauteur: 2 },
  rencontre: { largeur: 2, hauteur: 2 },
  'complot-principal': { largeur: 2, hauteur: 2 },
  'complots-secondaires': { largeur: 2, hauteur: 2 },
  'terrain-combat': { largeur: 3, hauteur: 2 },
  'terrain-soutien': { largeur: 3, hauteur: 2 },
  'piles-joueur': { largeur: 1, hauteur: 2 },
  annexes: { largeur: 1, hauteur: 1 },
  main: { largeur: 4, hauteur: 2 },
}

/** La disposition d'origine reportee sur la grille 12 x 8 : le point de depart de l'editeur. */
export const DISPOSITION_DE_DEPART: Disposition = {
  ...GRILLE,
  zones: {
    'piles-rencontre': place(1, 1, 2, 2),
    rencontre: place(3, 1, 2, 2),
    'complot-principal': place(5, 1, 3, 2),
    'complots-secondaires': place(8, 1, 5, 2),
    'terrain-combat': place(3, 3, 10, 2),
    'terrain-soutien': place(3, 5, 10, 2),
    'piles-joueur': place(1, 5, 2, 2),
    annexes: place(1, 7, 2, 2),
    main: place(3, 7, 10, 2),
  },
}

const avecZone = (d: Disposition, zone: CleZone, nouvelle: PlaceZone): Disposition => ({
  ...d,
  zones: { ...d.zones, [zone]: nouvelle },
})

const respecteLesMinimums = (d: Disposition) =>
  ZONES.every((z) => d.zones[z].largeur >= MINIMUMS[z].largeur && d.zones[z].hauteur >= MINIMUMS[z].hauteur)

/** La zone posee ailleurs (coin haut-gauche en `col`, `ligne`), ou `undefined` si elle ne tient pas. */
export function deplacer(d: Disposition, zone: CleZone, col: number, ligne: number): Disposition | undefined {
  const suivante = avecZone(d, zone, { ...d.zones[zone], col, ligne })
  return estValide(suivante) ? suivante : undefined
}

/** La zone agrandie ou reduite, sans descendre sous son minimum ni chevaucher. */
export function redimensionner(d: Disposition, zone: CleZone, largeur: number, hauteur: number): Disposition | undefined {
  if (largeur < MINIMUMS[zone].largeur || hauteur < MINIMUMS[zone].hauteur) return undefined
  const suivante = avecZone(d, zone, { ...d.zones[zone], largeur, hauteur })
  return estValide(suivante) ? suivante : undefined
}

/** La taille des cartes de la zone, bornee et arrondie au vingtieme. */
export function changerTaille(d: Disposition, zone: CleZone, taille: number): Disposition {
  const bornee = Math.min(TAILLE_BORNES[1], Math.max(TAILLE_BORNES[0], Math.round(taille * 20) / 20))
  return avecZone(d, zone, { ...d.zones[zone], taille: bornee })
}

// ----------------------------------------------------------------------------
// LE TEXTE COMPACT, partage avec le serveur (`_table_valide`, server_get.py) :
// « 12x8|col,ligne,largeur,hauteur,taille% ; ... », les neuf zones dans
// l'ordre de `ZONES`.

export function ecrireTable(d: Disposition): string {
  const zones = ZONES.map((z) => {
    const p = d.zones[z]
    return `${p.col},${p.ligne},${p.largeur},${p.hauteur},${Math.round(p.taille * 100)}`
  })
  return `${d.colonnes}x${d.lignes}|${zones.join(';')}`
}

/**
 * Relit un texte compact. Tout ce qui ne tient pas (forme, bornes,
 * chevauchement, zone sous son minimum) rend `undefined` : la table REVIENT
 * ALORS A L'ORIGINE, c'est la remise en ordre automatique.
 */
export function lireTable(brut: unknown): Disposition | undefined {
  if (typeof brut !== 'string') return undefined
  const [tete, corps] = brut.split('|')
  if (tete !== `${GRILLE.colonnes}x${GRILLE.lignes}` || corps === undefined) return undefined
  const morceaux = corps.split(';')
  if (morceaux.length !== ZONES.length) return undefined
  const zones = {} as Record<CleZone, PlaceZone>
  for (const [rang, zone] of ZONES.entries()) {
    const nombres = morceaux[rang].split(',')
    if (nombres.length !== 5 || !nombres.every((n) => /^\d+$/.test(n))) return undefined
    const [col, ligne, largeur, hauteur, pourcent] = nombres.map(Number)
    zones[zone] = { col, ligne, largeur, hauteur, taille: pourcent / 100 }
  }
  const d: Disposition = { ...GRILLE, zones }
  return estValide(d) && respecteLesMinimums(d) ? d : undefined
}

/** La cle de preference du compte pour ce nombre de joueurs (1 a 4). */
export function cleTable(nombreDeJoueurs: number): string {
  return `table-${Math.min(4, Math.max(1, Math.round(nombreDeJoueurs) || 1))}`
}

/** Le style d'une zone : la taille de ses cartes, quand elle n'est pas 1. */
export function styleDeZone(disposition: Disposition, cle: string): Record<string, string> {
  const place = (disposition.zones as Record<string, PlaceZone | undefined>)[cle]
  if (!place || place.taille === 1) return {}
  return { '--taille-zone': String(place.taille) }
}
