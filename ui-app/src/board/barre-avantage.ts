// LA BARRE D'AVANTAGE : l'ESTIMATION (22/10/2026, backlog n°3, docs/BACKLOG.md).
//
// ⚠ C'EST UNE ESTIMATION, PAS UNE PROBABILITE DE VICTOIRE. Jeu cooperatif, decks caches, hasard : on ne peut pas
// calculer qui gagne. On mesure seulement la COURSE entre deux choses lisibles dans l'etat du jeu :
//   - combien de tours avant que la manigance principale n'atteigne son seuil (defaite) ;
//   - combien de PV il reste au mechant (victoire), et ce qu'il reste aux heros.
// Fonction PURE (ni DOM ni stockage) : testee par barre-avantage.test.ts.
//
// Valable quand le scenario a une manigance principale avec un seuil. Sinon : « indisponible », jamais un chiffre
// invente. Les scenarios atypiques auront des fiches reglage plus tard (rien d'ecrit pour l'instant).
import type { World, WorldCard } from './world'

export type Avantage =
  | { etat: 'masque' }
  | { etat: 'indisponible' }
  | {
      etat: 'ok'
      /** 0 = le mechant va gagner, 1 = les heros dominent. */
      valeur: number
      /** Tours estimes avant la defaite, ou null. */
      tours: number | null
      /** PV restants du mechant, en %, ou null (PV infinis ou inconnus). */
      mechantPct: number | null
      /** PV restants des heros, en %, ou null. */
      herosPct: number | null
      /** Sbires engages contre les heros. */
      sbires: number
    }

/** Au-dela de ce nombre de tours avant la defaite, la menace est « confortable ». */
const TOURS_CONFORTABLES = 12
const POIDS = { tours: 0.4, mechant: 0.35, heros: 0.25 }
const PENALITE_PAR_SBIRE = 0.03
const PENALITE_MAX = 0.15

const borne = (x: number) => Math.max(0, Math.min(1, x))
const nombre = (x: unknown): number | undefined => (typeof x === 'number' && Number.isFinite(x) ? x : undefined)

function fractionDePv(carte: WorldCard | undefined): number | null {
  if (!carte || carte.info.is_infinite_health) return null
  const max = nombre(carte.info.max_health)
  const pv = nombre(carte.info.health)
  if (max === undefined || max <= 0 || pv === undefined) return null
  return borne(pv / max)
}

/** La menace ajoutee a chaque tour : celle du dernier fait de menace, sinon une escalade minimale (1 par joueur). */
function menaceParTour(monde: World, joueurs: number): number {
  const faits = monde.faits_mechant ?? []
  for (let i = faits.length - 1; i >= 0; i--) {
    const fait = faits[i]
    if (fait.genre === 'menace' && fait.montant > 0) return fait.montant
  }
  return Math.max(1, joueurs)
}

export function estimerAvantage(monde: World | undefined): Avantage {
  // Hors des cas ou « heros contre mechant » a un sens : pas de barre du tout.
  if (!monde || monde.game_over || monde.manuel_actif || (monde.teams && monde.teams.length > 0)) {
    return { etat: 'masque' }
  }
  const manigance = (monde.area_schemes_main ?? []).find(
    (c) => c.is_face_up && nombre(c.info.target_threat) !== undefined && nombre(c.info.target_threat)! > 0
  )
  if (!manigance) return { etat: 'indisponible' }

  const seuil = nombre(manigance.info.target_threat)!
  const menace = nombre(manigance.info.k_threat) ?? 0
  const joueurs = monde.players.filter((p) => !p.is_eliminated).length || 1
  const parTour = menaceParTour(monde, joueurs)
  const tours = menace >= seuil ? 0 : Math.floor((seuil - menace) / parTour)

  const mechant = (monde.area_villain ?? []).find((c) => c.is_face_up && nombre(c.info.max_health) !== undefined)
  const fMechant = fractionDePv(mechant)

  const fractionsHeros = monde.players
    .filter((p) => !p.is_eliminated)
    .map((p) => fractionDePv(p.area_hero[0]))
    .filter((f): f is number => f !== null)
  const fHeros = fractionsHeros.length ? fractionsHeros.reduce((a, b) => a + b, 0) / fractionsHeros.length : null

  const sbires = monde.players.reduce((n, p) => n + (p.engaged_enemies?.length ?? 0), 0)

  let somme = POIDS.tours * borne(tours / TOURS_CONFORTABLES)
  let poids = POIDS.tours
  if (fMechant !== null) {
    somme += POIDS.mechant * (1 - fMechant)
    poids += POIDS.mechant
  }
  if (fHeros !== null) {
    somme += POIDS.heros * fHeros
    poids += POIDS.heros
  }
  const valeur = borne(somme / poids - Math.min(PENALITE_MAX, sbires * PENALITE_PAR_SBIRE))

  return {
    etat: 'ok',
    valeur,
    tours,
    mechantPct: fMechant === null ? null : Math.round(fMechant * 100),
    herosPct: fHeros === null ? null : Math.round(fHeros * 100),
    sbires,
  }
}
