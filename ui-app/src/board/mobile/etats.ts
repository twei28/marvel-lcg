// Les etats poses sur un personnage : coriace, sonne, desoriente.
//
// Le moteur les attache comme des CARTES (kind 'status'). Sur une carte de
// 100 px, une carte glissee derriere ne se lit pas : ces etats deviennent des
// pastilles lettrees au coin de la carte. Cette table dit la lettre, la classe
// CSS et le libelle de chacun. Partagee par CartePosee (paysage) et par le
// medaillon tant qu'il existe.

import type { ScanCardProps } from '../../components/ScanCard'

export type Etat = { lettre: string; classe: string; nom: string }

export const ETATS: Record<string, Etat> = {
  tough: { lettre: 'T', classe: 'est-coriace', nom: 'Coriace' },
  stunned: { lettre: 'S', classe: 'est-sonne', nom: 'Sonné' },
  confused: { lettre: 'C', classe: 'est-desoriente', nom: 'Désorienté' },
}

export function etatDe(carte: ScanCardProps): Etat | undefined {
  const connu = ETATS[carte.name.trim().toLowerCase()]
  if (connu) return connu
  if (carte.kind !== 'status') return undefined
  // Un statut au nom inconnu (traduit, ou maison) reste un etat : on garde son
  // initiale plutot que de le perdre en silence.
  const nom = carte.name.trim()
  return { lettre: (nom[0] ?? '?').toUpperCase(), classe: 'est-autre', nom }
}

export function separerAttachees(attachees: ScanCardProps[]): {
  etats: Etat[]
  ameliorations: ScanCardProps[]
} {
  const etats: Etat[] = []
  const ameliorations: ScanCardProps[] = []
  for (const attachee of attachees) {
    const etat = etatDe(attachee)
    if (etat) etats.push(etat)
    else ameliorations.push(attachee)
  }
  return { etats, ameliorations }
}
