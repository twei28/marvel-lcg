// Une rangee du plateau paysage : son etiquette, ses cartes, ses piles.
//
// Les cartes DEFILENT horizontalement quand elles ne tiennent plus, avec
// accroche carte par carte. Rien n'est condense ni replie : douze sbires font
// douze cartes, et le voile « +N » au bord droit dit combien sont hors champ.
// Les piles (deck, defausse) sont epinglees a droite, hors du defilement.
//
// Pendant un ciblage, la rangee ramene sa premiere cible dans le champ : on ne
// doit pas avoir a chercher ce que le moteur demande de choisir.

import { Fragment, useCallback, useEffect, useRef, useState } from 'react'
import type { CardEffectDelta, ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import { t } from '../langue'
import { CartePosee } from './CartePosee'
import { PilesEpinglees } from './PilesEpinglees'
import { mesurerHorsChamp } from './hors-champ'
import type { CleRangee } from './rangees'
import './paysage.css'

export type GroupeRangee = {
  cle: string
  unites: UniteAffichee[]
  /** Le groupe du heros ACTIF (solo a deux heros) : trait de couleur dessous. */
  actif?: boolean
}

export type RangeeCartesProps = {
  cle: CleRangee
  titre: string
  groupes: GroupeRangee[]
  piles: UniteAffichee[]
  /** Nombre de cibles legales ici pendant un ciblage. */
  cibles?: number
  /** Variations de compteurs en cours, par identifiant de carte. */
  effets?: Map<number, CardEffectDelta>
  onOuvrirCarte: (carte: ScanCardProps) => void
  onOuvrirPile: (titre: string, cartes: ScanCardProps[]) => void
}

export function RangeeCartes({
  cle,
  titre,
  groupes,
  piles,
  cibles,
  effets,
  onOuvrirCarte,
  onOuvrirPile,
}: RangeeCartesProps) {
  const defilement = useRef<HTMLDivElement>(null)
  const [horsChamp, setHorsChamp] = useState(0)
  const vide = groupes.every((groupe) => groupe.unites.length === 0)

  const mesurer = useCallback(() => {
    if (defilement.current) setHorsChamp(mesurerHorsChamp(defilement.current))
  }, [])

  // Remesure quand les cartes changent, et quand la fenetre change de taille
  // (rotation, barre du navigateur). ResizeObserver n'existe pas sous jsdom.
  useEffect(() => {
    mesurer()
    const element = defilement.current
    if (!element || typeof ResizeObserver === 'undefined') return
    const observateur = new ResizeObserver(mesurer)
    observateur.observe(element)
    return () => observateur.disconnect()
  }, [mesurer, groupes])

  // Un ciblage commence : la premiere cible revient dans le champ.
  useEffect(() => {
    if (!cibles || !defilement.current) return
    const cible = defilement.current.querySelector<HTMLElement>('.state-targetable')?.closest<HTMLElement>('.carte-posee')
    if (cible && typeof cible.scrollIntoView === 'function') {
      cible.scrollIntoView({ inline: 'nearest', block: 'nearest', behavior: 'smooth' })
    }
  }, [cibles])

  const avancer = () => {
    const element = defilement.current
    if (element) element.scrollBy({ left: element.clientWidth, behavior: 'smooth' })
  }

  return (
    <section className={`rangee-cartes rangee-${cle}`} role="region" aria-label={titre}>
      <div className="rangee-cartes-titre">
        <span className="rangee-cartes-nom">{titre}</span>
        {cibles ? (
          <span className="rangee-cartes-cibles" aria-label={`${cibles} ${t('cibles ici')}`}>
            {cibles}
          </span>
        ) : null}
      </div>
      <div className="rangee-cartes-corps">
        <div className="rangee-cartes-defilement" ref={defilement} onScroll={mesurer}>
          {vide ? (
            <span className="rangee-cartes-vide">{t('Vide')}</span>
          ) : (
            groupes.map((groupe, index) => (
              <Fragment key={groupe.cle}>
                {index > 0 ? <span className="rangee-cartes-separateur" role="separator" /> : null}
                <div className={`rangee-cartes-groupe${groupe.actif ? ' est-actif' : ''}`}>
                  {groupe.unites.map((unite) => (
                    <CartePosee
                      key={unite.cle}
                      unite={unite}
                      effet={effets?.get(Number(unite.carte.id))}
                      onOuvrir={onOuvrirCarte}
                    />
                  ))}
                </div>
              </Fragment>
            ))
          )}
        </div>
        {horsChamp > 0 ? (
          <button
            type="button"
            className="rangee-cartes-suite"
            data-tactile="suite"
            aria-label={`${horsChamp} ${t('cartes hors champ')}`}
            onClick={avancer}
          >
            +{horsChamp}
          </button>
        ) : null}
        {piles.length > 0 ? <PilesEpinglees piles={piles} onOuvrirPile={onOuvrirPile} /> : null}
      </div>
    </section>
  )
}
