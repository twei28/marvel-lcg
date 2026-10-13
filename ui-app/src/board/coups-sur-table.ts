// LES COUPS QUI ARRIVENT SUR LA TABLE (essai, 13/10/2026).
//
// Demandes de l'utilisateur, dans l'ordre : a l'ecran « Menace », la manigance
// reste a son niveau d'AVANT ; un jeton part du debut du trait et ne vole vers
// la carte qu'au clic sur Continuer, ou le compteur change a son arrivee.
// Puis : les manigances du mechant et des sbires, les attaques (et la Riposte),
// et tout ce qu'une carte revelee fait a une carte de la table.
//
// Partie PURE : ce que l'ecran dit (ses coups), le monde dont les compteurs
// touches sont figes, et la courbe du vol. Le mouvement est dans
// `JetonsMenace.tsx`.
import type { EtapeDeroule } from './deroule-phase'
import type { BoutFleche, Point } from './fleches-phase'
import type { World } from './world'

export type GenreCoup = 'menace' | 'degats' | 'acceleration'

/**
 * Un coup de l'ecran : `montant` jetons de `genre` partent de `depuis` vers la
 * carte `cibleId`, dont le compteur valait `avant`. `montant` a 0 : rien ne
 * vole, la carte est seulement figee a `avant` (la Riposte, sur l'ecran de
 * l'attaque qu'elle suit : son ecran a elle vient ensuite).
 */
export type Coup = { genre: GenreCoup; cibleId: number; avant: number; montant: number; depuis: BoutFleche }

const CORPS: BoutFleche = { lieu: 'boite-corps' }

/** Le champ du monde qui porte le compteur : menace sur la carte, PV restants. */
export const CHAMP: Record<GenreCoup, 'k_threat' | 'health' | 'k_acceleration_token'> = {
  menace: 'k_threat',
  degats: 'health',
  acceleration: 'k_acceleration_token',
}

/** Le compteur avant le coup, a partir de celui d'apres. */
function avantDe(genre: GenreCoup, restant: number, montant: number): number {
  return genre === 'degats' ? restant + montant : Math.max(0, restant - montant)
}

function coup(genre: GenreCoup, cibleId: number | undefined, montant: number | undefined, restant: number | null | undefined, depuis: BoutFleche, avant?: number): Coup | undefined {
  if (cibleId === undefined || montant === undefined || montant <= 0 || restant === undefined || restant === null) return undefined
  return { genre, cibleId, avant: avant ?? avantDe(genre, restant, montant), montant, depuis }
}

/** Les coups que cet ecran raconte, quand ils se chiffrent. Une annonce n'en a aucun. */
export function coupsDeLEtape(etape: EtapeDeroule | undefined): Coup[] {
  if (!etape || etape.etat === 'annule' || etape.etat === 'annonce') return []
  const coups: Array<Coup | undefined> = []
  const { titre, temps, carteId, cibleId, montant, restant } = etape
  if (temps === 'menace') {
    coups.push(coup('menace', cibleId, montant, restant, CORPS))
  } else if (titre === 'manigance') {
    // Le mechant est colle a la manigance sur la table : son trait part de la boite.
    const depuis: BoutFleche = temps === 'sbires' && carteId !== undefined ? { lieu: 'table', id: carteId } : CORPS
    coups.push(coup('menace', cibleId, montant, restant, depuis, etape.menaceAvant))
  } else if (titre === 'attaque' && carteId !== undefined) {
    // Comme le trait : le defenseur qui n'est pas la carte touchee frappe en second.
    const de = etape.defenseurId !== undefined && etape.defenseurId !== cibleId ? etape.defenseurId : carteId
    coups.push(coup('degats', cibleId, montant, restant, { lieu: 'table', id: de }))
    const riposte = etape.riposte
    if (riposte && typeof riposte.restant === 'number' && riposte.degats > 0) {
      coups.push({ genre: 'degats', cibleId: carteId, avant: riposte.restant + riposte.degats, montant: 0, depuis: CORPS })
    }
  } else if (titre === 'paquet-vide') {
    // 13/10/2026 (encadré ②) : le jeton d'accélération vole de la boîte à la manigance.
    coups.push(coup('acceleration', cibleId, montant, restant, CORPS))
  } else if (titre === 'riposte' && carteId !== undefined) {
    coups.push(coup('degats', cibleId, montant, restant, { lieu: 'table', id: carteId }))
  }
  if (temps === 'revelation' || titre === 'entree' || titre === 'stade-revele') {
    const depuis: BoutFleche = temps === 'revelation' && carteId !== undefined ? { lieu: 'boite', id: carteId } : CORPS
    for (const effet of etape.effets ?? []) {
      if (effet.genre === 'menace') coups.push(coup('menace', effet.cible_id, effet.montant, effet.restant, depuis))
      else if (effet.genre === 'degats') coups.push(coup('degats', effet.cible_id, effet.montant, effet.restant, depuis))
    }
  }
  // Deux coups sur la meme carte : le compteur d'avant est celui du PREMIER.
  const resultat: Coup[] = []
  for (const c of coups) {
    if (!c) continue
    const cle = `${c.genre}:${c.cibleId}`
    const deja = resultat.find((r) => `${r.genre}:${r.cibleId}` === cle)
    if (deja) {
      deja.montant += c.montant
      continue
    }
    resultat.push({ ...c })
  }
  return resultat
}

/** Le point de la courbe quadratique `depart` > `controle` > `arrivee` a l'instant t (0 a 1). */
export function pointDeLaCourbe(depart: Point, controle: Point, arrivee: Point, t: number): Point {
  const u = 1 - t
  return {
    x: u * u * depart.x + 2 * u * t * controle.x + t * t * arrivee.x,
    y: u * u * depart.y + 2 * u * t * controle.y + t * t * arrivee.y,
  }
}

/** Ce que la table doit afficher a la place du monde : une valeur par carte et par compteur. */
export type Fige = { genre: GenreCoup; cibleId: number; valeur: number }

/**
 * Le monde ou chaque carte de `figes` montre la valeur donnee. Copie ce qui
 * change, ou que soit la carte (zones du mechant, des joueurs) ; rend le meme
 * objet si rien ne change.
 */
export function avecCompteursFiges(monde: World, figes: readonly Fige[]): World {
  if (figes.length === 0) return monde
  const parId = new Map<number, Fige[]>()
  for (const f of figes) parId.set(f.cibleId, [...(parId.get(f.cibleId) ?? []), f])
  const parcourir = (valeur: unknown): unknown => {
    if (Array.isArray(valeur)) {
      let copie: unknown[] | undefined
      valeur.forEach((element, i) => {
        const suivant = parcourir(element)
        if (suivant !== element) {
          copie ??= [...valeur]
          copie[i] = suivant
        }
      })
      return copie ?? valeur
    }
    if (typeof valeur !== 'object' || valeur === null) return valeur
    const objet = valeur as Record<string, unknown>
    const id = objet.id
    const aFiger = typeof id === 'number' && typeof objet.info === 'object' && objet.info !== null ? parId.get(id) : undefined
    let copie: Record<string, unknown> | undefined
    if (aFiger) {
      const info = { ...(objet.info as Record<string, unknown>) }
      for (const f of aFiger) info[CHAMP[f.genre]] = f.valeur
      copie = { ...objet, info }
    }
    for (const [cle, element] of Object.entries(objet)) {
      if (cle === 'info') continue
      const suivant = parcourir(element)
      if (suivant !== element) {
        copie ??= { ...objet }
        copie[cle] = suivant
      }
    }
    return copie ?? valeur
  }
  return parcourir(monde) as World
}
