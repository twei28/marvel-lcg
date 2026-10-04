// LA TABLE CALEE SUR LE RECIT DE LA PHASE DU MECHANT (04/10/2026).
//
// Signale par l'utilisateur : « sur la table il retourne la carte boost ou
// rencontre avant qu'on ait fait suivant ». Cause : le cartouche relache tout
// de suite une trame qui ne lui fabrique aucune etape (`cartoucheAJour`). Or le
// retournement d'un boost ou d'une carte rencontre arrive dans de telles
// trames : l'etape « attaque » n'est completee qu'a la RESOLUTION. Le moteur
// avance donc, et la table, qui dessinait le monde le plus recent, devancait
// le recit.
//
// Choix de l'utilisateur : « table calee sur le recit ». Ce qui n'est pas
// encore raconte n'apparait pas sur la table : on retient, pour chaque etape,
// le monde au moment ou elle a pris sa forme actuelle, et la table dessine
// celui de l'etape affichee.
//
// ⚠ Deux exceptions, voulues :
//  - une QUESTION du moteur au joueur : la table repasse sur le monde reel,
//    les clics doivent viser les cartes telles qu'elles sont ;
//  - hors phase du mechant, ou sans instantane pour l'etape (le bilan) : le
//    monde reel, comme avant.
import type { EtapeDeroule } from './deroule-phase'
import type { World } from './world'

export type Instantane = { signature: string; monde: World }
export type Instantanes = ReadonlyMap<string, Instantane>

/**
 * Le nouvel etat des instantanes apres l'arrivee d'un monde.
 *
 * Une etape garde le monde de la trame ou sa SIGNATURE (son contenu affiche) a
 * change pour la derniere fois. Les trames qui ne la changent pas, comme le
 * retournement d'un boost avant la resolution de l'attaque, ne la touchent pas.
 */
export function majInstantanes(
  precedents: Instantanes,
  etapes: readonly EtapeDeroule[],
  monde: World | undefined,
  phaseEnCours: boolean
): Instantanes {
  if (!phaseEnCours || !monde) return precedents.size === 0 ? precedents : new Map()
  let suivants: Map<string, Instantane> | undefined
  for (const etape of etapes) {
    const signature = JSON.stringify(etape)
    if (precedents.get(etape.cle)?.signature === signature) continue
    suivants ??= new Map(precedents)
    suivants.set(etape.cle, { signature, monde })
  }
  return suivants ?? precedents
}

/** Le monde que la table doit dessiner, ou `undefined` pour le monde reel. */
export function mondeDeLaTable(
  instantanes: Instantanes,
  cleAffichee: string | undefined,
  questionAuJoueur: boolean
): World | undefined {
  if (questionAuJoueur || cleAffichee === undefined) return undefined
  return instantanes.get(cleAffichee)?.monde
}
