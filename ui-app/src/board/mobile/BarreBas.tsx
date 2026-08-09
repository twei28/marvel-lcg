// La barre du bas : tout le chrome du plateau mobile.
//
// Il n'y a PLUS de barre en haut. Sur les premières captures elle débordait de
// l'écran — sept boutons libellés sur 375 px — et elle volait la hauteur au
// plateau. Tout est descendu là où le pouce arrive.
//
// Elle a deux visages. Au repos elle porte les outils et les onglets de joueurs.
// Quand le moteur pose une question, elle SE TRANSFORME : les outils cèdent la
// place à la demande, puis reviennent. Aucune hauteur ajoutée, aucun panneau
// qui recouvre la table au moment précis où l'on a besoin de la voir.

import type { ReactNode } from 'react'
import './mobile.css'

export type BarreBasProps = {
  /** La demande du moteur en cours. Sa présence fait basculer la barre. */
  demande?: ReactNode
  /** Undo / Sauver / Options / Historique. */
  outils?: ReactNode
  /** Sélecteur de vue : en multi, c'est lui qui porte les onglets de joueurs. */
  onglets?: ReactNode
}

export function BarreBas({ demande, outils, onglets }: BarreBasProps) {
  if (demande) {
    return (
      <div className="pm-barre pm-barre-demande" role="group">
        {demande}
      </div>
    )
  }

  if (!outils && !onglets) return null

  return (
    <div className="pm-barre">
      {onglets ? <div className="pm-onglets">{onglets}</div> : null}
      {outils ? <div className="pm-outils">{outils}</div> : null}
    </div>
  )
}
