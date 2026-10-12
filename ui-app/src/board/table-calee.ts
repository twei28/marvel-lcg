// LA TABLE CALEE SUR LE RECIT DE LA PHASE DU MECHANT (04/10/2026).
//
// Signale par l'utilisateur : « sur la table il retourne la carte boost ou
// rencontre avant qu'on ait fait suivant ». Cause : le cartouche relache tout
// de suite une trame qui ne lui fabrique aucune etape (`cartoucheAJour`). Or le
// retournement d'un boost ou d'une carte rencontre arrive dans de telles
// trames : l'etape « attaque » n'est completee qu'a la RESOLUTION. Le moteur
// avance donc, et la table, qui dessinait le monde le plus recent, devancait
// le recit.
//
// Choix de l'utilisateur : « table calee sur le recit ». Ce qui n'est pas
// encore raconte n'apparait pas sur la table : on retient, pour chaque etape,
// le monde au moment ou elle a pris sa forme actuelle, et la table dessine
// celui de l'etape affichee.
//
// ⚠ Deux exceptions, voulues :
//  - une QUESTION du moteur au joueur : la table repasse sur le monde reel,
//    les clics doivent viser les cartes telles qu'elles sont ;
//  - hors phase du mechant, ou sans instantane pour l'etape (le bilan) : le
//    monde reel, comme avant.
import type { EtapeDeroule } from './deroule-phase'
import type { World } from './world'

/** Temps des etapes qui font ENTRER une carte en jeu, et de rien d'autre. */
const TITRES_QUI_FONT_ENTRER = new Set(['entree', 'revelation'])

/** Les zones EN JEU du monde (la table), par opposition aux piles et a la main. */
const ZONES_DU_MONDE = ['area_schemes_main', 'area_schemes_side', 'area_villain', 'area_environment'] as const
const ZONES_DU_JOUEUR = ['area_hero', 'allies', 'supports', 'engaged_enemies', 'obligations_area', 'environment_area'] as const

/** La carte `id` est-elle EN JEU, face visible, dans ce monde ? */
export function estEnJeu(monde: World, id: number): boolean {
  const dans = (cartes: unknown) =>
    Array.isArray(cartes) && cartes.some((c) => (c as { id?: number; is_face_up?: boolean }).id === id && (c as { is_face_up?: boolean }).is_face_up)
  const m = monde as unknown as Record<string, unknown> & { players?: Array<Record<string, unknown>> }
  if (ZONES_DU_MONDE.some((zone) => dans(m[zone]))) return true
  return (m.players ?? []).some((joueur) => ZONES_DU_JOUEUR.some((zone) => dans(joueur[zone])))
}

export type Instantane = { signature: string; monde: World }
export type Instantanes = ReadonlyMap<string, Instantane>

/**
 * Le nouvel etat des instantanes apres l'arrivee d'un monde.
 *
 * Une etape garde le monde de la trame ou sa SIGNATURE (son contenu affiche) a
 * change pour la derniere fois. Les trames qui ne la changent pas, comme le
 * retournement d'un boost avant la resolution de l'attaque, ne la touchent pas.
 */
export function majInstantanes(
  precedents: Instantanes,
  etapes: readonly EtapeDeroule[],
  monde: World | undefined,
  phaseEnCours: boolean,
  rafraichirEntrees = false
): Instantanes {
  if (!phaseEnCours || !monde) return precedents.size === 0 ? precedents : new Map()
  let suivants: Map<string, Instantane> | undefined
  for (const etape of etapes) {
    const signature = JSON.stringify(etape)
    const precedent = precedents.get(etape.cle)
    if (precedent?.signature === signature) {
      // REFONTE, LOT 4 (essai) : l'etape qui fait ENTRER une carte prend sa forme
      // AVANT que la carte soit posee (Weapons Runner revele, pas encore engage) :
      // son monde suit tant que la carte n'y est pas en jeu, pour qu'elle arrive
      // sur la table a SON ecran et pas a l'ecran suivant.
      if (
        rafraichirEntrees &&
        TITRES_QUI_FONT_ENTRER.has(etape.titre) &&
        etape.carteId !== undefined &&
        !estEnJeu(precedent.monde, etape.carteId) &&
        estEnJeu(monde, etape.carteId)
      ) {
        suivants ??= new Map(precedents)
        suivants.set(etape.cle, { signature, monde })
      }
      continue
    }
    suivants ??= new Map(precedents)
    suivants.set(etape.cle, { signature, monde })
  }
  return suivants ?? precedents
}

/** Le monde que la table doit dessiner, ou `undefined` pour le monde reel. */
export function mondeDeLaTable(
  instantanes: Instantanes,
  cleAffichee: string | undefined,
  questionAuJoueur: boolean
): World | undefined {
  if (questionAuJoueur || cleAffichee === undefined) return undefined
  return instantanes.get(cleAffichee)?.monde
}

// ---------------------------------------------------------------------------
// REFONTE, LOT 4 (essai, 12/10/2026, decisions 49 a 52) : ce qui n'est pas
// encore raconte n'est pas sur la table, a la carte pres et au chiffre pres.
// ---------------------------------------------------------------------------


/**
 * Les cartes qu'une etape PAS ENCORE AFFICHEE fera entrer en jeu.
 *
 * L'instantane d'une etape est le monde au moment ou elle a pris sa forme
 * finale : l'attaque de Klaw est resolue APRES que son boost ★ a mis Weapons
 * Runner en jeu, si bien que son instantane le montre deja, alors que son
 * entree n'est racontee qu'a l'etape suivante (decision 49).
 */
export function cartesAVenir(etapes: readonly EtapeDeroule[], cleAffichee: string | undefined): Set<number> {
  const ids = new Set<number>()
  if (cleAffichee === undefined) return ids
  const index = etapes.findIndex((etape) => etape.cle === cleAffichee)
  if (index < 0) return ids
  for (const etape of etapes.slice(index + 1)) {
    if (TITRES_QUI_FONT_ENTRER.has(etape.titre) && etape.carteId !== undefined) ids.add(etape.carteId)
  }
  return ids
}

type CarteDuMonde = { id: number; is_face_up: boolean; bind_object_id?: number }

function estCarte(valeur: unknown): valeur is CarteDuMonde {
  return (
    typeof valeur === 'object' &&
    valeur !== null &&
    typeof (valeur as { id?: unknown }).id === 'number' &&
    'is_face_up' in valeur
  )
}

/**
 * Le monde sans les cartes FACE VISIBLE de `ids` (ni ce qui leur est attache).
 *
 * Face visible seulement : une carte rencontre encore distribuee (face cachee)
 * garde sa place pres du joueur jusqu'a sa revelation.
 */
export function sansCartesAVenir(monde: World, ids: ReadonlySet<number>): World {
  if (ids.size === 0) return monde
  const retires = new Set<number>()
  const parcourir = (valeur: unknown): unknown => {
    if (Array.isArray(valeur)) {
      let change = false
      const garde: unknown[] = []
      for (const element of valeur) {
        if (estCarte(element) && element.is_face_up && (ids.has(element.id) || retires.has(element.bind_object_id ?? -1))) {
          retires.add(element.id)
          change = true
          continue
        }
        const suivant = parcourir(element)
        if (suivant !== element) change = true
        garde.push(suivant)
      }
      return change ? garde : valeur
    }
    if (typeof valeur === 'object' && valeur !== null) {
      let copie: Record<string, unknown> | undefined
      for (const [cle, element] of Object.entries(valeur)) {
        const suivant = parcourir(element)
        if (suivant !== element) {
          copie ??= { ...(valeur as Record<string, unknown>) }
          copie[cle] = suivant
        }
      }
      return copie ?? valeur
    }
    return valeur
  }
  return parcourir(monde) as World
}

/**
 * Le monde JUSTE AVANT l'etape affichee : l'instantane de l'etape precedente
 * qui en a un. Sert pendant qu'une attaque retourne encore ses boosts (decision
 * 51) : les PV ne baissent qu'a l'ecran du resultat.
 */
export function mondeAvantEtape(
  instantanes: Instantanes,
  etapes: readonly EtapeDeroule[],
  cleAffichee: string | undefined
): World | undefined {
  if (cleAffichee === undefined) return undefined
  const index = etapes.findIndex((etape) => etape.cle === cleAffichee)
  for (let i = index - 1; i >= 0; i -= 1) {
    const precedent = instantanes.get(etapes[i].cle)
    if (precedent) return precedent.monde
  }
  return undefined
}
