// Pose la mise en scene d'une etape sur les vraies cartes du plateau.
//
// IMPERATIF, comme halo-statut.ts et pas-a-pas.ts : classes ajoutees puis
// retirees sur l'element reel. Passer par React ferait re-rendre le plateau
// entier a chaque etape pour une decoration transitoire, et le plateau est
// lourd (plusieurs dizaines de cartes).
//
// Le nettoyage est fait a CHAQUE changement d'etape et au demontage : sans
// lui, quitter la phase laisserait une carte agrandie et un plateau assombri
// pour le reste de la partie.
//
// Et le voile ne s'allume QUE si une carte a ete trouvee : voir la regle de
// surete plus bas.

import { useEffect } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'

const EN_AVANT = 'deroule-en-avant'
const CIBLE = 'deroule-cible'
const VOILE = 'deroule-voile'

function carteDe(id: number): HTMLElement | null {
  return document.querySelector<HTMLElement>(
    `.plateau-scene .scan-card[data-card-id="${id}"]`
  )
}

export function useDerouleScene(etape: EtapeDeroule | undefined, actif: boolean): void {
  // On depend de la CLE, pas de l'objet `etape` : celui-ci vient de
  // `etapes[index]` dans DeroulePhase, et `etapes` est reconstruit a chaque
  // re-parse du monde par le moteur, meme quand rien n'a change. Deja corrige
  // une fois dans pas-a-pas.ts pour la meme raison (« le meme rendu peut etre
  // republie plusieurs fois ») : sans cela, l'effet se demonterait et se
  // remonterait a chaque trame, retirant puis reposant les classes.
  const cle = etape?.cle
  useEffect(() => {
    if (!actif || !etape) return
    const scene = sceneDe(etape)

    const auteur = scene.carteEnAvant !== undefined ? carteDe(scene.carteEnAvant) : null
    const cible = scene.cible !== undefined ? carteDe(scene.cible) : null

    auteur?.classList.add(EN_AVANT)
    cible?.classList.add(CIBLE)
    // REGLE DE SURETE, et elle vaut pour TOUTES les etapes, pas pour une seule :
    // le voile ne s'allume que si quelque chose ressort dessous. Assombrir le
    // plateau sans rien y designer ne rend jamais service, et c'est exactement
    // ce que le joueur a vu en partie a l'etape de menace : « il assombrit
    // tout, on sait pas sur quoi on doit cliquer ».
    //
    // `sceneDe` decide de la mise en scene sans voir le plateau : elle ne peut
    // pas savoir qu'une carte a quitte la table. C'est donc ICI, la ou l'on
    // sait ce qu'on a trouve, que la regle se pose.
    const misEnAvant = auteur !== null || cible !== null
    if (scene.voile && misEnAvant) document.body.classList.add(VOILE)

    return () => {
      auteur?.classList.remove(EN_AVANT)
      cible?.classList.remove(CIBLE)
      document.body.classList.remove(VOILE)
    }
    // `cle` suffit : une etape est immuable, sa cle l'identifie (meme choix
    // que usePasAPas).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cle, actif])
}
