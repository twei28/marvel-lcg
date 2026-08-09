// Une carte posée, ouverte en grand — avec ses actions.
//
// Le médaillon ne porte volontairement ni nom ni texte de règles : c'est ce qui
// le rend lisible à 56 px. Il faut donc un moyen de LIRE la carte, sinon le
// plateau devient un jeu de devinettes. C'était la décision 5 de la refonte, et
// elle manquait : toucher un médaillon ne l'agrandissait pas.
//
// Le bouton d'action n'apparaît que si le moteur en propose une (`onSelect`
// posé par l'interaction). Une carte qu'on ne peut qu'ouvrir se referme d'un
// appui à l'extérieur.

import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import { t } from '../langue'
import { useAppuiLong } from './useAppuiLong'
import './medaillon.css'

export function CarteOuverte({
  carte,
  onFermer,
}: {
  carte: ScanCardProps
  onFermer: () => void
}) {
  // Même geste que dans la main : on ouvre le médaillon pour LIRE, puis on
  // maintient le doigt sur la grande carte pour agir. Le bouton du dessous
  // reste : c'est lui qui rend l'action découvrable la première fois.
  const appui = useAppuiLong(
    carte.onSelect
      ? () => {
          carte.onSelect?.()
          onFermer()
        }
      : undefined
  )

  return (
    <div className="carte-ouverte-voile" onPointerDown={onFermer}>
      <section
        className="carte-ouverte"
        role="dialog"
        aria-label={carte.name}
        onPointerDown={(evenement) => evenement.stopPropagation()}
      >
        <div className="carte-ouverte-scan" {...appui.gestes}>
          {/* Sans onSelect, ScanCard ne rend pas de bouton : la carte est ici
              une image à lire, l'action vit dans le maintien et dans le
              bandeau du dessous. */}
          <ScanCard {...carte} onSelect={undefined} />
        </div>

        {carte.onSelect ? (
          <span className="carte-ouverte-aide">{t('Maintenir pour utiliser')}</span>
        ) : null}

        <div className="carte-ouverte-actions">
          {carte.onSelect ? (
            <button
              type="button"
              className="carte-ouverte-agir"
              onClick={() => {
                carte.onSelect?.()
                onFermer()
              }}
            >
              {t('Utiliser cette carte')}
            </button>
          ) : null}
          <button type="button" className="carte-ouverte-fermer" onClick={onFermer}>
            {t('Fermer')}
          </button>
        </div>
      </section>
    </div>
  )
}
