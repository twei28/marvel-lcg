// LES FLÈCHES DE LA PHASE DU MÉCHANT (refonte, lot 3, essai, 12/10/2026).
//
// Décisions 21 à 25, 39 et 40 de
// .planning/todos/2026-10-12-phase-mechant-schema-et-questions.md : une flèche
// courbe relie la source à sa cible, dans la couleur du joueur visé (gris acier
// pour ce qui touche toute la table). Attaque : table → table. Carte qui arrive
// (boost ★ qui entre en jeu, carte révélée) : boîte → sa place sur la table.
// Menace : boîte → manigance. Riposte : un coup du héros sur le sbire, donc une
// flèche dans l'autre sens, sans règle à part. Un défenseur qui n'est pas la
// carte touchée (Overkill, défenseur parti) : deux flèches.
//
// ⚠ CE MODULE NE MESURE RIEN. Il dit quelles flèches l'étape appelle ; le
// composant (`FlechesPhase.tsx`) écarte celles dont un bout n'est pas à l'écran
// (un boost ★ qui n'est pas entré en jeu n'a pas de place sur la table).
import { COULEUR_COMMUNE, type CadreJoueur } from './couleur-joueur'
import type { EtapeDeroule } from './deroule-phase'

/** Un bout de flèche : une carte de la table, une carte de la boîte, ou le corps de la boîte. */
export type BoutFleche =
  | { lieu: 'table'; id: number }
  | { lieu: 'boite'; id: number }
  | { lieu: 'boite-corps' }

export type FlecheSpec = {
  cle: string
  de: BoutFleche
  vers: { lieu: 'table'; id: number }
  couleur: string
}

export type ContexteFleches = {
  cadres: CadreJoueur[]
  joueurDeCarte: (id: number | undefined) => number | undefined
  /** Boosts déjà retournés : un boost encore caché n'a pas de flèche. */
  boostsMontres?: number
}

function couleurDuJoueurDe(id: number | undefined, ctx: ContexteFleches): string {
  const joueur = ctx.joueurDeCarte(id)
  return (joueur === undefined ? undefined : ctx.cadres[joueur]?.couleurs[0]) ?? COULEUR_COMMUNE
}

function cleDe(bout: BoutFleche): string {
  return bout.lieu === 'boite-corps' ? 'corps' : `${bout.lieu}-${bout.id}`
}

export function flechesDeLEtape(etape: EtapeDeroule | undefined, ctx: ContexteFleches): FlecheSpec[] {
  if (!etape || etape.etat === 'annule' || etape.temps === 'bilan') return []
  const fleches: FlecheSpec[] = []
  const ajouter = (de: BoutFleche, versId: number | undefined, couleur: string) => {
    if (versId === undefined) return
    if (de.lieu !== 'boite-corps' && de.lieu === 'table' && de.id === versId) return
    const cle = `${cleDe(de)}>${versId}`
    if (fleches.some((f) => f.cle === cle)) return
    fleches.push({ cle, de, vers: { lieu: 'table', id: versId }, couleur })
  }

  // Étape 1 : la menace part de la boîte (le calcul posé) vers la manigance.
  if (etape.temps === 'menace') {
    ajouter({ lieu: 'boite-corps' }, etape.cibleId, COULEUR_COMMUNE)
    return fleches
  }

  const cible = etape.cibleId ?? etape.cibleAnnonceeId
  const estRevelation = etape.temps === 'revelation'

  // Une activation, ou un coup porté par une carte de la table (Riposte).
  if (!estRevelation && etape.carteId !== undefined && cible !== undefined) {
    if (etape.titre === 'manigance') {
      ajouter({ lieu: 'table', id: etape.carteId }, cible, COULEUR_COMMUNE)
    } else if (etape.defenseurId !== undefined && etape.defenseurId !== cible) {
      // Le défenseur n'est pas la carte touchée : Overkill, ou défenseur parti.
      ajouter({ lieu: 'table', id: etape.carteId }, etape.defenseurId, couleurDuJoueurDe(etape.defenseurId, ctx))
      ajouter({ lieu: 'table', id: etape.defenseurId }, cible, couleurDuJoueurDe(cible, ctx))
    } else {
      ajouter({ lieu: 'table', id: etape.carteId }, cible, couleurDuJoueurDe(cible, ctx))
    }
  }

  // Les boosts ★ déjà retournés : s'ils sont entrés en jeu, de la boîte à leur place.
  const montres = ctx.boostsMontres ?? etape.boosts.length
  for (const boost of etape.boosts.slice(0, montres)) {
    if (boost.etoile) ajouter({ lieu: 'boite', id: boost.cibleId }, boost.cibleId, couleurDuJoueurDe(boost.cibleId, ctx))
  }

  // Un sbire qui entre en jeu en pleine phase (souvent un boost ★) : de la boîte à sa place.
  if (etape.titre === 'entree' && etape.carteId !== undefined) {
    ajouter({ lieu: 'boite', id: etape.carteId }, etape.carteId, couleurDuJoueurDe(etape.carteId, ctx))
  }

  // La carte révélée, vers l'endroit où elle s'installe (rien pour une traîtrise).
  if (estRevelation && etape.carteId !== undefined) {
    ajouter({ lieu: 'boite', id: etape.carteId }, etape.carteId, couleurDuJoueurDe(etape.carteId, ctx))
  }

  // Ce que la carte a fait sur la table.
  const source: BoutFleche = etape.carteId !== undefined && estRevelation ? { lieu: 'boite', id: etape.carteId } : { lieu: 'boite-corps' }
  for (const effet of etape.effets ?? []) {
    if (effet.genre === 'entree') {
      const proprietaire = effet.engage_avec_id ?? effet.carte_id
      const couleur = effet.type === 'sbire' ? couleurDuJoueurDe(proprietaire, ctx) : COULEUR_COMMUNE
      ajouter({ lieu: 'boite', id: effet.carte_id }, effet.carte_id, couleur)
    } else if (effet.genre === 'menace') {
      ajouter(source, effet.cible_id, COULEUR_COMMUNE)
    } else if (effet.genre === 'degats') {
      ajouter(source, effet.cible_id, couleurDuJoueurDe(effet.cible_id, ctx))
    }
  }
  return fleches
}

export type Rect = { x: number; y: number; w: number; h: number }
export type Point = { x: number; y: number }

/** Le point du bord de `r` sur le segment qui va de son centre vers `vers`. */
export function bordVers(r: Rect, vers: Point): Point {
  const cx = r.x + r.w / 2
  const cy = r.y + r.h / 2
  const dx = vers.x - cx
  const dy = vers.y - cy
  if (dx === 0 && dy === 0) return { x: cx, y: cy }
  const tx = dx === 0 ? Infinity : r.w / 2 / Math.abs(dx)
  const ty = dy === 0 ? Infinity : r.h / 2 / Math.abs(dy)
  const k = Math.min(tx, ty, 1)
  return { x: cx + dx * k, y: cy + dy * k }
}

export type TraceFleche = { d: string; pointe: string; longueur: number; depart: Point; arrivee: Point }

/** La courbe d'un rectangle à l'autre : du bord de la source au bord de la cible, bombée vers le haut. */
export function traceEntre(de: Rect, vers: Rect): TraceFleche {
  const cDe = { x: de.x + de.w / 2, y: de.y + de.h / 2 }
  const cVers = { x: vers.x + vers.w / 2, y: vers.y + vers.h / 2 }
  const depart = bordVers(de, cVers)
  const arrivee = bordVers(vers, cDe)
  const dx = arrivee.x - depart.x
  const dy = arrivee.y - depart.y
  const longueurDroite = Math.hypot(dx, dy) || 1
  const bombe = Math.min(90, longueurDroite * 0.22)
  // La normale qui pointe vers le haut de l'écran : la courbe passe au-dessus.
  let nx = -dy / longueurDroite
  let ny = dx / longueurDroite
  if (ny > 0) {
    nx = -nx
    ny = -ny
  }
  const mx = (depart.x + arrivee.x) / 2 + nx * bombe
  const my = (depart.y + arrivee.y) / 2 + ny * bombe
  const longueur = Math.hypot(mx - depart.x, my - depart.y) + Math.hypot(arrivee.x - mx, arrivee.y - my)
  const angle = Math.atan2(arrivee.y - my, arrivee.x - mx)
  const s = 14
  const p1 = { x: arrivee.x - s * Math.cos(angle - 0.45), y: arrivee.y - s * Math.sin(angle - 0.45) }
  const p2 = { x: arrivee.x - s * Math.cos(angle + 0.45), y: arrivee.y - s * Math.sin(angle + 0.45) }
  const r = (n: number) => Math.round(n * 10) / 10
  return {
    d: `M${r(depart.x)},${r(depart.y)} Q${r(mx)},${r(my)} ${r(arrivee.x)},${r(arrivee.y)}`,
    pointe: `M${r(arrivee.x)},${r(arrivee.y)} L${r(p1.x)},${r(p1.y)} L${r(p2.x)},${r(p2.y)} Z`,
    longueur: Math.ceil(longueur),
    depart,
    arrivee,
  }
}
