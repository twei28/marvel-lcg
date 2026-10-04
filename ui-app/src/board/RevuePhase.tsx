// « REVOIR LA PHASE DU MECHANT » (decision du 03/10/2026) : apres la phase, en
// lecture seule, dans le volet du journal (la console est abandonnee). La meme
// frise que le cartouche, tous les onglets passes ; un clic sur un onglet liste
// ses coups, un clic sur un coup en donne le detail. Rien ne part au moteur.

import { useState } from 'react'
import { avecBilan, type EtapeDeroule } from './deroule-phase'
import { ONGLETS, avecTempsVides, resumeOnglet, type CleOnglet } from './frise-phase'
import { DetailCoup, ListeDesCoups } from './DetailCoup'
import { etapeEnLangue } from './etape-en-langue'
import { t } from './langue'
import './deroule-onglets.css'

export function RevuePhase({
  etapes,
  pvMaxParNom,
  nomFr,
}: {
  /** Les etapes de la phase FINIE, telles qu'`etapesDeroule` les rend. */
  etapes: EtapeDeroule[]
  pvMaxParNom?: Map<string, number>
  /** Le nom francais d'une carte, comme dans le cartouche (board.tsx). */
  nomFr?: (id: number) => string | undefined
}) {
  const [choix, setChoix] = useState<{ temps: CleOnglet; cle?: string }>({ temps: 'bilan' })
  const toutes = avecBilan(avecTempsVides(etapes, true), pvMaxParNom).map((e) => etapeEnLangue(e, nomFr))
  if (toutes.length === 0) return null
  const duTemps = toutes.filter((e) => e.temps === choix.temps)
  const lue =
    (choix.cle !== undefined ? duTemps.find((e) => e.cle === choix.cle) : undefined) ??
    (duTemps.length === 1 ? duTemps[0] : undefined)
  return (
    <section className="deroule-phase est-revue" aria-label={t('Revoir la phase du méchant')}>
      <ol className="deroule-temps">
        {ONGLETS.map((onglet) => (
          <li key={onglet.cle} className={`est-passe${choix.temps === onglet.cle ? ' est-relu' : ''}`}>
            <button type="button" className="deroule-onglet-bouton" onClick={() => setChoix({ temps: onglet.cle })}>
              <span className="deroule-onglet-nom">{t(onglet.libelle)}</span>
              {onglet.cle === 'bilan' ? null : (
                <small className="deroule-onglet-resume">{resumeOnglet(toutes, onglet.cle)}</small>
              )}
            </button>
          </li>
        ))}
      </ol>
      {lue ? (
        <DetailCoup etape={lue} />
      ) : (
        <ListeDesCoups coups={duTemps} choisir={(cle) => setChoix({ temps: choix.temps, cle })} />
      )}
      {lue && duTemps.length > 1 ? (
        <div className="deroule-boutons">
          <button type="button" className="bh-bouton" onClick={() => setChoix({ temps: choix.temps })}>
            {t('Tous les coups')}
          </button>
        </div>
      ) : null}
    </section>
  )
}
