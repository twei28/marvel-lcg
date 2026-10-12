// LES NOMS DE CARTES DE LA BOITE, SURVOLABLES (refonte du 12/10/2026, lot 2,
// decision 55) : dans la boite de l'essai, tout nom de carte ecrit (titre,
// calcul pose, resultats, bilan) se souligne en pointilles et ouvre la carte
// dans l'apercu habituel, a droite du plateau. Le survol est celui de la
// section (`apercu-survol.ts`) : le nom porte le meme `data-card-id` qu'une
// carte, rien d'autre a faire.
//
// Hors de l'essai, aucun fournisseur n'est pose : `Texte` rend sa chaine telle
// quelle, et le rendu d'avant ne change pas d'un octet.
import { createContext, useContext, type ReactNode } from 'react'
import type { ScanCardProps } from '../components/ScanCard'
import { decouperPhrase } from './deroule-textes'

export type NomDeCarte = { nom: string; carteId: number }

const NomsDeLaBoite = createContext<readonly NomDeCarte[]>([])

export const NomsSurvolables = NomsDeLaBoite.Provider

/** Un nom trop court (« X ») soulignerait des morceaux de mots. */
const LONGUEUR_MIN = 3

/**
 * Les noms a souligner : ceux dont la carte est MONTRABLE (presente dans la
 * liste que la loupe interroge), un seul identifiant par nom.
 */
export function nomsMontrables(
  candidats: ReadonlyArray<{ nom?: string; carteId?: number } | undefined>,
  scans: readonly ScanCardProps[]
): NomDeCarte[] {
  const montrables = new Set(scans.map((scan) => scan.id))
  const vus = new Set<string>()
  const noms: NomDeCarte[] = []
  for (const candidat of candidats) {
    const nom = candidat?.nom?.trim()
    const id = candidat?.carteId
    if (!nom || id === undefined || nom.length < LONGUEUR_MIN || vus.has(nom)) continue
    if (!montrables.has(String(id))) continue
    vus.add(nom)
    noms.push({ nom, carteId: id })
  }
  return noms
}

/** Une phrase dont les noms de cartes connus deviennent survolables. */
export function Texte({ children }: { children: string | undefined | null }): ReactNode {
  const noms = useContext(NomsDeLaBoite)
  if (!children || noms.length === 0) return children ?? null
  const morceaux = decouperPhrase(
    children,
    noms.map((n) => n.nom),
    noms.map((n) => n.carteId)
  )
  if (!morceaux.some((morceau) => morceau.gras)) return children
  return morceaux.map((morceau, rang) =>
    morceau.gras && morceau.carteId !== undefined ? (
      <b key={rang} className="essai-nom" data-card-id={String(morceau.carteId)}>
        {morceau.texte}
      </b>
    ) : (
      <span key={rang}>{morceau.texte}</span>
    )
  )
}
