// QUI L'ON ATTEND, quand le plateau ne bouge plus.
//
// Le moteur Python n'avance qu'une fois que TOUS les clients ont accuse
// reception de la trame (`WaitSync`, engine/controller/manager.py), et il
// n'interroge qu'un joueur a la fois (`asking_players`). Deux facons d'attendre
// quelqu'un d'autre, donc, et le plateau ne disait ni l'une ni l'autre : il
// affichait « La suite arrive… », qui parle du MOTEUR, que le moteur soit
// occupe ou qu'un coequipier soit parti chercher un cafe (constat F5 de l'audit
// du 06/09/2026).
//
// CE QUE LE MOTEUR NE DIT PAS. Le serveur sait exactement quel client est en
// retard (`client_manager.client_synced`, engine/device/manager/web/client.py),
// mais ce tableau n'entre PAS dans la trame poussee au plateau
// (`FrameDescriptor`, game/render/descriptor/frame.py, qui ne porte que
// `ask_players`, `total_players` et `sieges_absents`). Aucun client ne peut
// donc nommer celui qui n'a pas encore acquitte. On sait seulement, ici :
//
//  - QUI le moteur interroge (`ask_players[0]`, publie sous `joueurDemande`) :
//    la, on peut nommer le joueur ;
//  - que plus rien n'arrive depuis un moment : la, on ne peut dire que
//    « un autre joueur ».
//
// Ce module est PUR (a l'exception de son hook, qui n'est qu'un minuteur) :
// aucune lecture du DOM, aucune traduction, de quoi le verifier sans plateau.

import { useEffect, useState } from 'react'

/**
 * Le silence au bout duquel on dit qu'on attend quelqu'un d'autre.
 *
 * Une trame en chasse une autre en quelques dizaines de millisecondes quand la
 * table suit : deux secondes et demie de silence complet pendant la phase du
 * mechant ne s'expliquent plus par le calcul du moteur. Assez long pour ne pas
 * clignoter a chaque respiration du reseau, assez court pour que le joueur
 * comprenne avant de croire que sa partie a plante.
 */
export const DELAI_SILENCE_TABLE_MS = 2500

/** Le siege que le moteur interroge, quand ce n'est pas le notre. */
export type JoueurAttendu = { numero: number; nom?: string }

/**
 * Le moteur interroge-t-il QUELQU'UN D'AUTRE ?
 *
 * `joueurDemande` est `ask_players[0]`, pousse a TOUS les clients (voir
 * `server_socket.py`) : chacun sait donc a qui la question est posee, meme
 * quand le serveur lui refuse le contenu de la question (sieges proteges,
 * `handle_get_ask` rend `{}` au client non interroge).
 *
 * HOT-SEAT : rien du tout. Hors multijoueur, ce navigateur tient TOUS les
 * sieges et repond pour chacun d'eux (voir `adresseSocket`, moteur.ts) : le
 * moteur n'attend jamais quelqu'un d'autre, et annoncer « En attente de
 * Spider-Man » a celui qui joue Spider-Man serait un contresens.
 */
export function joueurAttendu({
  joueurDemande,
  playerId,
  multijoueur,
  nomsHerosParJoueur = [],
}: {
  joueurDemande?: number
  playerId: number
  multijoueur: boolean
  nomsHerosParJoueur?: readonly (string | undefined)[]
}): JoueurAttendu | undefined {
  if (!multijoueur) return undefined
  if (joueurDemande === undefined) return undefined
  if (joueurDemande === playerId) return undefined
  // Le nom peut manquer (monde pas encore lu, siege vide) : on rend le numero
  // seul, et l'affichage retombe sur « un autre joueur » plutot que d'inventer.
  return { numero: joueurDemande + 1, nom: nomsHerosParJoueur[joueurDemande] || undefined }
}

/**
 * LA TABLE NE DIT PLUS RIEN depuis `DELAI_SILENCE_TABLE_MS`.
 *
 * C'est tout ce qu'un client peut savoir du retard d'un autre : le moteur ne
 * publie pas `client_synced` (voir l'en-tete). Le cas vise est celui de F5 : un
 * joueur en Instantane, un en Detaille. Le premier acquitte tout de suite, le
 * second retient, et le premier voit son plateau se figer sans un mot.
 *
 * `renderId` est un NOMBRE, pas le monde : une dependance d'effet sur l'objet
 * du monde re-armerait le minuteur a chaque rendu et il n'arriverait jamais a
 * echeance (meme piege que dans `useDerouleScene` et `DeroulePhase`).
 *
 * `actif` est la seule chose qui allume le guetteur : l'appelant y met ce qui
 * fait de ce silence une attente (multijoueur, phase du mechant en cours, et
 * rien a faire de notre cote). Faux, le hook oublie tout de suite ce qu'il
 * avait constate.
 */
export function useTableSilencieuse(renderId: number | undefined, actif: boolean): boolean {
  const [silencieuse, setSilencieuse] = useState(false)
  useEffect(() => {
    setSilencieuse(false)
    if (!actif) return
    const minuteur = window.setTimeout(() => setSilencieuse(true), DELAI_SILENCE_TABLE_MS)
    return () => window.clearTimeout(minuteur)
  }, [renderId, actif])
  return silencieuse
}
