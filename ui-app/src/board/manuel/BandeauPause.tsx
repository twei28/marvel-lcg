// BandeauPause.tsx — la pause manuelle EN COURS DE PARTIE (tâche 3).
//
// Une table ordinaire (mode_manuel = faux) qui rencontre un bug se met en
// PAUSE (route `POST /manuel_pause`, `triche.basculerPause`) : le moteur se
// tait le temps qu'on corrige à la main, exactement comme le fait le mode
// manuel DÉCLARÉ (`leMoteurSeTait`), mais sans en avoir la nature — voir
// `mode.ts`, `estEnPause`, pour la distinction.
//
// ⚠ CE BANDEAU EST EXEMPTÉ DU MASQUAGE (ruling du plan, 20/09/2026) : il est
// le SEUL moyen de reprendre la partie. Le masquer avec le reste des couches
// du moteur (bandeau de phase, assistant, barre d'actions...) rendrait la
// pause définitive. `board.tsx` doit donc le monter INCONDITIONNELLEMENT,
// jamais derrière la même garde que `bh-fin-tour` ou consorts.
//
// Sur une table EN LIGNE, chaque joueur voit sa propre partie s'arrêter sans
// prévenir : sans dire QUI a posé la pause et DEPUIS QUAND, les autres
// croient à une panne. C'est le cœur de la tâche — voir `enPause.par` /
// `enPause.depuis`, posés côté moteur par `World.BasculerPauseManuelle`
// (`Scene.pause_par` / `Scene.pause_a`, effacés à la reprise).
import { t } from '../langue'

/** L'état de la pause EN COURS, tel que la trame le publie. */
export type InfoPause = {
  /** Faux hors pause : le bandeau ne s'affiche alors pas. */
  actif: boolean
  /** Pseudo de qui a posé la pause. Vide = aucun pseudo n'a voyagé. */
  par: string
  /** Horodatage tel que le moteur l'a formaté (`Scene.pause_a`). Vide = tu. */
  depuis: string
}

export type BandeauPauseProps = {
  enPause: InfoPause
  /** Reprend la partie (`POST /manuel_pause` avec `actif: false`). */
  onReprendre: () => void
  /**
   * Passe la question fautive du moteur (tâche 5 du plan) : le bouton et son
   * branchement existent ici, mais le geste réel — route dédiée, lecture du
   * drapeau d'annulation que porte la question courante — arrive à la tâche
   * 5, qui modifie ce fichier. Aucun comportement n'est inventé ici au-delà
   * de « appeler ce qu'on m'a donné ».
   */
  onPasser: () => void
}

export function BandeauPause({ enPause, onReprendre, onPasser }: BandeauPauseProps) {
  if (!enPause.actif) return null

  const qui = enPause.par || t('Quelqu’un')

  return (
    <div className="bandeau-pause" role="alert">
      <span className="bandeau-pause-titre">
        <span aria-hidden="true">⏸</span> {t('Partie en pause')}
      </span>
      <span className="bandeau-pause-texte">
        {qui} {t('a mis la partie en pause')}
        {enPause.depuis ? ` ${t('depuis')} ${enPause.depuis}` : ''}
      </span>
      <span className="bandeau-pause-boutons">
        <button type="button" className="bandeau-pause-passer" onClick={onPasser}>
          {t('Passer la question')}
        </button>
        <button type="button" className="bandeau-pause-reprendre" onClick={onReprendre}>
          {t('Reprendre')}
        </button>
      </span>
    </div>
  )
}
