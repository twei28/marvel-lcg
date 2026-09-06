// Mise en phrase des etapes du deroule.
//
// Separe du decoupage (deroule-phase.ts) a dessein : le decoupage est une
// question de regles du jeu, la mise en phrase une question de langue. Les
// deux se testent separement, et le decoupage reste verifiable sans toucher
// au dictionnaire.

import type { EtapeDeroule } from './deroule-phase'
import { t } from './langue'

/** Cles de titre que ce module sait rediger. Tout autre titre passe tel quel. */
const REDIGES = new Set(['attaque', 'manigance', 'menace'])

export function titreEtape(etape: EtapeDeroule): string {
  if (!REDIGES.has(etape.titre)) return etape.titre

  if (etape.titre === 'menace') return t('Menace sur la manigance principale')

  // Les noms viennent du FAIT (voir deroule-phase.ts), pas d'une recherche
  // dans l'index du monde courant : une carte morte pendant la phase n'y est
  // plus, et l'etape affichait alors « Ultron attaque #88 ».
  const auteur = etape.auteurNom ?? ''
  const cible = etape.cibleNom ?? ''
  return etape.titre === 'attaque'
    ? `${auteur} ${t('attaque')} ${cible}`
    : `${auteur} ${t('complote contre')} ${cible}`
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
