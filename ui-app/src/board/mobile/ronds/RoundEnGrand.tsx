// « ROUND 3 » EN GRAND, une seconde, au debut d'un nouveau round (decision Q27, 24/10/2026). Il ne s'allume qu'au CHANGEMENT de
// round (jamais au chargement de la page ni au round 1), ne capte aucun toucher, et se coupe si le systeme demande moins
// d'animations (le numero reste alors dans le bandeau du haut).
import { useEffect, useRef, useState, type ReactElement } from 'react'
import { t } from '../../langue'

export const DUREE_ROUND_EN_GRAND_MS = 1300

export function RoundEnGrand({ round }: { round: number | undefined }): ReactElement | null {
  const avant = useRef(round)
  const [vu, setVu] = useState<number | null>(null)
  useEffect(() => {
    if (round === undefined) return
    const precedent = avant.current
    avant.current = round
    // Jamais au chargement ni au round 1 : le grand « ROUND » annonce un round qui COMMENCE apres le premier.
    if (precedent === undefined || round <= precedent || round < 2) return
    setVu(round)
    const fin = window.setTimeout(() => setVu(null), DUREE_ROUND_EN_GRAND_MS)
    return () => window.clearTimeout(fin)
  }, [round])
  if (vu === null) return null
  return (
    <div className="round-en-grand" aria-hidden="true">
      <b>
        {t('ROUND')} {vu}
      </b>
      <span>{t('À TOI DE JOUER')}</span>
    </div>
  )
}
