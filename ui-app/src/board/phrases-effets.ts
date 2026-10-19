// Les phrases qui disent CE QUI ARRIVE À UNE CARTE : une seule source.
//
// ⚠ POURQUOI ELLE EXISTE (T15, 19/10/2026). Le toast posé au-dessus d'une carte
// disait « Klaw gagne 1 menace » quand on posait un statut Sonné sur Klaw :
// `board.tsx` tenait tout effet qui n'était ni des dégâts ni des soins pour de la
// menace. « Cette phrase ne veut rien dire », constat de l'utilisateur : un
// statut est une carte qu'on pose, pas une menace. Le même mot « gagne » servait
// aussi, dans le cartouche et le bilan, à poser un statut (« Klaw gagne Sonné »).
//
// Règle : « gagne / perd » ne se dit que de ce qui se compte (menace, jeton
// nommé) ; un statut se REÇOIT ou se PERD, et son nom est précédé du mot
// « statut ». Les PV et les dégâts gardent leurs verbes (« subit », « récupère »).
import { nomDeCompteur } from './compteurs-fr'
import { libelleStatut, type Statut } from './effets-statuts'
import { langueActuelle, t } from './langue'
import type { CardEffectDelta } from '../components/ScanCard'

/** « dégât » au singulier, « dégâts » au pluriel : le français accorde dès 2. */
function pluriel(nombre: number, singulier: string, pluriels: string): string {
  return Math.abs(nombre) < 2 ? t(singulier) : t(pluriels)
}

/** « Klaw reçoit un statut Sonné ». */
export function phraseStatutRecu(nom: string, statut: string): string {
  return `${nom} ${t('reçoit un statut')} ${statut}`
}

/** « Klaw perd le statut Sonné ». */
export function phraseStatutPerdu(nom: string, statut: string): string {
  return `${nom} ${t('perd le statut')} ${statut}`
}

/** Plusieurs statuts d'un coup : « Hulk reçoit les statuts Sonné et Désorienté ». */
export function phraseStatutsRecus(nom: string, statuts: string[]): string {
  if (statuts.length === 1) return phraseStatutRecu(nom, statuts[0])
  const dernier = statuts[statuts.length - 1]
  return `${nom} ${t('reçoit les statuts')} ${statuts.slice(0, -1).join(', ')} ${t('et')} ${dernier}`
}

export function phraseStatutsPerdus(nom: string, statuts: string[]): string {
  if (statuts.length === 1) return phraseStatutPerdu(nom, statuts[0])
  const dernier = statuts[statuts.length - 1]
  return `${nom} ${t('perd les statuts')} ${statuts.slice(0, -1).join(', ')} ${t('et')} ${dernier}`
}

/** « Trafic Clandestin gagne 3 menaces » : seulement pour une VRAIE menace (une manigance). */
export function phraseMenace(nom: string, variation: number): string {
  const n = Math.abs(variation)
  return `${nom} ${variation > 0 ? t('gagne') : t('perd')} ${n} ${pluriel(n, 'menace', 'menaces')}`
}

/** « Spider-Man subit 2 dégâts ». */
export function phraseDegats(nom: string, montant: number): string {
  const n = Math.abs(montant)
  return `${nom} ${t('subit')} ${n} ${pluriel(n, 'dégât', 'dégâts')}`
}

/** « Hulk récupère 2 PV ». */
export function phraseSoin(nom: string, montant: number): string {
  return `${nom} ${t('récupère')} ${Math.abs(montant)} ${t('PV')}`
}

/**
 * « Spider-Man gagne 1 jeton Rage », « Spider-Man perd 2 jetons Toile ».
 * `cle` est la clé du compteur du moteur (`rage`, `web`, `acceleration`...).
 */
export function phraseJeton(nom: string, cle: string, variation: number): string {
  const n = Math.abs(variation)
  const verbe = variation > 0 ? t('gagne') : t('perd')
  if (cle === 'acceleration') {
    return `${nom} ${verbe} ${n} ${pluriel(n, 'jeton d’accélération', 'jetons d’accélération')}`
  }
  const brut = nomDeCompteur(cle)
  const libelle = brut.charAt(0).toUpperCase() + brut.slice(1)
  return `${nom} ${verbe} ${n} ${pluriel(n, 'jeton', 'jetons')} ${libelle}`
}

/** Le nom d'un statut dans la langue du plateau (« Sonné », « Hébété »...). */
export function nomDeStatut(statut: Statut): string {
  return libelleStatut(statut, 1, langueActuelle())
}

/**
 * La phrase du toast pour un changement constaté sur une carte. Chaque genre a
 * son verbe, et son OBJET : jamais de menace pour ce qui n'en est pas.
 */
export function phraseDeLEffet(nom: string, effet: CardEffectDelta): string {
  switch (effet.kind) {
    case 'damage':
      return phraseDegats(nom, effet.value)
    case 'heal':
      return phraseSoin(nom, effet.value)
    case 'threat':
      return phraseMenace(nom, effet.value)
    case 'token':
      return phraseJeton(nom, effet.jeton, effet.value)
    case 'status': {
      const tous = [{ statut: effet.statut, value: effet.value }, ...(effet.aussi ?? [])]
      const recus = tous.filter((x) => x.value > 0).map((x) => nomDeStatut(x.statut))
      const perdus = tous.filter((x) => x.value < 0).map((x) => nomDeStatut(x.statut))
      const phrases = []
      if (recus.length > 0) phrases.push(phraseStatutsRecus(nom, recus))
      if (perdus.length > 0) phrases.push(phraseStatutsPerdus(nom, perdus))
      return phrases.join(' · ')
    }
  }
}
