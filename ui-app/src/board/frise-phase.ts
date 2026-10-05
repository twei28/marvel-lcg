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
export type Totaux = { degats: number; menaces: number; statuts: string[]; sbires: number; autres: number }

/** Des totaux a zero, a remplir par `compter`. */
export function totauxVides(): Totaux {
  return { degats: 0, menaces: 0, statuts: [], sbires: 0, autres: 0 }
}

/**
 * UN COUP ELEMENTAIRE de la phase : ce qu'UNE carte a encaisse (degats,
 * menaces, un statut), ou une carte entree en jeu. Une etape en porte zero,
 * un ou plusieurs (ses effets, ses consequences).
 *
 * ⚠ LA REGLE DE COMPTAGE N'EXISTE QU'ICI (piege 43 de la carte du 04/10/2026).
 * Le resultat court des onglets (`resumeOnglet`, par `compter`) et le bilan en
 * trois colonnes du cartouche du bas (`bilanTroisColonnes`, vue-cartouche.ts)
 * lisent tous deux ces coups : deux totaux differents pour la meme phase ne
 * peuvent plus apparaitre.
 */
export type Coup =
  | {
      genre: 'degats' | 'menaces'
      montant: number
      cibleNom?: string
      cibleId?: number
      /** Le compteur de la cible apres ce coup, quand la source le donne. */
      restant?: number
      plafond?: number
    }
  | { genre: 'statut'; statut: string; cibleNom?: string; cibleId?: number }
  | { genre: 'sbire' | 'autre'; carteNom?: string; carteId?: number }

/** Les coups d'une etape, ses effets et ses consequences compris, dans l'ordre. */
export function coupsDe(etape: EtapeDeroule): Coup[] {
  const coups: Coup[] = []
  const resolue = etape.etat === undefined || etape.etat === 'resolu'
  const montant = etape.montant ?? 0
  const cible = { cibleNom: etape.cibleNom, cibleId: etape.cibleId, restant: etape.restant, plafond: etape.plafond }
  if (etape.titre === 'attaque' && resolue) coups.push({ genre: 'degats', montant, ...cible })
  if ((etape.titre === 'manigance' && resolue) || etape.titre === 'menace') coups.push({ genre: 'menaces', montant, ...cible })
  if (etape.titre === 'statut') {
    const nom = libelleDeStatut(etape.statut)
    if (nom) coups.push({ genre: 'statut', statut: nom, cibleNom: etape.cibleNom, cibleId: etape.cibleId })
  }
  if (etape.titre === 'entree') coups.push({ genre: 'sbire', carteNom: etape.cibleNom, carteId: etape.carteId })
  for (const effet of etape.effets ?? []) {
    if (effet.genre === 'degats' || effet.genre === 'menace') {
      coups.push({
        genre: effet.genre === 'degats' ? 'degats' : 'menaces',
        montant: effet.montant,
        cibleNom: effet.cible,
        cibleId: effet.cible_id,
        restant: effet.restant ?? undefined,
      })
    } else {
      coups.push({ genre: effet.type === 'sbire' ? 'sbire' : 'autre', carteNom: effet.carte, carteId: effet.carte_id })
    }
  }
  for (const consequence of etape.consequences ?? []) coups.push(...coupsDe(consequence))
  return coups
}

/**
 * Ajoute aux totaux ce qu'une etape a coute. Exportee pour le bilan du
 * cartouche du bas : une seule regle de comptage (voir `Coup`).
 */
export function compter(etape: EtapeDeroule, totaux: Totaux): void {
  for (const coup of coupsDe(etape)) {
    if (coup.genre === 'degats') totaux.degats += coup.montant
    else if (coup.genre === 'menaces') totaux.menaces += coup.montant
    else if (coup.genre === 'statut') {
      if (!totaux.statuts.includes(coup.statut)) totaux.statuts.push(coup.statut)
    } else if (coup.genre === 'sbire') totaux.sbires += 1
    else totaux.autres += 1
  }
}

/**
 * LA DISTRIBUTION FONDUE DANS LES CARTES RENCONTRE (decision D15 du
 * 04/10/2026, scene PC seulement). Les etapes du point 3 sont RETIREES de la
 * liste avant le controleur : elles ne coutent plus aucun clic, et leur compte
 * voyage a part, en tete de la pastille « 3. Cartes rencontre ».
 *
 * ⚠ ELLE RETIRE, ELLE NE CREE RIEN. Aucune cle n'est fabriquee ni changee :
 * les cles pilotent le rythme (`cartouche-a-jour.ts`), et une cle neuve ferait
 * defiler ou figer la phase. Rien a retirer : la MEME reference est rendue,
 * pour ne pas relancer les memos de l'appelant.
 */
export function fusionnerDistribution(etapes: EtapeDeroule[]): { etapes: EtapeDeroule[]; cartesDistribuees: number } {
  if (!etapes.some((e) => e.temps === 'distribution')) return { etapes, cartesDistribuees: 0 }
  const cartesDistribuees = etapes.reduce(
    (somme, e) => somme + (e.temps === 'distribution' && e.titre === 'distribution' ? (e.montant ?? 1) : 0),
    0
  )
  return { etapes: etapes.filter((e) => e.temps !== 'distribution'), cartesDistribuees }
}

/** Le compte des cartes distribuees retenu pour une phase (voir ci-dessous). */
export type DistribueesRetenues = { round: number | undefined; compte: number }

/**
 * LE COMPTE DES CARTES DISTRIBUEES, RETENU POUR LA PHASE (D15, board.tsx).
 *
 * Le moteur incremente le round dans la meme foulee qu'il quitte la phase du
 * mechant : le journal du round se vide, `fusionnerDistribution` rend 0, et le
 * bilan doit pourtant encore dire « 1 carte distribuée ». Le compte se garde
 * donc d'un round a l'autre, et ne repart de zero que lorsque la phase du
 * mechant d'un AUTRE round s'ouvre (ou qu'un autre round apporte sa propre
 * distribution). Jamais au simple changement de round : ce serait avant le
 * bilan. Meme reference quand rien ne change.
 */
export function retenirCartesDistribuees(
  precedent: DistribueesRetenues,
  maintenant: { round: number | undefined; compte: number; enPhase: boolean }
): DistribueesRetenues {
  if (precedent.round !== maintenant.round) {
    if (maintenant.compte > 0 || maintenant.enPhase) return { round: maintenant.round, compte: maintenant.compte }
    return precedent
  }
  return maintenant.compte > precedent.compte ? { round: precedent.round, compte: maintenant.compte } : precedent
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
  const totaux = totauxVides()
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
  // ⚠ LA DISTRIBUTION N'EST JAMAIS DECLAREE VIDE (04/10/2026). En scene PC ses
  // etapes sont retirees AVANT d'arriver ici (`fusionnerDistribution`) : la
  // declarer vide fabriquerait une etape, donc un clic, que la fusion supprime.
  // Et une phase reelle distribue toujours au moins une carte.
  const vides: EtapeDeroule[] = TEMPS_DE_LA_CARTE.filter(
    (temps, rang) => temps !== 'distribution' && rang > rangPremier && rang < rangDernier && !presents.has(temps)
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
