// L'annonce de la phase du mechant.
//
// Un bandeau rouge qui traverse l'ecran, avec un eclair. Il ne coute AUCUN
// clic et ne bloque rien : la premiere etape est deja derriere lui.
//
// Il se raccourcit a partir du round 4. Deux secondes de solennite valent pour
// l'ouverture d'une partie ; repetees douze fois, elles se subissent.

import { useEffect, useState } from 'react'
import { t } from './langue'

/** Rounds 1 a 3 : on prend le temps de l'effet. */
export const DUREE_LONGUE_MS = 2000
/** A partir du round 4 : moitie moins. */
export const DUREE_COURTE_MS = 1000
/** Round a partir duquel l'annonce se raccourcit. */
export const ROUND_COURT = 4

export function BandeauPhase({
  round,
  actif,
  onFini,
}: {
  round: number
  actif: boolean
  /**
   * Appele quand le bandeau a fini de jouer.
   *
   * ⚠ AJOUTE LE 14/09/2026 POUR LE MODE « Sur la table ». L'utilisateur : « d'abord
   * le bandeau, puis apres on montre la manigance. On attend que le bandeau soit
   * parti. » Les deux se superposaient : la premiere etape s'affichait pendant
   * que le bandeau passait encore.
   *
   * Le bandeau garde son minuteur - c'est lui qui sait combien de temps il dure,
   * et il dure moins longtemps passe un certain round. Il se contente de dire
   * quand il a fini.
   */
  onFini?: () => void
}) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (!actif) {
      setVisible(false)
      return
    }
    setVisible(true)
    const duree = round >= ROUND_COURT ? DUREE_COURTE_MS : DUREE_LONGUE_MS
    const minuteur = window.setTimeout(() => {
      setVisible(false)
      onFini?.()
    }, duree)
    // Nettoyage indispensable : sans lui, un changement de round pendant que
    // l'ancien minuteur court ferait apparaitre deux annonces superposees.
    return () => window.clearTimeout(minuteur)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- `onFini` ne doit
    // PAS re-armer le minuteur : une fonction recreee a chaque rendu du plateau
    // le remettrait a zero plus vite qu'il n'arrive a echeance, et le bandeau
    // ne partirait jamais.
  }, [actif, round])

  if (!visible) return null

  return (
    <div className="bandeau-phase" aria-hidden="true">
      <span className="bandeau-phase-eclair" />
      <p className="bandeau-phase-texte">
        {t('Phase du méchant')}
        <em>
          {t('Round')} {round}
        </em>
      </p>
    </div>
  )
}
