// « Remets ton telephone droit » : le verrou portrait (reglage du telephone,
// zone 3) quand le navigateur refuse de figer l'orientation lui-meme (hors
// plein ecran, iOS). Il couvre la table tant que le telephone reste couche ;
// la partie continue dessous, rien n'est perdu.
import type { ReactElement } from 'react'
import { t } from '../langue'
import './telephone.css'

export function EcranTourne(): ReactElement {
  return (
    <div className="ecran-tourne" role="alert">
      <span className="ecran-tourne-icone" aria-hidden="true">
        ⟲
      </span>
      <strong>{t('Remets ton téléphone droit')}</strong>
      <span>{t('Le verrou portrait est actif (Réglages, Apparence).')}</span>
    </div>
  )
}
