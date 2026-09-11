// Une carte de la table en PETIT, avec ses chiffres en gros A COTE.
//
// C'est le geste central du portrait, releve sur play.marvelsimulator.com le
// 11/09/2026 : ils ne posent JAMAIS un chiffre sur l'illustration. Sur un
// telephone, une bulle « 14/14 » collee sur une carte de 70 px devient
// illisible et cache le dessin ; le meme chiffre pose a cote, en gros, se lit
// sans effort et laisse la carte entiere.
import type { ReactElement } from 'react'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'

export function CarteAvecChiffres({
  carte,
  nom,
  surtitre,
  chiffres,
  onOuvrir,
}: {
  carte: ScanCardProps
  nom: string
  surtitre?: string
  chiffres: Array<{ valeur: string; libelle: string }>
  onOuvrir?: () => void
}): ReactElement {
  // `stats` est retire avant le spread : toScanCard() le peuple TOUJOURS pour
  // une carte reelle, et ScanCard pose alors ses propres badges chiffres EN
  // PLUS, colles sur l'illustration (.scan-stats-calee, position absolute) —
  // exactement ce que ce composant existe pour eviter. `chiffres` porte deja
  // cet affichage, a cote de la carte.
  const { stats: _stats, ...carteSansStats } = carte
  return (
    <div className="portrait-carte">
      <ScanCard {...carteSansStats} highlight={false} onSelect={onOuvrir} />
      <div className="portrait-carte-texte">
        {surtitre ? <span className="portrait-surtitre">{surtitre}</span> : null}
        <strong className="portrait-nom">{nom}</strong>
      </div>
      {chiffres.length > 0 ? (
        <div className="portrait-carte-chiffres">
          {chiffres.map(({ valeur, libelle }) => (
            <span className="portrait-chiffre" key={libelle}>
              <b>{valeur}</b>
              <small>{libelle}</small>
            </span>
          ))}
        </div>
      ) : null}
    </div>
  )
}
