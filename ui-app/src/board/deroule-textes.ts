// Mise en phrase des etapes du deroule.
//
// Separe du decoupage (deroule-phase.ts) a dessein : le decoupage est une
// question de regles du jeu, la mise en phrase une question de langue. Les
// deux se testent separement, et le decoupage reste verifiable sans toucher
// au dictionnaire.

import type { EtapeDeroule, LigneBilan } from './deroule-phase'
import { t } from './langue'

/** Cles de titre que ce module sait rediger. Tout autre titre passe tel quel. */
const REDIGES = new Set(['attaque', 'manigance', 'menace', 'bilan'])

/**
 * Accord du pluriel francais : « 1 degat », « 2 degats ». L'anglais rend le
 * meme mot des deux cotes du dictionnaire, ce qui est correct la-bas.
 */
function pluriel(nombre: number, singulier: string, pluriels: string): string {
  return Math.abs(nombre) < 2 ? t(singulier) : t(pluriels)
}

export function titreEtape(etape: EtapeDeroule): string {
  if (!REDIGES.has(etape.titre)) return etape.titre

  // Le bilan n'a ni auteur ni cible : c'est le point final de la phase, pas un
  // coup de plus. Son detail se lit sur ses lignes, juste en dessous.
  if (etape.titre === 'bilan') return t('Fin de la phase du méchant')

  // Les noms viennent du FAIT (voir deroule-phase.ts), pas d'une recherche
  // dans l'index du monde courant : une carte morte pendant la phase n'y est
  // plus, et l'etape affichait alors « Ultron attaque #88 ».
  const auteur = etape.auteurNom ?? ''
  const cible = etape.cibleNom ?? ''

  if (etape.titre === 'menace') {
    // Repli sur l'ancienne formule generique quand la source ne donne ni nom
    // ni montant : une phrase vague vaut mieux qu'une phrase fausse, et
    // « gagne undefined menaces » serait pire que tout.
    if (!cible || etape.montant === undefined) return t('Menace sur la manigance principale')
    return `${cible} ${t('gagne')} ${etape.montant} ${pluriel(etape.montant, 'menace', 'menaces')}`
  }

  return etape.titre === 'attaque'
    ? `${auteur} ${t('attaque')} ${cible}`
    : `${auteur} ${t('complote contre')} ${cible}`
}

/**
 * Le chiffre du coup, sous le titre : « → 4 dégâts », « → 2 menaces ».
 *
 * Vide pour l'etape de menace, dont le chiffre est deja dans le titre, et
 * pour toute etape dont la source ne donne pas de montant.
 */
export function resultatEtape(etape: EtapeDeroule): string {
  if (etape.montant === undefined) return ''
  if (etape.titre === 'attaque') {
    return `→ ${etape.montant} ${pluriel(etape.montant, 'dégât', 'dégâts')}`
  }
  if (etape.titre === 'manigance') {
    return `→ ${etape.montant} ${pluriel(etape.montant, 'menace', 'menaces')}`
  }
  return ''
}

/**
 * Le compteur de la cible apres le coup, a droite du titre : « 5/8 » pour une
 * manigance sur son seuil, « 7 » pour des points de vie, qui n'en ont pas.
 *
 * Rien du tout sans compteur : un « undefined » ou un « 0/0 » vaut moins que
 * l'absence, et un compteur faux serait pire que pas de compteur. Aucun
 * passage par le dictionnaire ici, il n'y a que des chiffres.
 */
function compteur(restant: number | undefined, plafond: number | undefined): string {
  if (typeof restant !== 'number' || !Number.isFinite(restant)) return ''
  // Le seuil ne s'affiche que s'il en est un : un plafond absent ou nul ne dit
  // rien et donnerait un « 0/0 ».
  if (typeof plafond === 'number' && plafond > 0) return `${restant}/${plafond}`
  return `${restant}`
}

export function compteurEtape(etape: EtapeDeroule): string {
  return compteur(etape.restant, etape.plafond)
}

/**
 * Une ligne du bilan : « Colossus a pris 6 dégâts », « L’Effraction ! a gagné
 * 3 menaces ». Le total est deja fait (voir `lignesBilan`), on le met en
 * phrase et rien de plus.
 */
export function texteLigneBilan(ligne: LigneBilan): string {
  if (ligne.genre === 'degats') {
    return `${ligne.cibleNom} ${t('a pris')} ${ligne.total} ${pluriel(ligne.total, 'dégât', 'dégâts')}`
  }
  return `${ligne.cibleNom} ${t('a gagné')} ${ligne.total} ${pluriel(ligne.total, 'menace', 'menaces')}`
}

/**
 * Le compteur de la cible a droite de sa ligne de bilan, meme regle qu'ailleurs
 * dans le cartouche : rien du tout quand la source n'en donne pas.
 *
 * Les points de vie s'affichent donc SEULS (« 8 »), pas « 8/14 » : le moteur ne
 * publie pas les PV maximum du heros a cote de ses faits, et un maximum invente
 * serait pire que pas de maximum.
 */
export function compteurLigneBilan(ligne: LigneBilan): string {
  return compteur(ligne.restant, ligne.plafond)
}

/**
 * L'annonce de la chute d'un heros : « Colossus est vaincu ».
 *
 * Rien du tout sans la marque posee par `etapesDeroule` (voir
 * `EtapeDeroule.defaite`), et rien du tout sans nom : une defaite anonyme
 * n'apprendrait rien, et une defaite annoncee a tort ferait douter le joueur de
 * tout le reste du cartouche.
 *
 * Accord au masculin, comme partout ailleurs sur le plateau (« Les heros sont
 * vaincus », « Heros vaincu : il ne participe pas... ») : le monde ne publie
 * pas le genre d'un heros, et l'inventer se tromperait une fois sur deux.
 */
export function texteDefaite(etape: EtapeDeroule): string {
  if (!etape.defaite) return ''
  const nom = etape.cibleNom ?? ''
  if (!nom) return ''
  // Cle a trous plutot qu'une concatenation : l'anglais ne place pas le verbe
  // au meme endroit (« Colossus is defeated »).
  return t('%1 est vaincu').replace('%1', nom)
}

/** La phrase qui dit que le deroule s'arrete la. */
export function texteArretDefaite(): string {
  return t('La phase s\'arrête ici.')
}

/** Ce que dit le bilan quand la phase n'a rien coute du tout. */
export function texteBilanVide(): string {
  return t('Aucun dégât, aucune menace.')
}

const REGLES: Record<string, string> = {
  'regle:menace': 'Point 1 : chaque joueur ajoute 1 menace à la manigance principale.',
  'regle:activations': 'Point 2 : chaque ennemi s\'active contre le héros engagé avec lui.',
  'regle:revelation': 'Point 4 : chaque joueur révèle sa carte rencontre et en applique l\'effet.',
}

export function regleEtape(etape: EtapeDeroule): string {
  const regle = REGLES[etape.regle]
  return regle ? t(regle) : ''
}
