// La carte ouverte EN GRAND, au milieu de l'ecran : le geste de lecture du
// telephone (tap). Avec ses attachees et ses statuts en dessous (spec du
// 12/09/2026 : « lisible, avec ses attachements ») : un tap sur l'une d'elles
// l'ouvre a son tour.
//
// Trois sorties sans rien engager : tap sur le voile, Fermer, Retour Android
// (`.carte-ouverte-voile` est dans FERMABLES). L'action du moteur, quand il
// y en a une, vit dans le maintien et dans le bouton du dessous.
import { ScanCard, type ScanCardProps } from '../../components/ScanCard'
import { t } from '../langue'
import { useAppuiLong } from './useAppuiLong'
import './portrait.css'

export function CarteOuverte({
  carte,
  attachees = [],
  onOuvrirAttachee,
  onFermer,
}: {
  carte: ScanCardProps
  attachees?: ScanCardProps[]
  onOuvrirAttachee?: (carte: ScanCardProps) => void
  onFermer: () => void
}) {
  const appui = useAppuiLong(
    carte.onSelect
      ? () => {
          carte.onSelect?.()
          onFermer()
        }
      : undefined
  )
  // Les statuts (Tough, Stunned...) d'abord, en petit, puis les ameliorations.
  const statuts = attachees.filter((a) => a.kind === 'status')
  const ameliorations = attachees.filter((a) => a.kind !== 'status')

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

        {attachees.length > 0 ? (
          <div className="carte-ouverte-attachees" aria-label={t('Attachées')}>
            {[...statuts, ...ameliorations].map((attachee) => (
              <button
                type="button"
                className={`carte-ouverte-attachee${attachee.kind === 'status' ? ' est-statut' : ''}`}
                key={attachee.id}
                data-tactile="attachee"
                aria-label={attachee.name}
                onClick={() => onOuvrirAttachee?.(attachee)}
              >
                <ScanCard {...attachee} onSelect={undefined} highlight={false} />
              </button>
            ))}
          </div>
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
