// Les ETATS d'un personnage (cartes de statut) en etiquettes, aux couleurs des cartes du jeu (decision du
// 24/10/2026) : Sonne (vert), Desoriente (violet), Tenace (orange), Hebete (rouge), Intensifie (rose).
// Plus de deux etats : des initiales colorees, pour ne pas deborder du rond.
import type { ScanCardProps } from '../../../components/ScanCard'
import { libelleStatut, type Statut } from '../../effets-statuts'
import { langueActuelle } from '../../langue'

export type EtatRond = {
  cle: string
  texte: string
  initiales: string
  fond: string
  encre: string
}

const FAMILLES: Array<{ statut: Statut; motif: RegExp; fond: string; encre: string }> = [
  { statut: 'stunned', motif: /stun|sonn/i, fond: '#8fcf3a', encre: '#14210a' },
  { statut: 'confused', motif: /confus|d[ée]sorient/i, fond: '#7a3a82', encre: '#f2e6f7' },
  { statut: 'tough', motif: /tough|tenace|robuste/i, fond: '#ef8b18', encre: '#2a1600' },
  { statut: 'dazed', motif: /daze|h[ée]b[ée]t/i, fond: '#9a2624', encre: '#ffe9a8' },
  { statut: 'intensified', motif: /intensif/i, fond: '#f4a7c2', encre: '#3b0a1c' },
]
const AUTRE = { fond: '#6a7280', encre: '#ffffff' }

/** Les deux premieres lettres, avec une majuscule : « Sonné » -> « So ». */
export function initialesDe(nom: string): string {
  const mot = nom.trim()
  return mot.length === 0 ? '?' : mot.charAt(0).toUpperCase() + mot.charAt(1).toLowerCase()
}

export function etatsDe(attachees: ScanCardProps[]): EtatRond[] {
  const langue = langueActuelle()
  return attachees
    .filter((carte) => carte.kind === 'status')
    .map((carte) => {
      const famille = FAMILLES.find((f) => f.motif.test(`${carte.name} ${carte.codeCarte ?? ''} ${carte.id}`))
      // ⚠ Le moteur sert le nom du statut dans SA langue a lui (souvent l'anglais, « Tough »), pas celle du
      // plateau : sans traduction, un joueur FR voyait « Tough » au lieu de « Tenace » (constat du 04/11/2026,
      // etiquette sur Rhino en telephone). `libelleStatut` connait les 7 statuts dans les deux langues ;
      // un statut hors de cette liste (mod custom non reconnu) garde son nom brut, mieux qu'un texte vide.
      const texte = famille ? libelleStatut(famille.statut, 1, langue) : carte.name
      const couleurs = famille ?? AUTRE
      return { cle: carte.id, texte, initiales: initialesDe(texte), fond: couleurs.fond, encre: couleurs.encre }
    })
}

/** Etiquettes completes jusqu'a deux etats, initiales au-dela. */
export const SEUIL_INITIALES = 2
