// « Remets ton telephone droit » : le verrou portrait (reglage du telephone,
// zone 3) quand le navigateur refuse de figer l'orientation lui-meme (hors
// plein ecran, iOS). Il couvre la table tant que le telephone reste couche ;
// la partie continue dessous, rien n'est perdu.
import type { ReactElement } from 'react'
import { t } from '../langue'
import './telephone.css'

// La tablette s'en sert aussi, dans l'autre sens (24/10/2026, decision 0) :
// le plateau PC se joue en paysage, la tablette debout est couverte.
export function EcranTourne({ tablette = false }: { tablette?: boolean }): ReactElement {
  return (
    <div className="ecran-tourne" role="alert">
      <span className="ecran-tourne-icone" aria-hidden="true">
        ⟲
      </span>
      <strong>{tablette ? t('Tourne ta tablette') : t('Remets ton téléphone droit')}</strong>
      <span>{tablette ? t('Le plateau se joue en paysage.') : t('Le verrou portrait est actif (Réglages, Apparence).')}</span>
    </div>
  )
}
