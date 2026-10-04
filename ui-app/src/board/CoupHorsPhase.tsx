// LE CARTOUCHE D'UN SEUL COUP, hors de la phase du mechant (decision du
// 03/10/2026). Pendant le tour d'un joueur, une attaque ou une manigance du
// mechant (une carte qui le fait frapper) ouvre le cartouche pour ce coup-la,
// puis « Continuer » le referme. Le moteur ne l'attend pas : il est purement
// informatif, et ne retient aucune trame.
//
// Les etapes viennent de `etapesHorsPhase` (deroule-phase.ts) ; les memes
// phrases que le cartouche de la phase (deroule-textes.ts).

import { useRef, useState } from 'react'
import type { EtapeDeroule } from './deroule-phase'
import { detailEtape, lignesEtoileBoost, texteActivationAnnulee, texteCauseActivation, titreEtape } from './deroule-textes'
import { t } from './langue'

export function CoupHorsPhase({
  etapes,
  ignorerLesPremiers = false,
}: {
  etapes: EtapeDeroule[]
  /**
   * Au chargement de la page, les coups DEJA dans le journal ont ete vus avant
   * le rechargement : on ne les remontre pas (board.tsx le passe a vrai).
   */
  ignorerLesPremiers?: boolean
}) {
  const vus = useRef<Set<string> | undefined>(undefined)
  if (vus.current === undefined) {
    vus.current = new Set(ignorerLesPremiers ? etapes.map((e) => e.cle) : [])
  }
  const [, redessiner] = useState(0)
  // Une annonce attend sa resolution : le coup n'a pas encore eu lieu, et la
  // question de defense passe par le panneau central comme d'habitude.
  const coup = etapes.find((e) => e.etat !== 'annonce' && !vus.current?.has(e.cle))
  if (!coup) return null
  const fermer = () => {
    vus.current?.add(coup.cle)
    redessiner((n) => n + 1)
  }
  const resultat = detailEtape(coup)
  const annulee = texteActivationAnnulee(coup)
  const cause = texteCauseActivation(coup)
  return (
    <section className="deroule-phase est-hors-phase" role="dialog" aria-label={t('Hors de la phase du méchant')}>
      <p className="deroule-surtitre">{t('Hors de la phase du méchant')}</p>
      <div className="deroule-entete">
        <p className="deroule-titre">{titreEtape(coup)}</p>
      </div>
      {resultat ? <p className="deroule-resultat">{resultat}</p> : null}
      {lignesEtoileBoost(coup).map((ligne) => (
        <p key={ligne} className="deroule-etoile">{ligne}</p>
      ))}
      {annulee ? <p className="deroule-annulee">{annulee}</p> : null}
      {cause ? <p className="deroule-cause">{cause}</p> : null}
      <div className="deroule-boutons">
        <button type="button" className="bh-bouton deroule-suivant" onClick={fermer}>
          {t('Continuer')}
        </button>
      </div>
    </section>
  )
}
