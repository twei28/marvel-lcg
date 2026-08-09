// Ta main, posée par-dessus le plateau.
//
// Ce sont des CARTES, pas une bande. La version précédente resserrait
// l'éventail jusqu'à 22 px d'écart pour tout faire tenir : sur des cartes de
// 92 px, il n'en dépassait qu'un quart, et six cartes ainsi empilées formaient
// une texture verticale continue où l'on ne distinguait plus rien. Même
// parfaitement cadrée, elle serait restée illisible.
//
// La règle est donc inversée : la taille et l'écart NE BOUGENT JAMAIS, et
// quand la main ne tient plus, on la balaie.
//
// Les gestes. L'appui long a d'abord été posé sur la petite carte : on
// demandait de jouer avant d'avoir pu lire. Il vit maintenant sur la carte
// AGRANDIE, ce qui donne la séquence réclamée — voir `useAppuiLong` :
//
//   appui n'importe où sur la main -> elle s'ouvre en entier ;
//   appui court sur une carte      -> elle sort du paquet, agrandie ;
//   appui maintenu sur la GRANDE   -> elle est jouée.

import { useState } from 'react'
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import { t } from '../langue'
import { useAppuiLong } from './useAppuiLong'
import './mobile.css'

export type MainEventailProps = {
  cartes: ScanCardProps[]
  /**
   * Un paiement est en cours : la main change de règle.
   *
   * On ne consulte plus, on dépense. Un simple appui envoie donc la carte au
   * paiement, et la main s'ouvre d'office puisqu'on ne peut pas choisir ce
   * qu'on ne voit pas.
   */
  modePaiement?: boolean
  onJouer: (carte: ScanCardProps) => void
}

export function MainEventail({ cartes, modePaiement, onJouer }: MainEventailProps) {
  const [levee, setLevee] = useState(false)
  const [choisie, setChoisie] = useState<string | undefined>(undefined)

  const ouverte = levee || !!modePaiement
  const carteEnAvant = cartes.find((carte) => carte.id === choisie)

  // Le maintien porte sur la carte mise en avant, jamais sur la vignette.
  const appui = useAppuiLong(
    carteEnAvant
      ? () => {
          onJouer(carteEnAvant)
          setChoisie(undefined)
        }
      : undefined
  )

  return (
    <>
      <div
        className={`main-eventail${ouverte ? ' est-levee' : ''}`}
        // Toute la surface ouvre la main : c'est ce qu'on vise, pas une poignée
        // de quelques pixels. Les cartes arrêtent l'événement pour elles.
        onClick={() => {
          if (modePaiement) return
          setLevee((etat) => !etat)
          setChoisie(undefined)
        }}
        role="button"
        tabIndex={0}
        data-tactile="main"
        aria-expanded={ouverte}
        aria-label={`${t('Main')} (${cartes.length})`}
      >
        <span className="main-poignee" aria-hidden="true">
          {t('Main')} ({cartes.length})
        </span>

        <div className="main-cartes">
          {cartes.map((carte) => (
            <span
              className="main-carte"
              key={carte.id}
              onClick={(evenement) => evenement.stopPropagation()}
            >
              {modePaiement ? (
                // On rend la main au moteur : `carte.onSelect` est l'action de
                // dépense posée par l'interaction. L'écraser ici rendrait les
                // cartes de la main indépensables.
                <ScanCard {...carte} />
              ) : (
                // Un appui simple ne fait qu'AGRANDIR. Rien n'est engagé tant
                // qu'on n'a pas maintenu le doigt sur la grande carte.
                <ScanCard
                  {...carte}
                  onSelect={() => setChoisie(choisie === carte.id ? undefined : carte.id)}
                />
              )}
            </span>
          ))}
        </div>
      </div>

      {/* La carte mise en avant est rendue HORS du défilement : à l'intérieur,
          elle serait coupée par le découpage horizontal, et une carte de bord
          sortirait de l'écran une fois agrandie. */}
      {carteEnAvant ? (
        <div className="main-avant" onClick={() => setChoisie(undefined)}>
          <span
            className="main-avant-carte"
            {...appui.gestes}
            onClick={(evenement) => evenement.stopPropagation()}
          >
            <ScanCard {...carteEnAvant} onSelect={undefined} />
          </span>
          {carteEnAvant.onSelect ? (
            <span className="main-avant-aide">{t('Maintenir pour jouer')}</span>
          ) : null}
        </div>
      ) : null}
    </>
  )
}
