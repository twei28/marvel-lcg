/**
 * Ce qu'on voit pendant qu'on glisse une carte : la carte soulevee sous le
 * pointeur, un trait qui la relie a ce qu'elle vise, et une etiquette qui dit
 * ce qui va se passer.
 *
 * ⚠ CETTE COUCHE NE CAPTE JAMAIS LE POINTEUR (`pointer-events: none` en CSS).
 * Sans cela, la carte fantome se trouverait en permanence sous le curseur et
 * `elementFromPoint` ne verrait plus jamais la table : on ne pourrait viser
 * personne.
 *
 * ⚠ ELLE NE TOUCHE PAS A LA MISE EN PAGE DU PLATEAU. Elle se pose par-dessus,
 * en coordonnees ecran, comme les autres couches (`CoucheCurseurs`,
 * `CoucheAnimations`).
 */
import type { CSSProperties } from 'react'
import type { ScanCardProps } from '../../components/ScanCard'
import { ScanCard } from '../../components/ScanCard'
import type { EtatGlisser } from './useGlisser'
import './glisser.css'

/** Le rectangle de la carte soulevee, telle qu'elle est posee sur la table. */
function rectangleDeLaSource(sourceId: number): DOMRect | undefined {
  const element = document.querySelector<HTMLElement>(`.scan-card[data-card-id="${sourceId}"]`)
  return element?.getBoundingClientRect()
}

export function CoucheGlisser({
  glisse,
  carte,
  libelle,
  refuse,
}: {
  glisse: EtatGlisser
  carte?: ScanCardProps
  libelle?: string
  /** La cible survolee refuse le lacher : le trait et l'etiquette virent au rouge. */
  refuse?: boolean
}) {
  const depart = rectangleDeLaSource(glisse.sourceId)
  return (
    <div className="couche-glisser" aria-hidden="true">
      {depart ? (
        <svg className="glisser-trait">
          <line
            className={refuse ? 'est-refuse' : undefined}
            x1={depart.left + depart.width / 2}
            y1={depart.top + depart.height / 2}
            x2={glisse.x}
            y2={glisse.y}
          />
          <circle
            className={refuse ? 'est-refuse' : undefined}
            cx={glisse.x}
            cy={glisse.y}
            r={5}
          />
        </svg>
      ) : null}

      {carte ? (
        <div
          className="glisser-carte"
          style={{ left: `${glisse.x}px`, top: `${glisse.y}px` }}
        >
          <ScanCard {...carte} state={undefined} onSelect={undefined} targetPulse={false} />
        </div>
      ) : null}

      {libelle ? (
        <div
          className={`glisser-etiquette${refuse ? ' est-refuse' : ''}`}
          style={{ left: `${glisse.x}px`, top: `${glisse.y}px` }}
        >
          {libelle}
        </div>
      ) : null}
    </div>
  )
}

/**
 * Le refus, apres un lacher rate : la raison, dans les mots du moteur, la ou
 * la carte a ete lachee. Elle s'efface toute seule ; c'est l'appelant qui tient
 * le minuteur, pour que la bulle reste un affichage sans memoire.
 */
export function BulleRefus({
  x,
  y,
  texte,
}: {
  x: number
  y: number
  texte: string
}) {
  return (
    <div className="couche-glisser">
      {/* Bornée à l'écran (lot 2 du 06/10/2026) : centrée sur le lâcher
          (`max-width: 300px`), elle sortait à moitié près d'un bord.
          Annoncée par un lecteur d'écran (lot 6) : la couche n'est plus
          `aria-hidden`, qui taisait son `role="status"`. */}
      <div
        className="glisser-refus"
        style={{ '--refus-x': `${x}px`, '--refus-y': `${y}px` } as CSSProperties}
        role="status"
      >
        {texte}
      </div>
    </div>
  )
}
