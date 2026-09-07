// « Tourne ton telephone » : le voile qui couvre le plateau en portrait.
//
// Le plateau paysage n'a PAS de rendu portrait (spec du 07/09/2026, §3). Ce
// voile ne demonte rien : la partie continue dessous, la connexion au moteur
// aussi, et une question posee pendant la rotation est toujours la au retour.

import { t } from '../langue'
import './paysage.css'

export function EcranPortrait() {
  return (
    <div className="ecran-portrait" role="dialog" aria-modal="true" aria-label={t('Tourne ton téléphone')}>
      <span className="ecran-portrait-icone" aria-hidden="true" />
      <p>
        <strong>{t('Tourne ton téléphone')}</strong>
        <br />
        {t('Le plateau se joue en paysage.')}
      </p>
    </div>
  )
}
