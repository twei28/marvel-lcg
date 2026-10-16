// Les etats poses sur un personnage : coriace, sonne, desoriente, expose, camoufle.
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
  // QUATRIEME carte d'etat, ajoutee par le pack `sentinel` (T-Wrecks). Sans
  // cette ligne le repli generique plus bas afficherait deja un « E », mais
  // avec le nom ANGLAIS et la classe fourre-tout.
  exposed: { lettre: 'E', classe: 'est-expose', nom: 'Exposé' },
  // CINQUIEME carte d'etat (« Cloaked », pack TMNT, Shredder v3, scan Inkwire) :
  // +2 au prochain pouvoir de base / a la prochaine activation, OU -2 aux
  // prochains degats, puis la carte part. Meme raison que `exposed` : sans cette
  // ligne, le repli generique afficherait un « C » (deja pris par Désorienté)
  // avec le nom anglais.
  cloaked: { lettre: 'K', classe: 'est-camoufle', nom: 'Camouflé' },
  // SIXIEME carte d'etat (« Dazed », pack TMNT, Baxter Stockman v3, scan Inkwire) :
  // -2 au prochain pouvoir de base / a la prochaine activation, OU +2 aux
  // prochains degats, puis la carte part. Lettre H (le D est ambigu) ; sans
  // cette ligne le repli generique afficherait un « D » avec le nom anglais.
  dazed: { lettre: 'H', classe: 'est-hebete', nom: 'Hébété' },
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
