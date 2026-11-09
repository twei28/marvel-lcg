// PisteDesPhases.tsx — la piste des phases du mode manuel (retour testeur du 09/11/2026).
//
// En manuel le moteur ne raconte plus rien : le joueur voyait un plateau sans repère. Cette
// bande, posée en haut du plateau comme le suivi de phase de DragnCards, montre TOUJOURS
// toutes les étapes : phase des héros, les cinq temps de la phase du méchant (menace,
// activation du méchant, activation des sbires, carte de rencontre, révélation), fin du
// round. On clique une étape pour s'y placer ; « Étape suivante » avance, et « Fin du round »
// ouvre le round suivant. Le compteur de round est tenu ici et gardé en sessionStorage.
// Rien n'est envoyé au moteur : ce n'est PAS le BandeauPhase du moteur.
import { useEffect, useRef, useState } from 'react'
import { t } from '../langue'
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
  const piste = useRef<HTMLDivElement>(null)

  // Sur telephone la piste defile (voir le CSS) : l'etape courante est recentree pour ne jamais rester hors de vue.
  // Sans debordement (bureau), scrollLeft ne bouge pas : aucun effet.
  useEffect(() => {
    const conteneur = piste.current
    const courante = conteneur?.querySelector<HTMLElement>('.piste-phases-etape.est-courante')
    if (!conteneur || !courante || conteneur.scrollWidth <= conteneur.clientWidth) return
    conteneur.scrollLeft = courante.offsetLeft - (conteneur.clientWidth - courante.offsetWidth) / 2
  }, [etat.index])

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
  const debutMechant = ETAPES_MANUEL.findIndex((e) => e.phase === 'mechant')
  const finMechant = ETAPES_MANUEL.length - 2

  return (
    <div ref={piste} className="piste-phases" role="group" aria-label={t('Phases du round')}>
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
