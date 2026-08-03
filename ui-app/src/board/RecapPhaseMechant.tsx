// Le bilan de la phase du méchant, en une fois.
//
// En mode rapide, la phase s'enchaîne sans s'arrêter : plus de présentation
// plein écran, plus de « Continue » à chaque activation. On ne voit donc plus
// passer ce qu'on a encaissé. Ce panneau le rejoue à la fin, groupé.
//
// Il ne réinvente rien : il relit les entrées que l'historique a déjà produites
// pendant la phase. Chaque entrée porte le round et la phase où elle est née,
// c'est tout ce qu'il faut pour les retrouver.

import { useEffect, useRef, useState } from 'react'
import type { EntreeHistorique } from './HistoriquePartie'
import { t } from './langue'
import type { World } from './world'

/**
 * Les étapes que le moteur appelle « phase du méchant ». Il n'a pas d'état
 * unique pour elle : il la découpe (voir game/world/phase.py, Phase.State).
 */
const PHASES_MECHANT = new Set([
  'Main Scheme Place Threat',
  'Enemy Activation',
  'Deal Encounter Cards',
  'Reveal Encounter Cards',
])

type Bilan = {
  cle: string
  round: number
  degats: EntreeHistorique[]
  menace: EntreeHistorique[]
  cartes: EntreeHistorique[]
}

function bilanDeLaPhase(entrees: EntreeHistorique[], round: number): Bilan | undefined {
  const dedans = entrees.filter((e) => e.round === round && PHASES_MECHANT.has(e.phase))
  // Ordre du jeu : l'historique empile les plus récentes en tête.
  const ordonnees = [...dedans].reverse()
  const degats = ordonnees.filter((e) => e.type === 'damage')
  const menace = ordonnees.filter((e) => e.type === 'threat')
  const cartes = ordonnees.filter((e) => e.type === 'card')
  if (degats.length + menace.length + cartes.length === 0) return undefined
  return { cle: `${round}`, round, degats, menace, cartes }
}

export function RecapPhaseMechant({
  entrees,
  monde,
  actif,
}: {
  entrees: EntreeHistorique[]
  monde: World | undefined
  actif: boolean
}) {
  const [bilan, setBilan] = useState<Bilan | undefined>(undefined)
  const phasePrecedente = useRef<string | undefined>(undefined)

  useEffect(() => {
    const phase = monde?.phase
    const avant = phasePrecedente.current
    phasePrecedente.current = phase

    if (!actif || phase === undefined || avant === undefined) return
    // On ne déclenche qu'à la SORTIE de la phase du méchant.
    if (!PHASES_MECHANT.has(avant) || PHASES_MECHANT.has(phase)) return
    setBilan(bilanDeLaPhase(entrees, monde?.round_id ?? 0))
  }, [monde?.phase, monde?.round_id, actif, entrees])

  if (!bilan) return null

  const section = (titre: string, liste: EntreeHistorique[]) =>
    liste.length === 0 ? null : (
      <section className="recap-mechant-groupe">
        <span className="plateau-eyebrow">{titre}</span>
        <ul>
          {liste.map((entree) => (
            <li key={entree.cle}>
              <b>{entree.titre}</b>
              {entree.detail ? <small>{entree.detail}</small> : null}
            </li>
          ))}
        </ul>
      </section>
    )

  return (
    <div className="recap-mechant" role="dialog" aria-label={t('Bilan de la phase du méchant')}>
      <div className="recap-mechant-carte">
        <header>
          <span className="plateau-eyebrow">{t('Phase du méchant')}</span>
          <strong>
            {t('Round')} {bilan.round}
          </strong>
        </header>

        {section(t('Dégâts'), bilan.degats)}
        {section(t('Menace'), bilan.menace)}
        {section(t('Révélé'), bilan.cartes)}

        <button type="button" className="recap-mechant-ok" onClick={() => setBilan(undefined)} autoFocus>
          {t('Continuer')}
        </button>
      </div>
    </div>
  )
}
