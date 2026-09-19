// FinManuelle.tsx — déclarer la fin d'une partie manuelle (tâche 7).
//
// En mode manuel, le moteur ne conduit et ne surveille plus rien après la
// mise en place : plus aucune capacité ni effet de règle ne se déclenche, il
// ne peut donc plus constater qu'un vilain est vaincu ou qu'un complot a
// débordé. Personne d'autre que le joueur ne déclarera la fin de la partie —
// décision prise avec l'utilisateur : en manuel, c'est lui qui déclare tout.
//
// ⚠ CORRECTION (ronde 1) : la version précédente affirmait que ce geste ne
// se rattrape pas. C'ÉTAIT FAUX, et le relecteur a tracé le chemin complet
// pour le prouver : le Ctrl+Z du mode (`triche.annulerDernierGeste`) rejoue
// la partie moins son dernier geste, fin de partie déclarée comprise — un
// nouveau monde se construit, les gestes se rejouent amputés de la fin, et
// la partie manuelle reprend. Le serveur ne refuse rien, l'état obtenu est
// sain. Décider l'inverse (rendre CE geste-là irréversible) demanderait un
// cas particulier dans le moteur, pour retirer au joueur une porte de
// sortie qui lui rend service — une fin déclarée par erreur qu'on peut
// défaire est un filet, pas un défaut.
//
// Les DEUX temps de cet écran (choix, puis confirmation) restent donc,
// mais pour une raison différente : pas pour protéger d'un geste
// irréversible, mais pour ne pas déclencher par mégarde un rejeu complet
// de la partie — une reconstruction moteur d'une à deux secondes
// (mise en place puis rejeu de tous les gestes), pas rien.
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

  // Cette confirmation ne protège PLUS d'un geste irréversible (voir la
  // correction en tête de fichier) : elle évite de déclencher par mégarde
  // le rejeu complet que fait le Ctrl+Z pour revenir en arrière — une
  // reconstruction moteur d'une à deux secondes, pas un clic anodin.
  return (
    <div className="fin-manuelle-confirmation">
      <p className="fin-manuelle-avertissement">
        {choix
          ? t('Déclarer la victoire ?')
          : t('Déclarer la défaite ?')}{' '}
        {t('Tu pourras revenir en arrière avec Ctrl+Z si tu te trompes.')}
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
