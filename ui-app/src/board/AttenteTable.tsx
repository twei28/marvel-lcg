// « En attente de Spider-Man », pour le joueur qui n'a pas de cartouche.
//
// Le mode Instantane n'affiche aucun deroule : quand la table attend un joueur
// en Detaille, son plateau se fige sans un cartouche, sans un bouton, sans un
// message (constat F5 de l'audit du 06/09/2026). Le reglage est presente comme
// personnel alors qu'il est impose a toute la table par le plus lent, et rien
// ne le disait.
//
// Une LIGNE, pas un bandeau : la table n'est pas en panne, elle attend, et
// l'attente dure d'ordinaire quelques secondes. Rien a cliquer, rien qui
// recouvre une carte (voir `.attente-table` dans board.css).

import { texteAttente } from './deroule-textes'

export function AttenteTable({ nom }: { nom?: string }) {
  return (
    <p className="attente-table" role="status" aria-live="polite">
      {texteAttente({ autreJoueur: true, nom })}
    </p>
  )
}
