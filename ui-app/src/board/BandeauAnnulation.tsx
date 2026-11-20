// BandeauAnnulation.tsx — le retour visible d'une annulation (16/11/2026, « il faut que l'animation du undo soit hyper propre »).
//
// Le moteur met près d'une seconde à répondre (il remet toute la partie en place, puis recalcule la question) : sans retour, l'écran semblait
// figé, puis le monde changeait d'un coup. « Annulation… » dès le clic, « Coup annulé » quand le moteur confirme, puis plus rien. Aucun
// mouvement de cartes : le monde reste immobile, seul ce bandeau parle.
import type { ReactElement } from 'react'
import { t } from './langue'
import type { EtatBandeau } from './annulation'
import './annulation.css'

export function BandeauAnnulation({ etat }: { etat: EtatBandeau }): ReactElement | null {
  if (etat === 'aucun') return null
  return (
    <div className={`bandeau-annulation est-${etat}`} role="status" aria-live="polite">
      <span className="bandeau-annulation-ico" aria-hidden="true">
        ↶
      </span>
      {etat === 'attente' ? t('Annulation…') : t('Coup annulé')}
    </div>
  )
}
