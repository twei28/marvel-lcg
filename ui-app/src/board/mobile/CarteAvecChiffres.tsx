// Une carte de la table en PETIT, avec ses chiffres en gros A COTE.
//
// C'est le geste central du portrait, releve sur play.marvelsimulator.com le
// 11/09/2026 : ils ne posent JAMAIS un chiffre sur l'illustration. Sur un
// telephone, une bulle « 14/14 » collee sur une carte de 70 px devient
// illisible et cache le dessin ; le meme chiffre pose a cote, en gros, se lit
// sans effort et laisse la carte entiere.
import type { ReactElement } from 'react'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import { useAppuiLong } from './useAppuiLong'

export function CarteAvecChiffres({
  carte,
  nom,
  surtitre,
  chiffres,
  onOuvrir,
  onJouer,
}: {
  carte: ScanCardProps
  nom: string
  surtitre?: string
  chiffres: Array<{ valeur: string; libelle: string }>
  /** Tap : ouvrir la carte pour la lire. */
  onOuvrir?: () => void
  /** Appui long : jouer la carte directement, comme dans la main. */
  onJouer?: () => void
}): ReactElement {
  // Meme geste que la main (MainPortrait) : tap pour lire, maintien pour
  // jouer. `useAppuiLong` tient un minuteur par appel, d'ou son appel ici,
  // une fois par carte, et jamais dans une boucle du parent.
  const appui = useAppuiLong(onJouer)
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
    <div className="portrait-carte" {...appui.gestes}>
      <ScanCard
        {...carteSansChiffres}
        highlight={false}
        onSelect={() => {
          // Le maintien vient de jouer la carte : le clic qui suit le
          // relachement ne doit pas AUSSI l'ouvrir, sinon un seul geste ferait
          // les deux. Meme garde que CarteMainPortrait.
          if (appui.vientDeDeclencher()) return
          // A defaut d'ouverture demandee, on laisse passer le `onSelect` que
          // la carte porte : c'est l'action DIRECTE posee par le moteur via
          // `avecInteraction`. L'ecrire `onSelect={onOuvrir}` sans repli
          // l'ecrasait par `undefined`, et plus rien n'etait jouable.
          if (onOuvrir) onOuvrir()
          else carteSansChiffres.onSelect?.()
        }}
      />
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
