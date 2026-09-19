// FinManuelle.tsx — déclarer la fin d'une partie manuelle (tâche 7).
//
// En mode manuel, le moteur ne conduit et ne surveille plus rien après la
// mise en place : plus aucune capacité ni effet de règle ne se déclenche, il
// ne peut donc plus constater qu'un vilain est vaincu ou qu'un complot a
// débordé. Personne d'autre que le joueur ne déclarera la fin de la partie —
// décision prise avec l'utilisateur : en manuel, c'est lui qui déclare tout.
//
// C'est le SEUL geste de tout le mode qui ne se rattrape pas : le Ctrl+Z du
// mode (`triche.annulerDernierGeste`) annule un geste sur la table, pas une
// fin de partie déjà déclarée au moteur. D'où les deux temps de cet écran :
// un choix, puis une confirmation distincte — jamais un déclenchement au
// premier clic.
import { useState } from 'react'
import { t } from '../langue'

export type FinManuelleProps = {
  /** Appelé seulement après confirmation. `true` = victoire, `false` = défaite. */
  onDeclarer: (gagne: boolean) => void
}

export function FinManuelle({ onDeclarer }: FinManuelleProps) {
  const [choix, setChoix] = useState<boolean | undefined>(undefined)

  if (choix === undefined) {
    return (
      <div className="fin-manuelle-choix">
        <p className="fin-manuelle-aide">
          {t('Le moteur ne surveille plus la table : c’est à toi de déclarer la fin.')}
        </p>
        <div className="fin-manuelle-boutons">
          <button type="button" className="fin-manuelle-victoire" onClick={() => setChoix(true)}>
            {t('Victoire')}
          </button>
          <button type="button" className="fin-manuelle-defaite" onClick={() => setChoix(false)}>
            {t('Défaite')}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="fin-manuelle-confirmation">
      <p className="fin-manuelle-avertissement">
        {choix
          ? t('Déclarer la victoire ?')
          : t('Déclarer la défaite ?')}{' '}
        {t('Cette décision ne se reprend pas : le Ctrl+Z ne la rattrape pas.')}
      </p>
      <div className="fin-manuelle-boutons">
        <button type="button" className="fin-manuelle-confirmer" onClick={() => onDeclarer(choix)}>
          {t('Confirmer')}
        </button>
        <button type="button" className="fin-manuelle-annuler" onClick={() => setChoix(undefined)}>
          {t('Annuler')}
        </button>
      </div>
    </div>
  )
}
