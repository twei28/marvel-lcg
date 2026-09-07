// La barre du pas à pas : où on en est de la phase, et de quoi reprendre la main.
//
// ⚠ DÉBRANCHÉE, à la demande de l'utilisateur : ce composant n'est monté nulle
// part. Le mode d'emploi du remontage est dans board.tsx, au commentaire qui
// explique pourquoi (double emploi avec le cartouche du déroulé) et quelles
// deux props n'ont plus de contrepartie dans le moteur.
//
// Elle ne capte PAS les clics elle-même, hors ses propres boutons : l'écoute se
// fait sur la fenêtre, en capture. Une nappe transparente plein écran aurait
// mangé le survol des cartes — et pendant la phase du méchant, lire une carte
// au survol est justement ce qu'on veut pouvoir faire.
//
// Le clic « passer à la suite » est donc global, mais il ignore les clics sur
// un bouton : sinon « Tout passer » avancerait d'une étape avant de sauter la
// phase, et le geste compterait double.

import { useEffect } from 'react'
import { t } from './langue'

/**
 * Les points de la carte de référence, tels que le moteur nomme ses phases.
 * Mêmes clés que RecapPhaseMechant : le pas à pas et le bilan doivent raconter
 * la même histoire, découpée pareil.
 */
const POINTS: Record<string, { numero: number; titre: string }> = {
  'Main Scheme Place Threat': { numero: 1, titre: 'Menace sur la manigance' },
  'Enemy Activation': { numero: 2, titre: 'Activations' },
  'Deal Encounter Cards': { numero: 3, titre: 'Cartes distribuées' },
  'Reveal Encounter Cards': { numero: 4, titre: 'Cartes révélées' },
}

export function pointDeLaPhase(phase: string | undefined): { numero: number; titre: string } | undefined {
  return phase ? POINTS[phase] : undefined
}

export function CouchePasAPas({
  actif,
  enPause,
  phase,
  onAvancer,
  onBasculerPause,
  onToutPasser,
}: {
  actif: boolean
  enPause: boolean
  phase: string | undefined
  onAvancer: () => void
  onBasculerPause: () => void
  onToutPasser: () => void
}) {
  // Clic n'importe où = l'étape a été lue, on passe à la suivante.
  useEffect(() => {
    if (!actif) return
    const surClic = (e: MouseEvent) => {
      const cible = e.target as HTMLElement | null
      if (cible?.closest('button, a, input, select, label')) return
      onAvancer()
    }
    window.addEventListener('click', surClic, true)
    return () => window.removeEventListener('click', surClic, true)
  }, [actif, onAvancer])

  if (!actif) return null
  const point = pointDeLaPhase(phase)

  return (
    <div className="pas-a-pas-barre" role="status" aria-live="polite">
      {point ? (
        <span className="pap-point">
          <b>{point.numero}.</b> {t(point.titre)}
        </span>
      ) : null}
      <span className="pap-aide">{enPause ? t('En pause') : t('Clic : suite · Espace : pause')}</span>
      <button type="button" className="pap-bouton" onClick={onBasculerPause}>
        {enPause ? t('Reprendre') : t('Pause')}
      </button>
      <button type="button" className="pap-bouton" onClick={onToutPasser}>
        {t('Tout passer')}
      </button>
    </div>
  )
}
