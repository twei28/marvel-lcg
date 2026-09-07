// Le choix d'une cible DANS la scene du deroule detaille.
//
// Livraison D de la spec du 7 septembre 2026 : pendant la phase du mechant,
// quand le moteur fait choisir une cible ou un ordre (les deux sbires a
// activer), les candidats s'affichent ici en cartes, a la meme taille que les
// autres cartes de la scene, et se cliquent la. La table reste cliquable
// derriere (le voile ne capte pas les clics) : les deux chemins menent au
// meme `agir`.

import { ScanCard, type ScanCardProps } from '../components/ScanCard'
import { t } from './langue'
import { avecIcones, marquerRessources } from './icones-ressources'

export type CibleScene = {
  props: ScanCardProps
  choisie: boolean
  /** Combien de fois cette cible est prise, quand une cible compte plusieurs fois. */
  fois?: number
  agir?: () => void
}

export type CiblesSceneProps = {
  /** Le nom de l'action en cours, pour savoir ce qu'on choisit. */
  titre: string
  cibles: CibleScene[]
  choisies: number
  minimum: number
  maximum: number
  /** La reponse peut partir ; sinon `raison` dit ce qui manque. */
  prete: boolean
  raison: string
  valider: () => void
  annuler: () => void
}

export function CiblesScene({
  titre,
  cibles,
  choisies,
  minimum,
  maximum,
  prete,
  raison,
  valider,
  annuler,
}: CiblesSceneProps) {
  return (
    <div className="cibles-scene" role="group" aria-label={`${t('Cibles possibles :')} ${titre}`}>
      <div className="cibles-scene-entete">
        <span className="plateau-eyebrow">{t('Choisir la cible')}</span>
        <strong>{avecIcones(marquerRessources(titre))}</strong>
        {/* « 1 / 2 » : combien de cibles sont prises sur combien il en faut.
            Le minimum et le maximum ne s'ecrivent que s'ils different. */}
        <span className="cibles-scene-compte">
          {choisies} / {maximum}
          {minimum !== maximum ? ` (${t('min')} ${minimum})` : ''}
        </span>
      </div>
      {cibles.length > 0 ? (
        <div className="cibles-scene-cartes">
          {cibles.map((cible) => (
            <span key={cible.props.id} className="cibles-scene-carte">
              <ScanCard
                {...cible.props}
                state={cible.choisie ? 'selected' : 'targetable'}
                onSelect={cible.agir}
                spentCount={cible.fois}
                counters={undefined}
                schemeThreat={undefined}
                allyHp={undefined}
                stats={undefined}
                labelType={undefined}
                camp={undefined}
                masquerType
              />
            </span>
          ))}
        </div>
      ) : null}
      <div className="cibles-scene-boutons">
        {!prete && raison ? <span className="cibles-scene-raison">{raison}</span> : null}
        <button type="button" className="bh-bouton" onClick={annuler}>
          {t('Annuler')}
        </button>
        <button type="button" className="bh-bouton deroule-suivant" disabled={!prete} onClick={valider}>
          {t('Confirmer')}
        </button>
      </div>
    </div>
  )
}
