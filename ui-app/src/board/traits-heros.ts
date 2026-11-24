// LES TRAITS D'UN HEROS, CE QU'IL A EN CE MOMENT (idee de Lilipulse, 28/10/2026) : « je joue Rocket, il gagne Aerien, mais
// toutes les cartes sont entassees : je ne sais plus si j'ai le trait ». Le moteur envoie deja les traits COURANTS dans
// `WorldCard.traits` (cles `t_AERIAL`, voir `GetInfoTraits`, trait.py) ; le catalogue donne les traits IMPRIMES. La difference
// des deux, c'est ce qui a change : gagne (Jet Boots) ou perdu (« loses the X trait »).
import { TRAITS_FR } from './traits-fr'

export type EtatTrait = 'imprime' | 'gagne' | 'perdu'

export type PastilleTrait = {
  /** Cle normalisee (« AERIAL », « WEB-WARRIOR »), stable d'un affichage a l'autre. */
  cle: string
  /** Le libelle affiche, dans la langue du jeu. */
  texte: string
  etat: EtatTrait
}

/** Les trois reglages : tous les traits, seulement ceux qui changent, ou rien. */
export type ModeTraits = 'tous' | 'changements' | 'aucun'

/**
 * Meme forme pour les deux sources. Le moteur ecrit `t_` + le trait avec les espaces en soulignes et sans « ! »
 * (`GetInfoTraits`) ; le catalogue, lui, garde le trait tel qu'imprime.
 */
export function normaliserTrait(trait: string): string {
  const sansPrefixe = trait.startsWith('t_') ? trait.slice(2) : trait
  return sansPrefixe.replace(/!/g, '').replace(/_/g, ' ').replace(/\s+/g, ' ').trim().toUpperCase()
}

function libelle(cle: string, langue: 'fr' | 'en'): string {
  return langue === 'fr' ? (TRAITS_FR[cle] ?? cle) : cle
}

/**
 * Les pastilles d'une carte : imprimes d'abord (dans l'ordre du scan), puis les gagnes, puis les perdus.
 *
 * `actuels` = les cles du descripteur (`t_AERIAL`...). Rendu vide quand le moteur ne dit rien (`undefined`) : une carte dont on
 * ne connait pas les traits courants ne doit pas passer pour « les avoir tous perdus ».
 */
export function pastillesDeTraits(
  imprimes: readonly string[] | undefined,
  actuels: readonly string[] | undefined,
  langue: 'fr' | 'en'
): PastilleTrait[] {
  if (actuels === undefined) return []
  const courants = new Set(actuels.map(normaliserTrait))
  const origine: string[] = []
  for (const trait of imprimes ?? []) {
    const cle = normaliserTrait(trait)
    if (cle && !origine.includes(cle)) origine.push(cle)
  }
  const resultat: PastilleTrait[] = []
  for (const cle of origine) {
    resultat.push({ cle, texte: libelle(cle, langue), etat: courants.has(cle) ? 'imprime' : 'perdu' })
  }
  for (const cle of courants) {
    if (cle && !origine.includes(cle)) resultat.push({ cle, texte: libelle(cle, langue), etat: 'gagne' })
  }
  // Gagnes avant perdus : ce qu'on a en plus se lit avant ce qu'on n'a plus.
  const rang: Record<EtatTrait, number> = { imprime: 0, gagne: 1, perdu: 2 }
  return resultat.sort((a, b) => rang[a.etat] - rang[b.etat])
}

/** Ce que le reglage laisse voir. « changements » ne montre rien tant que rien n'a bouge. */
export function pastillesVisibles(pastilles: readonly PastilleTrait[], mode: ModeTraits): PastilleTrait[] {
  if (mode === 'aucun') return []
  if (mode === 'tous') return [...pastilles]
  return pastilles.filter((p) => p.etat !== 'imprime')
}
