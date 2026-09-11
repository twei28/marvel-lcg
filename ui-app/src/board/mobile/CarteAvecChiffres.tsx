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
  // `stats`, `jauge`, `allyHp` et `schemeThreat` sont retires avant le spread :
  // toScanCard() les peuple pour une carte reelle, et ScanCard pose alors ses
  // PROPRES chiffres sur l'illustration (badges cales, bande PV/menace,
  // pastilles PV/menace) — exactement ce que ce composant existe pour eviter.
  // Sur un telephone, un chiffre pose sur une carte de 64 px est illisible et
  // cache le dessin ; `chiffres` porte deja tout cet affichage, a cote de la
  // carte (correction post tache 6 : `jauge`/`allyHp`/`schemeThreat`
  // fuyaient encore vers ScanCard, meme apres le retrait de `stats`).
  const { stats: _stats, jauge: _jauge, allyHp: _allyHp, schemeThreat: _schemeThreat, ...carteSansChiffres } = carte
  return (
    <div className="portrait-carte">
      <ScanCard {...carteSansChiffres} highlight={false} onSelect={onOuvrir} />
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
