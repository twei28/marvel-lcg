// PisteDesPhases.tsx — la piste des phases du mode manuel (retour testeur du 09/11/2026).
//
// En manuel le moteur ne raconte plus rien : le joueur voyait un plateau sans repère. Cette
// bande, posée en haut du plateau comme le suivi de phase de DragnCards, montre TOUJOURS
// toutes les étapes : phase des héros, les cinq temps de la phase du méchant (menace,
// activation du méchant, activation des sbires, carte de rencontre, révélation), fin du
// round. On clique une étape pour s'y placer ; « Étape suivante » avance, et « Fin du round »
// ouvre le round suivant. Le compteur de round est tenu ici et gardé en sessionStorage.
// Rien n'est envoyé au moteur : ce n'est PAS le BandeauPhase du moteur.
//
// TÉLÉPHONE : la piste n'est PAS rendue (décision du 09/11/2026 : sur 390 px elle recouvrait le plateau, même repliée
// sur une ligne). Même critère que le plateau mobile (`useModeMobile`, seuil 767 px, ou `?mobile`) ; le bureau est
// inchangé.
import { useState } from 'react'
import { t } from '../langue'
import { useModeMobile } from '../mobile/useModeMobile'
import './PisteDesPhases.css'
import { ETAPES_MANUEL, etapeSuivante, etatInitial, type PisteEtat } from './phases-manuel'

export const CLE_PISTE_PHASES = 'marvel-board-piste-phases'

function relire(round: number | undefined): PisteEtat {
  try {
    const brut = window.sessionStorage.getItem(CLE_PISTE_PHASES)
    if (brut) {
      const lu = JSON.parse(brut) as Partial<PisteEtat>
      if (
        Number.isInteger(lu.round) &&
        Number.isInteger(lu.index) &&
        lu.index! >= 0 &&
        lu.index! < ETAPES_MANUEL.length
      ) {
        return { round: Math.max(1, lu.round!), index: lu.index! }
      }
    }
  } catch {
    /* repère non critique */
  }
  return etatInitial(round)
}

export function PisteDesPhases({ round }: { round?: number }) {
  const [etat, setEtat] = useState<PisteEtat>(() => relire(round))
  const { mode } = useModeMobile()

  function aller(suivant: PisteEtat) {
    setEtat(suivant)
    try {
      window.sessionStorage.setItem(CLE_PISTE_PHASES, JSON.stringify(suivant))
    } catch {
      /* repère non critique */
    }
  }

  const bouton = (i: number) => {
    const etape = ETAPES_MANUEL[i]
    return (
      <button
        key={etape.id}
        type="button"
        className={`piste-phases-etape${i === etat.index ? ' est-courante' : ''}`}
        aria-current={i === etat.index ? 'step' : undefined}
        title={t(etape.detail)}
        onClick={() => aller({ round: etat.round, index: i })}
      >
        {t(etape.libelle)}
      </button>
    )
  }
  if (mode === 'mobile') return null
  const debutMechant = ETAPES_MANUEL.findIndex((e) => e.phase === 'mechant')
  const finMechant = ETAPES_MANUEL.length - 2

  return (
    <div className="piste-phases" role="group" aria-label={t('Phases du round')}>
      <span className="piste-phases-round">{`${t('Round')} ${etat.round}`}</span>
      {bouton(0)}
      <span
        className={`piste-phases-mechant${etat.index >= debutMechant && etat.index <= finMechant ? ' est-courante' : ''}`}
      >
        <span className="piste-phases-titre">{t('Phase du méchant')}</span>
        {ETAPES_MANUEL.slice(debutMechant, finMechant + 1).map((_, k) => bouton(debutMechant + k))}
      </span>
      {bouton(ETAPES_MANUEL.length - 1)}
      <button
        type="button"
        className="piste-phases-suivant"
        onClick={() => aller(etapeSuivante(etat))}
      >
        {t('Étape suivante')} ›
      </button>
    </div>
  )
}
