// LA FRISE de la phase du mechant : six onglets, un resultat court par onglet,
// et les temps vides dits par une etape courte (decisions de l'utilisateur du
// 03/10/2026, questions une a une ; inspirees de quincarter pour la frise et de
// marvelsimulator.com pour « une phrase par etape, etapes vides dites »).
//
// Module PUR, comme deroule-phase.ts : il compte et ordonne, le composant
// (DeroulePhase) dessine.

import { libelleDeStatut } from './deroule-textes'
import type { EtapeDeroule, TempsPhase } from './deroule-phase'
import { t } from './langue'

export type CleOnglet = 'menace' | 'mechant' | 'sbires' | 'distribution' | 'revelation' | 'bilan'

/**
 * Les intitules OFFICIELS, numerotes (choix de l'utilisateur, 03/10/2026). En
 * anglais, les titres du Rules Reference v1.8 (« 1. Place Threat », « 2. Enemies
 * Activate »...). L'etape 2 officielle couvre le mechant ET ses sbires ; la
 * frise les separe, d'ou 2a et 2b. Le Bilan est le sixieme onglet.
 */
export const ONGLETS: { cle: CleOnglet; libelle: string }[] = [
  { cle: 'menace', libelle: '1. Placer les menaces' },
  { cle: 'mechant', libelle: '2a. Le méchant s’active' },
  { cle: 'sbires', libelle: '2b. Les sbires s’activent' },
  { cle: 'distribution', libelle: '3. Attribuer les cartes Rencontre' },
  { cle: 'revelation', libelle: '4. Révéler les cartes Rencontre' },
  { cle: 'bilan', libelle: 'Bilan' },
]

/** Les cinq temps de la carte de reference : ceux qui peuvent etre vides. */
const TEMPS_DE_LA_CARTE: TempsPhase[] = ['menace', 'mechant', 'sbires', 'distribution', 'revelation']

const pluriel = (n: number, un: string, plusieurs: string) => t(n < 2 ? un : plusieurs)

/** Ce qu'une etape (et ce qui est range sous elle) a coute, additionne. */
type Totaux = { degats: number; menaces: number; statuts: string[]; sbires: number; autres: number }

function compter(etape: EtapeDeroule, totaux: Totaux): void {
  const resolue = etape.etat === undefined || etape.etat === 'resolu'
  const montant = etape.montant ?? 0
  if (etape.titre === 'attaque' && resolue) totaux.degats += montant
  if ((etape.titre === 'manigance' && resolue) || etape.titre === 'menace') totaux.menaces += montant
  if (etape.titre === 'statut') {
    const nom = libelleDeStatut(etape.statut)
    if (nom && !totaux.statuts.includes(nom)) totaux.statuts.push(nom)
  }
  if (etape.titre === 'entree') totaux.sbires += 1
  for (const effet of etape.effets ?? []) {
    if (effet.genre === 'degats') totaux.degats += effet.montant
    else if (effet.genre === 'menace') totaux.menaces += effet.montant
    else if (effet.type === 'sbire') totaux.sbires += 1
    else totaux.autres += 1
  }
  for (const consequence of etape.consequences ?? []) compter(consequence, totaux)
}

/**
 * Le RESULTAT COURT d'un onglet : le total par effet (« 3 dégâts · +1 menace »),
 * « aucun » quand rien n'a ete encaisse. Le Bilan resume toute la phase.
 *
 * L'ordre des effets est fixe (degats, menaces, statuts, entrees) : deux
 * onglets se comparent d'un coup d'oeil.
 */
export function resumeOnglet(etapes: EtapeDeroule[], cle: CleOnglet): string {
  const concernees = etapes.filter((e) => e.titre !== 'vide' && e.temps !== 'bilan' && (cle === 'bilan' || e.temps === cle))
  const totaux: Totaux = { degats: 0, menaces: 0, statuts: [], sbires: 0, autres: 0 }
  for (const etape of concernees) compter(etape, totaux)
  const morceaux: string[] = []
  if (totaux.degats > 0) morceaux.push(`${totaux.degats} ${pluriel(totaux.degats, 'dégât', 'dégâts')}`)
  if (totaux.menaces > 0) morceaux.push(`+${totaux.menaces} ${pluriel(totaux.menaces, 'menace', 'menaces')}`)
  morceaux.push(...totaux.statuts)
  if (totaux.sbires > 0) morceaux.push(`+${totaux.sbires} ${pluriel(totaux.sbires, 'sbire', 'sbires')}`)
  if (totaux.autres > 0) morceaux.push(`+${totaux.autres} ${pluriel(totaux.autres, 'carte en jeu', 'cartes en jeu')}`)
  if (morceaux.length === 0 && cle === 'distribution') {
    // Distribuer n'est pas encaisser : on compte les cartes recues.
    const cartes = concernees.reduce((somme, e) => somme + (e.titre === 'distribution' ? (e.montant ?? 1) : 0), 0)
    if (cartes > 0) return `${cartes} ${pluriel(cartes, 'carte', 'cartes')}`
  }
  if (morceaux.length === 0 && cle === 'revelation') {
    const cartes = concernees.filter((e) => e.titre === 'revelation').length
    if (cartes > 0) return `${cartes} ${pluriel(cartes, 'carte révélée', 'cartes révélées')}`
  }
  return morceaux.length > 0 ? morceaux.join(' · ') : t('aucun')
}

/**
 * LES TEMPS VIDES, dits par une etape courte avec « Suivant » (decision du
 * 03/10/2026) : « aucune menace posée », « le méchant ne s'active pas »,
 * « pas de sbire engagé », « rien à révéler ». Avant, un temps vide etait saute
 * sans un clic et seulement barre dans la frise : le joueur ne savait pas s'il
 * avait rate quelque chose.
 *
 * Une etape vide n'est inseree que pour un temps DEJA PASSE : apres le premier
 * temps qui a des etapes, et avant le dernier (ou jusqu'au bout une fois la
 * phase finie). Un temps a venir
 * n'est jamais declare vide (constat en partie : « Sbires (aucun) » affiche
 * pendant que le moteur demandait dans quel ordre activer deux sbires).
 *
 * Les etapes gardent l'ordre des temps : le tri est stable, et chaque etape
 * vide prend la place de son temps.
 */
export function avecTempsVides(etapes: EtapeDeroule[], phaseFinie: boolean): EtapeDeroule[] {
  if (etapes.length === 0) return etapes
  const presents = new Set(etapes.map((e) => e.temps))
  const rangs = etapes.map((e) => TEMPS_DE_LA_CARTE.indexOf(e.temps)).filter((r) => r !== -1)
  if (rangs.length === 0) return etapes
  // ⚠ RIEN AVANT LE PREMIER TEMPS CONNU. Le moteur inscrit toujours la menace
  // du point 1 (meme nulle) : un temps anterieur au premier fait connu vient
  // d'un journal incomplet (moteur ancien, sauvegarde), et le declarer vide
  // serait affirmer ce qu'on ne sait pas.
  const rangPremier = Math.min(...rangs)
  const rangDernier = phaseFinie ? TEMPS_DE_LA_CARTE.length : Math.max(...rangs)
  const vides: EtapeDeroule[] = TEMPS_DE_LA_CARTE.filter(
    (temps, rang) => rang > rangPremier && rang < rangDernier && !presents.has(temps)
  ).map((temps) => ({ cle: `vide:${temps}`, temps, titre: 'vide', regle: '', boosts: [] }))
  if (vides.length === 0) return etapes
  // ⚠ INSERER, NE PAS RETRIER. La liste recue est deja dans l'ordre du recit
  // (etapesDeroule) et le rythme des accuses en depend (« pose sur la DERNIERE
  // etape connue », cartouche-a-jour.ts) : un tri deplacerait une etape neuve.
  // Chaque etape vide se place devant la premiere etape d'un temps plus tardif.
  const ordre = (temps: TempsPhase) => {
    const rang = TEMPS_DE_LA_CARTE.indexOf(temps)
    return rang === -1 ? TEMPS_DE_LA_CARTE.length : rang
  }
  const resultat = [...etapes]
  for (const vide of vides) {
    const place = resultat.findIndex((e) => e.titre !== 'vide' && ordre(e.temps) > ordre(vide.temps))
    if (place === -1) resultat.push(vide)
    else resultat.splice(place, 0, vide)
  }
  return resultat
}
