// RegarderDessus.tsx — « regarder les X cartes du dessus d'un deck », mode manuel.
//
// Demande du testeur (09/11/2026, Carquois de Hawkeye) : au jeu réel on regarde les 5 premières cartes
// d'un deck SANS les prendre en main ; l'ouverture complète de la pile (`PileTriche`) ne propose que
// « En main » / « Mettre en jeu ». Ici, rien ne bouge : c'est un REGARD, local à CE joueur (aucun état
// partagé avec les spectateurs, contrairement à la pile ouverte), et les cartes sont celles que le
// descripteur du monde donne déjà : aucun appel moteur.
//
// Ordre : `pile.cartes` va du fond vers le dessus (le dessus est la DERNIÈRE, voir `pilesParDessus`) ;
// on montre ici la carte du dessus en premier, numérotée 1.

import { scanUrl } from '../card-model'
import { t } from '../langue'
import type { WorldCard } from '../world'
import './RegarderDessus.css'

/** Le nombre demandé par défaut (« les 5 premières cartes du deck »). */
export const REGARD_PAR_DEFAUT = 5

/** Borne le nombre demandé entre 1 et la taille du deck ; un champ vidé ou absurde retombe sur le défaut. */
export function nombreARegarder(brut: number, tailleDuDeck: number): number {
  const voulu = Number.isFinite(brut) && brut >= 1 ? Math.floor(brut) : REGARD_PAR_DEFAUT
  return Math.max(1, Math.min(voulu, Math.max(1, tailleDuDeck)))
}

/** Les X cartes du dessus, la carte du dessus d'abord. Ne modifie pas `cartes`. */
export function cartesDuDessus(cartes: readonly WorldCard[], x: number): WorldCard[] {
  return cartes.slice(-nombreARegarder(x, cartes.length)).reverse()
}

type Props = {
  cartes: readonly WorldCard[]
  x: number
  onChangerX: (x: number) => void
  /** Revient à la pile entière. */
  onToutVoir: () => void
}

export function RegarderDessus({ cartes, x, onChangerX, onToutVoir }: Props) {
  const vues = cartesDuDessus(cartes, x)
  return (
    <div className="regarder-dessus">
      <div className="regarder-dessus-barre">
        <label>
          {t('Regarder les')}{' '}
          <input
            type="number"
            min={1}
            max={Math.max(1, cartes.length)}
            value={x}
            aria-label={t('Nombre de cartes à regarder')}
            onChange={(evenement) => onChangerX(evenement.target.valueAsNumber)}
          />{' '}
          {t('cartes du dessus')} <small>({vues.length}/{cartes.length})</small>
        </label>
        <span className="regarder-dessus-note">
          {t('Regard seul : rien n’est déplacé, aucune carte ne va en main.')}
        </span>
        <button type="button" onClick={onToutVoir}>{t('Voir toute la pile')}</button>
      </div>
      <div className="pile-triche-cartes">
        {vues.map((carte, rang) => (
          <span className="pile-triche-carte regarder-dessus-carte" key={`${carte.id}-${rang}`}>
            <small className="regarder-dessus-rang">{rang + 1}</small>
            <img src={scanUrl(carte.pic_id)} alt={carte.name} loading="lazy" />
          </span>
        ))}
      </div>
    </div>
  )
}
