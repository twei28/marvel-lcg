// Témoin d'affichage des piles du joueur (rapport de bug n°48, 04/10/2026).
//
// Un joueur a signalé que son deck n'était pas dessiné alors que le survol en
// donnait le nombre de cartes. Les données du rapport étaient saines
// (`construirePlateau` produisait bien la pile) : le défaut est donc entre le
// descripteur et l'écran, et un rapport texte ne le montre pas. Cette sonde lit
// ce que le NAVIGATEUR a réellement posé pour chaque pile du joueur, et le
// rapport l'écrit, pour que le prochain cas dise où la pile disparaît.

/** Les piles qu'on regarde : le deck et la défausse du héros. */
const PILES = ['joueur-deck', 'joueur-defausse'] as const

/** Sous ce seuil, une pile est considérée comme invisible. */
const OPACITE_MINI = 0.05

type Constat = {
  pile: string
  /** Présente dans le DOM ? */
  presente: boolean
  largeur: number
  hauteur: number
  /** `visibility`, `display` et `opacity` CALCULÉS sur la pile. */
  visibilite: string
  affichage: string
  opacite: number
  /** Le premier ancêtre qui masque la pile, s'il y en a un. */
  masquePar?: string
  /** Le cadre de la carte et son image : dessinés, chargés ? */
  cadre: 'absent' | 'present'
  /** Classe `retourne-*` posée sur le cadre : animation de retournement en
   *  cours, ou BLOQUÉE (cause du n°48 : le cadre reste de chant, invisible). */
  retournement?: string
  image: 'absente' | 'chargee' | 'en-erreur' | 'en-cours'
}

/** `opacity` calculée ; vide (hors navigateur réel) = opaque. */
function opaciteDe(style: CSSStyleDeclaration): number {
  const valeur = parseFloat(style.opacity)
  return Number.isNaN(valeur) ? 1 : valeur
}

function decrire(el: Element): string {
  const classes = typeof el.className === 'string' ? el.className.trim().split(/\s+/).slice(0, 3).join('.') : ''
  return `${el.tagName.toLowerCase()}${classes ? '.' + classes : ''}`
}

/** Le premier élément, en remontant, qui rend la pile invisible. */
function ancetreMasquant(depart: Element): string | undefined {
  for (let el: Element | null = depart; el; el = el.parentElement) {
    const style = getComputedStyle(el)
    if (style.display === 'none') return `${decrire(el)} display:none`
    if (style.visibility === 'hidden') return `${decrire(el)} visibility:hidden`
    if (opaciteDe(style) < OPACITE_MINI) return `${decrire(el)} opacity:${style.opacity}`
  }
  return undefined
}

function constater(racine: ParentNode, pile: string): Constat {
  const unite = racine.querySelector(`[data-pile="${pile}"]`)
  if (!unite) {
    return {
      pile, presente: false, largeur: 0, hauteur: 0, visibilite: '-', affichage: '-',
      opacite: 0, cadre: 'absent', image: 'absente',
    }
  }
  const boite = unite.getBoundingClientRect()
  const style = getComputedStyle(unite)
  const img = unite.querySelector('img')
  return {
    pile,
    presente: true,
    largeur: Math.round(boite.width),
    hauteur: Math.round(boite.height),
    visibilite: style.visibility,
    affichage: style.display,
    opacite: opaciteDe(style),
    masquePar: ancetreMasquant(unite),
    cadre: unite.querySelector('.scan-frame') ? 'present' : 'absent',
    retournement: /\bretourne-\w+/.exec(unite.querySelector('.scan-frame')?.className ?? '')?.[0],
    image: !img
      ? 'absente'
      : (img as HTMLElement).dataset.missing === 'true'
        ? 'en-erreur'
        : img.complete && img.naturalWidth > 0
          ? 'chargee'
          : 'en-cours',
  }
}

/** Une pile vue par le moteur comme non vide mais invisible à l'écran. */
function anomalie(c: Constat, cartesDansLaPile: number): boolean {
  if (cartesDansLaPile === 0) return false
  return !c.presente || c.largeur < 4 || c.hauteur < 4 || c.cadre === 'absent' || c.masquePar !== undefined ||
    c.retournement !== undefined
}

/**
 * Une ligne par pile du joueur, prête pour le rapport. `compte` donne le nombre
 * de cartes que le MOTEUR met dans chaque pile (`player_deck`, ...).
 *
 * Retourne `[]` hors navigateur, pour que le module reste testable sans DOM.
 */
export function sonderPilesDuJoueur(
  compte: { deck: number; defausse: number },
  racine: ParentNode | undefined = typeof document === 'undefined' ? undefined : document
): string[] {
  if (!racine) return []
  return PILES.map((pile) => {
    const attendu = pile === 'joueur-deck' ? compte.deck : compte.defausse
    const c = constater(racine, pile)
    const etat = anomalie(c, attendu) ? 'ANOMALIE ' : ''
    const detail = c.presente
      ? `boîte ${c.largeur}x${c.hauteur}, display ${c.affichage}, visibility ${c.visibilite}, opacity ${c.opacite}, ` +
        `cadre ${c.cadre}${c.retournement ? ` (${c.retournement})` : ''}, image ${c.image}${c.masquePar ? `, masquée par ${c.masquePar}` : ''}`
      : 'absente du DOM'
    return `${etat}${pile} : ${attendu} carte(s) côté moteur ; ${detail}`
  })
}
