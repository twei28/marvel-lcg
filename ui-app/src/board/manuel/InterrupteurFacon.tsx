// InterrupteurFacon.tsx — « Auto / Manuel », toujours dans la barre du haut.
//
// Remplace l'ancien bouton « Mettre en pause » : on peut passer en manuel à
// tout moment (un bug dans une automatisation, ou simplement l'envie de
// jouer à la main) et revenir en Auto quand on veut.
//
// Deux cas pour revenir en Auto, selon comment la partie a commencé :
//  - commencée en AUTO : le moteur reprend exactement à sa question
//    (`basculerPause(false)`, `onReprendre`) ;
//  - commencée en MANUEL (le moteur n'a jamais posé de question) : il faut dire
//    où on en est, la fenêtre `ChoixReprise` s'ouvre et `onReprendreA` part avec
//    la phase choisie.
import { useState } from 'react'
import { t } from '../langue'
import type { PhaseDeReprise, ResultatPasser } from '../triche'
import { transformDecalage, useGlisserPanneau } from '../placement/useGlisserPanneau'

export type InterrupteurFaconProps = {
  /** Le moteur s'est tu (`leMoteurSeTait`). */
  manuel: boolean
  /** La partie a commencé en manuel et n'a jamais été rendue au moteur. */
  commenceEnManuel: boolean
  /** Spectateur : on voit l'état, on ne le change pas. */
  lectureSeule?: boolean
  /** Passe la table en manuel. Rend faux si le moteur a refusé. */
  onManuel: () => Promise<boolean>
  /** Reprend à la question du moteur (partie commencée en auto). Rend faux si refusé. */
  onReprendre: () => Promise<boolean>
  /** Reprend à la phase choisie (partie commencée en manuel). */
  onReprendreA: (phase: PhaseDeReprise) => Promise<ResultatPasser>
}

const CHOIX: { phase: PhaseDeReprise; titre: string; detail: string }[] = [
  { phase: 'heros', titre: 'Au début de la phase héros', detail: 'Les héros jouent, puis le méchant' },
  { phase: 'mechant', titre: 'Au début de la phase méchant', detail: 'Les héros ont fini leur tour' },
  { phase: 'tour', titre: 'Au début d’un nouveau tour', detail: 'Le tour reprend de zéro, comme un tour normal' },
]

export function InterrupteurFacon({
  manuel,
  commenceEnManuel,
  lectureSeule = false,
  onManuel,
  onReprendre,
  onReprendreA,
}: InterrupteurFaconProps) {
  const [fenetre, setFenetre] = useState(false)
  const [refus, setRefus] = useState<string | undefined>(undefined)
  const { decalage, gestes } = useGlisserPanneau('choix-reprise')

  async function passerManuel(): Promise<void> {
    setRefus(undefined)
    if (!(await onManuel())) setRefus(t('Le moteur a refusé de passer en manuel'))
  }

  async function passerAuto(): Promise<void> {
    setRefus(undefined)
    if (commenceEnManuel) {
      setFenetre(true)
      return
    }
    if (!(await onReprendre())) setRefus(t('Le moteur a refusé de reprendre'))
  }

  async function choisir(phase: PhaseDeReprise): Promise<void> {
    setRefus(undefined)
    const resultat = await onReprendreA(phase)
    if (resultat.ok) setFenetre(false)
    else setRefus(t('Le moteur a refusé de reprendre'))
  }

  // Avant la fin de la mise en place d'une partie commencée en manuel, le moteur
  // n'est pas encore tu : rien à basculer, on grise « Manuel ».
  const miseEnPlace = commenceEnManuel && !manuel

  return (
    <span className="bh-facon" role="group" aria-label={t('Façon de jouer')}>
      <button
        type="button"
        className={`bh-facon-choix${manuel ? '' : ' est-actif'}`}
        aria-pressed={!manuel}
        aria-label={t('Mode automatique')}
        disabled={lectureSeule}
        title={t('Le moteur applique les règles et pose les questions')}
        onClick={() => { if (manuel) void passerAuto() }}
      >
        {t('Auto')}
      </button>
      <button
        type="button"
        className={`bh-facon-choix${manuel ? ' est-actif' : ''}`}
        aria-pressed={manuel}
        aria-label={t('Mode manuel')}
        disabled={lectureSeule || miseEnPlace}
        title={t('Le moteur se tait : tu joues à la main, comme sur OCTGN')}
        onClick={() => { if (!manuel) void passerManuel() }}
      >
        {t('Manuel')}
      </button>
      {refus ? <span className="bh-facon-refus" role="status">{refus}</span> : null}

      {fenetre ? (
        <div className="pile-triche-voile" onPointerDown={() => setFenetre(false)}>
          <section
            className="pile-triche choix-reprise"
            role="dialog"
            aria-label={t('On en est où ?')}
            style={transformDecalage(decalage)}
            onPointerDown={(evenement) => evenement.stopPropagation()}
          >
            <header className="pile-triche-entete">
              <h2
                className="poignee-glisser"
                onPointerDown={gestes.onPointerDown}
                onPointerMove={gestes.onPointerMove}
                onPointerUp={gestes.onPointerUp}
                onPointerCancel={gestes.onPointerCancel}
              >
                {t('On en est où ?')}
              </h2>
              <button type="button" onClick={() => setFenetre(false)}>{t('Annuler')}</button>
            </header>
            <p className="choix-reprise-aide">
              {t('Le moteur recalcule la table et reprend exactement là.')}
            </p>
            <ul className="choix-reprise-liste">
              {CHOIX.map((c) => (
                <li key={c.phase}>
                  <button type="button" onClick={() => { void choisir(c.phase) }}>
                    <strong>{t(c.titre)}</strong>
                    <span>{t(c.detail)}</span>
                  </button>
                </li>
              ))}
            </ul>
            {refus ? <p className="bh-facon-refus" role="status">{refus}</p> : null}
          </section>
        </div>
      ) : null}
    </span>
  )
}
