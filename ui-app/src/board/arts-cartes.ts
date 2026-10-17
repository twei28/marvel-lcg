// Arts alternatifs des CARTES DE DECK (regle de l'utilisateur, 17/10/2026).
//
// Meme carte pour le moteur, seule l'image change. Le choix vit dans la table
// `mc_card_art_v1` { card_id officiel -> code } du navigateur, ecrite par la
// preparation et le deck-builder. Sans choix : l'art de la serie du heros du
// joueur (TMNT pour un heros TMNT), sinon l'officielle.
//
// Miroir de `public/js/prepare/arts-cartes-choix.js` (module pur de la
// preparation) : arts-cartes.test.ts compare les deux. Les tables viennent de
// data/arts_alternatifs.json via tools/generer_arts_cartes.py.
import { ARTS_CARTES, ORIGINES_CARTES, SERIES_ARTS } from './arts-cartes-table'

/** Cle partagee avec la preparation et le deck-builder. */
export const CLE_ARTS_CARTES = 'mc_card_art_v1'

export const STANDARD = 'standard'

export type ChoixArtsCartes = Record<string, string>

let cache: ChoixArtsCartes | undefined

/** Choix par carte, lu une seule fois : la page est rechargee apres un choix. */
export function lireArtsCartes(): ChoixArtsCartes {
  if (cache === undefined) {
    try {
      const brut = window.localStorage.getItem(CLE_ARTS_CARTES)
      cache = brut ? (JSON.parse(brut) as ChoixArtsCartes) : {}
    } catch {
      cache = {}
    }
  }
  return cache
}

/** Pour les tests : oublie la lecture en cache. */
export function oublierArtsCartes(): void {
  cache = undefined
}

function cleHeros(cardId: string): string {
  return cardId.split(',')[0]!.replace(/[a-z]$/, '')
}

/** La serie d'art d'un heros (« tmnt »), d'apres le card_id de sa face. */
export function serieDuHeros(herosCardId: string | undefined): string | null {
  if (!herosCardId) return null
  const cle = cleHeros(String(herosCardId))
  for (const [code, serie] of Object.entries(SERIES_ARTS)) {
    if (serie.heros_cartes.includes(cle)) return code
  }
  return null
}

/**
 * Identifiant d'image d'une carte de deck : « 56013_tmnt » si l'art alternatif
 * s'applique, sinon l'identifiant inchange.
 */
export function picIdCarte(
  picId: string,
  herosCardId: string | undefined,
  choix: ChoixArtsCartes = lireArtsCartes()
): string {
  // Une reimpression identique (`full_link`) prend l'image et le choix de l'officielle.
  const id = ORIGINES_CARTES[picId] ?? picId
  const codes = ARTS_CARTES[id]
  if (!codes || codes.length === 0) return picId
  const voulu = choix[id]
  if (voulu === STANDARD) return picId
  if (voulu && codes.includes(voulu)) return `${id}_${voulu}`
  const serie = serieDuHeros(herosCardId)
  return serie && codes.includes(serie) ? `${id}_${serie}` : picId
}
