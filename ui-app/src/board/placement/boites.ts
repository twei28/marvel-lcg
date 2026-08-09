// Mesures d'écran : où sont les cartes, où sont les panneaux.
//
// Tout ce qui touche au DOM pour le placement passe par ici. Le calcul de
// position, lui, est purement géométrique et vit dans placer.ts — c'est ce
// découpage qui le rend testable sans navigateur.
//
// Le repère est celui de `getBoundingClientRect` : viewport, origine en haut à
// gauche. Les panneaux sont en `position: fixed`, donc dans le même repère —
// aucune conversion nécessaire, y compris quand la table est mise à l'échelle
// (le `scale` de .plateau-scene est déjà pris en compte par le rect).

export type Boite = { x: number; y: number; w: number; h: number }

export function boiteDe(el: Element): Boite {
  const r = el.getBoundingClientRect()
  return { x: r.left, y: r.top, w: r.width, h: r.height }
}

/** Une boîte sans surface ne cache rien : elle ne doit pas peser dans le calcul. */
const aUneSurface = (b: Boite): boolean => b.w > 0 && b.h > 0

/**
 * Rectangles des cartes désignées, repérées par l'identifiant que chaque carte
 * porte déjà dans le DOM.
 *
 * On vise `[data-card-id]` SANS le préfixe `.scan-card`, et c'est délibéré : le
 * plateau a deux rendus. Sur PC une carte est une `.scan-card`, mais en mode
 * mobile c'est un `.medaillon` — même attribut, même espace d'identifiants,
 * balise différente. Le sélecteur restreint ne trouvait donc RIEN sur mobile, et
 * les panneaux y retombaient silencieusement sur leur position par défaut, celle
 * qu'on cherche justement à corriger. `CoucheTriche` visait déjà large, à raison.
 *
 * Un identifiant introuvable est simplement ignoré — une cible peut être hors
 * table (dans un deck, une défausse), et ce n'est pas une anomalie.
 */
export function boitesDesCartes(
  ids: Iterable<number>,
  racine: ParentNode = document
): Boite[] {
  const sorties: Boite[] = []
  for (const id of new Set(ids)) {
    // 0 est la valeur « aucune carte » de bind_id : elle ne désigne rien.
    if (!id) continue
    for (const el of racine.querySelectorAll(`[data-card-id="${id}"]`)) {
      const boite = boiteDe(el)
      if (aUneSurface(boite)) sorties.push(boite)
    }
  }
  return sorties
}

/**
 * Rectangles des panneaux déjà posés qu'il faut contourner.
 *
 * On interroge le DOM plutôt que de tenir un registre entre composants : les
 * panneaux à éviter sont toujours affichés AVANT celui qui les évite (on ne
 * survole une carte qu'une fois la décision ouverte), donc ils sont là quand on
 * mesure. Pas d'ordre de montage à orchestrer, pas d'état partagé à nettoyer.
 */
export function boitesDesPanneaux(
  selecteurs: Iterable<string>,
  sauf?: Element | null,
  racine: ParentNode = document
): Boite[] {
  const sorties: Boite[] = []
  for (const selecteur of selecteurs) {
    for (const el of racine.querySelectorAll(selecteur)) {
      if (el === sauf || (sauf && el.contains(sauf))) continue
      const boite = boiteDe(el)
      if (aUneSurface(boite)) sorties.push(boite)
    }
  }
  return sorties
}
