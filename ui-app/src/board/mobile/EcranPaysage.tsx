// « Remets ton telephone droit » : le voile qui couvre le plateau en paysage.
//
// C'est l'exact inverse d'EcranPortrait, qui disait le contraire jusqu'au
// 11/09/2026. Le telephone joue desormais DEBOUT : c'est ainsi qu'on le tient,
// et la hauteur est ce qui permet au panneau de decision de vivre en bas.
//
// Comme son predecesseur, ce voile ne demonte rien : la partie continue
// dessous, la connexion au moteur aussi, et une question posee pendant la
// rotation est toujours la au retour.
import { t } from '../langue'
import './portrait.css'

export function EcranPaysage() {
  return (
    <div
      className="ecran-paysage"
      role="dialog"
      aria-modal="true"
      aria-label={t('Remets ton téléphone droit')}
    >
      <span className="ecran-paysage-icone" aria-hidden="true" />
      <p>
        <strong>{t('Remets ton téléphone droit')}</strong>
        <br />
        {t('Le plateau se joue debout.')}
      </p>
    </div>
  )
}
