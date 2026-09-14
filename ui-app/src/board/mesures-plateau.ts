// Mesurer le plateau : où est le cadre, où est telle carte.
//
// Le seul endroit qui interroge le DOM pour la phase jouée sur la table. Les
// deux modules qui s'en servent (`phase-sur-table.ts` pour le cartouche,
// `trait-phase.ts` pour le trait) ne font que de l'arithmétique sur les
// rectangles rendus ici, et se testent donc sans navigateur.
//
// ⚠ TOUT EST DANS LE REPÈRE DU CADRE, pas dans celui de la fenêtre. Le plateau
// est centré et mis à l'échelle (`--echelle`) sous une barre d'outils : des
// coordonnées de fenêtre poseraient le cartouche et le trait décalés de toute
// cette hauteur.

export type Boite = { x: number; y: number; w: number; h: number }

/** Le cadre du plateau, ou `undefined` s'il n'est pas mesurable. */
export function cadreDuPlateau(): { element: HTMLElement; origine: DOMRect; boite: Boite } | undefined {
  const element = document.querySelector<HTMLElement>('.plateau-cadre')
  if (!element) return undefined
  const origine = element.getBoundingClientRect()
  // ⚠ jsdom ne calcule aucune géométrie : tous les rectangles y valent 0. Un
  // cadre de taille nulle ne peut rien ancrer, et les appelants le savent.
  if (origine.width === 0 || origine.height === 0) return undefined
  return { element, origine, boite: { x: 0, y: 0, w: origine.width, h: origine.height } }
}

/**
 * Le rectangle d'une carte du monde, par son identifiant d'objet.
 *
 * ⚠ `data-card-id` PORTE L'IDENTIFIANT DU MONDE, pas le code de la carte : deux
 * exemplaires de la même carte ont le même `card_id` de catalogue mais deux
 * identifiants distincts. C'est la même clé que `CoucheAnimations` interroge
 * pour faire voler les cartes, et c'est voulu : une seule convention.
 *
 * Rend `undefined` quand la carte n'est plus sur la table (un sbire tué pendant
 * la phase a disparu de l'index du monde). L'appelant décide alors quoi faire ;
 * il n'y a rien à inventer ici.
 */
export function boiteDeCarte(
  id: number | undefined,
  cadre: { element: HTMLElement; origine: DOMRect }
): Boite | undefined {
  if (id === undefined) return undefined
  const el = cadre.element.querySelector<HTMLElement>(`.scan-card[data-card-id="${id}"]`)
  if (!el) return undefined
  const r = el.getBoundingClientRect()
  if (r.width === 0 || r.height === 0) return undefined
  return {
    x: r.left - cadre.origine.left,
    y: r.top - cadre.origine.top,
    w: r.width,
    h: r.height,
  }
}

/**
 * Le rectangle du DECK RENCONTRE sur la table.
 *
 * C'est l'ancre des deux gestes du mode « Sur la table » qui parlent du paquet :
 * les cartes boost qui en sortent pour se poser à côté, et la carte rencontre
 * qu'on agrandit juste à côté de lui. L'utilisateur l'a demandé ainsi le
 * 14/09/2026, parmi trois emplacements : « on voit d'où elle vient ».
 *
 * ⚠ LA PREMIÈRE CARTE DE LA ZONE, PAS UN IDENTIFIANT. Un deck n'est pas une
 * carte du monde : il est dessiné comme une pile, et son représentant change à
 * chaque pioche. La zone, elle, ne bouge pas.
 */
export function boiteDuDeckRencontre(cadre: {
  element: HTMLElement
  origine: DOMRect
}): Boite | undefined {
  const el = cadre.element.querySelector<HTMLElement>('.zone-piles-rencontre .scan-card')
  if (!el) return undefined
  const r = el.getBoundingClientRect()
  if (r.width === 0) return undefined
  return {
    x: r.left - cadre.origine.left,
    y: r.top - cadre.origine.top,
    w: r.width,
    h: r.height,
  }
}
