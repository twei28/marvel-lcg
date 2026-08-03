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
import { BandeHeros } from './BandeHeros'
import { BandeMobile } from './BandeMobile'
import { repartir, type CleBande } from './bandes'
import { useCouches } from './couches'
import { ZoneFocus } from './ZoneFocus'
import './mobile.css'

/**
 * Poids RELATIFS des bandes : pas des pixels absolus. L'espace vertical
 * reellement disponible (mesure sur .pm-bandes, voir useHauteurCadre) est
 * reparti entre les bandes affichees au prorata de ces poids (calcul de
 * budget.hauteur dans le composant, plus bas). Ces valeurs viennent des
 * hauteurs de repos de la spec ; ce qui a change (task 11) c'est qu'elles ne
 * sont plus prises pour argent comptant, seulement pour LEURS PROPORTIONS
 * relatives.
 */
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
 * Cout vertical fixe d'une bande, hors tuiles : le min-height de .bande-titre
 * (44px) + le padding vertical de .bande (6px*2) + sa bordure basse (1px) +
 * l'ecart de grille avec les tuiles (gap:4px de .bande). Mesure en Chromium
 * reel (task 11, gabarit s24) : 60px pile, constant quel que soit le contenu
 * ou la bande. (Pour la bande Heros, les bandeaux-joueur replies deplacent de
 * la hauteur DEPUIS les tuiles VERS eux-memes a l'interieur du meme budget
 * (voir BandeHeros.tsx) : le total consomme par la bande reste budget+60,
 * cette constante n'a donc pas besoin de connaitre le nombre de joueurs.)
 */
const OVERHEAD_BANDE = 60

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

/**
 * Hauteur reelle de .pm-bandes (la ligne 1fr entre le HUD et la barre
 * d'action), tenue a jour par un ResizeObserver. Independante du CONTENU de
 * .pm-bandes : min-height:0 dans mobile.css la laisse epouser exactement sa
 * part de grille, quel que soit ce qui est dedans (voir le commentaire sur
 * .pm-bandes dans mobile.css). Mesurer cet element ne boucle donc pas sur
 * lui-meme.
 *
 * C'est la piece qui manquait avant task 11 : BUDGETS etait fixe, sans lien
 * avec l'espace REEL restant apres le HUD et la barre d'action (qui varient
 * avec le contenu). Une bande pouvait donc recevoir un budget que la grille
 * CSS ne lui donnait pas vraiment, et le surplus etait invisible, avale par
 * l'overflow:hidden de .bande-tuiles, sans jamais faire deborder
 * .plateau-mobile ni .pm-bandes eux-memes.
 */
function useHauteurCadre(cadre: React.RefObject<HTMLDivElement | null>) {
  const [hauteur, setHauteur] = useState(() => window.innerHeight)

  useEffect(() => {
    const element = cadre.current
    if (!element) return

    const recalculer = () => {
      const { height } = element.getBoundingClientRect()
      if (height === 0) return
      setHauteur(height)
    }

    recalculer()
    const observateur = new ResizeObserver(recalculer)
    observateur.observe(element)
    return () => observateur.disconnect()
  }, [cadre])

  return hauteur
}

export function PlateauMobile({
  world,
  playerId,
  plateau,
  outils,
  actionsPartie,
  bas,
  onCardClick,
}: BoardProps) {
  const cadre = useRef<HTMLDivElement>(null)
  const cadreBandes = useRef<HTMLDivElement>(null)
  const largeur = useLargeurCadre(cadre)
  const hauteurBandes = useHauteurCadre(cadreBandes)
  const { pile, ouvrir, fermer } = useCouches()

  const bandes = useMemo(() => repartir(plateau), [plateau])

  // L'espace vraiment disponible pour les tuiles : la hauteur reelle de
  // .pm-bandes, moins le cout fixe (titre + padding + bordure + gap) de
  // CHAQUE bande affichee. Reparti au prorata des poids de BUDGETS entre les
  // bandes presentes : la somme des budgets rendus ne peut donc jamais
  // depasser ce que la grille CSS accorde reellement, quel que soit le
  // nombre de bandes visibles.
  const hauteurTuilesDisponible = Math.max(0, hauteurBandes - bandes.length * OVERHEAD_BANDE)
  const sommeBudgets = bandes.reduce((somme, bande) => somme + BUDGETS[bande.cle], 0)

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

      <div className="pm-bandes" ref={cadreBandes}>
        {bandes.map((bande) => {
          // Math.floor, jamais Math.round ni Math.ceil : arrondir la part de
          // chaque bande VERS LE BAS est la seule direction sure. Vers le
          // haut, la somme des parts arrondies peut depasser de 1px la
          // hauteur reellement mesuree (l'arrondi flottant de la division),
          // et ce depassement est exactement le genre de debordement d'un
          // pixel que ce budget existe pour empecher.
          const budget = {
            largeur: Math.max(0, largeur - MARGES_LATERALES),
            hauteur:
              sommeBudgets > 0
                ? Math.floor((BUDGETS[bande.cle] / sommeBudgets) * hauteurTuilesDisponible)
                : 0,
          }
          const onOuvrirBande = () => ouvrir({ sorte: 'focus', bande: bande.cle })

          return bande.cle === 'heros' ? (
            <BandeHeros
              key={bande.cle}
              bande={bande}
              budget={budget}
              playerId={playerId}
              onOuvrirBande={onOuvrirBande}
              onOuvrirCarte={ouvrirCarte}
            />
          ) : (
            <BandeMobile
              key={bande.cle}
              bande={bande}
              budget={budget}
              onOuvrirBande={onOuvrirBande}
              onOuvrirCarte={ouvrirCarte}
            />
          )
        })}
      </div>

      {bas ? <div className="pm-barre-action">{bas}</div> : null}

      {bandeEnFocus ? (
        <ZoneFocus bande={bandeEnFocus} onFermer={fermer} onOuvrirCarte={ouvrirCarte} />
      ) : null}
    </div>
  )
}
