// MenuTable.tsx — le menu de la TABLE elle-même, mode manuel uniquement.
//
// Distinct de MenuTriche (le menu d'UNE carte) : un clic droit hors de toute
// carte ouvre celui-ci (voir `CoucheTriche.tsx`, `surClicDroit`). Ajouté en
// ronde de correction 1 de la tâche 6 : « Faire apparaître une carte » est
// une action de TABLE, pas une action de carte — le jour où l'on cherche une
// carte, c'est justement parce qu'il en manque une, on ne doit pas avoir à en
// viser une pour l'atteindre. C'est aussi le geste de Tabletop Simulator, donc
// il ne surprend personne. Si d'autres actions de table se présentent plus
// tard, elles ont leur place toute trouvée ici plutôt que dans MenuTriche.

import { useEffect, useRef } from 'react'
import { t } from '../langue'

export type MenuTableProps = {
  /** Position du clic, en pixels écran. */
  x: number
  y: number
  onFermer: () => void
  /** Ouvre le catalogue (`CatalogueManuel`). */
  onFaireApparaitre: () => void
  /**
   * Ouvre `FinManuelle` (tâche 7) : une action de TABLE, comme « Faire
   * apparaître une carte » juste au-dessus — elle ne vise aucune carte
   * précise, elle a donc sa place ici plutôt que dans `MenuTriche`.
   */
  onTerminerPartie: () => void
}

export function MenuTable({
  x,
  y,
  onFermer,
  onFaireApparaitre,
  onTerminerPartie,
}: MenuTableProps) {
  const boite = useRef<HTMLDivElement | null>(null)

  // Même fermeture que MenuTriche : au clic extérieur et à Échap, sinon un
  // menu oublié reste par-dessus le plateau et intercepte les clics de jeu.
  useEffect(() => {
    const dehors = (evenement: MouseEvent) => {
      if (boite.current && !boite.current.contains(evenement.target as Node)) onFermer()
    }
    const touche = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') onFermer()
    }
    document.addEventListener('mousedown', dehors)
    document.addEventListener('keydown', touche)
    return () => {
      document.removeEventListener('mousedown', dehors)
      document.removeEventListener('keydown', touche)
    }
  }, [onFermer])

  // Même clamp que MenuTriche : un clic droit près du bord ouvrirait sinon un
  // menu partiellement invisible.
  const style = {
    left: Math.min(x, window.innerWidth - 240),
    top: Math.min(y, window.innerHeight - 340),
  }

  return (
    <div className="menu-triche" style={style} ref={boite} role="menu">
      <header className="menu-triche-titre">
        <span>{t('Table')}</span>
      </header>
      <ul className="menu-triche-liste">
        <li>
          <button
            type="button"
            onClick={() => {
              onFaireApparaitre()
              onFermer()
            }}
          >
            {t('Faire apparaître une carte')}
          </button>
        </li>
        <li>
          <button
            type="button"
            className="est-danger"
            onClick={() => {
              onTerminerPartie()
              onFermer()
            }}
          >
            {t('Terminer la partie')}
          </button>
        </li>
      </ul>
    </div>
  )
}
