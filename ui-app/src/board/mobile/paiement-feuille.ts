// Les cartes que la feuille de PAIEMENT montre DANS la fenetre (26/10/2026).
//
// Avant : « PAY 2 TO PLAY » etait une boite posee au centre qui cachait la main. Le joueur ne pouvait plus toucher les cartes a
// depenser. Maintenant la feuille (la meme qu'on glisse pour les cibles) porte la rangee des cartes qui PEUVENT payer :
//  - celles de la main d'abord (c'est la qu'on paie presque toujours), puis celles de la table (soutiens qui produisent) ;
//  - une carte deja posee en paiement reste dans la rangee : un second toucher la retire (le moteur bascule, `basculerRessource`) ;
//  - une carte n'apparait qu'une fois, et seules celles que le moteur propose (role `ressource`) y entrent.
import type { CardEffectDelta } from '../../components/ScanCard'
import { avecInteraction } from '../Board'
import type { EtatInteractif } from '../interaction'
import type { Plateau, UniteAffichee } from '../zones'

export function cartesPayantes(
  plateau: Plateau,
  interactifs: Map<number, EtatInteractif>,
  effets: Map<number, CardEffectDelta>
): UniteAffichee[] {
  const vues = new Set<string>()
  const main: UniteAffichee[] = []
  const table: UniteAffichee[] = []
  for (const emplacement of plateau.emplacements) {
    const destination = emplacement.cle === 'main' ? main : table
    for (const groupe of emplacement.groupes) {
      for (const unite of groupe) {
        if (vues.has(unite.carte.id)) continue
        if (interactifs.get(Number(unite.carte.id))?.role !== 'ressource') continue
        vues.add(unite.carte.id)
        destination.push({ ...unite, carte: avecInteraction(unite.carte, interactifs, effets) })
      }
    }
  }
  return [...main, ...table]
}

export type ResumePaiement = {
  requis: number
  paye: number
  /** Ce qu'il reste a payer (0 des que le cout est couvert, surpaiement compris). */
  manque: number
  couvert: boolean
}

export function resumePaiement({ coutRequis, coutPaye }: { coutRequis?: number; coutPaye: number }): ResumePaiement {
  if (coutRequis === undefined || coutRequis <= 0) return { requis: 0, paye: 0, manque: 0, couvert: false }
  const manque = Math.max(0, coutRequis - coutPaye)
  return { requis: coutRequis, paye: coutPaye, manque, couvert: manque === 0 }
}
