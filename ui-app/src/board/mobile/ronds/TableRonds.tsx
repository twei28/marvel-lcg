// La TABLE en ronds : trois rangees de deux zones (voir repartir-ronds.ts), a la place des quatre bandes de cartes.
// Elle ne porte aucune logique de jeu : les ronds appellent `ouvrirCarte` / `agir` comme les bandes (PlateauPortrait).
import { useEffect, useMemo, useRef, useState, type ReactElement, type ReactNode } from 'react'
import { t } from '../../langue'
import type { BandesPortrait } from '../bandes-portrait'
import { Rond, type DecorRonds } from './Rond'
import type { UniteAffichee } from '../../zones'
import { repartirEnRonds, type TitresRonds, type ZoneRonds } from './repartir-ronds'
import './ronds.css'

/** Les ronds qui viennent de quitter une zone de combat (sbire vaincu, allie vaincu) : fantomes grises « VAINCU » un instant (Q44). */
function useVaincus(zone: ZoneRonds): UniteAffichee[] {
  const avant = useRef<UniteAffichee[]>(zone.unites)
  const [fantomes, setFantomes] = useState<UniteAffichee[]>([])
  useEffect(() => {
    const encore = new Set(zone.unites.map((u) => u.cle))
    const partis = avant.current.filter((u) => !encore.has(u.cle))
    avant.current = zone.unites
    if (partis.length === 0 || (zone.cle !== 'sbires' && zone.cle !== 'allies')) return
    setFantomes((f) => [...f, ...partis])
    const fin = window.setTimeout(() => setFantomes((f) => f.filter((x) => !partis.includes(x))), 1100)
    return () => window.clearTimeout(fin)
  }, [zone.unites, zone.cle])
  return fantomes
}

function Zone({ zone, decor, onglets }: { zone: ZoneRonds; decor: DecorRonds; onglets?: ReactNode }): ReactElement {
  const vaincus = useVaincus(zone)
  return (
    <section
      className={`ronds-zone ronds-zone-${zone.cle}${zone.unites.length === 0 && vaincus.length === 0 ? ' est-vide' : ''}`}
      data-zone={zone.cle}
      aria-label={zone.titre}
    >
      <h2 className="ronds-titre">
        {zone.titre}
        {onglets}
      </h2>
      <div className="ronds-liste">
        {zone.unites.map((unite) => (
          <Rond key={unite.cle} unite={unite} zone={zone.cle} decor={decor} />
        ))}
        {vaincus.map((unite) => (
          <Rond key={`vaincu-${unite.cle}`} unite={unite} zone={zone.cle} decor={decor} vaincu />
        ))}
      </div>
    </section>
  )
}

export function TableRonds({
  bandes,
  decor,
  onglets,
}: {
  bandes: BandesPortrait
  decor: DecorRonds
  /** Les onglets du multijoueur, dans l'en-tete de la zone du heros. */
  onglets?: ReactNode
}): ReactElement {
  const titres: TitresRonds = {
    vilain: t('Méchant'),
    manigances: t('Manigances'),
    allies: t('Alliés'),
    sbires: t('Sbires'),
    heros: t('Héros'),
    enJeu: t('Cartes en jeu'),
  }
  const rangees = useMemo(() => repartirEnRonds(bandes, titres), [bandes]) // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div className="table-ronds">
      {rangees.map((rangee) => (
        <div key={rangee.cle} className={`ronds-rangee ${rangee.cle}`}>
          <Zone zone={rangee.gauche} decor={decor} onglets={rangee.cle === 'rangee-heros' ? onglets : undefined} />
          <span className="ronds-separateur" aria-hidden="true" />
          <Zone zone={rangee.droite} decor={decor} />
        </div>
      ))}
    </div>
  )
}
