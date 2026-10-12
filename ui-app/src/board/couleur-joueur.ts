// LA COULEUR DU JOUEUR dans la phase du méchant (refonte du 12/10/2026,
// décisions 14 à 20 et 57 de .planning/todos/2026-10-12-phase-mechant-schema-et-questions.md).
//
// La couleur vient de l'ASPECT du deck (Q14). Deux joueurs du même aspect :
// même couleur, mais le second porte un motif rayé et son numéro de siège
// (Q15). Plusieurs aspects : pastille partagée (Q16). Basique seul : gris.
// Les moments qui concernent toute la table (menace, bilan, manigance
// complétée) : gris acier (Q20, Q57), pour ne pas se confondre avec le rouge
// de l'Agressivité.
import type { Aspect, Catalogue } from './catalogue'
import type { World, WorldCard, WorldPlayer } from './world'
import type { EtapeDeroule } from './deroule-phase'

/** Les teintes du liseré d'aspect du plateau (board.css, `--lisere-aspect`). */
export const COULEUR_ASPECT: Partial<Record<Aspect, string>> = {
  aggression: '#d1382c',
  justice: '#e6be3c',
  leadership: '#3f86e0',
  protection: '#34ae61',
  pool: '#ef67b0',
  determination: '#965cc4',
  venomized: '#6b6b7a',
}

/** Basique seul (aucun aspect) : gris neutre. */
export const COULEUR_SANS_ASPECT = '#8b8f98'

/** Les moments communs à toute la table. */
export const COULEUR_COMMUNE = '#7f93a6'

export type CadreJoueur = {
  /** Une couleur par aspect, la plus représentée d'abord. */
  couleurs: string[]
  /** Même jeu d'aspects qu'un joueur assis avant lui : motif rayé. */
  raye: boolean
  /** Siège (1 = premier joueur du monde), affiché quand `raye`. */
  siege: number
}

export type CadreDeLEtape = { genre: 'commun' } | ({ genre: 'joueur'; joueur: number } & CadreJoueur)

const ZONES: (keyof WorldPlayer)[] = [
  'area_hero',
  'allies',
  'supports',
  'hand_cards',
  'player_deck',
  'player_discard_pile',
]

/** Les aspects d'un joueur, du plus représenté au moins représenté. */
export function aspectsDuJoueur(joueur: WorldPlayer, catalogue: Catalogue): Aspect[] {
  const compte = new Map<Aspect, number>()
  for (const zone of ZONES) {
    const cartes = joueur[zone]
    if (!Array.isArray(cartes)) continue
    for (const carte of cartes as WorldCard[]) {
      if (!carte?.card_id) continue
      const aspect = catalogue.aspect(carte.card_id)
      if (!aspect || !COULEUR_ASPECT[aspect]) continue
      compte.set(aspect, (compte.get(aspect) ?? 0) + 1)
    }
  }
  return [...compte.entries()].sort((a, b) => b[1] - a[1]).map(([aspect]) => aspect)
}

/** Le cadre de chaque joueur, dans l'ordre de `World.players`. */
export function cadresDesJoueurs(monde: World | undefined, catalogue: Catalogue): CadreJoueur[] {
  const vus = new Set<string>()
  return (monde?.players ?? []).map((joueur, index) => {
    const aspects = aspectsDuJoueur(joueur, catalogue)
    const couleurs = aspects.length > 0 ? aspects.map((a) => COULEUR_ASPECT[a] as string) : [COULEUR_SANS_ASPECT]
    const signature = [...couleurs].sort().join('|')
    const raye = vus.has(signature)
    vus.add(signature)
    return { couleurs, raye, siege: index + 1 }
  })
}

/** Le joueur à qui appartient une carte de la table (identité, allié, sbire engagé…). */
export function joueurDeLaCarte(monde: World | undefined, id: number | undefined): number | undefined {
  if (id === undefined || !monde) return undefined
  const index = (monde.players ?? []).findIndex((joueur) =>
    ZONES.concat(['engaged_enemies']).some((zone) => {
      const cartes = joueur[zone]
      return Array.isArray(cartes) && (cartes as WorldCard[]).some((carte) => carte?.id === id)
    })
  )
  return index === -1 ? undefined : index
}

/**
 * Le cadre d'une étape : commun pour la menace, le bilan et un changement de
 * stade ; sinon le joueur concerné (celui qui révèle, ou celui que l'ennemi
 * vise). Inconnu : commun, plutôt qu'une couleur devinée.
 */
export function cadreDeLEtape(
  etape: EtapeDeroule | undefined,
  cadres: CadreJoueur[],
  joueurDeCarte: (id: number | undefined) => number | undefined
): CadreDeLEtape {
  if (!etape || etape.temps === 'menace' || etape.temps === 'bilan' || etape.temps === 'premier-joueur' || etape.stade) {
    return { genre: 'commun' }
  }
  const joueur =
    etape.joueur ?? joueurDeCarte(etape.cibleAnnonceeId) ?? joueurDeCarte(etape.cibleId) ?? joueurDeCarte(etape.defenseurId)
  const cadre = joueur === undefined ? undefined : cadres[joueur]
  return cadre && joueur !== undefined ? { genre: 'joueur', joueur, ...cadre } : { genre: 'commun' }
}

/** Les variables CSS du bord de la boîte. */
export function styleDuCadre(cadre: CadreDeLEtape): Record<string, string> {
  if (cadre.genre === 'commun') return { '--cadre-joueur': COULEUR_COMMUNE, '--cadre-pastille': COULEUR_COMMUNE }
  const [premiere] = cadre.couleurs
  const n = cadre.couleurs.length
  const pastille =
    n === 1
      ? premiere
      : `conic-gradient(${cadre.couleurs.map((c, i) => `${c} ${(i * 360) / n}deg ${((i + 1) * 360) / n}deg`).join(', ')})`
  return { '--cadre-joueur': premiere, '--cadre-pastille': pastille }
}
