// Les compteurs de la rencontre : gros chiffre, libelle minuscule.
//
// « 33 RENCONTRE · 0 DÉFAUSSE ». Meme hierarchie que le reste du portrait : le
// chiffre saute aux yeux, le mot se lit si on le cherche.
import type { ReactElement } from 'react'

export function CompteursPortrait({
  compteurs,
}: {
  compteurs: Array<{ valeur: number; libelle: string }>
}): ReactElement | null {
  if (compteurs.length === 0) return null
  return (
    <div className="portrait-compteurs">
      {compteurs.map(({ valeur, libelle }) => (
        <span className="portrait-chiffre" key={libelle}>
          <b>{valeur}</b>
          <small>{libelle}</small>
        </span>
      ))}
    </div>
  )
}
