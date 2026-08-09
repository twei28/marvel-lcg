// « Untel est déconnecté » — et que faire.
//
// Jusqu'ici, un joueur qui décrochait arrêtait la partie SANS UN MOT. Le moteur
// continue pourtant jusqu'à son tour — CheckSync rend la main dès qu'un client
// n'est plus connecté — puis il l'interroge, personne ne répond, et tout le
// monde regarde un écran figé, exactement comme une partie qui attend un joueur
// qui n'est pas encore arrivé. Deux causes opposées, un seul écran muet.
//
// Ce bandeau n'apparaît QUE quand le moteur interroge un siège abandonné : tant
// que c'est le tour de quelqu'un d'autre, la partie avance et il n'a rien à
// dire.

import { t } from './langue'

export type BandeauAbsentProps = {
  /** Nom du héros du siège abandonné, s'il est connu. */
  nom?: string
  /** Numéro affiché du joueur (index technique + 1). */
  numero: number
  /** Prendre la main sur ce héros. */
  onReprendre: () => void
}

export function BandeauAbsent({ nom, numero, onReprendre }: BandeauAbsentProps) {
  return (
    <div className="bandeau-absent" role="alert">
      <span className="bandeau-absent-texte">
        <b>{nom ?? `${t('Joueur')} ${numero}`}</b> {t('est déconnecté')}
      </span>
      <span className="bandeau-absent-detail">
        {t('Sa reprise dure jusqu’à la fin de son tour.')}
      </span>
      <button type="button" className="bandeau-absent-agir" onClick={onReprendre}>
        {t('Jouer pour lui')}
      </button>
    </div>
  )
}
