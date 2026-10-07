// Ce qu'on voit pendant qu'on range une carte (Alt + glisser) : la carte
// tenue sous le pointeur et un trait net entre les deux cartes ou elle se
// posera, par-dessus la carte tenue. Rien ne capte le pointeur.
import type { ScanCardProps } from '../../components/ScanCard'
import { ScanCard } from '../../components/ScanCard'
import type { GesteOrdre } from './useReordonner'
import './ordre.css'

export function CoucheOrdre({ geste, carte }: { geste: GesteOrdre; carte?: ScanCardProps }) {
  const { repere } = geste
  return (
    <div className="couche-ordre" aria-hidden="true">
      {carte ? (
        <div className="ordre-carte" style={{ left: `${geste.x}px`, top: `${geste.y}px` }}>
          <ScanCard {...carte} state={undefined} onSelect={undefined} targetPulse={false} />
        </div>
      ) : null}
      {repere ? (
        <div
          className="ordre-repere"
          data-pile={repere.pile ? '' : undefined}
          style={{ left: `${repere.gauche}px`, top: `${repere.haut}px`, height: `${repere.hauteur}px` }}
        />
      ) : null}
    </div>
  )
}
