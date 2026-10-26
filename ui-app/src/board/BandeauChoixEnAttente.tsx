// Fenetre de choix fermee SANS annuler (telephone, demande du 26/10/2026) : un bandeau discret dit que le choix attend et
// propose de rouvrir. Il ne couvre pas la table : une ligne en haut, cible tactile de 44 px au moins.
import type { ReactElement } from 'react'
import { t } from './langue'
import './choix-en-attente.css'

export function BandeauChoixEnAttente({ titre, onRouvrir }: { titre: string; onRouvrir: () => void }): ReactElement {
  return (
    <div className="plateau-choix-attente" role="status">
      <span className="plateau-choix-attente-texte">
        <strong>{t('Choisis une carte')}</strong>
        {titre ? <span> · {titre}</span> : null}
      </span>
      <button type="button" className="plateau-choix-attente-rouvrir" onClick={onRouvrir}>
        {t('Rouvrir')}
      </button>
    </div>
  )
}
