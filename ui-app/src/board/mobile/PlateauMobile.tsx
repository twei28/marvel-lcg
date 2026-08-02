// Le niveau 1 : la vue d'etat. Elle tient TOUJOURS a l'ecran, en entier, et ne
// defile jamais. Ce n'est pas le plateau en petit, c'est l'etat de la partie en
// objets condenses.
//
// Elle accepte exactement les BoardProps du plateau PC : c'est ce qui permet a
// board.tsx de choisir l'un ou l'autre sans rien adapter.

import { useEffect, useMemo, useRef, useState } from 'react'
import { phaseAffichee, type BoardProps } from '../Board'
import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import { BandeMobile } from './BandeMobile'
import { repartir, type CleBande } from './bandes'
import { useCouches } from './couches'
import { ZoneFocus } from './ZoneFocus'
import './mobile.css'

/** Hauteurs de repos de la spec, en pixels CSS. La condensation fait le reste. */
const BUDGETS: Record<CleBande, number> = {
  vilain: 140,
  complots: 110,
  terrain: 120,
  rencontre: 64,
  heros: 200,
  main: 76,
}

/** Largeur utile d'une bande : la fenetre moins les marges laterales de mobile.css. */
const MARGES_LATERALES = 20

/**
 * Largeur reelle du cadre, tenue a jour par un ResizeObserver.
 *
 * Meme motif que useEchelle dans Board.tsx : window.resize ne voit pas les
 * changements de mise en page qui ne sont pas des redimensionnements de fenetre
 * (barre d'URL de Chrome mobile qui apparait ou disparait), donc seul un
 * ResizeObserver sur le cadre lui-meme est fiable.
 */
function useLargeurCadre(cadre: React.RefObject<HTMLDivElement | null>) {
  const [largeur, setLargeur] = useState(() => window.innerWidth)

  useEffect(() => {
    const element = cadre.current
    if (!element) return

    const recalculer = () => {
      const { width } = element.getBoundingClientRect()
      if (width === 0) return
      setLargeur(width)
    }

    recalculer()
    const observateur = new ResizeObserver(recalculer)
    observateur.observe(element)
    return () => observateur.disconnect()
  }, [cadre])

  return largeur
}

export function PlateauMobile({
  world,
  plateau,
  outils,
  actionsPartie,
  bas,
  onCardClick,
}: BoardProps) {
  const cadre = useRef<HTMLDivElement>(null)
  const largeur = useLargeurCadre(cadre)
  const { pile, ouvrir, fermer } = useCouches()

  const bandes = useMemo(() => repartir(plateau), [plateau])

  const couche = pile[pile.length - 1]
  const bandeEnFocus =
    couche?.sorte === 'focus' ? bandes.find((bande) => bande.cle === couche.bande) : undefined

  const ouvrirCarte = (carte: ScanCardProps) => {
    if (carte.onSelect) carte.onSelect()
    else onCardClick?.(carte)
  }

  return (
    <div className="plateau-mobile" ref={cadre}>
      <header className="pm-hud">
        <span className="pm-etat">
          <strong>{phaseAffichee(world.phase)}</strong>
          <span className="pm-tour">
            {t('Tour')} {world.round_id}
          </span>
        </span>
        <span className="pm-outils">
          {actionsPartie}
          {outils}
        </span>
      </header>

      <div className="pm-bandes">
        {bandes.map((bande) => (
          <BandeMobile
            key={bande.cle}
            bande={bande}
            budget={{
              largeur: Math.max(0, largeur - MARGES_LATERALES),
              hauteur: BUDGETS[bande.cle],
            }}
            onOuvrirBande={() => ouvrir({ sorte: 'focus', bande: bande.cle })}
            onOuvrirCarte={ouvrirCarte}
          />
        ))}
      </div>

      {bas ? <div className="pm-barre-action">{bas}</div> : null}

      {bandeEnFocus ? (
        <ZoneFocus bande={bandeEnFocus} onFermer={fermer} onOuvrirCarte={ouvrirCarte} />
      ) : null}
    </div>
  )
}
