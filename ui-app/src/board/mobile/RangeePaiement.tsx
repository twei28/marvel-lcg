import { useLayoutEffect, useRef, useState } from 'react'
import { t } from '../langue'
import type { UniteAffichee } from '../zones'
import { CarteMainPortrait } from './MainPortrait'

type Props = { cartes: UniteAffichee[]; nbMain: number }

export function RangeePaiement({ cartes, nbMain }: Props) {
  const rangee = useRef<HTMLDivElement>(null)
  const [debordeAGauche, setDebordeAGauche] = useState(false)
  const [debordeADroite, setDebordeADroite] = useState(false)
  const mesurer = () => {
    const el = rangee.current
    if (!el) return
    setDebordeAGauche(el.scrollLeft > 4)
    setDebordeADroite(el.scrollLeft + el.clientWidth < el.scrollWidth - 4)
  }
  useLayoutEffect(mesurer, [cartes.length])
  const nbTable = cartes.length - nbMain
  const carte = (unite: UniteAffichee) => (
    // Le type de la carte (« Événement », « Amélioration ») n'aide pas a payer : la pastille de type se tait, la carte gagne en hauteur.
    <CarteMainPortrait
      key={unite.cle}
      unite={{ ...unite, carte: { ...unite.carte, masquerType: true } }}
      choisie={false}
      onOuvrir={() => undefined}
      paiement
    />
  )
  return (
    <div className="feuille-paiement-rangee">
      <p className="feuille-paiement-compte">
        {nbTable > 0 ? `${t('Main')} ${nbMain} | ${t('Table')} ${nbTable}` : `${t('Main')} ${nbMain}`}
      </p>
      <div className="feuille-paiement-defilement">
        <div className="feuille-paiement-main" ref={rangee} onScroll={mesurer}>
          {cartes.slice(0, nbMain).map(carte)}
          {nbMain > 0 && nbTable > 0 ? <span className="feuille-paiement-separateur" aria-hidden="true" /> : null}
          {cartes.slice(nbMain).map(carte)}
        </div>
        {debordeAGauche ? <span className="feuille-paiement-degrade est-gauche" aria-hidden="true" /> : null}
        {debordeADroite ? <span className="feuille-paiement-degrade est-droite" aria-hidden="true" /> : null}
      </div>
    </div>
  )
}
